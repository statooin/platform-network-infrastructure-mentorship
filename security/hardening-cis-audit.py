#!/usr/bin/env python3
"""
Automated CIS Benchmark Network Security Audit
--------------------------------------------
This script performs a localized audit of Linux network security configurations
based on Center for Internet Security (CIS) benchmarks. It strictly uses built-in
libraries to ensure portability across hardened minimal environments.
"""

import os
import subprocess
import re
import sys

# Terminal Colors
class Colors:
    PASS = '\033[92m'
    FAIL = '\033[91m'
    WARN = '\033[93m'
    INFO = '\033[94m'
    ENDC = '\033[0m'

def print_result(check_name, status, details=""):
    if status == "PASS":
        print(f"{Colors.PASS}[PASS]{Colors.ENDC} {check_name}: {details}")
    elif status == "FAIL":
        print(f"{Colors.FAIL}[FAIL]{Colors.ENDC} {check_name}: {details}")
    else:
        print(f"{Colors.WARN}[WARN]{Colors.ENDC} {check_name}: {details}")

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except Exception as e:
        return ""

def check_root_ssh():
    """CIS 5.2.14 Ensure SSH PermitRootLogin is disabled"""
    sshd_config = "/etc/ssh/sshd_config"
    if not os.path.exists(sshd_config):
        print_result("SSH Root Login", "WARN", f"{sshd_config} not found.")
        return

    with open(sshd_config, 'r') as f:
        config_data = f.read()
    
    # Look for active PermitRootLogin no
    match = re.search(r'^\s*PermitRootLogin\s+no\b', config_data, re.MULTILINE)
    if match:
        print_result("SSH Root Login", "PASS", "PermitRootLogin is set to 'no'")
    else:
        print_result("SSH Root Login", "FAIL", "PermitRootLogin is NOT explicitly disabled in sshd_config")

def check_ipv4_forwarding():
    """CIS 3.1.1 Ensure IP forwarding is disabled (unless acting as a router)"""
    val = run_command("sysctl net.ipv4.ip_forward")
    if "net.ipv4.ip_forward = 0" in val:
        print_result("IPv4 Forwarding", "PASS", "IP forwarding is disabled.")
    else:
        print_result("IPv4 Forwarding", "FAIL", f"IP forwarding is enabled: {val}")

def check_icmp_redirects():
    """CIS 3.2.2 Ensure ICMP redirects are not accepted"""
    val = run_command("sysctl net.ipv4.conf.all.accept_redirects")
    if "net.ipv4.conf.all.accept_redirects = 0" in val:
        print_result("ICMP Redirects", "PASS", "ICMP redirects are disabled.")
    else:
        print_result("ICMP Redirects", "FAIL", "ICMP redirects are accepted. Vulnerable to MITM routing attacks.")

def check_unencrypted_services():
    """Check for commonly exploited unencrypted protocols listening on local ports (Telnet, FTP)"""
    ss_output = run_command("ss -lnt")
    
    # Default ports for Telnet (23) and FTP (21)
    unencrypted_ports = [21, 23]
    failures = []

    for port in unencrypted_ports:
        # Match exactly the port number after a colon
        if re.search(rf':{port}\b', ss_output):
            failures.append(str(port))

    if not failures:
        print_result("Unencrypted Services", "PASS", "No listening services detected on ports 21 or 23.")
    else:
        print_result("Unencrypted Services", "FAIL", f"Unencrypted protocols listening on ports: {', '.join(failures)}")

def main():
    if os.geteuid() != 0:
        print(f"{Colors.FAIL}ERROR:{Colors.ENDC} This audit script must be run as root.")
        sys.exit(1)

    print(f"{Colors.INFO}=== Starting CIS Network Security Audit ==={Colors.ENDC}\n")
    check_root_ssh()
    check_ipv4_forwarding()
    check_icmp_redirects()
    check_unencrypted_services()
    print(f"\n{Colors.INFO}=== Audit Complete ==={Colors.ENDC}")

if __name__ == "__main__":
    main()