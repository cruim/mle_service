import unittest
import app as app_
import json
from flask import jsonify


class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = app_.app.test_client()

    def _set_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Accept': "*/*",
            'Connections': 'keep-alive'
        }
        return headers

    def _test_object(self):
        data = {
            "models": ["001"],
            "data":
                {
                    "pclass": "1",
                    "name": "Futrelle, Mrs. Jacques Heath (Lily May Peel)",
                    "sex": "female",
                    "sibsp": "1",
                    "parch": "0",
                    "embarked": "Q",
                    "fare": "53",
                    "age": "25"
                }
        }
        return data

    def check_keys_in_dict(self, keys, dict_):
        for key in keys:
            if key not in dict_:
                return False
        return True

    def test_main_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_predict_success(self):
        params = self._test_object()
        response = self.app.post('api/predict', data=json.dumps(params), headers=self._set_headers(), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'result', response.data)

    def test_get_predict_error(self):
        response = self.app.post('api/predict', data=json.dumps({"test": "test"}), headers=self._set_headers(), follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'message', response.data)

    def test_convert_passenger_fare(self):
        data = {"fare": 100}
        self.assertIsInstance(app_.convert_passenger_fare(data), int)
        self.assertIn(app_.convert_passenger_fare(data), [0, 1, 2, 3])

    def test_convert_passenger_embarked(self):
        data = {"embarked": "Q"}
        self.assertIsInstance(app_.convert_passenger_embarked(data), int)
        self.assertIn(app_.convert_passenger_embarked(data), [0, 1, 2])

    def test_convert_passenger_age(self):
        data = {"age": 42}
        self.assertIsInstance(app_.convert_passenger_age(data), int)
        self.assertIn(app_.convert_passenger_age(data), [0, 1, 2, 3, 4])

    def test_format_keys(self):
        data = {'pclass': '1', 'sex': '1', 'sibsp': '1', 'parch': '0', 'embarked': '2', 'fare': '2', 'age': '1'}
        keys = {'Pclass', 'Sex', 'SibSp', 'Parch', 'Embarked', 'Fare', 'Age'}
        self.assertTrue(self.check_keys_in_dict(keys=keys, dict_=app_.format_keys(data)))

    def test_prepare_data(self):
        data = {'pclass': '1', 'name': 'Test', 'sex': 'female', 'sibsp': '1',
                'parch': '0', 'embarked': 'Q', 'fare': '53', 'age': '25'}
        self.assertIsInstance(app_.prepare_data(data), dict)

    def test_predict(self):
        self.assertIsInstance(app_.predict(self._test_object()), list)


if __name__ == "__main__":
    unittest.main()
