import pandas as pd
import glob, os
import numpy as np

files = glob.glob('./legalActivity_*.csv')

for file in files:
    recordCounter = 0
    legalErrorCounter = 0
    print('Processing file: ' + file)
    df = pd.read_csv(file, sep=',', encoding='latin-1', dtype={'CreditorReference': object, 'CourtCode': object})

#LegalActivity Header
# CreditorReference, CourtCode, ProceedingNumber, Stage, Status, LastAction, LastActionDate, Impulse, ImpulseKind,
    # ImpulseDate, Seizure, SeizureDate, SeizureKind, Comments
#LegalInfo Header
#CreditorReference, PresentedAmount, CreditRankBK, ID, RecognizedAmountBK, RecognizedAmountLE, CourtCode, ProceedingNumber

    df['PresentedAmount'] = ''
    df['CreditRankBK'] = ''
    df['ID'] = ''
    df['RecognizedAmountBK'] = ''
    df['RecognizedAmountLE'] = ''

    df = df.reindex(['CreditorReference', 'PresentedAmount', 'CreditRankBK', 'ID',
                     'RecognizedAmountBK', 'RecognizedAmountLE', 'CourtCode', 'ProceedingNumber'], axis=1)

    new_filename = os.path.splitext(file)[0]
    new_filename = new_filename.replace('LegalActivity_', 'LegalInfo_')
    new_filename = new_filename.replace('legalActivity_', 'LegalInfo_') +'.csv'
    date_from_filename = new_filename[-12:]

    new_filename = new_filename.split('_')[0] + '_' + new_filename.split('_')[1] + '_' + new_filename.split('_')[2] + '_'+ date_from_filename

    df.to_csv(new_filename, index=False)

#df.to_csv('Subrogaciones_output.csv', index = False)