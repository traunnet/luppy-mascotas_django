from django.shortcuts import render
from .models import TipoServicio
# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def inicioServ(request):
    servs = TipoServicio.objects.all()
    return render(request, 'inicioServ.html', {"servs": servs})