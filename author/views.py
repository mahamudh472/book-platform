from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='accounts:login')
def author_dashboard(request):
    return render(request, 'author/admin_dashboard.html')

@login_required(login_url='accounts:login')
def author_content(request):
    return render(request, 'author/admin_content.html')

@login_required(login_url='accounts:login')
def author_analytics(request):
    return render(request, 'author/admin_analytics.html')

@login_required(login_url='accounts:login')
def author_community(request):
    return render(request, 'author/admin_community.html')

@login_required(login_url='accounts:login')
def author_earn(request):
    return render(request, 'author/admin_earn.html')

@login_required(login_url='accounts:login')
def author_copyright(request):
    return render(request, 'author/admin_copyright.html')

@login_required(login_url='accounts:login')
def content_details(request):
    return render(request, 'author/content_details.html')

@login_required(login_url='accounts:login')
def content_analytics(request):
    return render(request, 'author/content_analytics.html')

@login_required(login_url='accounts:login')
def content_comments(request):
    return render(request, 'author/content_comments.html')

@login_required(login_url='accounts:login')
def content_copyright(request):
    return render(request, 'author/content_copyright.html')

@login_required(login_url='accounts:login')
def content_translate(request):
    return render(request, 'author/content_translate.html')

