from django.shortcuts import render

from main.models import Experience, Projects

def show_main(request):
    context = {
        "name": "Alphard Qodaruddin",
        "npm": "2506632910",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "6 years of experience as an indie video game developer at AlphardZero Studios and an undergraduate Computer Science student at Universitas Indonesia."
        ),
    }
    return render(request, "index.html", context)

def show_experience(request):
    context = {
        "name": "Alphard Qodaruddin",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_projects(request):
    context = {
        "name": "Alphard Qodaruddin",
        "projects_list": Projects.objects.all(),
    }
    return render(request, "projects.html", context)