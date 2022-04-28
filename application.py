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

class DataStore2():
    Grupo=None
    Palabra=None
    Prod= None

class DataStore3():
    Grupo=None
    Revista=None
    Prod= None
data=DataStore()
data2=DataStore2()
data3=DataStore3()


@application.route("/main",methods=["GET","POST"])

#3. Define main code
@application.route("/",methods=["GET","POST"])
def homepage():
    Grupo = request.form.get('Group_field','GIIRA')
    
    data.Grupo=Grupo
    
    
    df = pd.read_csv('data/PublicacionesxAno.csv')
    df2 = pd.read_csv('data/PalabrasFrecxGrupoIngles.csv')
    df3 = pd.read_csv('data/GrupoXRevistas.csv')
    # dfP=dfP
    
    
    # print(Grupo)
    #Year = data.Year
    #data.Year = Year

    # choose columns to keep, in the desired nested json hierarchical order
    df = df[df.Grupo == Grupo]
    df2=df2.drop(['Grupo1','numero'], axis=1);
    df3 = df3[df3.Grupo == Grupo]
    #print(df2)
    #print("holi",df.head())
    # df = df.drop(
    # ['Country', 'Item Code', 'Flag', 'Unit', 'Year Code', 'Element', 'Element Code', 'Code', 'Item'], axis=1)
    
    df = df[["Grupo", "Year", "Value"]]
    df3 = df3[["Grupo", "Revista", "Cantidad"]]
    df = df.drop(["Grupo"],axis=1)
    df3 = df3.drop(["Grupo"],axis=1)
   # print (df)
    # order in the groupby here matters, it determines the json nesting
    # the groupby call makes a pandas series by grouping 'the_parent' and 'the_child', while summing the numerical column 'child_size'
    

    # start a new flare.json document
    flare = dict()
    d = {'name': "flare", "children": []}
    #print(df.values)
    for line in df.values:
        Anio = line[0]
        value = line[1]

        # make a list of keys
        keys_list = []

        for item in d['children']:
            
            keys_list.append(item['name'])
        #print (keys_list); 
       
        # if 'the_parent' IS a key in the flare.json, add a new child to it
        
        d['children'].append({"name": int(Anio), "size": int(value)})
        #print (d); 
    flare = d
    e = json.dumps(flare)
    data.Prod = json.loads(e)
    #Prod=data.Prod






# start a new flare.json document
    grupo_name=""
    flare2 = dict()
    d2 = {"name": "flare", "children": []}
    d3 = {"name": "flare", "children": []}
    #print(df.values)
    for line in df2.values:
        grupo = line[0]
        palabra = line[1]
        value = line[2]
        if(grupo_name!=grupo):
            print("holi")
            if(grupo_name!=""):
                
                d2['children'].append(d3)
                print(d2)
                d3['children'].clear()
                print(d3)
            grupo_name=grupo
           # d2['children'].append({"name":grupo, "children":[]})
            d3['name']=grupo_name
            print(grupo_name)
            d3['children'].append({"name": palabra, "value": int(value)})
            
        else:
            
            d3['children'].append({"name": palabra, "value": int(value)})
            # make a list of keys
            keys_list = []

            for item in d2['children']:
                
                keys_list.append(item['name'])
           # print (keys_list); 
       
        # if 'the_parent' IS a key in the flare.json, add a new child to it
        #d2['children'].append({"name":"holi"})
        print(d2)
           # d2[d2['children']['name']==grupo].append({"name": palabra, "children": int(value)})
        #print (d2); 
    flare2 = d2
    e2 = json.dumps(flare2)
    data2.Prod = json.loads(e2)
    
    with open('mydata2.json', 'w') as f:
        json.dump(data2.Prod , f)
   





    flare3 = dict()
    d4 = {}
    #print(df.values)
    for line in df3.values:
        Revista = line[0]
        value = line[1]

        # make a list of keys
        keys_list = []

        for item in d4:
            
            keys_list.append(item['name'])
        #print (keys_list); 
       
        # if 'the_parent' IS a key in the flare.json, add a new child to it
        
        d4.append({"name": Revista, "value": int(value)})
        print (d4); 
    flare3 = d4
    e3 = json.dumps(flare3)
    data3.Prod = json.loads(e3)
    with open('mydata3.json', 'w') as f:
        json.dump(data3.Prod , f)


    return render_template("index3.html",Grupo=Grupo,Prod=data.Prod)


@application.route("/get-data",methods=["GET","POST"])
def returnProdData():
    f=data.Prod

    return jsonify(f)
# export the final result to a json file


if __name__ == "__main__":
    application.run(debug=True)



