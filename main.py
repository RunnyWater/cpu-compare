from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_soup_object():
    url = "https://www.cpubenchmark.net/cpu_list.php"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup
        
def get_search_names():
    input_file_path = 'input.txt'    
    with open(input_file_path, 'r') as input_file:
        search_names = {line.strip().replace('\t', ' ') for line in input_file}
        return search_names


def get_cpu_table(soup):
    table = soup.find(id="cputable")
    return table

def get_table_header_columns(table):
    table_header = table.select_one("thead tr").select('th')
    columns= []
    for header in table_header:
        columns.append(header.text.strip())

    return columns

def get_cpu_info(table, df : pd.DataFrame):
    columns = df.columns
    table_rows = table.select("tbody tr")  
    for row in (table_rows):
        name_link = row.select_one("td a")
        if name_link:
            name = name_link.text.strip()
            if name.strip() in df['CPU Name'].values:
                cpu_values =[value.text.replace(',', '').strip() if ',' in value.text else value.text.strip()  for value in row.select('td')[1:]]
                df.loc[df['CPU Name'] == name.strip(), columns[1:]] = [cpu_values]

    return df
                


def save_to_output_csv(df):
    df.to_csv('output.csv', index=False)
    


if __name__ == "__main__":
    table = get_cpu_table(get_soup_object())
    df_template= pd.DataFrame(columns=get_table_header_columns(table))
    df_template['CPU Name'] = list(get_search_names())
    final_df = get_cpu_info(table, df_template)
    save_to_output_csv(final_df)