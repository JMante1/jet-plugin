import plotly

def sankey_graph(filename, component_df, node_label_col, url_col,
                node_colour_col, source_col,target_col,value_col,
                link_colour_col, graph_title, url_not_name=True ):
    """
    Uses the plotly library to plot a sankey graph with the colour and width of links 
    determined by the input as well as the colour of the nodes.
    
    Requirements
    -------
    import plotly
        
    Parameters
    ----------
    filename : string
        File location where the html document containing the sankey graph is saved (e.g. 'current_working_directory//sankey_name.html')
    component_df: pandas dataframe, shape(n, 7)
        Dataframe with the columns: 'Source' (integer, from here),	'Target' (integer, to here), 'Value' (integer, width of link),
        'Color' (string, node colour (hex) e.g. #04BB3D), 'Node, Label' (str, name of the node e.g. GFP), 
        'Link' (str, link for the node e.g. https://synbiohub.org/public/igem/BBa_R0040/1),
        'Link Color' (string, (hex) e.g. rgba(4,187,61,0.5)
    node_label_col: string
        the component_df column name that contains the 'names' of each of the nodes, i.e. the text to display above each node
    url_col: string
        the column name for the column in component_df that contains the urls for the nodes to link out to (these
        links will only be used if url_not_name is False - though currently there is a bug in plotly so it doesn't work)
    source_col: string
        the component_df column name that contains the 'sources' of each of the links.
        For example if 0 then a link will be formed from the node described in row zero (goes to the node referenced
        by the target in the same row as the source)
    target_col: string
        the component_df column name that contains the 'targets' of each of the links.
        For example if 1 then a link will be formed to the node described in row zero (goes from the node referenced
        by the source in the same row as the target)
    value_col: string
        the component_df column name that contains the widths of each of the links (it refers to the width of the link
        described by the corresponding source and target in the row)
    link_colour_col: string
        the component_df column name that contains the colours of each of the links (it refers to the colour of the link
        described by the corresponding source and target in the row)
    graph_title: string
        Title to put on the bar graph
    url_not_name: Boolean, default:True 
        When true nodes are labelled with clickable links rather than just names (currenlty there is a bug in plotly so
        this doesn't work)
    
    Returns
    -------
    Nothing is returned but an image is created at the address given by the filename
   
    Example
    --------
    import pandas as pd
    import os
    
    diction = {'Source': [0, 1, 2, 3, 4, 5, 6, nan],
               'Target': [5, 5, 6, 6, 6, 7, 7, nan],
               'Value': [100.0, 100.0, 100.0, 100.0, 100.0, 200.0, 300.0, nan],
               'Color': ['#04BB3D', '#04BB3D', '#956EDB', '#956EDB', '#956EDB', '#04BB3D', '#956EDB', '#CA3A20'],
               'Node, Label': ['Cat', 'Dog', 'Gold Fish', 'Tuna', 'Salmon', 'Mammals', 'Fish', 'Animals'],
               'Link': ['https://en.wikipedia.org/wiki/Animal','https://en.wikipedia.org/wiki/Cat','https://en.wikipedia.org/wiki/Dog',
                        'https://en.wikipedia.org/wiki/Goldfish','https://en.wikipedia.org/wiki/Tuna',
                        'https://en.wikipedia.org/wiki/Salmon', 'https://en.wikipedia.org/wiki/Mammal',
                        'https://en.wikipedia.org/wiki/Fish'],
               'Link Color': ['rgba(4,187,61,0.5)', 'rgba(4,187,61,0.5)', 'rgba(4,187,61,0.5)', 'rgba(4,187,61,0.5)',
                          'rgba(4,187,61,0.5)', 'rgba(4,187,61,0.5)', 'rgba(4,187,61,0.5)', nan]}
                          
    component_df = pd.DataFrame.from_dict(diction)
    
    cwd = os.getcwd()
    filename = os.path.join(cwd, 'Animal_Groups_Sankey.html')
    
    sankey_graph(filename, component_df, 'Node, Label', 'Link', 'Color', 'Source', 'Target', 'Value',
                'Link Color', 'Animal Groups', url_not_name=False)
                
                
    Output:
    (Sankey connections will look like this (in colour and with appropriate thicknesses though)
    
    Cat ------------\
                    Mamals --------\
    Dog ------------/               \
                                    Animals
    Gold Fish ------\               /
    Tuna -----------Fish ----------/
    Salmon ---------/
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
