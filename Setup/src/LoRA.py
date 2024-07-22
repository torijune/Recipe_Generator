from peft import LoraConfig, get_peft_model

class LoraModelConfig:
    '''
    LoRa Config에 대한 parameter는 상황에 따라 변경 가능
    아래에 있는 parameter를 변경 (주로 r과 target_modules를 변경)
    '''
    def __init__(self, model, r=8, lora_alpha=32, target_modules=["query_key_value"], 
                 lora_dropout=0.05, bias="none", task_type="CAUSAL_LM"):
        self.model = model
        self.config = LoraConfig(
            r=r,
            lora_alpha=lora_alpha,
            target_modules=target_modules,  # QKV 레이어에만 LoRA 적용
            lora_dropout=lora_dropout,
            bias=bias,
            task_type=task_type
        )

    def apply_lora(self):
        self.model = get_peft_model(self.model, self.config)
        print("Model LoRA Complete")
        return self.model