from django.shortcuts import render
# from .models import Menu

# Create your views here.
# def menu(request):
#     menu_data = Menu.objects.all()
#     main_data = {'menu': menu_data}
#     return render(request, 'menu.html', {"menu": main_data})

def index(request):
    return render(request, 'index.html', {})