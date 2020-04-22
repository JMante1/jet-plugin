def sankey(url, title, instance):
    import requests
    import json
    import pandas as pd
    from pandas.io.json import json_normalize
    
    #to create the sankey diagram two linked tables are needed
    #1) about nodes: indexes, names and colours
    #2) about the links: from node a (index), to node b (index), width, colour
    
    #the creation of this table for the particular part referenced by the url is given her
    
     
    #read in the sparql query to perform
    fl = open("Preceding_Percent_Query.txt", "r")
    sparqlquery = fl.read()
    
    #substitute in the name of the particular part
    sparqlquery = sparqlquery.replace('https://synbiohub.org/public/igem/BBa_E0040/1',url)
    r = requests.post(instance+"sparql", data = {"query":sparqlquery}, headers = {"Accept":"application/json"})
    
    #reformat query results
    d = json.loads(r.text)
    order_df = json_normalize(d['results']['bindings'])
    
    #rename columns from ['average_preceeding.datatype', 'average_preceeding.type',
    #       'average_preceeding.value', 'count.datatype', 'count.type',
    #       'count.value', 'def2.type', 'def2.value', 'displayId.type',
    #       'displayId.value', 'role.type', 'role.value', 'title.type',
    #      'title.value']
    order_df.columns = ['ad', 'at','centfol', 'cd', 'ct', 'count', 'dt','deff', 'dt1', 'displayId','rt', 'roletog', 'tt','title']
    
    #drop unneeded columns
    order_df = order_df.drop(['ad', 'at', 'cd', 'ct', 'dt', 'dt1', 'rt', 'tt'], axis=1)
    
    """
    #columns left are:
    #'centfol' - percentage of the instance of co-occurance where 
    #this part follows the part of interest (0 means all instances 
    #have the poi following this part)
    #'count' - total number of part co-occurances
    #'deff'- uri of the part
    #'displayId' - display id of the part
    #'roletog' - role of the part (e.g. http://identifiers.org/so/SO:0000141)
    #'title' - human name of the part
    """
    #change number columns from strings to number type
    order_df['count'] = order_df['count'].apply(pd.to_numeric)
    order_df['centfol'] = order_df['centfol'].apply(pd.to_numeric)
    
    #makes sure uris point to the correct instance (even for dev.synbiohub.org)
    order_df['deff'] = order_df.deff.replace('synbiohub.org', instance.replace('https://', '').replace('/',''), regex=True)
    
    #parts which have no title have the title field filled in using the displayId field
    order_df.title[order_df.title.isnull()] = order_df.displayId[order_df.title.isnull()]
    
    #Break the dataframe down into dataframes for:
    #promoters, rbs, cds, terminators, and other parts
    
    #df with just promoters
    prom = order_df.loc[order_df['roletog'] == 'http://identifiers.org/so/SO:0000167']
    
    #df with just rbs
    rbs = order_df.loc[order_df['roletog'] == 'http://identifiers.org/so/SO:0000139']
    
    #df with just cds
    cds = order_df.loc[order_df['roletog'] == 'http://identifiers.org/so/SO:0000316']
    
    #df with just terminators
    term = order_df.loc[order_df['roletog'] == 'http://identifiers.org/so/SO:0000141']
    
    #remove all parts that were in any of the other part type data frames
    other = order_df[order_df['roletog'] != 'http://identifiers.org/so/SO:0000167']
    other = other[other['roletog'] != 'http://identifiers.org/so/SO:0000139']
    other = other[other['roletog'] != 'http://identifiers.org/so/SO:0000316']
    other = other[other['roletog'] != 'http://identifiers.org/so/SO:0000141']
    
    #create a list containing the previous data frames
    part_array = [prom, rbs, cds, term, other]
    
    #array of the lengths of the above
    part_array_lengths = [len(prom), len(rbs), len(cds), len(term), len(other)]
    
    #set up colours for links and nodes
    #slightly transparent ones(green, purple, blue, red, orange)
    link_colours = ["rgba(4,187,61,0.5)", "rgba(149,110,219,0.5)", "rgba(119,157,205,0.5)", "rgba(202,58,32,0.5)", "rgba(255, 128,0,0.5)"]
    
    #fully coloured ones(green, purple, blue, red, orange)
    node_colours = ["#04BB3D", "#956EDB", "#779DCC", "#CA3A20", "#FF8000"]
    
    #colour of the node for the part itself (black)
    part_colour = "#000000"
                   
    #initialise lists
    source = []
    list_target = []
    value = []
    percent = []
    multiplier = []
    list_link_colour = []
    len_part_type = []
    len_part_type = []
    target = 5 #target starts at 5 as the node with index 5 is the first promoter
    # (after preceeding __ nodes for each type)
    
    #list of node colours starts with the five colours as the first 
    #five nodes are the outflow ones for preceeding in each category 
    list_node_colour =  node_colours
    
    #first five node names
    node_label = ["Preceeding Promoters", "Preceeding RBS", "Preceeding CDS", "Preceeding Terminator", "Preceeding Other"]
    
    #the first five nodes don't have a url link
    node_url = ["NA", "NA","NA","NA", "NA"]
    
    
    """part type to preceding parts"""
    for part_type_index in range(0,5):
        #make sure no length used is greater than 10
        len_part_type += [min(part_array_lengths[part_type_index], 10)]
        
        #iterate over the parts upto ten in the array prom, rbs, cds, term, other
        for index in range(0,len_part_type[part_type_index]):
            #add a link colour for the link from preceeding label to node in this list
            list_link_colour.append(link_colours[part_type_index])
            
            #add a node colour for the node of this list
            list_node_colour.append(node_colours[part_type_index])
            
            #add the label to the list of node labels (e.g. p(tetR))
            node_label.append(part_array[part_type_index]['title'].iloc[index])
            
            #add the uri to the list of node uris
            node_url.append(part_array[part_type_index]['deff'].iloc[index])
            
            #add the percentage following to the list of percentages
            percent.append(part_array[part_type_index]['centfol'].iloc[index])
            
            #add the count of co-occurances to the list of counts
            multiplier.append(part_array[part_type_index]['count'].iloc[index])
    
            
            #add the counts*(1-percent) to the list of link widths
            value.append((part_array[part_type_index]['count'].iloc[index])*(1-part_array[part_type_index]['centfol'].iloc[index]))
            
            #the links all start from index associated with the preceeding number
            source.append(part_type_index)
            
            #add target to list of targets
            list_target.append(target)
            
            #increment target by one
            target += 1
            
    
    
    """Preceding parts to POI"""
    #tells the number of links made so far
    #how many promoters, rbs, cds, terminators, and other parts preceed the poi
    num_colocated_parts = len(list_link_colour)
    
    #as the links to and from preceeding parts
    #all must have the same colour in the same order
    #just double the list of the link colours
    list_link_colour += list_link_colour
    
    #for the same reason add the values currently in values to the end
    #of the values link again (links are the same width)
    value += value
    
    #the targets from preceeding must become the source going to the poi
    #so add the targets to the end of the source list
    source += list_target
    
    #the target for each of them is the poi so add that
    list_target += [target]*num_colocated_parts
    
    """Add POI node"""
    #add the name
    node_label.append(title)
    
    #add the uri/url link
    node_url.append(url)
    
    #add the colour of the part node
    list_node_colour.append(part_colour)
    
    """POI to following"""
    #source will be from poi (and the source is used as many times as there were parts
    #found colocated with the poi, upto 50)
    source += [target]*num_colocated_parts
    
    #target list will be the same length as the original number of nodes added
    #and continous from there
    list_target += list(range(target+1, target+num_colocated_parts+1))
    
    #add link colours (same as for preceeding inbound links)
    list_link_colour += list_link_colour[:num_colocated_parts]
    
    #add link width based on count and the percentage not preceeding
    value += [(p)*m for p,m in zip(percent,multiplier)]
    
    
    #add node labels same as the preceeding ones
    node_label += node_label[5:-1]
    
    #add node colours (same as for preceeding colocated parts)
    list_node_colour += list_node_colour[5:-1]
    
    #add node uris (same as for preceeding colocated parts)
    node_url += node_url[5:-1]
    
    """Following to Following labels"""
    """link colour, link width, source, target, node labels, node colours, node uris"""
    #source will be from colocated parts to following parts groups
    #(e.g. following terminators)
    source += list(range(target+1, target+num_colocated_parts+1))
    
    #target list will be based on the original groups of the preceeding parts
    #but shifted to take into account the current point in the list
    list_target += [x +target+num_colocated_parts+1 for x in source[:num_colocated_parts]]
    
    #add link colours (same as for preceeding inbound links)
    list_link_colour += list_link_colour[:num_colocated_parts]
    
    #add link width based on count and the percentage not preceeding
    value += [(p)*m for p,m in zip(percent,multiplier)]
    
    #add node labels for following groups
    node_label += ["Following Promoters", "Following RBS", "Following CDS", "Following Terminator", "Following Other"]
    
    #final node colours are based on the groups
    list_node_colour += ["#04BB3D", "#956EDB", "#779DCC", "#CA3A20", "#FF8000"]
    
    #final group nodes have no uri/urls
    node_url += ["NA", "NA","NA","NA", "NA"]
    
    
    """Make DataFrame"""
    skey =  pd.DataFrame(data =[source, list_target, value, list_node_colour,
                                node_label, node_url, list_link_colour],
                        index =["Source", "Target", "Value","Color","Node, Label",
                                "Link","Link Color"])
    
    #transpose so columns are source, target, etc
    skey = skey.T
    return(skey)
