import http.client
import json
import APIKey


#Replace this with data pulled from database, using test data for now
ingredients = ["apples","bananas","milk","butter","chicken","steak","carrots","yoghurt","ketchup"]


def get_recipes_by_ingredients(ingredients):

    #[[id,title,extra ingredient needed, used ingredients, ranking, prep mins, servings]]
    recipeList = []
    numOfResults = 10

    conn1 = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': APIKey.key,
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    requestUrl = "/recipes/findByIngredients?ingredients="
    for i in ingredients:
        requestUrl += i + "%2C"

    requestUrl = requestUrl[:-3] + "&number="+str(numOfResults)
    conn1.request("GET", requestUrl, headers=headers)

    res = conn1.getresponse()
    data = res.read()

    ingredientSearchResult = data.decode("utf-8")
    ingredientSearchResultJSON = json.loads(ingredientSearchResult)

    conn2 = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': APIKey.key,
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    requestUrl = "/recipes/informationBulk?ids="

    for i in ingredientSearchResultJSON:
        requestUrl += str(i["id"]) + "%2C"
        tempRank = i["usedIngredientCount"]/(len(ingredients)+i["missedIngredientCount"])
        recipeList.append([i["id"],i["title"],i["missedIngredientCount"],i["usedIngredientCount"],tempRank])

    requestUrl = requestUrl[:-3]

    conn2.request("GET", requestUrl, headers=headers)

    res = conn2.getresponse()
    data = res.read()

    bulkRecipeInfoJSON = json.loads(data.decode("utf-8"))
    #print(bulkRecipeInfoJSON)
    for i in bulkRecipeInfoJSON:
        recipeList[bulkRecipeInfoJSON.index(i)].append(i["preparationMinutes"])
        recipeList[bulkRecipeInfoJSON.index(i)].append(i["servings"])
        
    #print(bulkRecipeInfoJSON)
    
    sorted_recipeList = sorted(recipeList, key=lambda x: x[4], reverse=True)

    ranked_recipes = {rank: recipe for rank, recipe in enumerate(sorted_recipeList, start=1)}
    #return recipeList
    return ranked_recipes

print(get_recipes_by_ingredients(ingredients))
