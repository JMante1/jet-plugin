import plotly

def sankey_graph(filename, component_df, displayid, node_label_col, url_col,
                node_colour_col, source_col,target_col,value_col,
                link_colour_col, graph_title, url_not_name=True ):
  """
    This function creates the table needed to make the sankey diagram
    to create the sankey diagram two linked tables are needed
    1) about nodes: indexes, names and colours
    2) about the links: from node a (index), to node b (index), width, colour
    
    Requirements
    -------
    import requests
    import json
    import pandas as pd
    from pandas.io.json import json_normalize
    Preceding_Percent_Query.txt
    
    
    Parameters
    ----------
    url : string
        the url that links to the part, note that due to spoofing it may not be the same as the uri
        e.g. url = 'https://dev.synbiohub.org/public/igem/BBa_E0040/1' (uri may be https://synbiohub.org/public/igem/BBa_E0040/1)
    uri : string
        the unique identifier of a part, note that due to spoofing it may not be the same as the url
        e.g. uri = 'https://synbiohub.org/public/igem/BBa_E0040/1' (url may be https://dev.synbiohub.org/public/igem/BBa_E0040/1)
    title: string
        The human readable name of the poi e.g. 'GFP'
    instance : string
        the synbiohub instance where information is to be retrieved from (where the sparql query is to be run)
        e.g. 'https://synbiohub.org/'
    
    Returns
    -------
    skey: pandas dataframe, shape(n, 7)
        Dataframe with the columns: 'Source' (integer, from here),	'Target' (integer, to here), 'Value' (integer, width of link),
        'Color' (string, node colour (hex) e.g. #04BB3D), 'Node, Label' (str, name of the node e.g. GFP), 
        'Link' (str, link for the node e.g. https://synbiohub.org/public/igem/BBa_R0040/1),
        'Link Color' (string, (hex) e.g. rgba(4,187,61,0.5)
       
    Example
    --------
    uri = 'https://synbiohub.org/public/igem/BBa_E0040/1'
    url = 'https://dev.synbiohub.org/public/igem/BBa_E0040/1'
    instance = 'https://dev.synbiohub.org/'
    title = 'GFP'
    
    skey = sankey(url, uri, title, instance)
      'Source','Target',Value,Color,"Node, Label",Link,Link Color
    1,6,100,#04BB3D,Animals,https://en.wikipedia.org/wiki/Animal,"rgba(4,187,61,0.5)"
    2,6,100,#956EDB,Cat,https://en.wikipedia.org/wiki/Cat,"rgba(4,187,61,0.5)"
    3,7,100,#779DCC,Dog,https://en.wikipedia.org/wiki/Dog,"rgba(4,187,61,0.5)"
    4,7,100,#CA3A20,Gold Fish,https://en.wikipedia.org/wiki/Goldfish,"rgba(4,187,61,0.5)"
    5,7,100,#CA3A21,Tuna,https://en.wikipedia.org/wiki/Tuna,"rgba(4,187,61,0.5)"
    6,0,200,#CA3A22,Salmon,https://en.wikipedia.org/wiki/Salmon,"rgba(4,187,61,0.5)"
    7,0,300,#FF8000,Mammals,https://en.wikipedia.org/wiki/Mammal,"rgba(4,187,61,0.5)"
    ,,,#04BB3D,Fish,https://en.wikipedia.org/wiki/Fish,
  """
  
    #removes any NAs from the list of node names
    xnames = component_df[node_label_col].dropna(axis=0, how='any')
    
    #removes any pandas NAs from the list of links
    xlinks = component_df[url_col].dropna(axis=0, how='any')
    
    #if url_not_name is true than uses an html version that
    #displays the names but links to the urls
    if url_not_name:
        sourcethings = '<a xlink:href="'+xlinks+'">'+xnames+'</a>'
    else:
        sourcethings = xnames
    
    #make the data package for plotly to use
    #https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.Sankey.html
    
    data_trace = dict(
        type='sankey',
        domain = dict(
            x = [0,1], #indicates the plot streches from x = 0 to x = 1
            y = [0,1]), #indicates the plot streches from y = 0 to y = 1
        orientation = "h", #Sets the orientation of the Sankey diagram - h = horizontal
        valueformat = ".0f", #Sets the label value formatting rule using d3 formatting mini-language
        arrangement = "perpendicular", #nodes can only move perpendicular to direction of flow, so preserve 'columns' in this case
        node = dict(
            pad = 10, #Sets the padding (in px) between the nodes
            thickness = 30, #Sets the thickness, here it means the nodes are 30 pixels wide
            line = dict( #outlines nodes with a black 0.5 line
                color = "black",
                width = 0.5),
            label = sourcethings, #the labels to use for the nodes
            color = component_df[node_colour_col].dropna(axis=0, how='any'),), #colours of nodes
        link = dict(
            source = component_df[source_col].dropna(axis=0, how='any'), #link goes from this source
            target = component_df[target_col].dropna(axis=0, how='any'), #to this target
            value = component_df[value_col].dropna(axis=0, how='any'), #with this thickness/width
            color = component_df[link_colour_col].dropna(axis=0, how='any'),)) #in this colour
    
    layout = dict(
        title = graph_title, #add a title to the figure
        height = 772, #set figure height
        width = 950, #set figure width
        font = dict(size = 10),) #set fontsize to 10
    
    fig = dict(data=[data_trace], layout=layout)
    
    #create the graph
    #need filename =filename not just filename, otherwise a random filename is generated
    plotly.offline.plot(fig, filename=filename, auto_open=False)
    return
