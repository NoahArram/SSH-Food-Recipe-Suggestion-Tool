import http.client
import json
from API import APIKey

def get_recipe_info(recipeID):
    conn = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")
    #recipeInfo = [ingredients, instructions]
    recipeInfo = []
    ingredients = []
    instructions = []

    headers = {
        'x-rapidapi-key': APIKey.key,
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    conn.request("GET", "/recipes/"+str(recipeID)+"/information", headers=headers)

    res = conn.getresponse()
    data = res.read()

    recipeData = data.decode("utf-8")
    recipeDataJSON = json.loads(recipeData)

    for i in recipeDataJSON["extendedIngredients"]:
        ingredients.append(i["original"])

    for i in recipeDataJSON["analyzedInstructions"]:
        for j in i["steps"]:
            instructions.append(j["step"])
    
    recipeInfo.append(ingredients)
    recipeInfo.append(instructions)
    recipeInfo.append(recipeDataJSON["readyInMinutes"])
    recipeInfo.append(recipeDataJSON["servings"])
    recipeInfo.append(recipeDataJSON["title"])
    recipeInfo.append(recipeDataJSON["image"])
    
    return recipeInfo

#debug
print(get_recipe_info(875447))



