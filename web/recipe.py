import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# ChatOllama 모델 초기화
llm = ChatOllama(model="RGRG:latest")

def get_chain():
    # Chain 생성
    prompt = ChatPromptTemplate.from_template("{topic}에 대해 정확하게 답변해주세요.")
    chain = prompt | llm | StrOutputParser()
    return chain

def get_response(topic):
    chain = get_chain()
    response = chain.invoke({"topic": topic})
    return response

def main():
    st.title("질문을 입력해주세요.")
    topic = st.text_input("프롬포트를 입력하세요 : ")

    if st.button("검색"):
        st.session_state['recipe_response'] = get_response(topic)
        response = st.session_state['recipe_response']
        st.write(response)