import os
import glob
import sys
from ProcessZip import process_zip_file

def get_zip_files(directory):
    zip_files = glob.glob(os.path.join(directory, '*.zip'))
    return zip_files

def main():

    # Parse the command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python script.py <zipfile_path>")
        sys.exit(1)
    
    zip_files = get_zip_files(sys.argv[1])

    csv = []
    csv.append("Zip File, Date, Symbol, Volume")
    # Print the full paths of the zip files
    for zip_file in zip_files:
        print("zip File: " + zip_file)
        csv.extend(process_zip_file(zip_file))

    with open('output.txt', 'w') as output_file:
        for line in csv:
            output_file.write(line + "\n")

if __name__ == "__main__":
    main()
