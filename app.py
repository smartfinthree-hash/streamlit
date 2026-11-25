import pandas as pd
import streamlit as st

st.set_page_config(page_title="나의 지출 대시보드", page_icon="💰", layout="centered")
st.title("💰 나의 지출 대시보드")
st.write("항목별 월 지출을 입력하면 합계와 차트를 확인할 수 있습니다.")

categories = ["식비", "교통비", "쇼핑", "통신비", "기타"]
expenses = {}
for category in categories:
    expenses[category] = st.number_input(
        f"{category} (원)", min_value=0, max_value=10_000_000,
        value=100_000 if category == "식비" else 50_000,
        step=10_000,
    )

total = sum(expenses.values())
st.metric("이번 달 총지출", f"{total:,}원")

if total > 0:
    df = pd.DataFrame({"항목": list(expenses), "지출액": list(expenses.values())})
    st.subheader("항목별 지출")
    st.bar_chart(df.set_index("항목"))
    largest = max(expenses, key=expenses.get)
    st.info(f"가장 지출이 큰 항목: {largest} ({expenses[largest]:,}원)")
else:
    st.info("지출액을 입력하면 차트가 나타납니다.")

st.caption("교육 실습용 예제 · 입력한 데이터는 서버에 영구 저장되지 않습니다.")
