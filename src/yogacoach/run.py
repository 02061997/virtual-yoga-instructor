import argparse

import matplotlib.pyplot as plt
import pandas as pd

from .artifacts import environment, output_dir, save
from .core import (
    ANGLE_TRIPLETS,
    LANDMARK_NAMES,
    benchmark,
    packet_to_json,
    perturb,
    reference_tree_pose,
    score_pose,
    extract_angles,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    out = output_dir(args.smoke)
    reference = reference_tree_pose()
    target = extract_angles(reference)
    noises = [0, 0.01] if args.smoke else [0, 0.01, 0.03, 0.05, 0.1, 0.2]
    rows = []
    for noise in noises:
        for seed in range(2 if args.smoke else 30):
            packet = score_pose(perturb(reference, noise, seed), target)
            rows.append(
                {
                    "noise": noise,
                    "seed": seed,
                    "score": packet.score,
                    "feedback_count": len(packet.prompts),
                    "payload_bytes": len(packet_to_json(packet).encode()),
                }
            )
    frame = pd.DataFrame(rows)
    frame.to_parquet(out / "predictions.parquet", index=False)
    summary = frame.groupby("noise").score.agg(["mean", "std"]).reset_index()
    ax = summary.plot(x="noise", y="mean", marker="o", legend=False, ylabel="Pose score")
    ax.figure.tight_layout()
    ax.figure.savefig(out / "robustness.png", dpi=180)
    plt.close(ax.figure)
    save(
        out / "metrics.json",
        {
            "geometry_latency_ms": benchmark(reference, target),
            "robustness": summary.to_dict(orient="records"),
        },
    )
    save(
        out / "statistical_tests.json",
        {
            "paper_user_study": {
                "participants": 30,
                "male": 23,
                "female": 7,
                "age_range": [22, 35],
                "versions": ["baseline", "intermediate", "full"],
                "criteria": ["ease_of_use", "interaction", "engagement", "informativeness", "retention"],
                "raw_scores_available": False,
            }
        },
    )
    save(out / "environment.json", environment())
    save(
        out / "data_manifest.json",
        {
            "source": "deterministic MediaPipe-compatible 33-landmark tree-pose fixture",
            "landmarks": len(LANDMARK_NAMES),
            "angles": len(ANGLE_TRIPLETS),
            "camera_frames_included": False,
        },
    )
    save(
        out / "config.yaml",
        {"tolerance_degrees": 15, "transport": "TCP/IP newline-delimited JSON with ACK"},
    )
    (out / "run.log").write_text("completed\n")
    print(out)


if __name__ == "__main__":
    main()
