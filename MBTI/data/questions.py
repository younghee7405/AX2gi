# -*- coding: utf-8 -*-
"""
무역 MBTI - 20개 진단 문항

각 문항은 다음 정보를 갖는다.
- id: 문항 번호 (1~20)
- axis: 소속 축 번호 (1~4)
- text: 문항 질문
- option_a / option_b: 선택지 A / B 텍스트
- letter_a / letter_b: 각 선택지를 골랐을 때 부여되는 알파벳

축 구성:
  축1: G(대외지향형) vs L(대내집중형)
  축2: D(디테일형)   vs B(빅픽처형)
  축3: R(원칙형)     vs H(관계형)
  축4: S(안정형)     vs F(유연형)
"""

QUESTIONS = [
    # ---- 축1. 대외지향(G) vs 대내집중(L) ----
    {
        "id": 1,
        "axis": 1,
        "text": "해외 바이어와 갑자기 화상미팅이 잡혔다. 나는?",
        "option_a": "오히려 반갑다, 바로 소통하고 싶다",
        "option_b": "살짝 부담스럽다, 자료부터 꼼꼼히 준비하고 싶다",
        "letter_a": "G",
        "letter_b": "L",
    },
    {
        "id": 2,
        "axis": 1,
        "text": "새 프로젝트를 맡는다면 나는?",
        "option_a": "해외 출장·현지 파트너 미팅이 있는 업무를 원한다",
        "option_b": "사무실에서 데이터·서류를 다루는 업무를 원한다",
        "letter_a": "G",
        "letter_b": "L",
    },
    {
        "id": 3,
        "axis": 1,
        "text": "낯선 해외 거래처에 처음 연락해야 할 때 나는?",
        "option_a": "전화나 화상통화로 바로 컨택한다",
        "option_b": "이메일로 먼저 내용을 정리해서 보낸다",
        "letter_a": "G",
        "letter_b": "L",
    },
    {
        "id": 4,
        "axis": 1,
        "text": "팀 회의에서 나는 주로?",
        "option_a": "외부 파트너 반응이나 시장 상황을 공유한다",
        "option_b": "진행 상황과 숫자, 문서를 정리해 보고한다",
        "letter_a": "G",
        "letter_b": "L",
    },
    {
        "id": 5,
        "axis": 1,
        "text": "방학 인턴을 고른다면 나는?",
        "option_a": "해외영업팀·바이어 상담 업무",
        "option_b": "무역사무·물류 관리팀 업무",
        "letter_a": "G",
        "letter_b": "L",
    },
    # ---- 축2. 디테일형(D) vs 빅픽처형(B) ----
    {
        "id": 6,
        "axis": 2,
        "text": "계약서를 받았을 때 나는?",
        "option_a": "조항 하나하나 놓치지 않고 검토한다",
        "option_b": "전체 거래 구조와 리스크부터 그려본다",
        "letter_a": "D",
        "letter_b": "B",
    },
    {
        "id": 7,
        "axis": 2,
        "text": "새로운 시장을 공부할 때 나는?",
        "option_a": "관세율, 규정, 통계자료부터 찾아본다",
        "option_b": "그 나라의 트렌드와 기회 요인을 먼저 살펴본다",
        "letter_a": "D",
        "letter_b": "B",
    },
    {
        "id": 8,
        "axis": 2,
        "text": "팀 프로젝트에서 나는?",
        "option_a": "세부 일정과 체크리스트를 챙기는 역할을 맡는다",
        "option_b": "방향과 전략을 제안하는 역할을 맡는다",
        "letter_a": "D",
        "letter_b": "B",
    },
    {
        "id": 9,
        "axis": 2,
        "text": "무역 뉴스를 볼 때 나는?",
        "option_a": "구체적인 수치와 통계에 집중한다",
        "option_b": "앞으로의 흐름과 시사점에 집중한다",
        "letter_a": "D",
        "letter_b": "B",
    },
    {
        "id": 10,
        "axis": 2,
        "text": "발표 자료를 만든다면 나는?",
        "option_a": "표와 근거자료를 꼼꼼히 채운다",
        "option_b": "큰 그림과 스토리라인을 먼저 짠다",
        "letter_a": "D",
        "letter_b": "B",
    },
    # ---- 축3. 원칙형(R) vs 관계형(H) ----
    {
        "id": 11,
        "axis": 3,
        "text": "거래처가 계약과 다른 요청을 해온다면 나는?",
        "option_a": "계약과 규정 기준으로 정중히 거절한다",
        "option_b": "관계를 생각해 유연하게 조율해본다",
        "letter_a": "R",
        "letter_b": "H",
    },
    {
        "id": 12,
        "axis": 3,
        "text": "업무에서 가장 중요한 가치를 고른다면?",
        "option_a": "정확성과 원칙 준수",
        "option_b": "신뢰와 관계 유지",
        "letter_a": "R",
        "letter_b": "H",
    },
    {
        "id": 13,
        "axis": 3,
        "text": "신규 거래처를 뚫을 때 나는?",
        "option_a": "조건과 신용도를 먼저 꼼꼼히 검토한다",
        "option_b": "사람 대 사람으로 신뢰부터 쌓는다",
        "letter_a": "R",
        "letter_b": "H",
    },
    {
        "id": 14,
        "axis": 3,
        "text": "규정과 관행이 부딪힐 때 나는?",
        "option_a": "규정을 우선한다",
        "option_b": "상황과 관계를 고려해 판단한다",
        "letter_a": "R",
        "letter_b": "H",
    },
    {
        "id": 15,
        "axis": 3,
        "text": "협상 자리에서 나는?",
        "option_a": "원칙과 기준을 분명히 밝힌다",
        "option_b": "상대방 입장을 먼저 듣고 공감한다",
        "letter_a": "R",
        "letter_b": "H",
    },
    # ---- 축4. 안정형(S) vs 유연형(F) ----
    {
        "id": 16,
        "axis": 4,
        "text": "갑자기 선적 일정이 틀어졌다. 나는?",
        "option_a": "정해진 매뉴얼과 절차대로 차분히 대응한다",
        "option_b": "상황에 맞게 즉흥적으로 대안을 찾는다",
        "letter_a": "S",
        "letter_b": "F",
    },
    {
        "id": 17,
        "axis": 4,
        "text": "나의 업무 스타일은?",
        "option_a": "계획을 세우고 그대로 지키는 편",
        "option_b": "상황에 따라 유연하게 바꾸는 편",
        "letter_a": "S",
        "letter_b": "F",
    },
    {
        "id": 18,
        "axis": 4,
        "text": "환율이나 시장이 급변할 때 나는?",
        "option_a": "리스크를 줄이는 안전한 선택을 한다",
        "option_b": "기회로 보고 빠르게 움직인다",
        "letter_a": "S",
        "letter_b": "F",
    },
    {
        "id": 19,
        "axis": 4,
        "text": "여러 업무가 동시에 몰릴 때 나는?",
        "option_a": "우선순위를 정해 순서대로 처리한다",
        "option_b": "임기응변으로 빠르게 처리한다",
        "letter_a": "S",
        "letter_b": "F",
    },
    {
        "id": 20,
        "axis": 4,
        "text": "새로운 규제(예: 관세 변경)가 생기면 나는?",
        "option_a": "매뉴얼·가이드부터 업데이트한다",
        "option_b": "일단 해보면서 감을 잡는다",
        "letter_a": "S",
        "letter_b": "F",
    },
]

# 축 메타데이터 (결과 화면의 점수 그래프 등에 사용)
AXES = {
    1: {"name": "대외지향 vs 대내집중", "a": "G", "b": "L", "a_label": "대외지향형 (Global)", "b_label": "대내집중형 (Local)"},
    2: {"name": "디테일 vs 빅픽처", "a": "D", "b": "B", "a_label": "디테일형 (Detail)", "b_label": "빅픽처형 (Big-picture)"},
    3: {"name": "원칙 vs 관계", "a": "R", "b": "H", "a_label": "원칙형 (Rule)", "b_label": "관계형 (Human)"},
    4: {"name": "안정 vs 유연", "a": "S", "b": "F", "a_label": "안정형 (Stable)", "b_label": "유연형 (Flexible)"},
}
