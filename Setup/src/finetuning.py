from LoRA import LoraModelConfig
from quantization import QuantizationConfig
from transformers import Trainer, TrainingArguments
from datasets import load_dataset

class FineTuning:
    def __init__(self, model_id, file_path, output_dir='./results', epochs=3, batch_size=8):
        self.model_id = model_id
        self.file_path = file_path
        self.output_dir = output_dir
        self.epochs = epochs
        self.batch_size = batch_size

    def prepare_model(self):
        # 양자화 모델 준비
        quant_config = QuantizationConfig(self.model_id)
        quant_model = quant_config.quantize_model()

        # LoRA 설정 적용
        lora_config = LoraModelConfig(quant_model)
        lora_model = lora_config.apply_lora()
        
        return lora_model, quant_config.tokenizer

    def preprocess_data(self, tokenizer):
        dataset = load_dataset("json", data_files=self.file_path)
        tr_data = dataset.map(
            lambda x: {'text': f"### 역할: {x['instruction']}\n\n### 레시피 검색을 위한 질문: {x['prompt']}\n\n### 요리에 대한 재료 및 레시피: {x['response']}"}
        )
        train_dataset = tr_data.map(lambda samples: tokenizer(samples["text"]), batched=True)
        return train_dataset

    def train(self):
        model, tokenizer = self.prepare_model()
        train_dataset = self.preprocess_data(tokenizer)

        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=self.epochs,
            per_device_train_batch_size=self.batch_size,
            per_device_eval_batch_size=self.batch_size,
            evaluation_strategy="epoch",
            save_strategy="epoch",
            logging_dir=f'{self.output_dir}/logs',
            logging_steps=10,
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            tokenizer=tokenizer,
        )

        trainer.train()

if __name__ == "__main__":
    # FineTuning 인스턴스 생성 및 학습 실행
    model_id = "gpt2"  # Hugging Face 모델 ID
    file_path = "C:/Users/dnjsw/Desktop/Projects/FOM/FOM_Conference_Project/NLP/Recipe_Generator/Fine_Tuning_Data/ten_recipes/demo_prompts_2.json"
    finetuning = FineTuning(model_id=model_id, file_path=file_path)
    finetuning.train()