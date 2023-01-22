from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return render(request,"twitter/index.html")

def actions(request):

    # Get start and end points
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))

    # Generate list of arbitrary data and pack it up and send it
    def generateData():
        return(["wertgvc","wertg","qazxw","poiuiolk"])

    data = []
    for i in range(start, end+1):
        data.append(generateData())

    return JsonResponse({
        "actions":data
    })


