def input_data(uri, instance):
    import json
    import requests
    from pandas.io.json import json_normalize
    status = 200
    
    req = requests.get(instance)
    if req.status_code != 200: #if synbiohub is offline return an error
        status = 424
    else:
        fl = open("Input_Query.txt", "r")
        sparqlquery = fl.read()
        
        #replace the uri in the pre written sparql query with the uri of the part
        sparqlquery = sparqlquery.replace('https://synbiohub.org/public/igem/BBa_B0012/1',uri)
        
        #accept repsonses
        r = requests.post(instance+"sparql", data = {"query":sparqlquery}, headers = {"Accept":"application/json"})
        
        #format responses
        d = json.loads(r.text)
        a = json_normalize(d['results']['bindings'])
        
        #renames columns from ['count.datatype', 'count.type', 'count.value', 'def.type', 'def.value',
        #   'displayId.type', 'displayId.value', 'role.type', 'role.value',
        #   'title.type', 'title.value']
        a.columns = ['cd', 'ct','count', 'dt', 'deff', 'dist', 'displayId','rt', 'roletog', 'tt', 'title']
        
        #split column roletog at SO: to leave the http://identifiers.org/so in the column http
        #and the roler number (e.g. 0000141) in the column role
        a[['http','role']] = a.roletog.str.split("SO:",expand=True) 
        
        #drop unnecessary columns to leave: ['count', 'deff', 'displayId', 'title', 'role']
        a = a.drop(['cd', 'ct', 'dt', 'dist', 'rt', 'roletog', 'tt', 'http'],axis=1)
        
        #creates a df that has only one row (where the deff is the part in question)
        self_df = a[a.deff == uri]
        
        #obtains the displayid using the self df
        display_id = self_df['displayId'][0]
        
        #obtains the title/human readable name using the self df
        title = self_df['title'][0]
        
        #in case there was no title
        if str(title) == "nan":
            title = display_id
            
        #obtains the role (as a number, e.g. 000141) using the self df
        role = self_df['role'][0]
        
        #obtains the count using the self df
        count = self_df['count'][0]
        
    return (self_df, display_id, title, role, count)
