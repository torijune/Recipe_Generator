import json

class RecipeMerger:
    def __init__(self, lunch_file, breakfast_file, dinner_file):
        self.lunch_file = lunch_file
        self.breakfast_file = breakfast_file
        self.dinner_file = dinner_file
        self.merged_recipes = {}

    def load_list_from_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return []
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {filename}.")
            return []

    def add_meal_time(self, recipes, meal_time):
        for recipe in recipes:
            if 'meal_time' in recipe:
                recipe['meal_time'].append(meal_time)
            else:
                recipe['meal_time'] = [meal_time]
        return recipes

    def merge_recipes(self, recipes):
        for recipe in recipes:
            key = (recipe['name'], recipe['ingredients'], tuple(recipe['recipe']))  # 고유 키로 사용
            if key in self.merged_recipes:
                self.merged_recipes[key]['meal_time'].extend([mt for mt in recipe['meal_time'] if mt not in self.merged_recipes[key]['meal_time']])
            else:
                self.merged_recipes[key] = recipe

    def run(self):
        lunch_recipes = self.load_list_from_file(self.lunch_file)
        breakfast_recipes = self.load_list_from_file(self.breakfast_file)
        dinner_recipes = self.load_list_from_file(self.dinner_file)

        lunch_recipes = self.add_meal_time(lunch_recipes, '점심')
        breakfast_recipes = self.add_meal_time(breakfast_recipes, '아침')
        dinner_recipes = self.add_meal_time(dinner_recipes, '저녁')

        self.merge_recipes(lunch_recipes)
        self.merge_recipes(breakfast_recipes)
        self.merge_recipes(dinner_recipes)

        try:
            with open('new_merged_recipes.json', 'w', encoding='utf-8') as f:
                json.dump(list(self.merged_recipes.values()), f, ensure_ascii=False, indent=4)
            print("Merged recipes saved successfully.")
        except Exception as e:
            print(f"Error saving merged recipes: {e}")

        print(f"Total merged recipes: {len(self.merged_recipes)}")

if __name__ == "__main__":
    lunch_file = r'C:\Users\dnjsw\Desktop\Projects\FOM\FOM_Conference_Project\NLP\Recipe_Generator\code\flattened_lunch_recipes.json'
    breakfast_file = r'C:\Users\dnjsw\Desktop\Projects\FOM\FOM_Conference_Project\NLP\Recipe_Generator\code\flattened_breakfast_recipes.json'
    dinner_file = r'C:\Users\dnjsw\Desktop\Projects\FOM\FOM_Conference_Project\NLP\Recipe_Generator\code\flattened_dinner_recipes.json'

    merger = RecipeMerger(lunch_file, breakfast_file, dinner_file)
    merger.run()
