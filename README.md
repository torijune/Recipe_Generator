# Recipe_Generator by RAG with TTS   

## 프로젝트 개요   
본 프로젝트는 LLM을 활용하여 RAG를 구현하여 레시피 생성 기능, GoogleAPI를 활용하여 Translate, TTS를 구현하여 웹사이트 베포를 하는 프로젝트입니다.

# Deployment Using Streamlit
- Reciep Generator with RAG - RGRG
> ![스크린샷 2023-12-05 오후 4 24 24](https://github.com/sparkerhoney/Congress-Competition/assets/108461006/6ba7d0c4-35a4-4f69-8593-8299902a39e7)


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
│   ├── RGRG_test.ipynb
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
<br>
<br>
---

> `Project Owner : Torijune`
