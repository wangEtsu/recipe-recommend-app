# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 18:27:17 2020

@author: joeip
"""

import mysql.connector
import requests
import random

# get id that has already been used and delete from pool
pool = set([str(i) for i in range(1,1000000)])
with open('recorded_id.csv', 'r') as f:
    already = set(f.read().split())

pool = pool - already
id_ = random.sample(pool,150)

# add new batch to record
with open('recorded_id.csv', 'a') as f:
    for i in id_:
        print(i, file = f)


# connection to db
db = mysql.connector.connect(host='localhost',user='root',password='root', database='food_recommendation')

#d3815d84b59b45d3b341803166d008f7
#d4f16bf4ed0441d39c28b3ad4a1f765b
#fc70d1ef09fd4cedac3974e5c1b1027e
#cbd19aeac4af4055963616665a10d187

for z in range(len(id_)):
# get data from api
    q_head = 'https://api.spoonacular.com/recipes/'
    ID = id_[z]
    q_tail = "/information?apiKey=d3815d84b59b45d3b341803166d008f7&includeNutrition=true"
    
    query = ''.join([q_head,ID,q_tail])
    response = requests.get(query)
    data = response.json()
    ###############################
    # check whether recipe with this id exist
    try:
        data['title']
    except:
        continue

    # check whether recipe exist in DB
    cs = db.cursor()
    cs.execute("""
    SELECT COUNT(*) from recipe
    WHERE recipe_id = 
    """ + "'"+ str(data['id'])+"'")

    for row in cs:
        count = row[0]

    if count == 1:
        continue
    #     print('exception')
    # recipe table
    recipe_id = data['id']
    recipe_name = data['title']
    try:
        recipe_image_url = data['image']
    except:
        recipe_image_url = 'None'
        
    vegetarian = data['vegetarian']
    vegan = data['vegan']
    glutenFree = data['glutenFree']
    veryHealthy = data['veryHealthy']
    veryPopular = data['veryPopular']
    aggLikes = data['aggregateLikes']
    healthScore = data['healthScore']
    readMin = data['readyInMinutes']

    nutrients = {}
    for i in data['nutrition']['nutrients']:
        nutrients[i['title']] = i['amount']

    calories = nutrients['Calories']
    fat = nutrients['Fat']
    saturated_fat = nutrients['Saturated Fat']
    carbohydrates = nutrients['Carbohydrates']
    sugar = nutrients['Sugar']
    protein = nutrients['Protein']

    mycursor = db.cursor()
    try:
        mycursor.execute("""
        INSERT INTO recipe (recipe_id, recipe_name, recipe_url, vegetarian, vegan, glutenfree, veryHealthy, veryPopular, 
        aggregateLikes, healthyScore, readyin_minutes, Calories, Fat, Saturated_fat, Carbohydrates, protein, Sugar)
    
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)
        """, (recipe_id, recipe_name, recipe_image_url, vegetarian, vegan, glutenFree, veryHealthy, veryPopular, aggLikes, healthScore,\
             readMin, calories, fat, saturated_fat, carbohydrates,protein,sugar))
    except:
        print('wrong')
        pass
    ######################################
    # dish type
    for i in data['dishTypes']:
        mycursor = db.cursor()
        q_string = 'SELECT COUNT(*) from dish_type WHERE dish_type_name = ' + '"' + i + '"'
        mycursor.execute(q_string)
        for j in mycursor:
            count = j[0]

        if count == 0:
            c1 = db.cursor()
            c1.execute("""
            INSERT INTO dish_type (dish_type_name)
            VALUES (%s)
            """, (i,))

        c3 = db.cursor()
        try:
            c3.execute("""
            SELECT dish_type_id FROM dish_type
            WHERE dish_type_name = 
            """ + "'" + i +"'")
        except:
            pass
        
        for k in c3:
            dish_type_id = k[0]

        c2 = db.cursor()
        try:
            c2.execute("""
            INSERT INTO recipe_dish (recipe_id, dish_type_id)
            VALUES (%s,%s)
            """, (recipe_id, dish_type_id))
        except:
            pass
    #############################
    #diet
    for i in data['diets']:
        mycursor = db.cursor()
        q_string = 'SELECT COUNT(*) from diet WHERE diet_name = ' + '"' + i + '"'
        mycursor.execute(q_string)
        for j in mycursor:
            count = j[0]

        if count == 0:
            c1 = db.cursor()
            c1.execute("""
            INSERT INTO diet (diet_name)
            VALUES (%s)
            """, (i,))

        c3 = db.cursor()
        try:
            c3.execute("""
            SELECT diet_id FROM diet
            WHERE diet_name = 
            """ + "'" + i +"'")
        except:
            pass

        for k in c3:
            diet_id = k[0]

        c2 = db.cursor()
        try:
            c2.execute("""
            INSERT INTO recipe_diet (recipe_id, diet_id)
            VALUES (%s,%s)
            """, (recipe_id, diet_id))
        except:
            pass
    ###################################
    # cuisine
    for i in data['cuisines']:
        mycursor = db.cursor()
        q_string = 'SELECT COUNT(*) from cuisine WHERE cuisine_name = ' + '"' + i + '"'
        mycursor.execute(q_string)
        for j in mycursor:
            count = j[0]

        if count == 0:
            c1 = db.cursor()
            try:
                c1.execute("""
                INSERT INTO cuisine (cuisine_name)
                VALUES (%s)
                """, (i,))
            except:
                pass

        c3 = db.cursor()
        try:
            c3.execute("""
            SELECT cuisine_id FROM cuisine
            WHERE cuisine_name = 
            """ + "'" + i +"'")
        except:
            pass

        for k in c3:
            cuisine_id = k[0]

        c2 = db.cursor()
        try:
            c2.execute("""
            INSERT INTO recipe_cuisine (recipe_id, cuisine_id)
            VALUES (%s,%s)
            """, (recipe_id, cuisine_id))
        except:
            pass
    ###############################
    # instructions
    try:
        for i in data['analyzedInstructions'][0]['steps']:
            step_no = i['number']
            step = i['step']

            c = db.cursor()

            c.execute("""

            INSERT INTO recipe_instructions (recipe_id, steps_no, steps_description)
            VALUES (%s,%s,%s)

            """, (recipe_id, step_no, step))
    except:
        pass
    ##############################
    # ingredients
    for i in data['extendedIngredients']:
        ingredient_id = i['id']
        ingredient_image_url = i['image']
        ingredient_name = i['name']
        ingredient_amount = i['measures']['metric']['amount']
        ingredient_unit = i['measures']['metric']['unitLong']


        mycursor = db.cursor()
        q_string = 'SELECT COUNT(*) from ingredients WHERE ingredient_name = ' + '"' + ingredient_name + '"'
        mycursor.execute(q_string)
        for j in mycursor:
            count = j[0]

        if count == 0:
            c1 = db.cursor()
            try:
                c1.execute("""
                INSERT INTO ingredients (ingredient_id, ingredient_name, ingredient_image_url)
                VALUES (%s,%s,%s)
                """, (ingredient_id, ingredient_name, ingredient_image_url))
            except:
                pass

        c2 = db.cursor()
        try:
            c2.execute("""
            INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount, units)
            VALUES (%s,%s,%s,%s)

            """ , (recipe_id, ingredient_id, ingredient_amount, ingredient_unit))
        except:
            pass

    db.commit()