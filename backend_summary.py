

import openai

openai.api_key = "*"


# 요약 함수를 먼저 만들고 api로 올려보자
def summarize(text):
    system_instruction = "assistant는 user의 입력을 bullet point로 3줄 요약해준다."

    messages = [{"role": "system", "content": system_instruction},
                {"role": "user", "content": text}]
    
    response = openai.ChatCompletion.create(model = 'gpt-3.5-turbo',
                                            messages = messages)
    
    result = response['choices'][0]['message']['content']

    return result

text = """
웹에는 CRUD 라는 개념이 있음. create, read, update, delete. 컴퓨터에 어떤 정보를 만들면 create. 이미 저장된 정보를 읽으면 read. 저장된 정보를 업데이트하는 것. 저장된 정보를 지우는 것. 컴퓨터와 상호작용하는 많은 행위를 추상홯하면 위 네 개로 분류할 수 있음
"""

print(summarize(text))


# from fastapi import FastAPI
# from pydantic import BaseModel
# # pydantic은 post 메서드 사용할 때 필요
# import openai

# openai.api_key = "*"

# def summarize(text):
#     system_instruction = "assistant는 user의 입력을 bullet point로 3줄 요약해준다."

#     messages = [{"role": "system", "content": system_instruction},
#                 {"role": "user", "content": text}]
    
#     response = openai.ChatCompletion.create(model = 'gpt-3.5-turbo',
#                                             messages = messages)
    
#     result = response['choices'][0]['message']['content']

#     return result

# app = FastAPI()

# class InputText(BaseModel):
#     text: str

# @app.post("/summarize")
# def post_summarize(input_text: InputText):
#     summary = summarize(input_text.text)

#     return {"summary": summary}


# # 백엔드는 이렇게 간단하게 했고, 잘 띄워졌는데 swagger로 확인함
# # uvicorn backend_summary:app --reload

