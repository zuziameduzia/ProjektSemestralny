from data_analysis import load_clear_merge, analysis
import run_analysis
import pandas as pd
import numpy as np

def test_load_returns_non_empty_dataframes():
    # przykładowe pliki
    input_file_1 = np.array([[1, 2, 3]])
    input_file_2 = np.array([[4, 5, 6]])
    input_file_3 = np.array([[7, 8, 9]])

    # wywołanie funkcji load
    result = load_clear_merge.load(input_file_1, input_file_2, input_file_3)

    # Sprawdzanie czy df są niepuste
    for df in result:
        assert not df.empty


def test_clear():
    # dane testowe
    df_gdp = pd.DataFrame({"Country Name": ["USA", "Canada", "Mexic"],
                           "GDP": [1, 3, np.nan],
                           "Year": [2, 3, 4]})
    df_number_of_inhabitants = pd.DataFrame({"Country Name": ["USA", "Canad", "Mexico"],
                                             "Number of Inhabitants": [1, 2, np.nan],
                                             "Country Code": [2, 3, 4]})
    df_emission = pd.DataFrame({"Country": ["USA", "Canda", "Mexico"],
                                "Year": [1, 2, 3],
                                "Emission": [2, 3, 4]})
    list_of_df = [df_gdp, df_number_of_inhabitants, df_emission]

    # Oczekiwane wyniki
    expected_df_gdp = pd.DataFrame({"Country Name": ["USA", "Canada", "Mexico"],
                                    "GDP": [1, 3, 2],
                                    "Year": [2, 3, 4]})
    expected_df_number_of_inhabitants = pd.DataFrame({"Country Name": ["USA", "Canada", "Mexico"],
                                                      "Number of Inhabitants": [1, 2, 1.5],
                                                      "Year": [2, 3, 4]})
    expected_df_emission = pd.DataFrame({"Country Name": ["USA", "Canada", "Mexico"],
                                         "Year": [1, 2,3],
                                         "Emission": [2, 3, 4]})
    expected_list_of_df = [expected_df_gdp, expected_df_number_of_inhabitants, expected_df_emission]

    # Wywołanie funkcji i porównanie wyników z oczekiwaniami
    result_list_of_df = load_clear_merge.clear(list_of_df, None, None)
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
        "Year": [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019],
        "Country Name": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        "Total": [20100, 20110, 20120, 20130, 20140, 20150, 20160, 20170, 20180, 20190],
        "Number of Inhabitants": [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        "GDP": [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    })
    #oczekiwane wyniki
    expected_output = [
        pd.DataFrame({
            "Year": [2019, 2018, 2017, 2016, 2015],
            "Country Name": ["J", "I", "H", "G", "F"],
            "CO2 emission per person": [2019, 2018, 2017, 2016, 2015],
            "Total": [20190, 20180, 20170, 20160, 20150]
        }),
        pd.DataFrame({
            "Year": [2019, 2018, 2017, 2016, 2015],
            "Country Name": ["J", "I", "H", "G", "F"],
            "GDP per person": [1000, 900, 800, 700, 600],
            "GDP": [10000, 9000, 8000, 7000, 6000]
        }),
        pd.DataFrame(),
        pd.DataFrame()
    ]
    results = analysis.analysis(data)
    assert all([expected.equals(result) for expected, result in zip(expected_output, results)])



