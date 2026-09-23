# StockPilotAI

StockPilotAI is a Python-based stock research and portfolio analysis project built with FastAPI, SQLAlchemy, and market-data integrations. The application is designed to expose stock information through a simple API and to evolve into an AI-assisted investment research tool.

At its current stage, the project includes:

- A FastAPI backend
- Stock research endpoints
- YFinance-based market data retrieval
- SQLAlchemy database models for storing stock metadata
- A test suite for the research service and data layer

## Why this project exists

The goal of StockPilotAI is to provide a foundation for analyzing stocks, collecting market metrics, and eventually generating AI-driven insights for investors. The project combines structured financial data with backend API services so that results can be consumed by web apps, dashboards, or AI workflows.

## Project overview

The application is organized around a backend service layer that retrieves market information for a given stock symbol and exposes it through REST endpoints. The current implementation focuses on fetching core trading metadata such as current price and market capitalization.

## Tech stack

- Python 3.13+
- FastAPI for API routes
- SQLAlchemy for database access
- Pydantic for validation and settings
- YFinance for real-market financial data
- Ollama-ready architecture for AI-based analysis
- Pytest for automated testing

## Repository structure

```text
StockpilotAI/
├── backend/
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── health.py
│   │   └── research.py
│   ├── database/
│   │   ├── connection.py
│   │   ├── dependencies.py
│   │   └── init_db.py
│   ├── models/
│   │   └── stock.py
│   ├── repositories/
│   │   ├── market_data.py
│   │   ├── yfinance_client.py
│   │   └── yfinance_market_data.py
│   ├── schemas/
│   ├── services/
│   │   └── research.py
│   ├── utils/
│   │   └── config.py
│   ├── main.py
│   └── __init__.py
├── src/
│   └── stockpilotai/
│       └── __init__.py
├── tests/
│   ├── test_db_init.py
│   ├── test_research_service.py
│   ├── test_research_with_yfinance_provider.py
│   ├── test_stock_api.py
│   └── test_yfinance_market_data.py
├── pyproject.toml
├── README.md
├── .env.example (recommended to create locally)
└── data/
```

## Current functionality

The project currently provides a research API for stock symbols.

### Health endpoint

```http
GET /health
```

Returns the status of the API.

### Stock research endpoint

```http
GET /stocks/{symbol}/research
```

Example:

```bash
curl http://localhost:8000/stocks/RELIANCE.NS/research
```

This route calls the research service, which retrieves stock market data from a provider and returns structured stock information.

## How it works

1. A request comes in through FastAPI.
2. The route in the API layer delegates work to the research service.
3. The service uses a market data provider abstraction.
4. The provider fetches data from YFinance.
5. The result is returned as a Pydantic model representing stock market data.

This design keeps the controller layer thin and makes it easy to switch providers or expand the service logic.

## Environment configuration

This project reads environment variables through Pydantic settings. Create a .env file in the project root with values similar to the following:

```env
APP_NAME=StockPilotAI
APP_VERSION=0.1.0
OLLAMA_BASE_URL=http://localhost:11434
DATABASE_URL=sqlite:///./stockpilot.db
```

The settings object is defined in backend/utils/config.py and is used by the database connection layer.

## Setup

### Prerequisites

- Python 3.13+
- uv installed for dependency management

### Install dependencies

```bash
uv sync
```

If you are using a virtual environment manually:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the app

Start the FastAPI server with:

```bash
uv run uvicorn backend.main:app --reload
```

The application will be available at:

- http://localhost:8000/
- http://localhost:8000/health
- http://localhost:8000/stocks/{symbol}/research

## Run tests

```bash
uv run python -m pytest
```

The project includes tests for:

- research service behavior
- database init flow
- stock API endpoints
- YFinance provider integration

## Typical usage

Use the stock endpoint with a known ticker or symbol from the market provider:

```bash
curl "http://localhost:8000/stocks/AAPL/research"
```

The response is currently structured as stock metadata, including the symbol and basic financial values when available from the provider.

## Notes on the current state

This repository is a working foundation for a stock-analysis platform. Some parts are intentionally minimal and designed to be expanded. The architecture already supports:

- adding more market data providers
- storing stock metadata in a database
- integrating AI tooling through Ollama
- extending the research service with deeper analyst insights

## Future direction

Planned enhancements may include:

- AI-generated research summaries with Ollama
- portfolio-level analysis for multiple holdings
- historical price and trend analysis
- valuation metrics and recommendations
- frontend dashboard integration
- caching and rate-limit friendly data fetching

## License

This project does not currently include a license file. If you plan to distribute or deploy it publicly, add an appropriate open-source license before release.

## Contributing

Contributions are welcome. For a local workflow:

1. Fork the repository
2. Create a feature branch
3. Add or update tests
4. Run the test suite
5. Open a pull request with a clear description of the change

## Summary

StockPilotAI is a backend-first stock intelligence project that starts with real market data retrieval and grows toward AI-assisted stock research. It is useful as both an API starter and as a foundation for building a more complete investment-analysis platform.
