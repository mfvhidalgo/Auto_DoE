#%%

#python -m src.Common_DoEs.py

import pandas as pd
import numpy as np
import dexpy
import dexpy.factorial
import dexpy.ccd
import itertools
from typing import Dict
import doepy.build
import os
import sys
import copy

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
if parent_directory not in sys.path:
    sys.path.append(parent_directory)

if current_directory not in sys.path:
    sys.path.append(current_directory)

import functions.math_utils as math_utils

os.chdir(current_directory)

#%% import features

features = {'cont':pd.read_excel('Features.xlsx',sheet_name='Continuous').set_index('Feature'),
            'cat':pd.read_excel('Features.xlsx',sheet_name='Categorical').set_index('Feature')}

feature_names = {'cont':list(features['cont'].index),
                 'cat':list(features['cat'].index)
                 }

feature_levels = {'cont':{},
                  'cat':{}
                  }

for feature_cont in feature_names['cont']:
    feature_levels['cont'][feature_cont] = list(features['cont'].loc[feature_cont])
    
for feature_cat in feature_names['cat']:
    feature_levels['cat'][feature_cat] = list(features['cat'].loc[feature_cat].dropna())

designs = {}

has_cont = True if len(features['cont']) > 0 else False
has_cat = True if len(features['cat']) > 0 else False

rescalers = {}
for feature in feature_names['cont']:
    rescalers[feature] = math_utils.rescale.rescale(feature_levels['cont'][feature][0],
                                                    feature_levels['cont'][feature][1],
                                                    -1,1)

#%% functions

def add_categorical(feature_cat_levels: Dict,
                    input_df: pd.DataFrame = pd.DataFrame()
                    ) -> pd.DataFrame:
    """ 
    Takes in the DoE design and duplicates it for each combination of categorical terms

    Args:
        feature_cat_levels (Dict): dict where keys are the feature names and the values are their respective levels
        input_df (pd.DataFrame, optional): DoE design of the continous features.
                                           Defaults to pd.DataFrame().

    Returns:
        pd.DataFrame: Complete df of continous and categorical terms.
                      If input_df is empty, return all permutations of categorical features
    """

    df = pd.DataFrame()
    if len(input_df) == 0:
        base_df = pd.DataFrame({'dummy':0})
    else:
        base_df = input_df.copy()

    column_names = list(feature_cat_levels.keys())
    combinations = list(itertools.product(*list(feature_cat_levels.values())))
    for combo in combinations:
        for col_val,col_name in zip(combo,column_names):
            base_df[col_name] = [col_val]*len(base_df)
        df = pd.concat([base_df,df])

    if len(base_df) == 0:
        return df[list(feature_cat_levels.keys())]
    else:
        return df

def build_3n_factorial(n_features:int) -> pd.DataFrame:
    """Create a 3^n full factorial

    Args:
        n_features (int): Number of continuous features

    Returns:
        pd.DataFrame: 3^n full factorial
    """
    
    factor_data = []
    
    for run in itertools.product([-1,0,1],repeat=n_features):
        factor_data.append(list(run))
        
    return pd.DataFrame(factor_data)
    

#%% 2n

df = doepy.build.full_fact(feature_levels['cont'])
if has_cont & has_cat:
    designs['2n'] = add_categorical(feature_levels['cat'],df)

elif has_cont:
    designs['2n'] = df.copy()

elif has_cat:
    designs['2n'] = pd.DataFrame()

designs['2n'].reset_index(drop=True,inplace=True)

#%% 3n

df = build_3n_factorial(len(feature_names['cont']))
df.columns = feature_names['cont']
for feature in feature_names['cont']:
    df[feature] = rescalers[feature].reverse_transform(df[feature])

if has_cont & has_cat:
    designs['3n'] = add_categorical(feature_levels['cat'],df)

elif has_cont:
    designs['3n'] = df.copy()
    
elif has_cat:
    designs['3n'] = pd.DataFrame()

designs['3n'].reset_index(drop=True,inplace=True)

#%% CCF and CCD

for face,design in zip(['ccf','ccc'],['CCF','CCD']):

    df = doepy.build.build_central_composite(copy.deepcopy(feature_levels['cont']),face=face)

    if has_cont & has_cat:
        designs[design] = add_categorical(feature_levels['cat'].copy(),df)

    elif has_cont:
        designs[design] = df.copy()
        
    elif has_cat:
        designs[design] = pd.DataFrame()

    designs[design].reset_index(drop=True,inplace=True)

#%% BBD

if len(feature_levels['cont']) >= 3:

    df = doepy.build.box_behnken(copy.deepcopy(feature_levels['cont']))

    if has_cont & has_cat:
        designs['BBD'] = add_categorical(feature_levels['cat'],df)

    elif has_cont:
        designs['BBD'] = df.copy()
        
    elif has_cat:
        designs['BBD'] = pd.DataFrame()

    designs['BBD'].reset_index(drop=True,inplace=True)
else:
    designs['BBD'] = pd.DataFrame(columns=['No BBD was made because countinuous features < 3'])

#%% Export as df

with pd.ExcelWriter('Common_DoE_designs.xlsx', engine='openpyxl') as writer:
    for design,df in designs.items():
        df.to_excel(writer, sheet_name=design, index=False)

# #%% LHS (not implemented since we have not yet implemented a method to include num_exp)

# df = doepy.build.space_filling_lhs(feature_levels['cont'],num_exp)

# if has_cont & has_cat:
#     designs['LHS'] = add_categorical(feature_levels['cat'],df)

# elif has_cont:
#     designs['LHS'] = df.copy()
    
# elif has_cat:
#     designs['LHS'] = pd.DataFrame()

# designs['LHS'].reset_index(drop=True,inplace=True)

"""
Useful references

https://github.com/danieleongari/awesome-design-of-experiments

https://experimental-design.github.io/bofire/examples/
https://experimental-design.github.io/bofire/design_with_explicit_formula/

"""