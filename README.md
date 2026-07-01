# TradingAgents

**A trading floor of LLM agents that debate every trade before it fires.**

<!-- hero: 1600x600 diagram of the analyst -> researcher -> trader -> risk pipeline -->

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/powered_by-LangGraph-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

A multi-agent LLM framework for financial analysis. Fundamental, news, sentiment, and technical analysts each write a report; a bull and a bear researcher debate; a trader synthesises; a three-analyst risk team argues position sizing; a portfolio manager renders the final Buy/Overweight/Hold/Underweight/Sell.

---

## Why this exists

Solo trader-agents lie confidently. The LLM tells you "buy AAPL", but you don't know what part of that came from real data and what came from the model bluffing. TradingAgents forces disagreement — separate agents with separate contexts, an adversarial bull/bear stage, and an audit trail of who said what. The final signal is the output of a debate, not a monologue.

---

## Try it in 60 seconds

```bash
git clone https://github.com/Danush-Aries/TradingAgents
cd TradingAgents
pip install -r requirements.txt

export OPENAI_API_KEY=sk-...
python main.py --ticker AAPL --date 2025-12-31
```

Analyst reports and the full debate transcript land in `./results/`. Persistent memory means agents accumulate outcomes across runs.

---

## How it works

```
ticker + date
      |
      v
+-- Analyst team -----------------+
|  market   (technicals)          |
|  social   (sentiment)           |
|  news     (macro + company)     |
|  fund     (earnings + ratios)   |
+---------------|-----------------+
                v
+-- Research team ----------------+
|  bull researcher  <---debate--> |
|  bear researcher                |
|  research manager  ->  thesis   |
+---------------|-----------------+
                v
+-- Trader -----------------------+
|  synth reports -> trade plan    |
+---------------|-----------------+
                v
+-- Risk team --------------------+
|  aggressive / neutral / cons.   |
|  debate position sizing         |
+---------------|-----------------+
                v
+-- Portfolio manager ------------+
|  Buy / Overweight / Hold /      |
|  Underweight / Sell             |
+---------------------------------+
```

Every message logged. Every decision reviewable.

---

## Screenshots

<!-- screenshot: agent-graph.png -->
<!-- screenshot: debate-transcript.png -->
<!-- screenshot: final-signal.png -->

---

## Stack

| Layer | Tech |
|---|---|
| Orchestration | LangGraph |
| Memory | persistent trade-outcome log |
| CLI | Rich + Typer |
| Config | pyproject.toml + `uv` |
| Tests | pytest |

---

## More from Danush

Part of a broader stack of AI + security tooling:

- [jarvis](https://github.com/Danush-Aries/jarvis) — portable multi-provider AI assistant (voice/web/CLI)
- [breachintel](https://github.com/Danush-Aries/breachintel) — OSINT breach intelligence aggregator
- [cve-advisor](https://github.com/Danush-Aries/cve-advisor) — AI-powered CVE triage and patch recommendation
- [llm-fragility-lab](https://github.com/Danush-Aries/llm-fragility-lab) — adversarial testing lab for LLM robustness
- [network-intrusion-analyzer](https://github.com/Danush-Aries/network-intrusion-analyzer) — Suricata + Claude AI intrusion triage
- [autonomous-coding-agent](https://github.com/Danush-Aries/autonomous-coding-agent) — two-agent autonomous coding system

Built by [Dhanush](https://github.com/Danush-Aries) — AI engineering + cybersecurity.

## License

MIT.
