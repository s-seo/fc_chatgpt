# 파일 업로드, 다운로드도 같이

import streamlit as st
import requests
import pandas as pd
import os
import io

if 'prev_uploaded_file' not in st.session_state:
    st.session_state['prev_uploaded_file'] = None
    st.session_state['prev_df'] = None

summarize_url = "http://localhost:8000/summarize"

def summarize(text):
    response = requests.post(summarize_url,
                             json = {'text': text})

    summary = response.json()['summary']

    return summary

def summarize_df(df):

    # 다른 함수에 있는 변수에 접근 가능
    global progress_bar

    total = len(df)
    news_summaries = []
    for i, news_origin in enumerate(df['뉴스원문'], start = 1):
        summary = summarize(news_origin)

        news_summaries.append(summary)

        progress_bar.progress(i/total, text = 'progress')
    
    df['뉴스요약'] = news_summaries

    return df

# 일종의 api 사용한다 여기면 됨
# 스닙팻 코드..? 여튼 다른데 쓰이면 그대로 복붙해서 사용하면 됨
def to_excel(df):

    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine = 'xlsxwriter')
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    writer.save()
    processed_data = output.getvalue()

    return processed_data


st.title('요약 서비스')

tab1, tab2 = st.tabs(['실시간', '파일 업로드'])

# 실시간에선 텍스트 붙여넣고, 요약 버튼 누르면 3줄 요약 결과 출력되게
# 파일 업로드에선, 파일 업로드 버튼 눌러 업로드하면, 그 파일에 대해 요약된 엑셀을 테이블 형식으로 출력 후 다운로드 받는 버튼 제공

# 왜 with으로 감쌀까?
with tab1:
    input_text = st.text_area('여기에 텍스트를 입력하세요', height = 300)
    if st.button('요약'):
        if input_text:
            try:
                summary = summarize(input_text)
                st.success(summary)
            except:
                st.error('에러 발생')
        else:
            st.warning('텍스트를 입력하세요')


# 두번째 탭에서만 만들도록 하는 역할
with tab2:
    uploaded_file = st.file_uploader('Choose a file')

    if uploaded_file:
        st.success('업로드 성공')

        if uploaded_file == st.session_state['prev_uploaded_file']:
            df = st.session_state['prev_df']
            # df 할당만 하고 그 이후 프로세스 없으니 그냥 멈춘 것처럼 보임
        else:
            progress_bar = st.progress(0, text = 'progress')

            df = pd.read_excel(uploaded_file)

            df = summarize_df(df)

            st.dataframe(df)

            st.session_state['prev_uploaded_file'] = uploaded_file
            st.session_state['prev_df'] = df

        file_base_name = os.path.splitext(os.path.basename(uploaded_file.name))[0]

        st.download_button(
            label = 'Download',
            data = to_excel(df),
            file_name = f'{file_base_name}_summarized.xlsx'
        )

# download 버튼 누르면 페이지 다시 실행되는데, streamlit 자체 문제..
# 이걸 막으려면?
# 지난번 이미 업로드된 파일이면 다시 로드 안하도록 하는 제어문 필요
# 아래 코드를 Py 파일 맨 위에

# if 'prev_uploaded_file' not in st.session_state:
#     st.session_state['prev_uploaded_file'] = None
#     st.session_state['prev_df'] = None



