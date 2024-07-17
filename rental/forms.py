from django import forms
from .models import Drone

INPUT_CLASSES='w-full py-4 px-6 rounded-xl border'

class NewDroneForm(forms.ModelForm):
    class Meta:
        model=Drone
        fields=('brand','model','category','weight','image')
        widgets={          
            'brand': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'model': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'weight': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
        }