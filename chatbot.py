# -*- coding: utf-8 -*-
"""Chatbot.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cZSBTwlMLFTiA5WVxSHXOHs5hbxXG0Qs
"""

import os
import pandas as pd

def calc_distance(a, b):
    if a == b:
        return 0  # 같으면 0을 반환
    a_len = len(a)  # a 길이
    b_len = len(b)  # b 길이
    if a == "":
        return b_len
    if b == "":
        return a_len

    # 2차원 배열 준비
    matrix = [[0] * (b_len + 1) for _ in range(a_len + 1)]

    # 초기값 설정
    for i in range(a_len + 1):
        matrix[i][0] = i
    for j in range(b_len + 1):
        matrix[0][j] = j

    # 표 채우기
    for i in range(a_len):
        for j in range(b_len):
            ac = a[i]
            bc = b[j]
            cost = 0 if ac == bc else 1
            matrix[i + 1][j + 1] = min([
                matrix[i][j + 1] + 1,    # 문자 제거: 위쪽에서 +1
                matrix[i + 1][j] + 1,    # 문자 삽입: 왼쪽에서 +1
                matrix[i][j] + cost      # 문자 변경: 대각선에서 +cost
            ])

    return matrix[a_len][b_len]

class SimpleChatBot:
    def __init__(self, data_directory):
        # 학습 데이터(질문, 답변 쌍)를 로드
        self.questions, self.answers = self.load_data(data_directory)

    def load_data(self, data_directory):
        # CSV 파일 경로 설정
        filepath = os.path.join(data_directory, 'ChatbotData.csv')
        # CSV 파일로부터 질문과 답변 데이터를 불러옴
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()
        answers = data['A'].tolist()
        return questions, answers

    def find_best_answer(self, input_sentence):
        # 1. 학습데이터의 질문과 chat의 질문의 유사도를 레벤슈타인 거리를 이용해 구하기
        distances = [calc_distance(input_sentence, question) for question in self.questions]
        # 2. chat의 질문과 레벤슈타인 거리가 가장 유사한 학습데이터의 질문의 인덱스를 구하기
        best_match_index = distances.index(min(distances))
        # 3. 학습 데이터의 인덱스의 답을 chat의 답변으로 채택한 뒤 출력
        return self.answers[best_match_index]

# 데이터 파일이 있는 디렉토리 경로를 지정
data_directory = './'

# 챗봇 객체를 생성
chatbot = SimpleChatBot(data_directory)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)