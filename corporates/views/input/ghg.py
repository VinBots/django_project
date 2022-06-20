from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse

from corporates.forms import GHGForm
from corporates.models import Corporate, GHGQuant
from corporates.views.utilities import add_context
from corporates.views.input.permissions import (
    AllowedCorporateMixin,
    restrict_query_corp,
    restrict_query_user,
)


class GHGListView(AllowedCorporateMixin, ListView):
    """
    Handles the 'VIEW' functionality of the 'GHG Inventory' section of the input interface
    """

    template_name = "input/ghg/corp_ghg_list.html"
    model = GHGQuant
    context_object_name = "ghg"
    success_msg = "Data was successfully saved!"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="ghg")
        if self.request.GET.get("success") == "yes":
            self.extra_context["success_message"] = self.success_msg
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        query = super().get_queryset()
        restricted_query = restrict_query_corp(self, query)
        restricted_query = restrict_query_user(self, restricted_query)
        return restricted_query


class GHGListCreate(AllowedCorporateMixin, CreateView):
    """
    Handles the 'CREATE' functionality of the 'GHG Inventory' section of the input interface
    """

    form_class = GHGForm
    template_name = "input/ghg/corp_ghg_create.html"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="ghg")
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_ghg_home", kwargs={"corp_name": context["corp_name"]}
            )
            + "?success=yes"
        )
        self.extra_context = add_context(init_kwargs=kwargs, category_name="ghg")

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.company = Corporate.objects.get(name=self.kwargs["corp_name"])
        form.instance.submitter = self.request.user
        form.instance.status = "submitted"
        return super(GHGListCreate, self).form_valid(form)


class GHGListUpdate(AllowedCorporateMixin, UpdateView):
    """
    Handles the 'UPDATE' functionality of the 'GHG Inventory' section of the input interface
    """

    model = GHGQuant
    template_name = "input/ghg/corp_ghg_update.html"
    form_class = GHGForm

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="ghg")
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):

        query = super().get_queryset()
        return restrict_query_user(self, query)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_ghg_home", kwargs={"corp_name": context["corp_name"]}
            )
            + "?success=yes"
        )
        self.extra_context = add_context(init_kwargs=kwargs, category_name="ghg")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.company = Corporate.objects.get(name=self.kwargs["corp_name"])
        form.instance.submitter = self.request.user
        form.instance.status = "submitted"
        return super(GHGListUpdate, self).form_valid(form)


class GHGListDelete(AllowedCorporateMixin, DeleteView):
    """
    Handles the 'DELETE' functionality of the 'GHG Inventory' section of the input interface
    """

    model = GHGQuant
    success_url = "/"
    template_name = "input/ghg/corp_ghg_delete.html"
    # form_class = GHGForm

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="ghg")
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):

        query = super().get_queryset()
        return restrict_query_user(self, query)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_ghg_home", kwargs={"corp_name": context["corp_name"]}
            )
            + "?success=yes"
        )
        self.extra_context = add_context(init_kwargs=kwargs, category_name="ghg")
        return super().post(request, *args, **kwargs)
