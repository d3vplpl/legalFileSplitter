import pandas as pd
import glob, os
import eliminateNonDca
import numpy as np

#test 048735752000001606
files = glob.glob('./legal_*.csv')

for file in files:
    print('Processing file: ' + file)
    df = pd.read_csv(file, sep=',', encoding='latin-1', dtype={'CourtNumber': object, 'ClientAccountNumber': object})
    df1 = df[df.duplicated(subset=['ProceedingNumber', 'ID'], keep='first')]
    #print(df.ClientAccountNumber)
    df2 = df1.reindex(['ClientAccountNumber', 'ProceedingNumber', 'ID'], axis=1)
    df2.to_csv('duplicates.csv', index=False)