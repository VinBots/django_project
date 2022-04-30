from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse

from corporates.forms import NetZeroForm
from corporates.models import Corporate, NetZero
from corporates.views.utilities import add_context
from corporates.views.input.permissions import AllowedCorporateMixin


class NetZeroListView(AllowedCorporateMixin, ListView):
    """
    Handles the 'VIEW' functionality of the 'NetZero' section of the input interface
    """

    template_name = "input/netzero/corp_netzero_list.html"
    model = NetZero
    context_object_name = "netzero"
    success_msg = "Data was successfully saved!"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="netzero")
        if self.request.GET.get("success") == "yes":
            self.extra_context["success_message"] = self.success_msg
        return super().get(request, *args, **kwargs)

    def get_queryset(self):

        corp_name = self.extra_context.get("corp_name")
        return (
            super()
            .get_queryset()
            .filter(submitter=self.request.user, company__name=corp_name)
        )


class NetZeroListCreate(AllowedCorporateMixin, CreateView):
    """
    Handles the 'CREATE' functionality of the 'NetZero' section of the input interface
    """

    form_class = NetZeroForm
    template_name = "input/netzero/corp_netzero_create.html"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="netzero")
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_netzero_home", kwargs={"corp_name": context["corp_name"]}
            )
            + "?success=yes"
        )
        self.extra_context = add_context(init_kwargs=kwargs, category_name="netzero")

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.company = Corporate.objects.get(name=self.kwargs["corp_name"])
        if self.request.user != "django":
            form.instance.submitter = self.request.user
            # form.instance.verifier = "pending"
            form.instance.status = "submitted"
        return super(NetZeroListCreate, self).form_valid(form)


class NetZeroListUpdate(AllowedCorporateMixin, UpdateView):
    """
    Handles the 'UPDATE' functionality of the 'NetZero' section of the input interface
    """

    model = NetZero
    template_name = "input/netzero/corp_netzero_update.html"
    form_class = NetZeroForm

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="netzero")
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_netzero_home", kwargs={"corp_name": context["corp_name"]}
            )
            + "?success=yes"
        )
        self.extra_context = add_context(init_kwargs=kwargs, category_name="netzero")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.company = Corporate.objects.get(name=self.kwargs["corp_name"])
        if self.request.user != "django":
            form.instance.submitter = self.request.user
            # form.instance.verifier = "pending"
            form.instance.status = "submitted"
        return super(NetZeroListUpdate, self).form_valid(form)


class NetZeroListDelete(AllowedCorporateMixin, DeleteView):
    """
    Handles the 'DELETE' functionality of the 'NetZero' section of the input interface
    """

    model = NetZero
    success_url = "/"
    template_name = "input/netzero/corp_netzero_delete.html"

    def get(self, request, *args, **kwargs):
        self.extra_context = add_context(init_kwargs=kwargs, category_name="netzero")
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        context = kwargs
        self.success_url = (
            reverse(
                "input_by_corp_netzero_home", kwargs={"corp_name": context["corp_name"]}
            )
            + "?success=yes"
        )
        self.extra_context = add_context(init_kwargs=kwargs, category_name="netzero")
        return super().post(request, *args, **kwargs)
