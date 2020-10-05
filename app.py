
import os
from notion.client import NotionClient
from flask import Flask
from flask import request
import datetime
import re

app = Flask(__name__)

def convert_to_date(data_string):
    x = re.match("(\d\d\d\d)-(\d\d)-(\d\d)", data_string)
    return datetime.datetime(int(x.group(1)), int(x.group(2)), int(x.group(3)))

def add_entry_into_table(token, collectionURL, content):
    # notion
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)
    
    row = cv.collection.add_row()

    for property in cv.collection.get_schema_properties():
        if property['name'] in content.keys():
            print("{} -> {}".format(property['name'], str(content[property['name']])))
            # text, title
            if property['type'] in ["text", "title"]:
                row.set_property(property['name'], content[property['name']])

            # multi_select
            if property['type'] == "multi_select":
                row.set_property(property['name'], [content[property['name']]])


            if property['type'] == "select":
                try:
                    row.set_property(property['name'], content[property['name']])
                except:
                    print("{} is not a valid option".format(str(content[property['name']])))
            if property['type'] == "checkbox":
                row.set_property(property['name'],content[property['name']].lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup','certainly', 'uh-huh'])
            if property['type'] == "file":
                # Change the property
                row.set_property(property['name'], content[property['name']])

            # person ?
            if property['type'] == "person":
                # Change the property
                row.set_property(property['name'], content[property['name']])
            # date ?
            if property['type'] == "date":
                print("\t date {} -> {}".format(property['name'], str(content[property['name']])))
                # Change the property
                date_value = convert_to_date(content[property['name']])
                date_string = "{} {}, {}".format(date_value.strftime("%b"),
                                         date_value.strftime("%d"),
                                         date_value.strftime("%d"))
                print(date_string)
                row.set_property(property['name'], date_string)
            # number
            if property['type'] == "number":
                row.set_property(property['name'], content[property['name']])

            # missing types: url, email, phone



@app.route('/add_entry', methods=['POST'])
def add_entry():
    json_data = request.get_json()
    token_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    add_entry_into_table(token_v2, url, json_data)
    return f'OK'


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
