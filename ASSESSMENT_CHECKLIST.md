# Network Mentorship Assessment Checklist

This rubric is utilized to evaluate mentees graduating from the Network Infrastructure & DevSecOps curriculum. A passing grade requires a demonstration of architectural maturity, focusing on failure domains, observability, and deterministic security.

## 1. Idempotency & Automation
- [ ] **Infrastructure as Code:** All infrastructure is defined in Terraform. The mentee can run `terraform apply` twice consecutively with the second run showing `0 added, 0 changed, 0 destroyed`.
- [ ] **Configuration Management:** Server configurations (e.g., sysctl, BIND9, Envoy) are automated via Ansible/Cloud-Init without manual SSH interventions.
- [ ] **Interview Question:** "Explain the blast radius of manual iptables rules versus an IaC-managed Cilium Network Policy."

## 2. Security by Default (Zero Trust)
- [ ] **Micro-segmentation:** Can demonstrate that inter-pod or inter-VM communication is dropped by default and explicitly allowed via mTLS-backed identities.
- [ ] **Kernel Hardening:** Demonstrates proper execution of CIS benchmark audits, ensuring unused protocols (IPv6 if not needed, ICMP redirects) are disabled.
- [ ] **Interview Question:** "Explain the difference between an iptables `ACCEPT` rule at Layer 4 and a Cilium Network Policy at Layer 7."
  - *Expected Answer:* L4 just checks IP/Port. L7 eBPF policies can validate HTTP paths, gRPC methods, or specific Kafka topics, tying identity to the workload rather than a transient IP address.

## 3. Observability & Debugging
- [ ] **eBPF Utilization:** Mentee can write or execute a `bpftrace` script to find silent TCP drops or conntrack exhaustion without relying on application logs.
- [ ] **Metrics:** Envoy telemetry is correctly scraped by Prometheus, displaying P50, P90, and P99 latency histograms for inference endpoints.
- [ ] **Interview Question:** "If an application returns a 502 Bad Gateway under load but CPU and Memory are at 20%, what three kernel parameters do you check first?"
  - *Expected Answer:* `nf_conntrack_count`, `somaxconn` (listen backlog), and ephemeral port exhaustion.

## 4. Performance & Scalability
- [ ] **Throughput Optimization:** System utilizes BBR congestion control and proper `rmem/wmem` scaling for high-bandwidth model weights.
- [ ] **Load Balancing Architecture:** Demonstrates understanding of Anycast DNS and how to route requests dynamically based on region or endpoint health.
- [ ] **Interview Question:** "Why is BBR superior to CUBIC for long-fat networks (LFN) typical in cross-region GPU parameter synchronization?"
  - *Expected Answer:* CUBIC reacts to packet loss (which occurs frequently in LFNs due to buffer bloat), slashing throughput. BBR models the actual bottleneck bandwidth and round-trip time, maintaining high throughput even with minor packet loss.