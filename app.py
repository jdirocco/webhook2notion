
import os
from notion.client import NotionClient
from flask import Flask
from flask import request


app = Flask(__name__)


def createNotionTask(token, collectionURL, content):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.title = content


@app.route('/create_todo', methods=['POST'])
def create_todo():
    json_data = request.get_json()
    print(json_data)
    print(json_data['name'])
    print(json_data['age'])
    #todo = request.args.get('todo')
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    print(token_v2)
    print(url)
    #createNotionTask(token_v2, url, todo)
    return f'Juri to PRINTS'


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
