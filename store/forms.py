# forms.py
from django import forms
from .models import Items

class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['title', 'slug', 'description', 'price', 'mainimage', 'subimage1', 'subimage2', 'subimage3', 'desimage1', 'desimage2', 'desimage3']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'slug': forms.TextInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'description': forms.Textarea(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'mainimage': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'subimage1': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'subimage2': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'subimage3': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'desimage1': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'desimage2': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'desimage3': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
        }
