# Verified Results

## Provenance

This is a reconstructed geometry and feedback benchmark, not the original
application code. Camera, MediaPipe, and end-to-end device latency experiments
remain `NOT_RUN`.

## Local reproduction

`make reproduce-results` completed locally on June 11, 2026.

| Landmark noise | Mean pose score | Std. dev. |
|---|---:|---:|
| 0.00 | 100.00 | 0.00 |
| 0.01 | 99.07 | 0.41 |
| 0.03 | 97.19 | 1.25 |
| 0.05 | 95.29 | 2.10 |
| 0.10 | 90.39 | 4.30 |
| 0.20 | 79.71 | 8.53 |

Pure scoring latency averaged 0.0267 ms per pose on the local M3 Max.
That number excludes camera capture and landmark inference and must not be
presented as end-to-end latency.
