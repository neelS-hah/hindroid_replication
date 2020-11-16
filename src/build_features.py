import pandas as pd 
import os,glob
import re
from pathlib import Path
import pandas as pd
import numpy as np
from collections import defaultdict

#constants

def get_smali_files(smali_list, fp):
    #iterate through dir 
    for subdir, dirs, files in os.walk(fp):
        for filename in files:
            filepath = subdir + os.sep + filename
            #find smali files
            if filepath.endswith(".smali"):
                smali_list.append(filepath)
    print("Fetched .smali files")


def helper(app_type, app_name, elem, num_blocks, def_dict, invoke_type):
    tracking_number = 'method' + str(num_blocks)
    final = re.sub(re.compile('^[^}]*}'), '', str(elem))
    api_call = final[2:]
    apiNoParam = re.match(re.compile('[^(]*') , api_call)
    api_call = apiNoParam.group(0) + str('()')
    package = re.search(re.compile('^(.*?)->'), api_call)
    def_dict[app_type][app_name]['Packages'][package.group(1)].append(api_call)
    def_dict[app_type][app_name]['combined']['APIs'].append(api_call)
    def_dict[app_type][app_name]['invoke_type'][invoke_type].append(api_call)
    def_dict[app_type][app_name]['blocks'][tracking_number].append(api_call)

def create_struct(fp):
    #constants
    flag = False
    num_blocks = 0
    tracking_number = 'method' + str(num_blocks)
    def_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
    inside_block = False
    block_list = []
    smali_list = []
    get_smali_files(smali_list, fp)

    api_list = ['invoke-static', 'invoke-virtual', 'invoke-direct', 'invoke-super', 'invoke-interface']

    api_list = ['invoke-static', 'invoke-virtual', 'invoke-direct', 'invoke-super', 'invoke-interface']
    for i in smali_list:
        f = open(i, "r")
        app_type = i.split('/')[5]
        app_name = i.split('/')[6]
        code = f.readlines()
        for index, elem in enumerate(code):
            if '.method' in elem:
                flag = True
        
            if inside_block and ('.end method' in elem):
                #Assign default values
                block_list = []
                flag = False
                num_blocks += 1  

            if flag and (api_list[0] in elem): 
                helper(app_type, app_name, elem, num_blocks, def_dict, api_list[0])
            if flag and (api_list[1] in elem):
                helper(app_type, app_name, elem, num_blocks, def_dict, api_list[1])
            if flag and (api_list[2] in elem): 
                helper(app_type, app_name, elem, num_blocks, def_dict, api_list[2])
            if flag and (api_list[3] in elem): 
                helper(app_type, app_name, elem, num_blocks, def_dict, api_list[3])
            if flag and (api_list[4] in elem):
                helper(app_type, app_name, elem, num_blocks, def_dict, api_list[4])

    #return (pd.Series(def_dict).head())
    return def_dict 

if __name__ == '__main__':
    API_create_struct()
    

