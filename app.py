#FLASK_APP=app.py flask run
from flask import Flask, request, abort
from input_data import input_data
from find_role_name import find_role_name
from sankey import sankey
from sankey_graph import sankey_graph
from retrieve_html import retrieve_html

from most_used_bar import most_used_bar
from bar_plot import bar_plot
from most_used_by_type_bar import most_used_by_type_bar
from toggle_bars import toggle_bars

import os

app = Flask(__name__)

#flask run --host=0.0.0.0
@app.route("/sankey/status")
def Sankey_Status():
    return("The sankey plugin is up and running")

@app.route("/sankey/evaluate", methods=["POST"])
def Sankey_Evaluate():
    data = request.get_json(force=True)
    rdf_type = data['type']
    
    ########## REPLACE THIS SECTION WITH OWN RUN CODE #################
    #uses rdf types
    accepted_types = {'Component'}
    
    acceptable = rdf_type in accepted_types
    
    # #to ensure it shows up on all pages
    # acceptable = True
    ################## END SECTION ####################################
    
    if acceptable:
        return f'The type sent ({rdf_type}) is an accepted type', 200
    else:
        return f'The type sent ({rdf_type}) is NOT an accepted type', 415


@app.route("/sankey/run", methods=["POST"])
def Sankey_Run():
    data = request.get_json(force=True)
    
    top_level_url = data['top_level']
    complete_sbol = data['complete_sbol']
    instance_url = data['instanceUrl']
    size = data['size']
    rdf_type = data['type']
    shallow_sbol = data['shallow_sbol']
    
    url = complete_sbol.replace('/sbol','')
    
    try:
        
        #instance_ur = 'https://synbiohub.org/'
        #url = 'https://synbiohub.org/public/igem/BBa_B0012/1'
        #top_level_url = 'https://dev.synbiohub.org/public/igem/BBa_B0012/1'
        
        #get current working directory
        cwd = os.getcwd()

        #retrieve information about the poi
        self_df, display_id, title, role, count = input_data(top_level_url, instance_url)

        #print("Find role name")
        #Find the role name in the ontology of the part of interest
        role_link = find_role_name(role, plural = False)

        #create data for the sankey diagram and format it correctly
        df_sankey = sankey(url, top_level_url, title, instance_url)

        sankey_title = "Parts Co-Located with "+ title + " (a "+role_link+")"
        filename= os.path.join(cwd, f'sankey_{display_id}_.html')

        #create the sankey diagram
        sankey_graph(filename, df_sankey, 'Node, Label',
                    'Link', 'Color', 'Source','Target', 'Value',
                    'Link Color', sankey_title, url_not_name=False) 

        #obtain the html from the sankey diagram
        result = retrieve_html(filename)

        #delete the copy of the sankey diagram on the server
        os.remove(filename)
       
        return result 
    except Exception as e:
        print(e)
        abort(400)

#flask run --host=0.0.0.0
@app.route("/bar/status")
def Bar_Status():
    return("The bar plugin is up and running")


@app.route("/bar/evaluate", methods=["POST"])
def Bar_Evaluate():
    data = request.get_json(force=True)
    rdf_type = data['type']
    
    ########## REPLACE THIS SECTION WITH OWN RUN CODE #################
    #uses rdf types
    accepted_types = {'Component'}
    
    acceptable = rdf_type in accepted_types
    
    # #to ensure it shows up on all pages
    # acceptable = True
    ################## END SECTION ####################################
    
    if acceptable:
        return f'The type sent ({rdf_type}) is an accepted type', 200
    else:
        return f'The type sent ({rdf_type}) is NOT an accepted type', 415


@app.route("/bar/run", methods=["POST"])
def Bar_Run():
    data = request.get_json(force=True)
    
    top_level_url = data['top_level']
    complete_sbol = data['complete_sbol']
    instance_url = data['instanceUrl']
    size = data['size']
    rdf_type = data['type']
    shallow_sbol = data['shallow_sbol']
    
    url = complete_sbol.replace('/sbol','')

    try:
        
        #current working directory
        cwd = os.getcwd()

        #create input data
        self_df, display_id, title, role, count = input_data(top_level_url, instance_url)
        
        #create and format data for the most_used barchart
        bar_df = most_used_bar(top_level_url, instance_url, display_id, title, role, 
                        count)
        
        #graph title for most used barchart
        graph_title = f'Top Ten Parts by Number of Uses Compared to <a href="{url}" target="_blank">{title}</a>'

        #where to save the file
        filename1= os.path.join(cwd, f'bar1_{display_id}.html')

        #create the most used barchart
        bar_plot('title','count','color',bar_df, graph_title, filename1, 'deff')

        #retrieve html
        most_used = retrieve_html(filename1)

        #remove file
        os.remove(filename1)

        #find poi role ontology link
        role_link = find_role_name(role, plural = False)

        bar_df = most_used_by_type_bar(top_level_url,instance_url, display_id, title, 
                      role, count)

        #graph title for most used barchart
        graph_title = f'Top Ten {role_link} by Number of Uses Compared to <a href="{url}" target="_blank">{title}</a>'

        #where to save the file
        filename2= os.path.join(cwd, f'bar2_{display_id}.html')

        #create the most used barchart
        bar_plot('title','count','color',bar_df, graph_title, filename2, 'deff')

        #retrieve html
        by_role = retrieve_html(filename2)

        #remove file
        os.remove(filename2)

        #create bar toggle html
        toggle_display = toggle_bars(most_used,by_role)

        return toggle_display
    except Exception as e:
        print(e)
        abort(400)
