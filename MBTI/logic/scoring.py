# -*- coding: utf-8 -*-
"""
무역 MBTI - 채점 및 직무 매칭 로직

흐름:
    answers (20개 응답, 각 'A' 또는 'B')
        -> calculate_axis_scores()  : 축별 A/B 득점 집계
        -> determine_type_code()    : 축별 우세 알파벳 -> 4글자 유형 코드
        -> match_job()               : 기획서 4절의 if/else 트리로 직무 결정
        -> get_result()              : 위 세 단계를 한 번에 실행하는 편의 함수
"""

from data.questions import QUESTIONS, AXES
from data.jobs import JOBS


def calculate_axis_scores(answers):
    """
    answers: list[str]
        QUESTIONS와 같은 순서로, 각 문항에서 고른 선택지 ('A' 또는 'B') 20개.

    반환값: dict
        {축번호: {"A": a_count, "B": b_count}}
    """
    if len(answers) != len(QUESTIONS):
        raise ValueError(
            f"응답 개수({len(answers)})가 문항 개수({len(QUESTIONS)})와 일치하지 않습니다."
        )

    scores = {axis: {"A": 0, "B": 0} for axis in AXES}

    for question, answer in zip(QUESTIONS, answers):
        answer = answer.upper()
        if answer not in ("A", "B"):
            raise ValueError(f"잘못된 응답 값: {answer!r} (문항 {question['id']})")
        scores[question["axis"]][answer] += 1

    return scores


def determine_type_code(axis_scores):
    """
    축별 점수를 받아 4글자 유형 코드를 만든다.

    동점 처리(기획서 5절): A/B 점수가 같으면 기본값으로 첫 번째 성향
    (G/D/R/S, 즉 옵션 A 쪽)을 채택한다.

    반환값: str, 예) "GBHF"
    """
    letters = []
    for axis_num in sorted(AXES.keys()):
        axis_meta = AXES[axis_num]
        a_count = axis_scores[axis_num]["A"]
        b_count = axis_scores[axis_num]["B"]
        if a_count >= b_count:
            letters.append(axis_meta["a"])
        else:
            letters.append(axis_meta["b"])
    return "".join(letters)


def match_job(type_code):
    """
    기획서 4절의 트리 로직으로 4글자 유형 코드를 6개 직무 중 하나에 매칭한다.

    type_code: str, 예) "GBHF" (축1,축2,축3,축4 순서의 알파벳 4글자)

    반환값: str, JOBS 딕셔너리의 key
    """
    if len(type_code) != 4:
        raise ValueError(f"유형 코드는 4글자여야 합니다: {type_code!r}")

    axis1, axis2, _axis3_placeholder, axis4 = None, None, None, None
    # type_code 순서: [축1, 축2, 축3, 축4]
    axis1, axis2, axis3, axis4 = type_code[0], type_code[1], type_code[2], type_code[3]

    if axis1 == "G" and axis3 == "H":
        return "overseas_sales" if axis4 == "F" else "global_sourcing"
    if axis1 == "G" and axis3 == "R":
        return "customs_broker"
    if axis1 == "L" and axis3 == "H":
        return "logistics_scm"
    if axis1 == "L" and axis3 == "R":
        return "trade_operator" if axis2 == "D" else "trade_finance"

    # 이론상 축1={G,L}, 축3={R,H} 조합은 위 4가지로 전부 커버되므로 도달하지 않는다.
    raise ValueError(f"매칭 가능한 직무를 찾을 수 없습니다: {type_code!r}")


def get_result(answers):
    """
    answers -> 전체 결과를 한 번에 계산하는 편의 함수.

    반환값: dict
        {
            "axis_scores": {...},
            "type_code": "GBHF",
            "job_key": "overseas_sales",
            "job": JOBS["overseas_sales"],
        }
    """
    axis_scores = calculate_axis_scores(answers)
    type_code = determine_type_code(axis_scores)
    job_key = match_job(type_code)
    return {
        "axis_scores": axis_scores,
        "type_code": type_code,
        "job_key": job_key,
        "job": JOBS[job_key],
    }
