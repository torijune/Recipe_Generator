import streamlit as st
from googletrans import Translator

def translate_text(text, dest, src='auto'):
    translator = Translator()
    translation = translator.translate(text, src=src, dest=dest)
    return translation.text

def main():
    st.subheader("Welcome to Text Translator !")
    
    text = st.session_state['recipe_response']

    dest = st.selectbox("번역할 언어를 선택하세요", ["en", "ko", "ja", "zh-cn", "fr", "de", "es", "it"])
        
    if st.button("번역"):
        st.session_state['translated_text'] = translate_text(text = text, dest = dest)
        translated_text = st.session_state['translated_text']
        st.markdown("## 번역된 텍스트:")
        st.write(translated_text)