# eBPF Observability Toolkit: Deep Packet Inspection

## Scenario Overview
Your alerting systems are firing. The Envoy Gateway is reporting elevated P99 latencies (500ms+) when routing requests from the Application Backend to the internal Vector Database (Milvus/Qdrant) during a massive data ingestion phase. Standard `ping` shows 1ms latency, and `top` shows 30% CPU. Traditional tools are failing you. 

As a Senior SRE, you know that microbursts are likely causing socket-level drops or TCP retransmissions that `top` and `ping` cannot see. We will use `bpftrace` to hook directly into the Linux kernel and observe the exact behavior of the network stack.

## Prerequisites
- Ubuntu 22.04 LTS or newer
- Kernel 5.15+ (compiled with `CONFIG_BPF_SYSCALL=y`)
- `bpftrace` installed (`apt install bpftrace`)

## Lab 1: Tracking TCP Retransmissions

When a vector database gets overwhelmed, it might stop ACKing packets, forcing the sender to retransmit. `bpftrace` can trace the `tcp_retransmit_skb` kernel function.

### The One-Liner
```bash
sudo bpftrace -e 'kprobe:tcp_retransmit_skb { printf("Retransmit detected! PID: %d, Comm: %s\n", pid, comm); }'
```

### Advanced Script: `tcp_retrans_monitor.bt`
For a more detailed view including IPs and ports, save this to `tcp_retrans_monitor.bt` and run `sudo bpftrace tcp_retrans_monitor.bt`:

```c
#include <linux/socket.h>
#include <net/sock.h>

kprobe:tcp_retransmit_skb
{
    $sk = (struct sock *)arg0;
    $inet_family = $sk->__sk_common.skc_family;

    if ($inet_family == AF_INET || $inet_family == AF_INET6) {
        $daddr = $sk->__sk_common.skc_daddr;
        $dport = $sk->__sk_common.skc_dport;
        
        // dport is in network byte order; swap it
        $dport_host = ($dport >> 8) | (($dport & 0xff) << 8);

        printf("Time: %s | TCP Retransmission | PID: %d | Comm: %s | Dest IP: %s | Dest Port: %d\n",
               strftime("%H:%M:%S", nsecs), pid, comm, ntop($daddr), $dport_host);
    }
}
```
*How to Read the Output:* If you see bursts of retransmissions pointing to port 19530 (Milvus) originating from your ingestion microservice, you know the vector DB network buffers are saturated, not the application CPU.

## Lab 2: Detecting Kernel-Level Packet Drops

If the SYN backlog (`net.ipv4.tcp_max_syn_backlog`) is exceeded, the kernel silently drops packets. `bpftrace` can reveal this by tracing `kfree_skb`.

### The One-Liner
```bash
sudo bpftrace -e 'kprobe:kfree_skb /comm == "envoy"/ { @drops = count(); } interval:s:1 { print(@drops); clear(@drops); }'
```

### Explanation
This script attaches a probe to the `kfree_skb` kernel function (where socket buffers are freed/dropped). It filters by the `envoy` command. Every second, it prints the number of dropped packets. If this number spikes concurrently with your P99 latency alerts, you have proven that Envoy's listener backlog is dropping connections before they ever reach the application layer.

## Conclusion
By bypassing abstraction layers and querying the kernel directly, you have moved from guessing to mathematical certainty. This is the difference between a Junior SysAdmin randomly rebooting services and a Staff SRE surgically tuning `somaxconn`.