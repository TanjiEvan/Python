import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from flask import Flask,request,jsonify,render_template
 
    
application=Flask(__name__)
app=application
 #"It creates an instance of Flask Class,which will be your WSGI Application"

import os
ridge_model = pickle.load(open(os.path.join(os.path.dirname(__file__), 'models/ridge.pkl'), 'rb'))
Standard_Scaler = pickle.load(open(os.path.join(os.path.dirname(__file__), 'models/scaler.pkl'), 'rb'))


### IMPORT RIDGE nd STANDARD-SCALER PICKLE
#ridge_model=pickle.load(open('models/ridge.pkl','rb'))
#Standard_Scaler=pickle.load(open('models/scaler.pkl','rb'))

@app.route("/")
def index():
    return render_template('index.html') 

@app.route("/predictdata",methods=["GET","POST"])
def predict_datapoint():
    if request.method=="POST":
        Temperature=float(request.form.get('Temperature'))
        RH = float(request.form.get('RH'))
        Ws = float(request.form.get('Ws'))
        Rain = float(request.form.get('Rain'))
        FFMC = float(request.form.get('FFMC'))
        DMC = float(request.form.get('DMC'))
        ISI = float(request.form.get('ISI'))
        Classes = float(request.form.get('Classes'))
        Region = float(request.form.get('Region'))

        new_data=Standard_Scaler.transform([[Temperature,RH,Ws,Rain,FFMC,DMC,ISI,Classes,Region]])
        result=ridge_model.predict(new_data)
        return render_template('home.html',result=result[0])

    else:
        return render_template("home.html")
    




if __name__=="__main__":
    app.run(host="0.0.0.0") 