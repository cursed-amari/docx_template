import re


def sort_list(input_list):
    has_numeric_prefix = any(re.match(r'^\d+', item) for item in input_list)

    if has_numeric_prefix:
        sorted_list = sorted(input_list, key=lambda x: int(re.match(r'^\d+', x).group()))
        return sorted_list
    else:
        return input_list
