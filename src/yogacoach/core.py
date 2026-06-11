from __future__ import annotations

import time
import numpy as np


def angle(a, b, c):
    ba, bc = np.asarray(a) - np.asarray(b), np.asarray(c) - np.asarray(b)
    cosine = np.dot(ba, bc) / max(np.linalg.norm(ba) * np.linalg.norm(bc), 1e-12)
    return float(np.degrees(np.arccos(np.clip(cosine, -1, 1))))


def score_pose(landmarks, target, tolerance=15):
    errors = {joint: abs(angle(*landmarks[joint]) - expected) for joint, expected in target.items()}
    score = max(0.0, 100 * (1 - np.mean(list(errors.values())) / 90))
    feedback = [
        f"Adjust {joint}: error {error:.1f}°"
        for joint, error in errors.items()
        if error > tolerance
    ]
    return {"score": score, "errors": errors, "feedback": feedback}


def perturb(landmarks, noise, seed):
    rng = np.random.default_rng(seed)
    return {
        name: tuple((np.asarray(points) + rng.normal(0, noise, (3, 2))).tolist())
        for name, points in landmarks.items()
    }


def benchmark(landmarks, target, repeats=1000):
    start = time.perf_counter()
    for _ in range(repeats):
        score_pose(landmarks, target)
    return (time.perf_counter() - start) * 1000 / repeats
