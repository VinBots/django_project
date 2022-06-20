from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse

from corporates.forms import VerifForm
from corporates.models import Corporate, Verification
from corporates.views.utilities import add_context
from corporates.views.input.permissions import (
    AllowedCorporateMixin,
    restrict_query_corp,
    restrict_query_user,
)


class VerifListView(AllowedCorporateMixin, ListView):
    """
    Handles the 'VIEW' functionality of the 'Verification' section of the input interface
    """

    template_name = "input/verif/corp_verif_list.html"
    model = Verification
    context_object_name = "verif"
    success_msg = "Data was successfully saved!"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="verif")
        if self.request.GET.get("success") == "yes":
            self.extra_context["success_message"] = self.success_msg
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        query = super().get_queryset()
        restricted_query = restrict_query_corp(self, query)
        restricted_query = restrict_query_user(self, restricted_query)
        return restricted_query


class VerifListCreate(AllowedCorporateMixin, CreateView):
    """
    Handles the 'CREATE' functionality of the 'Verification' section of the input interface
    """

    form_class = VerifForm
    template_name = "input/verif/corp_verif_create.html"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="verif")
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_verif_home", kwargs={"corp_name": context["corp_name"]}
            )
            + "?success=yes"
        )
        self.extra_context = add_context(init_kwargs=kwargs, category_name="verif")

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.company = Corporate.objects.get(name=self.kwargs["corp_name"])
        form.instance.submitter = self.request.user
        form.instance.status = "submitted"
        return super(VerifListCreate, self).form_valid(form)


class VerifListUpdate(AllowedCorporateMixin, UpdateView):
    """
    Handles the 'UPDATE' functionality of the 'Verification' section of the input interface
    """

    model = Verification
    template_name = "input/verif/corp_verif_update.html"
    form_class = VerifForm
    context_object_name = "verif"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="verif")
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):

        query = super().get_queryset()
        return restrict_query_user(self, query)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_verif_home", kwargs={"corp_name": context["corp_name"]}
            )
            + "?success=yes"
        )
        self.extra_context = add_context(
            init_kwargs=kwargs,
            category_name="verif",
        )
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.company = Corporate.objects.get(name=self.kwargs["corp_name"])
        form.instance.submitter = self.request.user
        form.instance.status = "submitted"
        return super(VerifListUpdate, self).form_valid(form)


class VerifListDelete(AllowedCorporateMixin, DeleteView):
    """
    Handles the 'DELETE' functionality of the 'Verification' section of the input interface
    """

    model = Verification
    success_url = "/"
    template_name = "input/verif/corp_verif_delete.html"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="verif")
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):

        query = super().get_queryset()
        return restrict_query_user(self, query)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_verif_home", kwargs={"corp_name": context["corp_name"]}
            )
            + "?success=yes"
        )
        self.extra_context = add_context(init_kwargs=kwargs, category_name="verif")
        return super().post(request, *args, **kwargs)
