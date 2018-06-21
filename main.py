import pandas as pd
import glob, os
import eliminateNonDca

processForBankruptcy = False
eliminateCourtCode0 = False
import numpy as np

def cleanSpanishLetter(input_string):
    #print (input_string)
    input_string = str(input_string)
    result = input_string.replace('ó','o')
    result = result.replace('á', 'a')
    result = result.replace('à', 'a')
    result = result.replace('é', 'e')
    result = result.replace('í', 'i')
    result = result.replace('Á', 'A')
    result = result.replace('À', 'A')
    result = result.replace('Ú', 'U')
    result = result.replace('ú', 'u')
    result = result.replace('È', 'E')
    result = result.replace('É', 'E')
    result = result.replace('Ó', 'O')
    result = result.replace('Ò', 'O')
    result = result.replace('Í', 'I')
    result = result.replace('Ü', 'U')

    return result

def tryAnotherType(type):
    if (type == 'JUZGADO_DE_PRIMERA_INSTANCIA_E_INSTRUCCIÓN' ):
        return 'JUZGADO_DE_PRIMERA_INSTANCIA'
    elif (type =='JUZGADO_DE_PRIMERA_INSTANCIA'):
        return 'JUZGADO_DE_PRIMERA_INSTANCIA_E_INSTRUCCIÓN'



def searchForCourtCode(cType, cNumber, cLocation):
    #print(cLocation)
    cLocation = cleanSpanishLetter(cLocation).upper()
    #print(cType + ' ' + str(cNumber) + ' ' + str(cLocation) )
    in_same_location = (courtDict.loc[(courtDict['CourtLocation'] == (str(cLocation)).upper()   )])
    same_type = in_same_location.loc[(in_same_location['CourtType'] == cType)]
    if not (same_type["CourtCode"].values.any()):
        same_type = in_same_location.loc[(in_same_location['CourtType'] == tryAnotherType(cType))]
    same_number = same_type.loc[(same_type['CourtNumber'] == cNumber)]
    #print('Court Code: ' + same_number["CourtCode"].values)
    if (same_number["CourtCode"].values.any()):
        return (same_number["CourtCode"].values[0])
    else:
        result = searchForCourtCodeInAnotherDict(cType, cNumber, cLocation)

        if result != '0':
            return result
        else:
            if (str(cNumber) != '000'):
                pass
                #print(cType + ' ' + str(cNumber) + ' ' + str(cLocation))
            #print('Court Code: ' + result)
            return '0'


def searchForCourtCodeInAnotherDict(cType, cNumber, cLocation):
    cLocation = cleanSpanishLetter(cLocation).upper()

    #print(cType + ' ' + str(cNumber) + ' ' + str(cLocation) )
    in_same_location = (courtDict_v3.loc[(courtDict_v3['CourtLocation'] == (str(cLocation)).upper()   )])
    same_type = in_same_location.loc[(in_same_location['CourtType'] == cType)]
    if not (same_type["CourtCode"].values.any()):
        same_type = in_same_location.loc[(in_same_location['CourtType'] == tryAnotherType(cType))]
    same_number = same_type.loc[(same_type['CourtNumber'] == cNumber)]
    #print('Court Code: ' + same_number["CourtCode"].values)
    if (same_number["CourtCode"].values.any()):
        return (same_number["CourtCode"].values[0])
    else:
        result = searchForCourtCodeInYetAnotherDict(cType, cNumber, cLocation)
        return result

def searchForCourtCodeInYetAnotherDict(cType, cNumber, cLocation):
    cLocation = cleanSpanishLetter(cLocation).upper()

    #print(cType + ' ' + str(cNumber) + ' ' + str(cLocation) )
    in_same_location = (courtDict_v4.loc[(courtDict_v4['CourtLocation'] == (str(cLocation)).upper()   )])
    same_type = in_same_location.loc[(in_same_location['CourtType'] == cType)]
    if not (same_type["CourtCode"].values.any()):
        same_type = in_same_location.loc[(in_same_location['CourtType'] == tryAnotherType(cType))]
    same_number = same_type.loc[(same_type['CourtNumber'] == cNumber)]
    #print('Court Code: ' + same_number["CourtCode"].values)
    if (same_number["CourtCode"].values.any()):
        return (same_number["CourtCode"].values[0])
    else:
        return '0'

files = glob.glob('./legal_*.csv')
print(files)
courtDict = pd.read_csv('CourtCodes.csv', sep=',', encoding='latin-1', dtype={'CourtNumber': object, 'CourtCode': object})
courtDict_v3 = pd.read_csv('CourtCodes_v3.csv', sep=',', encoding='latin-1', dtype={'CourtNumber': object, 'CourtCode': object})
courtDict_v4 = pd.read_csv('CourtCodes_v4.csv', sep=',', encoding='latin-1', dtype={'CourtNumber': object, 'CourtCode': object})

for file in files:
    recordCounter = 0
    legalErrorCounter = 0
    print('Processing file: ' + file)
    df = pd.read_csv(file, sep=',', encoding='latin-1', dtype={'CourtNumber': object, 'ClientAccountNumber': object})
    #Eliminate bankruptcies
    if (not (processForBankruptcy)):
        df = df.loc[df['RecognizedAmountBK'].isin(['0'])]

    df.rename(columns={'ClientAccountNumber': 'CreditorReference'}, inplace=True)
    df.rename(columns={'ProceedingAmount': 'PresentedAmount'}, inplace=True)
    df.rename(columns={'UpdatedClaimedAmount': 'RecognizedAmountLE'}, inplace=True)
    df["CourtCode"] = ""
    if not (processForBankruptcy):
        df["ID"] = ""
        df = df.loc[~df['Stage'].isin(['CONCURSO'])]



    for index, row in df.iterrows():

        if eliminateNonDca.isNonDca(row['CreditorReference']):
            df.drop(index, inplace=True)
            continue
        df.set_value(index,'CourtCode', searchForCourtCode(row["CourtType"], row["CourtNumber"], row["CourtLocation"]))


        recordCounter = recordCounter + 1



    if eliminateCourtCode0:
        #df1 = df1[df1.CourtCode != 0]
        df = df.loc[~df['CourtCode'].isin(['0'])]
    df1 = df.reindex(['CreditorReference', 'PresentedAmount', 'CreditRankBK', 'ID', 'RecognizedAmountBK',
                      'RecognizedAmountLE', 'CourtCode', 'ProceedingNumber'], axis=1)

    #print(list(df))
    new_filename = os.path.splitext(file)[0]
    new_filename = new_filename.replace('Legal_', 'LegalInfo_')
    new_filename = new_filename.replace('legal_', 'LegalInfo_') + '.csv'
    date_from_filename = new_filename[-12:]
    date_from_filename = date_from_filename[:8]
    day_from_filename = date_from_filename[-2:]
    month_from_filename = date_from_filename[4:6]
    year_from_filename = date_from_filename[:4]
    new_filename = new_filename.split('_')[0] + '_' + new_filename.split('_')[1] + '_' + new_filename.split('_')[2] + '_' + day_from_filename + month_from_filename + year_from_filename
    new_filename = new_filename + '.csv'
    #print('new filename: ' + new_filename)
    df1.to_csv(new_filename, index=False)
    #print ('record:' + str(recordCounter))
    #print ('errors:' + str(legalErrorCounter))
#LegalActiviy header
#CreditorReference,CourtCode,ProceedingNumber,Stage,Status,LastAction,LastActionDate,Impulse,ImpulseKind,ImpulseDate,Seizure,SeizureDate,SeizureKind,Comments

    df2 = df.reindex(['CreditorReference','CourtCode','ProceedingNumber','Stage',
                     'Status','LastAction','LastActionDate','Impulse','ImpulseKind','ImpulseDate','Seizure','SeizureDate',
                     'SeizureKind','Comments'], axis=1)

    #df2 = df2[df2.LastAction != 'NO_DEFINIDO']
    df2['LastActionDate'].replace('', np.nan, inplace=True)
    df2.dropna(subset=['LastActionDate'], inplace=True)


    new_filename = os.path.splitext(file)[0]
    new_filename = new_filename.replace('Legal_', 'LegalActivity_')
    new_filename = new_filename.replace('legal_', 'LegalActivity_') + '.csv'
    date_from_filename = new_filename[-12:]
    date_from_filename = date_from_filename[:8]
    day_from_filename = date_from_filename[-2:]
    month_from_filename = date_from_filename[4:6]
    year_from_filename = date_from_filename[:4]
    new_filename = new_filename.split('_')[0] + '_' + new_filename.split('_')[1] + '_' + new_filename.split('_')[2] + '_' + day_from_filename + month_from_filename + year_from_filename
    new_filename = new_filename + '.csv'
    df2.to_csv(new_filename, index=False)



#searchForCourtCode('JUZGADO_DE_PRIMERA_INSTANCIA_E_INSTRUCCIÓN','001','AMURRIO')