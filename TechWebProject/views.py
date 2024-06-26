from django.http import HttpResponse


def home(request):
    if not request.user.is_authenticated:
        print('user not auth.')
    return HttpResponse("<h1>Hello Worldo</h1>")


def elenca_params(request):
    response = ""
    for k in request.GET:
        response += request.GET[k] + " "
    return HttpResponse(response)
