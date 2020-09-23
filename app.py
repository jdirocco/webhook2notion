
import os
from notion.client import NotionClient
from flask import Flask
from flask import request


app = Flask(__name__)


def createNotionTask(token, collectionURL, content):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    #row = cv.collection.add_row()
    #row.Name = content['name']
    #row.juri = str(content['age'])
    row = cv.collection.add_row()

    for value in cv.collection.get_schema_properties():
        if value['name'] in content.keys():
            print(value['name'])
            if value['type'] in ["text", "title"]:
                row.set_property(value['name'], content[value['name']])

            if value['type'] == "multi_select":
                row.set_property(value['name'], [content[value['name']]])
            # the value has to be a defined option
            if value['type'] == "select":
                try:
                    row.set_property(value['name'], content[value['name']])
                except:
                    print("{} is not a valid option".format(str(content[value['name']])))
            if value['type'] == "checkbox":
                row.set_property(value['name'],
                                 content[value['name']].lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup',
                                                                 'certainly', 'uh-huh'])
            if value['type'] == "file":
                # Change the property
                row.set_property(value['name'], content[value['name']])
            if value['type'] == "person":
                # Change the property
                row.set_property(value['name'], content[value['name']])
            if value['type'] == "date":
                # Change the property
                row.set_property(value['name'], content[value['name']])
            # Others ??



@app.route('/create_todo', methods=['POST'])
def create_todo():
    json_data = request.get_json()
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createNotionTask(token_v2, url, json_data)
    return f'OK'


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
