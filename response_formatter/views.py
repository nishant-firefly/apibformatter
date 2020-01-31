from django.shortcuts import render
from django.http import JsonResponse
from response_formatter.models import Action
# Create your views here.
def index(request):
    data = {}
    actions  = Action.objects.all()
    for action in actions : 
        hub_name = action.resource.group.hub.name
        group_name = action.resource.group.name
        resource_name = action.resource.name
        #resource_url = action.resource.url
        if hub_name not in data:
            data[hub_name] = {}
        if group_name not in data[hub_name]:
            data[hub_name][group_name] = {}
        if resource_name not in data[hub_name][group_name]:
            data[hub_name][group_name][resource_name] = {"url":action.resource.url,"actions":[]}
        data[hub_name][group_name][resource_name]["actions"].append(
            {
                "name":action.name,
                "request_data":action.request_data,
                "request_method":action.request_method.method,
                "response_data":action.response_data,
                "response_header_status":action.response_header_status.header,
                "request_header_status":action.request_header_status.header,
                "url":action.url

            }
        )
        #resource_url_map[(hub_name,group_name,resource_name)]=resource_url

    return render(request,'index.html',{"data":data})