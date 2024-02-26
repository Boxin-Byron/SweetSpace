from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('gender', 'user_lover',)

    def clean_user_lover(self):
        username = self.cleaned_data['user_lover']
        if username:
            try:
                user_lover = User.objects.get(username=username, user_lover__isnull=True)
                return user_lover
            except User.DoesNotExist:
                raise forms.ValidationError("This username does not exist or already has a lover.")
        return None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_lover'].label = '你的另一半'  