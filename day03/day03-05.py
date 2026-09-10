# 인코딩 자동 감지 + 한글 폰트 막대그래프
# 여러 인코딩("utf-8-sig", "cp949", "euc-kr") 순서대로 시도
# 내가 쓸 폰트 같은 경로에 있어에 함
#객실등급별 생존율 막대그래프 생성후 그림으로 저장  chart.png
# 실행 streamlit run day03-05.py.

import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from matplotlib import font_manager


st.title("📊 인코딩 자동 감지 + 한글 폰트 막대그래프 (Titanic 연습)")
st.caption("여러 인코딩을 순서대로 시도해서 파일을 읽고, 객실등급별 생존율을 그래프로 그립니다.")

CSV_PATH = os.path.join(os.path.dirname(__file__),"titanic_cleaned.csv") 
FONT_PATH=os.path.join(os.path.dirname(__file__),"NanumGothicEco.otf") 


def read_csv_with_auto_encoding(file_path: str, **kwargs) -> pd.DataFrame:
    """
    여러 인코딩('utf-8-sig', 'cp949', 'euc-kr')을 순서대로 시도하여
    CSV 파일을 불러오는 함수입니다.
    """
    encodings = ["utf-8-sig", "cp949", "euc-kr"]
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding, **kwargs)
            st.write(f"{encoding}으로 읽었습니다")
            return df
        except UnicodeDecodeError:
            continue
            
    raise ValueError(f"지원하는 인코딩({encodings})으로 파일을 디코딩할 수 없습니다: {file_path}")



# 인코딩 자동 감지로 Csv읽기
st.subheader("1) 인코딩 자동 감지")

df = read_csv_with_auto_encoding(CSV_PATH)

st.markdown("---")
# 객실등급(Pclass) 별 생존율집계
# Survived 사망0 / 생존1 등급별 평균을 내면
#  그대로가 등급의 생존 비율이 된다
# 10명 남 3 여자7
# 1000  생존300   300/1000 0.3


 
pclass_survival_rate = df.groupby("Pclass")["Survived"].mean().sort_index()
st.dataframe(  (pclass_survival_rate * 100 ).round(1).rename("생존율(%)")  )

# df_df = st.dataframe(  (pclass_survival_rate * 100 ).round(1).rename("생존율(%)")  )
# st.write(df_df)

 
# 차트 그리기


st.markdown("---")
st.subheader("3)  객실등급별 생존율 막대그래프")
try :
    # 폰트 파일이 없으면 FileNotFoundError 가 발생
    font_prop = font_manager.FontProperties(fname=FONT_PATH)
    # matplotlib font_manager에 폰트를 등록하고, 전역 폰트로 설정
    font_manager.fontManager.addfont(FONT_PATH)
    plt.rcParams["font.family"]= font_prop.get_name()    
    st.write("NanumGothicEco 폰트를 적용했습니다")
except FileNotFoundError:
    st.warning("NanumGothicEco 폰트파일을 찾을수가 없습니다.")


fig, ax = plt.subplots(figsize=(8,5))
(pclass_survival_rate * 100 ).plot(kind="bar", color="blue", ax=ax)
ax.set_title("객실 등급별 생존율")
ax.set_xlabel("객실등급(Pclass)")
ax.set_ylabel("생존율(%)")

st.pyplot(fig)

output_png = output_path = os.path.join(os.path.dirname(__file__),"chart.png")
fig.savefig(output_png)







