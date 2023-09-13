
import streamlit as st

st.title("this is title")
st.write("this is text")

# 아래는 마크다운으로 인식함
"""
# This is title
## This is subtitle

- first
- second
"""

# steamlit run app.py


# 정보를 보여주는건 이렇게
# 정보를 받아오는건?

st.text_input("text input")

# 이것만 하면 프론트에서 텍스트 입력해도 아무 일 없음
# 입력한 텍스트를 가져와서 처리하는 코드 필요

text = st.text_input("text input ver2")

st.write(text)


selected = st.checkbox("개인정보 사용에 동의하시겠습니까")

if selected:
    st.success("동의함")

market = st.selectbox("시장", {"코스닥", "코스피", "나스닥"})
st.write(f"selected market: {market}")


options = st.multiselect('종목', ['네이버', '카카오', '삼성전자', '현대자동차'])

st.write(', '.join(options))


# 지표 나타내는 위젯
st.metric(label = "네이버", value =  "200000 원", delta = "-1000 원")





