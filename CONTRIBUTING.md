# Contribution Guidelines

As an elite engineering organization, we treat our documentation, infrastructure as code, and tooling with the same rigor as our Tier 1 production services. 

## Git Workflow & Conventional Commits

We strictly adhere to [Conventional Commits](https://www.conventionalcommits.org/). Every commit message must be structured as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Allowed Types:
- `feat`: A new feature (e.g., adding a new script or Terraform module)
- `fix`: A bug fix (e.g., resolving a failing sysctl parameter)
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools and libraries

### Example:
```
perf(kernel): optimize tcp_bbr for inference workloads

Increased net.ipv4.tcp_max_syn_backlog to prevent SYN drops
during high-concurrency LLM bursts.
```

## Pull Request Requirements

1. **No Drafts Without Context**: All PRs must have a clear description of the problem being solved.
2. **Benchmark Proofs**: Any pull request that modifies performance tuning (e.g., sysctl changes, proxy configurations) **must** include statistical evidence (e.g., a baseline and a post-change flamegraph, `iperf3` metrics, or `bpftrace` histograms).
3. **Security by Default**: Infrastructure changes must pass strict local validation (`terraform validate`, `tflint`, `tfsec`).
4. **Idempotency**: All scripts and IaC must be strictly idempotent. Running them twice should not result in errors or duplicated configurations.

## Documentation Standard
- Avoid colloquialisms; maintain an authoritative, technical tone.
- Do not use placeholders like "TODO". If it is incomplete, do not merge it.
- All diagrams must be provided as raw code (e.g., Mermaid.js) to ensure they can be version controlled and updated seamlessly.