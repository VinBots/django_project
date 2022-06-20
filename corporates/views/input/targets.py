from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse

from corporates.forms import TargetForm
from corporates.models import Corporate, TargetQuant
from corporates.views.utilities import add_context
from corporates.views.input.permissions import (
    AllowedCorporateMixin,
    restrict_query_corp,
    restrict_query_user,
)


class TargetListView(AllowedCorporateMixin, ListView):
    """
    Handles the 'VIEW' functionality of the 'Target' section of the input interface
    """

    template_name = "input/target/corp_target_list.html"
    model = TargetQuant
    context_object_name = "target"
    success_msg = "Data was successfully saved!"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="target")
        if self.request.GET.get("success") == "yes":
            self.extra_context["success_message"] = self.success_msg
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        query = super().get_queryset()
        restricted_query = restrict_query_corp(self, query)
        restricted_query = restrict_query_user(self, restricted_query)
        return restricted_query


class TargetListCreate(AllowedCorporateMixin, CreateView):
    """
    Handles the 'CREATE' functionality of the 'Target' section of the input interface
    """

    form_class = TargetForm
    template_name = "input/target/corp_target_create.html"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="target")
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_target_home", kwargs={"corp_name": context["corp_name"]}
            )
            + "?success=yes"
        )
        self.extra_context = add_context(init_kwargs=kwargs, category_name="target")

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.company = Corporate.objects.get(name=self.kwargs["corp_name"])
        form.instance.submitter = self.request.user
        form.instance.status = "submitted"
        return super(TargetListCreate, self).form_valid(form)


class TargetListUpdate(AllowedCorporateMixin, UpdateView):
    """
    Handles the 'UPDATE' functionality of the 'Target' section of the input interface
    """

    model = TargetQuant
    template_name = "input/target/corp_target_update.html"
    form_class = TargetForm

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="target")
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):

        query = super().get_queryset()
        return restrict_query_user(self, query)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_target_home", kwargs={"corp_name": context["corp_name"]}
            )
            + "?success=yes"
        )
        self.extra_context = add_context(init_kwargs=kwargs, category_name="target")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.company = Corporate.objects.get(name=self.kwargs["corp_name"])
        form.instance.submitter = self.request.user
        form.instance.status = "submitted"
        return super(TargetListUpdate, self).form_valid(form)


class TargetListDelete(AllowedCorporateMixin, DeleteView):
    """
    Handles the 'DELETE' functionality of the 'TargetQuant' section of the input interface
    """

    model = TargetQuant
    success_url = "/"
    template_name = "input/target/corp_target_delete.html"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="target")
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):

        query = super().get_queryset()
        return restrict_query_user(self, query)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_target_home", kwargs={"corp_name": context["corp_name"]}
            )
            + "?success=yes"
        )
        self.extra_context = add_context(init_kwargs=kwargs, category_name="target")
        return super().post(request, *args, **kwargs)
