import numpy as np
import re

TABLE_STYLE = \
"""background-color: rgba(0, 0, 0, 0);
border-bottom-color: rgb(0, 0, 0);
border-bottom-style: none;
border-bottom-width: 0px;
border-collapse: collapse;
border-image-outset: 0px;
border-image-repeat: stretch;
border-image-slice: 100%;
border-image-source: none;
border-image-width: 1;
border-left-color: rgb(0, 0, 0);
border-left-style: none;
border-left-width: 0px;
border-right-color: rgb(0, 0, 0);
border-right-style: none;
border-right-width: 0px;
border-top-color: rgb(0, 0, 0);
border-top-style: none;
border-top-width: 0px;
box-sizing: border-box;
color: rgb(0, 0, 0);
display: table;
font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
font-size: 12px;
height: 1675px;
line-height: 20px;
margin-left: 0px;
margin-right: 0px;
margin-top: 12px;
table-layout: fixed;
text-size-adjust: 100%;
width: 700px;
-webkit-border-horizontal-spacing: 0px;
-webkit-border-vertical-spacing: 0px;
-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"""

def style_table(df):
    """
    Transform the DataFrame into an HTML table with custom styling.

    :param df: dataframe to be styled
    :type  df: `pd.DataFrame`

    :return: HTML code with styling
    :rtype:  str
    """
    # define the css style for the table
    table_style = '<style>table {{{}}}</style>'.format(TABLE_STYLE)

    # convert dataframe to html
    df_html = df.to_html(index=False, escape=False)

    # generate a random id for the table
    random_id = 'id%d' % np.random.choice(np.arange(1000000))

    # modify the css style to apply to the specific table
    new_style = []
    for line in table_style.split('\n'):
        line = line.strip()
        if not re.match(r'^table', line):
            line = re.sub(r'^', 'table ', line)
        new_style.append(line)
    new_style = ['<style>'] + new_style + ['</style>']
    table_style = re.sub(r'table(#\S+)?', 'table#%s' % random_id, '\n'.join(new_style))

    # add the table id to the html table
    df_html = re.sub(r'<table', r'<table id=%s ' % random_id, df_html)

    # combine the css style and html table
    styled_table = table_style + df_html
    return styled_table


def read_error_messages_from_log_file(file_path):
    """
    Read error messages from a log file.

    :param file_path: The path to the log file.
    :type file_path: str
    :return: A list of error messages extracted from the log file.
    :rtype: list
    """
    error_messages = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # use regular expression to search for error or failure
                # messages
                match = re.search(r'(error|failure|failed)', line, re.IGNORECASE)
                if match:
                    error_messages.append(line.strip())
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return error_messages
