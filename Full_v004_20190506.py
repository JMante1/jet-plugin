def inputdata(url, instance):
    import json
    import requests
    from pandas.io.json import json_normalize
    status = 200
    
    req = requests.get(instance)
    if req.status_code != 200: #if synbiohub is offline return an error
        status = 424
    else:
        fl = open("sparql.txt", "r")
        sparqlquery = fl.read()
        
        #replace the uri in the pre written sparql query with the uri of the part
        sparqlquery = sparqlquery.replace('https://synbiohub.org/public/igem/BBa_B0012/1',url)
        
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
        self_df = a[a.deff == url]
        
        #obtains the displayid using the self df
        display_id = self_df['displayId'][0]
        
        #obtains the title/human readable name using the self df
        title = self_df['title'][0]
        
        #in case there was no title
        if str(title) == "nan":
            humanname = display_id
            
        #obtains the role (as a number, e.g. 000141) using the self df
        role = self_df['role'][0]
        
        #obtains the count using the self df
        count = self_df['count'][0]
        
    return (self_df, display_id, title, role, count)

def sankeygraph(filename, component_df, displayid, nodelabelcol, linkcol, nodecolourcol, sourcecol,targetcol,valuecol, linkcolourcol, graphtitle, urlnotname=True ):
    import plotly
    
    xnames = component_df[nodelabelcol].dropna(axis=0, how='any')
    xlinks = component_df[linkcol].dropna(axis=0, how='any')
    if urlnotname:
        sourcethings = '<a xlink:href="'+xlinks+'">'+xnames+'</a>'
    else:
        sourcethings = xnames
    
    data_trace = dict(
    type='sankey',
    domain = dict(
    x = [0,1],
    y = [0,1]
    ),
    orientation = "h",
    valueformat = ".0f",
    arrangement = "perpendicular",
    node = dict(
    pad = 10,
    thickness = 30,
    line = dict(
    color = "black",
    width = 0.5
    ),
    
    label = sourcethings,
    color = component_df[nodecolourcol].dropna(axis=0, how='any'),
    ),
    
    link = dict(
    source = component_df[sourcecol].dropna(axis=0, how='any'),
    target = component_df[targetcol].dropna(axis=0, how='any'),
    value = component_df[valuecol].dropna(axis=0, how='any'),
    color = component_df[linkcolourcol].dropna(axis=0, how='any'),
    )
    )
    
    layout = dict(
    title = graphtitle,
    height = 772,
    width = 950,
    font = dict(
    size = 10
    ),
    )
    
    fig = dict(data=[data_trace], layout=layout)
    #plotly.offline.plot(fig, filename = 'static/componentsfrom_'+displayid+'_.html', auto_open=True)
    plotly.offline.plot(fig, filename = 'static/'+filename+'_'+displayid+'_.html', auto_open=False)
    return

def sankeyalazach(url, instance, narcissus, displayid, humanname, parttype, narcissuscount, graphtitle, printer = False):
    import requests
    import json
    import pandas as pd
    import numpy as np
    from pandas.io.json import json_normalize
    
    partcolour = "#000000" 
    
    fl = open("SparqlPreecedingPercent2.txt", "r")
    #fl = open("SparqlPreecedingPercent.txt", "r")
    sparqlquery = fl.read()
    sparqlquery = sparqlquery.replace('https://synbiohub.org/public/igem/BBa_E0040/1',url)
    r = requests.post(instance+"sparql", data = {"query":sparqlquery}, headers = {"Accept":"application/json"})
    print("Got R")
    print(instance+"sparql")
    print(sparqlquery)
    d = json.loads(r.text)
    #print(d)
    preflow = json_normalize(d['results']['bindings'])
    print(preflow)
    print(preflow.shape)
    preflow.columns = ['ad', 'at','centfol', 'cd', 'ct', 'count', 'dt','deff', 'dt1', 'displayId','rt', 'roletog', 'tt','title']
    preflow = preflow.drop(preflow.columns[[0,1, 3, 4, 6, 8,10,12]], axis=1)
    
    preflow['count'] = preflow['count'].apply(pd.to_numeric)
    preflow['centfol'] = preflow['centfol'].apply(pd.to_numeric)
    preflow = preflow[preflow['deff'] != url]
    preflow['deff'] = preflow.deff.replace('synbiohub.org', instance.replace('https://', '').replace('/',''), regex=True)
    preflow.title[preflow.title.isnull()] = preflow.displayId[preflow.title.isnull()]

    other = preflow
    prom = preflow.loc[preflow['roletog'] == 'http://identifiers.org/so/SO:0000167']
    other = preflow[preflow['roletog'] != 'http://identifiers.org/so/SO:0000167']
    rbs = preflow.loc[preflow['roletog'] == 'http://identifiers.org/so/SO:0000139']
    other = other[other['roletog'] != 'http://identifiers.org/so/SO:0000139']
    cds = preflow.loc[preflow['roletog'] == 'http://identifiers.org/so/SO:0000316']
    other = other[other['roletog'] != 'http://identifiers.org/so/SO:0000316']
    term = preflow.loc[preflow['roletog'] == 'http://identifiers.org/so/SO:0000141']
    other = other[other['roletog'] != 'http://identifiers.org/so/SO:0000141']
    partarray = [prom, rbs, cds, term, other]
    
    greatlengths = [len(prom), len(rbs), len(cds), len(term), len(other)]
    linkcolours = ["rgba(4,187,61,0.5)", "rgba(149,110,219,0.5)", "rgba(119,157,205,0.5)", "rgba(202,58,32,0.5)", "rgba(255, 128,0,0.5)"]
    nodecolours = ["#04BB3D", "#956EDB", "#779DCC", "#CA3A20", "#FF8000"]
    
    arsource = []
    artarget = []
    arvalue = []
    arpercent = []
    armultiplier = []
    arnodecolour =  nodecolours
    arnodelabel = ["Preceeding Promoters", "Preceeding RBS", "Preceeding CDS", "Preceeding Terminator", "Preceeding Other"]
    arnodeurl = ["NA", "NA","NA","NA", "NA"]
    arlinkcolour = []
    
    lenparttype = [0,0,0,0,0]
    target = 4
    
    #part type to preceding parts
    for parttypeindex in range(0,5):
        lenparttype[parttypeindex] = min(greatlengths[parttypeindex], 10)
        for index in range(0,lenparttype[parttypeindex]):
            arlinkcolour.append(linkcolours[parttypeindex])
            arnodecolour.append(nodecolours[parttypeindex])
            arnodelabel.append(partarray[parttypeindex].iloc[index,5])
            arnodeurl.append(partarray[parttypeindex].iloc[index,2])
            percent = partarray[parttypeindex].iloc[index,0]
            arpercent.append(percent) 
            armultiplier.append(partarray[parttypeindex].iloc[index,1])
            arvalue.append(partarray[parttypeindex].iloc[index,1]*(1-percent))
            arsource.append(parttypeindex)
            target = target + 1
            artarget.append(target)
    
    #Preceding parts to POI
    xlength = len(arlinkcolour)
    xlinkcolour = arlinkcolour
    xvalue = arvalue
    xtarget = artarget
    xname = arnodelabel[5:]
    xurl = arnodeurl[5:]
    xnodecolour = arnodecolour[5:]
    xmultiplier = armultiplier
    xsource = arsource
    arlinkcolour = arlinkcolour +xlinkcolour
    arsource = arsource + xtarget
    arvalue = arvalue + xvalue
    poinode = target+1
    artarget = artarget + [poinode]*xlength
    
    #POI
    arnodelabel.append(humanname)
    arnodecolour.append(partcolour)
    tempurl = url.replace('https://synbiohub.org/', instance)
    arnodeurl.append(tempurl)
    
    #POI to following parts
    arsource = arsource + [poinode]*xlength
    artarget = artarget + [x for x in range(poinode + 1, np.sum(lenparttype)+poinode+1)]
    arlinkcolour = arlinkcolour + xlinkcolour
    yvalue = np.array(xmultiplier)*arpercent
    arvalue = arvalue + yvalue.tolist()
    
    arnodelabel = arnodelabel + xname
    arnodeurl = arnodeurl +xurl
    arnodecolour = arnodecolour + xnodecolour
    
    
    #Following parts to part types
    arnodelabel = arnodelabel + ["Following Promoters", "Following RBS", "Following CDS", "Following Terminator", "Following Other"]
    arnodeurl = arnodeurl + ["NA", "NA","NA","NA", "NA"]
    arnodecolour = arnodecolour + ["#04BB3D", "#956EDB", "#779DCC", "#CA3A20", "#FF8000"]
    
    arsource = arsource + [x for x in range(poinode + 1, np.sum(lenparttype)+poinode+1)]
    a = np.array(xsource)+arsource[-1]+1
    artarget = artarget + a.tolist()
    arlinkcolour = arlinkcolour + xlinkcolour
    arvalue = arvalue + yvalue.tolist()
    
    
    skey =  pd.DataFrame(data =[arsource, artarget, arvalue, arnodecolour, arnodelabel, arnodeurl, arlinkcolour], index =["Source", "Target", "Value","Color","Node, Label","Link","Link Color"])
    skey = skey.T
    #skey.to_csv('out.csv')
    
    
    component_df = skey
    nodelabelcol = 'Node, Label'
    linkcol = 'Link'
    nodecolourcol = 'Color'
    sourcecol = 'Source'
    targetcol = 'Target'
    valuecol = 'Value'
    linkcolourcol = 'Link Color'
    filename= 'percentcomponentsfrom'
    sankeygraph(filename, component_df, displayid, nodelabelcol, linkcol, nodecolourcol, sourcecol,targetcol,valuecol, linkcolourcol, graphtitle, urlnotname=False)
    sankey= 'static/'+'percentcomponentsfrom'+'_'+displayid+'_.html'                  
    sankey = retrievehtml(sankey)
    
    if printer:
        skey.to_csv('static/'+'sankey'+'_' + displayid + '.csv')
#        Html_file= open('static/'+'sankey'+'_' + displayid + '.csv',"w")
#        Html_file.write(skey)
#        Html_file.close()
    
    return (sankey)

def barart (names,freq, colour, bar_df, title, filename,urllink,displayid):
    import plotly
    import plotly.graph_objs as go

    xnames = bar_df[names].dropna(axis=0, how='any')
    xlinks = bar_df[urllink].dropna(axis=0, how='any')

    sourcethings = '<a href="'+xlinks+'" target="_blank">'+xnames+'</a>'

    trace0 = go.Bar(
        x= sourcethings,
        y=bar_df[freq].dropna(axis=0, how='any'),
        hoverinfo = "y",
        marker=dict(
            color=bar_df[colour].dropna(axis=0, how='any')),
    )

    data = [trace0]
    layout = go.Layout(
        title = title
    )

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename = 'static/'+filename+'_'+displayid+'_.html', auto_open=False)
    return

def mostused(url, instance, narcissus, displayid, humanname, parttype, narcissuscount, graphtitle):
    import pandas as pd
    import requests
    import json
    from pandas.io.json import json_normalize
    
    fl = open("Sparqlmostused.txt", "r")
    sparqlquery = fl.read()
    r = requests.post(instance+"sparql", data = {"query":sparqlquery}, headers = {"Accept":"application/json"})
    d = json.loads(r.text)
    raisingthebar = json_normalize(d['results']['bindings'])
    raisingthebar.columns = ['cd', 'ct','count', 'dt', 'deff', 'dist', 'displayId','rt', 'roletog', 'tt', 'title']
    raisingthebar = raisingthebar.drop(raisingthebar.columns[[0,1, 3, 5,7, 9]], axis=1)
    raisingthebar = raisingthebar[raisingthebar.displayId != displayid]
    robustness = min(10, len(raisingthebar)-1)
    raisingthebar = raisingthebar.iloc[0:robustness+1]
    raisingthebar['deff'] = raisingthebar.deff.replace('synbiohub.org', instance.replace('https://', '').replace('/',''), regex=True)
    tempurl = url.replace('https://synbiohub.org/', instance)
    raisingthebar.iloc[robustness] = [narcissuscount,tempurl,displayid,"http://identifiers.org/so/SO:"+str(parttype),humanname]
    colormap = {
        'http://identifiers.org/so/SO:0000167': 'rgba(4,187,61,1)', 
        'http://identifiers.org/so/SO:0000139':'rgba(149,110,219,1)',
        'http://identifiers.org/so/SO:0000316':'rgba(119,157,205,1)',
        'http://identifiers.org/so/SO:0000141':'rgba(202,58,32,1)',
        
    }
    colours = []
    for index in range(0, len(raisingthebar.index)):
        try:
            colours.append(colormap[raisingthebar.iloc[index,3]])
        except KeyError:
            colours.append("rgba(255, 128,0,1)")
    raisingthebar['color'] = pd.Series(colours, index=raisingthebar.index)
    raisingthebar.title[raisingthebar.title.isnull()] = raisingthebar.displayId[raisingthebar.title.isnull()]
    
    bar_df = raisingthebar
    colour = 'color'
    names = 'title'
    freq = 'count'
    urllink = 'deff'
    filename = 'mostused'
    barart(names,freq,colour,bar_df, graphtitle, filename, urllink,displayid)
    bar1= 'static/'+'mostused'+'_'+displayid+'_.html'
    bar1 = retrievehtml(bar1)
    return (bar1)

def bytype(url, instance, narcissus, displayid, humanname, parttype, narcissuscount, graphtitle):
    import pandas as pd
    import requests
    import json
    from pandas.io.json import json_normalize
    
    fl = open("Sparqlmostused1.txt", "r")
    sparqlquery = fl.read()
    sparqlquery = sparqlquery.replace("0000167", parttype)
    r = requests.post(instance+"sparql", data = {"query":sparqlquery}, headers = {"Accept":"application/json"})
    d = json.loads(r.text)
    behindbars = json_normalize(d['results']['bindings'])
    
    behindbars.columns = ['cd', 'ct','count', 'dt', 'deff', 'dist', 'displayId','rt', 'roletog', 'tt', 'title']
    behindbars = behindbars.drop(behindbars.columns[[0,1, 3, 5,7, 9]], axis=1)
    behindbars = behindbars[behindbars.displayId != displayid]
    robustness = min(10, len(behindbars)-1)
    behindbars = behindbars.iloc[0:robustness+1]
    behindbars['deff'] = behindbars.deff.replace('synbiohub.org', instance.replace('https://', '').replace('/',''), regex=True)
    tempurl = url.replace('https://synbiohub.org/', instance)
    behindbars.iloc[robustness] = [narcissuscount,tempurl,displayid,"http://identifiers.org/so/SO:"+str(parttype),humanname]
    
    colormap = {
        'http://identifiers.org/so/SO:0000167': 'rgba(4,187,61,1)', 
        'http://identifiers.org/so/SO:0000139':'rgba(149,110,219,1)',
        'http://identifiers.org/so/SO:0000316':'rgba(119,157,205,1)',
        'http://identifiers.org/so/SO:0000141':'rgba(202,58,32,1)',
        
    }
    
    rolethedice = "http://identifiers.org/so/SO:0000167".replace("0000167", parttype)
    try:
        flyingcolours = [colormap[rolethedice]]
    except KeyError:
        flyingcolours = ["rgba(255, 128,0,1)"]
    flyingcolours = flyingcolours*len(behindbars.index)
    
    behindbars['color'] = pd.Series(flyingcolours, index=behindbars.index)
    behindbars.title[behindbars.title.isnull()] = behindbars.displayId[behindbars.title.isnull()]
    
    bar_df = behindbars
    colour = 'color'
    names = 'title'
    freq = 'count'
    urllink = 'deff'
    filename = 'mostusedtype'
    barart(names,freq,colour,bar_df, graphtitle, filename, urllink,displayid)
    bar2= 'static/'+'mostusedtype'+'_'+displayid+'_.html'
    bar2 = retrievehtml(bar2)
    return (bar2)

def retrievehtml(htmllink):
    fl = open(htmllink, "r")
    readhtml = fl.read()
    return (readhtml)



def togglebars(bar1,bar2, displayid, savehtml = True):
    a = bar1
    a = a.replace("</div>\n</body>\n</html>","")
    a = a.replace('<html>\n<head><meta charset="utf-8" /></head>\n<body>\n    <div>\n       ','')
    
    b = bar2
    b = b.replace("</div>\n</body>\n</html>","")
    b = b.replace('<html>\n<head><meta charset="utf-8" /></head>\n<body>\n    <div>\n       ','')
    
    fl = open("toggleswitchhtml.txt", "r")
    display = fl.read()
    display = display.replace('<h2>Frequency</h2>',a) 
    display = display.replace('<h2>By type</h2>',b) 
    
    if savehtml:
        Html_file= open('static/'+'toggle'+'_' + displayid + '.html',"w")
        Html_file.write(display)
        Html_file.close()
    return (display)

def onlycapitalise(string):
    a = [x for x, v in enumerate(string) if v == ' ']
    newstr = ""
    for i in range(0, len(string)):
        if i-1 in a or i == 0:
            newstr = newstr + string[i].capitalize()
        else:
            newstr = newstr + string[i]
    return(newstr)

def findrolename(rolenumber, plural = False):
    import requests
    from bs4 import BeautifulSoup
    
    url = 'http://www.ontobee.org/ontology/SO?iri=http://purl.obolibrary.org/obo/SO_'+rolenumber
    response = requests.get(url)
    # parse html
    page = str(BeautifulSoup(response.content, "lxml"))
    a = page.find('<class rdf:about="http://purl.obolibrary.org/obo/SO_'+rolenumber+'">\n<rdfs:label')
    b = page.find('</rdfs:label',a)
    rolename = page[a+129:b]
    rolename = rolename.replace("_"," ")
    rolename = onlycapitalise(rolename)
    if plural:
        rolename = rolename+"s"
    rolelink = "<a href='https://www.ebi.ac.uk/ols/ontologies/so/terms?obo_id=SO:0000167'>Role</a>"
    rolelink = rolelink.replace("0000167",rolenumber)
    rolelink = rolelink.replace("Role",rolename)
    return(rolelink)






