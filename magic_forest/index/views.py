from django.shortcuts import render
import json
from django.http import HttpResponse
from service import *
import matplotlib.colors as colors
# Create your views here.


def index(request):
    return render(request, "index.html")


def generate(request):
    return render(request,'generate.html')

def result(request):
    forest = TreeImage(
               count = int(request.POST['Trees_number']), 
               width = int(request.POST['Width']), 
               height = int(request.POST['Heigth']),
               trunk_color = np.array(colors.hex2color(request.POST['Trunk_color'])) * 255,
               leaf_color = np.array(colors.hex2color(request.POST['Leaf_color'])) * 255,
               background_color = tuple([int(255. * c) for c in colors.hex2color(request.POST['Background_color'])]) + 
                     (100 - int(request.POST['Background_transparency']),),
               color_std = float(request.POST['Color_std'])
             )
    im = forest.create() #.save('example.png',format = 'png',quality = 90)
    response =  HttpResponse(content_type="image/png")
    im.save('example.png',format = 'png')
    im.save(response, format = 'png')
    print('tree generation done')
    return response
    #return render(request,'polls/generate.html')

