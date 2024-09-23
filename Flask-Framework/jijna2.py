from flask import Flask,render_template,request,redirect,url_for    

#render_template --> Redirects to html page
    
app=Flask(__name__)
 #"It creates an instance of Flask Class,which will be your WSGI Application"
  
@app.route("/")
def welcome():
    return "<html><H1>HTML Integration with Flask</H1></html>"

@app.route("/index",methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/submit",methods=["GET","POST"])
def submit():
    if request.method=="POST":
        name=request.form["name"]
        return f'Hello {name}'
    return render_template("form.html")


@app.route("/about")
def about():
    return render_template("about.html")

## Variable Rule--> restricting a parameter with respect to data type
@app.route("/success/<int:score>")
def success(score):
    #return "The marks you got is," + str(score)
    res=""
    if score>=50:
        res="PASSED"
    else:
        res="FAILED"
    return render_template("result.html",results=res)

#### Jinja2 Template Engine 

'''
{{...}} --> expressions to print output in html
{%...%} --> conditions statement,loops
{#...#} --> Comments

'''

##With LOOP(in HTML)
@app.route("/successres/<int:score>")
def successres(score):
    #return "The marks you got is," + str(score)
    res=""
    if score>=50:
        res="PASSED"
    else:
        res="FAILED"

    exp={"score":score,"res":res}

    return render_template("result1.html",results=exp)


## With If-Else(in HTML)
@app.route("/successif/<int:score>")
def successif(score):
    #return "The marks you got is," + str(score)

   return render_template("result2.html",results=score)


##Dynamic URL

@app.route("/fail/<int:score>")
def fail(score):
    
  
    return render_template("result.html",results=score)

@app.route("/check", methods=["POST", "GET"])
def check():
    total_score = 0
    if request.method == "POST":
        science = float(request.form["science"])
        maths = float(request.form["maths"])
        c = float(request.form["c"])
        data_science = float(request.form["datascience"])

        total_score = (science + maths + c + data_science) / 4

    else:
        return render_template("get_result.html")
    
    return redirect(url_for("successres", score=int(total_score)))  






if __name__=="__main__":
    app.run(debug=True)  ##Entry point of any py file"
## Debug used for autosave