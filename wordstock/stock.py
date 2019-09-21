from argparse import ArgumentParser
from tabulate import tabulate
import datetime
import glob
import logging
import os
import pandas as pd
import sys
import time


def build_argparser():
    """
    WordStock command line parser
    :return: parser built by the function
    """
    parser = ArgumentParser(description='Gather products from other repos')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable debug logging')
    parser.add_argument('-i', '--datadir', type=str,
                        help='''Input the directory location to find the
                            dataset. Wordstock looksup at all text files
                            (.txt extension) in this directory as dataset.
                            This is a mandatory parameter''', required=True)
    parser.add_argument('-p', '--seeddir', type=str,
                        help='''Input the directory location to find the
                            word patterns to be tracked. Wordstock sees all
                            text files (.txt extension) in this directory as
                            dataset. This is a mandatory parameter''',
                        required=True)
    parser.add_argument('-f', '--outputformat', type=str,
                        choices=["csv", "json"],
                        help='''Output format - csv, or json''',
                        required=True)
    parser.add_argument('-o', '--outputdir', type=str,
                        help='''Input the directory location to store the
                            Wordstock file output. This is a mandatory
                            parameter''',
                        required=True)
    return parser


def build_frame(input_dir, frame_name):
    """
    Build pandas dataframe
    :param input_dir: Directory containing the dataset used to form the frame
    :param frame_name: Column name to store in the frame to denote dataset
    :return: pandas dataframe built from input files
    """
    input_dir.rstrip("/")
    files = glob.glob(input_dir + '/*.txt')
    file_data = list()
    for file in files:
        with open(file, encoding='utf-8') as f:
            file_name = os.path.basename(file.split('.')[0])
            try:
                file_data.append(pd.DataFrame(
                    {frame_name: file_name,
                     'lines': f.readlines()}))
            except UnicodeDecodeError:
                logging.warning("Unicode decode error on file " + file_name)
                continue
    if len(file_data) > 0:
        file_doc = pd.concat(file_data)
        file_doc['words'] = file_doc.lines.str.strip().str.split('[\\W_]+')
        rows = file_doc.explode('words')
        frame = pd.DataFrame(rows, columns=[frame_name, 'words'])
        frame = frame[frame.words.str.len() > 0]
        return frame
    else:
        return None


def get_unique_words(frame):
    """
    Get a list of unique words from frame
    :param frame:
    :return:
    """
    return frame.words.unique().tolist()


def write_output(frame, output_dir, output_format):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_file = \
        output_dir + "/out_" + \
        str(datetime.datetime.now().strftime("%Y_%m_%d_TIME_%H_%M_%S")) \
        + "." + output_format
    with open(output_file, 'w'):
        if output_format == "csv":
            frame.to_csv(output_file)
        elif output_format == "json":
            frame.to_json(output_file)
        else:
            logging.warning("Unknown output format " + output_format)
    print(tabulate(frame, headers='keys', tablefmt='psql'))


def check_dir(input_dirs):
    """
    Test sanity of input
    :param input_dirs:
    """
    if input_dirs:
        for directory in input_dirs:
            if not os.path.isdir(directory):
                logging.error("Directory not found" + directory)
                logging.error("Please check the test input directories")
                sys.exit(1)


def get_word_count(frame, pattern_list, group_by_name):
    """
    Compute word count and return a dataframe
    :param frame:
    :param pattern_list:
    :param column_name:
    :return: frame with count or None if pattern_list is empty
    """
    if not pattern_list or len(pattern_list) == 0:
        return None
    else:
        return pd.DataFrame(frame[frame.words.isin(pattern_list)].
                            groupby(group_by_name).words.value_counts()
                            .to_frame())


def main():
    """
    WordStock - Main method
    """
    # Build WordStock input parser
    parser = build_argparser()

    # Retrieve input arguments
    ns = parser.parse_args()
    pattern_dir = ns.seeddir
    data_dir = ns.datadir
    output_dir = ns.outputdir

    # Check Test input sanity
    check_dir([data_dir, pattern_dir])

    # Build pattern and data frames
    pattern_list = []
    pattern_frame = build_frame(pattern_dir, "word_pattern")
    if pattern_frame is not None:
        pattern_list = get_unique_words(pattern_frame)
    if len(pattern_list) == 0:
        logging.error("Pattern list is empty."
                      "Please provide test data to take WordStock")
        sys.exit(1)
    data_frame = build_frame(data_dir, "data_set")
    if data_frame is None:
        logging.error("Data set is empty. "
                      "Please provide test data to take WordStock")
        sys.exit(1)

    # Get word count
    count_frame = get_word_count(data_frame, pattern_list, "data_set")
    if count_frame is not None:
        write_output(count_frame, output_dir, ns.outputformat)
    else:
        logging.info("Requested word patterns not found in the given data set")


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print("Execution Time: " + str(end - start))
