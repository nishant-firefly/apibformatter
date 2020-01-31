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
        resource_url = action.resource.url
        if hub_name not in data:
            data[hub_name] = {}
        if group_name not in data[hub_name]:
            data[hub_name][group_name] = {}
        if (resource_name,resource_url) not in data[hub_name][group_name]:
            data[hub_name][group_name][(resource_name,resource_url)] = []
        data[hub_name][group_name][(resource_name,resource_url)].append(
            {
                "name":action.name,
                "request_data":action.request_data,
                "request_method":action.request_method.method,
                "response_data":action.response_data,
                "response_header_status":action.response_header_status,
                "request_header_status":action.request_header_status,
                "url":action.url

            }
        )
    

    s="""FORMAT: 1A
HOST: https://polls.apiblueprint.org/

"""
    for hub, groups in data.items():
        s=s+"""# %s

"""%hub.capitalize()
        for group,resources in groups.items():
            s=s+"""## Group %s

"""%group
            for resource_and_url,actions in   resources.items():
                s=s+"""### %s [%s]

"""%resource_and_url
                #for action in actions:
            for action in actions: 
                request_data =action["request_data"]
                response_data =action["response_data"]
                s = s + """#### %s for %s [%s %s]
+ %s

%s

+ %s

%s

"""%(action['name'],group,action["request_method"],action["url"],
    action["request_header_status"],request_data, action["response_header_status"],response_data )
    return render(request,'index.html',{"data":s})
    """
    name =models.CharField(max_length=200, unique=True)
    resource = models.ForeignKey(Resource,on_delete=models.CASCADE)
    request_data = models.TextField()
    request_method = models.ForeignKey(RequestMethod,on_delete=models.CASCADE)
    response_data = models.TextField()
    response_header_status = models.ForeignKey(ResponseHeaderStatus,on_delete=models.CASCADE)
    url
"""