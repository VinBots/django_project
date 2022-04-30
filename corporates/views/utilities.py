from corporates.models import Corporate


def add_context(init_kwargs={}, category_name="ghg"):

    extra_context = init_kwargs
    extra_context["category"] = category_name

    if init_kwargs["corp_name"]:
        extra_context["company_id"] = Corporate.objects.filter(
            name=init_kwargs["corp_name"]
        )[0].company_id
    return extra_context
