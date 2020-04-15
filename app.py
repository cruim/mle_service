from flask import Flask, request, jsonify
from catboost import CatBoostClassifier
import pandas as pd
import numpy as np
from validate import validate_json


CATBOOST_MODEL = CatBoostClassifier().load_model(fname='catboost_model')


app = Flask(__name__)


@app.route(rule='/', methods=['GET'])
def index():
    return 'сheck'


@app.route(rule='/api/predict', methods=['POST'])
@validate_json
def get_predict(*args):
    data = request.get_json()
    return jsonify(name=data['name'], status=predict(data)), 200


def prepare_data(input):
    del input['name']
    input['sex'] = np.where(input['sex'] == 'female', 1, 0).item(0)
    input['age'] = convert_passenger_age(input)
    input['embarked'] = convert_passenger_embarked(input)
    input['fare'] = convert_passenger_fare(input)
    return format_keys(input)


def convert_passenger_fare(input):
    if input['fare'] <= 17:
        return 0
    elif 17 < input['fare'] <= 30:
        return 1
    elif 30 < input['fare'] <= 100:
        return 2
    else:
        return 3


def convert_passenger_embarked(input):
    embarked_map = {'S': 0, 'C': 1, 'Q': 2}
    return embarked_map[input['embarked']]


def convert_passenger_age(input):
    if input['age'] <= 15:
        return 0  # Дети
    elif 15 < input['age'] <= 25:
        return 1  # Молодые
    elif 25 < input['age'] <= 35:
        return 2  # Взрослые
    elif 35 < input['age'] <= 48:
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
    input = prepare_data(input)
    df = pd.DataFrame.from_dict([input], orient='columns')
    prediction = CATBOOST_MODEL.predict(df)
    return prediction.item(0)


# @app.after_request
# def init_model():
#     global CATBOOST_MODEL
#     CATBOOST_MODEL = CatBoostClassifier()
#     CATBOOST_MODEL.load_model(fname='catboost_model')
