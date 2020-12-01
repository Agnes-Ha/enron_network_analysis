"""
Pre-processes the data for network analysis
"""

import pandas as pd
#import numpy as np
#import re
#import email
#import itertools
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

lay_comm = prep_dataframe(lay_parsed)
lay_comm['recipients'] = lay_comm['recipients'].apply(
    lambda x: x.split(','))

lay_full = get_pairwise_communication(
    lay_comm['sender'], lay_comm['recipients'])
lay_full['recipient'] = lay_full['recipient'].str.strip(' \n\t')

print(lay_full['sender'].unique())

lay_sender = lay_full[lay_full['sender'].str.contains(
    'kenneth.lay@enron.com|klay@enron.com')]

lay_edges = lay_sender.value_counts(['sender', 'recipient'])
lay_edges = lay_edges.reset_index()
lay_edges = lay_edges.rename(columns={0: 'num_emails'})
lay_edges.to_csv('./data/lay_edges.csv', index=False)

# Process emails of Jeffrey Skilling
skilling = sent.loc[sent['file'].str.contains('skilling-j')]
skilling_parsed = pd.DataFrame(
    list(map(get_email_from_string, skilling['message'])))

skilling_comm = prep_dataframe(skilling_parsed)
skilling_comm['recipients'] = skilling_comm['recipients'].apply(
    lambda x: x.split(','))

skilling_full = get_pairwise_communication(
    skilling_comm['sender'], skilling_comm['recipients'])
skilling_full['recipient'] = skilling_full['recipient'].str.strip(' \n\t')

print(skilling_full['sender'].unique())

skilling_sender = skilling_full[skilling_full['sender'].str.contains(
    'jeff.skilling@enron.com')]

skilling_edges = skilling_sender.value_counts(['sender', 'recipient'])
skilling_edges = skilling_edges.reset_index()
skilling_edges = skilling_edges.rename(columns={0: 'num_emails'})
skilling_edges.to_csv('./data/skilling_edges.csv', index=False)

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

kaminski_edges = kaminski_sender.value_counts(['sender', 'recipient'])
kaminski_edges = kaminski_edges.reset_index()
kaminski_edges = kaminski_edges.rename(columns={0: 'num_emails'})
kaminski_edges.to_csv('./data/kaminski_edges.csv', index=False)
