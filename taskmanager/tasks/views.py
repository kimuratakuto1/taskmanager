from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.utils import timezone


#タスクリスト
def task_list(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            Task.objects.create(title=title)
            return redirect('/')
        
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

#タスク編集
def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.save()
        return redirect('/')
    
    return render(request, 'tasks/task_edit.html', {'task': task})


#タスク消去
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('/')

    return render(request, 'tasks/task_delete.html', {'task': task})


#タスク完了
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.is_done = True
        task.completed_at = timezone.now()
        task.save()
        return redirect('/')


#業務終了
def end_of_day(request):
    if request.method == 'POST':
        today = timezone.now().date()
        completed_tasks = Task.objects.filter(is_done=True, completed_at__date=today)
        report = "\n".join([task.title for task in completed_tasks])
        return render(request, 'tasks/end_of_day_report.html', {'report': report})