## Requirements mapping

| Case-study requirement | Implementation |
|---|---|
| Text from at least two sources | BBC Business RSS and Guardian Business RSS, both verified during development |
| Sentiment score | Learned TF-IDF/logistic regression model, P(positive) minus P(negative), range -1 to +1 |
| Event category | Geopolitical, Macroeconomic, Credit Event, Merger/Acquisition, Product Launch, Other |
| Impact estimate | Transparent severity heuristic, bounded 1–10, with keyword evidence |
| Structured output | JSON API, signal inspector, JSON export |
| Module A | Ten mock stock positions, normalized sentiment weights and weight history |
| Module B | Synthetic loans, bonds, equities and a derivative with event-triggered shocks |
| Public source repository | This repository |
| Demonstration <=5 minutes | Public dashboard and timed walkthrough |
| Presentation <=7 slides | Seven-slide editable PPTX in docs/ |

## Data and measured sentiment performance

The model uses the publisher's MIT-labeled **Twitter Financial News Sentiment** dataset, rather than the initial synthetic training examples. Source revision, data hashes, label mapping, cleaning and split counts are recorded in `data/evaluation.json`.

- 9,374 training records after canonical deduplication and conflict removal.
- 2,318 evaluation records from the publisher's validation split after overlap removal.
- Held-out accuracy: **82.05%**.
- Held-out macro-F1: **0.761**.

These results assess sentiment labels on this split. They do not measure market-risk prediction, event extraction, portfolio returns or generalization to new publishers. The split is not temporal or entity-disjoint. Model posteriors are not calibrated confidence estimates.

The application distributes learned weights in `model.json.gz`. Original pinned publisher CSVs and exact cleaned splits are bundled in data/. To reproduce training:

```bash
python -m venv .venv
# Activate the environment on your operating system.
python -m pip install -r requirements-training.txt
python scripts/train_model.py --cache data/raw
```

The training script downloads source files at a pinned revision, uses fixed hyperparameters and never fits/tunes on the evaluation split. Normalized text forms are used to remove exact duplicate overlap. Near-duplicate stories can still exist.

## Architecture

Local: publisher RSS -> parsing/cleanup -> learned sentiment + event/impact rules -> SQLite -> JSON API -> dashboard.

Public: embedded read-only Worker API -> RSS publishers -> same JavaScript inference. Browser state stays in memory. The GitHub Pages dashboard calls the Worker through a narrow CORS allowlist.

The public API does not store visitor text or require sign-in. The local API persists analyzed signals in SQLite, with source+text duplicate suppression. Both modes have request-size limits and explicit source errors. Feed responses cache for 60 seconds per process/isolate. Cached records can therefore be up to 60 seconds old plus the publisher's own delay.

## JSON API

- `GET /api/health`
- `POST /api/analyze`: `{"rows":[{"text":"Apple reports strong profit growth","source":"manual","company":"AAPL"}]}`
- `POST /api/ingest`: `{"source":"bbc"}` or `{"source":"guardian"}`
- `POST /api/stress`: `{"signal":{"impact_score":10,"event_classification":"Geopolitical"},"threshold":7,"multiplier":1}`. Optional `portfolio`.
- Local only: `GET /api/signals`, `POST /api/rebalance`.
- Public only: `GET /api/metrics`.

The local server binds to 127.0.0.1 and is a demo server, not a hardened public web server. An optional local SEC connector remains available with `SEC_CONTACT_EMAIL`, but BBC and Guardian satisfy the two-source requirement.

## Portfolio contracts

The supplied sample transaction file was not provided, and the case study permits other data sources. This project uses a self-authored **synthetic portfolio**, documented in `data/portfolio.json`. It contains $4m loans, $3m bonds, $2m equities and a $1m derivative carrying signed rate sensitivity.

Stress triggers when impact is **strictly greater than** the threshold, default 7. Default geopolitical shocks: equity -10%, rates +2 percentage points and credit spreads +1.5 percentage points. Each simulation starts from the original portfolio.

First-order asset change:

`value * (equity_beta * equity_shock - duration * rate_shock - spread_duration * spread_shock) + rate_sensitivity * rate_shock`

The synthetic geopolitical scenario produces a $1.02m loss, reducing value from $10m to $8.98m. Shocks and exposures are illustrative and are not calibrated forecasts. Derivative sensitivity is currency per unit change in rate. Positive sentiment does not reverse an adverse stress scenario.

Module A uses ten mock positions with equal starting weights. Raw weight `1 + 0.5 * latest company sentiment`, then normalize to sum to 100%. Basic company aliases/ticker tags support routing. GLOBAL events do not change company positions. The chart follows AAPL, MSFT and TSLA, with every position included in exported history. This is a mock index, without price-based backtesting or transaction costs.

## Verification

```bash
python -m unittest discover -s tests -v
node tests/browser-engine.mjs
python scripts/replay.py
python scripts/build_worker.py
node tests/worker-api.mjs
```

`tests/integration.py` runs against the local server and checks API behavior, persistence, duplicate suppression and Python/browser parity. It expects a clean demonstration database. Browser test execution creates its parity fixture.

Tests validate calculation and API behavior. Held-out sentiment metrics are separately recorded in `data/evaluation.json`.

## Limitations

Keyword event classification and impact scoring can miss negation, ambiguity and mixed events. Basic aliases do not resolve arbitrary entities. Tweet-trained sentiment can shift on long news articles. The public browser session resets on reload unless you export its results. Exposure valuation omits nonlinear option effects, convexity, recovery assumptions and liquidity constraints. No live trading is implemented.

## Sources and attribution

- Dataset publisher: https://huggingface.co/datasets/zeroshot/twitter-financial-news-sentiment
- BBC RSS: https://support.bbc.co.uk/platform/feeds/NewsFeeds.htm
- Guardian RSS: https://www.theguardian.com/help/feeds
- Assignment: supplied case-study screenshots.

Live publisher content remains attributed and linked to its original source. This application is a case-study demonstration. See `THIRD_PARTY_NOTICES.md` for data attribution and usage context.
