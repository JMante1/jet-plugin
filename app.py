#FLASK_APP=app.py flask run
from flask import Flask, request, abort
from input_data import input_data
from find_role_name import find_role_name
from sankey import sankey
from sankey_graph import sankey_graph
from retrieve_html import retrieve_html
from Full_v004_20190506 import *
import os
app = Flask(__name__)

#flask run --host=0.0.0.0
@app.route("/sankey/status")
def imdoingfine():
    return("Not dead Jet")

@app.route("/sankey/evaluate", methods=["POST", "GET"])
def evalsankey():
    return("Not dead Jet")


@app.route("/sankey/run", methods=["POST"])
def wrapper():
    data = request.json
    url = data['complete_sbol'].replace('/sbol','')
    instance = data['instanceUrl'].replace('/sbol','')
    toplevel = data['top_level']
    try:
        #instance = "synbiohub.org"
        print(url)
        print(instance)
        
        #instance = 'https://synbiohub.org/'
        #url = 'https://synbiohub.org/public/igem/BBa_B0012/1'
        #top_level = url

        
        #cwd = os.getcwd()
        #print(cwd)

        #retrieve information about the poi
        self_df, display_id, title, role, count = input_data(top_level, instance)

        #Find the role name in the ontology of the part of interest
        role_link = find_role_name(role, plural = False)

        #create data for the sankey diagram and format it correctly
        df_sankey = sankey(url, title, instance)

        sankey_title = "Parts Co-Located with "+ title + " (a "+role_link+")"
        filename= f'{cwd}\\percentcomponentsfrom_{display_id}_.html'

        #create the sankey diagram
        sankey_graph(filename, df_sankey, display_id, 'Node, Label',
                    'Link', 'Color', 'Source','Target', 'Value',
                    'Link Color', sankey_title, url_not_name=False) 

        #obtain the html from the sankey diagram
        sankey = retrieve_html(filename)

        #delete the copy of the sankey diagram on the server
        os.remove(filename)
       
        return sankey
    except Exception as e:
        print(e)
        abort(404)

#flask run --host=0.0.0.0
@app.route("/bar/status")
def imdoingfine2():
    return("Not dead Jet")

#@app.route("/bar/evaluate", methods=["POST", "GET"])
#def evalbar():
#    return("Not dead Jet")

@app.route("/bar/evaluate", methods=["POST", "GET"])
def evalbar():
    return("Not dead Jet")


@app.route("/bar/run", methods=["POST"])
def wrapper2():
    data = request.json
    url = data['complete_sbol'].replace('/sbol','')
    instance = data['instanceUrl'].replace('/sbol','')
    toplevel = data['top_level']
    try:
        #instance = "synbiohub.org"
        #instance = instance.replace('https://', '').replace('/','')
        narcissus, displayid, humanname, parttype, narcissuscount = inputdata(toplevel, instance)
        
        bar1 = mostused(toplevel, instance, narcissus, displayid, humanname, parttype, narcissuscount, "Top Ten Parts by Number of Uses Compared to "+ humanname)
        
        rolelink = findrolename(parttype, plural=True)
        bar2 = bytype(toplevel,instance, narcissus, displayid, humanname, parttype, narcissuscount, "Top Ten " +rolelink+" by Number of Uses Compared to "+ humanname)
        
        toggledisplay = togglebars(bar1,bar2, displayid)
        return toggledisplay
    except Exception as e:
        print(e)
        abort(404)
