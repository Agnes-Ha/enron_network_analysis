"""
Pre-processes the data for subsequent network analysis
"""

import pandas as pd
from utils import get_email_from_string, prep_dataframe, get_pairwise_communication

# Load in data
df = pd.read_csv('./data/emails.csv')

# Pre-process complete dataset
#df_parsed = pd.DataFrame(list(map(get_email_from_string, df['message'])))

# Subset emails in sent folders only
sent = df.loc[df['file'].str.contains('sent')]

# From sent subset extract and process emails of Kaminski
kaminski = sent.loc[sent['file'].str.contains('kaminski-v')]
kaminski_parsed = pd.DataFrame(
    list(map(get_email_from_string, kaminski['message'])))
kaminski_parsed.dropna(subset=['To'], inplace=True)
kaminski_parsed.to_csv('./data/kaminski_parsed.csv', index=False)

kaminski_comm = prep_dataframe(kaminski_parsed)
kaminski_comm['recipients'] = kaminski_comm['recipients'].apply(
    lambda x: x.split(','))

kaminski_full = get_pairwise_communication(
    kaminski_comm['sender'], kaminski_comm['recipients'])
kaminski_full['recipient'] = kaminski_full['recipient'].str.strip(' \n\t')

kaminski_sender = kaminski_full[kaminski_full['sender'].str.contains(
    'vince.kaminski.enron.com|j.kaminski@enron.com')]
to_kaminski = kaminski_full[kaminski_full['recipient'].str.contains(
    'vince.kaminski.enron.com|j.kaminski@enron.com')]

to_kaminski_edges = to_kaminski.value_counts(['sender', 'recipient'])
to_kaminski_edges = to_kaminski_edges.reset_index()
to_kaminski_edges = to_kaminski_edges.rename(columns={0: 'num_emails'})
to_kaminski_edges.to_csv('./data/to_kaminski_edges.csv', index=False)

kaminski_edges = kaminski_sender.value_counts(['sender', 'recipient'])
kaminski_edges = kaminski_edges.reset_index()
kaminski_edges = kaminski_edges.rename(columns={0: 'num_emails'})
kaminski_edges.dropna(subset=['recipient'], inplace=True)
kaminski_edges.to_csv('./data/kaminski_edges.csv', index=False)
