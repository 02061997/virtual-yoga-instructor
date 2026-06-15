# Virtual Yoga Instructor Feedback Engine

Paper-faithful Python companion for *Virtual Yoga Instructor with Real-Time
Feedback* (CISS 2025).

It implements the MediaPipe 33-landmark schema, eight reference-pose joint
angles, tolerance scoring, 16 directional correction prompts, marker
coordinates, and acknowledged TCP/JSON messages for the Unity boundary.
Unity/Mixamo/Blender assets and participant records are not redistributed.

Full runs generate `feedback_demo.gif` and `pose_feedback_overlay.png` under
`reports/latest/` so the geometry feedback behavior can be inspected visually.
These are synthetic landmark renders, not camera or Unity recordings.

```bash
uv sync
make test
make reproduce-smoke
make reproduce-results
```
