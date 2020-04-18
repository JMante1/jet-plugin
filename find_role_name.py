def find_role_name(rolenumber, plural = False):  
    import requests
    from bs4 import BeautifulSoup
    from capitalise_each_word import capitalise_each_word
    
    #url to get the part name
    url = 'http://www.ontobee.org/ontology/SO?iri=http://purl.obolibrary.org/obo/SO_'+role_number
    
    #get the part type ontology page information
    response = requests.get(url)
    
    # parse html
    
    page = str(BeautifulSoup(response.content, "lxml"))
    
    #find the location of the start of the particular page
    a = page.find('<class rdf:about="http://purl.obolibrary.org/obo/SO_'+role_number+'">\n<rdfs:label')
    
    #find closure of the bracket of information
    b = page.find('</rdfs:label',a)
    
    #pull out the information
    role_name = page[a+129:b]
    
    #if there are spaces in the name they are now put in (represented in the ontology using '_')
    role_name = role_name.replace("_"," ")
    
    
    role_name = capitalise_each_word(role_name)
    
    #if flag plural add an s to the end of the role name
    if plural:
        role_name = role_name+"s"
        
    #format required to make a hyperlink to the ontology page in html   
    role_link = "<a href='https://www.ebi.ac.uk/ols/ontologies/so/terms?obo_id=SO:0000167'>Role</a>"
    
    #substitute in the correct name and number for the particular part
    role_link = role_link.replace("0000167",role_number)
    role_link = role_link.replace("Role",role_name)
    
    return(role_link)
