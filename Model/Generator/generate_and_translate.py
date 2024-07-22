import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, MarianMTModel, MarianTokenizer
import os

class TextGenerator:
    def __init__(self, model_path, model_id='gpt2'):
        self.model_path = model_path
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def generate_text(self, prompt, max_length=50, num_return_sequences=1):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            inputs.input_ids,
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            do_sample=True,  # 샘플링을 사용하여 다양성 증가
            top_k=50,        # 확률이 높은 k개의 단어만 샘플링
            top_p=0.95,      # 누적 확률이 p 이하인 단어만 샘플링
            temperature=0.7  # 텍스트 다양성 제어
        )
        return [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

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

if __name__ == "__main__":
    model_path = './results'  # 파인 튜닝된 모델이 저장된 경로
    generator = TextGenerator(model_path=model_path)

    # 사용자로부터 프롬프트 입력 받기
    prompt = input("텍스트 생성을 위한 프롬프트를 입력하세요: ")

    # 텍스트 생성
    generated_texts = generator.generate_text(prompt)
    
    # 생성된 텍스트 출력 및 파일로 저장
    with open("generated_text.txt", "w", encoding="utf-8") as f:
        for i, text in enumerate(generated_texts):
            print(f"\n생성된 텍스트 {i+1}:")
            print(text)
            f.write(f"생성된 텍스트 {i+1}:\n")
            f.write(text + "\n\n")

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
