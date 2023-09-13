# 번역 서비스

import openai
import streamlit as st

openai.api_key = '*'


def translate_text_using_davinci(text, src_lang, trg_lang):
    response = openai.Completion.create(engine = "text-davinci-003",
                                        prompt = f"Translate the following {src_lang} text to {trg_lang}: {text}",
                                        max_tokens = 200,
                                        n = 1,
                                        temperature = 1)

    translated_text = response.choices[0].text.strip()

    return translated_text


def translate_text_using_chatgpt(text, src_lang, trg_lang):
    system_instruction = f"assistant는 번역앱으로서 동작한다. {src_lang}을 {trg_lang}으로 적절하게 번역하고 번역된 텍스트만 출력한다."

    messages = [{"role": "system", "content": system_instruction},
                {"role": "user", "content": text}]
    
    
    response = openai.ChatCompletion.create(model = "gpt-3.5-turbo",
                                            messages = messages)
    
    translated_text = response['choices'][0]['message']['content']

    return translated_text


st.title("번역 서비스")

# 번역해야 할 text box 필요
# text box 밑에 source language, target language 선택할 수 있는 select box 필요
# 번역 실행 버튼 필요
# 번역 결과 나올 수 있는 박스 필요

# 두번째
text = st.text_area("번역할 텍스트를 입력하세요", "")

src_lang = st.selectbox("원본 언어", ["영어", "한국어", "일본어"])
trg_lang = st.selectbox("목표 언어", ["영어", "한국어", "일본어"], index = 1)

# 기본값은 첫번째 값인데, index를 설정하면, 이 값에 대응하는 값을 기본값으로 설정할 수 있음

if st.button("번역"):

    # 번역 함수 만들어서, text, src_lang, trg_lang) -> translated_text 
    translated_text = translate_text_using_chatgpt(text, src_lang, trg_lang)

    st.success(translated_text)


# text-davinci-003 은 큰 모델. 가격이 비쌈
# 실제 서비스 만들 땐 chatGPT 사용해도


# 텍스트 잘 넣어도 번역 이상한데..
# 이럴 때 prompt engineering 필요
# 몇가지 예제를 주는 Few show 필요
# 어떤 식으로 응답해야 하는지 모델에게 알려주는 작업


def translate_text_using_chatgpt(text, src_lang, trg_lang):
    def build_fewshot(src_lang, trg_lang):
        src_examples = parallel_example[src_lang]
        trg_examples = parallel.example[trg_lang]

        fewshot_messages = []

        for src_text, trg_text in zip(src_examples, trg_examples):
            fewshot_messages.append({"role": "user", "content": src_text})
            fewshot_messages.append({"role": "assistant", "content": trg_text})

        return fewshot_messages

    system_instruction = f"assistant는 번역앱으로서 동작한다. {src_lang}을 {trg_lang}으로 적절하게 번역하고 번역된 텍스트만 출력한다."

    fewshot_messages = build_fewshot(src_lang, trg_lang)

    messages = [{"role": "system", "content": system_instruction},
                *fewshot_messages,
                {"role": "user", "content": text}]
    
    
    response = openai.ChatCompletion.create(model = "gpt-3.5-turbo",
                                            messages = messages)
    
    translated_text = response['choices'][0]['message']['content']

    return translated_text

# fewshot 직접 입력하기 번거로워서 실행은 안 시킴

