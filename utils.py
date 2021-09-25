def dict_to_list(dataset):
    results = []
    for k, v in dataset.items():
        results.append([k, v])
    return results
