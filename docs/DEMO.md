# Five-minute live demonstration

Presenter: Aarohi Chadha (`aarohichadha`).
Dashboard: https://aarohichadha.github.io/RiskRadar/

0:00–0:35: Explain that RiskRadar ingests text from two publishers, extracts structured sentiment/event/impact signals, and demonstrates both downstream modules. Identify the learned sentiment model and the heuristic impact estimate.

0:35–1:15: Fetch BBC, then Guardian. Show publisher labels, original source links and timestamps. Start live polling if useful. Explain the 60-second cache and publisher-dependent freshness. Source outages must be shown honestly.

1:15–1:55: Run replay and choose the war/sanctions signal. Show its structured output and matching keywords. State that replay events are synthetic demonstration fixtures, separate from the real sentiment training dataset.

1:55–2:50: Show the portfolio before and after the geopolitical scenario. $10m becomes $8.98m, a $1.02m loss (10.2%). Explain $280k loan loss, $480k bond loss, $200k equity loss and $60k derivative loss. Change the shock multiplier to 0.5 and observe the halved loss. Each test starts from baseline.

2:50–3:35: Show the ten-position index and weight history. Positive company sentiment increases raw weight. Negative sentiment decreases it. The weights normalize to 100%. GLOBAL events do not alter company weights.

3:35–4:15: Analyze a new financial headline. Open its evidence JSON. Export signals, weight history and stress outputs as JSON.

4:15–5:00: Explain the real training corpus and held-out evaluation: 9,374 training records, 2,318 evaluation records, 82.05% accuracy and 0.761 macro-F1 after duplicate-overlap removal. Show the source repository and seven-slide deck. Close with limitations: event/impact heuristics, sentiment domain shift and simplified portfolio valuation.

## Backup

Run `python server.py` and open http://localhost:8000. No package install is needed. Replay works without live-source access. Show any source outage rather than presenting synthetic replay as live data. Have the downloaded PPTX ready locally.

## Submission format

The brief requests a live demonstration lasting no more than five minutes. A recording is not assumed to replace a live presentation. Check the separate organizer guidelines for the required format.
