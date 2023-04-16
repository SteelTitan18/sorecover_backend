from django import forms
from recovering.models import *


class CommunityForm(forms.ModelForm):
    # use_required_attribute = False

    class Meta:
        model = Community
        fields = ['name', 'status', 'creator', 'members']
        widgets = {
            # 'title': forms.TextInput(attrs={'placeholder': 'Titre'}),
            # 'content': forms.Textarea(attrs={'placeholder': 'Contenu'}),
            'members': forms.CheckboxSelectMultiple()
        }
