from django.contrib import admin

from .models import OpenDataPortal
from .models import LoadRound
from .models import Tag
from .models import Dataset
from .models import Group

admin.site.register(OpenDataPortal)
admin.site.register(LoadRound)
admin.site.register(Tag)
admin.site.register(Dataset)
admin.site.register(Group)
