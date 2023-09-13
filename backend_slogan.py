
# fastapi api 서버
# openai api를 활용해서 만든 광고 문구 작성 함수를 호출
# 이 함수를 먼저 만들고, fastapi 서버로 서빙하는 형태

from fastapi import FastAPI
from pydantic import BaseModel
import os
import openai

openai.api_key = "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"

# 클래스로 여러 api 함수를 감싸는 형태

class SolganGenerator:
    def __init__(self, engine = 'gpt-3.5-turbo'):
        self.engine = engine
        self.infer_type = self._get_infer_type_by_engine(engine) # or completion

    # under-score(_) 를 붙이면 이 클래스 내에서만 사용함을 명시적으로 알리는데 있음
    # 기능적으론 아무 의미 없음.
    def _get_infer_type_by_engine(self, engine):
        if engine.startswith("text-"):
            return 'completion'
        elif engine.startswith("gpt-"):
            return 'chat'
        
        return Exception(f'Unknown engine type: {engine}')

    def _infer_using_completion(self, prompt):
        response = openai.Completion.create(engine = self.engine,
                                            prompt = prompt,
                                            max_tokens = 200,
                                            n = 1)
        
        result = response.choices[0].text.strip()

        return result
    
    def _infer_using_chatgpt(self, prompt):
        system_instruction = "assistant는 마케팅 문구 작성 도우미로 동작한다. user의 내용을 참고하여 마케팅 문구를 작성해라"

        messages = [{"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}]
        
        response = openai.ChatCompletion.create(model = self.engine,
                                                messages = messages)

        result = response['choices'][0]['message']['content']

        return result

    # 외부에서 호출할 함수
    def generate(self, product_name, details, tone_and_manner):
        prompt = f'제품 이름: {product_name}\n주요 내용: {details}\n광고 문구의 스타일: {tone_and_manner} 위 내용을 참고하여 마케팅 문구를 만들어라'

        if self.infer_type == 'completion':
            result = self._infer_using_completion(prompt = prompt)
        elif self.infer_type == 'chat':
            result = self._infer_using_chatgpt(prompt = prompt)

        return result

# slogan_generator = SolganGenerator(engine = 'gpt-3.5-turbo')
# result = slogan_generator.generate('나이키 신발', details = '이쁘고 편안합니다', tone_and_manner = '과장')
# print(result)

app = FastAPI()

# post로 api를 만들거라 입력받을 데이터 형식을 미리 지정
class Product(BaseModel):
    product_name: str
    details: str
    tone_and_manner: str

@app.post("/create_ad_slogan")
def create_ad_slogan(product: Product):
    slogan_generator = SolganGenerator('gpt-3.5-turbo')

    ad_slogan = slogan_generator.generate(product_name = product.product_name,
                                          details = product.details,
                                          tone_and_manner= product.tone_and_manner)
    
    return {'ad_slogan': ad_slogan}

# 이 api를 streamlit 에서 호출할 수 있게 해볼 것
