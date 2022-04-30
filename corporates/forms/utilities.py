import copy


def get_upload_fields_to_display(initial, upload_field_count=5):

    optional_fields = [
        f"upload_{field_count}" for field_count in range(upload_field_count, 1, -1)
    ]

    fields_to_display = copy.deepcopy(optional_fields)
    for field in optional_fields:
        if not initial.get(field, None):
            fields_to_display.pop(0)
        else:
            return fields_to_display
