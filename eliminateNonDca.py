import pandas as pd
import glob

nonDca = pd.read_csv('NonDcaAccounts.csv', sep=',', encoding='latin-1', dtype={'AccountReference': object})
correctedTypes = pd.read_csv('correctedCourtTypes.csv', sep=',', encoding='latin-1')
duplicateBankruptcies = pd.read_csv('duplicates.csv', sep=',', encoding='latin-1', dtype={'ClientAccountNumber': object})
phase1BNK = pd.read_csv('phase1BNK_IDs.csv', sep=',', encoding='latin-1')

#files = glob.glob('./legal_*.csv')
#print(files)


def isNonDca(clientAccountNumber):

    for index2, row2 in nonDca.iterrows():
        if (clientAccountNumber == row2['AccountReference']):
            print(str(row2['AccountReference'])+','+str(row2['processTag']))
            return True
    return False


def is_duplicate(clientAccountNumber):


    for index2, row2 in duplicateBankruptcies.iterrows():

        if (clientAccountNumber == row2['ClientAccountNumber']):
            #print(str(row2['ClientAccountNumber']))
            return True
    return False


def is_phase1(ID):


    for index2, row2 in phase1BNK.iterrows():

        if (ID == row2['ID']):
            print(str(row2['ID']))
            return True
    return False

#print(is_duplicate('048716542000000959'))
