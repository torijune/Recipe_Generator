import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, MarianMTModel, MarianTokenizer

class TextGenerator:
    def __init__(self, model_path, model_id='EleutherAI/gpt-neo-125m'):
        # model_path에는 fine tuning한 model이 들어가야함 -> Fine Tuning 후 진행 or huggingface에 있는 모델도 가능 -> app.py에서 관리
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
