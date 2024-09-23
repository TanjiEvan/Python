from flask import Flask,render_template

#render_template --> Redirects to html page
    
app=Flask(__name__)
 #"It creates an instance of Flask Class,which will be your WSGI Application"
  
@app.route("/")
def welcome():
    return "<html><H1>HTML Integration with Flask</H1></html>"

@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__=="__main__":
    app.run(debug=True)  ##Entry point of any py file"
## Debug used for autosave