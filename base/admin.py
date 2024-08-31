from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.contrib.sessions.models import Session
from django.contrib.contenttypes.models import ContentType

try:
    admin.site.unregister(Group)

    class GroupAdminModel(GroupAdmin):
        list_display = ["name", "id"]

    admin.site.register(Group, GroupAdminModel)
    admin.site.register(ContentType)
except Exception as e:
    print(e)


try:
    admin.site.register(Session)
except Exception as e:
    print(e)


admin.site.index_title = "E-Procurement"
admin.site.site_title = "E-Procurement"
