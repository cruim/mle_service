from flask import Flask, request, jsonify
from catboost import CatBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
import pickle
import pandas as pd
import numpy as np
from validate import validate_json


CATBOOST_MODEL = CatBoostClassifier().load_model(fname='catboost_model')
GRADIENT_BOOSTING_CLASSIFIER_MODEL = pickle.load(open("gradient_boosting_classifier_model.dat", "rb"))


app = Flask(__name__)


@app.route(rule='/', methods=['GET'])
def index():
    return 'сheck'


@app.route(rule='/api/predict', methods=['POST'])
@validate_json
def get_predict():
    data = request.get_json()
    return jsonify(result=predict(data)), 200


def prepare_data(input):
    del input['name']
    input['sex'] = np.where(input['sex'] == 'female', 1, 0).item(0)
    input['age'] = convert_passenger_age(input)
    input['embarked'] = convert_passenger_embarked(input)
    input['fare'] = convert_passenger_fare(input)
    return format_keys(input)


def convert_passenger_fare(input):
    fare = int(input['fare'])
    if fare <= 17:
        return 0
    elif 17 < fare <= 30:
        return 1
    elif 30 < fare <= 100:
        return 2
    else:
        return 3


def convert_passenger_embarked(input):
    embarked_map = {'S': 0, 'C': 1, 'Q': 2}
    return embarked_map[input['embarked']]


def convert_passenger_age(input):
    age = int(input['age'])
    if age <= 15:
        return 0  # Дети
    elif 15 < age <= 25:
        return 1  # Молодые
    elif 25 < age <= 35:
        return 2  # Взрослые
    elif 35 < age <= 48:
        return 3  # Средний возраст
    else:
        return 4  # Пожилые


# Приведение ключей к формату модели
def format_keys(input):
    mapping = {'pclass': 'Pclass',
               'sex': 'Sex',
               'sibsp': 'SibSp',
               'parch': 'Parch',
               'embarked': 'Embarked',
               'fare': 'Fare',
               'age': 'Age'}
    for key, value in mapping.items():
        input[value] = input.pop(key)
    return input


def predict(input):
    result = []
    mapping = {"001": CATBOOST_MODEL, "002": GRADIENT_BOOSTING_CLASSIFIER_MODEL}
    df = pd.DataFrame.from_dict([prepare_data(input['data'])], orient='columns')
    for mod in input['models']:
        model = mapping.get(mod, False)
        if model:
            result.append({"model_id": mod, "value": model.predict(df).item(0), "result_code": 0})
        else:
            result.append({"model_id": mod, "error": "Model not found", "result_code": 1})
    return result


@app.errorhandler(400)
def handle_custom_exception(error):
    return jsonify(message=str(error.description)), error.code
