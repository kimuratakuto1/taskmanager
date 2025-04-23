from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, TaskTemplate
from django.utils import timezone
from django.utils.timezone import now


#タスク追加
def task_list(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        date = request.POST.get("date")
        task_type = request.POST.get("task_type")
        if title:
            if task_type == "daily":
                TaskTemplate.objects.create(title=title, description=description, is_daily=True)
            else:
                Task.objects.create(title=title, description=description, date=date)
            return redirect('/')
    incomplete_tasks = Task.objects.filter(is_done=False)
    today = now().date()
    completed_today_tasks = Task.objects.filter(is_done=True, completed_at__date=today)
    template_tasks = TaskTemplate.objects.all()
    return render(request, 'tasks/task_list.html', {
        'incomplete_tasks': incomplete_tasks,
        'completed_today_tasks': completed_today_tasks,
        'today': today,
        'template_tasks': template_tasks,
    })


#タスク編集
def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.save()
        return redirect('/')
    
    return render(request, 'tasks/task_edit.html', {'task': task})

#定型タスク編集
def template_task_edit(request, task_id):
    task = get_object_or_404(TaskTemplate, pk=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.save()
        return redirect('/')
    return render(request, 'tasks/template_task_edit.html', {'task': task})


#タスク消去
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('/')

    return render(request, 'tasks/task_delete.html', {'task': task})

#定型タスク消去
def template_task_delete(request, task_id):
    task = get_object_or_404(TaskTemplate, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request, 'tasks/template_task_delete.html', {'task': task})



#タスク完了
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.is_done = True
        task.completed_at = timezone.now()
        task.save()
        return redirect('/')


#業務開始
def start_of_day(request):
    if request.method == 'POST':
        print("POST request received")
        today = timezone.now().date()
        templates = TaskTemplate.objects.filter(is_daily=True)
        
        if not templates:
            print("No daily templates found")
        
        for template in templates:
            print(f"Checking task for: Title: {template.title}, Description: {template.description}, Date: {today}")
            
            # 既存のタスクがあるかどうか確認
            existing_task = Task.objects.filter(
                title=template.title,
                description=template.description,
                date=today
            ).exists()
            
            if not existing_task:
                print(f"Creating task: Title: {template.title}, Description: {template.description}, Date: {today}")
                Task.objects.create(
                    title=template.title,
                    description=template.description,
                    date=today
                )
            else:
                print(f"Task already exists for: {template.title}, {template.description}")
        
        print("Task creation process completed.")
        return redirect('/')  # トップページにリダイレクト



# 業務終了
def end_of_day(request):
    if request.method == 'POST':
        today = timezone.now().date()
        completed_tasks = Task.objects.filter(is_done=True, completed_at__date=today)
        report = "\n".join([task.title for task in completed_tasks])
        return render(request, 'tasks/end_of_day_report.html', {'report': report})