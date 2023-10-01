from reporting.transformers import relevant_df


def _transform_radial(data):
    # Prepare dataframe
    source = data[['remote', 'rating_score', 'seniority_score']]
    source.rename(columns={'remote': 'Remote', 'rating_score': 'Rating', 'seniority_score': 'Seniority'}, inplace=True)

    source['Seniority'] = source['Seniority'].replace([3, 1, 0, -1], ['Junior', 'Unspecified', 'Graduate', 'Senior'])
    source['Rating'] = source['Rating'].replace([-3, -2, -1, 0, 1, 2, 3], ['< 20 Percentile', '20-40 Percentile',
                                                                           '40-50 Percentile', 'Median', '50-60 Percentile',
                                                                           '60-80 Percentile', '> 80 Percentile'])

    target = []
    for col in source.columns:
        # Get the unique values and their counts in the current column
        value_counts = source[col].value_counts()

        # Convert the value counts to a list of dictionaries
        data_list = [{"x": str(value), "y": count} for value, count in value_counts.items()]

        # Append the data for the current column to the target list
        target.append({"id": col, "data": data_list})

    return target


radial_data = _transform_radial(relevant_df)
