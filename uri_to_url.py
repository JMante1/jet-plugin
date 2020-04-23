import pandas as pd

def uri_to_url(data, instance):
    """
    Converts uris to urls (written to circumvent spoofing). Can cause issues if distributed search was used.
    
    Requirements
    -------
    import pandas as pd
    
    Parameters
    ----------
    data : pandas series OR string
        The input with urls that must be changed. The cells/string should containg string(s) of the format:
        'https://something_to_be_replaced/something_to_keep'
    instance : string
        the synbiohub instance where information is to be retrieved from (where the sparql query is to be run)
        e.g. 'https://synbiohub.org/' (note it must have the https:// and the / at the start/end)
        
    Returns
    -------
    data: pandas series OR string
        The df column/string with uris converted to urls of the format: 'instance something_to_keep',
        e.g. 'https://synbiohub.org/someting_to_keep'
   
    Example
    --------
    import pandas as pd
    
    lst = ['https://notice_the_caveat.org/public/igem/BBa_E1010/1', 'https://synbiohub.org/public/igem/BBa_C0051/1',
       'https://synbiohub.org/public/igem/BBa_C0040/1']
    series = pd.Series(lst)
    
    new_series = uri_to_url(series, 'https://dev.synbiohub.org/')
    
    Output:
    0     https://dev.synbiohub.org/public/igem/BBa_E1010/1
    1     https://dev.synbiohub.org/public/igem/BBa_C0051/1
    2     https://dev.synbiohub.org/public/igem/BBa_C0040/1
    """

    #finds the data type of the input data
    data_type = type(data)

    #case that it is a column of a pandas dataframe (i.e. it is a Pandas Series)
    if data_type == pd.core.series.Series:
        for idx, deff in data.items():
          # for every cell replace 'https://^/*' so that it becomes 'instance*'
          data[idx] = deff.replace(deff[:deff.find('/', 8)+1], instance) 

    #case that it is a simple string
    elif data_type == str:
        #replace 'https://^/*' so that it becomes 'instance*'
        data = data.replace(data[:data.find('/', 8)+1], instance) 
      
  return(data)
