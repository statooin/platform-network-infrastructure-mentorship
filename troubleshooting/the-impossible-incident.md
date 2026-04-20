# Post-Mortem: The "Impossible" Incident

**Date:** 2026-03-15  
**Severity:** SEV-1  
**Impact:** 45 minutes of intermittent 502 Bad Gateway errors across all LLM inference endpoints.

## 1. Context & Architecture
Our infrastructure utilizes Envoy as an edge gateway routing incoming HTTPS traffic to a fleet of backend LLM inference pods (Python/FastAPI) running on GPU nodes. The infrastructure is robust, scaled dynamically, and network metrics (bandwidth, CPU, Memory) were well within safe thresholds during the incident.

## 2. The Anomaly
At 14:00 UTC, a sudden burst of parallel inference requests hit the API due to a newly released marketing campaign. 

- **Symptoms:** Envoy started returning `502 Bad Gateway` to 15% of client requests.
- **Initial Diagnostics:** 
  - Application logs showed zero errors. The FastAPI servers were completely unaware of the dropped requests.
  - CPU/Memory on both Envoy nodes and GPU workers were < 40%.
  - Network bandwidth was at 20% capacity.
- **The "Impossible" Element:** The load balancers claimed the backends were unhealthy, but the backends were perfectly healthy and largely idle.

## 3. Deep-Dive Debugging
Standard observability tools failed to identify the issue because the failure was occurring in the Linux kernel layer, bypassing the application entirely. 

### Step 1: Checking Kernel Logs
Running `dmesg -T` on the Envoy gateway nodes immediately revealed the true nature of the failure:
```
[Mon Mar 15 14:12:05 2026] nf_conntrack: nf_conntrack: table full, dropping packet
```

### Step 2: Validating Netfilter
Netfilter's connection tracking (`conntrack`) maintains a state table for all logical network connections. We checked the current count versus the maximum limit:
```bash
# Check maximum allowed
cat /proc/sys/net/netfilter/nf_conntrack_max
> 65536

# Check current usage
cat /proc/sys/net/netfilter/nf_conntrack_count
> 65536
```
The table was completely full. The kernel was indiscriminately dropping new TCP SYN packets because it could not track them. Envoy perceived this as a backend timeout and threw a 502.

### Step 3: Why was the table full?
We investigated the socket states using `ss -s`:
```
Total: 70000 (kernel 71000)
TCP:   68000 (estab 2000, closed 65000, orphaned 0, synrx 0, timewait 65000/0), ports 0
```
There were 65,000 sockets stuck in `TIME_WAIT`.

### Root Cause Analysis
The internal communication between Envoy and the Python inference pods was using **HTTP/1.1 without Keep-Alive**. 
Every single API request created a new TCP connection. Upon request completion, the connection was closed, entering the `TIME_WAIT` state for 60 seconds (kernel default) to ensure delayed packets were not misrouted. 

During the burst of traffic, Envoy generated over 65,000 unique connections in under a minute, instantly exhausting both the ephemeral port range and the `nf_conntrack` table.

## 4. The Permanent Fix

The fix required action at both the application and kernel layers.

### Application Layer (Envoy)
Configured Envoy's backend clusters to use HTTP/2 (which multiplexes requests over a single TCP connection) and enabled strict connection pooling/keep-alive for HTTP/1.1 fallbacks.

### Kernel Layer (Sysctl Tuning)
We updated our immutable infrastructure configuration to account for hyper-scale connection rates:

1. **Increase Conntrack Limit:** 
   ```bash
   sysctl -w net.netfilter.nf_conntrack_max=2000000
   ```
2. **Expand Ephemeral Ports:**
   ```bash
   sysctl -w net.ipv4.ip_local_port_range="1024 65535"
   ```
3. **Aggressive TIME_WAIT Re-use:**
   ```bash
   sysctl -w net.ipv4.tcp_tw_reuse=1
   ```

## 5. Lessons Learned
"The network is reliable" is a fallacy. Application developers assume if they write an API, it will receive the data. Senior Site Reliability Engineers know that every single request must traverse a gauntlet of kernel buffers, queues, and state tables. Observability must extend into `eBPF` and kernel-space, not just application APMs.