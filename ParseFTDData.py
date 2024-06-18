import sys
import zipfile
import re

# Example how to run:
# python TrackSkeleton.py "C:\Location\Of\Zip\cnsfails202405b.zip"

def print_symbol_and_volume(splitLines):
    for splitLine in splitLines:
        print(splitLine[0] + ", " + splitLine[2] + ", " + splitLine[3])

def process_zip_file(zip_filepath):
    # Open the zip file
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        # Assuming there is only one file inside the zip file
        file_name = zip_ref.namelist()[0]
        with zip_ref.open(file_name) as file:
            print("Date, Symbol, Volume")
            gmeSplitLines = []
            xrtSplitLines = []
            for line in file:
                line = line.decode('utf-8')
                
                if re.search(r'\|GME\|', line):
                    gmeSplitLines.append(line.split('|'))

                if re.search(r'\|XRT\|', line):
                    xrtSplitLines.append(line.split('|'))

            print_symbol_and_volume(gmeSplitLines)
            print_symbol_and_volume(xrtSplitLines)

if __name__ == "__main__":
    # Check if the script received a filepath argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <zipfile_path>")
        sys.exit(1)
    
    # Get the zip file path from the command-line arguments
    zip_filepath = sys.argv[1]
    process_zip_file(zip_filepath)
