#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# Kernel Network Tuner for AI Workloads (Inference & RDMA)
# ==============================================================================
# This script applies aggressive network sysctl tuning optimized for high-throughput,
# low-latency environments such as massive concurrent LLM API connections and 
# GPU-to-GPU parameter synchronization.
#
# Must be run as root.
# ==============================================================================

if [[ "$EUID" -ne 0 ]]; then
  echo "ERROR: This script must be run as root." >&2
  exit 1
fi

echo ">> Tuning Linux Network Stack for AI / Inference Workloads..."

# 1. Congestion Control & Queueing
# BBR (Bottleneck Bandwidth and Round-trip propagation time) significantly improves
# throughput and reduces latency for high-bandwidth links, critical for RDMA and large model transfers.
# fq (Fair Queueing) is required for BBR to operate correctly.
sysctl -w net.core.default_qdisc=fq
sysctl -w net.ipv4.tcp_congestion_control=bbr

# 2. Connection Tracking & Ephemeral Ports
# High-concurrency LLM inference APIs quickly exhaust ephemeral ports and conntrack tables.
# We expand the ephemeral port range and increase the conntrack maximum.
sysctl -w net.ipv4.ip_local_port_range="1024 65535"
sysctl -w net.netfilter.nf_conntrack_max=2000000

# 3. Socket Buffers & Window Scaling
# AI model weights are large. Maximize socket buffer sizes to allow for massive
# inflight data without application-level blocking. (Values up to 16MB/32MB).
sysctl -w net.core.rmem_max=33554432
sysctl -w net.core.wmem_max=33554432
sysctl -w net.ipv4.tcp_rmem="4096 87380 33554432"
sysctl -w net.ipv4.tcp_wmem="4096 65536 33554432"
sysctl -w net.ipv4.tcp_window_scaling=1

# 4. Connection Backlog & SYN Handling
# Bursty inference requests (e.g., flash traffic during an event) will fill the SYN backlog.
# We increase somaxconn and the SYN backlog to prevent silent packet drops.
sysctl -w net.core.somaxconn=65535
sysctl -w net.ipv4.tcp_max_syn_backlog=65535
sysctl -w net.core.netdev_max_backlog=65535

# 5. Keepalive & TIME_WAIT Handling
# Reusing TIME_WAIT sockets is crucial when sitting behind load balancers/Envoy proxies.
# Reduce keepalive time to detect dead peers faster (important for GPU interconnect failure detection).
sysctl -w net.ipv4.tcp_tw_reuse=1
sysctl -w net.ipv4.tcp_keepalive_time=600
sysctl -w net.ipv4.tcp_keepalive_intvl=60
sysctl -w net.ipv4.tcp_keepalive_probes=5
sysctl -w net.ipv4.tcp_fin_timeout=15

echo ">> Applying changes to sysctl runtime..."
sysctl -p

echo ">> Tuning complete. Verification:"
sysctl net.ipv4.tcp_congestion_control
sysctl net.core.somaxconn

exit 0