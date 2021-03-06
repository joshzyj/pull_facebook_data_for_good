#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 20:48:26 2020

@author: hamishgibbs
"""

import sys
from utils import download_data, move_most_recent_files, get_update_date, remove_empty_files
from mobility import get_file_dates, get_urls
from itertools import compress

def pull_mobility(outdir, keys, country, dl_variables, update, movement_type):
    '''
    
    Parameters
    ----------
    outdir : str
        Output directory.
    keys : list
        user credentials [username, password].
    country : str
        Country name - must match .config file exactly (names with spaces must replace ' ' with '_').
    dl_variables : dict
        download specific variables in a dict, 'id' = dataset id, 'origin' = dataset origin datetime.datetime object.
    update : boolean
        Whether an existing dataset is being updated.

    Returns
    -------
    None.

    '''
            
    country_output = outdir + "/" + country + '_' + movement_type
        
    base_url = 'https://www.facebook.com/geoinsights-portal/downloads/vector/?id=' + str(dl_variables['id']) + '&ds='

    earliest_date = dl_variables['origin']    
    
    data_dates = get_file_dates(earliest_date)
            
    if update:
        data_dates = list(compress(data_dates, [x > get_update_date(country_output) for x in data_dates]))
    
    if len(data_dates) == 0:
        sys.exit('No datasets to download. Exiting.')
        
    urls = get_urls(base_url, data_dates)
    
    start_time = download_data(urls, keys)

    move_most_recent_files(country_output, urls, start_time)
    
    remove_empty_files(country_output)
    
    print('Success.')
