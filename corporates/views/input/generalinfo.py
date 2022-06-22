from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse

from corporates.forms import GeneralInfoForm
from corporates.models import Corporate, GeneralInfo
from corporates.views.utilities import add_context
from corporates.views.input.permissions import (
    AllowedCorporateMixin,
    restrict_query_corp,
    restrict_query_user,
)


class GeneralInfoListView(AllowedCorporateMixin, ListView):
    """
    Handles the 'VIEW' functionality of the 'GeneralInfo' section of the input interface
    """

    template_name = "input/generalinfo/corp_generalinfo_list.html"
    model = GeneralInfo
    context_object_name = "generalinfo"
    success_msg = "Data was successfully saved!"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(
            init_kwargs=kwargs, category_name="generalinfo"
        )
        if self.request.GET.get("success") == "yes":
            self.extra_context["success_message"] = self.success_msg
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        query = super().get_queryset()
        restricted_query = restrict_query_corp(self, query)
        restricted_query = restrict_query_user(self, restricted_query)
        return restricted_query


class GeneralInfoListCreate(AllowedCorporateMixin, CreateView):
    """
    Handles the 'CREATE' functionality of the 'GeneralInfo' section of the input interface
    """

    form_class = GeneralInfoForm
    template_name = "input/generalinfo/corp_generalinfo_create.html"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(
            init_kwargs=kwargs, category_name="generalinfo"
        )
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_generalinfo_home",
                kwargs={"corp_name": context["corp_name"]},
            )
            + "?success=yes"
        )
        self.extra_context = add_context(
            init_kwargs=kwargs, category_name="generalinfo"
        )

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.company = Corporate.objects.get(name=self.kwargs["corp_name"])
        form.instance.submitter = self.request.user
        form.instance.status = "submitted"
        return super(GeneralInfoListCreate, self).form_valid(form)


class GeneralInfoListUpdate(AllowedCorporateMixin, UpdateView):
    """
    Handles the 'UPDATE' functionality of the 'GeneralInfo' section of the input interface
    """

    model = GeneralInfo
    template_name = "input/generalinfo/corp_generalinfo_update.html"
    form_class = GeneralInfoForm
    context_object_name = "generalinfo"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(
            init_kwargs=kwargs, category_name="generalinfo"
        )
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):

        query = super().get_queryset()
        return restrict_query_user(self, query)

    def post(self, request, *args, **kwargs):
        print(request.POST)

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_generalinfo_home",
                kwargs={"corp_name": context["corp_name"]},
            )
            + "?success=yes"
        )
        self.extra_context = add_context(
            init_kwargs=kwargs, category_name="GeneralInfo"
        )

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.company = Corporate.objects.get(name=self.kwargs["corp_name"])
        form.instance.submitter = self.request.user
        # form.instance.status = "submitted"
        return super(GeneralInfoListUpdate, self).form_valid(form)


class GeneralInfoListDelete(AllowedCorporateMixin, DeleteView):
    """
    Handles the 'DELETE' functionality of the 'GeneralInfo' section of the input interface
    """

    model = GeneralInfo
    success_url = "/"
    template_name = "input/generalinfo/corp_generalinfo_delete.html"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(
            init_kwargs=kwargs, category_name="generalinfo"
        )
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):

        query = super().get_queryset()
        return restrict_query_user(self, query)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_generalinfo_home",
                kwargs={"corp_name": context["corp_name"]},
            )
            + "?success=yes"
        )
        self.extra_context = add_context(
            init_kwargs=kwargs, category_name="generalinfo"
        )
        return super().post(request, *args, **kwargs)
