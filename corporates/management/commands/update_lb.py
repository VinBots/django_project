import os, sys

# from corporates.models import Corporate
from django.core.management import BaseCommand
from django.conf import settings

sys.path.append(os.path.join(settings.SERVER_BASE_DIR, "scripts"))
from transformers.update_lb import (
    update_lb,
    delete_all_file_fields,
    write_uploads_to_model,
)


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("company_name", type=str)

    def handle(self, *args, **options):
        delete_all_file_fields()
        # update_lb()
        write_uploads_to_model()
