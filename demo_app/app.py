import streamlit as st
from generate_and_translate import TextGenerator, TextTranslator
from TTS import TextToSpeech

# Initialize models
# fine tuning한 model의 로컬 경로를 model_path에 넣음
model_path = './results'
generator = TextGenerator(model_path=model_path)
# translator는 뒤에서 언어를 선택 후 정의하기 위해 None으로 정의
translator = None
tts = TextToSpeech()

def main():
    st.title("Recipe Assistant")
    
    st.markdown("### Step 1: Generate a Recipe")
    if st.button("Generate Recipe"):
        prompt = st.text_input("Enter the dish you want the recipe for:")
        if prompt:
            generated_texts = generator.generate_text(prompt)
            generated_recipe = generated_texts[0]
            st.write(f"Generated Recipe:\n{generated_recipe}")
            st.session_state['generated_recipe'] = generated_recipe
        else:
            st.error("Please enter a dish name.")

    st.markdown("### Step 2: Translate the Recipe")
    if st.button("Translate Recipe"):
        if 'generated_recipe' in st.session_state:
            tgt_lang = st.text_input("Enter the target language (e.g., en, de, fr, es, zh, ja):")
            if tgt_lang:
                translator = TextTranslator(src_lang='ko', tgt_lang=tgt_lang)
                translated_text = translator.translate_text(st.session_state['generated_recipe'])[0]
                st.write(f"Translated Recipe ({tgt_lang}):\n{translated_text}")
                st.session_state['translated_recipe'] = translated_text
            else:
                st.error("Please enter a target language.")
        else:
            st.error("Please generate a recipe first.")

    st.markdown("### Step 3: Convert Recipe to Audio")
    if st.button("Convert Audio"):
        if 'generated_recipe' in st.session_state or 'translated_recipe' in st.session_state:
            recipe_choice = st.radio("Choose the recipe to convert to audio:", ('Original', 'Translated'))
            if recipe_choice == 'Original' and 'generated_recipe' in st.session_state:
                tts.convert_text_to_speech(st.session_state['generated_recipe'], 'recipe_audio.mp3')
                audio_file = open('recipe_audio.mp3', 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
            elif recipe_choice == 'Translated' and 'translated_recipe' in st.session_state:
                tts.convert_text_to_speech(st.session_state['translated_recipe'], 'recipe_audio.mp3')
                audio_file = open('recipe_audio.mp3', 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
            else:
                st.error("Please generate or translate a recipe first.")
        else:
            st.error("Please generate or translate a recipe first.")

if __name__ == "__main__":
    main()
