from fileinput import filename
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Lightning, LightningFiles
from modules.imports import handle_lighting_data


def index(request):
    context = {
        'page_title': 'Dashboard',
    }
    return render(request, 'dashboard.html', context)

def upload_lightning(request):
    if request.method == "POST" and request.FILES:
        csvs = request.FILES.getlist('files[]')

        for f in csvs:
            # save_lightning_data(f)
            obj  = LightningFiles.objects.create(filename=f, files= f)
            handle_lighting_data(obj)
        return redirect('upload-lightning')

    lighting_files = LightningFiles.objects.all()
    context = {
        'page_title': 'Upload Lightning Dataset',
        'page_desc': 'Upload lightning dataset with CSV format',
        'files': lighting_files,
    }

    return render(request, 'upload_lightning.html', context)

def detail_lightning(request, id_files):
    files_obj = LightningFiles.objects.get(id = id_files)
    lightning_obj = Lightning.objects.filter(files_id = id_files)

    context = {
        'page_title': files_obj,
        'lightnings' : lightning_obj
    }

    return render(request, 'detail_lightning.html', context)