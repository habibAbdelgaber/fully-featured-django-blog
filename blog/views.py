from django.shortcuts import  render
# "files.associations": {
#     "**/*.html": "html",
#     "**/templates/**/*.html": "django-html",
#     "**/templates/**/*": "django-txt",
#     "**/requirements{/**,*}.{txt,in}": "pip-requirements"
# },
def index(request):
    return render(request, 'posts/index.html')