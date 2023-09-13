# conda create --name chatgptapi python=3.8
# conda activate chatgptapi
# conda deactivate

import os
import openai

# openai API key 발급 받아야 함

# Load your API key from an environment variable or secret management service
# openai.api_key = "<OPENAI_API_KEY>"
# export OPEN_API_KEY = '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'
# 위 구문으로 환경변수 설정해서 os.getenv('OPENAI_API_KEY')로 가져올 수 있음
openai.api_key = "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"


# prompt = """
# 다음 문장이 긍정이면 positive, 부정이면 negative를 만들어라

# text: 이 영화 최악이다
# sentiment: negative

# text: 배우들이 연기를 너무 잘하네
# sentiment: positive

# text: 이 영화 나쁘네 """

# prompt = prompt + "\nsentiment: "

# response = openai.Completion.create(model="text-davinci-003",
#                                     prompt=prompt,
#                                     temperature=0,
#                                     max_tokens=7)
# print(response)
# print(response['choices'][0]['text'])






# ChatCompletion API 는?
# system - user 순서의 대화형 API
# user의 응답을 돕는 assistant도 있음
# 이걸 딕셔너리 형태의 인풋으로 메서드에 부여함









# system_instruction = """
# 너는 햄버거 가게 AI비서야

# 아래는 햄버거 종류야. 아래 종류의 버거 말고는 다른 버거는 없어

# - 빅맥
# - 쿼터파운더
# - 치즈버거

# 위의 메뉴 말고는 없다고 생각하면돼
# """

# messages = [{"role": "system", "content": system_instruction}]

# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=messages)

# print(response.to_dict_recursive())







# 챗봇으로 만듦

system_instruction = """
너는 햄버거 가게 AI비서야

아래는 햄버거 종류야. 아래 종류의 버거 말고는 다른 버거는 없어

- 빅맥
- 쿼터파운더
- 치즈버거

위의 메뉴 말고는 없다고 생각하면돼
"""

messages = [{"role": "system", "content": system_instruction}]

def ask(text):
    user_input = {"role": "user", "content": text}
    messages.append(user_input)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)

    bot_text = response['choices'][0]['message']['content']
    # 이걸로 문맥이 형성되는건가..? 신기하네
    bot_resp = {"role": "assistant", "content": bot_text}
    messages.append(bot_resp)
    return bot_text

# print(ask('뭐가 있죠'))

while True:
    user_input = input("user input: ")
    bot_resp = ask(user_input)

    print("-"*30)anj
    print(f"user_input: {user_input}")
    print(f"bot_resp: {bot_resp}")

