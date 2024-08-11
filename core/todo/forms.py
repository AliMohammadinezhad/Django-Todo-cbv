from django import forms

from .models import Todo


class TodoForm(forms.ModelForm):
    title = forms.CharField(max_length=512)

    class Meta:
        model = Todo
        fields = ("name",)
