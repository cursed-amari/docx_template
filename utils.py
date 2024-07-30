import os
import re
import pandas as pd


def check_folders():
    if not os.path.exists('./templates'):
        os.mkdir('./templates')
    if not os.path.exists('./templates/data.xlsx'):
        headers = ['Должность', 'ФИО']
        new_df = pd.DataFrame(columns=headers)
        new_file_path = './templates/data.xlsx'
        new_df.to_excel(new_file_path, index=False)
    if not os.path.exists('./result'):
        os.mkdir('./result')


def sort_list(input_list):
    has_numeric_prefix = any(re.match(r'^\d+', item) for item in input_list)

    if has_numeric_prefix:
        sorted_list = sorted(input_list, key=lambda x: int(re.match(r'^\d+', x).group()))
        return sorted_list
    else:
        return input_list


def get_data_dict():
    file_path = './templates/data.xlsx'
    sheet_name = 'Sheet1'

    df = pd.read_excel(file_path)

    data_dict = {}

    for index, row in df.iterrows():
        key = row.iloc[0]
        value = row.iloc[1]

        if key in data_dict.keys():
            data_dict[key].append(value)
        else:
            data_dict[key] = [value]

    return data_dict
