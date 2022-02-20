from django.contrib import admin

from .models import Company, GHGQuant, Source

admin.site.register(Source)
admin.site.register(Company)
admin.site.register(GHGQuant)
