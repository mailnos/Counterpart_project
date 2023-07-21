"""
title: counterpart case study
author: liam watson
date: 07/16/2023
version: 1
"""

from operator import concat
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import math
import openpyxl
import os


def main():
    print("printing from main "+str(rater({'Asset Size': 1200000, 'Limit': 5000000, 'Retention': 1000000,'Industry': 'Hazard Group 2'})))

def interpolate(xval, df, xcol, ycol):
# compute linear interp of x val in df - df is expected to be sorted
    return np.interp([xval], df[xcol], df[ycol])[0]

def data_load():
    asset_size = [ 1, 1000000, 2500000, 5000000, 10000000, 15000000, 20000000, 25000000, 50000000, 75000000, 100000000, 250000000]
    
    base_rate = [ 1065, 1819, 3966, 3619, 4291, 4905, 5120, 5499, 6279, 6966, 7156, 8380]

    limit = [ 0, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000, 35000, 50000, 75000, 100000, 125000,
    150000, 175000, 200000, 225000, 250000, 275000, 300000, 325000, 350000, 375000, 400000, 425000, 450000,
    475000, 500000, 525000, 550000, 575000, 600000, 625000, 650000, 675000, 700000, 725000, 750000, 775000,
    800000, 825000, 850000, 875000, 900000, 925000, 950000, 975000, 1000000, 2000000, 2500000, 3000000, 4000000, 5000000 ]

    factor = [ -0.76, -0.6, -0.51, -0.406, -0.303, -0.231, -0.128, -0.064, 0, 0.105, 0.175, 0.277, 0.35, 0.406,
    0.452, 0.491, 0.525, 0.555, 0.581, 0.605, 0.627, 0.648, 0.666, 0.684, 0.7, 0.715, 0.73, 0.743, 0.756, 0.807,
    0.819, 0.831, 0.842, 0.853, 0.864, 0.874, 0.883, 0.893, 0.902, 0.91, 0.919, 0.927, 0.935, 0.943, 0.95, 0.957,
    0.964, 0.971, 1, 1.415,  1.526, 1.637, 1.82, 1.986]

    asset_size_df = pd.DataFrame(asset_size, columns=['asset_size'])
    asset_size_df['base_rate'] = base_rate
    limit_df = pd.DataFrame(limit, columns=['limit'])
    limit_df['factor'] = factor
        
    industry_dict = {"Hazard Group 1": 1, "Hazard Group 2": 1.25, "Hazard Group 3": 1.5}

    return asset_size_df, limit_df, industry_dict




def rater(json_input):

    #data_load()

    # test if data load is successful, prompt used to have excel file in the same directory if not
    try:
        data_orig = pd.read_excel(r"Case_Study_Data.xlsx", "Rating Tables" )
        
        #split out asset size, limit and industry data into df
        asset_size_df = data_orig.iloc[6:18,2:4]
        asset_size_df.columns = ["asset_size","base_rate"]
        asset_size_df = asset_size_df.astype(float)

        limit_df = data_orig.iloc[20:74,2:4]
        limit_df.columns = ["limit","factor"]
        limit_df = limit_df.astype(float)
        
        industry_df = data_orig.iloc[77:80,2:4]
        industry_df.columns = ["hazard_group","factor"]
        industry_dict = industry_df.set_index("hazard_group")["factor"].to_dict()
    
    except:
        asset_size_df, limit_df, industry_dict = data_load()
        print("There was a data load exception, please check that rating table is in the working directory")
            
    #error handling    
    if  json_input["Asset Size"] < 1:
        return "Please Enter Asset Size > $1"
    elif json_input["Asset Size"] >  250000000:
        return "Please reach out to actuary for large account pricing"

    if  json_input["Limit"] < 1:
        return "Please Enter Limit > $1"
    elif json_input["Limit"] >  5000000:
        return "Please reach out to actuary for large account pricing"

    if  json_input["Retention"] < 0:
        return  "Please Enter Limit > $1"
    elif json_input["Retention"] >  5000000:
        return  "Please reach out to actuary for high excess account pricing"

    #straight line interpolate values if they are in the 
    rate_f = interpolate(json_input["Asset Size"],asset_size_df, "asset_size", "base_rate" )
    limit_f = interpolate(json_input["Limit"],limit_df, "limit", "factor" )
    retention_f = interpolate(json_input["Retention"],limit_df, "limit", "factor" )
    industry_f = industry_dict[json_input["Industry"]]

    #print(rate_f, limit_f, retention_f, industry_f)

    result = round(rate_f * (limit_f - retention_f) * industry_f * 1.7,0)

    return result

if __name__=="__main__":
    main()
  


 