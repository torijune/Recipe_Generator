import json

class RecipePromptGenerator:
    def __init__(self, recipe_file):
        self.recipe_file = recipe_file
        self.recipes = self.load_recipe()

    def load_recipe(self):
        try:
            with open(self.recipe_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File {self.recipe_file} not found.")
            return []
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {self.recipe_file}.")
            return []

    def create_prompt(self):
        prompt_response_pairs = []
        for recipe in self.recipes:
            # 프롬프트와 응답 쌍 생성
            prompt = f"""{recipe['name']}을 일반적인 한국 가정에서 요리할 수 있는 레시피를 제공해줘. 레시피를 제공하기 전에 {recipe['name']}에 꼭 들어가야 하는 재료들을 알려줘. 재료의 양을 자세히 알려줘 (재료의 양으로는 재료의 무게, 계량 컵의 갯수 등). {recipe['name']}을 확실하게 조리하기 위한 정확하고 따라할 수 있는 레시피를 제공해줘. 한국어로 대답해주고 단계별로 1,2,3,4,...의 순서로 구분해서 설명해줘. Let's think step by step"""

            response = f"""{recipe['name']}의 재료 : {recipe['ingredients']}
            {recipe['name']}의 레시피 : {' '.join(recipe['recipe'])}"""
            
            prompt_response_pairs.append({"prompt": prompt, "response": response})
        return prompt_response_pairs

    def save_prompts(self, prompts, output_file):
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(prompts, f, ensure_ascii=False, indent=4)
            print(f"Prompts saved successfully to {output_file}.")
        except Exception as e:
            print(f"Error saving prompts: {e}")

if __name__ == "__main__":
    recipe_file = r'C:\Users\dnjsw\Desktop\Projects\FOM\FOM_Conference_Project\NLP\Recipe_Generator\code\new_merged_recipes.json'
    output_file = 'demo_prompts.json'
    
    generator = RecipePromptGenerator(recipe_file)
    demo_prompts = generator.create_prompt()
    generator.save_prompts(demo_prompts, output_file)
