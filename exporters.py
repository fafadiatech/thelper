def export_tsv(file_to_save, dataset, is_dict=False):
    with open(file_to_save, "w") as output:
        if not is_dict:
            for current in dataset:
                row = "\t".join(current) + "\n"
                output.write(row)
        else:
            for item, value in dataset.items():
                row = f"{item}\t{value}\n"
                output.write(row)
    print(f"Saved output to {file_to_save}\n")
