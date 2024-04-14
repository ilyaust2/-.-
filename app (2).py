# Сервер для обработки JSON запросов отправке времени транспортного запаздывания
from flask import Flask, request, jsonify
from func_timedelta1 import func_timedelta1
from func_timedelta2 import func_timedelta2

app = Flask(__name__)

# Путь для расчёта времени запаздывания в первом задании (timedelta1)


@app.route('/api/timedelta1', methods=['GET'])
def timedelta1():
    data = request.get_json()
    timedelta = func_timedelta1(data)
    response = {
        'timedelta': timedelta
    }
    return jsonify(response)


# Путь для расчёта времени запаздывания во втором задании (timedelta2)


@app.route('/api/timedelta2', methods=['GET'])
def timedelta2():
    data = request.get_json()
    timedelta = func_timedelta2(data)
    response = {
        'timedelta': timedelta
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run()
