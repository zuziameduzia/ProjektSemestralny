from data_analysis import load_clear_merge, analysis
import run_analysis
import pandas as pd
import numpy as np
import os

def test_load():
    input_file_1 = os.path.join(os.path.dirname(__file__), 'test_file_1.csv')
    input_file_2 = os.path.join(os.path.dirname(__file__), 'test_file_2.csv')
    input_file_3 = os.path.join(os.path.dirname(__file__), 'test_file_3.csv')

    result = load_clear_merge.load(input_file_1, input_file_2, input_file_3)

    assert len(result) == 3
    assert isinstance(result[0], pd.DataFrame)
    assert isinstance(result[1], pd.DataFrame)
    assert isinstance(result[2], pd.DataFrame)

def test_clear():
    # dane testowe
    df_gdp = pd.DataFrame({"Country Name": ["United States", "Canada", "Mexic"],
                           'Country Code': ["USA", "Canada", "Mexic"],
                           'Indicator Name': ["USA", "Canada", "Mexic"],
                           'Indicator Code': ["USA", "Canada", "Mexic"],
                           '2010': [1, 2, 3],
                           '2011': [4, 5, 6],
                           'Unnamed: 66': [1, 2, 3]})
    df_number_of_inhabitants = pd.DataFrame({"Country Name": ["United States", "Canada", "Mexic"],
                                             'Country Code': ["USA", "Canada", "Mexic"],
                                             'Indicator Name': ["USA", "Canada", "Mexic"],
                                             'Indicator Code': ["USA", "Canada", "Mexic"],
                                             '2010': [1, 2, 3],
                                             '2011': [4, 5, 6],
                                             'Unnamed: 66': [1, 2, 3]})
    df_emission = pd.DataFrame({"Country": ["United States", "Canda", "Mexico"],
                                'Year': [2010, 2010, 2011],
                                'Country': ["UNITED KINGDOM", "POLAND", "GERMANY"],
                                'Total': [1, 2, 3],
                                'Solid Fuel': [1, 2, 3],
                                'Liquid Fuel': [1, 2, 3],
                                'Gas Fuel': [1, 2, 3],
                                'Cement': [1, 2, 3],
                                'Gas Flaring': [1, 2, 3],
                                'Per Capita': [1, 2, 3],
                                'Bunker fuels (Not in Total)': [0, 0, 0]})
    list_of_df = [df_gdp, df_number_of_inhabitants, df_emission]

    # Oczekiwane wyniki
    expected_df_gdp = pd.DataFrame({"Country Name": ["United States", "Canada", "Mexico","United States", "Canada", "Mexico"],
                          'Year':[2010, 2010, 2010, 2011, 2011, 2011],
                          'GDP':[1,2,3,4,5,6]})
    expected_df_number_of_inhabitants = pd.DataFrame({"Country Name": ["United States", "Canada", "Mexico", "United States", "Canada", "Mexico"],
                          'Year':[2010, 2010, 2010, 2011, 2011, 2011],
                          'Number of Inhabitants':[1,2,3,4,5,6]})
    expected_df_emission =pd.DataFrame({'Country Name': ["United Kingdom", "Poland", "Germany"],
                                'Year': [2010, 2010, 2011],
                               'Total': [1,2,3],
                               'Solid Fuel' :[1,2,3],
                               'Liquid Fuel' :[1,2,3],
                               'Gas Fuel' :[1,2,3],
                               'Cement':[1,2,3],
                               'Gas Flaring' : [1,2,3],
                               'Per Capita': [1,2,3],
                               'Bunker fuels (Not in Total)': [0,0,0]})
    expected_list_of_df = [expected_df_gdp, expected_df_number_of_inhabitants, expected_df_emission]

    # Wywołanie funkcji i porównanie wyników z oczekiwaniami
    result_list_of_df = load_clear_merge.clear(list_of_df, 2010, 2011)
    for i in range(3):
        pd.testing.assert_frame_equal(result_list_of_df[i], expected_list_of_df[i])


def test_merge():
    #dane testowe
    df_gdp = pd.DataFrame({'Country Name': ['A', 'B', 'C'], 'Year': [2010, 2011, 2012], 'Total': [100, 200, 300]})
    df_number_of_inhabitants = pd.DataFrame(
        {'Country Name': ['A', 'B', 'C'], 'Year': [2010, 2011, 2012], 'Number of Inhabitants': [10, 20, 30]})
    df_emission = pd.DataFrame({'Country Name': ['A', 'B', 'C'], 'Year': [2010, 2011, 2012], 'Emission': [1, 2, 3]})
    list_input = [df_gdp, df_number_of_inhabitants, df_emission]
    # wywołanie funkcji
    result = load_clear_merge.merge(list_input)
    # oczekiwany wynik
    expected_output = pd.DataFrame(
        {'Country Name': ['A', 'B', 'C'], 'Year': [2010, 2011, 2012], 'Total': [100, 200, 300],
         'Number of Inhabitants': [10, 20, 30], 'Emission': [1, 2, 3]})
    #porównanie wyników z oczekiwanymi
    pd.testing.assert_frame_equal(result, expected_output)



def test_analysis():
    #dane testowe

    data = pd.DataFrame({
        "Year": [2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2010, 2000, 2000, 2000, 2000, 2000, 2000, 2000,
                 2000, 2000, 2000],
        "Country Name": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "A", "B", "C", "D", "E", "F", "G", "H", "I","J"],
        "Total": [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
        "Number of Inhabitants": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "GDP": [200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200]
    })

    results = analysis.analysis(data)
    assert len(results) == 4
    assert isinstance(results[0], pd.DataFrame)
    assert isinstance(results[1], pd.DataFrame)
    assert isinstance(results[2], pd.Series)
    assert isinstance(results[3], pd.Series)