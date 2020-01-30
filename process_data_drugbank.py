#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author:TenYun
@time: 2020/1/29
@contact: tenyun.zhang.cs@gmail.com
"""

import lxml.etree as ET
from tqdm import tqdm
import numpy as np

drugbank_path = "G:\\CEGNN\\materials\\drugbank_all_full_database\\drugbank.xml"
drugbank = ET.parse(drugbank_path)
root = drugbank.getroot()
# nodes = root.xpath("//drugbank-id[@primary='true']")
# for node in nodes:
#     print(node.text)
ns = {'db': 'http://www.drugbank.ca'}
drug_content = []
drug_network = []

for drug in tqdm(root.xpath("db:drug[db:groups/db:group='approved']", namespaces=ns)):
    drugName = drug.find("db:name", ns).text
    drugbank_id = drug.find("db:drugbank-id[@primary='true']", ns).text
    drugDescription = drug.find("db:description", ns).text
    if drugDescription is not None:
        drugDescription = drugDescription.replace("\n", "")
        drugDescription = drugDescription.replace("\r", "")
    state = drug.find("db:state", ns)
    if state is not None:
        state = state.text
    else:
        state = "None"
    drug_interactions = drug.xpath("db:drug-interactions/db:drug-interaction", namespaces=ns)
    drug_content.append([drugbank_id, drugName, state, drugDescription])

    for t in drug_interactions:
        t_drugbank_id = t.find("db:drugbank-id", ns).text
        name = t.find("db:name", ns).text
        interaction = t.find("db:description", ns).text
        drug_network.append([drugbank_id, t_drugbank_id, name, interaction])
drug_content = np.array(drug_content, dtype=np.str)
drug_network = np.array(drug_network, dtype=np.str)
np.savetxt("drugbank.content", drug_content, fmt="%s", delimiter=',', encoding="utf-8")
np.savetxt("drugbank.cites", drug_network, fmt="%s", delimiter=',', encoding="utf-8")
np.savetxt("drugbank_d2d.cites", drug_network[:, [0, 1]], fmt="%s", delimiter=",", encoding="utf-8")