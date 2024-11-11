from bs4 import BeautifulSoup
import requests

def initialize():
    url = "https://www.cpubenchmark.net/cpu_list.php"
    response = requests.get(url)
    input_file_path = 'input.txt'    
      

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        with open(input_file_path, 'r') as input_file:
            search_names = {line.strip().replace('\t', ' ') for line in input_file}
            return (search_names, soup)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

def get_cpu_data(search_names, soup):
    output_file_path = 'output.csv'
    table = soup.find(id="cputable")
    if not table:
        print("Table with ID 'cputable' not found in the HTML file.")
    else:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            text_header = get_text_header(table)
            output_file.write(f"{text_header}\n")
            table_rows = table.select("tbody tr")  
            if not table_rows:
                print("No rows found in the table's <tbody>.")
            else:
                for row in (table_rows):
                    name_link = row.select_one("td a")
                    if name_link:
                        name = name_link.text.strip()
                        if name.strip() in search_names:
                            line_row = f'{name.strip()}'
                            cpu_values = row.select('td')[1:]
                            for cpu_value in cpu_values:
                                line_row = line_row + "," + cpu_value.text.replace(',', '')
                            output_file.write(f"{line_row.replace('\t', ' ').replace('\n', '')}\n")

def get_text_header(table):
    table_header = table.select_one("thead tr").select('th')
    text_header = table_header[0].text
    for header in table_header[1:]:
        if '\n' in header.text:
            text_header += ','+header.text.strip().split('\n')[0]
        else: text_header += ','+header.text.strip()

    return text_header

get_cpu_data( *initialize() )


print("Process completed. Check the output file for results.")
