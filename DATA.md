# Data Documentation

## Original Project Data

The CISS 2025 project involved camera input, MediaPipe pose estimation,
Unity/Mixamo/Blender assets, and participant questionnaire data. Those assets
and participant records are not redistributed in this public companion.

## Included Fixture

Executable experiments use a deterministic synthetic 33-landmark
MediaPipe-compatible tree-pose fixture. The fixture validates joint-angle
geometry, correction prompts, JSON packet encoding, robustness analysis, and
generated visual overlays.

## Redistribution Boundary

No camera frames, participant records, Unity scenes, Mixamo assets, Blender
files, or raw user-study responses are included. The committed GIF and PNG are
generated synthetic landmark renders, not recordings.

## Generated Artifacts

`make reproduce-results` writes `reports/latest/`, including:

- `metrics.json`
- `predictions.parquet`
- `statistical_tests.json`
- `feedback_demo.gif`
- `pose_feedback_overlay.png`
- `robustness.png`

## NOT_RUN Limitations

End-to-end camera plus MediaPipe plus Unity latency and the 30-participant
questionnaire reproduction remain `NOT_RUN`. Geometry-only latency should not
be reported as full application latency.
