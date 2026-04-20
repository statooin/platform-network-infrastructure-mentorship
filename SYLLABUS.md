# Network Infrastructure & DevSecOps Syllabus

This 10-module progression is designed to transition an engineer from foundational operational tasks to architecting robust, AI-ready network infrastructure. 

| Module | Junior/Mid Task | Senior SRE / AI-Ops Outcome |
|---|---|---|
| **01 - Networking** | Configure static IPs, VLANs, and basic iptables rules. | Design BGP-based Anycast architectures for multi-region LLM API routing with dynamic anycast convergence and automated DDoS mitigation. |
| **02 - DNS** | Install and configure BIND9/CoreDNS for local domain resolution. | Architect a split-horizon DNS infrastructure with DNSSEC and global server load balancing (GSLB) optimized for multi-cloud inference endpoints. |
| **03 - Email** | Deploy Postfix and configure basic SMTP relay. | Implement strict DMARC, SPF, and DKIM architectures to ensure automated AI reporting and alert pipelines bypass carrier spam filters without fail. |
| **04 - HTTP** | Set up Nginx/Apache to serve static content with basic SSL. | Deploy and tune Envoy/WASM gateways for complex L7 routing, intelligent retries, and rate limiting tailored to gRPC-based LLM inference APIs. |
| **05 - FS Access** | Mount NFS/SMB shares with standard user permissions. | Architect parallel distributed file systems (e.g., Ceph/Lustre) with RDMA over Converged Ethernet (RoCE) for high-bandwidth AI model weight distribution. |
| **06 - Auth** | Configure PAM and set up basic LDAP/Active Directory integration. | Design a comprehensive Zero Trust Network using SPIFFE/SPIRE for workload identity and mTLS for all inter-microservice communication. |
| **07 - Security Basics** | Implement basic UFW firewalls and run vulnerability scanners. | Write strict, kernel-enforced eBPF/Cilium network policies implementing micro-segmentation for multi-tenant machine learning training clusters. |
| **08 - Diagnostics** | Troubleshoot connectivity using `ping`, `traceroute`, and `tcpdump`. | Utilize deep eBPF observability tools (`bpftrace`, `bcc`) to root-cause microsecond tail latencies and kernel-level packet drops in GPU interconnects. |
| **09 - Data Integrity** | Configure regular backups and monitor RAID arrays. | Implement immutable infrastructure paradigms and cryptographic attestation to guarantee the supply chain integrity of deployed foundational models. |
| **10 - Service Security** | Apply CIS benchmarks manually and respond to basic alerts. | Automate continuous compliance and chaos engineering pipelines to proactively validate the resilience of inference APIs against volumetric attacks. |