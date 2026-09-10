# kljsdfsdl kjfklsdjf klsd
# sdf lsdfkjsdklfsdlkfj sdkljf setsdflk jsdfj sdklfj
# sdkf jsdlkf
# sdflk sdl;ksd
# sdf l;skdf sortedsd;fl ksdf
# sdf dsl;k jsdf
#  sd
import os
import pandas as pd
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="수출 실적 분석 리포트",
    page_icon="📊",
    layout="wide"
)

st.title("📊 HS 85(반도체류) 대미·대베트남 수출 상위 10건 분석")

# 2. 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMMON_DIR = os.path.join(BASE_DIR, "..", "common")
DATA_PATH = os.path.join(COMMON_DIR, "raw_trade_data.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "report.csv")

# 3. 데이터 로드 함수
@st.cache_data
def load_data(filepath):
    if not os.path.exists(filepath):
        alt_path = os.path.join("common", "raw_trade_data.csv")
        if os.path.exists(alt_path):
            filepath = alt_path
        else:
            return None
    try:
        return pd.read_csv(filepath, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(filepath, encoding="cp949")

df = load_data(DATA_PATH)

if df is None:
    st.error(f"❌ 파일을 찾을 수 없습니다: `{DATA_PATH}`")
else:
    # 컬럼명 앞뒤 공백 정리
    df.columns = df.columns.astype(str).str.strip()

    # 영문/한글 컬럼명 유연하게 매핑 (hs_code 등 지원)
    col_hs = "hs_code" if "hs_code" in df.columns else "HS코드"
    
    # 국가명 컬럼 탐색
    for c in ["국가명", "country", "stat_cd_kor", "cntry_nm"]:
        if c in df.columns:
            col_country = c
            break
    else:
        col_country = "국가명"

    # 수출금액 컬럼 탐색
    for c in ["수출금액", "export_amount", "exp_amt", "expusd"]:
        if c in df.columns:
            col_amount = c
            break
    else:
        col_amount = "수출금액"

    # 필수 컬럼 존재 확인
    if col_hs not in df.columns or col_country not in df.columns or col_amount not in df.columns:
        st.error(f"❌ 필요한 컬럼을 확인해주세요. 인식된 컬럼: HS코드(`{col_hs}`), 국가(`{col_country}`), 수출액(`{col_amount}`)")
        st.info(f"현재 파일 컬럼 목록: {list(df.columns)}")
    else:
        # 4. 다중 조건 필터링
        # (1) HS코드: 85로 시작
        hs_series = (
            df[col_hs]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.replace(r"\.0$", "", regex=True)
        )
        cond_hs = hs_series.str.startswith("85")

        # (2) 국가명: 미국 또는 베트남 (영문 표기 'USA', 'Vietnam' 포함 대응)
        target_countries = ["미국", "베트남", "USA", "United States", "Vietnam", "VIET NAM"]
        cond_country = df[col_country].astype(str).str.strip().isin(target_countries)

        # (3) 수출금액: 0 초과 (문자열 콤마 제거 후 수치 변환)
        numeric_amount = pd.to_numeric(
            df[col_amount].astype(str).str.replace(",", "").str.strip(),
            errors="coerce"
        ).fillna(0)
        cond_amount = numeric_amount > 0


        # 필터링 적용
        filtered_df = df[cond_hs & cond_country & cond_amount].copy()
        filtered_df[col_amount] = numeric_amount[cond_hs & cond_country & cond_amount]

        # 5. 상위 10건 내림차순 정렬
        top10_df = (
            filtered_df.sort_values(by=col_amount, ascending=False)
            .head(10)
            .reset_index(drop=True)
        )

        # 6. report.csv 자동 저장 (Excel 한글 깨짐 방지: utf-8-sig)
        top10_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

        # 7. 화면 지표 및 테이블 출력
        col1, col2, col3 = st.columns(3)
        col1.metric("조건 부합 건수", f"{len(filtered_df):,}건")
        col2.metric("상위 10건 총 수출액", f"{top10_df[col_amount].sum():,.0f}")
        col3.metric("최고 수출액", f"{top10_df[col_amount].max():,.0f}" if len(top10_df) > 0 else "0")

        st.write("")
        st.subheader("📋 수출금액 상위 10건 내역")
        st.dataframe(top10_df, use_container_width=True)

        st.success(f"✅ 상위 10건 데이터가 `{OUTPUT_PATH}` 파일로 자동 저장되었습니다.")

        # 브라우저 다운로드 버튼
        csv_bytes = top10_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
        st.download_button(
            label="📥 report.csv 브라우저 다운로드",
            data=csv_bytes,
            file_name="report.csv",
            mime="text/csv",
        )