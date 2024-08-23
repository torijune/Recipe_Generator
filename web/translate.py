import streamlit as st
from deep_translator import GoogleTranslator

def translate_text(text, dest):
    # deep-translator를 사용하여 번역 수행
    translator = GoogleTranslator(source='auto', target=dest)
    translated_text = translator.translate(text)
    return translated_text

def main():
    st.subheader("Welcome to Text Translator !")
    
    # 번역할 텍스트 설정
    text = st.session_state.get('recipe_response', '')

    if text:
        dest = st.selectbox("번역할 언어를 선택하세요", ["en", "ko", "ja", "zh-cn", "fr", "de", "es", "it"])

        if st.button("번역"):
            translated_text = translate_text(text=text, dest=dest)
            st.session_state['translated_text'] = translated_text
            st.markdown("## 번역된 텍스트:")
            st.write(translated_text)
    else:
        st.write("먼저 번역할 텍스트를 입력하세요.")