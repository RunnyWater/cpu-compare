from bs4 import BeautifulSoup

# File paths
cpu_file_path = 'cpu_file.php'   # Local HTML file with CPU data
input_file_path = 'input.txt'    # Text file with input names to search for
output_file_path = 'output.csv'  # Output file to save matching <tr> elements

# Load the CPU data from the file
with open(cpu_file_path, 'r', encoding='utf-8') as cpu_file:
    soup = BeautifulSoup(cpu_file, 'html.parser')

# Load the input names
with open(input_file_path, 'r') as input_file:
    search_names = {line.strip().replace('\t', ' ') for line in input_file}

# Open the output file
def get_cpu_data():

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        # Find all <tr> elements within the table with ID 'cputable'
        table = soup.find(id="cputable")
        
        # Check if the table was found
        if not table:
            print("Table with ID 'cputable' not found in the HTML file.")
        else:
            table_header = table.select_one("thead tr").select('th')
            text_header = table_header[0].text
            for header in table_header[1:]:
                if '\n' in header.text:
                    text_header += ','+header.text.strip().split('\n')[0]
                else: text_header += ','+header.text.strip()

            output_file.write(f"{text_header}\n")


            table_rows = table.select("tbody tr")  # Locate rows within the table's <tbody>
            
            # Ensure we have rows to process
            if not table_rows:
                print("No rows found in the table's <tbody>.")
            else:
                for row in (table_rows):
                    # Find the <a> tag within the first <td> of each row
                    name_link = row.select_one("td a")

                    if name_link:
                        name = name_link.text.strip()
                        # Check if the name matches any in the search list
                        if name.strip() in search_names:
                            # Write the entire <tr> element HTML to the output file
                            line_row = f'{name.strip()}'
                            cpu_values = row.select('td')[1:]
                            for cpu_value in cpu_values:
                                line_row = line_row + "," + cpu_value.text.replace(',', '')
                            output_file.write(f"{line_row.replace('\t', ' ').replace('\n', '')}\n")
                            # output_file.write(f"{name_link, row.select('td')}\n\n")
get_cpu_data()

print("Process completed. Check the output file for results.")
