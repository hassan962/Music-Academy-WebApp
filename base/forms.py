from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Course, Lesson, LiveClass
from django.forms.widgets import DateTimeInput

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = [ 'first_name', 'last_name','username', 'email', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'video', 'material']


class LiveClassForm(forms.ModelForm):
    class Meta:
        model = LiveClass
        fields = ['course', 'title', 'description', 'scheduled_datetime', 'meeting_link']
        widgets = {
            'scheduled_datetime': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LiveClassForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['course'].queryset = Course.objects.filter(teacher=user)
