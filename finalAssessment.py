#!/usr/bin/env python
# coding: utf-8

# # Final Assessment
# 
# Your university is collaborating with a company to develop a tool for processing reports of cases of a particular disease. The company has a very specific way of doing things, and has asked you to design and build a JavaScript object to interact with their proprietary code. Your supervisor wants you to submit an example of your code working within a Jupyter notebook (her preferred environment!) so she can review it before sending it off to the company.
# 
# Remember - your code will be tested against other input data, so make sure that you are being careful in your assumptions!
# 
# ### Task 1
# 
# You have been provided with a sample of the case incidence records to help you test your code in the file "sampleCases.tsv". The company has done a questionable job of digitising these records, however, and you will need to clean them up a bit before you process them. Remember, .tsv files are "tab separated values", meaning that the entries are separated by tabs rather than commas (see [here](https://docs.python.org/3/reference/lexical_analysis.html#literals) for more information).
# 
# Read in the file and store each record as an element within a list.

# In[1]:


##defines CHECKRECORDTYPE function, which takes two parameters: DATA AND INDEX 
#1) when passed these parameters, the function assigns the 0-th value of the INDEX-th entry 
#   in the DATA list to the RECORD var, once splitting the 0-th value into multiple list entries 
#   via ";"
#2) create LENGTH variable equal to the number of entries in RECORD; create INDEX equal to
#   zero; create empty TYPELIST list
#3) use while loop to iterate when INDEX is less than LENGTH:
#  TRY: 
#4) to convert RECORD's INDEX-th entry to a float; if possible, append "num" to TYPELIST
#   in the INDEX-th position
#  EXCEPT: 
#5) if the RECORD'S INDEX-th entry cannot be converted, then append "else" to TYPELIST  
#   in the INDEX-th position
#6) return the TYPELIST for use in the CHECKHEADER function
#Parameters:
########### data (list)
########### index (integer)
##########################################################################################
def checkRecordType(data,index):
#1)
    record = data[index][0].split(";")
#2)
    length = len(record)
    index = 0
    typeList = []
#3)
    while index < length:
        try:
#4)
            float(record[index])
            typeList.append("num")
            index = index + 1
        except:
#5)
            typeList.append("else")
            index = index + 1
#6)
    return typeList
##########################################################################################
##########################################################################################
##defines CHECKHEADER function, which takes one parameter: DATA 
#1) create INDEX, FIRST, and SECOND variables, all equal to zero
#2) use while loop to iterate while FIRST is still equal to zero:
#3) use if to increase INDEX by 1 if the INDEX-th entry in data is an empty line; 
#4) use elif to set the value of FIRST var to the TYPELIST of the INDEX-th entry of DATA, 
#   as produced by CHECKRECORDTYPE function
#3) set INDEX to 1 plus itself, so that we start one line below FIRST in the following while
#   loop
#4) use while loop to iterate while SECOND is still equal to zero:
#5) IF the INDEX-th entry in DATA is an empty line, increase INDEX by 1 if  
#6) ELIF the INDEX-th entry is not an empty line, set the value of SECOND to the TYPELIST 
#   of the INDEX-th entry of DATA, as produced by CHECKRECORDTYPE function
#7) create HEADER var with the boolean value "False" if the first and second entries variable 
#   types do not match, or with boolean value "True" if they do
#8) return HEADER var for use in the TSVFILE function
#Parameter:
########### data (list)
##########################################################################################
def checkHeader(data):
#1)
    index = 0
    first = 0
    second = 0
#2)
    while first == 0:
#3)
        if data[index] == "":
            index = index + 1
#4)
        elif data[index] != "":
            first = checkRecordType(data,index)
#5)
    index = index + 1
#6)
    while second == 0:
        if data[index] == "":
            index = index + 1
        elif data[index] != "":
            second = checkRecordType(data,index)
#7)
    header = first == second
#8)
    return header
##########################################################################################
##########################################################################################
##defines the TSVFILE function, which takes one parameter: FILENAME
#  TRY:
#1) create FILENAME var equal to the string of FILENAME; create FILECONTENT var equal to
#   the raw read-in of FILENAME parameter, using READLINES() funtion; create empty DATA
#   list
#2) using a for loop for each LINE in FILECONTENT:
#3) create empty list LINELIST; append this list with with LINE from FILECONTENT, with the
#   LINE's tab-separators ("\t") replaced by ";", and with its line-breaks ("\n") replaced
#   by ""
#4) IF LINELIST does not represent an empty line, append LINELIST to DATA
#5) ELSE print a warning message telling the user that LINELIST's line was omitted from
#   DATA because it is empty
#6) IF CHECKHEADER function returns "False" when passed DATA, then remove the 0-th entry
#   and print message telling user that a header has been removed
#7) create DATADICT dictionary which holds "NAME" and "DATA" keys, so that this info can 
#   be preserved for following analysis and tasks; "name" is equal to FILENAME while
#   "data" is equal to DATA
#8) return DATADICT for use in following tasks
#  EXCEPT:
#9) if passed FILENAME parameter is either misspecified or does not exist, then print out
#   error message telling the user
#Parameter: 
########### filename (string)
##########################################################################################
def TSVFile(filename):
    try:
#1)
        fileName=str(filename)
        fileContent=open(fileName).readlines()
        data=[]
#2)
        for line in fileContent:
#3)
            lineList = []
            lineList.append(line.replace("\t", ";").replace("\n",""))
#4)
            if lineList[0] != "":
                data.append(lineList)
#5)
            else:
                print("Line " + str(fileContent.index(line)) + 
                      " was omitted from the data because it is empty.")
#6)
        if checkHeader(data) == False:
            data.pop(0)
            print("Header was removed.")
#7)
        dataDict = {
            "name" : fileName,
            "data" : data
        }
#8
        return dataDict
    except:
#9
        print("Error: your file does not exist or was misspecified.")
##########################################################################################
##########################################################################################
data = TSVFile("sampleCases.tsv")


# ### Task 2
# 
# If you look at the records, you find that the latitudes and longitudes of cases are sometimes formatted strangely - apparently the automatic text recognitition software used by the company has a few bugs in it! Go through the records and prompt the user to input the corrected values in cases where the elements cannot be processed as numbers.

# In[2]:


##define CHECKLAT function which takes two parameters: RECORDLIST and RECORDID
#1) create LATITUDE var eaual to the 1-st entry in the pass RECORDLIST parameter
#  TRY:
#2) convert LATITUDE to a float (i.e. check if it is a number) 
#  EXCEPT:
#3) if LATITUDE cannot be converted, prompt the user to set the correct latitude; identifies
#   the record by RECORDID when prompting user
#4) use while loop to iterate when LATITUDE converted to a float is outside [-90,90]; this
#   makes sure that the input latitude is geographically feasible
#5) while the LATITUDE is infeasibler, prompt user to reset LATITUDE until it is 
#6) returns LATITUDE for use in the CHECK function
#Parameters:
########### recordList (list)
########### recordID (string)
##########################################################################################
def checkLat(recordList, recordID):
#1)
    latitude = recordList[1]
    try:
#2
        latitude = float(latitude)
    except:
#3
        latitude = input("Please input the correct latitude for " + str(recordID) + ".\n")
#4
    while ((float(latitude) < -90) or (float(latitude) > 90)):
#5
        latitude = float(input("Please input the correct latitude for " + str(recordID) + ".\n"))
#6
    return float(latitude)
##########################################################################################
##########################################################################################
##define CHECKLONG function which takes two parameters: RECORDLIST and RECORDID
#1) create LONGITUDE var eaual to the 2-nd entry in the pass RECORDLIST parameter
#  TRY:
#2) convert LONGITUDE to a float (i.e. check if it is a number) 
#  EXCEPT:
#3) if LONGITUDE cannot be converted, prompt the user to set the correct longitude; identifies
#   the record by RECORDID when prompting user
#4) use while loop to iterate when LONGITUDE converted to a float is outside [-180,180]; this
#   makes sure that the input longitude is geographically feasible
#5) while the LONGITUDE is infeasibler, prompt user to reset LONGITUDE until it is 
#6) returns LONGITUDE for use in the CHECK function
#Parameters:
########### recordList (list)
########### recordID (string)
##########################################################################################
def checkLong(recordList, recordID):
#1)
    longitude = recordList[2]
    try:
#2)
        longitude = float(longitude)
    except:
#3)
        longitude = input("Please input the correct longitude for " + str(recordID) + ".\n")
#4)
    while ((float(longitude) < -180) or (float(longitude) > 180)):
#5)
        longitude = float(input("Please input the correct longitude for " + str(recordID) + ".\n"))
#6)
    return float(longitude)
##########################################################################################
##########################################################################################
##define CHECK function which takes one parameters: COORDDICT
#1) create INPUTLIST var from the "data" key of the input COORDDICT parameter;
#   create empty CORRECTCOORDS list
#2) FOR RECORD in INPUTLIST:
#   set RECORDLIST value to the RECORD's 0-th entry, split on ";"
#   set RECORDID value to the 0-th entry in RECORDLIST
#3) set the 1-st entry of RECORDLIST equal to the LATITUDE passed back by the CHECKLAT
#   function after passing it RECORDLIST and RECORDID
#4) set the 2-nd entry of RECORDLIST equal to the LONGITUDE passed back by the CHECKLONG
#   function after passing it RECORDLIST and RECORDID
#5) append RECORDLIST to CORRECTCOORDS
#6) return CORRECTCOORDS for use in following tasks
#Parameter:
########### coordDict (dictionary)
##########################################################################################
def check(coordDict):
#1)
    inputList = coordDict["data"]
    correctCoords = []
#2)
    for record in inputList:
        recordList = record[0].split(";")
        recordID = recordList[0]
#3)
        recordList[1] = checkLat(recordList, recordID)
#4)
        recordList[2] = checkLong(recordList, recordID)
#5)
        correctCoords.append(recordList)
#6)
    return correctCoords
##########################################################################################
##########################################################################################
correctCoords = check(data)


# ### Task 3
# 
# It's time to format the data so that you can transfer it to the JavaScript portion of your work. You'll need to copy over the latitudes and longitudes. You may format these as a set of dictionaries, a pair of lists, or some other structure - it is up to you. 

# In[3]:


##define COORDLIST function which takes two parameters: CORRECTCOORDS and RECORDCOORDINDEX
#1) create emptyCOORDLIST list
#2) FOR RECORD in CORRECTCOORDS input parameter:
#   append the RECORDCOORDINDEX-th entry of RECORD to COORDLIST
#3) return COORDLIST for use in COORDDICT function
#Parameters:
########### correctCoords        (list)
########### recordCoordIndex     (integer)
##########################################################################################
def coordList(correctCoords, recordCoordIndex):
#1)
    coordList = []
#2)
    for record in correctCoords:
        coordList.append(record[recordCoordIndex])
#3)
    return coordList
##########################################################################################
##########################################################################################
##defines COORDDICT function which takes one parameter: CORRECTCOORDS
#1) create LATS list by passing the COORDLIST function the CORRECTCOORDS parameter and 1;
#   1 is the index that correlates to latitude's position in CORRECTCOORDS' entries
#2) create LONGS list by passing the COORDLIST function the CORRECTCOORDS parameter and 2;
#   2 is the index that correlates to longitude's position in the CORRECTCOORDS' entries
#3) create COORDDICT dictionary, which consists of a "lats" key equal to LATS and a "longs"
#   key equal to LONGS
#4) return COORDDICT so that it can be used in following tasks
#Parameter:
########### correctCoords        (list)
##########################################################################################
def coordDict(correctCoords):
#1)
    lats = coordList(correctCoords,1)
#2)
    longs = coordList(correctCoords,2)
#3)
    coordDict = {
        "lats" : lats,
        "longs" : longs
    }
#4)
    return coordDict
##########################################################################################
##########################################################################################
coordDict = coordDict(correctCoords)
print(coordDict)


# ### Task 4
# 
# The company wants you to create a kind of object called a `CaseStudy` to help them deal with all of the records associated with this file. In the future, they will use other `CaseStudy` objects to compare this set of data with other sets of data. But in this case, you just want to test creating a single `CaseStudy` and using its functions. 
# 
# The `CaseStudy` object should be able to:
# 
# * return its geographic extent (the minimum and maximum of both latitude and longitude) as a list (e.g. `[min_lat, max_lat, min_lon, max_lon]`)
# * return the weighted centroid of the points as a list (e.g. `[cent_lat, cent_lon]`)
# 
# The `CaseStudy` object should also have attributes to hold:
# 
# * the name of the case study (a string)
# * the year in which the case study was conducted (an integer)
# * a value indicating whether the company took part in gathering the data (a boolean)
# 
# Your supervisor would like for you to create the instance of `CaseStudy` based on the data given here, calculate both the geographic extent and the weighted centroid, and export those two values back to your Python environment. You may set the name, year, and participation values of the `CaseStudy` to whatever you like.

# In[122]:


get_ipython().run_cell_magic(u'javascript', u'', u'// you can use this to test/practice your JavaScript!\n////////////////////////////////////////////////////PRACTICE DATA///////////////////////////////////////////////////////////////\nvar coordDict = {\'lats\': [\'8.167\', \'8.127\', \'8.198\', \'0\', \'8.240\', \'8.208\', \'8.221\', \'0\', \'8.191\', \'8.192\'], \n                \'longs\': [\'-10.650\', \'-10.712\', \'0\', \'-10.677\', \'-10.639\', \'-10.558\', \'-10.714\', \'-10.691\', \'-10.659\', \'0\']};\n\nvar lats = coordDict["lats"];\nvar longs = coordDict["longs"];\n////////////////////////////////////////////////////PRACTICE DATA///////////////////////////////////////////////////////////////\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n//defines GETMIN function which takes one parameter: COORDLIST\n//1) create I var equal to zero;\n//   create length var equal to the number of entries in COORDLIST;\n//   create MIN var equal to the 0-th entry of COORDLIST, converted to a number\n//2) WHILE I is less than LENGTH:\n//3) IF the I-th entry in COORDLIST converted to a number is less than or equal to MIN, then set MIN equal to that entry,\n//   converted to a number\n//4) within the WHILE loop, set I to I plus 1, so that COORDLIST is iterated through and all entries are checked for the MIN\n//5) return MIN for use in the GETGEOEXT and GETCENTROID functions\n//Parameter:\n/////////// coordList (list)\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\nfunction getMin(coordList)\n{\n//1)\n    var i = 0,\n        length = coordList.length,\n        min = Number(coordList[0]);\n//2)\n    while (i < length)\n    {\n//3)\n        if (Number(coordList[i]) <= min)\n        {\n            min = Number(coordList[i]);\n        }\n//4)\n        i = i + 1;\n    }\n//5)\n    return min;\n}\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n//defines GETMAX function which takes one parameter: COORDLIST\n//1) create I var equal to zero;\n//   create length var equal to the number of entries in COORDLIST;\n//   create MAX var equal to the 0-th entry of COORDLIST, converted to a number\n//2) WHILE I is less than LENGTH:\n//3) IF the I-th entry in COORDLIST converted to a number is greater than MAX, then set MAX equal to that entry,\n//   converted to a number\n//4) within the WHILE loop, set I to I plus 1, so that COORDLIST is iterated through and all entries are checked for the MAX\n//5) return MAX for use in the GETGEOEXT and GETCENTROID functions\n//Parameter:\n/////////// coordList (list)\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\nfunction getMax(coordList)\n{\n//1)\n    var i = 0,\n        length = coordList.length,\n        max = Number(coordList[0]);\n//2)\n    while (i < length)\n    {\n//3)\n        if (Number(coordList[i]) > max)\n        {\n            max = Number(coordList[i])\n        }\n//4)\n        i = i + 1\n    }\n//5)\n    return max\n}\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n//defines GETGEOEXT function which takes two parameters: LATS and LONGS\n//1) create LATSMIN var equal to the output of GETMIN function when it is passed the LATS parameter\n//   create LONGSMIN var equal to the output of GETMIN function when it is passed the LONGS parameter\n//   create LATSMAX var equal to the output of GETMAX function when it is passed the LATS parameter\n//   create LONGSMAX var equal to the output of GETMAX function when it is passed the LONGS parameter\n//2) create GEOEXT list var equal to [LATSMIN, LATSMAX, LONGSMIN, LONGSMAX]\n//3) return GEOEXT for use in CASESTUDY function\n//Parameters:\n/////////// lats (list)\n/////////// longs (list)\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\nfunction getGeoExt(lats,longs){\n//1)\n    var latsMin = getMin(lats);\n    var longsMin = getMin(longs);\n    var latsMax = getMax(lats);\n    var longsMax = getMax(longs);\n//2)\n    var geoExt = [latsMin, latsMax, longsMin, longsMax];\n//3)\n    return geoExt;\n}\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n//defines GETCENTROID function which takes two parameters: LATS and LONGS\n//1) create LATSMIN var equal to the output of GETMIN function when it is passed theLATS parameter\n//   create LONGSMIN var equal to the output of GETMIN function when it is passed the LONGS parameter\n//   create LATSMAX var equal to the output of GETMAX function when it is passed the LATS parameter\n//   create LONGSMAX var equal to the output of GETMAX function when it is passed the LONGS parameter\n//2) create CENTROID list var equal to [ (LATSMIN + LATSMAX)/2 , (LONGSMIN + LONGSMAX)/2 ], a list of the centroid\'s\n//   coordinates, which are obtained by calculating the midpoints for latitudes and longitudes\n//3) return CENTROID for use in CASESTUDY function\n//Parameters:\n/////////// lats (list)\n/////////// longs (list)\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\nfunction getCentroid(lats, longs){\n//1)\n    var latsMin = getMin(lats);\n    var longsMin = getMin(longs);\n    var latsMax = getMax(lats);\n    var longsMax = getMax(longs);\n//2)\n    var centroid = [((latsMin + latsMax)/2),((longsMin + longsMax)/2)];\n//3)\n    return centroid;\n}\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n//defines CASESTUDY object function which takes four parameters: NAME, YEAR, PARTICIPATED, and COORDDICT\n//1) create LATS var equal to input parameter LATS;\n//   create LONGS var equal to input parameter LONGS;\n//   give the object being created a "name" of the input parameter NAME\n//   give the object being created a "extent" of the output of the GETGEOEXT function passed LATS and LONGS\n//   give the object being created a "centroid" of the output of the GETCENTROID function passed LATS and LONGS\n//   give the object being created a "year" of the input parameter YEAR\n//   give the object being created a "participated" of the input parameter PARTICIPATED\n//Parameters:\n/////////// name (string)\n/////////// year (integer)\n/////////// participated (JavaScript boolean, passed as string)\n/////////// coordDict (dictionary)\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\nfunction CaseStudy(name, year, participated, coordDict) \n{\n//1)\n    lats = coordDict["lats"];\n    longs = coordDict["longs"];\n    this.name = name;\n    this.extent = getGeoExt(lats,longs);\n    this.centroid = getCentroid(lats,longs);\n    this.year = year;\n    this.participated = participated;\n}\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\nvar caseStudy1 = new CaseStudy("CaseStudy12", 2018, "false", coordDict);\nconsole.log(caseStudy1)')


# In[5]:


from IPython.display import display, Javascript

display(Javascript("""
function getMin(coordList)
{
//1)
    var i = 0,
        length = coordList.length,
        min = Number(coordList[0]);
//2)
    while (i < length)
    {
//3)
        if (Number(coordList[i]) <= min)
        {
            min = Number(coordList[i]);
        }
//4)
        i = i + 1;
    }
//5)
    return min;
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//defines GETMAX function which takes one parameter: COORDLIST
//1) create I var equal to zero;
//   create length var equal to the number of entries in COORDLIST;
//   create MAX var equal to the 0-th entry of COORDLIST, converted to a number
//2) WHILE I is less than LENGTH:
//3) IF the I-th entry in COORDLIST converted to a number is greater than MAX, then set MAX equal to that entry,
//   converted to a number
//4) within the WHILE loop, set I to I plus 1, so that COORDLIST is iterated through and all entries are checked for the MAX
//5) return MAX for use in the GETGEOEXT and GETCENTROID functions
//Parameter:
/////////// coordList (list)
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function getMax(coordList)
{
//1)
    var i = 0,
        length = coordList.length,
        max = Number(coordList[0]);
//2)
    while (i < length)
    {
//3)
        if (Number(coordList[i]) > max)
        {
            max = Number(coordList[i])
        }
//4)
        i = i + 1
    }
//5)
    return max
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//defines GETGEOEXT function which takes two parameters: LATS and LONGS
//1) create LATSMIN var equal to the output of GETMIN function when it is passed the LATS parameter
//   create LONGSMIN var equal to the output of GETMIN function when it is passed the LONGS parameter
//   create LATSMAX var equal to the output of GETMAX function when it is passed the LATS parameter
//   create LONGSMAX var equal to the output of GETMAX function when it is passed the LONGS parameter
//2) create GEOEXT list var equal to [LATSMIN, LATSMAX, LONGSMIN, LONGSMAX]
//3) return GEOEXT for use in CASESTUDY function
//Parameters:
/////////// lats (list)
/////////// longs (list)
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function getGeoExt(lats,longs){
//1)
    var latsMin = getMin(lats);
    var longsMin = getMin(longs);
    var latsMax = getMax(lats);
    var longsMax = getMax(longs);
//2)
    var geoExt = [latsMin, latsMax, longsMin, longsMax];
//3)
    return geoExt;
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//defines GETCENTROID function which takes two parameters: LATS and LONGS
//1) create LATSMIN var equal to the output of GETMIN function when it is passed theLATS parameter
//   create LONGSMIN var equal to the output of GETMIN function when it is passed the LONGS parameter
//   create LATSMAX var equal to the output of GETMAX function when it is passed the LATS parameter
//   create LONGSMAX var equal to the output of GETMAX function when it is passed the LONGS parameter
//2) create CENTROID list var equal to [ (LATSMIN + LATSMAX)/2 , (LONGSMIN + LONGSMAX)/2 ], a list of the centroid's
//   coordinates, which are obtained by calculating the midpoints for latitudes and longitudes
//3) return CENTROID for use in CASESTUDY function
//Parameters:
/////////// lats (list)
/////////// longs (list)
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function getCentroid(lats, longs){
//1)
    var latsMin = getMin(lats);
    var longsMin = getMin(longs);
    var latsMax = getMax(lats);
    var longsMax = getMax(longs);
//2)
    var centroid = [((latsMin + latsMax)/2),((longsMin + longsMax)/2)];
//3)
    return centroid;
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//defines CASESTUDY object function which takes four parameters: NAME, YEAR, PARTICIPATED, and COORDDICT
//1) create LATS var equal to input parameter LATS;
//   create LONGS var equal to input parameter LONGS;
//   give the object being created a "name" of the input parameter NAME
//   give the object being created a "extent" of the output of the GETGEOEXT function passed LATS and LONGS
//   give the object being created a "centroid" of the output of the GETCENTROID function passed LATS and LONGS
//   give the object being created a "year" of the input parameter YEAR
//   give the object being created a "participated" of the input parameter PARTICIPATED
//Parameters:
/////////// name (string)
/////////// year (integer)
/////////// participated (JavaScript boolean, passed as string)
/////////// coordDict (dictionary)
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function CaseStudy(name, year, participated, coordDict) 
{
//1)
    var lats = coordDict["lats"];
    var longs = coordDict["longs"];
    this.name = name;
    this.extent = getGeoExt(lats,longs);
    this.centroid = getCentroid(lats,longs);
    this.year = year;
    this.participated = participated;
}
var caseStudy = new CaseStudy(%s, %s, %s, %s);

IPython.notebook.kernel.execute('extent=' + caseStudy.extent + ';');
IPython.notebook.kernel.execute('centroid=' + caseStudy.centroid + ';');
IPython.notebook.kernel.execute('name="' + caseStudy.name + '";');
IPython.notebook.kernel.execute('year="' + caseStudy.year + '";');
IPython.notebook.kernel.execute('participated="' + caseStudy.participated + '";');

""" %("'CaseStudy12'", 2020, "false", coordDict)))


# ### Task 5
# 
# As a final step, write out the geographic extent, centroid, and the original filename of the data to a file named "output.txt".

# In[6]:


##define WRITETOTXT function which takes one parameter: FILENAME
#1) create FILE var by using the OPEN function with a string of the FILENAME parameter and 
#   "w", so that the user has permission to write to the file
#2) use the WRITE function to write to FILENAME a formatted version of variables: 
#   NAME
#   EXTENT
#   CENTROID
#   YEAR
#   PARTICIPATED
#   input file name as DATA["name"]
#3) close the file
#Parameter:
########### fileName  (string)
##########################################################################################
def writeToTXT(fileName):
#1)
    file = open(str(fileName), "w")
#2)
    file.write("Case Name:          " + str(name) + 
                    "\nGeographic Extent:  " + str(extent) + 
                    "\nCentroid:           " + str(centroid) +
                    "\nYear:               " + str(year) +
                    "\nParticipated:       " + str(participated) +
                    "\nInput File Name:    " + data["name"])
#3)
    file.close()
##########################################################################################
##########################################################################################
writeToTXT("output.txt")

