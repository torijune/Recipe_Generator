import requests
import json
from bs4 import BeautifulSoup

class RecipeCrawler:
    '''
    RecipeCrawler 클래스는 만개의 레시피 사이트에서 주어진 음식 이름에 대한 레시피를 크롤링하는 기능을 제공
    '''
    def __init__(self, name):
        self.name = name
        self.base_url = "https://www.10000recipe.com/recipe/list.html?q="
    
    def get_html(self, url):
        '''
        주어진 URL에 대한 HTML 내용을 가져옴

        PARAMETERS
            - url (str): 접근할 URL
        RETURN
            - html (str): URL에 해당하는 HTML 내용
        '''
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("HTTP response error :", response.status_code)
            return None
    
    def parse_food_list(self, html):
        '''
        음식 목록을 파싱하여 반환

        PARAMETERS
            - html (str): 파싱할 HTML 내용
        RETURN
            - food_list (list): 음식 목록
        '''
        soup = BeautifulSoup(html, 'html.parser')
        food_list = soup.find_all(attrs={'class':'common_sp_link'})
        return food_list
    
    def parse_recipe(self, food_id):
        '''
        주어진 음식 ID에 대한 레시피를 파싱하여 반환

        PARAMETERS
            - food_id (str): 음식 ID
        RETURN
            - res (dict): 레시피 정보
        '''
        new_url = f'https://www.10000recipe.com/recipe/{food_id}'
        html = self.get_html(new_url)
        if html is None:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        food_info = soup.find(attrs={'type':'application/ld+json'})
        if food_info:
            result = json.loads(food_info.text)
            ingredient = ','.join(result['recipeIngredient'])
            recipe = [result['recipeInstructions'][j]['text'] for j in range(len(result['recipeInstructions']))]
            for j in range(len(recipe)):
                recipe[j] = f'{j+1}. ' + recipe[j]
            
            res = {
                'name': self.name,
                'ingredients': ingredient,
                'recipe': recipe
            }
            return res
        else:
            print(f"No detailed info found for recipe id {food_id}")
            return None
    
    def get_recipes(self):
        '''
        주어진 음식 이름에 대한 최대 10개의 레시피를 크롤링

        RETURN
            - results (list): 레시피 정보 목록 (breakfast, lunch, dinner 속 요리 레시피 정보)
        '''
        url = self.base_url + self.name
        html = self.get_html(url)
        if html is None:
            return None
        
        food_list = self.parse_food_list(html)
        if not food_list:
            print(f"No recipe found for {self.name}")
            return None
        
        results = []
        for i in range(min(10, len(food_list))):  # 최대 10개의 레시피 가져오기
            food_id = food_list[i]['href'].split('/')[-1]
            recipe = self.parse_recipe(food_id)
            if recipe:
                results.append(recipe)
        
        return results

    def crawl_multiple_recipes(self, dishes, meal_type):
        '''
        주어진 여러 음식 이름에 대해 레시피를 크롤링하고 결과를 JSON 파일로 저장

        PARAMETERS
            - dishes (list): 음식 이름 목록 (breakfast, lunch, dinner)
            - meal_type (str): 끼니 종류 (breakfast, lunch, dinner) -> dishes와 똑같은 단어 입력
        USEAGE
            - crawl_multiple_recipes(breakfast,"breakfast")
        '''
        meal_recipes = []
        failed_recipes = []

        for dish in dishes:
            try:
                recipe_info = self.get_recipes(dish)
                if recipe_info:
                    meal_recipes.append(recipe_info)
                else:
                    failed_recipes.append(dish)
            except Exception as e:
                print(f"Error occurred for {dish}: {e}")
                failed_recipes.append(dish)

        # JSON 파일로 저장
        with open(f'{meal_type}_recipes.json', 'w', encoding='utf-8') as f:
            json.dump(meal_recipes, f, ensure_ascii=False, indent=4)

        # 실패한 레시피 리스트 저장
        with open(f'{meal_type}_failed_recipes.json', 'w', encoding='utf-8') as f:
            json.dump(failed_recipes, f, ensure_ascii=False, indent=4)