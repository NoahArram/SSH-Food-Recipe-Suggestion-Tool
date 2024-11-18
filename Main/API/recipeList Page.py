import http.client
import json


#Replace this with data pulled from database, using test data for now
ingredients = ["apples","bananas","milk","butter","chicken","steak","carrots","yoghurt","ketchup"]


conn1 = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "XXX",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

requestUrl = "/recipes/findByIngredients?ingredients="
for i in ingredients:
    requestUrl+=i+"%2C"

requestUrl = requestUrl[:-3]+"number=2"
conn1.request("GET", requestUrl, headers=headers)

res = conn1.getresponse()
data = res.read()

ingredientSearchResult = data.decode("utf-8")
ingredientSearchResultJSON = json.loads(ingredientSearchResult)
#print(type(ingredientSearchResult))


conn2 = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "XXX",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}


requestUrl = "/recipes/informationBulk?ids="

for i in ingredientSearchResultJSON:
    print(i)
    
    requestUrl+=str(i["id"])+"%2C"

requestUrl=requestUrl[:-3]

conn2.request("GET", requestUrl, headers=headers)

res = conn2.getresponse()
data = res.read()

bulkRecipeInfoJSON = json.loads(data.decode("utf-8"))
#print(bulkRecipeInfoJSON)
