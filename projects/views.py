import re;
from importlib.metadata import requires
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Prefetch


from .models import Project, Tag
from .utils import searchProjects, paginateProjects
from .forms import ProjectForm, ReviewForm
from django.http import HttpResponse

def projects(request):
    #return HttpResponse("Here are our projects")
    
    #Search projects
    projects, search_query = searchProjects(request)
    #exclude projects with userID null
    projects = projects.exclude(owner__isnull=True) 
 
    #pagination projects
    results = 6
    custom_range, projects = paginateProjects(request, projects, results)
    
    context = {'projects': projects, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    #return HttpResponse("Single Project" +" "+ str(pk))

    projectObj = Project.objects.get(id=pk) 
    form = ReviewForm()

    if request.method =='POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        #update project vote count
        projectObj.getVoteCount
        
        messages.success(request, 'Your review was successfully submited!')
        return redirect('project', pk = projectObj.id)


    context = {'project': projectObj, 'form':form}
    return render(request,'projects/single-project.html', context )

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    
    #get all distinct tags used by the User on their other projects.
    tagsId = Project.objects.filter(owner=profile.id).values_list('tags', flat=True).exclude(tags__isnull=True).order_by().distinct()
    otherTags = Tag.objects.filter(id__in=tagsId)
    
    if request.method == 'POST':
        newtags = request.POST.get('newtags')
        #remove non word characters
        newtags = re.sub('[^A-Za-z0-9-]+', " ", newtags).split()

        #get selected tags
        tagsChecked = request.POST.getlist('tags')
        
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            project.tags.set(tagsChecked)
            for tag in newtags:
                tag,created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')

    context={'form':form, 'otherTags':otherTags}
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
    
    #get all distinct tags used by the User on their other projects.
    tagsId = Project.objects.filter(owner=profile.id).values_list('tags', flat=True).exclude(tags__isnull=True).order_by().distinct()
    otherTags = Tag.objects.filter(id__in=tagsId).exclude( id__in=project.tags.all())
    

    if request.method == 'POST':
        newtags = request.POST.get('newtags')
        #remove non word characters
        newtags = re.sub('[^A-Za-z0-9-]+', " ", newtags).split()
        
        #get selected tags
        tagsChecked = request.POST.getlist('tags')
        
        form = ProjectForm(request.POST, request.FILES, instance = project)
        if form.is_valid():      
            project = form.save()
            project.tags.set(tagsChecked)
            for tag in newtags:
                tag,created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            
            #list of tags used in all projects
            allUsedTags = Project.objects.all().values_list('tags', flat=True).exclude(tags__isnull=True).order_by().distinct()
            #list of tags not linked to any project, then delete them.
            unusedTags = Tag.objects.all().exclude(id__in=allUsedTags)
            unusedTags.delete()

            return redirect('account')

    context={'form':form, 'project':project, "otherTags":otherTags}
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
