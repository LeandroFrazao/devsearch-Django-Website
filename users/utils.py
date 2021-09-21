from django.db.models import Q
from .models import Profile, Skill


def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)
        
    profiles = Profile.objects.distinct().filter(
    Q(name__icontains=search_query) | 
    Q(short_intro__icontains=search_query) | 
    Q(bio__icontains = search_query)|
    Q(skill__in=skills)
    )    
    #else:
    #   profiles = Profile.objects.all()

    return profiles, search_query