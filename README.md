# Platform Network Infrastructure Mentorship

[![Ubuntu](https://img.shields.io/badge/Ubuntu_24.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)
[![Debian](https://img.shields.io/badge/Debian_12-A81D33?style=for-the-badge&logo=debian&logoColor=white)](https://www.debian.org/)
[![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Envoy](https://img.shields.io/badge/Envoy_Proxy-E459B5?style=for-the-badge&logo=envoyproxy&logoColor=white)](https://www.envoyproxy.io/)

## 🚀 Philosophy
Network reliability and security are the backbone of Distributed AI and LLM inference clusters. In an era where GPU hours dictate business survival, a dropped packet is no longer just a transient failure—it is a measurable degradation in inference latency, throughput, and ultimately, ROI. Modern Site Reliability Engineering demands we move beyond basic connectivity. We must architect systems where the network is intrinsically aware of its workloads, securely segmenting multi-tenant data while providing microsecond-level predictability for RDMA and parameter synchronization traffic.

This repository is designed not just to train engineers, but to forge true Systems Architects. It is an end-to-end framework that bridges the gap between traditional network administration and hyper-scale DevSecOps paradigms.

## 🛠️ Tech Stack
Our approach relies on a battle-tested, high-performance open-source stack:
- **Ubuntu/Debian:** The bedrock of our bare-metal and containerized compute nodes.
- **BIND9:** Foundation for deep DNS architectures, ensuring resilient internal service discovery.
- **eBPF & Cilium:** Providing identity-based network security, Layer 7 observability, and zero-trust policies with kernel-level performance.
- **Envoy:** The edge and service proxy layer handling dynamic request routing, TLS termination, and rate limiting.
- **Terraform:** Immutable infrastructure as code (IaC) defining the entirety of our network topology.

## 📚 Table of Contents
1. [Syllabus & Progression Mapping](./SYLLABUS.md)
2. [Kernel Tuning for AI Workloads](./scripts/kernel-ai-perf-tuner.sh)
3. [eBPF Observability Toolkit](./labs/ebpf-observability-toolkit.md)
4. [Infrastructure Topology (Terraform)](./infra/topology-bootstrap.tf)
5. [Zero Trust Architecture](./docs/zero-trust-architecture.mermaid)
6. [Automated Security Auditing](./security/hardening-cis-audit.py)
7. [Incident Post-Mortem: The Impossible Incident](./troubleshooting/the-impossible-incident.md)
8. [Mentee Assessment Checklist](./ASSESSMENT_CHECKLIST.md)
9. [Contribution Guidelines](./CONTRIBUTING.md)

## 🤝 Mentorship Assessment

If you are participating in the mentorship program or using this framework for self-evaluation, refer to the [Assessment Checklist](./assessment-checklist.md) to validate your comprehension of senior-level architectural and systems engineering concepts.

---
*Developed for the next generation of SREs and Platform Architects.*
