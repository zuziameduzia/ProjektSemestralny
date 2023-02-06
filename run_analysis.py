import argparse
from data_analysis import load_clear_merge, analysis



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("GDP", help="Enter the path to the GDP file")
    parser.add_argument("number_of_inhabitants", help="Enter the path to the file with numer of inhabitants")
    parser.add_argument("co2_emissions", help="Enter the path to the CO2 emissions file")
    parser.add_argument("start_year", help="Enter the year from which you are interested in the analysis")
    parser.add_argument("stop_year", help="Enter the year to which you are interested in the analysis")
    args = parser.parse_args()
    assert args.start_year <= args.stop_year, "Incorrect data"
    input_file_1 = args.GDP
    input_file_2 = args.number_of_inhabitants
    input_file_3 = args.co2_emissions
    start_year = args.start_year
    stop_year = args.stop_year
    start_year = int(start_year)
    stop_year = int(stop_year)
    input_data = load_clear_merge.load(input_file_1, input_file_2, input_file_3)
    data_for_analysis = load_clear_merge.clear(input_data, start_year, stop_year)
    merged_data = load_clear_merge.merge(data_for_analysis)
    results = analysis.analysis(merged_data)
    print(results)

if __name__ == '__main__':
        main()