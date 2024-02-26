from django import forms

from .models import Bottletext, Topic, Entry

class BottleForm(forms.ModelForm):
    class Meta:
        model = Bottletext
        fields = ['title', 'text', 'image', 'date_unlock']
        widgets = {
            'date_unlock': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        super(BottleForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

#心愿单
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry：'}
        widgets = {'text': forms.Textarea(attrs={'cols': 200})}