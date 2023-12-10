import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here

    df = df.pivot(index='id_1', columns='id_2', values='car')

    df = df.fillna(0)

    return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here

    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                              labels=['low', 'medium', 'high'], right=False)

    type_counts = df['car_type'].value_counts().to_dict()

    sorted_type_counts = dict(sorted(type_counts.items()))


    return dict(sorted_type_counts)


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here

    bus_mean = df['bus'].mean()

    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    sorted_bus_indexes = sorted(bus_indexes)

    return list(sorted_bus_indexes)


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here

    avg_truck_by_route = df.groupby('route')['truck'].mean()

    selected_routes = avg_truck_by_route[avg_truck_by_route > 7].index.tolist()

    sorted_routes = sorted(selected_routes)

    return list(sorted_routes)


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here

    def multiply_logic(value):

        if value > 20:
            return round(value * 0.75, 1)
        else:
            return round(value * 1.25, 1)

    matrix = df.applymap(multiply_logic)

    return matrix


def time_check(df2)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series

            """
    # Write your logic here

    # Convert startDay and endDay to datetime format
    df2['startTime'] = pd.to_datetime(df2['startTime'])
    df2['endTime'] = pd.to_datetime(df2['endTime'])
    
    # Group by id and id_2
    grouped = df2.groupby(['id', 'id_2'])
    
    # Initialize an empty series to store the results
    results = pd.Series(dtype=bool)
    
    # Iterate over each group
    for name, group in grouped:
        # Check if the timestamps cover a full 24-hour period and span all 7 days of the week
        if (group['startTime'].min().time() != pd.Timestamp('00:00:00').time() or
            group['endTime'].max().time() != pd.Timestamp('23:59:59').time() or
            group['startDay'].nunique() != 7 or
            group['endDay'].nunique() != 7):
            results[name] = True
        else:
            results[name] = False
    
    return results

    # return pd.Series()

df = pd.read_csv("MapUp-Data-Assessment-F-main\datasets\dataset-1.csv")
df2 = pd.read_csv("MapUp-Data-Assessment-F-main\datasets\dataset-2.csv")

result1 = generate_car_matrix(df)
print("", result1)
print()
result2 = get_type_count(df)
print(result2)
print()
result3 = get_bus_indexes(df)
print(result3)
print()
result4 = filter_routes(df)
print(result4)
print()
result5 = multiply_matrix(df)
print(result5)
print()

def test_check_timestamps():
    data = dict(zip(df2.id, df2.id_2, df2.startDay, df2.startTime, df2.endDay, df2.endTime))
    
    expected = pd.Series([True, True, True, True, False], index=pd.MultiIndex.from_tuples([(1040000, -1), (1040010, -1), (1040020, -1), (1040030, -1), (1050000, 1050001)]))
    
    assert check_timestamps(data).equals(expected)

result6 = time_check(df2)
print(result6)
print()