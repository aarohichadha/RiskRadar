# Final submission materials

Author: Aarohi Chadha (`aarohichadha`).

1. Public source repository: https://github.com/aarohichadha/RiskRadar
2. Public demonstration dashboard: https://aarohichadha.github.io/RiskRadar/
3. Seven-slide presentation: docs/RiskRadar-Presentation.pptx in the repository.
4. Live demonstration: follow docs/DEMO.md and stay within five minutes.

The downloadable ZIP is a backup. It does not replace the public source repository.

## Answer-box text

RiskRadar is an AI/NLP financial risk platform that ingests live text from BBC Business and Guardian Business RSS. It outputs a sentiment score, event category and heuristic impact score as JSON, then demonstrates tactical index rebalancing and portfolio stress testing.

Source code: https://github.com/aarohichadha/RiskRadar
Live dashboard: https://aarohichadha.github.io/RiskRadar/
Presentation: https://github.com/aarohichadha/RiskRadar/blob/main/docs/RiskRadar-Presentation.pptx

The sentiment model uses a published financial-tweet dataset with a disjoint held-out evaluation after duplicate-overlap removal. It achieves 82.05% sentiment accuracy and 0.761 macro-F1 on 2,318 evaluation records. Replay events, portfolio exposures and scenario shocks are documented synthetic data. Event/impact extraction is heuristic and no market-prediction accuracy is claimed.

Local setup: Python 3.10+, run python server.py and open http://localhost:8000. The repository includes reproducible training, exported model weights, evaluation statistics, tests, dataset provenance and the five-minute walkthrough.

## Organizer-dependent item

The separate submission-guidelines link was cut off in the supplied screenshots. Verify that document for the precise upload/link format and whether they expect a live session or a recording. No assessment answer has been submitted automatically.
