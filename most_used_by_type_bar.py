def most_used_by_type_bar(url, instance, display_id, title, role, count):
    import pandas as pd
    import requests
    import json
    from pandas.io.json import json_normalize
    
    #get part url from uri
    part_url = url.replace('https://synbiohub.org/', instance)
    
    
    #open the query to collect the necessary data
    fl = open("Most_Used_By_Type_Query.txt", "r")
    sparql_query = fl.read()
    
    #replace the role with the relevant role
    sparql_query = sparql_query.replace("0000167", role)
    
    #perform the query
    r = requests.post(instance+"sparql", data = {"query":sparql_query}, headers = {"Accept":"application/json"})
    
    #format the data
    d = json.loads(r.text)
    bars_df = json_normalize(d['results']['bindings'])
    
    #rename the columns from ['count.datatype', 'count.type', 'count.value',
    #        'def.type', 'def.value', 'displayId.type', 'displayId.value', 
    #        'role.type', 'role.value', 'title.type', 'title.value']
    bars_df.columns = ['cd', 'ct','count', 'dt', 'deff', 'dist', 'displayId',
                       'rt', 'roletog', 'tt', 'title']
    
    #drop unneeded columns
    bars_df = bars_df.drop(['cd', 'ct', 'dt', 'dist', 'rt', 'tt'], axis=1)
    
    #remove the poi if it appears in the data
    bars_df = bars_df[bars_df.displayId != display_id]
    
    #make sure it still works if less than 11 parts are present in the database
    robustness = min(10, len(bar_df)-1)
    
    #only accept the top robustness parts (usually the top eleven most used parts)
    bars_df = bar_df.iloc[0:robustness+1]
    
    #replace uris with urls
    bars_df['deff'] = bar_df.deff.replace('synbiohub.org', 
          instance.replace('https://', '').replace('/',''), regex=True)
        
    #change the final row in the dataframe (usually row 11)
    #to contain the information about the poi
    bars_df.iloc[robustness] = [count,part_url,display_id,
               "http://identifiers.org/so/SO:"+str(role),title]
    
    #define what colour each role should get (other is ignored)
    colormap = {
        'http://identifiers.org/so/SO:0000167': 'rgba(4,187,61,1)', 
        'http://identifiers.org/so/SO:0000139':'rgba(149,110,219,1)',
        'http://identifiers.org/so/SO:0000316':'rgba(119,157,205,1)',
        'http://identifiers.org/so/SO:0000141':'rgba(202,58,32,1)',
        
    }
        
    #get full identifiers form of role
    part_role = "http://identifiers.org/so/SO:0000167".replace("0000167", role)
    
    
    try:
        colours = [colormap[part_role]] #make colours based on colormap
    except KeyError:
        colours = ["rgba(255, 128,0,1)"] #oran geif part type is other
        
    #ensure the length of colours is as long as the dataframe (generally 10)
    colours = colours*len(bars_df.index) 
    
    #add the column  colour to the dataframe
    bars_df['color'] = pd.Series(colours, index=bars_df.index)
    
    #if columns lack a human readable name used the displayid instead
    bars_df.title[bars_df.title.isnull()] = bars_df.displayId[bars_df.title.isnull()]
    
    return(bars_df)
