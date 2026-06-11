import argparse
import pandas as pd
import matplotlib.pyplot as plt
from .artifacts import environment, output_dir, save
from .core import benchmark, perturb, score_pose


LANDMARKS = {
    "left_elbow": ((0, 0), (1, 0), (1, 1)),
    "right_elbow": ((2, 0), (1, 0), (1, 1)),
    "left_knee": ((0, 2), (0, 1), (1, 1)),
    "right_knee": ((2, 2), (2, 1), (1, 1)),
}
TARGET = {name: 90.0 for name in LANDMARKS}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    out = output_dir(args.smoke)
    noises = [0, 0.01] if args.smoke else [0, 0.01, 0.03, 0.05, 0.1, 0.2]
    rows = []
    for noise in noises:
        for seed in range(2 if args.smoke else 30):
            result = score_pose(perturb(LANDMARKS, noise, seed), TARGET)
            rows.append(
                {
                    "noise": noise,
                    "seed": seed,
                    "score": result["score"],
                    "feedback_count": len(result["feedback"]),
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
            "latency_ms": benchmark(LANDMARKS, TARGET),
            "robustness": summary.to_dict(orient="records"),
        },
    )
    save(out / "statistical_tests.json", {"seeds": int(frame.seed.nunique())})
    save(out / "environment.json", environment())
    save(out / "data_manifest.json", {"source": "synthetic normalized landmarks"})
    save(out / "config.yaml", {"tolerance_degrees": 15})
    (out / "run.log").write_text("completed\n")
    print(out)


if __name__ == "__main__":
    main()
