from yogacoach.core import (
    ANGLE_TRIPLETS,
    LANDMARK_NAMES,
    acknowledge,
    angle,
    decode_message,
    encode_message,
    extract_angles,
    reference_tree_pose,
    render_pose_frame,
    score_pose,
)


def test_mediapipe_schema_and_eight_angles():
    landmarks = reference_tree_pose()
    assert len(LANDMARK_NAMES) == 33
    assert landmarks.shape == (33, 3)
    assert len(ANGLE_TRIPLETS) == 8
    assert len(extract_angles(landmarks)) == 8


def test_arctangent_right_angle():
    assert abs(angle((0, 0), (1, 0), (1, 1)) - 90) < 1e-8


def test_perfect_pose_and_protocol_roundtrip():
    landmarks = reference_tree_pose()
    packet = score_pose(landmarks, extract_angles(landmarks))
    decoded = decode_message(encode_message(packet))
    assert packet.score == 100
    assert decoded["score"] == 100
    assert decode_message(acknowledge(9)) == {"ack": 9}


def test_sixteen_directional_prompt_space():
    prompts = {f"{direction}_{joint}" for joint in ANGLE_TRIPLETS for direction in ("fold", "extend")}
    assert len(prompts) == 16


def test_pose_renderer_marks_feedback_frame():
    landmarks = reference_tree_pose()
    target = extract_angles(landmarks)
    packet = score_pose(landmarks, target)
    image = render_pose_frame(landmarks, packet, size=256, title="test")
    assert image.size == (256, 256)
    assert image.mode == "RGB"
