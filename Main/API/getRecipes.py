import http.client
import json
from API import APIKey


#Replace this with data pulled from database, using test data for now
ingredients = ["apples","bananas","milk","butter","chicken","steak","carrots","yoghurt","ketchup"]


def get_recipes_by_ingredients(ingredients):
    recipeList = []
    numOfResults = 10

    conn1 = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com", timeout=300)

    headers = {
        'x-rapidapi-key': APIKey.key,
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    requestUrl = "/recipes/findByIngredients?ingredients="
    for i in ingredients:
        requestUrl += i + "%2C"
    requestUrl = requestUrl[:-3] + "&number=" + str(numOfResults)

    conn1.request("GET", requestUrl, headers=headers)
    res = conn1.getresponse()
    data = res.read()

    if res.status != 200:
        print(f"Error: Received status code {res.status}")
        print("Response:", data.decode())
        return {}

    try:
        ingredientSearchResultJSON = json.loads(data.decode())
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        print("Response:", data.decode())
        return {}

    conn2 = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': APIKey.key,
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    requestUrl = "/recipes/informationBulk?ids="

    for i in ingredientSearchResultJSON:
        requestUrl += str(i["id"]) + "%2C"
        tempRank = i["usedIngredientCount"] / (len(ingredients) + i["missedIngredientCount"])
        recipeList.append([i["id"], i["title"], i["missedIngredientCount"], i["usedIngredientCount"], tempRank])

    requestUrl = requestUrl[:-3]  # Remove the trailing '%2C'

    conn2.request("GET", requestUrl, headers=headers)
    res = conn2.getresponse()
    data = res.read()

    if res.status != 200:
        print(f"Error: Received status code {res.status}")
        print("Response:", data.decode())
        return {}

    try:
        bulkRecipeInfoJSON = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        print("Response:", data.decode())
        return {}

    # Verify the structure of the JSON response
    if isinstance(bulkRecipeInfoJSON, list):
        for idx, i in enumerate(bulkRecipeInfoJSON):
            recipeList[idx].append(i["readyInMinutes"])
            recipeList[idx].append(i["servings"])
            recipeList[idx].append(i["image"])
    else:
        print("Unexpected data structure received.")
        print("Response:", bulkRecipeInfoJSON)
        return {}

    sorted_recipeList = sorted(recipeList, key=lambda x: x[4], reverse=True)
    ranked_recipes = {rank: recipe for rank, recipe in enumerate(sorted_recipeList, start=1)}
    return ranked_recipes

#print(get_recipes_by_ingredients(ingredients))
