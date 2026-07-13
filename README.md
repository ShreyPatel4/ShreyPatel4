# Hi, I’m Shrey Patel 👋

I build systems that are production-oriented, performance-driven, and reproducible — from low-latency C++ engines and paravirtual drivers to Python ML/automation tooling, tenant-fair LLM inference, and distributed control planes.

- 🔭 Current work: founding **[Coconut Labs](https://github.com/coconut-labs)** — tenant-fair LLM inference orchestration ([kvwarden](https://github.com/coconut-labs/kvwarden)), observability, and Generative AI engineering
- 🌱 Interested in: systems, distributed control planes, low-latency trading infra, tooling, and ML for system observability
- ⚡ Fun: game QA automation, synthetic data & logs, and hardware-accelerated I/O

## Recent Highlights — Last 2 Months (Mar–May 2026)

- **Founded [Coconut Labs](https://github.com/coconut-labs)** — independent inference research lab at [coconutlabs.org](https://coconutlabs.org). Shipped org profile, landing page ([ccocnutlabs-LP](https://github.com/coconut-labs/ccocnutlabs-LP)), 4-dot brand mark, and contact / newsletter rebrand off the kvwarden domain.
- **Launched [kvwarden](https://github.com/coconut-labs/kvwarden) v0.1.1 → v0.1.3** — tenant-fair LLM inference orchestration on a single GPU (no Kubernetes). Renamed from InferGrid and ran a multi-gate fairness ladder on H100 / A100 with vLLM and SGLang covering Llama-3.1-70B (TP=4), Mixtral-8x7B MoE, and mixed prompt-length distributions. Highlights:
  - DRR-priority admission with per-tenant token-bucket rate limiting (closed a 523× starvation gap to baseline).
  - Per-tenant TTFT histograms, fairness Grafana dashboard, opt-in anonymous telemetry receiver on Cloudflare Workers.
  - Streaming router fixes (admission-slot lifetime, real TTFT, max-stream-duration fence), interactive CLI + `doctor` + man pages.
  - Show HN launch with one-pager, FAQ, pitch, and architecture overview.
- **kvwarden — Gate 3 / T2 (cache-pressure admission)** — RFC + KV-eviction config + runbook, T2 admission test skeleton, `TenantPolicy` + `tenant_id` surface stub, M4 bench harness flags (`--prefix-overlap`, `--bias-flooder-cost`), py3.13 CI, and a one-command Docker Compose eval bundle.
- **`Minierva-SEPA`** *(private)* — algorithmic SEPA (Specific Entry Point Analysis) for Indian markets: NIFTY-500 screener with VCP detection, IBD-weighted RS percentile, 7-level exit hierarchy, walk-forward backtesting, TradingView Pine export.
- **`mlxd`** *(private)* — research + strategy docs for tenant-fair LLM inference on Apple Silicon (pre-product).
- **[solution_SnowConvertAI_final](https://github.com/ShreyPatel4/solution_SnowConvertAI_final)** — SQL Server → Snowflake migration take-home with a verification harness and head-to-head comparison vs. SnowConvert AI.
- **[SP-K8s-Control-Panel-Using-Streamlit](https://github.com/ShreyPatel4/SP-K8s-Control-Panel-Using-Streamlit)** — Streamlit-based Kubernetes control panel for deployment scaling and pod operations.
- **[dream_team](https://github.com/ShreyPatel4/dream_team)** — a 31-agent engineering organization running as a daemon, forking OpenClaw as the gateway/UI layer (Slack / Discord / Telegram bridges, web dashboard) with per-agent identity files (`SOUL.md`, `AGENTS.md`).
- **[risk-hotpath-hft](https://github.com/ShreyPatel4/risk-hotpath-hft)** — overlay analytics + reporting with audit/compliance, local-first with optional cloud switches.

## Spotlight Projects

- kvwarden — Tenant-fair LLM inference orchestration on a single GPU. No Kubernetes.
  https://github.com/coconut-labs/kvwarden

- UI-State-DOM-Capture-Multi-Agent — Modular, scalable Python-based UI state capture agent designed to automate and document user flows in web applications.
  https://github.com/ShreyPatel4/UI-State-DOM-Capture-Multi-Agent

- stage-0 — One canonical Stage-0 exactly as 2016-era Notion would have shipped, broken down into the smallest grain.
  https://github.com/ShreyPatel4/stage-0

- OpenPlay_Tester — Autonomous QA agent for a tiny Godot game with full data pipelines, RL/IL play, video anomaly detection, OOD checks, and an LLM triage assistant.
  https://github.com/ShreyPatel4/OpenPlay_Tester

- FastLane_NVMe — Paravirtual NVMe with RDMA and FPGA-ready hooks (Rust systems & drivers).
  https://github.com/ShreyPatel4/FastLane_NVMe

- Adaptive-Market-Microstructure-Intelligence-System-AMMIS — Real-time pipeline and ML engine that ingests live tick data and delivers deterministic-latency C++ signals.
  https://github.com/ShreyPatel4/Adaptive-Market-Microstructure-Intelligence-System-AMMIS-

- ArcBridge — Hybrid resource projection & extension platform for managing many Kubernetes clusters and projecting their state into a central control plane.
  https://github.com/ShreyPatel4/ArcBridge-Hybrid-Resource-Projection-and-Extension-Platform

- hyper-realistic-synthetic-logs-generator — Minimal, extensible framework to generate hyper-realistic synthetic logs and metrics with configurable characteristics.
  https://github.com/ShreyPatel4/hyper-realistic-synthetic-logs-generator

- risk-hotpath-hft — Overlay analytics and reporting with strong audit/compliance features; local-first with optional cloud switches.
  https://github.com/ShreyPatel4/risk-hotpath-hft

(Additional repos: Data-Kitchen — A brewing hot product idea)

## Repo of the week
<!-- REPO_OF_WEEK_START -->
### Repo of the week

- **[ShreyPatel4/OpenPlay_Tester](https://github.com/ShreyPatel4/OpenPlay_Tester)**
<!-- REPO_OF_WEEK_END -->

## What I built this week
<!-- BUILT_THIS_WEEK_START -->
_Nothing added to the journal yet._
<!-- BUILT_THIS_WEEK_END -->

## Latest blog / RSS
<!-- RSS_START -->
_RSS not configured._
<!-- RSS_END -->

## Now coding
<!-- NOW_CODING_START -->
[184ebb2](https://github.com/ShreyPatel4/ShreyPatel4/commit/184ebb214d90effea3aea58463c7512c1d688dbe) - chore: update README (repo-of-week & journal) (by github-actions[bot])
<!-- NOW_CODING_END -->

## Languages & Tech Highlights
Based on public repositories:
- Python, Rust, Go, C/C++, GDScript
- LLM inference & serving: vLLM, SGLang, tenant-fair scheduling (DRR + token-bucket), per-tenant TTFT/Grafana telemetry
- Systems engineering: low-latency C++ pipelines, Rust drivers, paravirtual devices
- Automation & tooling: Python agents, synthetic data, QA automation
- Cloud & infra: Kubernetes, observability, CI/CD, Cloudflare Workers

## How to collaborate
Open to collaborations, contract work, and speaking about systems & infra. Best contact: patelshrey77@gmail.com

## License
This profile README is available under CC0 — reuse as you like.
