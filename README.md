# Recipe_Generator Using LLM fine tuning with QLoRA And Recipe to speech with TTS   

## 프로젝트 개요   
이 프로젝트는 자연어 처리(NLP) 모델의 양자화, 파인 튜닝 및 텍스트 생성을 다룹니다. 프로젝트는 데이터 크롤링, 데이터 전처리, 모델 양자화, 모델 파인 튜닝, 텍스트 생성 그리고 텍스트 음성 변환의 전체 워크플로우를 포함합니다.   

## 프로젝트 구조
```
.
├── Crawling                
│   ├── recipe_crawling.ipynb     
│   ├── readme.md
│   ├── breakfast.txt
│   ├── lunch.txt    
│   └── dinner.txt    
├── Data                    
│   ├── breakfast_recipes.json
│   ├── lunch_recipes.json
│   ├── dinner_recipes.json
│   └── merged_recipes.json    
├── Fine_Tuning_Data    
│   └── demo_prompts.json   
├── Model                   
├── Notebook                
│   ├── 
├── PDF                     
│   └── 
├── README.md               
├── Setup                   
│   ├── __init__.py
│   ├── finetuning.py       
│   ├── generate_text.py    
│   ├── merge_recipes.ipynb
│   ├── create_prompt.ipynb
│   ├── LoRA.py     
│   └── quantization.py    
└── requirements.txt       
```
