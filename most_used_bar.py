import pandas as pd
import requests
import json
from pandas.io.json import json_normalize

def most_used_bar(uri, instance, display_id, title, role, count):
    """
    Uses a sparql query to obtain information about the most used parts and format the data in such a way
    that a graph can be made comparing the poi (part of interest) to the most used parts
    
    Requirements
    -------
    import pandas as pd
    import requests
    import json
    from pandas.io.json import json_normalize
    Most_Used_Query.txt
    
    Parameters
    ----------
    uri : string
        the unique identifier of a part, note that due to spoofing it may not be the same as the url
        e.g. uri = 'https://synbiohub.org/public/igem/BBa_E0040/1' (url may be https://dev.synbiohub.org/public/igem/BBa_E0040/1)
    instance : string
        the synbiohub instance where information is to be retrieved from (where the sparql query is to be run)
        e.g. 'https://synbiohub.org/'
    display_id: string
        The display id of the poi e.g. 'BBa_E0040'
    title: string
        The human readable name of the poi e.g. 'GFP'
    role: string
        The number (as a string) of the sequence ontology of the role of the poi e.g. '0000316'    
    count: integer
        The number of times the poi is used (how often it is a subpart) e.g. 2348
        
    Returns
    -------
    bar_df: pandas dataframe, shape(11,6)
        columns are ['count', 'deff', 'displayId', 'roletog', 'title', 'color']
   
    Example
    --------
    display_id = 'BBa_E0040'
    title = 'GFP'
    role = '0000316'
    count = 2348
    
    uri = 'https://synbiohub.org/public/igem/BBa_E0040/1'
    instance = 'https://dev.synbiohub.org/'
    
    bar_df = most_used_bar(uri, instance, display_id, title, role, count)
    
    Output:
    count,deff,displayId,roletog,title,color
    12824,'https://synbiohub.org/public/igem/BBa_B0034/1','BBa_B0034','http://identifiers.org/so/SO:0000139','BBa_B0034','rgba(149,110,219,1)'
    9052,'https://synbiohub.org/public/igem/BBa_B0012/1','BBa_B0012','http://identifiers.org/so/SO:0000141','BBa_B0012','rgba(202,58,32,1)'
    8742,'https://synbiohub.org/public/igem/BBa_B0010/1','BBa_B0010','http://identifiers.org/so/SO:0000141','BBa_B0010','rgba(202,58,32,1)'
    4658,'https://synbiohub.org/public/igem/BBa_B0015/1','BBa_B0015','http://identifiers.org/so/SO:0000141','BBa_B0015','rgba(202,58,32,1)'
    2686,'https://synbiohub.org/public/igem/BBa_R0040/1','BBa_R0040','http://identifiers.org/so/SO:0000167','p(tetR)','rgba(4,187,61,1)'
    2550,'https://synbiohub.org/public/igem/BBa_J176041/1','BBa_J176041','http://identifiers.org/so/SO:0000110','scar','rgba(255, 128,0,1)'
    2030,'https://synbiohub.org/public/igem/BBa_B0030/1','BBa_B0030','http://identifiers.org/so/SO:0000139','BBa_B0030', 'rgba(149,110,219,1)'
    1902,'https://synbiohub.org/public/igem/BBa_B0032/1','BBa_B0032','http://identifiers.org/so/SO:0000139','BBa_B0032','rgba(149,110,219,1)'
    1876,'https://synbiohub.org/public/igem/BBa_R0010/1','BBa_R0010','http://identifiers.org/so/SO:0000167','LacI','rgba(4,187,61,1)'
    1306,'https://synbiohub.org/public/igem/BBa_R0011/1','BBa_R0011','http://identifiers.org/so/SO:0000167','lacI+pL','rgba(4,187,61,1)'
    2348,'https://synbiohub.org/public/igem/BBa_E0040/1','BBa_E0040','http://identifiers.org/so/SO:0000316','GFP','rgba(119,157,205,1)'
    """
    
    #get part url from uri
    part_url = uri.replace(uri[:uri.find('/', 8)+1], instance)
    
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
    for idx, deff in bar_df['deff'].items():
        bar_df['deff'][idx] = deff.replace(deff[:deff.find('/', 8)+1], instance)   

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
