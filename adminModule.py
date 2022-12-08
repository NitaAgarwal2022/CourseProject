import pytoml
import os
import re
import sqlite3

  
def buildCorpus(rawDataPath,prefix):
    
    path=prefix+"/"+rawDataPath
    datFile = open("courseraData.dat", "a")
    labelFile = open("courseraData.labels", "a")
    for file in os.listdir(path):
        if file.endswith(".txt"):
            file_path = f"{path}\{file}"      
            with open(file_path, 'r') as f:
                doc=f.read()
                print("doc=",doc)
                
                processedLine1 = re.sub("\n", "", doc)
                processedLine2 = re.sub("\"", "", processedLine1)
                processedLine3 = re.sub("”", "", processedLine2)
                
                datFile.write(processedLine3)
                datFile.write("\n")
                labelFile.write(re.sub(".en.txt",".mp4",file))
                labelFile.write("\n")
                f.close()
                
    datFile.close()
    labelFile.close()
    return "value"

def getResults():
    conn = sqlite3.connect("C:/Users/nitaj/MS_work/sqlitedbFiles/TISProject.db")
    cursor = conn.cursor()
    #print("opened db")
    mpValue="MP2.1"
    #print(mpValue)
    rows = cursor.execute("SELECT l.label FROM search_results s, label_mapping l where s.mp_id=? and s.document_id=l.document_id ORDER by s.score desc",(mpValue,))
    #print("rows=",rows)
    value=""
    for i in rows:
        value+=i[0]
        value+="\n"
    #print("value=",value)
    conn.close()
    return "nita"


if __name__ == '__main__':
    cfg = "adminConfig.toml"
    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)
   

    rawDataPath = cfg_d['rawLectureData']
    prefix=cfg_d['prefix']
    #print("rawData",rawDataPath)
    buildCorpus(rawDataPath,prefix)
    getResults()