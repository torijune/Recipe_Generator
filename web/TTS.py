from melo.api import TTS
'''
Dependency를 위한 install list

conda create -n melotts python=3.10
conda activate melotts
git clone https://github.com/myshell-ai/MeloTTS.git
cd MeloTTS
pip3 install -e .
python3 -m unidic download
'''
class MultilingualTTS:
    def __init__(self, text_file_path, device='auto'):
        self.text_file_path = text_file_path
        self.device = device
        self.languages = {
            "한국어": {"code": "KR", "speaker": "KR"},
            "영어": {"code": "EN", "speaker": "EN-Default"},
            "스페인어": {"code": "ES", "speaker": "ES"},
            "프랑스어": {"code": "FR", "speaker": "FR"},
            "중국어": {"code": "ZH", "speaker": "ZH"},
            "일본어": {"code": "JP", "speaker": "JP"}
        }
        self.text = self.load_text()

    def load_text(self):
        with open(self.text_file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()

    def get_user_input(self):
        speed = float(input("속도를 입력하세요 (1~3): "))
        language = input("원하는 언어를 선택하세요 (한국어/영어/스페인어/프랑스어/중국어/일본어): ")
        if language not in self.languages:
            raise ValueError("지원되지 않는 언어입니다.")
        return speed, language

    def generate_tts(self, speed, language):
        lang_config = self.languages[language]
        model = TTS(language=lang_config["code"], device=self.device)
        speaker_ids = model.hps.data.spk2id
        output_path = f'demo_audio_{lang_config["code"]}.wav'

        # 음성 파일로 저장
        model.tts_to_file(self.text, speaker_ids[lang_config["speaker"]], output_path, speed=speed)

    def run(self):
        speed, language = self.get_user_input()
        self.generate_tts(speed, language)

def main():
    # streamlit activate code 필요
    text_file_path = r'C:\Users\dnjsw\Desktop\Projects\FOM\FOM_Conference_Project\NLP\Recipe_Generator\Model\Generator\input_text.txt'
    tts_system = MultilingualTTS(text_file_path)
    tts_system.run()

if __name__ == "__main__":
    main()
