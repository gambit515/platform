from django.shortcuts import render

def video_page(request):
    return render(request, 'videoapp/scary.html')


def math_anal(request):
    return render(request, 'videoapp/video_page.html')