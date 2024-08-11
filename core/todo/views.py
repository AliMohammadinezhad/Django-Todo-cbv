from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from .models import Todo


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = "todo/index.html"
    context_object_name = "todos"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ["name"]
    context_object_name = "todo"
    success_url = reverse_lazy("todo:todo-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ["name"]
    success_url = reverse_lazy("todo:todo-list")
    template_name = "todo/update.html"


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    context_object_name = "todo"
    success_url = reverse_lazy("todo:todo-list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TodoCompleteView(LoginRequiredMixin, View):
    model = Todo
    success_url = reverse_lazy("todo:todo-list")

    def get(self, request, *args, **kwargs):
        object = Todo.objects.get(id=kwargs.get("pk"))
        object.status = True
        object.save()
        return redirect(self.success_url)
