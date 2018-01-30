def import_training_dataframe():
    path_to_dataframe = local_path + 'training_set.pickle'
    return pd.read_pickle(path_to_dataframe)


# Get training data
training_data = import_training_dataframe()
