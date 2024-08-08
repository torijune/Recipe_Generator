import streamlit as st
from recipe import main as get_response
from translate import main as translate_recipe
from audio import main as TTS

st.set_page_config(page_title="FOM RGRG - Recipe Generator with RAG", page_icon="🍕")

st.title("레시피 알쥐?알쥐? - RGRG")

st.write("사이드 바에서 원하는 기능을 선택해주세요.")

with st.sidebar:
    page = st.radio('Go to', ('홈페이지', '질문창','번역','레시피 음성 변환'))

if page == '홈페이지':
    st.write("레시피 알쥐?알쥐?는 요리에 대한 재료와 레시피를 알려주는 어플입니다. 사이드 바에서 원하는 기능을 선택해주세요.")

if page == '질문창':
    if 'recipe_response' in st.session_state:
        st.write(st.session_state['recipe_response'])  # 세션 상태에 저장된 검색 결과를 표시
    else : 
        get_response()

if page == '번역':
    if 'recipe_response' in st.session_state:
        translate_recipe()
    else:
        st.warning("먼저 '레시피 및 재료 검색' 페이지에서 레시피를 검색해주세요.")

if page == '레시피 음성 변환':
    if 'recipe_response' in st.session_state:
        TTS()
    else :
        st.warning("먼저 '레시피 및 재료 검색' 페이지에서 레시피를 검색해주세요.")
