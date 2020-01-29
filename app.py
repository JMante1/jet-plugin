#FLASK_APP=app.py flask run
from flask import Flask, request, abort
from Full_v004_20190506 import *
app = Flask(__name__)

#flask run --host=0.0.0.0
@app.route("/sankey/status")
def imdoingfine():
    return("Not dead Jet")

@app.route("/sankey/evaluate")
def evalsankey():
    return("Not dead Jet")


@app.route("/sankey/run", methods=["POST"])
def wrapper():
    data = request.json
    url = data['complete_sbol'].replace('/sbol','')
    instance = data['instanceUrl'].replace('/sbol','')
    try:
        #instance = "synbiohub.org"
        print(url)
        print(instance)
        #instance = instance.replace('https://', '').replace('/','')
        narcissus, displayid, humanname, parttype, narcissuscount = inputdata(url, instance)
        
       
        rolelink = findrolename(parttype)
        print(rolelink)
        sankey = sankeyalazach(url, instance, narcissus, displayid, humanname, parttype, narcissuscount, "Parts Co-Located with "+ humanname + " (a "+rolelink+")")
        #print(sankey)
        return sankey
    except Exception as e:
        print(e)
        abort(404)

#flask run --host=0.0.0.0
@app.route("/bar/status")
def imdoingfine2():
    return("Not dead Jet")

@app.route("/bar/evaluate")
def evalbar():
    return("Not dead Jet")


@app.route("/bar/run", methods=["POST"])
def wrapper2():
    data = request.json
    url = data['complete_sbol'].replace('/sbol','')
    instance = data['instanceUrl'].replace('/sbol','')
    try:
        #instance = "synbiohub.org"
        #instance = instance.replace('https://', '').replace('/','')
        narcissus, displayid, humanname, parttype, narcissuscount = inputdata(url, instance)
        
        bar1 = mostused(url, instance, narcissus, displayid, humanname, parttype, narcissuscount, "Top Ten Parts by Number of Uses Compared to "+ humanname)
        
        rolelink = findrolename(parttype, plural=True)
        bar2 = bytype(url,instance, narcissus, displayid, humanname, parttype, narcissuscount, "Top Ten " +rolelink+" by Number of Uses Compared to "+ humanname)
        
        toggledisplay = togglebars(bar1,bar2, displayid)
        return toggledisplay
    except Exception as e:
        print(e)
        abort(404)

