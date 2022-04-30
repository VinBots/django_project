from django.contrib.auth.mixins import LoginRequiredMixin

from corporates.models.users import UserProfile
from corporates.models.corp import Corporate


class AllowedCorporateMixin(LoginRequiredMixin):

    login_url = "login"

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated or not self.isCorporateAllowed(
            *args, **kwargs
        ):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def isCorporateAllowed(self, *args, **kwargs):

        corp = kwargs["corp_name"]
        test0 = test1 = test2 = True
        test0 = Corporate.objects.filter(name=corp).exists()

        if test0:
            test1 = UserProfile.objects.filter(
                user=self.request.user, allowed_corporates_all=True
            ).exists()

            if not test1:
                test2 = UserProfile.objects.filter(
                    user=self.request.user, allowed_corporates__name=corp
                ).exists()

        msg = f"Does the company name exist in the DB? {test0}"
        if test0:
            msg = f"{msg}; Is the registered user aloowed to view all the companies? {test1}"

            if not test1:
                msg = f"{msg}; Is the registered user allowed to view the specific company? {test2}"

        print(msg)

        return (test0) and (test1 or test2)
