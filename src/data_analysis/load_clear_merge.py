import pandas as pd
from fuzzywuzzy import process
from pycountry import countries


def load(input_file_1, input_file_2, input_file_3):
    # wczytanie 1 pliku
    df_gdp = pd.read_csv(input_file_1, skiprows=4)
    # wczytanie 2 pliku
    df_number_of_inhabitants = pd.read_csv(input_file_2, skiprows=4)
    # wczytanie 3 pliku
    df_emission = pd.read_csv(input_file_3)
    list = [df_gdp, df_number_of_inhabitants, df_emission]
    return list
def clear(list_of_df, start_year, stop_year):
    df_gdp = list_of_df[0]
    df_number_of_inhabitants = list_of_df[1]
    df_emission = list_of_df[2]
    # usuwanie ostatniej kolumny i kolumny Country Code, Indicator Name, Code
    df_gdp = df_gdp.drop('Unnamed: 66', axis=1)
    df_gdp = df_gdp.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code'], axis=1)
    # zmienianie braków danych na średnią z danej kolumny
    for column_name in df_gdp.columns[1:]:
        df_gdp[column_name] = df_gdp[column_name].fillna(value=df_gdp[column_name].mean())
    # usuwanie niekrajów i poprawianie literówek w kolumnie Country Name
    country = [c.name for c in countries]
    def correct_country(row):
        match = process.extractOne(row['Country Name'], country)
        if match[1] > 80:  # Próg dopasowania
            return match[0]
        else:
            return None
    #zmienianie None na średnią wartość
    df_gdp['Country Name'] = df_gdp.apply(correct_country, axis=1)
    df_gdp.dropna(subset=['Country Name'], inplace=True)
    #czyszczenie 2 pliku, robimy dokładnie to samo co z pierwszym
    df_number_of_inhabitants = df_number_of_inhabitants.drop('Unnamed: 66', axis=1)
    df_number_of_inhabitants = df_number_of_inhabitants.drop(
        columns=['Country Code', 'Indicator Name', 'Indicator Code'], axis=1)
    for column_name in df_number_of_inhabitants.columns[1:]:
        df_number_of_inhabitants[column_name] = df_number_of_inhabitants[column_name].fillna(
            value=df_number_of_inhabitants[column_name].mean())
    df_number_of_inhabitants['Country Name'] = df_number_of_inhabitants.apply(correct_country, axis=1)
    df_number_of_inhabitants.dropna(subset=['Country Name'], inplace=True)
    #czyszczenie 3 pliku
    df_emission["Country"] = df_emission["Country"].str.title()
    df_emission.rename(columns={"Country": "Country Name"}, inplace=True)
    for column_name in df_emission.columns[2:]:
        df_emission[column_name] = df_emission[column_name].fillna(value=df_emission[column_name].mean())
    df_emission['Country Name'] = df_emission.apply(correct_country, axis=1)
    df_emission.dropna(subset=['Country Name'], inplace=True)
    # tworzenie df z danych z lat i usuwanie duplikatów (mamy 3 df):
    gdp_years = df_gdp.columns[1:]
    gdp_years = gdp_years.astype('int64')
    df_gdp_years = pd.DataFrame({'Year': gdp_years})
    df_gdp_years = df_gdp_years.drop_duplicates()
    # print(df_gdp_years)
    number_of_inhabitants_years = df_number_of_inhabitants.columns[1:]
    number_of_inhabitants_years = number_of_inhabitants_years.astype('int64')
    df_number_of_inhabitants_years = pd.DataFrame({'Year': number_of_inhabitants_years})
    df_number_of_inhabitants_years = df_number_of_inhabitants_years.drop_duplicates()
    # print(df_number_of_inhabitants_years)
    df_emission_years = pd.DataFrame({'Year': df_emission['Year']})
    df_emission_years = df_emission_years.drop_duplicates()
    # print (df_emission_years)

    # teraz patrzymy, które lata powtarzają się we wszystkich 3 df

    df_emission_years = df_emission_years.assign(
        result=df_emission_years['Year'].isin(df_number_of_inhabitants_years['Year']).astype('int64'))
    df_emission_years = df_emission_years.loc[df_emission_years['result'] == 1]
    df_emission_years = df_emission_years.assign(
        result2=df_emission_years['Year'].isin(df_gdp_years['Year']).astype('int64'))
    df_emission_years = df_emission_years.loc[df_emission_years['result2'] == 1]
    # usuwam kolumny ze sprawdzaniem
    common_years = df_emission_years.drop(columns=["result", "result2"])

    # print(common_years)
    # print(common_years['Year'].dtype)

    # sprawdzamy czy w common_year są stop year i start year jak nie to wyrzucam błąd
    if (common_years["Year"] != start_year).all():
        raise ValueError("the column don't have the start_year")
    if (common_years["Year"] != stop_year).all():
        raise ValueError("the column don't have the stop_year")
    # i tutaj zmiejszamy zasięg common_years do tego z start_year i stop_year
    list = []
    for i in range(start_year, stop_year + 1):
        list.append(i)
    df_given_years = pd.DataFrame(list, columns=['Year'])
    common_years = common_years.assign(result=common_years['Year'].isin(df_given_years['Year']).astype('int64'))

    common_years = common_years.loc[common_years['result'] == 1]

    common_years = common_years.drop(['result'], axis=1)

    # zmienianie formatu dataframe GDP i number_of_inhibitats, żeby miały taką samą strukturą jak df_emission
    # print(df_gdp)

    df_gdp = pd.melt(df_gdp, id_vars=['Country Name'], value_vars=df_gdp[1:])
    df_gdp.rename(columns={"variable": "Year", "value": "GDP"}, inplace=True)

    df_number_of_inhabitants = pd.melt(df_number_of_inhabitants, id_vars=['Country Name'])
    df_number_of_inhabitants.rename(columns={"variable": "Year", "value": "Number of Inhabitants"}, inplace=True)

    # zmiana typów kolumn z object na int64 żeby zadziałała funkcja isin
    df_gdp['Year'] = df_gdp['Year'].astype('int64')
    df_number_of_inhabitants['Year'] = df_number_of_inhabitants['Year'].astype('int64')

    # usuwanie nieistotnych lat w df, zostają tylko te co mają  result =1 :
    df_emission = df_emission.assign(result=df_emission['Year'].isin(common_years['Year']).astype('int64'))
    df_emission = df_emission.loc[df_emission['result'] == 1]

    df_gdp = df_gdp.assign(result=df_gdp['Year'].isin(common_years['Year']).astype('int64'))
    df_gdp = df_gdp.loc[df_gdp['result'] == 1]

    df_number_of_inhabitants = df_number_of_inhabitants.assign(
        result=df_number_of_inhabitants['Year'].isin(common_years['Year']).astype('int64'))
    df_number_of_inhabitants = df_number_of_inhabitants.loc[df_number_of_inhabitants['result'] == 1]

    # usunięcie kolumny result
    df_gdp = df_gdp.drop(['result'], axis=1)
    df_number_of_inhabitants = df_number_of_inhabitants.drop(['result'], axis=1)
    df_emission = df_emission.drop(['result'], axis=1)

    # df_gdp['Year'] = df_gdp['Year'].astype('string')
    # df_number_of_inhabitants['Year'] = df_number_of_inhabitants['Year'].astype('string')
    list = [df_gdp, df_number_of_inhabitants, df_emission]
    return list
def merge(list):
    df_gdp = list [0]
    df_number_of_inhabitants = list [1]
    df_emission = list [2]
    # scalanie (z indeksem x są dane z df_gdp), pojawi się nowa kolumna _merge z wartościami: both, left_only, right_only
    merged_df = pd.merge(df_gdp, df_number_of_inhabitants, on=['Country Name', 'Year'],how='outer', indicator=True)
    for i, row in merged_df.iterrows():
        if row._merge == 'left_only':
            print(f"Country Name {row['Country Name']} and Year {row['Year']} don't occur in the dataframe with number of inhabitants.")
        elif row._merge == 'right_only':
            print(f"Country Name {row['Country Name']} and Year {row['Year']} don't occur in the dataframe with GDP.")
    # usuwanie wierszy z left_only
    merged_df = merged_df[merged_df._merge != 'left_only']
    # usuwanie wierszy z right_only
    merged_df = merged_df[merged_df._merge != 'right_only']
    # usuwanie kolumny _merge
    merged_df = merged_df.drop(['_merge'], axis=1)
    merged_df = pd.merge(merged_df, df_emission, on=['Country Name', 'Year'], how='outer', indicator=True)
    for i, row in merged_df.iterrows():
        if row._merge == 'left_only':
            print(f"Country Name {row['Country Name']} and Year {row['Year']} don't occur in the dataframe with emission.")
        elif row._merge == 'right_only':
            print(f"Country Name {row['Country Name']} and Year {row['Year']} don't occur in the dataframe with GDP and number of inhabitants.")
    # usuwanie wierszy z left_only
    merged_df = merged_df[merged_df._merge != 'left_only']
    # usuwanie wierszy z right_only
    merged_df = merged_df[merged_df._merge != 'right_only']
    # usuwanie kolumny _merge
    merged_df = merged_df.drop(['_merge'], axis=1)
    return merged_df

