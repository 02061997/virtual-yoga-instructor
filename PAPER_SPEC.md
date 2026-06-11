# Paper Specification

Source: *Virtual Yoga Instructor with Real-Time Feedback*, CISS 2025,
DOI `10.1109/CISS64860.2025.10944737`.

## Implemented specification

- MediaPipe Pose's 33 three-dimensional landmarks.
- Eight bilateral elbow, shoulder, hip, and knee angles using the paper's
  arctangent construction.
- Reference-pose comparison with configurable plus/minus tolerance.
- Sixteen fold/extend correction prompts and landmark marker coordinates.
- Score, angles, prompts, and markers serialized as TCP/IP JSON messages.
- Acknowledgment-message support for the Unity client boundary.
- Tree-pose fixture and robustness/geometry-latency evaluation.

The paper's Unity/Mixamo/Blender assets and raw 30-participant questionnaire
responses were unavailable and are not reconstructed or invented. The reported
user-study design is documented separately from local geometry results.
