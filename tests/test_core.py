from yogacoach.core import angle, score_pose


def test_right_angle():
    assert abs(angle((0, 0), (1, 0), (1, 1)) - 90) < 1e-8


def test_perfect_pose_scores_100():
    landmarks = {"joint": ((0, 0), (1, 0), (1, 1))}
    assert score_pose(landmarks, {"joint": 90})["score"] == 100
