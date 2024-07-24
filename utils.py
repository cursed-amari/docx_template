import re
from docx import Document


def parse_docx(doc: Document):
    pattern = re.compile(r'\{param: (\d+)\}')

    found_params = set()

    for para in doc.paragraphs:
        matches = pattern.findall(para.text)
        for match in matches:
            found_params.add(f'param: {match}')

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                matches = pattern.findall(cell.text)
                for match in matches:
                    found_params.add(f'param: {match}')

    return found_params


def sort_list(input_list):
    has_numeric_prefix = any(re.match(r'^\d+', item) for item in input_list)

    if has_numeric_prefix:
        sorted_list = sorted(input_list, key=lambda x: int(re.match(r'^\d+', x).group()))
        return sorted_list
    else:
        return input_list
