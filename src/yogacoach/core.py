from __future__ import annotations

import json
import time
from dataclasses import dataclass

import numpy as np


LANDMARK_NAMES = (
    "nose", "left_eye_inner", "left_eye", "left_eye_outer", "right_eye_inner",
    "right_eye", "right_eye_outer", "left_ear", "right_ear", "mouth_left",
    "mouth_right", "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
    "left_wrist", "right_wrist", "left_pinky", "right_pinky", "left_index",
    "right_index", "left_thumb", "right_thumb", "left_hip", "right_hip", "left_knee",
    "right_knee", "left_ankle", "right_ankle", "left_heel", "right_heel",
    "left_foot_index", "right_foot_index",
)
LANDMARK_INDEX = {name: index for index, name in enumerate(LANDMARK_NAMES)}
ANGLE_TRIPLETS = {
    "left_elbow": ("left_shoulder", "left_elbow", "left_wrist"),
    "right_elbow": ("right_shoulder", "right_elbow", "right_wrist"),
    "left_shoulder": ("left_elbow", "left_shoulder", "left_hip"),
    "right_shoulder": ("right_elbow", "right_shoulder", "right_hip"),
    "left_hip": ("left_shoulder", "left_hip", "left_knee"),
    "right_hip": ("right_shoulder", "right_hip", "right_knee"),
    "left_knee": ("left_hip", "left_knee", "left_ankle"),
    "right_knee": ("right_hip", "right_knee", "right_ankle"),
}


@dataclass(frozen=True)
class FeedbackPacket:
    score: float
    angles: dict[str, float]
    prompts: dict[str, str]
    markers: dict[str, tuple[float, float, float]]


def angle(a, b, c) -> float:
    """Paper-aligned arctangent joint angle using image-plane X/Y coordinates."""
    a, b, c = np.asarray(a)[:2], np.asarray(b)[:2], np.asarray(c)[:2]
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )
    degrees = abs(float(np.degrees(radians)))
    return 360 - degrees if degrees > 180 else degrees


def extract_angles(landmarks: np.ndarray) -> dict[str, float]:
    if landmarks.shape != (33, 3):
        raise ValueError("MediaPipe Pose landmarks must have shape (33, 3)")
    return {
        joint: angle(
            landmarks[LANDMARK_INDEX[first]],
            landmarks[LANDMARK_INDEX[pivot]],
            landmarks[LANDMARK_INDEX[last]],
        )
        for joint, (first, pivot, last) in ANGLE_TRIPLETS.items()
    }


def directional_prompt(joint: str, error: float) -> str:
    action = "extend" if error < 0 else "fold"
    return f"{action}_{joint}"


def score_pose(
    landmarks: np.ndarray,
    target_angles: dict[str, float],
    tolerance: float = 15,
) -> FeedbackPacket:
    measured = extract_angles(landmarks)
    prompts = {}
    markers = {}
    correct = 0
    for joint, expected in target_angles.items():
        signed_error = measured[joint] - expected
        if abs(signed_error) <= tolerance:
            correct += 1
            continue
        prompts[joint] = directional_prompt(joint, signed_error)
        markers[joint] = tuple(float(value) for value in landmarks[LANDMARK_INDEX[joint]])
    score = 100 * correct / len(target_angles)
    return FeedbackPacket(score, measured, prompts, markers)


def packet_to_json(packet: FeedbackPacket) -> str:
    return json.dumps(
        {
            "score": packet.score,
            "angles": packet.angles,
            "prompts": packet.prompts,
            "markers": packet.markers,
        },
        sort_keys=True,
        separators=(",", ":"),
    )


def encode_message(packet: FeedbackPacket) -> bytes:
    return (packet_to_json(packet) + "\n").encode()


def decode_message(payload: bytes) -> dict:
    return json.loads(payload.decode().strip())


def acknowledge(sequence: int) -> bytes:
    return (json.dumps({"ack": sequence}, separators=(",", ":")) + "\n").encode()


def perturb(landmarks: np.ndarray, noise: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return landmarks + rng.normal(0, noise, landmarks.shape)


def benchmark(landmarks: np.ndarray, target: dict[str, float], repeats: int = 1000) -> float:
    start = time.perf_counter()
    for _ in range(repeats):
        score_pose(landmarks, target)
    return (time.perf_counter() - start) * 1000 / repeats


def reference_tree_pose() -> np.ndarray:
    points = np.zeros((33, 3), dtype=float)
    coordinates = {
        "left_shoulder": (-0.3, 1.5, 0), "right_shoulder": (0.3, 1.5, 0),
        "left_elbow": (-0.7, 1.9, 0), "right_elbow": (0.7, 1.9, 0),
        "left_wrist": (0.0, 2.2, 0), "right_wrist": (0.0, 2.2, 0),
        "left_hip": (-0.2, 0.9, 0), "right_hip": (0.2, 0.9, 0),
        "left_knee": (-0.2, 0.2, 0), "right_knee": (0.55, 0.75, 0),
        "left_ankle": (-0.2, -0.6, 0), "right_ankle": (0.05, 0.45, 0),
    }
    for name, coordinate in coordinates.items():
        points[LANDMARK_INDEX[name]] = coordinate
    return points
