# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 14:19:37 2020

@author: User
"""

import sys
import json
import numpy as np


def function(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
    bond_list = data['data']
    # create corporate bond list and government bond list
    corporate_bond = []
    government_bond = []
    for bond in bond_list:
        if(bond['type']=="corporate"):
            # get rid of bond with null values
            if(None not in [bond[i] for i in bond]):
                # convert years into numbers
                bond['tenor'] = float(bond['tenor'].replace(" years",""))
                # convert yield into numbers
                bond['yield'] = int(float(bond['yield'].replace("%",""))*100)
                corporate_bond.append(bond)
        elif (bond['type'] == "government"):
            # convert years into numbers
            bond['tenor'] = float(bond['tenor'].replace(" years",""))
            # convert yield into numbers
            bond['yield'] = int(float(bond['yield'].replace("%",""))*100)
            government_bond.append(bond)
    government_bond.sort(key = lambda x:(x['tenor'],x['amount_outstanding']))
    result = []
    government_tenor = np.array([x['tenor'] for x in government_bond])
    for bond in corporate_bond:
        idx = np.searchsorted(government_tenor,bond['tenor'],side='right')
        if(idx==0):
            dictionary = {'corporate_bond_id':bond['id'], 'government_bond_id': government_bond[0]['id'],"spread_to_benchmark":str(abs(government_bond[0]['yield']-bond['yield']))+" bps"}
            result.append(dictionary)
        elif(idx==len(government_bond)):
            dictionary = {'corporate_bond_id':bond['id'], 'government_bond_id': government_bond[-1]['id'],"spread_to_benchmark":str(abs(government_bond[-1]['yield']-bond['yield']))+" bps"}
            result.append(dictionary)
        else:
            left_diff = round(abs(government_bond[idx-1]['tenor']-bond['tenor']),2)
            right_diff = round(abs(government_bond[idx]['tenor']-bond['tenor']),2)
            if(left_diff < right_diff):
                dictionary = {'corporate_bond_id':bond['id'], 'government_bond_id': government_bond[idx-1]['id'],"spread_to_benchmark":str(abs(bond['yield']-government_bond[idx-1]['yield']))+" bps"}
                result.append(dictionary)
            elif(left_diff > right_diff):
                dictionary = {'corporate_bond_id':bond['id'], 'government_bond_id': government_bond[idx]['id'],"spread_to_benchmark":str(abs(government_bond[idx]['yield']-bond['yield']))+" bps"}
                result.append(dictionary)
            else:
                if(government_bond[idx-1]['amount_outstanding']>government_bond[idx]['amount_outstanding']):
                    dictionary = {'corporate_bond_id':bond['id'], 'government_bond_id': government_bond[idx-1]['id'],"spread_to_benchmark":str(abs(bond['yield']-government_bond[idx-1]['yield']))+" bps"}
                    result.append(dictionary)
                else:
                    dictionary = {'corporate_bond_id':bond['id'], 'government_bond_id': government_bond[idx]['id'],"spread_to_benchmark":str(abs(government_bond[idx]['yield']-bond['yield']))+" bps"}
                    result.append(dictionary)
    return {'data': result}



result = function(sys.argv[1])
json_object = json.dumps(result)
with open(sys.argv[2],"w") as f:
    f.write(json_object)

