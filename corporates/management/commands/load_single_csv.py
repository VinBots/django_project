import csv
import os

from django.core.management import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User

from ..imports.config import csv_file_mapping


RECORDS_LIMIT = 100000


class Command(BaseCommand):
    help = "Loads data from CSV file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        start_time = timezone.now()
        file_path = options["file_path"]
        file_name = os.path.basename(file_path)
        print(file_name)
        cols_to_fetch_list = csv_file_mapping.get(file_name, "")["cols_to_fetch"]
        Model_to_Use_list = csv_file_mapping.get(file_name, "")["Model_to_Use"]
        add_arg_bool_list = csv_file_mapping.get(file_name, "")["add_arg"]

        if not cols_to_fetch_list:
            print("could not find the filename in the csv_file_mapping dictionary")
            return

        for cols_to_fetch, Model_to_Use, add_arg_bool in zip(
            cols_to_fetch_list, Model_to_Use_list, add_arg_bool_list
        ):

            count = 0

            with open(file_path, "r", encoding="utf8") as csv_file:
                data = csv.DictReader(csv_file)
                records = []

                for row in data:
                    if file_name != "score_desc.csv":
                        if not row["company_id"] or count > RECORDS_LIMIT:
                            break
                    count += 1
                    kwargs = {}
                    for key, value in cols_to_fetch.items():

                        col_to_fetch_name = key
                        model_field = value["model_field"]

                        csv_raw_value = row[col_to_fetch_name]
                        if value["map"]:
                            tf_value = value["mapping"](csv_raw_value)
                        else:
                            tf_value = csv_raw_value

                        if not value["fk"]:
                            new_arg = {model_field: tf_value}

                        else:
                            fk_model = value["fk_model"]
                            fk_kwargs = {value["fk_field"]: tf_value}
                            fk_object = fk_model.objects.get(**fk_kwargs)
                            new_arg = {model_field: fk_object}

                        kwargs.update(new_arg)

                    if add_arg_bool:
                        add_arg = {
                            "submitter": User.objects.get(
                                username="auto_ingestion_from_csv"
                            )
                        }
                        kwargs.update(add_arg)

                    # print(kwargs.values())

                    record = Model_to_Use(**kwargs)
                    records.append(record)
                    if len(records) > 5000:
                        Model_to_Use.objects.bulk_create(records)
                        records = []

                if records:
                    Model_to_Use.objects.bulk_create(records)
            end_time = timezone.now()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds."
                )
            )
