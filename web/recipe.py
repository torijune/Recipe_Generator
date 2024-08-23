import streamlit as st
import time
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

# ChatOllama 모델 초기화
llm = ChatOllama(model="RGRG:latest")

def generate_text_stream(text, delay=0.1):
    """텍스트를 실시간으로 생성하는 것처럼 출력"""
    placeholder = st.empty()
    output = ""
    for char in text:
        output += char
        placeholder.markdown(f"<div style='color: #ffffff; font-size: 16px;'>{output}</div>", unsafe_allow_html=True)
        time.sleep(delay)  # 지연시간 설정

def get_response(persona, topic, file):
    retriever = None
    if file is not None:
        # PDF 파일 읽기
        reader = PdfReader(file)
        pages = [page.extract_text() for page in reader.pages]

        if pages:
            
            # 각 페이지의 텍스트를 Document 객체로 변환
            documents = [Document(page_content=page) for page in pages]
            
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50)
            texts = text_splitter.split_documents(documents)
            
            model_name = "jhgan/ko-sbert-nli"
            encode_kwargs = {'normalize_embeddings': True}
            hf = HuggingFaceEmbeddings(model_name=model_name, encode_kwargs=encode_kwargs)
            
            db = FAISS.from_documents(texts, hf)
            retriever = db.as_retriever(search_type="similarity", search_kwargs={'k': 3})
            
        else:
            st.sidebar.write("파일 업로드에 실패하였습니다.")

    if retriever is not None:
        # 프롬프트 생성 및 LLM 호출
        prompt = ChatPromptTemplate.from_template("{persona} {topic} \n\nContext: {context}")
        chain = prompt | llm | StrOutputParser()

        docs = retriever.get_relevant_documents(topic)
        context = "\n\n".join([doc.page_content for doc in docs])

        response = chain.invoke({"persona": persona, "topic": topic, "context": context})
        return response

def main():
    uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf", "txt", "docx"])
    if uploaded_file is not None:
        st.sidebar.write("파일이 정상적으로 업로드되었습니다!")

        st.subheader("질문을 입력해주세요.")
    
        if 'persona' not in st.session_state:
            st.session_state['persona'] = "20대 대학교 자취생"
        
        topic = st.text_input("프롬포트를 입력하세요 : ")

        if st.button("검색"):
            persona = st.session_state['persona']
            response = get_response(persona, topic, uploaded_file)
            st.session_state['recipe_response'] = response
            generate_text_stream(response, delay=0.05)
    else :
        st.sidebar.write("파일을 다시 업로드 해주세요.")
    
    # st.subheader("질문을 입력해주세요.")
    
    # if 'persona' not in st.session_state:
    #     st.session_state['persona'] = "20대 대학교 자취생"
    
    # topic = st.text_input("프롬포트를 입력하세요 : ")

    # if st.button("검색"):
    #     persona = st.session_state['persona']
    #     response = get_response(persona, topic, uploaded_file)
    #     st.session_state['recipe_response'] = response
    #     st.write_stream(response)