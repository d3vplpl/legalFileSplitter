import pandas as pd
import glob

correctedTypes = pd.read_csv('correctedCourtTypes.csv', sep=',', encoding='latin-1', dtype={'courtCode': object})

courtDict = pd.read_csv('CourtCodes.csv', sep=',', encoding='latin-1', dtype={'CourtNumber': object, 'CourtCode': object})
courtDict_v3 = pd.read_csv('CourtCodes_v3.csv', sep=',', encoding='latin-1', dtype={'CourtNumber': object, 'CourtCode': object})
courtDict_v4 = pd.read_csv('CourtCodes_v4.csv', sep=',', encoding='latin-1', dtype={'CourtNumber': object, 'CourtCode': object})


def correctTheType (courtCode,currentType):


    for index, row in correctedTypes.iterrows():
        if (courtCode == row['courtCode']):
            print (row['finalType'])
            return row['finalType']
    return currentType

def fixDict(dict):

    for index, row in dict.iterrows():

        dict.set_value(index,'CourtType', correctTheType(row['CourtCode'],row['CourtType']))
    dict.to_csv('fixedDict.csv', index=False, encoding='latin-1')


fixDict(courtDict)
