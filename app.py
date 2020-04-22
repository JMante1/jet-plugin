#FLASK_APP=app.py flask run
from flask import Flask, request, abort
from input_data import input_data
from find_role_name import find_role_name
from sankey import sankey
from sankey_graph import sankey_graph
from retrieve_html import retrieve_html
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
    uri = data['top_level']
    try:
        #instance = "synbiohub.org"
        print(url)
        print(instance)
        
        #instance = 'https://synbiohub.org/'
        #url = 'https://synbiohub.org/public/igem/BBa_B0012/1'
        #top_level = url

        
        cwd = os.getcwd()
        #print(cwd)

        #retrieve information about the poi
        self_df, display_id, title, role, count = input_data(uri, instance)

        #Find the role name in the ontology of the part of interest
        role_link = find_role_name(role, plural = False)

        #create data for the sankey diagram and format it correctly
        df_sankey = sankey(url, uri, title, instance)

        sankey_title = "Parts Co-Located with "+ title + " (a "+role_link+")"
        filename= os.path.join(cwd, f'sankey_{display_id}_.html')

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
    uri = data['top_level']
    try:
        #instance = 'https://synbiohub.org/'
        #url = 'https://synbiohub.org/public/igem/BBa_B0012/1'
        #top_level = url
        
        cwd = os.getcwd()
        print(cwd)

        from most_used_bar import most_used_bar
        from bar_plot import bar_plot
        from most_used_by_type import most_used_by_type
        from retrieve_html import retrieve_html
        from toggle_bars import toggle_bars

        #create input data
        self_df, display_id, title, role, count = input_data(uri, instance)

        #create and format data for the most_used barchart
        bar_df = most_used_bar(top_level, instance, display_id, title, role, 
                        count)

        #graph title for most used barchart
        graph_title = f'Top Ten Parts by Number of Uses Compared to <a href="{top_level}" target="_blank">{title}</a>'

        #where to save the file
        filename1= os.path.join(cwd, f'bar1_{display_id}_.html')

        #create the most used barchart
        bar_plot('title','count','color',bar_df, graph_title, filename1, 'deff',display_id)

        #retrieve html
        most_used = retrieve_html(filename1)

        #remove file
        os.remove(filename1)

        #find poi role ontology link
        role_link = find_role_name(role, plural = False)

        bar_df = most_used_by_type_bar(top_level,instance, display_id, title, 
                      role, count)

        #graph title for most used barchart
        graph_title = f'Top Ten {role_link} by Number of Uses Compared to <a href="{top_level}" target="_blank">{title}</a>'

        #where to save the file
        filename2= os.path.join(cwd, f'bar2_{display_id}_.html')

        #create the most used barchart
        bar_plot('title','count','color',bar_df, graph_title, filename2, 'deff',display_id)

        #retrieve html
        by_role = retrieve_html(filename2)

        #remove file
        os.remove(filename2)

        #create bar toggle html
        toggle_display = toggle_bars(most_used,by_role, display_id)

        return toggle_display
    except Exception as e:
        print(e)
        abort(404)
