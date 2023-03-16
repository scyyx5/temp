import sys
sys.path.insert(1, '../../visualization/')
import re
import os

def adjustData(filename, ageTitle, cohortTitle, defaultFlagTitle, predictedDefaultTitle):
    filename = '../../visualization/' + filename + ".csv"
    #if(separator != ","):
    #    undateSeperator(filename,separator)
    #print(filename, separator, ageTitle, cohortTitle, defaultFlagTitle, predictedDefaultTitle)
    if(ageTitle != "t"):
        alterTitle(filename,ageTitle,"t")
    if(cohortTitle != "v"):
        alterTitle(filename,cohortTitle,"v")
    if(defaultFlagTitle != "y"):
        alterTitle(filename,defaultFlagTitle,"y")
    if(predictedDefaultTitle != "pd"):
        alterTitle(filename,predictedDefaultTitle,"pd")

'''
def undateSeperator(filename,separator):
    file = open(filename,"r")
    lines = file.readlines()
    file.close()
    file = open(filename,"w+")
    for line in lines:
        a = re.sub(",","",line)
        a = re.sub(separator,",",a)
        file.writelines(a)
    file.close
'''

def alterTitle(filename,old_str,new_str):
    with open(filename, "r") as f1,open("%s.bak" % filename, "w") as f2:
        for line in f1:
            if old_str in line:
                line = line.replace(old_str, new_str)
            f2.write(line)
    os.remove(filename)
    os.rename("%s.bak" % filename, filename)

    


