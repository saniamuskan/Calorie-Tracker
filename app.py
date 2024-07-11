
from flask import Flask, request, jsonify, render_template
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
import requests
import json

app = Flask(__name__)

CALORIE_GOAL_LIMIT = 2400  # kcal
PROTEIN_GOAL = 180  # grams
FAT_GOAL = 80  # grams
CARBS_GOAL = 300  # grams

today = []

@dataclass
class Food:
    name: str
    calories: int
    proteins: int
    fat: int
    carbs: int

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_food', methods=['POST'])
def add_food():
    data = request.json
    query = data['query']

    api_url = f'https://api.calorieninjas.com/v1/nutrition?query={query}'
    response = requests.get(api_url, headers={'X-Api-Key': '9/hMSxemNd16bneLeTei8Q==LNxmuVFBNqirgDgO'})
    
    if response.status_code == requests.codes.ok:
        food_data = response.json()["items"][0]
        food = Food(
            name=query,
            calories=food_data["calories"],
            proteins=food_data["protein_g"],
            fat=food_data["fat_total_g"],
            carbs=food_data["carbohydrates_total_g"]
        )
        today.append(food)
        return jsonify({"message": "Successfully added!"})
    else:
        return jsonify({"error": True, "message": response.text})

@app.route('/get_progress')
def get_progress():
    calorie_sum = sum(food.calories for food in today)
    protein_sum = sum(food.proteins for food in today)
    fat_sum = sum(food.fat for food in today)
    carbs_sum = sum(food.carbs for food in today)

    return jsonify({
        "foods": [{"name": food.name, "calories": food.calories, "proteins": food.proteins, "fat": food.fat, "carbs": food.carbs} for food in today],
        "calories": calorie_sum,
        "proteins": protein_sum,
        "fats": fat_sum,
        "carbs": carbs_sum,
        "protein_goal": PROTEIN_GOAL,
        "fat_goal": FAT_GOAL,
        "carbs_goal": CARBS_GOAL,
        "calorie_goal": CALORIE_GOAL_LIMIT,
        "protein_percentage": (protein_sum / PROTEIN_GOAL) * 100,
        "fat_percentage": (fat_sum / FAT_GOAL) * 100,
        "carbs_percentage": (carbs_sum / CARBS_GOAL) * 100
    })

@app.route('/set_goals', methods=['POST'])
def set_goals():
    data = request.json
    height = data['height']
    weight = data['weight']
    age = data['age']
    gender = data['gender']

    # Simple BMR calculation using the Harris-Benedict equation
    if gender == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    calorie_goal = bmr * 1.2  # Assuming a sedentary lifestyle for simplicity
    protein_goal = weight * 1.6  # 1.6 grams of protein per kg of body weight
    fat_goal = calorie_goal * 0.25 / 9  # 25% of calories from fat

    global CALORIE_GOAL_LIMIT, PROTEIN_GOAL, FAT_GOAL, CARBS_GOAL
    CALORIE_GOAL_LIMIT = calorie_goal
    PROTEIN_GOAL = protein_goal
    FAT_GOAL = fat_goal
    CARBS_GOAL = (calorie_goal - (protein_goal * 4 + fat_goal * 9)) / 4

    return jsonify({
        "calorie_goal": calorie_goal,
        "protein_goal": protein_goal,
        "fat_goal": fat_goal,
        "carbs_goal": CARBS_GOAL
    })

if __name__ == '__main__':
    app.run(debug=True)
