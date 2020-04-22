import plotly
import plotly.graph_objs as go

def bar_plot (names,freq, colour, bar_df, graph_title, filename, url_link, display_id):
    
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
