from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a custom config
config = DEFAULT_CONFIG.copy()
# Use confirmed, production-available OpenAI models.
# Change llm_provider and model names to use a different provider.
config["llm_provider"] = "openai"
config["deep_think_llm"] = "gpt-4.1"
config["quick_think_llm"] = "gpt-4.1-mini"
config["max_debate_rounds"] = 1  # Number of bull/bear debate rounds

# Configure data vendors (default uses yfinance, no extra API keys needed)
config["data_vendors"] = {
    "core_stock_apis": "yfinance",           # Options: alpha_vantage, yfinance
    "technical_indicators": "yfinance",      # Options: alpha_vantage, yfinance
    "fundamental_data": "yfinance",          # Options: alpha_vantage, yfinance
    "news_data": "yfinance",                 # Options: alpha_vantage, yfinance
}

# Initialize with custom config
ta = TradingAgentsGraph(debug=True, config=config)

# Run analysis for a ticker on a specific date
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)

# Optional: reflect on outcomes to build trading memory
# ta.reflect_and_remember(1000)  # parameter is the position returns in dollars
