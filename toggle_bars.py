def toggle_bars(bar1,bar2, save_html = False, filename=None):
    """
    Combines two pieces of html and shows them depending on the toggle state
    
    Requirements
    -------
    Toggle_Switch_html.txt
        
    Parameters
    ----------
    bar1 : string
        An html formatted string for the content shown when the toggle is not selected (the default setting).
        The html must include '</div>\n</body>\n</html>' and 
        '<html>\n<head><meta charset="utf-8" /></head>\n<body>\n    <div>\n       '.
    bar2: string
        An html formatted string for the content shown when the toggle is selected (not the default setting).
        The html must include '</div>\n</body>\n</html>' and 
        '<html>\n<head><meta charset="utf-8" /></head>\n<body>\n    <div>\n       '.
    save_html: boolean, default:False
        if True then the html toggle document will be saved, if false then no document with the html string will be saved
    filename : string, default: None
        File location where the html document containing the toggled is saved (e.g. 'current_working_directory//toggle_name.html')
        This is only used if save_html is True. Example of possible filename: 'current_working_directory\\toggle_display.html'
    
    Returns
    -------
    display: string
        An html string which contains a toggle element and two pieces of html to vary between
   
    Example
    --------
    import os
    
    #current working directory
    cwd = os.getcwd()

    #create input data
    self_df, display_id, title, role, count = input_data(uri, instance)

    #create and format data for the most_used barchart
    bar_df = most_used_bar(uri, instance, display_id, title, role, 
                    count)

    #where to save the file
    filename1= os.path.join(cwd, f'bar1_{display_id}.html')

    #create the most used barchart
    bar_plot('title','count','color',bar_df, 'Top Ten Parts by Number of Uses', filename1, 'deff')

    #retrieve html
    most_used = retrieve_html(filename1)

    bar_df = most_used_by_type_bar(uri,instance, display_id, title, 
                  role, count)

    #where to save the file
    filename2= os.path.join(cwd, f'bar2_{display_id}.html')

    #create the most used barchart
    bar_plot('title','count','color',bar_df, 'Top Ten by Number of Uses', filename2, 'deff')

    #retrieve html
    by_role = retrieve_html(filename2)

    #create bar toggle html
    toggle_display = toggle_bars(most_used,by_role)
    """
    
    htmls = [bar1, bar2]
    
    for index, bar_html in enumerate(htmls):
        #remove header and footer of the html
        bar_html = bar_html.replace('</div>\n</body>\n</html>','')
        bar_html = bar_html.replace('<html>\n<head><meta charset="utf-8" /></head>\n<body>\n    <div>\n       ','')
        htmls[index] = bar_html
    
    #read in toggle html text
    fl = open("Toggle_Switch_html.txt", "r")
    display = fl.read()
    
    #put in the two bargraphs
    display = display.replace('<h2>Frequency</h2>',htmls[0]) 
    display = display.replace('<h2>By type</h2>',htmls[1]) 
    
    #saves html toggle file
    if save_html:
        Html_file= open(filename,"w")
        Html_file.write(display)
        Html_file.close()
        
    return (display)
