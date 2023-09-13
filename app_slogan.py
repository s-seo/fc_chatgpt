
import streamlit as st
import requests
# fastapi에 요청보낼 때 requests 라이브러리 사용함


st.title('광고 문구 작성 서비스')

# 난 프론트, 백엔드 간 뭐 주고 받을 때 모듈 임포트 하듯이 뭘 하는줄 알았는데
# url로 호출하고 보내는걸 이제 알았다
# 
generate_ad_slogan_url = "http://localhost:8000/create_ad_slogan"

product_name = st.text_input('제품 이름')
details = st.text_input('주요 내용')
options = st.multiselect('광고 문구의 톤 앤 매너', options = {'기본', '과장스럽게', '차분함', '웃긴'}, default = '기본')

if st.button('광고 문구 생성'):
    try:
        response = requests.post(generate_ad_slogan_url,
                    json= {'product_name': product_name,
                            'details': details,
                            'tone_and_manner': ', '.join(options)})

        ad_slogan = response.json()['ad_slogan']
        st.success(ad_slogan)
    except:
        st.error('예상치 못한 에러가 발생했습니다')


# 백엔드에선 특정 url에 접근하면 어떤 액션을 수행하는 함수를 만들어 놓고 대기
# 프론트에서 버튼 클릭하는 액션 -> 백엔드에서 만들어놓은 url에 post 요청 보냄
# 근데 왜 post지? 광고 문구를 'create'하는거니까
# 백엔드에서 post 요청에 담긴 json을 받아서 openapi 거쳐서 어떤 응답을 받아내고 출력
# 이 때 출력은 딕셔너리로 뱉게끔 백엔드 파일에서 설정함
# 출력값을 받아서 다시 프론트에 쏘는 과정
# 뭔가 살짝 아름답게 느껴지네.. 경이롭기도 하고

