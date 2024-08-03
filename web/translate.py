import torch
from transformers import MarianMTModel, MarianTokenizer
import streamlit as st

class TextTranslator:
    def __init__(self, src_lang='ko', tgt_lang='en'):
        model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def translate_text(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(self.device)
        translated = self.model.generate(**inputs)
        return [self.tokenizer.decode(t, skip_special_tokens=True) for t in translated]
    

def main():
    # 번역 언어 선택
    src_lang = 'ko'  # 생성된 텍스트가 한국어라고 가정
    tgt_lang = input("번역할 언어를 선택하세요 (예: en, de, fr, es, zh, ja): ")

    # 번역기 초기화
    translator = TextTranslator(src_lang=src_lang, tgt_lang=tgt_lang)

    # 텍스트 번역 및 파일로 저장
    with open("translated_text.txt", "w", encoding="utf-8") as f:
        for i, text in enumerate(generated_texts):
            translated_text = translator.translate_text(text)
            print(f"\n번역된 텍스트 {i+1} ({tgt_lang}):")
            print(translated_text[0])
            f.write(f"번역된 텍스트 {i+1} ({tgt_lang}):\n")
            f.write(translated_text[0] + "\n\n")

if __name__ == "__main__":
    main()
