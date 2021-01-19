"""
Helper functions for pre-processing data
"""
import email
from itertools import chain
import pandas as pd
import numpy as np


def get_email_from_string(raw_email):
    """
    Input:
        String
    Function:
        Extracts header and contant information from a string representing a
        MIME type email. Converts the header information to keys and the
        respective content as values and returns a dictionary.
    Output:
        Dictionary
    """

    msg = email.message_from_string(raw_email)

    content = []
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            content.append(part.get_payload())

    result = {}
    for key in msg.keys():
        result[key] = msg[key]
    result["content"] = ''.join(content)

    return result


def prep_dataframe(df):
    """
    Input:
        DataFrame
    Function:
        - Extracts columns "From", "To", "Cc" and "Bcc" from original DataFrame
          to a new DataFrame
        - Merges columns "To", "Cc" and "Bcc" in new DataFrame to new column
          "recipients"
        - Renames column "From" to "sender" in new DataFrame
        - Drops columns "To", "Cc" and "Bcc" from new DataFrame
    Output:
        DataFrame
    """

    df_short = df[['From', 'To', 'Cc', 'Bcc']]

    df_short['recipients'] = df_short[df_short.columns[1:]].apply(
        lambda x: ','.join(x.dropna()), axis=1)

    df_short = df_short.rename(columns={'From': 'sender',
                                        'X-Origin': 'email_account',
                                        'Date': 'date'})

    df_short.drop(columns=['To', 'Cc', 'Bcc'], inplace=True)

    df_short['recipients'].str.replace(' \n\t', '')

    df_short = df_short[['sender', 'recipients']]

    return df_short


def get_pairwise_communication(df_col1, df_col2):
    """
    Input:
        DataFrame columns
    Function:
        If recipient column contains multiple recipients, extracts individual
        recipients from recipient column and matches row-wise with respective
        sender. Returns a DataFrame.
    Output:
        DataFrame
    """

    result_df = pd.DataFrame({"sender": np.repeat(df_col1.values,
                                                  df_col2.str.len()),
                              "recipient": list(chain.from_iterable(df_col2))})

    return result_df
