from jinja2 import Template
from datetime import datetime


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


def export_html(file_to_save, context):
    with open("templates/report_base.html") as t_contents:
        template = Template(t_contents.read())
        output = open(file_to_save, "w")
        output.write(template.render(today=datetime.now().date(), context=context))
        print(f"Saved output to {file_to_save}\n")
