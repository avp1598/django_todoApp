from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from datetime import datetime, timezone, timedelta
from .models import Todo
from django.conf import settings
from django.contrib import messages

def index(request):
    todos = Todo.objects.all()

    context = {
        'todos':todos
    }
    for todo in todos:
        if(todo.time==datetime.now() and not todo.complete):
            subject = 'todo check'
            message = ' check complete '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['nakulparmar15@gmail.com']
            send_mail( subject, message, email_from, recipient_list ) #Mailing user 

        c=todo.time-datetime.now(timezone.utc)
        timedelta(0, 8, 562000)
        diff_seconds=divmod(c.days * 86400 + c.seconds, 60)
        #if 10 hours left for deadline alert user
        if(diff_seconds[0]<1230 and not todo.complete):  messages.info(request,'Your todos deadline is approaching!!!')

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
        complete = request.POST.get('cm', False)
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
