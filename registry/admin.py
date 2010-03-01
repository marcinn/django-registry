from django.contrib import admin
from django.utils.translation import ugettext as _
from django.conf import settings

import models


class EntryAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    list_filter = ('type',)
    search_fields = ('key','value_text','value_numeric','value_bool',)


admin.site.register(models.Entry, EntryAdmin)

