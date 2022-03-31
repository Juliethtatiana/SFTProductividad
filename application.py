from flask import Flask, flash, redirect, render_template, request, session, abort,send_from_directory,send_file,jsonify
import pandas as pd

import json




#1. Declare application
application= Flask(__name__)

#2. Declare data stores
class DataStore():
    Grupo=None
    Year=None
    Prod= None
data=DataStore()


@application.route("/main",methods=["GET","POST"])

#3. Define main code
@application.route("/",methods=["GET","POST"])
def homepage():
    Grupo = request.form.get('Group_field','GIIRA')
    
    data.Grupo=Grupo
    
    
    df = pd.read_csv('data/PublicacionesxAno.csv')
    # dfP=dfP
    
    
    # print(Grupo)
    #Year = data.Year
    #data.Year = Year

    # choose columns to keep, in the desired nested json hierarchical order
    df = df[df.Grupo == Grupo]
    print(df.head())
    # df = df.drop(
    # ['Country', 'Item Code', 'Flag', 'Unit', 'Year Code', 'Element', 'Element Code', 'Code', 'Item'], axis=1)
    df = df[["Grupo", "Year", "Value"]]

    # order in the groupby here matters, it determines the json nesting
    # the groupby call makes a pandas series by grouping 'the_parent' and 'the_child', while summing the numerical column 'child_size'
    

    # start a new flare.json document
    flare = dict()
    d = {"name": "flare", "children": []}

    for line in df.values:
        Anio = line[1]
        value = line[2]

        # make a list of keys
        keys_list = []

        for item in d['children']:
            
            keys_list.append(item['name'])
        print (keys_list); 
       
        # if 'the_parent' IS a key in the flare.json, add a new child to it
        
        d['children'].append({"name": Anio, "size": value})
        print (d); 
    flare = d
    e = json.dumps(flare)
    data.Prod = json.loads(e)
    Prod=data.Prod

    
   



    return render_template("index.html",Grupo=Grupo,Prod=Prod)


@application.route("/get-data",methods=["GET","POST"])
def returnProdData():
    f=data.Prod

    return jsonify(f)
# export the final result to a json file


if __name__ == "__main__":
    application.run(debug=True)



