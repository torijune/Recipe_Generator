from gtts import gTTS
import streamlit as st
import os

def generate_tts(text, language, speed):
    lang_codes = {
        "한국어": "ko",
        "영어": "en",
        "스페인어": "es",
        "프랑스어": "fr",
        "중국어": "zh",
        "일본어": "ja"
    }

    if language not in lang_codes:
        raise ValueError("지원되지 않는 언어입니다.")
    
    tts = gTTS(text=text, lang=lang_codes[language], slow=(speed < 1.5))
    tts.save("output.mp3")
    
    audio_file = open("output.mp3", "rb")
    audio_bytes = audio_file.read()
    os.remove("output.mp3")
    
    return audio_bytes

def main():
    st.subheader("Welcome to TTS Service!")
    
    if 'recipe_response' not in st.session_state:
        st.warning("텍스트 생성을 먼저 진행해주세요.")
    else : 
        text = st.session_state['recipe_response']


    speed = st.slider("속도를 선택하세요 (0.5 ~ 1.5):", 0.5, 1.5, 1.0)
    language = st.selectbox("언어를 선택하세요:", ["한국어", "영어", "스페인어", "프랑스어", "중국어", "일본어"])

    if st.button("Generate Audio"):
        st.markdown("## 변환된 오디오 데이터 :")
        st.session_state['audio'] = generate_tts(text, language, speed)
        audio_bytes = st.session_state['audio']
        st.audio(audio_bytes, format='audio/mp3')