# todos/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TodoItem
from .forms import TodoForm # Crearemos TodoForm más adelante

@login_required
def todo_list(request):
    todos = TodoItem.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'todos/todo_list.html', {'todos': todos})

@login_required
def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todos/add_todo.html', {'form': form})

@login_required
def edit_todo(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/edit_todo.html', {'form': form})

@login_required
def delete_todo(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'todos/delete_todo.html', {'todo': todo})

@login_required
def toggle_todo(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')