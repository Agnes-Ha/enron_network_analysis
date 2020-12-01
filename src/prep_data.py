"""
Pre-processes the data for network analysis
"""

import pandas as pd
import numpy as np
import re
import email
import itertools
from utils import get_email_from_string, prep_dataframe, get_pairwise_communication

# Load in data
df = pd.read_csv('./data/emails.csv')

# Pre-process complete dataset
df_parsed = pd.DataFrame(list(map(get_email_from_string, df['message'])))
print(df_parsed.info())
print(df_parsed.describe())
print(df_parsed['X-Origin'].value_counts())


# Subset emails in sent folders only
sent = df.loc[df['file'].str.contains('sent')]

# From sent subset extract and process emails of specific persons: 
# Process emails of Kenneth Lay
lay = sent.loc[sent['file'].str.contains('lay-k')]
lay_parsed = pd.DataFrame(list(map(get_email_from_string, lay['message'])))


# Process emails of Jeffrey Skilling
skilling = sent.loc[sent['file'].str.contains('skilling-j')]
skilling_parsed = pd.DataFrame(
    list(map(get_email_from_string, skilling['message'])))


# Process emails of Vincent J. Kaminski
kaminski = sent.loc[sent['file'].str.contains('kaminski-v')]
kaminski_parsed = pd.DataFrame(
    list(map(get_email_from_string, kaminski['message'])))

print(kaminski_parsed.describe())

kaminski_comm = prep_dataframe(kaminski_parsed)
kaminski_comm['recipients'] = kaminski_comm['recipients'].apply(
    lambda x: x.split(','))

kaminski_full = get_pairwise_communication(
    kaminski_comm['sender'], kaminski_comm['recipients'])
kaminski_full['recipient'] = kaminski_full['recipient'].str.strip(' \n\t')

kaminski_sender = kaminski_full[kaminski_full['sender'].str.contains(
    'vince.kaminski.enron.com|j.kaminski@enron.com')]

edges = kaminski_sender.value_counts(['sender', 'recipient'])
edges = edges.reset_index()
edges = edges.rename(columns={0: 'num_emails'})


