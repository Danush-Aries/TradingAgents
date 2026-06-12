# TradingAgents

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![LangGraph](https://img.shields.io/badge/powered%20by-LangGraph-orange)](https://github.com/langchain-ai/langgraph)

**TradingAgents** is a multi-agent LLM framework for financial trading analysis. It deploys a coordinated team of specialized AI agents — fundamental analysts, news analysts, sentiment analysts, technical analysts, bull/bear researchers, a trader, and a risk management team — that collaboratively evaluate market conditions and produce a structured trading decision through structured debates and independent analysis.

---

## What It Does

TradingAgents runs a full investment analysis pipeline for any ticker symbol and date:

1. **Analyst Team** — Four independent agents each produce a specialist report:
   - *Market Analyst*: price action and technical indicators
   - *Social Media Analyst*: public sentiment and social signals
   - *News Analyst*: macro and company-specific news
   - *Fundamentals Analyst*: earnings, balance sheet, and financial ratios

2. **Research Team** — A bull and bear researcher debate investment merits; a research manager adjudicates and produces an investment recommendation.

3. **Trader** — Synthesises all reports into a concrete trading plan.

4. **Risk Management** — Three risk analysts (aggressive, conservative, neutral) debate position sizing and downside protection.

5. **Portfolio Manager** — Renders the final five-tier trading signal: `Buy / Overweight / Hold / Underweight / Sell`.

Decision logs, analyst reports, and debate transcripts are saved to disk for auditability. A persistent memory log accumulates outcomes over time so agents can learn from past decisions.

---

## Features

- **Multi-agent pipeline** built on [LangGraph](https://github.com/langchain-ai/langgraph) with structured state management
- **Bull/bear research debates** with a configurable number of rounds
- **Structured risk debate** with aggressive, neutral, and conservative perspectives
- **9 LLM providers**: OpenAI, Anthropic, Google Gemini, xAI Grok, DeepSeek, Qwen, GLM, Ollama (local), Azure OpenAI
- **2 data backends**: [yfinance](https://github.com/ranaroussi/yfinance) (no API key needed) and [Alpha Vantage](https://www.alphavantage.co/)
- **Per-vendor fallback**: if the primary data vendor hits a rate limit, the framework automatically falls back to the next available vendor
- **Checkpoint/resume**: LangGraph SQLite checkpointer lets a crashed run resume from the last completed node
- **Persistent trading memory**: decisions are logged and linked to future outcomes for reflective learning
- **Interactive CLI** with a live Rich dashboard showing agent progress, tool calls, and reports in real time
- **Programmatic Python API** for backtesting, batch runs, and integration into larger workflows
- **Output language selection**: analyst reports can be rendered in any language while internal reasoning stays in English

---

## Installation

**Requirements**: Python 3.10+

```bash
# Clone the repository
git clone https://github.com/your-org/TradingAgents.git
cd TradingAgents

# Install with pip (recommended)
pip install .

# Or install in editable mode for development
pip install -e .
```

### API Keys

Copy `.env.example` to `.env` and fill in the keys for the providers you plan to use:

```bash
cp .env.example .env
```

The **default data vendor is yfinance** — no API key is required to get started. Only set the keys you actually need:

```dotenv
# Required for OpenAI models (default provider)
OPENAI_API_KEY=sk-...

# Optional — other LLM providers
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
XAI_API_KEY=

# Optional — Alpha Vantage data (yfinance works without a key)
ALPHA_VANTAGE_API_KEY=
```

---

## Quick Start

### Python API

```python
from dotenv import load_dotenv
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

load_dotenv()

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"
config["deep_think_llm"] = "gpt-4.1"
config["quick_think_llm"] = "gpt-4.1-mini"
config["max_debate_rounds"] = 1

ta = TradingAgentsGraph(debug=True, config=config)
final_state, decision = ta.propagate("NVDA", "2024-05-10")

print(decision)  # e.g. "Buy"
```

### Interactive CLI

```bash
tradingagents analyze
```

The CLI walks you through:
1. Ticker symbol (e.g. `NVDA`, `CNC.TO`, `0700.HK`)
2. Analysis date
3. Output language
4. Which analysts to include
5. Research depth (debate rounds)
6. LLM provider and model selection

Add `--checkpoint` to enable resume on crash:

```bash
tradingagents analyze --checkpoint
```

### Using Anthropic Claude

```python
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "anthropic"
config["deep_think_llm"] = "claude-opus-4-5"
config["quick_think_llm"] = "claude-sonnet-4-6"

ta = TradingAgentsGraph(config=config)
_, decision = ta.propagate("AAPL", "2024-11-01")
```

### Using Google Gemini

```python
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "google"
config["deep_think_llm"] = "gemini-2.5-pro"
config["quick_think_llm"] = "gemini-2.5-flash"

ta = TradingAgentsGraph(config=config)
_, decision = ta.propagate("TSLA", "2024-11-01")
```

### Running Local Models with Ollama

```python
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "ollama"
config["deep_think_llm"] = "qwen3:32b"
config["quick_think_llm"] = "qwen3:latest"

ta = TradingAgentsGraph(config=config)
_, decision = ta.propagate("SPY", "2024-11-01")
```

### Selecting Specific Analysts

```python
# Only run news and fundamentals analysts (skip market and social)
ta = TradingAgentsGraph(
    selected_analysts=["news", "fundamentals"],
    config=config,
)
_, decision = ta.propagate("MSFT", "2024-11-01")
```

### Using Alpha Vantage as Data Backend

```python
config = DEFAULT_CONFIG.copy()
config["data_vendors"] = {
    "core_stock_apis": "alpha_vantage",
    "technical_indicators": "alpha_vantage",
    "fundamental_data": "alpha_vantage",
    "news_data": "alpha_vantage",
}
# Set ALPHA_VANTAGE_API_KEY in your .env file
```

---

## Configuration Reference

Key options in `DEFAULT_CONFIG` (see `tradingagents/default_config.py`):

| Key | Default | Description |
|-----|---------|-------------|
| `llm_provider` | `"openai"` | LLM backend: `openai`, `anthropic`, `google`, `xai`, `deepseek`, `qwen`, `glm`, `ollama`, `openrouter`, `azure` |
| `deep_think_llm` | `"gpt-4.1"` | Model for deep reasoning (research manager, portfolio manager) |
| `quick_think_llm` | `"gpt-4.1-mini"` | Model for fast, high-volume agents (analysts, researchers, trader) |
| `max_debate_rounds` | `1` | Bull/bear debate rounds |
| `max_risk_discuss_rounds` | `1` | Risk team discussion rounds |
| `data_vendors` | `yfinance` | Per-category data vendor (`yfinance` or `alpha_vantage`) |
| `checkpoint_enabled` | `False` | Save LangGraph state after each node for crash recovery |
| `output_language` | `"English"` | Language for analyst reports and final decision |
| `results_dir` | `~/.tradingagents/logs` | Directory for JSON decision logs |

---

## Project Structure

```
TradingAgents/
├── tradingagents/
│   ├── agents/
│   │   ├── analysts/          # Market, social, news, fundamentals analysts
│   │   ├── researchers/       # Bull and bear researchers
│   │   ├── risk_mgmt/         # Aggressive, conservative, neutral debators
│   │   ├── managers/          # Research manager, portfolio manager
│   │   ├── trader/            # Trader agent
│   │   └── utils/             # State definitions, tool bindings, memory
│   ├── dataflows/             # yfinance and Alpha Vantage data adapters
│   ├── graph/                 # LangGraph setup, checkpointing, signal processing
│   ├── llm_clients/           # Provider-agnostic LLM client factory
│   └── default_config.py      # Configuration defaults
├── cli/                       # Rich interactive CLI
├── main.py                    # Programmatic usage example
├── tests/                     # Test suite
└── pyproject.toml
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM abstraction | [LangChain](https://github.com/langchain-ai/langchain) |
| Default data | [yfinance](https://github.com/ranaroussi/yfinance) |
| Optional data | [Alpha Vantage](https://www.alphavantage.co/) |
| CLI / TUI | [Typer](https://typer.tiangolo.com/) + [Rich](https://github.com/Texel/rich) |
| Checkpointing | SQLite via `langgraph-checkpoint-sqlite` |
| Technical indicators | [stockstats](https://github.com/jealousleopard/stockstats) |

---

## Running Tests

```bash
# Install test dependencies
pip install -e .

# Run unit tests (no API keys required)
pytest tests/ -m unit

# Run all tests
pytest tests/
```

---

## Docker

A `docker-compose.yml` is provided for containerised deployment:

```bash
# Build and run
docker-compose up --build
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes and add tests
4. Run the test suite: `pytest tests/ -m unit`
5. Submit a pull request

---

## License

This project is licensed under the [MIT License](LICENSE).
