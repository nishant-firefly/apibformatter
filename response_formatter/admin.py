from django.contrib import admin
from django.contrib.auth.models import User,Group
from response_formatter.models import \
    RequestMethod,ResponseHeaderStatus,RequestHeaderStatus,Hub,HubGroup,Action,Resource
#from jsonformatter import JsonFormatter
import json
import textwrap
def indent(text, amount, ch=' '):
        return textwrap.indent(text, amount * ch)
class RequestHeaderStatusAdmin(admin.ModelAdmin):
    fields = list_display = ["header"]

class ResponseHeaderStatusAdmin(admin.ModelAdmin):
    fields = list_display = ["header"]

class RequestMethodAdmin(admin.ModelAdmin):
    fields = list_display = ["method"]
class HubAdmin(admin.ModelAdmin):
    fields = list_display = ["name"]

class GroupAdmin(admin.ModelAdmin):
    fields = list_display = ["hub","name"] 

class ResourceAdmin(admin.ModelAdmin):
    fields = list_display = ["name","url","group"]
class ActionAdmin(admin.ModelAdmin):
    fields = list_display = ["name","resource","url","request_method","request_header_status","response_header_status","request_data","response_data"]
    def save_model(self, request, obj, form, change):
        obj.request_data = indent(json.dumps(json.loads(obj.request_data),indent=4),8)
        obj.response_data = indent(json.dumps(json.loads(obj.response_data),indent=4),8)
        obj.save()

admin.site.register(Hub,HubAdmin)
admin.site.register(RequestHeaderStatus,RequestHeaderStatusAdmin)
admin.site.register(ResponseHeaderStatus,ResponseHeaderStatusAdmin)
admin.site.register(RequestMethod,RequestMethodAdmin)
admin.site.register(HubGroup,GroupAdmin)
admin.site.register(Resource,ResourceAdmin)
admin.site.register(Action,ActionAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)


