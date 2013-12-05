from django.shortcuts import render
from django.contrib.auth import (
    authenticate as django_auth,
    login as django_login,
    logout as django_logout
)
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from playerproject.apps.accounts.models import PPUser
from playerproject.apps.dashboard.models import (
    PPUserRecord,
    PPHockeyPlayerStats,
    PPPlayerStats
)
from playerproject.apps.dashboard.forms import PPUserRecordForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def home(request):
    return render(request, 'dashboard/home.html')


@login_required
def manager(request):
	playerrecords = PPUserRecord.objects.filter(recorded_by = request.user.id).order_by('time_modified')
	paginator = Paginator(playerrecords, 20) # Show 20 contacts per page
	page = request.GET.get('page')
	try:
		records = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
		records = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
		records = paginator.page(paginator.num_pages)

	return render(request,'dashboard/records.html', { 'records': records, 'paginator': paginator })


@login_required
def manager_add(request):
    if request.POST:
        form = PPUserRecordForm(request.POST)
        if form.is_valid():
            # commit=False means the form doesn't save at this time.
            # commit defaults to True which means it normally saves.
            item = form.save(commit=False)
            item.recorded_by = request.user
            item.save()
            #redirect
            return HttpResponseRedirect(reverse('dashboard_manager'))
        else:
            print('error')
            #failed
    else:
        form = PPUserRecordForm()

    return render(request, 'dashboard/recordadd.html', { 'form':form })


@login_required
def player(request, player_id):
    basicinfo =  PPUserRecord.objects.get(id = player_id)
    stats = PPPlayerStats.objects.get(id = player_id)
    hockeystats = PPHockeyPlayerStats.objects.get(ppplayerstats_ptr_id = player_id)
    return render(request, 'dashboard/player.html', {'basicinfo' : basicinfo, 'stats': stats , 'hockeystats': hockeystats} )



