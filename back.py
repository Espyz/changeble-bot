from database import Database
from bot import Bot
from flask import Flask, request
from threading import Thread
import json
app = Flask(__name__)

activeBotList = {

}

@app.route('/schema/add', methods=['POST'])
def scheme_handler():
    data = { 'message': 'error', 'status_code': 400 }
    client = Database()
    try:
        node_list = {}
        schema = request.get_json()['schema']
        nodes = schema['nodes']
        for node in nodes:
            if (node['type'] == 'parent'):
                continue
            node_list[node['id']] = { 'label': node['label'], 'childs': [] }
        edges = schema['edges']
        for edge in edges:
            node_list[edge['source']]['childs'].append(edge['target'])
        
        result = client.query('INSERT INTO schemes (front_schema, back_schema) VALUES (%s::jsonb, %s::jsonb) RETURNING id', [ json.dumps(schema), json.dumps(node_list) ])
        if (len(result) > 0):
            data = { 'message': 'success', 'status_code': 200 }
        else:
            data = { 'message': 'Не удалось сохранить схему', 'status_code': 409 }
    except Exception as err:
        print(err)
    finally:
        client.release()

    return data

@app.route('/schema/get', methods=['GET'])
def get_all_schemes():
    data = { 'message': 'error', 'status_code': 400 }
    client = Database()
    try:
        result = client.query('SELECT id, front_schema AS "schema" FROM schemes')
        if len(result) > 0:
            data = { 'message': result, 'status_code': 200 }
        else:
            data = { 'message': 'Не найдены сохранённые схемы', 'status_code': 409 }
    except Exception as err:
        print(err)
    finally:
        client.release()
    return data

@app.route('/bot/add', methods=['POST'])
def bot_new():
    data = { 'message': 'error', 'status_code': 400 }
    object = request.get_json()
    client = Database()
    try:
        result = client.query('INSERT INTO bots ("botName", "botUserName", "botLink", "botToken") VALUES (%s, %s, %s, %s) RETURNING id', [object['botName'], object['botUserName'], object['botLink'], object['botToken']])
        if len(result) > 0:
            data = { 'message': 'success', 'status_code': 200 }
        else:
            data = { 'message': 'Не удалось сохранить бота', 'status_code': 409 }
    except Exception as err:
        print(err)
    finally:
        client.release()
    return data

@app.route('/bot/schema', methods=['POST'])
def bot_schema():
    data = { 'message': 'error', 'status_code': 400 }
    object = request.get_json()
    client = Database()
    try:
        result = client.query('INSERT INTO connects ("botId", "schemeId") VALUES (%s, %s) RETURNING id', [ object['botId'], object['schemeId'] ])
        id = result[0][0]
        if len(result) > 0:
            bot_params = client.query('SELECT b."botToken", b."botName", s.back_schema FROM connects c INNER JOIN schemes s ON s.id = c."schemeId" INNER JOIN bots b ON b.id = c."botId" WHERE c.id = %s', [ id ])
            if (len(bot_params) > 0):
                bot = Bot(bot_params[0][0], bot_params[0][2])
                t1 = Thread(target=bot.start)
                t1.start()
                activeBotList[bot_params[0][1]] = bot
                data = { 'message': 'success', 'status_code': 200 }
            else: 
                data = { 'message': 'Не найдена информация о боте', 'status_code': 409 }
        else:
            data = { 'message': 'Не удалось сохранить связь бот/схема', 'status_code': 409 }
    except Exception as err:
        print(err)
    finally:
        client.release()
    return data


app.run(debug=True)
