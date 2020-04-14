import json
from flask import Flask, request, Response
from catboost import CatBoostClassifier
import pandas as pd
import numpy as np


app = Flask(__name__)


@app.route(rule='/', methods=['GET'])
def index():
    return 'сheck'


@app.route(rule='/api/is_passenger_survived', methods=['POST'])
def get_predict():
    if request.data:
        data = request.get_json()
        checking = check_valid_json_format(data)
        if checking is True:
            data = request.get_json()
            return Response(json.dumps({"name": data["Name"], "status": predict(data)}), status=200, mimetype='application/json')
        else:
            return Response(json.dumps({"error": checking}), status=500, mimetype='application/json')

    else:
        return Response(json.dumps({"error": "Uncorrect data type. Look for json."}))


def check_valid_json_format(input_request):
    # TODO: сделать проверку на тип данных, отправлять данные по всем некорректным полям
    expected_keys = {"Pclass": int,
                     "Name": str,
                     "Sex": str,
                     "SibSp": int,
                     "Parch": int,
                     "Embarked": str,
                     "Fare": int,
                     "Age": int}
    for key, value in expected_keys.items():
        if key not in input_request or not isinstance(input_request[key], value):
            return "Not valid json, field: " + key
    return True


def prepare_data(input):
    del input['Name']
    input['Sex'] = np.where(input['Sex'] == 'female', 1, 0).item(0)
    input['Age'] = convert_passenger_age(input)
    input['Embarked'] = convert_passenger_embarked(input)
    input['Fare'] = convert_passenger_fare(input)
    return input


def convert_passenger_fare(input):
    if input['Fare'] <= 17:
        return 0
    elif 17 < input['Fare'] <= 30:
        return 1
    elif 30 < input['Fare'] <= 100:
        return 2
    else:
        return 3


def convert_passenger_embarked(input):
    embarked_map = {'S': 0, 'C': 1, 'Q': 2}
    return embarked_map[input['Embarked']]


def convert_passenger_age(input):
    if input['Age'] <= 15:
        return 0  # Дети
    elif 15 < input['Age'] <= 25:
        return 1  # Молодые
    elif 25 < input['Age'] <= 35:
        return 2  # Взрослые
    elif 35 < input['Age'] <= 48:
        return 3  # Средний возраст
    else:
        return 4  # Пожилые


def predict(input):
    input = prepare_data(input)
    from_file = CatBoostClassifier()
    model = from_file.load_model(fname='catboost_model')
    df = pd.DataFrame.from_dict([input], orient='columns')
    prediction = model.predict(df)
    return prediction.item(0)


if __name__ == "__name__":
    app.run(debug=True)