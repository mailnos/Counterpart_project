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

def rater(json_input):

    #data_load()
    try:
        data_orig = pd.read_excel(r"Case_Study_Data.xlsx", "Rating Tables" )
    except:
        return "Please make sure the Excel Data File is in the working direcoty"

    #split out asset size data into df
    asset_size_df = data_orig.iloc[6:18,2:4]
    asset_size_df.columns = ["asset_size","base_rate"]
    asset_size_df = asset_size_df.astype(float)

    limit_df = data_orig.iloc[20:74,2:4]
    limit_df.columns = ["limit","factor"]
    limit_df = limit_df.astype(float)
    
    industry_df = data_orig.iloc[77:80,2:4]
    industry_df.columns = ["hazard_group","factor"]
    industry_dict = industry_df.set_index("hazard_group")["factor"].to_dict()



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

    rate_f = interpolate(json_input["Asset Size"],asset_size_df, "asset_size", "base_rate" )
    limit_f = interpolate(json_input["Limit"],limit_df, "limit", "factor" )
    retention_f = interpolate(json_input["Retention"],limit_df, "limit", "factor" )
    industry_f = industry_dict[json_input["Industry"]]

    #print(rate_f, limit_f, retention_f, industry_f)

    result = round(rate_f * (limit_f - retention_f) * industry_f * 1.7,0)

    return result

if __name__=="__main__":
    main()
  


 