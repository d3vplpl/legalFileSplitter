import pandas as pd
import glob, os
import eliminateNonDca
import numpy as np

#Subrogaciones header
#CreditorReference,ID,PresentationDate,StatusAdmited,DateAdmisionRejected,ReasonRejected,
# RequiredSubsanation,DateRequiredSubsanation,SubsanationDone,CourtCode,ProceedingNumber
#Old legal header
#Purse,ClientAccountNumber,ProceedingAmount,CreditRankBK,RecognizedAmountBK,
# UpdatedClaimedAmount,SubrogationDate,SubrogationCopyDate,CourtType,CourtNumber,CourtLocation,
# ,Stage,Status,LastAction,LastActionDate,Impulse,ImpulseKind,ImpulseDate,Seizure,SeizureDate,SeizureKind,Comments

files = glob.glob('./legal_*.csv')

for file in files:
    recordCounter = 0
    legalErrorCounter = 0
    print('Processing file: ' + file)
    df = pd.read_csv(file, sep=',', encoding='latin-1', dtype={'CourtNumber': object, 'ClientAccountNumber': object})


    #Eliminate emptySubrogationDate
    df['SubrogationDate'].replace('', np.nan, inplace=True)
    df.dropna(subset=['SubrogationDate'], inplace=True)


    df.rename(columns={'ClientAccountNumber': 'CreditorReference'}, inplace=True)
    df.rename(columns={'SubrogationDate':  'PresentationDate'}, inplace=True)
    df['ID'] = ''
    df['StatusAdmited'] = 'Admited'
    df['DateAdmisionRejected'] = ''
    df['ReasonRejected'] = ''
    df['RequiredSubsanation'] = ''
    df['DateRequiredSubsanation'] = ''
    df['SubsanationDone'] = ''
    df['CourtCode'] = '0001'

    # Subrogaciones header
    # CreditorReference,ID,PresentationDate,StatusAdmited,DateAdmisionRejected,ReasonRejected,
    # RequiredSubsanation,DateRequiredSubsanation,SubsanationDone,CourtCode,ProceedingNumber
    df = df.reindex(['CreditorReference', 'ID', 'PresentationDate', 'StatusAdmited',
                     'DateAdmisionRejected', 'ReasonRejected', 'RequiredSubsanation', 'DateRequiredSubsanation',
                     'SubsanationDone', 'CourtCode', 'ProceedingNumber'], axis=1)

    new_filename = os.path.splitext(file)[0]
    new_filename = new_filename.replace('Legal_', 'Subrogaciones_')
    new_filename = new_filename.replace('legal_', 'Subrogaciones_') + '.csv'
    date_from_filename = new_filename[-12:]
    date_from_filename = date_from_filename[:8]
    day_from_filename = date_from_filename[-2:]
    month_from_filename = date_from_filename[4:6]
    year_from_filename = date_from_filename[:4]
    new_filename = new_filename.split('_')[0] + '_' + new_filename.split('_')[1] + '_' + new_filename.split('_')[2] + '_' + day_from_filename + month_from_filename + year_from_filename
    new_filename = new_filename + '.csv'
    df.to_csv(new_filename, index=False)

#df.to_csv('Subrogaciones_output.csv', index = False)