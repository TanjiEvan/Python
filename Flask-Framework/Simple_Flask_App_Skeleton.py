from flask import Flask
 
    
app=Flask(__name__)
 #"It creates an instance of Flask Class,which will be your WSGI Application"
  
@app.route("/")
def welcome():
    return "Welcome to the first page, Learning FLASK, Leacture-01 (Done)"

@app.route("/index")
def index():
    return "Welcome to Index Page"

if __name__=="__main__":
    app.run(debug=True)  ##Entry point of any py file"
## Debug used for autosave