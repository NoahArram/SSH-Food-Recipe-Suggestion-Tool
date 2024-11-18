import http.client

#Replace this with data pulled from database, using test data for now
ingredients = ["apples","bananas","milk","butter","chicken","steak","carrots","yoghurt","ketchup"]


conn = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "855ba63510msh87c18edc980da90p1a2842jsncc58ceeb5d6a",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

requestUrl = "/recipes/findByIngredients?ingredients="
for i in ingredients:
    requestUrl+=i+"%2C"

requestUrl = requestUrl[:-3]+"number=10"
conn.request("GET", requestUrl, headers=headers)

res = conn.getresponse()
data = res.read()

ingredientSearchResult = data.decode("utf-8")
print(ingredientSearchResult)

