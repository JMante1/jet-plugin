import pandas as pd

def uri_to_url(data, instance, spoofed_instance):
    """
    Change the instance that is being refered to in the data to the instance given by instance if the current instance 
    they are referencing is the spoofed_instance
    
    Requirements
    -------
    import pandas as pd
    
    Parameters
    ----------
    data : pandas series OR string
        The input with urls that must be changed. The cells/string should containg string(s) of the format:
        'https://something_to_be_replaced/something_to_keep'
    instance : string
        the synbiohub instance where information is to be retrieved from
        e.g. 'https://synbiohub.org/' (note it must have the https:// and the / at the start/end)
    spoofed_instance : string
        the synbiohub instance that it is pretending to be
        e.g. 'https://dev.synbiohub.org/' pretends to be 'https://synbiohub.org/'
        
    Returns
    -------
    data: pandas series OR string
        The df column/string with uris converted to urls of the format: 'instance something_to_keep',
        e.g. 'https://synbiohub.org/someting_to_keep'
   
    Example
    --------
    import pandas as pd
    
    lst = ['https://shouldnt_change.org/public/igem/BBa_E1010/1', 'https://synbiohub.org/public/igem/BBa_C0051/1',
       'https://synbiohub.org/public/igem/BBa_C0040/1']
    series = pd.Series(lst)
    
    new_series = uri_to_url(series, 'https://dev.synbiohub.org/', 'https://synbiohub.org/')
    
    Output:
    0    https://shouldnt_change.org/public/igem/BBa_E1010/1
    1    https://dev.synbiohub.org/public/igem/BBa_C0051/1
    2    https://dev.synbiohub.org/public/igem/BBa_C0040/1
    """

    #finds the data type of the input data
    data_type = type(data)

    #case that it is a column of a pandas dataframe (i.e. it is a Pandas Series)
    if data_type == pd.core.series.Series:
        for idx, deff in data.items():
          uri_instance = deff[:deff.find('/', 8)+1]
          if uri_instance == spoofed_instance:
            data[idx] = deff.replace(uri_instance, instance) 

    #case that it is a simple string
    elif data_type == str:
        uri_instance = deff[:deff.find('/', 8)+1]
        if uri_instance == spoofed_instance:
            data = data.replace(data[:data.find('/', 8)+1], instance) 
      
  return(data)
