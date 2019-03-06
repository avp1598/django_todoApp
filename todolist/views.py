from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
import datetime
from .models import Todo
from django.conf import settings

def index(request):
    todos = Todo.objects.all()[:10]

    context = {
        'todos':todos
    }
    for todo in todos:
        if(todo.time==datetime.datetime.now() and not todo.complete):
            subject = 'todo check'
            message = ' check complete '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['nakulparmar15@gmail.com',]
            send_mail( subject, message, email_from, recipient_list )

    return render(request, 'index.html', context)

def details(request, id):
    todo = Todo.objects.get(id=id)

    context = {
        'todo':todo
    }
    return render(request, 'details.html', context)

def add(request):
    if(request.method == 'POST'):
        title = request.POST['title']
        text = request.POST['text']
        time = request.POST['time']
        complete = request.get('cm', False)
        if(complete=="on"): complete=True
        else: complete=False

        todo = Todo(title=title, text=text,time=time,complete=complete)
        todo.save()

        return redirect('/todos')
    else:
        return render(request, 'add.html')

def delete(request,id):
    Todo.objects.get(id=id).delete()
    return redirect('/todos')

def update(request, id):
    if(request.method == 'POST'):
        todo = Todo.objects.get(id=id)
        todo.title = request.POST['title']
        todo.text = request.POST['text']
        todo.time = request.POST['time']
        complete = request.POST.get('cm', False)
        print("c==",complete)
        if(complete=="on"): complete=True
        else: complete=False

        todo.complete=complete
        todo.save()
        return redirect('/todos')
    else:
        todo = Todo.objects.get(id=id)
        context = {
            'todo':todo
        }
        return render(request, 'update.html',context)
