from gdelt_wrapper import get_dictionary_of_words, get_latest_gdelt_file, get_all_training_dataset, get_list_gdelt_files ,download_compressed_file, extract_compressed_file, parse_file_to_csv
import argparse

def build_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all", help="process all CSV files",
                    action="store_true")
    return parser


def download_all_training():
    compressed_files = get_all_training_dataset()
    x = 1
    # Go through the last month of files.
    for compressed in compressed_files:
        print x
        download_compressed_file(local_path,compressed)
        extract_compressed_file(local_path,compressed)
        parse_file_to_csv(local_path,outfile_name,compressed,fips_country_code,list_of_words)
        x = x + 1

def download_latest_training():
    latest_compressed_file = get_latest_gdelt_file()
    download_compressed_file(local_path,latest_compressed_file)
    extract_compressed_file(local_path,latest_compressed_file)
    parse_file_to_csv(local_path,outfile_name,latest_compressed_file,fips_country_code,list_of_words)

if __name__ == "__main__":

    parser = build_args()
    args = parser.parse_args()

    # Local configuration
    local_path = '/Users/sam/Desktop/GDELT_Data/'
    outfile_name = '/Users/sam/Desktop/training_data.csv'

    # What is being looked for
    fips_country_code = 'US'
    list_of_words_path = '/Users/sam/Desktop/dictionary.txt'
    list_of_words = get_dictionary_of_words(list_of_words_path)

    # GDELT configuration
    list_of_files = get_list_gdelt_files()

    if args.all:
        articles = download_all_training()
    else:
        articles = download_latest_training()
