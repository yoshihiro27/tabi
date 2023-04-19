from django.contrib import admin
from .models import Tabi,TabiDate,Comment,Connection

# Register your models here.



class TabiDateInline(admin.StackedInline):
    model = TabiDate
    extra = 3


class TabiAdmin(admin.ModelAdmin):
    inlines = [TabiDateInline]

admin.site.register(TabiDate)
admin.site.register(Tabi,TabiAdmin)
admin.site.register(Comment)
admin.site.register(Connection)