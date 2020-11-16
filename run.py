import sys
import os
import json

sys.path.insert(0, 'src')

from build_features import create_struct
from eda import run_model

def main(targets):
    '''
    Runs the main project pipeline logic, given the targets.
    targets must contain: 'data', 'analysis', 'model'. 
    
    `main` runs the targets in order of data=>analysis=>model.
    '''


    if 'data' in targets:
        with open('config/data-params.json') as fh:
            data_cfg = json.load(fh)
        data_dict = create_struct(data_cfg['PATH'])
    
    if 'eda' in targets:
        with open('config/model-params.json') as fh:
            model_cfg = json.load(fh)
            print("fetched data, building model features and running baseline...")
            print(run_model(data_dict))


if __name__ == '__main__':
    # run via:
    # python main.py data features model
    targets = sys.argv[1:]
    main(targets)

