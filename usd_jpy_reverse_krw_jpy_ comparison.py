import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import streamlit as st

# Streamlit 제목 설정
st.title("USD/JPY 환율(반전상태) 엔원 비교")

# 날짜 입력 위젯
start_date = st.date_input("시작 날짜", pd.to_datetime("2024-05-01"))
end_date = st.date_input("종료 날짜", pd.to_datetime("2024-05-30"))

# 데이터 다운로드
jpy_krw = yf.download("JPYKRW=X", start=start_date, end=end_date)
jpy_usd = yf.download("JPY=X", start=start_date, end=end_date)

# # jpy_krw 끝에서 20개 출력
# st.table(jpy_krw.tail(10))
# st.table(jpy_usd.tail(10))


# 주가 데이터만 사용 (종가)
jpy_krw_close = jpy_krw['Close']
jpy_usd_close = jpy_usd['Close']

# USD/JPY 환율을 JPY/USD로 변환
jpy_usd_close_r = 1 / jpy_usd_close

# # 정규화
jpy_krw_close_norm = jpy_krw_close / jpy_krw_close.iloc[0]
jpy_usd_close_r_norm = jpy_usd_close_r / jpy_usd_close_r.iloc[0]

# # 데이터프레임 합치기
data_norm = pd.DataFrame({'jpy_krw': jpy_krw_close_norm, 'jpy_usd': jpy_usd_close_r_norm})

# # NaN 값 제거
data_norm.dropna(inplace=True)

# # 그래프 그리기
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(data_norm.index, data_norm['jpy_krw'], label='jpy_krw', color='blue')
ax.plot(data_norm.index, data_norm['jpy_usd'], label='jpy_usd', color='red')
# ax.set_title('S&P 500 지수와 애플 주가 비교 (정규화)')
ax.set_xlabel('날짜')
ax.set_ylabel('정규화된 주가')
ax.legend()
ax.grid(True)

# # Streamlit에 그래프 표시
st.pyplot(fig)
