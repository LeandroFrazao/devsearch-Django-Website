from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import Project
from .utils import searchProjects, paginateProjects
from .forms import ProjectForm
from django.http import HttpResponse

def projects(request):
    #return HttpResponse("Here are our projects")
    
    #Search projects
    projects, search_query = searchProjects(request)
    #exclude projects with userID null
    projects = projects.exclude(owner__isnull=True) 
 
    #pagination projects
    results = 3
    custom_range, projects = paginateProjects(request, projects, results)
    
    context = {'projects': projects, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    #return HttpResponse("Single Project" +" "+ str(pk))

    projectObj = Project.objects.get(id=pk) 
    context = {'project': projectObj}
    return render(request,'projects/single-project.html', context )

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context={'form':form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    try:
        project = profile.project_set.get(id=pk )
    except:
        messages.error(request,"Project not found")
        return redirect('account')
    
    form = ProjectForm(instance= project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance = project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context={'form':form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    try:
        project = profile.project_set.get(id=pk )
    except:
        messages.error(request,"Project not found")
        return redirect('account')

    if request.method == 'POST':
        project.delete()
        return redirect('account')

    context={'object':project}
    return render(request, 'delete_template.html', context)
