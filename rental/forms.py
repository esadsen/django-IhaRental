from django import forms
from .models import Drone,Rental

INPUT_CLASSES='w-full py-4 px-6 rounded-xl border'

class NewDroneForm(forms.ModelForm):
    class Meta:
        model=Drone
        fields=('brand','model','category','weight')
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
            
        }
        
class EditDroneForm(forms.ModelForm):
    class Meta:
        model=Drone
        fields=('brand','model','category','weight')
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
            
        }
        
class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['start_datetime', 'end_datetime']
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={
                'class': 'py-2 px-4 rounded-md border w-48', 
                'readonly': 'readonly'
            }),
            'end_datetime': forms.DateTimeInput(attrs={
                'class': 'py-2 px-4 rounded-md border w-48',  
                'readonly': 'readonly'
            }),
        }