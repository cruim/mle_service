Запуск gunicorn -c config.py app:app
Пример объекта для теста
 {
              "models": ["001","002","003"],
              "data":
                            {
                                          "pclass": "1",
                                          "name": "Futrelle, Mrs. Jacques Heath (Lily May Peel)",
                                          "sex": "male",
                                          "sibsp": "1",
                                          "parch": "0",
                                          "embarked": "S",
                                          "fare": "53",
                                          "age": "25"
                            }
}

Запуск тестов: nose2 -v tests.test_basic
Статистика: nose2 --with-coverage
Нет теста на встроенный метод errorhandler