def analysis (data):
    merged_df = data
    # ANALIZY
    # analizy podpunkt A
    # dodanie kolumny z emisją na osobę
    merged_df['CO2 emission per person'] = merged_df['Total'] / merged_df['Number of Inhabitants']

    # stworzenie df tylko z kolumnami z tymi danymi co nas inetersują
    df_analys_CO2 = merged_df[['Year','Country Name', 'CO2 emission per person', 'Total']]
    # print(df_analys_CO2)
    # wynik podpunktu A
    result_a = df_analys_CO2.groupby(['Year']).apply(lambda x: x.nlargest(5, 'CO2 emission per person'))

    #print(result_a)

    # podpunkt B
    # dodanie kolumny z dochodem na osobę
    # merged_df['GDP'] = merged_df['GDP'].astype('int64')
    merged_df['GDP per person'] = merged_df['GDP'] / merged_df['Number of Inhabitants']

    # stworzenie df tylko z tymi danymi co nas interesującymi
    df_analys_GDP = merged_df[['Year','Country Name', 'GDP per person', 'GDP']]
    # wynik podpunktu B

    result_b = df_analys_GDP.groupby(['Year']).apply(lambda x: x.nlargest(5, 'GDP per person'))
    #print(result_b)

    # PODPUNKT C
    # szukanie interesującego nas zakresu danych

    max_year = merged_df['Year'].max()
    min_year = max_year - 10
    #zrobienie df tylko z latami, które nas interesują
    filtered_df = merged_df[(merged_df['Year'] == min_year) | (merged_df['Year'] == max_year)]

    # print(filtered_df)
    df_pivot = filtered_df.pivot_table(index='Country Name', columns='Year', values='CO2 emission per person')
    co2_diff = df_pivot[max_year] - df_pivot[min_year]
    result_c_1 = co2_diff.nlargest(5)
    result_c_2 = co2_diff.nsmallest(5)
    #print(result_c_1)
    #print(result_c_2)
    list_of_results = [result_a, result_b, result_c_1, result_c_2]
    return list_of_results

