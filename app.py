
import os
from notion.client import NotionClient
from notion.collection import NotionDate
from flask import Flask
from flask import request
import datetime
import pytz

import re

app = Flask(__name__)

def convert_to_date(data_string):
    x = re.match("(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d)", data_string)
    utc = pytz.timezone('UTC')
    return datetime.datetime(int(x.group(1)), int(x.group(2)), int(x.group(3)), int(x.group(4)), int(x.group(5)), 0,0, utc)

def add_entry_into_table(token, collectionURL, content):
    # notion
    print(content)
    client = NotionClient(token)
    cv = client.get_collection_view(collectionURL)

    row = cv.collection.add_row()
    for property in cv.collection.get_schema_properties():
        if property['name'] in content.keys():
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
            if property['type'] == "number":
                row.set_property(property['name'], content[property['name']])
            # missing types: url, email, phone
        if property['type'] == "date":
            if property['name'] + "___start" in content.keys() and property['name'] + "___daily" in content.keys() and content[property['name'] + "___daily"] == True:
                print("Secco daily")
                date_start_value = convert_to_date(content[property['name'] + "___start"])
                date_notion = NotionDate(datetime.datetime(date_start_value.year, date_start_value.month, date_start_value.day, 0, 0, 0, 0, pytz.timezone('UTC')).astimezone('Europe/Rome'), timezone=pytz.timezone('Europe/Rome'))
                row.set_property(property['name'], date_notion)
            elif property['name'] + "___start" in content.keys() and not property['name'] + "___end" and (not property['name'] + "___daily" in content.keys() or
                    content[property['name'] + "___daily"] == False):
                print("Secco no daily")
                date_start_value = convert_to_date(content[property['name'] + "___start"])

                date_notion = NotionDate(date_start_value.astimezone('Europe/Rome'), timezone=pytz.timezone('Europe/Rome'))
                row.set_property(property['name'], date_notion)
            elif property['name'] + "___start" in content.keys() and property['name'] + "___end" in content.keys() and (not property['name'] + "___daily" in content.keys() or
                    content[property['name'] + "___daily"] == False):
                print("intervallo")
                datetime.timezone
                date_start_value = convert_to_date(content[property['name'] + "___start"])
                date_end_value = convert_to_date(content[property['name'] + "___end"])
                date_notion = NotionDate(date_start_value.astimezone('Europe/Rome'), date_end_value.astimezone('Europe/Rome'), timezone=pytz.timezone('Europe/Rome'))
                row.set_property(property['name'], date_notion)
            elif property['name'] + "___start" in content.keys():
                print("Secco no daily")
                date_start_value = convert_to_date(content[property['name'] + "___start"])
                date_notion = NotionDate(date_start_value.astimezone('Europe/Rome'), timezone=pytz.timezone('Europe/Rome'))
                row.set_property(property['name'], date_notion)
    if ("Name" in content.keys()):
        print("ECCOMI")
        value = content["Name"].split(":")
        print(value)
        if len(value)>1:
            if value[0].isupper():
                try:
                    row.set_property('Type', value[0])
                except:
                    print("{} is not a valid option".format(str(content['Type'])))
                row.set_property('Name', ":".join(value[1:]))

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
