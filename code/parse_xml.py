import csv 
import xml.etree.ElementTree as ET 
import os 
import re 
from os.path import dirname, abspath

def parseXLM(xlmfile,partier,krets_attributes=["KOD","MANDAT_VALKRETS","RÖSTER"] ,vote_attributes = ["RÖSTER","MANDAT","PROCENT"]):
    tree = ET.parse(xlmfile)
    root = tree.getroot()
    kommun = root.find("KOMMUN").attrib["KOD"]
    valkretsar = [] 
    for krets in root.findall("./KOMMUN/KRETS_KOMMUN"):
        valkrets = {attributes:krets.attrib[attributes] for attributes in krets_attributes }
        valkrets["KOMMUNKOD"] = kommun
        for parti in partier:
            match = "./GILTIGA/[@PARTI=\""+parti+"\"]"
            try:
                votes = krets.find(match).attrib
                for entry in votes:
                    if entry in vote_attributes:
                        valkrets[parti+"_"+entry] = votes[entry]
            except:
                continue
        valkretsar.append(valkrets)
    return valkretsar

def create_dataset(valar, partilista, outstub , krets_attributes=["KOD","MANDAT_VALKRETS","RÖSTER"] ,vote_attributes = ["RÖSTER","MANDAT","PROCENT"]):
    rootdir = dirname(dirname(abspath(__file__)))
    datapath = os.path.join(rootdir,"raw",str(valar))
    output = os.path.join(rootdir,"output", outstub + str(valar) + ".csv")
    valresultat = []
    for file in os.listdir(datapath):
        if re.match(r'.*\d{4}K.xml$',file):
            valresultat += parseXLM(os.path.join(datapath,file),partilista, krets_attributes, vote_attributes)

    with open(output, "w", newline = "") as csvfile:
        fieldnames = list(valresultat[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(valresultat) 


create_dataset(2010,["MP"],"valkrets_MP_")
create_dataset(2014,["MP"],"valkrets_MP_")
