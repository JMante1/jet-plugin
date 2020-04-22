def toggle_bars(bar1,bar2, display_id, save_html = False, filename=None):
    #e.g. filename = f'{cwd}\\toggle_display.html'
    
    htmls = [bar1, bar2]
    
    for index, bar_html in enumerate(htmls):
        #remove header and footer of the html
        bar_html = bar_html.replace("</div>\n</body>\n</html>","")
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
