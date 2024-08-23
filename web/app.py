import streamlit as st
from streamlit_option_menu import option_menu
from recipe import main as get_response
from translate import main as translate_recipe
from audio import main as TTS
from homepage import main as homepage

st.set_page_config(page_title="FOM RGRG - Recipe Generator with RAG", page_icon="🍕")

st.title("레시피 알쥐?알쥐? - RGRG")

st.write("사이드 바에서 원하는 기능을 선택해주세요.")

# CSS 코드로 사이드바의 크기 조정
st.markdown(
    """
    <style>
    /* 전체 사이드바의 크기 조정 */
    div[data-testid="stSidebar"] {
        min-width: 150px;
        max-width: 150px;
    }

    /* 사이드바 안의 요소들 크기 조정 */
    div[data-testid="stSidebar"] .css-1d391kg {
        min-width: 150px;
        max-width: 150px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    page = option_menu(
        "메뉴",                # 메뉴 제목
        ["홈페이지", "질문창", "번역", "레시피 음성 변환"],  # 메뉴 항목
        icons=['house', 'bi bi-robot', 'globe', 'volume-up'],  # 각 항목에 사용할 아이콘
        menu_icon="cast",      # 메뉴 아이콘 (사이드바 상단에 표시되는 아이콘)
        default_index=0,       # 기본으로 선택되는 메뉴 항목 인덱스
    )

if page == '홈페이지':
    homepage()

if page == '질문창':
    if 'recipe_response' in st.session_state:
        st.write(st.session_state['recipe_response'])  # 세션 상태에 저장된 검색 결과를 표시
    else : 
        get_response()

if page == '번역':
    if 'recipe_response' in st.session_state:
        translate_recipe()
    else:
        st.error("먼저 '레시피 및 재료 검색' 페이지에서 레시피를 검색해주세요.")

if page == '레시피 음성 변환':
    if 'recipe_response' in st.session_state:
        TTS()
    else :
        st.error("먼저 '레시피 및 재료 검색' 페이지에서 레시피를 검색해주세요.")