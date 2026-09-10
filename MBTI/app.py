# -*- coding: utf-8 -*-
"""
무역 MBTI (TradeType) - Streamlit 메인 앱

화면 흐름: 인트로 -> 질문(20문항) -> 결과
"""

import streamlit as st
import pandas as pd

from data.questions import QUESTIONS, AXES
from data.jobs import JOBS
from logic.scoring import get_result

st.set_page_config(page_title="무역 MBTI | TradeType", page_icon="🌏", layout="centered")

AXIS_ICONS = {1: "🌐", 2: "🔍", 3: "🤝", 4: "🧭"}


# ---------------------------------------------------------------------------
# 커스텀 스타일 (폰트 크기 확대, 카드형 UI, 모바일 대응)
# ---------------------------------------------------------------------------
def inject_custom_css():
    st.markdown(
        """
        <style>
        :root {
            --tm-primary: #2563EB;
            --tm-primary-dark: #1D4ED8;
            --tm-card-bg: var(--secondary-background-color, #F1F5F9);
        }

        /* 전체 컨텐츠 폭 & 여백: 데스크톱에서 너무 넓게 퍼지지 않도록, 모바일에선 % 기반이라 자동으로 꽉 참 */
        .block-container {
            max-width: 760px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* 본문 텍스트를 기본값보다 살짝 크고 읽기 편하게 */
        [data-testid="stMarkdownContainer"] p {
            font-size: 1.05rem;
            line-height: 1.7;
        }

        /* 인트로 / 결과 상단에 쓰는 히어로 카드 */
        .hero-card {
            background: linear-gradient(135deg, var(--tm-primary), var(--tm-primary-dark));
            color: #FFFFFF !important;
            border-radius: 20px;
            padding: 2rem 1.5rem;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .hero-card * { color: #FFFFFF !important; }
        .hero-emoji { font-size: 2.6rem; margin-bottom: 0.3rem; }
        .hero-title { font-size: 1.9rem; font-weight: 800; }
        .hero-code { font-size: 2.3rem; font-weight: 800; letter-spacing: 0.04em; }
        .hero-job { font-size: 1.5rem; font-weight: 700; margin-top: 0.3rem; }
        .hero-catch { font-size: 1.1rem; opacity: 0.92; margin-top: 0.6rem; }

        /* 축 뱃지 */
        .axis-badge {
            display: inline-block;
            background: var(--tm-card-bg);
            color: var(--tm-primary);
            border: 1px solid var(--tm-primary);
            border-radius: 999px;
            padding: 0.25rem 0.9rem;
            font-size: 0.85rem;
            font-weight: 700;
            margin-bottom: 0.9rem;
        }

        /* 질문 텍스트 - 눈에 띄게 크게 */
        .question-text {
            font-size: 1.5rem;
            font-weight: 700;
            line-height: 1.55;
            margin: 0 0 1.1rem 0;
        }

        /* 라디오 선택지: 카드처럼 보이게 + 글자 크게 (요청사항: 선택지 글자가 작아서 안 보임) */
        div[data-testid="stRadio"] > div[role="radiogroup"] {
            gap: 0.7rem;
        }
        div[data-testid="stRadio"] label {
            background: var(--tm-card-bg);
            border: 2px solid transparent;
            border-radius: 14px;
            padding: 1rem 1.1rem !important;
            width: 100%;
            transition: all 0.15s ease;
        }
        div[data-testid="stRadio"] label:hover {
            border-color: var(--tm-primary);
        }
        div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {
            font-size: 1.2rem !important;
            line-height: 1.6 !important;
            font-weight: 500;
            margin: 0;
        }

        /* 버튼 */
        .stButton button, .stDownloadButton button {
            border-radius: 12px;
            padding: 0.7rem 1.1rem;
            font-weight: 700;
            font-size: 1.05rem;
        }

        /* 진행바 두껍고 둥글게 */
        div[data-testid="stProgress"] div[role="progressbar"] {
            height: 14px;
            border-radius: 999px;
        }

        /* 섹션 소제목 */
        .section-title {
            font-size: 1.15rem;
            font-weight: 700;
            margin: 0.2rem 0 0.6rem 0;
        }

        /* ---- 모바일 화면 대응 ---- */
        @media (max-width: 480px) {
            .block-container { padding-left: 1rem; padding-right: 1rem; }
            .hero-title, .hero-code { font-size: 1.6rem; }
            .hero-job { font-size: 1.25rem; }
            .question-text { font-size: 1.3rem; }
            div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {
                font-size: 1.05rem !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_header(text):
    st.markdown(f"<div class='section-title'>{text}</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# session_state 초기화
# ---------------------------------------------------------------------------
def _init_state():
    if "stage" not in st.session_state:
        st.session_state.stage = "intro"  # intro -> quiz -> result
    if "answers" not in st.session_state:
        st.session_state.answers = [None] * len(QUESTIONS)
    if "current_q" not in st.session_state:
        st.session_state.current_q = 0


def reset_quiz():
    st.session_state.stage = "intro"
    st.session_state.answers = [None] * len(QUESTIONS)
    st.session_state.current_q = 0


# ---------------------------------------------------------------------------
# 화면 1. 인트로
# ---------------------------------------------------------------------------
def render_intro():
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-emoji">🌏</div>
            <div class="hero-title">무역 MBTI</div>
            <div class="hero-catch">나에게 맞는 무역 직무는?</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        "20개의 질문에 답하면 4개의 축으로 당신의 성향을 진단하고, "
        "무역 분야 대표 직무 6가지 중 가장 잘 맞는 하나를 찾아드려요."
    )
    st.caption("⏱ 소요 시간 약 3분 · 정답은 없어요, 솔직하고 편하게 답해주세요!")

    st.write("")
    section_header("어떤 축으로 진단하나요?")
    cols = st.columns(2)
    for i, axis_num in enumerate(sorted(AXES.keys())):
        meta = AXES[axis_num]
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"**{AXIS_ICONS[axis_num]} 축{axis_num}. {meta['name']}**")
                st.caption(f"{meta['a_label']} vs {meta['b_label']}")

    st.write("")
    if st.button("시작하기 →", type="primary", use_container_width=True):
        st.session_state.stage = "quiz"
        st.rerun()


# ---------------------------------------------------------------------------
# 화면 2. 질문
# ---------------------------------------------------------------------------
def render_quiz():
    total = len(QUESTIONS)
    idx = st.session_state.current_q
    question = QUESTIONS[idx]
    axis_meta = AXES[question["axis"]]

    st.progress(idx / total)
    st.caption(f"{idx + 1} / {total} 문항")

    with st.container(border=True):
        st.markdown(
            f"<span class='axis-badge'>{AXIS_ICONS[question['axis']]} 축{question['axis']} · "
            f"{axis_meta['name']}</span>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='question-text'>Q{question['id']}. {question['text']}</div>",
            unsafe_allow_html=True,
        )

        current_answer = st.session_state.answers[idx]
        choice = st.radio(
            label="선택해주세요",
            options=["A", "B"],
            format_func=lambda opt: (
                f"A) {question['option_a']}" if opt == "A" else f"B) {question['option_b']}"
            ),
            index=None if current_answer is None else ["A", "B"].index(current_answer),
            key=f"radio_{question['id']}",
            label_visibility="collapsed",
        )

    col1, col2 = st.columns([1, 1])
    with col1:
        if idx > 0:
            if st.button("← 이전", use_container_width=True):
                st.session_state.current_q -= 1
                st.rerun()
    with col2:
        next_label = "결과보기 →" if idx == total - 1 else "다음 →"
        if st.button(next_label, type="primary", use_container_width=True, disabled=(choice is None)):
            st.session_state.answers[idx] = choice
            if idx == total - 1:
                st.session_state.stage = "result"
            else:
                st.session_state.current_q += 1
            st.rerun()


# ---------------------------------------------------------------------------
# 화면 3. 결과
# ---------------------------------------------------------------------------
def render_result():
    result = get_result(st.session_state.answers)
    job = result["job"]
    type_code = result["type_code"]

    st.balloons()

    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-code">당신은 {type_code}형</div>
            <div class="hero-job">🎉 {job['name']}</div>
            <div class="hero-catch">{job['catchphrase']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        section_header("📋 하는 일")
        st.write(job["description"])
        section_header("🕒 하루 일과 예시")
        st.write(job["day_example"])
        section_header("🎯 왜 나와 잘 맞을까?")
        st.write(job["reason"])

    with st.container(border=True):
        section_header("📊 축별 점수")
        chart_rows = []
        for axis_num in sorted(AXES.keys()):
            meta = AXES[axis_num]
            scores = result["axis_scores"][axis_num]
            chart_rows.append({"성향": meta["a_label"], "점수": scores["A"]})
            chart_rows.append({"성향": meta["b_label"], "점수": scores["B"]})
        chart_df = pd.DataFrame(chart_rows).set_index("성향")
        st.bar_chart(chart_df)

    with st.container(border=True):
        section_header("🎓 어울리는 활동 & 관련 자격증")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**어울리는 활동/동아리**")
            for act in job["activities"]:
                st.markdown(f"- {act}")
        with col2:
            st.markdown("**관련 자격증**")
            for cert in job["certs"]:
                st.markdown(f"- {cert}")

    compat_key, compat_desc = job["compatible"]
    with st.container(border=True):
        section_header("🤝 궁합이 좋은 직무")
        st.info(f"**{JOBS[compat_key]['name']}** — {compat_desc}")

    st.write("")

    share_text = (
        f"[무역 MBTI 결과]\n"
        f"나는 {type_code}형, {job['name']}!\n"
        f"{job['catchphrase']}\n\n"
        f"{job['description']}\n\n"
        f"-- 무역 MBTI(TradeType)에서 테스트해보세요 --\n"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 다시 하기", use_container_width=True):
            reset_quiz()
            st.rerun()
    with col2:
        st.download_button(
            "📤 결과 저장하기 (.txt)",
            data=share_text,
            file_name=f"trade_mbti_{type_code}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with st.expander("결과 텍스트 복사해서 공유하기"):
        st.code(share_text, language=None)


# ---------------------------------------------------------------------------
# 메인
# ---------------------------------------------------------------------------
def main():
    inject_custom_css()
    _init_state()
    stage = st.session_state.stage
    if stage == "intro":
        render_intro()
    elif stage == "quiz":
        render_quiz()
    elif stage == "result":
        render_result()
    else:
        reset_quiz()
        st.rerun()


if __name__ == "__main__":
    main()
