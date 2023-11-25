from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>First Wellcome Page</h1>")