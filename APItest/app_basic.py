# 날씨 & 해당 국가 환율 자동 연동 대시보드
# pip install requests python-dotenv streamlit

import os
from pathlib import Path
import requests
import streamlit as st
from dotenv import load_dotenv

# 1. 상위 디렉터리(..)의 .env 파일 로드
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
EXCHANGE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")

# 2. 국가 코드(ISO2) -> 공식 통화 코드(ISO 4217) 매핑 테이블
COUNTRY_CURRENCY_MAP = {
    "KR": ("KRW", "대한민국 원", "₩", 1),
    "US": ("USD", "미국 달러", "$", 1),
    "JP": ("JPY", "일본 엔", "¥", 100),       # 100엔 기준
    "CN": ("CNY", "중국 위안", "¥", 1),
    "GB": ("GBP", "영국 파운드", "£", 1),
    "VN": ("VND", "베트남 동", "₫", 100),     # 100동 기준
    "TH": ("THB", "태국 바트", "฿", 1),
    "TW": ("TWD", "대만 달러", "NT$", 1),
    "HK": ("HKD", "홍콩 달러", "HK$", 1),
    "SG": ("SGD", "싱가포르 달러", "S$", 1),
    "AU": ("AUD", "호주 달러", "A$", 1),
    "CA": ("CAD", "캐나다 달러", "C$", 1),
    "CH": ("CHF", "스위스 프랑", "CHF", 1),
    "PH": ("PHP", "필리핀 페소", "₱", 1),
    # 유로존 주요 국가
    "FR": ("EUR", "유로", "€", 1),
    "DE": ("EUR", "유로", "€", 1),
    "IT": ("EUR", "유로", "€", 1),
    "ES": ("EUR", "유로", "€", 1),
    "NL": ("EUR", "유로", "€", 1),
    "BE": ("EUR", "유로", "€", 1),
    "AT": ("EUR", "유로", "€", 1),
}

# 3. Streamlit 페이지 설정
st.set_page_config(page_title="City Weather & Local FX", page_icon="🌍", layout="wide")

st.title("🌍 도시별 실시간 날씨 & 맞춤 환율 대시보드")
st.caption("선택한 도시의 날씨와 해당 국가의 실시간 환율이 자동으로 동기화됩니다.")

if not WEATHER_API_KEY:
    st.error("⚠️ `.env` 파일에서 `OPENWEATHER_API_KEY`를 찾을 수 없습니다.")
    st.stop()

# 4. 사이드바 컨트롤
with st.sidebar:
    st.header("⚙️ 도시 선택")
    default_cities = [
        "Seoul", "Tokyo", "Qingdao", "New York", "London", 
        "Paris", "Bangkok", "Singapore", "Sydney", "직접 입력"
    ]
    selected_option = st.selectbox("도시 목록", default_cities, index=0)
    
    if selected_option == "직접 입력":
        city_name = st.text_input("도시 영문명 입력", value="Osaka")
    else:
        city_name = selected_option
        
    units = st.radio("온도 단위", options=["metric", "imperial"], format_func=lambda x: "섭씨 (°C)" if x == "metric" else "화씨 (°F)")
    unit_symbol = "°C" if units == "metric" else "°F"
    
    st.button("데이터 새로고침", type="primary", use_container_width=True)

# 5. API 데이터 호출 함수 (캐싱 적용)
@st.cache_data(ttl=600)
def get_weather(city: str, api_key: str, unit: str):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": unit, "lang": "kr"}
    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            return None, "도시를 찾을 수 없습니다. 영문 철자를 확인해주세요."
        elif response.status_code == 401:
            return None, "Weather API 키가 유효하지 않습니다."
        return None, f"HTTP 오류: {response.status_code}"
    except Exception as err:
        return None, f"네트워크 오류: {err}"

@st.cache_data(ttl=1800)
def get_exchange_rates(api_key: str):
    if not api_key:
        return None, "`.env`에 `EXCHANGERATE_API_KEY`가 설정되지 않았습니다."
    
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("result") == "success":
            return data.get("conversion_rates"), None
        return None, f"환율 API 오류: {data.get('error-type', '알 수 없음')}"
    except Exception as err:
        return None, f"환율 조회 실패: {err}"

# 6. 메인 화면 렌더링
if city_name:
    weather_data, w_err = get_weather(city_name, WEATHER_API_KEY, units)
    rates, fx_err = get_exchange_rates(EXCHANGE_API_KEY)

    if w_err:
        st.error(w_err)
    elif weather_data:
        country_code = weather_data.get("sys", {}).get("country", "")
        city_display_name = weather_data.get("name", city_name)
        
        # 통화 매핑 확인 (등록되지 않은 국가는 기본 USD 처리)
        curr_code, curr_name, curr_symbol, base_unit = COUNTRY_CURRENCY_MAP.get(
            country_code, ("USD", "미국 달러(기본값)", "$", 1)
        )

        st.subheader(f"📍 {city_display_name} ({country_code}) 실시간 현황")

        # 상단: 날씨 & 해당 국가 환율 요약 (2열 반응형)
        col_weather_hero, col_fx_hero = st.columns([1, 1])

        # 날씨 요약 카드
        with col_weather_hero:
            weather_main = weather_data["weather"][0]
            main_stats = weather_data["main"]
            icon_url = f"https://openweathermap.org/img/wn/{weather_main['icon']}@2x.png"

            st.markdown("##### 🌤️ 현재 날씨")
            w_sub1, w_sub2 = st.columns([1, 3])
            with w_sub1:
                st.image(icon_url, width=80)
            with w_sub2:
                st.markdown(f"### {main_stats['temp']}{unit_symbol} ({weather_main['description']})")
                st.caption(f"체감 {main_stats['feels_like']}{unit_symbol} | 최고 {main_stats['temp_max']}{unit_symbol} / 최저 {main_stats['temp_min']}{unit_symbol}")

        # 해당 국가 환율 요약 카드
        with col_fx_hero:
            st.markdown(f"##### 💱 현지 통화 환율: {curr_name} ({curr_code})")
            
            if fx_err:
                st.warning(fx_err)
            elif rates:
                krw_per_usd = rates.get("KRW", 1)
                curr_per_usd = rates.get(curr_code, 1)

                if curr_code == "KRW":
                    st.info("💡 선택하신 도시는 대한민국(KRW)이므로 환율 계산이 필요하지 않습니다.")
                else:
                    # KRW 기준 교차 환율 계산
                    rate_krw = (krw_per_usd / curr_per_usd) * base_unit
                    unit_label = f"{base_unit} {curr_code}" if base_unit > 1 else f"1 {curr_code}"
                    
                    st.metric(
                        label=f"{unit_label} 기준 원화(KRW)",
                        value=f"₩ {rate_krw:,.2f}"
                    )
                    st.caption(f"통화 기호: {curr_symbol} | 기준: 1 USD = ₩{krw_per_usd:,.1f}")

        st.divider()

        # 하단 1: 날씨 세부 지표
        st.markdown("##### 📊 상세 날씨 지표")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("습도", f"{weather_data['main']['humidity']}%")
        m2.metric("풍속", f"{weather_data['wind']['speed']} m/s")
        m3.metric("기압", f"{weather_data['main']['pressure']} hPa")
        m4.metric("가시거리", f"{weather_data.get('visibility', 0) / 1000:.1f} km")

        # 하단 2: 현지 통화 즉시 환전기 & 글로벌 주요 통화
        if rates and curr_code != "KRW":
            st.divider()
            calc_col, global_col = st.columns([1, 1])

            # 좌측: 해당 도시 통화 맞춤 계산기
            with calc_col:
                st.markdown(f"##### 🔢 {city_display_name} 현지 경비 계산기")
                calc_val = st.number_input(
                    f"현지 금액 입력 ({curr_code})",
                    min_value=0.0,
                    value=float(100 * base_unit),
                    step=10.0
                )
                krw_calc = (calc_val / base_unit) * rate_krw
                st.success(f"👉 원화 환산액: **₩ {krw_calc:,.0f} 원**")

            # 우측: 글로벌 3대 통화 보조 지표
            with global_col:
                st.markdown("##### 🌐 글로벌 주요 통화 참고")
                g1, g2 = st.columns(2)
                g1.metric("USD / KRW", f"₩ {krw_per_usd:,.2f}")
                jpy_krw = (krw_per_usd / rates.get("JPY", 1)) * 100
                g2.metric("100 JPY / KRW", f"₩ {jpy_krw:,.2f}")