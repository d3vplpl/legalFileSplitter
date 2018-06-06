import pandas as pd
import glob

nonDca = pd.read_csv('NonDcaAccounts.csv', sep=',', encoding='latin-1', dtype={'AccountReference': object})


#files = glob.glob('./legal_*.csv')
#print(files)

def isNonDca(clientAccountNumber):


    for index2, row2 in nonDca.iterrows():
        if (clientAccountNumber == row2['AccountReference']):
            print(str(row2['AccountReference'])+','+str(row2['processTag']))
            return True
    return False


