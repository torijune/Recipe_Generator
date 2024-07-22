from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class QuantizationConfig:
    def __init__(self, model_name, device='cpu'):
        self.model_name = model_name
        self.device = device
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def quantize_model(self):
        self.model.to(self.device)
        self.model = torch.quantization.quantize_dynamic(
            self.model, {torch.nn.Linear}, dtype=torch.qint8
        )
        return self.model
