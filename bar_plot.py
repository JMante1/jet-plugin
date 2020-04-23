import plotly
import plotly.graph_objs as go

def bar_plot (names,freq, colour, bar_df, graph_title, filename, url_link):
    """
    Uses the plotly library to plot a bargraph with the colour determined by one input
    and the names linking out to the appropriate pages.
    
    Requirements
    -------
    plotly
    plotly.graph_objs as go
    
    Parameters
    ----------
    names : string
        the column name that contains the 'names' of each of the bars, i.e. the text to display below each bar
    freq : string
        the column name that contains the frequency or count for each bar (determines bar height)
    colour : string
        name of the column in bar_df which contains the colours for each of the in bars
    url_link : string
        name of the column in bar_df which contains the urls which the bar labels will link out to when clicked
    bar_df : pandas dataframe, shape (n, 4 )
        Dataframe with the bar graph information. It needs at least 4 columns with the names provided in names (string),
        freq (number), colour (string e.g. 'rgba(4,187,61,1)'), and url_link (string)
    graph_title: string
        Title to put on the bar graph
    filename : string
        File location where the html document containing the bargraph is saved (e.g. 'current_working_directory//bar_graph_name.html')
    
    Returns
    -------
    Nothing is returned but an image is created at the address given by the filename
    
    
    Example
    --------
    import pandas as pd
    import os
    d = {'bar_labels': ['cats', 'dogs'], 'frequency': [3, 4], 'colours':[ 'rgba(0, 140, 255, 1)', ' rgba(226, 47, 129, 1)'],
        'urls':['https://en.wikipedia.org/wiki/Cat','https://en.wikipedia.org/wiki/Dog']}
    df = pd.DataFrame(data=d)
    
    cwd = os.getcwd()
    filename = os.path.join(cwd, 'Cats_versus_Dogs.html'
    bar_plot ('bar_labels','frequency', 'colours', df, graph_title, filename, 'urls')
    """
    
    #drop any blank names or links
    xnames = bar_df[names].dropna(axis=0, how='any')
    xlinks = bar_df[url_link].dropna(axis=0, how='any')

    #create a label with the title of the part displayed linking out to
    #the link specified by url_link
    sourcethings = '<a href="'+xlinks+'" target="_blank">'+xnames+'</a>'

    #format data as needed
    #https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.bar.html
    
    data = go.Bar(
        x= sourcethings, #names for each of the bars
        y=bar_df[freq].dropna(axis=0, how='any'), #heights for each of the bars
        hoverinfo = "y", #if you hover over the bar the information from the y axis is given, i.e. the count
        marker=dict(color=bar_df[colour].dropna(axis=0, how='any')), #colours for bars
    )

    #provide data in the appopriate format
    data = [data]
    
    #https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.layout.title.html
    layout = go.Layout(title = graph_title)  #set graph title

    #put all of the information together
    fig = go.Figure(data=data, layout=layout)
    
    #create the graph
    #need filename =filename not just filename, otherwise a random filename is generated
    plotly.offline.plot(fig, filename = filename, auto_open=False)
    
    return
