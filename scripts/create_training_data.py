import requests
import lxml.html as lh
import os.path
import urllib
import zipfile
import glob
import operator
import glob

def get_dictionary_of_words(list_of_words_path):
    """Method that retrieves the dictionary.txt file and turns it into a list.

    Args:
        list_of_words_path (string): The location of the dictionary.txt file on the local machine.

    Returns:
        array: Array of words extracted from dictionary.txt file that was imported.

    """
    dictionary = []
    with open(list_of_words_path, "r") as filestream:
        for line in filestream:
            currentline = line.split(",")
            for word in currentline:
                dictionary.append(word.rstrip())
    return dictionary


def get_list_gdelt_files():
    """Method that retrieves the dictionary.txt file and turns it into a list.

    Args:
        list_of_words_path (string): The location of the dictionary.txt file on the local machine.

    Returns:
        array: Array of words extracted from dictionary.txt file that was imported.

    """
    page = requests.get(gdelt_base_url + 'index.html')
    doc = lh.fromstring(page.content)
    link_list = doc.xpath("//*/ul/li/a/@href")
    # Filter to those that we can read
    return [x for x in link_list if str.isdigit(x[0:4])]


def download_compressed_file(compressed_file):
    """Method that downloads a given compressed GDELT file

    Args:
        compressed_file (string): The name of the compressed file to download from the GDELT index.

    Returns:
        void

    """
    # if we dont have the compressed file stored locally, go get it. Keep trying if necessary.
    while not os.path.isfile(local_path + compressed_file):
        print 'downloading file,',
        urllib.urlretrieve(url=gdelt_base_url + compressed_file,
                           filename=local_path + compressed_file)


def extract_compressed_file(downloaded_file):
    """Method that extracts/unzips a compressed file

    Args:
        downloaded_file (string): The name of the compressed file that has been downloaded.

    Returns:
        compressed_file (string): The name of the compressed file

    """
    # extract the contents of the compressed file to a temporary directory
    print 'extracting file,',
    z = zipfile.ZipFile(file=local_path + compressed_file, mode='r')
    z.extractall(path=local_path + 'tmp/')
    return compressed_file

# Parse the extracted GDELT file to a CSV file


def parse_file_to_csv(extracted_file):
    # parse each of the csv files in the working directory,
    print 'parsing file'
    # remove .zip from name so we
    extracted_file = extracted_file[:-4]
    extracted_file_path = local_path + 'tmp/' + extracted_file
    # open the infile and outfile
    with open(extracted_file_path, mode='r') as infile, open(outfile_name, mode='w') as outfile:
        for line in infile:
            # extract lines with our interest country code
            if fips_country_code in operator.itemgetter(51, 37, 44)(line.split('\t')):
                # extract lines with our interest key words
                if any(word in operator.itemgetter(57)(line.split('\t')) for word in list_of_words):
                    outfile.write(line)

# Local configuration
local_path = '/Users/sam/Desktop/GDELT_Data/'
outfile_name = '/Users/sam/Desktop/training_data.csv'

# What is being looked for
fips_country_code = 'US'
list_of_words_path = '/Users/sam/Desktop/dictionary.txt'
list_of_words = get_dictionary_of_words(list_of_words_path)

# GDELT configuration
gdelt_base_url = 'http://data.gdeltproject.org/events/'
list_of_files = get_list_gdelt_files()

# Go through the last month of files.
for x in range(0, 200):
    compressed_file = list_of_files[x]
    # unzip the file.
    parse_file_to_csv(extract_compressed_file(download_compressed_file(compressed_file)))
