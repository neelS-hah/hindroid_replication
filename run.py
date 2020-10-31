import os
import re
import numpy as np
import pandas as pd
import sys 
'''
Potential Improvements 
1. We tried a more optimized version of the code, it had a couple errors, but we'll try and add it without the errors 
2. Return the DataFrame with counts, instead of just the list 

Note - currently the benign version takes some time to run 

We added the data-params.json in the config file,
'''

def process_data(data):
    #for i in os.listdir('/teams/DSC180A_FA20_A00/a04malware'):
    #    print(i)

    #the elements we are looking for
    test_apis_m = []
    test_packages_m = []
    test_invokes_m = []
    test_blocks_m = []
    test_app_m = []
    test_type_m = []


    for root, dirs, files in os.walk("/teams/DSC180A_FA20_A00/a04malware/test-apps/malware", topdown=True):
        for i in files:
            path = os.path.join(root,i)
            if i.endswith(".smali"):
                with open(path,'r') as fp:
                    smali_f = fp.read()
                    blocks = re.findall(r'\.method(.*[\s\S\n]+.*)\.end\smethod',smali_f)
                    for j in blocks:
                        api_calls = re.findall(r'invoke-.*\{.*\}\,.+\n', j)
                        for k in api_calls:
                            test_apis_m.append(re.findall(r'invoke-.*\{.*\}\, (.+\n)',j)[0])
                            test_packages_m.append(re.findall(r'(L.+?);',j)[0])
                            test_invokes_m.append(re.findall(r'invoke-.*\{.*\}',j)[0])
                            test_blocks_m.append(blocks)
                            test_app_m.append(path.split('/')[6])
                            test_type_m.append(path.split('/')[5])


    print(len(test_apis_m),
    len(test_packages_m),
    len(test_invokes_m),
    len(test_blocks_m),
    len(test_app_m),
    len(test_type_m))



    malware_df = pd.DataFrame(data={'Test_Apis':test_apis_m,'Test_Package':test_packages_m,'Test_Invoke':test_invokes_m,'Test_Block':test_blocks_m,'Test_App':test_app_m,'Test Type':test_type_m})
    print(malware_df.head(2))




    #the elements we are looking for
    test_apis_b = []
    test_packages_b = []
    test_invokes_b = []
    test_blocks_b = []
    test_app_b = []
    test_type_b = []


    for root, dirs, files in os.walk("/teams/DSC180A_FA20_A00/a04malware/test-apps/benign", topdown=True):
        for i in files:
            path = os.path.join(root,i)
            if i.endswith(".smali"):
                with open(path,'r') as fp:
                    smali_f = fp.read()
                    blocks = re.findall(r'\.method(.*[\s\S\n]+.*)\.end\smethod',smali_f)
                    #regex for method start and end statements
                    for j in blocks:
                        api_calls = re.findall(r'invoke-.*\{.*\}\,.+\n', j)
                        for k in api_calls:
                            test_apis_b.append(re.findall(r'invoke-.*\{.*\}\, (.+\n)',j)[0])
                            test_packages_b.append(re.findall(r'(L.+?);',j)[0])
                            test_invokes_b.append(re.findall(r'invoke-.*\{.*\}',j)[0])
                            test_blocks_b.append(blocks)
                            test_app_b.append(path.split('/')[6])
                            test_type_b.append(path.split('/')[5])

    #create dataframe
    df = pd.DataFrame(data={'Test_Apis':test_apis_b,'Test_Package':test_packages_b,'Test_Invoke':test_invokes_b,'Test_Block':test_blocks_b,'Test_App':test_app_b,'Test Type':test_type_b})

    print(len(test_apis_b),
    len(test_packages_b), 
    len(test_invokes_b),
    len(test_blocks_b),
    len(test_app_b),
    len(test_type_b))

    benign_df = pd.DataFrame(data={'Test_Apis':test_apis_b,'Test_Package':test_packages_b,'Test_Invoke':test_invokes_b,'Test_Block':test_blocks_b,'Test_App':test_app_b,'Test Type':test_type_b})
    print(benign_df.head(2))

def main():
    data = False 
    print("Adding benign and malware API call information to dataframe")
    if len(sys.argv) > 1:
        data = sys.argv[1]
        process_data(data)
    process_data(data)


if __name__ == "__main__":
    main()
