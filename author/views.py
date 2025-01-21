from django.shortcuts import render

# Create your views here.

def author_dashboard(request):
    return render(request, 'author/admin_dashboard.html')

def author_content(request):
    return render(request, 'author/admin_content.html')

def author_analytics(request):
    return render(request, 'author/admin_analytics.html')

def author_community(request):
    return render(request, 'author/admin_community.html')

def author_earn(request):
    return render(request, 'author/admin_earn.html')

def author_copyright(request):
    return render(request, 'author/admin_copyright.html')

def content_details(request):
    return render(request, 'author/content_details.html')

def content_analytics(request):
    return render(request, 'author/content_analytics.html')

def content_comments(request):
    return render(request, 'author/content_comments.html')

def content_copyright(request):
    return render(request, 'author/content_copyright.html')

def content_translate(request):
    return render(request, 'author/content_translate.html')

