import streamlit as st
from get_response import main as get_recipe
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

st.set_page_config(page_title="FOM RGRG - Recipe Generator with RAG, page_icon="🍕")


st.title("레시피 알쥐?알쥐? - RGRG")

st.write("사이드 바에서 원하는 기능을 선택해주세요.")

with st.sidebar:
    page = st.radio('Go to', ('홈페이지', '레시피 및 재료 검색','레시피 번역','레시피 음성 변환'))

if page == '홈페이지':
    st.write(" "레시피 알쥐?알쥐?"는 요리에 대한 재료와 레시피를 알려주는 어플입니다. 사이드 바에서 원하는 기능을 선택해주세요.")
elif page == '시피 및 재료 검색':
    get_recipe()
