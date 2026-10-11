# Dataset choices and provenance

## Sentiment training data

Publisher: `zeroshot/twitter-financial-news-sentiment` on Hugging Face.
Pinned revision: `ccbe24de388e287beb92dd393a335c376b350ac3`.
License metadata: MIT, according to the publisher's dataset card.
Label mapping: publisher 0 = Bearish -> negative, 1 = Bullish -> positive, 2 = Neutral -> neutral.

The files actually downloaded contain 9,543 train rows and 2,388 validation rows. The publisher card reports different totals in its narrative/table. This implementation reports the downloaded counts and exact hashes rather than repeating inconsistent card counts.

Cleaning canonicalizes to lowercase URL-stripped word tokens. It collapses duplicate canonical texts, excludes groups with conflicting labels and removes 55 remaining evaluation rows overlapping training. Final train = 9,374. Final evaluation = 2,318. The data hash, class counts, confusion matrix and per-class metrics appear in `data/evaluation.json`.

Model: TF-IDF word unigrams/bigrams, minimum document frequency 2, maximum 16,000 features, sublinear term frequency and L2 normalization. Balanced multinomial logistic regression with C=4, maximum 1,000 iterations and seed 42. No hyperparameter search on the evaluation split. Exported weights round to seven decimal places. Runtime parity checks use those exported weights.

Accuracy = 0.8205349439. Macro-F1 = 0.7605247651. These assess sentiment only. They are not independent market-risk validation or a time-separated benchmark.

Raw publisher tweets are not redistributed in this repository. The reproducible script fetches pinned files into an ignored cache directory. Source URLs and SHA-256 checksums are retained in the evaluation report.

## Live ingestion

BBC Business RSS and Guardian Business RSS are two distinct live publishers. Both fetched real records during development. Only headlines/descriptions, timestamps and source links are processed. Feed freshness depends on publishers and the 60-second cache.

## Self-authored demonstration data

`data/replay.json`: eight explicitly synthetic news/social records covering positive, negative and neutral signals, company updates, geopolitical risk, credit stress and macroeconomic events. These are demonstration fixtures, not sentiment training or evaluation data.

`data/portfolio.json`: a synthetic $10m portfolio with loans, bonds, equities and a derivative. Duration, spread-duration, equity beta and derivative sensitivity are explicit inputs. It is a self-authored alternative dataset permitted by the brief, rather than a claim to have used the unavailable transaction sample.

Event/impact rules and stress shocks are assumptions in code. They are not learned from the sentiment corpus. Their evidence and limitations are visible in the dashboard and presentation.
