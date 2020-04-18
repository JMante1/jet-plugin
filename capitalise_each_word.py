def capitalise_each_word(string):
    #a is a list of the indexes of spaces in the string
    a = [index for index, character in enumerate(string) if character == ' ']
    
    #initiate an empty string
    newstr = ""
    
    #for first letter or letters after spaces capitalise the letter
    for i in range(0, len(string)):
        if i-1 in a or i == 0:
            newstr = newstr + string[i].capitalize()
        else:
            newstr = newstr + string[i]
            
    return(newstr)
