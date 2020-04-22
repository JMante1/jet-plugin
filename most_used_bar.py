def most_used_bar(top_level, instance, display_id, title, role, count):
    import pandas as pd
    import requests
    import json
    from pandas.io.json import json_normalize
    
    #get part url from uri
    part_url = url.replace('https://synbiohub.org/', instance)
    
    #read in the query to find the top most used parts
    fl = open("Most_Used_Query.txt", "r")
    sparqlquery = fl.read()
    
    #send the query
    r = requests.post(instance+"sparql", data = {"query":sparqlquery}, 
                      headers = {"Accept":"application/json"})
    
    #format query results
    d = json.loads(r.text)
    bar_df = json_normalize(d['results']['bindings'])
    
    #rename columns from ['count.datatype', 'count.type', 'count.value', 
    #        'def.type', 'def.value', 'displayId.type', 'displayId.value', 
    #        'role.type', 'role.value', 'title.type', 'title.value']
    bar_df.columns = ['cd', 'ct','count', 'dt', 'deff', 'dist', 'displayId',
                      'rt', 'roletog', 'tt', 'title']
    
    #drop unneeded columns
    bar_df = bar_df.drop(['cd', 'ct', 'dt', 'dist', 'rt', 'tt'], axis=1)
    
    #make sure the poi is not in the bar_df
    bar_df = bar_df[bar_df.displayId != display_id]
    
    #incase the poi was dropped reset the index (needed for colours to work)
    bar_df.reset_index(drop=True, inplace=True)
    
    #make sure it still works if less than 11 parts are present in the database
    robustness = min(10, len(bar_df)-1)
    
    #only accept the top robustness parts (usually the top eleven most used parts)
    bar_df = bar_df.iloc[0:robustness+1]
    
    #replace uris with urls
    bar_df['deff'] = bar_df.deff.replace('synbiohub.org', 
          instance.replace('https://', '').replace('/',''), regex=True)
    
    #change the final row in the dataframe (usually row 11)
    #to contain the information about the poi
    bar_df.iloc[robustness] = [count,part_url,display_id,
               "http://identifiers.org/so/SO:"+str(role),title]
    
    #define what colour each role should get (other is ignored)
    colormap = {
        'http://identifiers.org/so/SO:0000167': 'rgba(4,187,61,1)', 
        'http://identifiers.org/so/SO:0000139':'rgba(149,110,219,1)',
        'http://identifiers.org/so/SO:0000316':'rgba(119,157,205,1)',
        'http://identifiers.org/so/SO:0000141':'rgba(202,58,32,1)',
        
    }
    
    
    colours = []
    
    #for every element in bar
    for index in range(0, len(bar_df.index)):
        try:
            colours.append(colormap[bar_df['roletog'][index]])
        except KeyError: #if it is not one of the four basic roles
            colours.append("rgba(255, 128,0,1)") #the colour used is orange
            
    #add the column colour to the dataframe
    bar_df['color'] = pd.Series(colours, index=bar_df.index)
    
    #where the human name doesn't exist/isnull use the displayid
    bar_df.title[bar_df.title.isnull()] = bar_df.displayId[bar_df.title.isnull()]
    
    return(bar_df)
