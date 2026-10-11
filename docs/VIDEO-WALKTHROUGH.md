# Ten-minute submission recording

Presenter: Aarohi Chadha, IGDTUW. Record the real application screen with your narration. This document is a recording script, not a completed video. Target 10 minutes according to the separate submission guidelines. Keep the five-minute live pitch separate.

Before recording: close unrelated tabs and notifications, set browser zoom to 90–100%, test microphone audio and download this repository. Show only project files, without credentials or private messages. Have the README and dashboard ready. If a feed is unavailable, show its error honestly and use the labeled synthetic replay for calculations.

## 0:00–0:40 — Introduction

Screen: presentation title slide, then dashboard.

Say: “Hello, I am Aarohi Chadha from Indira Gandhi Delhi Technical University for Women. My project is RiskRadar, a financial NLP engine with two downstream applications. Financial news is unstructured, so an analyst must interpret the event and relate it to portfolio exposures. This prototype turns text into a sentiment score, an event category and an impact estimate. It demonstrates sentiment-driven mock index rebalancing and event-driven portfolio stress testing. I will show setup, live inputs, processing, results and the assumptions behind them.”

## 0:40–1:30 — Start from the README

Screen: repository README Quickstart and your terminal. Show the exact commands you actually run.

```bash
python -m pip install -r requirements.txt
python server.py
```

Open http://localhost:8000.

Say: “The repository is public and contains the code, dependencies, data, architecture diagram and presentation. The application runs with Python 3.10 or later. Inference uses the standard library, so requirements.txt has no external runtime packages. The server runs locally and stores analyzed signals in SQLite. Training has a separate dependency file. The public dashboard uses the same exported sentiment parameters with JavaScript and calls a Worker API for live ingestion. Neither dashboard requires a visitor login.”

## 1:30–2:20 — Explain the architecture

Screen: docs/architecture.png and relevant README section.

Say: “There are two live publishers: BBC Business and Guardian Business. Their RSS titles and descriptions become text records with source links and publication times. Manual text and the synthetic JSON replay can enter the same engine. Sentiment comes from TF-IDF features and logistic regression. Event classification and impact use explicit keyword rules. Every signal retains evidence so the output can be inspected. Module A reads company sentiment. Module B reads event class and impact. API responses and exports provide machine-readable results. Local mode persists records in SQLite, while the public browser keeps session state in memory.”

## 2:20–3:30 — Fetch both real publishers

Screen: select BBC and click Fetch live, then select Guardian and click Fetch live. Inspect one record and its original source.

Say: “I am fetching BBC first and Guardian second. These are real publisher records, with their source and timestamp retained. The module suppresses duplicate text from the same source. The live polling button refreshes both once per minute while the page remains open. A 60-second cache limits repeated upstream requests, and freshness also depends on when publishers update their feeds. Company aliases route some stories to a ticker, while unmatched stories remain GLOBAL. These basic aliases do not perform unrestricted entity resolution.”

Pause to show the actual counts. Do not read preset counts if the feed returns different results. Explain any displayed error.

## 3:30–4:30 — Inspect a structured signal

Screen: Reset, Run replay, select “War escalation and sanctions…”, open Selected signal and model evidence.

Say: “I am switching to a repeatable synthetic replay to show a controlled calculation. These eight fixtures are separate from the real sentiment training data. The war and sanctions example produces sentiment approximately minus 0.519, a geopolitical event label and impact nine. Sentiment is the positive-class probability minus the negative-class probability, bounded from minus one to one. Impact is a severity heuristic from one to ten. It is not a calibrated prediction of market loss. The JSON shows class probabilities, matched keywords and source metadata. Low confidence is flagged when the maximum class probability is below 0.55. The probabilities themselves are not calibrated confidence estimates.”

## 4:30–6:00 — Demonstrate stress testing

Screen: show before/after cards and asset table. Change multiplier from 1 to 0.5, then back to 1. Set threshold 9 to demonstrate no trigger when impact equals threshold, then restore 7.

Say: “The synthetic portfolio starts at ten million dollars. It includes four million in loans, three million in bonds, two million in equity and one million in a derivative. Stress runs only when impact is strictly greater than the threshold. With threshold seven, this impact-nine event triggers the geopolitical scenario. The assumed shocks are a ten percent equity fall, a two percentage-point interest-rate increase and a one-and-a-half percentage-point credit-spread increase. These are illustrative inputs.”

Say: “The loan loss is 280 thousand dollars, the bond loss 480 thousand, the equity loss 200 thousand and the derivative loss 60 thousand. Total loss is 1.02 million, or 10.2 percent, leaving 8.98 million. The model uses first-order sensitivities. The derivative has a signed rate sensitivity, so its response follows that input. When I halve the multiplier, the linear model halves the loss. Each run starts from the original portfolio, avoiding accidental compounding. If I set the threshold to nine, impact nine no longer triggers because the comparison is strictly greater than.”

## 6:00–7:00 — Demonstrate index rebalancing

Screen: current weights and weight history chart.

Say: “Module A starts with ten equal ten-percent mock positions. Its raw weight is one plus half the latest company sentiment, then all raw weights normalize to 100 percent. Positive sentiment raises a company's raw weight and negative sentiment lowers it. In this replay, Apple is about 13.85 percent, Microsoft 13.61 percent and JPM about 5.07 percent. GLOBAL events do not directly change company weights. The chart follows three companies for readability, while the export contains every position. This demonstrates signal consumption, not trading execution or evidence of outperformance.”

## 7:00–7:45 — New input and JSON export

Screen: enter “Apple reports strong profit growth and record revenue”, company AAPL, source manual, Analyze text. Open the evidence. Click Export JSON and show the resulting file.

Say: “A new manual headline goes through the same engine. The company tag associates it with Apple. The sentiment changes the mock weights. The event class can be Other when no event rule applies, and its low impact does not trigger stress. The export contains structured signals, scenario results and weight history, allowing another application to consume the outputs. These APIs and JSON files satisfy the machine-readable output requirement.”

## 7:45–9:00 — Dataset and evaluation

Screen: data/manifest.json, data/evaluation.json, docs/DATASET.md. Show actual metrics and original/cleaned datasets in /data.

Say: “Sentiment trains on the published Twitter Financial News Sentiment dataset from zeroshot. Its pinned revision and publisher MIT license statement are recorded. The repository contains the original CSVs and exact cleaned training and evaluation splits. Cleaning collapses canonical exact duplicates, removes conflicting-label groups and excludes 55 evaluation records overlapping training. This leaves 9,374 training records and 2,318 evaluation records.”

Say: “The model uses word unigrams and bigrams, sublinear term frequency and balanced logistic regression. The held-out sentiment accuracy is 82.05 percent and macro-F1 is 0.761. I have not tuned hyperparameters on this evaluation split. The split is not temporal or entity-disjoint, so it should not be treated as evidence of future-market prediction. News articles can differ from financial tweets. The impact rules and scenario shocks are not trained on this corpus. Nine unit tests, integration checks and Python/JavaScript parity verify implementation behavior, separately from sentiment quality.”

## 9:00–10:00 — Impact, limitations and close

Screen: final slide and public repository links.

Say: “For a risk analyst, the shared signal format supports consistent news inspection. The stress dashboard relates an event assumption to asset-level exposures. The second module demonstrates another use of the same engine. This can support investigation and scenario comparison, but I have not measured analyst time savings or investment performance.”

Say: “Current limits include keyword rules that miss negation and mixed events, basic company aliases, sentiment domain shift and simplified linear valuation. Next steps are temporal sentiment evaluation and calibration of severity and shocks against observed market behavior. AI assistance supported implementation and documentation, and all data sources and assumptions are recorded. The individual candidate should understand the design and explain it during the jury pitch. Thank you.”

## Publish the recording

Upload the real screen recording to YouTube and select **Unlisted**. Copy the watch URL into the README Demo Video Link and the official submission form. Test playback in a private/incognito window without sign-in. Do not replace the required video with this script or the dashboard link.
