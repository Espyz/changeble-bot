import json
import sys
from flask import Flask, request
app = Flask(__name__)
start_id = str(sys.maxsize * 2 + 1)
@app.route('/schema', methods=['POST'])
def scheme_handler():
    global start_id
    node_list = {}
    schema = request.get_json()['schema']
    nodes = schema['nodes']
    for node in nodes:
        if (node['type'] == 'parent'):
            continue
        if (int(node['id']) < int(start_id)):
            start_id = node['id']
        node_list[node['id']] = { 'label': node['label'], 'childs': [] }
    edges = schema['edges']
    for edge in edges:
        node_list[edge['source']]['childs'].append(edge['target'])
    
    file = open('schemes.json', 'w', encoding='utf-8')
    json.dump(node_list, file, ensure_ascii=False)
    file.close()
    return { 'message': 'success', 'status_code': 200 }

app.run(debug=True)
