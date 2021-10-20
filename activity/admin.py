from django.contrib import admin
from .models import Activity,AuthActivityLog
# Register your models here.


admin.site.register(Activity)
admin.site.register(AuthActivityLog)