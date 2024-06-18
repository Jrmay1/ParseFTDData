import sys
import zipfile
import re

def get_date_symbol_and_volume(splitLines, file_name):
    result = []
    for splitLine in splitLines:
        result.append(f"{file_name}, {splitLine[0]}, {splitLine[2]}, {splitLine[3]}")
    return result

def process_zip_file(zip_filepath):
    csv = []
    try:
        # Open the zip file
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            # Check if there is at least one file inside the zip file
            if len(zip_ref.namelist()) == 0:
                print("The zip file is empty.")
                return
            
            # Assuming there is only one file inside the zip file
            file_name = zip_ref.namelist()[0]
            with zip_ref.open(file_name) as file:
                gmeSplitLines = []
                xrtSplitLines = []
                for line in file:
                    try:
                        line = line.decode('utf-8')
                        
                        if re.search(r'\|GME\|', line):
                            gmeSplitLines.append(line.split('|'))

                        if re.search(r'\|XRT\|', line):
                            xrtSplitLines.append(line.split('|'))

                    except UnicodeDecodeError as e:
                        if b'GME' in line or b'XRT' in line:
                            print(f"Error decoding line: {line} due to: {e}")
                        continue

                csv.extend(get_date_symbol_and_volume(gmeSplitLines, file_name))
                csv.extend(get_date_symbol_and_volume(xrtSplitLines, file_name))
    except zipfile.BadZipFile:
        print("Error: The file is not a valid zip file.")
    except FileNotFoundError:
        print(f"Error: The file {zip_filepath} was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return csv

if __name__ == "__main__":
    # Check if the script received a filepath argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <zipfile_path>")
        sys.exit(1)
    
    # Get the zip file path from the command-line arguments
    zip_filepath = sys.argv[1]
    csv = []              
    csv.append("Zip File, Date, Symbol, Volume")

    csv.append(process_zip_file(zip_filepath))

    with open('output.txt', 'w') as output_file:
        for line in csv:
            output_file.write(line + "\n")
