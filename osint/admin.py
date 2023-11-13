from django.contrib import admin
from .models import *

admin.site.register(Root)
admin.site.register(Folder)
admin.site.register(Child)
admin.site.register(Script)
#admin.site.register(Log)