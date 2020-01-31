from django.db import models
from django.forms import ValidationError
import json
# Create your models here..
METHOD_CHOICES = (
    ("GET","Get Method"),
    ("POST","Post Method"),
    ("PUT","Put Method"),
    ("DELETE","Delete Method"),
)
HUB_CHOICES = (
    ("workload","Workload"),
    ("hub","Hub"),
    ("logistics","Logistics")
)

RESPONSE_STATUS_CHOICES=(
    ("Response 200 (application/json)","Response 200 (application/json)"),

)

REQUEST_STATUS_CHOICES = (
    ("Request (application/json)","Request (application/json)"),
)


class ResponseHeaderStatus(models.Model):
    header =models.CharField(max_length=200, choices=RESPONSE_STATUS_CHOICES,unique=True)
    def __str__(self): return self.header


class RequestHeaderStatus(models.Model):
    header =models.CharField(max_length=200, choices=REQUEST_STATUS_CHOICES,unique=True)
    def __str__(self): return self.header

class RequestMethod(models.Model):
    method =models.CharField(max_length=200, choices=METHOD_CHOICES,unique=True)
    def __str__(self): return self.method

class Hub(models.Model):
    name =models.CharField(max_length=200, choices = HUB_CHOICES,unique=True)
    def __str__(self): return self.name


class HubGroup(models.Model):
    hub =models.ForeignKey(Hub, on_delete=models.CASCADE)
    name =models.CharField(max_length=200)
    def __str__(self): return self.name  +"=>" + str(self.hub)


class Resource(models.Model):
    group =models.ForeignKey(HubGroup, on_delete=models.CASCADE)
    name =models.CharField(max_length=200)
    url =models.CharField(max_length=200)
    def __str__(self): return self.name  +"=>" + str(self.group)


class Action(models.Model):
    name =models.CharField(max_length=200, unique=True)
    resource = models.ForeignKey(Resource,on_delete=models.CASCADE)
    request_data = models.TextField()
    request_method = models.ForeignKey(RequestMethod,on_delete=models.CASCADE)
    response_data = models.TextField()
    request_header_status = models.ForeignKey(RequestHeaderStatus,on_delete=models.CASCADE)
    response_header_status = models.ForeignKey(ResponseHeaderStatus,on_delete=models.CASCADE)
    url = models.CharField(max_length=1024, default="")
    def __str__(self):
        return self.name +"=>" +str(self.resource)
    def clean(self):
        try:
            json.loads(self.request_data)
        except Exception as e:
            raise ValidationError("Reequest Json Error " + str(e))
        try:
            json.loads(self.response_data)
        except Exception as e:
            raise ValidationError("Response Json Error " + str(e))
"""
# Hub (package)

 

## Group Team  (Group inside package folder)

 

### Cycles [/api/hub/team/{id}/cycle]   [Rsource]

 
##### Action1 



##### ACtions2 



#### Cycles for Team [GET]  ACtion :   <Action> for <Resource> (GET|POST|)
+ Response 200 (application/json)      (+ Response 200 (application/json)       | 201 |)

 

        [                                json
            {
                "id": 1,
                "code": "ctl1",
                "name: "cycle one"
            },
"""