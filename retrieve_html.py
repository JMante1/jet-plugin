def retrieve_html(htmllink):
    #open the htmllink file
    fl = open(htmllink, "r")
    
    #read in the html
    readhtml = fl.read()
    
    return (readhtml)
