import plotly

def sankey_graph(filename, component_df, displayid, node_label_col, url_col,
                node_colour_col, source_col,target_col,value_col,
                link_colour_col, graph_title, url_not_name=True ):
  
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
