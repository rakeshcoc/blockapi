from django.contrib import admin

# Register your models here.
from .models import transaction,blocks


admin.site.register(transaction)
admin.site.register(blocks)