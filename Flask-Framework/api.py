from flask import Flask,jsonify,request

app=Flask(__name__)

## Initial Data in to do list

items=[
    {"id":1 ,"name":"Item 1","Description":"This is Item 1"},
    {"id":2 ,"name":"Item 2","Description":"This is Item 2"}
]

@app.route('/')
def home():
    return "Welcome to the sample TO DO LIST App"

## Get : Retrieve all the items..

@app.route('/items',methods=["GET"])
def get_items():
    return jsonify(items)
'''
jsonify(items) converts the Python data (likely a dictionary, list, or other serializable types) 
into JSON format (JavaScript Object Notation) and returns it as an HTTP response.

--> JSON (JavaScript Object Notation) is a lightweight data-interchange 
format that's easy for both humans to read and write, and machines to parse and generate.

--> It is based on key-value pairs, where the key is a 
string and the value can be various data types like strings, numbers, lists, and dictionaries.
'''

##  Get : Retrive a specific item by ID..

@app.route("/items/<int:item_id>",methods=["GET"])
def get_item(item_id):
    item=next((item for item in items if item["id"]==item_id),None)
    if item is None:
        return jsonify({"Error":"Item not found"})
    return jsonify(item)

'''
next() retrieves the first item in the items list 
that matches the condition (item["id"] == item_id).

The generator expression (item for item in items if item["id"] == item_id)
 searches for the matching item.

'''

## Post : Create a new task 

@app.route("/items",methods=["POST"])
def create_item():
    if not request.json or not 'name' in request.json:
        return jsonify({"Error":"Item not found"})
    new_item={
        "id":items[-1]["id"]+1 if items else 1,
        "name":request.json["name"], 
        "Description":request.json["Description"]
        ##{"name":"New Item","description":"This is a new item"}
    }
    items.append(new_item)
    return jsonify(new_item)

## Put : Update an existing Item 

@app.route('/items/<int:item_id>',methods=["PUT"])
def update_item(item_id):
    item=next((item for item in items if item["id"]==item_id),None)
    if item is None:
        return jsonify({"Error":"Item not found"})
    item["name"]= request.json.get('name',item['name'])
    item["Description"]= request.json.get('Description',item['Description'])
    return jsonify(item)

## Delete : Delete an Item 
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"result": "Item deleted"})









if __name__=='__main__':
    app.run(debug=True)