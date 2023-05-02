from django.shortcuts import render

# Create your views here.


def handle_400_error(request, exception):
    return render(request, "helper/400.html")


def handle_403_error(request, exception):
    return render(request, "helper/403.html")


def handle_404_error(request, exception):
    return render(request, "helper/404.html")


def handle_500_error(request):
    return render(request, "helper/500.html")
