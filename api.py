import os
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import numpy as np
import pandas as pd
import random
import mysql.connector
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

# import model
if os.path.isfile('./cosine_sim.csv'):
    df = pd.read_csv('cosine_sim.csv', index_col = 0)
else:
    raise FileNotFoundError


# prediction
class Predict(Resource):
    def post(self):
        # get most popular recipe 
        # connect to db
        db = mysql.connector.connect(host='localhost',user='root',password='root', database='food_recommendation')
        c = db.cursor()
        c.execute("""
        SELECT recipe_name 
        FROM recipe
        WHERE Sugar < 10 AND protein IS NOT NULL AND Saturated_fat < 7
        ORDER BY aggregateLikes DESC
        LIMIT 100
        """)

        recipe = [i[0] for i in c]
        
        prompt_recipe = random.choice(recipe)
        # top 50 similar recipe
        top_recipe = df[prompt_recipe].sort_values()[:50].index
        # recipe now
        recipe = random.choice(top_recipe)
        
        # Query database and dump all info into a JSON
        # get recipe id
        c = db.cursor()
        c.execute("""
        SELECT recipe_id
        FROM recipe
        WHERE recipe_name = 
        """ + "'" + recipe + "'")

        for i in c:
            recipe_id = i[0]

        c = db.cursor()
        c.execute("""
        SELECT recipe_url, aggregateLikes, healthyScore, readyin_minutes, calories, Fat, Carbohydrates, Sugar, protein
        FROM recipe
        WHERE recipe_name = 

        """ + "'" + recipe + "'")
        
        for i in c:
            info = i

        ## get recipe diet
        c = db.cursor()
        c.execute("""
        SELECT rd.diet_id, d.diet_name
        FROM recipe_diet rd
        JOIN diet d
        ON rd.diet_id = d.diet_id
        WHERE rd.recipe_id = 
        """ + str(recipe_id))
        
        diet = []

        for i in c:
            diet.append(i[1])

        ## get recipe cuisine
        c = db.cursor()
        c.execute("""
        SELECT rc.cuisine_id, c.cuisine_name
        FROM recipe_cuisine rc
        JOIN cuisine c
        ON rc.cuisine_id = c.cuisine_id
        WHERE rc.recipe_id = 
        """ + str(recipe_id))
        
        cuisine = []

        for i in c:
            cuisine.append(i[1])
        
        
        ## get recipe dish
        c = db.cursor()
        c.execute("""
        SELECT rd.dish_type_id, d.dish_type_name
        FROM recipe_dish rd
        JOIN dish_type d
        ON rd.dish_type_id = d.dish_type_id
        WHERE rd.recipe_id = 
        """ + str(recipe_id))

        dish = []

        for i in c:
            dish.append(i[1])

        # get recipe ingredients
        c = db.cursor()
        c.execute("""
        SELECT ri.ingredient_id, i.ingredient_name, ri.amount, ri.units, ingredient_image_url
        FROM recipe_ingredients ri
        JOIN ingredients i
        ON ri.ingredient_id = i.ingredient_id
        WHERE ri.recipe_id = 
        """+ str(recipe_id))

        ingredients = []

        for i in c:
            ingredients.append((i[1], i[2], i[3], i[4]))

        # get recipe instructions
        c = db.cursor()
        c.execute("""
        SELECT steps_no, steps_description
        FROM recipe_instructions ri
        WHERE ri.recipe_id = 

        """ + str(recipe_id))

        instructions = []
        for i in c:
            instructions.append(i)

        data = {}
        data['recipe'] = {}
        data['recipe']['id'] = recipe_id
        data['recipe']['name'] = recipe
        data['recipe']['url'] = info[0]
        data['recipe']['likes'] = info[1]
        data['recipe']['healthy'] = info[2]
        data['recipe']['minute'] = info[3]
        data['nutrition'] = {}
        data['nutrition']['calories'] = info[4]
        data['nutrition']['fat'] = info[5]
        data['nutrition']['carbohydrate'] = info[6]
        data['nutrition']['sugar'] = info[7]
        data['nutrition']['protein'] = info[8]
        data['diet'] = []

        for d in diet:
            data['diet'].append(d)
        data['cuisine'] = []

        for c in cuisine:
            data['cuisine'].append(c)

        data['dish'] = []

        for d in dish:
            data['dish'].append(d)

        data['ingredients'] = []

        for i in ingredients:
            temp = {}
            temp['name'] = i[0]
            temp['amount'] = i[1]
            temp['unit'] = i[2]
            try:
                temp['image'] = 'https://spoonacular.com/cdn/ingredients_100x100/'+i[3]
            except:
                temp['image'] = None
            data['ingredients'].append(temp)

        data['instructions'] = []

        for i in instructions:
            temp = {}
            temp['step'] = i[0]
            temp['description'] = i[1]
            data['instructions'].append(temp)
            
            
        return json.dumps(data)

api.add_resource(Predict, "/predict")

if __name__=="__main__":
    app.run(debug=True)

