# Recipe_Generator Using LLM fine tuning with QLoRA And Recipe to speech with TTS   

## 프로젝트 개요   
이 프로젝트는 자연어 처리(NLP) 모델의 양자화, 파인 튜닝 및 텍스트 생성을 다룹니다. 프로젝트는 데이터 크롤링, 데이터 전처리, 모델 양자화, 모델 파인 튜닝, 텍스트 생성 그리고 텍스트 음성 변환의 전체 워크플로우를 포함합니다.   

## 프로젝트 구조
```
.
├── Crawling                
│   ├── recipe_crawling.py     
│   ├── breakfast.txt
│   ├── lunch.txt    
│   └── dinner.txt    
├── Data
│   ├── one_recipe
│   │   ├── breakfast_recipes.json
│   │   ├── lunch_recipes.json
│   │   ├── dinner_recipes.json
│   │   └── merged_recipes.json  
│   └── ten_recipe
│       ├── pdf_convert.ipynb        
│       ├── flatten_breakfast_recipes.json
│       ├── flatten_lunch_recipes.json
│       ├── flatten_dinner_recipes.json
│       ├── new_breakfast_recipes.json
│       ├── new_lunch_recipes.json
│       ├── new_dinner_recipes.json
│       └── new_merged_recipes.json  
├── Fine_Tuning_Data    
│   ├── one_recipe
│   │    ├──demo_prompts.json 
│   │    └── instruction_data.json
│   └── ten_recipe
│       └── demo_prompts_2.json
├── PDF                     
│   └── 
├── README.md               
├── Setup
│   ├── one_recipe
│   │   ├── create_prompt.ipynb
│   │   ├── merge_recipes.ipynb
│   │   ├── recipe_crawling.ipynb
│   └── src           
│       ├── finetuning.py       
│       ├── reciep_merger.py    
│       ├── prompt_gen.py
│       ├── LoRA.py     
│       └── quantization.py
└── Web
    ├── __pycache__
    ├── recipe_book.pdf
    ├── app.py
    ├── audio.py
    ├── homepage.py
    ├── recipe.py
    ├── translate.py
    └── requirements.txt   
    
```
