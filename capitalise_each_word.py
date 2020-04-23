def capitalise_each_word(str):
    """
    Capitalises each character after a space, and the first character, of a string
    
    Requirements
    -------
    None
    
    Parameters
    ----------
    str : string
        the string to be capitalised
    Returns
    -------
    newstr: string
        The newly capitalised string
        
    Example
    --------
    intro_str = 'hello world. how are you today?'
    new_intro = capitalise_each_word(intro_str)
    
    Output: 'Hello World. How Are You Today?'
    """
    #a is a list of the indexes of spaces in the string
    a = [index for index, character in enumerate(str) if character == ' ']
    
    #initiate an empty string
    newstr = ""
    
    #for first letter or letters after spaces capitalise the letter
    for i in range(0, len(str)):
        if i-1 in a or i == 0:
            newstr = newstr + str[i].capitalize()
        else:
            newstr = newstr + str[i]
            
    return(newstr)
