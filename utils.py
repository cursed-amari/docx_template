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


def sort_list(input_list: list) -> list:
    """
    Сортировка листа по первому числу\n
    :param input_list:
    :return: list
    """
    has_numeric_prefix = any(re.match(r'^\d+', item) for item in input_list)

    if has_numeric_prefix:
        sorted_list = sorted(input_list, key=lambda x: int(re.match(r'^\d+', x).group()))
        return sorted_list
    else:
        return input_list


def get_data_dict() -> dict:
    """
    Получить данные из data и преобразовать в dict  \n
    key первый столбец  \n
    value второй столбец  \n
    Если key повторяется то value идёт в list к тому же key  \n
    Если одна из строк в столбце пустая она будет записана как nan \n
    :return: dict
    """
    file_path = './templates/data.xlsx'

    df = pd.read_excel(file_path)

    data_dict = {}

    for index, row in df.iterrows():
        key = row.iloc[0]
        value = row.iloc[1]

        if key in data_dict.keys():
            data_dict[str(key)].append(str(value))
        else:
            data_dict[str(key)] = [str(value)]

    return data_dict
