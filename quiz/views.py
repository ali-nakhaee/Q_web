from django.shortcuts import render


def index(request):
    """The home page for Q_web."""
    return render(request, 'quiz/index.html')
