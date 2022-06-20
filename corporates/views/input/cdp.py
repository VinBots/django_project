from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse

from corporates.forms import CDPForm
from corporates.models import Corporate, CDP
from corporates.views.utilities import add_context
from corporates.views.input.permissions import (
    AllowedCorporateMixin,
    restrict_query_corp,
    restrict_query_user,
)


class CDPListView(AllowedCorporateMixin, ListView):
    """
    Handles the 'VIEW' functionality of the 'CDP' section of the input interface
    """

    template_name = "input/cdp/corp_cdp_list.html"
    model = CDP
    context_object_name = "cdp"
    success_msg = "Data was successfully saved!"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="cdp")
        if self.request.GET.get("success") == "yes":
            self.extra_context["success_message"] = self.success_msg
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        query = super().get_queryset()
        restricted_query = restrict_query_corp(self, query)
        restricted_query = restrict_query_user(self, restricted_query)
        return restricted_query


class CDPListCreate(AllowedCorporateMixin, CreateView):
    """
    Handles the 'CREATE' functionality of the 'CDP' section of the input interface
    """

    form_class = CDPForm
    template_name = "input/cdp/corp_cdp_create.html"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="cdp")
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_cdp_home", kwargs={"corp_name": context["corp_name"]}
            )
            + "?success=yes"
        )
        self.extra_context = add_context(init_kwargs=kwargs, category_name="cdp")

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.company = Corporate.objects.get(name=self.kwargs["corp_name"])
        form.instance.submitter = self.request.user
        form.instance.status = "submitted"
        return super(CDPListCreate, self).form_valid(form)


class CDPListUpdate(AllowedCorporateMixin, UpdateView):
    """
    Handles the 'UPDATE' functionality of the 'CDP' section of the input interface
    """

    model = CDP
    template_name = "input/cdp/corp_cdp_update.html"
    form_class = CDPForm

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="cdp")
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):

        query = super().get_queryset()
        return restrict_query_user(self, query)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_cdp_home", kwargs={"corp_name": context["corp_name"]}
            )
            + "?success=yes"
        )
        self.extra_context = add_context(init_kwargs=kwargs, category_name="cdp")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.company = Corporate.objects.get(name=self.kwargs["corp_name"])
        form.instance.submitter = self.request.user
        form.instance.status = "submitted"
        return super(CDPListUpdate, self).form_valid(form)


class CDPListDelete(AllowedCorporateMixin, DeleteView):
    """
    Handles the 'DELETE' functionality of the 'CDP' section of the input interface
    """

    model = CDP
    success_url = "/"
    template_name = "input/cdp/corp_cdp_delete.html"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="cdp")
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):

        query = super().get_queryset()
        return restrict_query_user(self, query)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_cdp_home", kwargs={"corp_name": context["corp_name"]}
            )
            + "?success=yes"
        )
        self.extra_context = add_context(init_kwargs=kwargs, category_name="cdp")
        return super().post(request, *args, **kwargs)
