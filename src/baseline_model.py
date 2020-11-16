import pandas as pd
import os,glob
import re
from pathlib import Path
import pandas as pd 
import numpy as np
from collections import defaultdict 
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

def create_features(def_dict):
    col1 = []
    col2 = []
    col3 = []
    col4 = []
    col5 = []
    col6 = []
    col7 = []
    col8 = []
    for elem1 in list(def_dict.keys()):
        for elem2 in list(def_dict[elem1].keys()):
            col1.append(elem1)
            col2.append(elem2)
            col3.append(len(def_dict[elem1][elem2]['combined']['APIs']))
            col4.append(len(def_dict[elem1][elem2]['invoke_type']['invoke-static']))
            col5.append(len(def_dict[elem1][elem2]['invoke_type']['invoke-virtual']))
            col6.append(len(def_dict[elem1][elem2]['invoke_type']['invoke-direct']))
            col7.append(len(def_dict[elem1][elem2]['invoke_type']['invoke-super']))
            col8.append(len(def_dict[elem1][elem2]['invoke_type']['invoke-interface']))
    df = pd.DataFrame([col1, col2, col3, col4, col5, col6, col7, col8]).T
    df['App Category'] = df[0]
    df['All API'] = df[2]
    df['invoke-static'] = df[3]
    df['invoke-virtual'] = df[4]
    df['invoke-direct'] = df[5]
    df['invoke-super'] = df[6]
    df['invoke-interface'] = df[7]
    df = df.drop([0,2,3,4,5,6,7],1)
    return df

def run_model(data_dict):
    #Split Data
    df = create_features(data_dict)
    y = df['App Category'].astype('category').cat.codes
    X = df.drop(['App Category',1],1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.7, random_state=42)

    #run GB classifier for baseline
    df = df[['App Category','All API','invoke-static','invoke-virtual','invoke-direct','invoke-super', 'invoke-interface']]
    grandientboosting = GradientBoostingClassifier()
    grandientboosting.fit(X_train,y_train)
    grandientboosting.predict(X_test)
    print("Model Accuracy - ")
    return grandientboosting.score(X_test, y_test)


