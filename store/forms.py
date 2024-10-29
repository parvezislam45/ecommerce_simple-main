# forms.py
from django import forms
from .models import Items

class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['title', 'slug', 'description', 'price', 'mainimage', 'subimage1', 'subimage2', 'subimage3','subimage4', 'subimage5', 'subimage6','subimage7', 'subimage8', 'desimage1', 'desimage2', 'desimage3', 'desimage4', 'desimage5', 'desimage6', 'desimage7', 'desimage8']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'block w-full p-4 text-gray-900 border border-gray-300 rounded-lg bg-gray-100 text-base focus:ring-blue-500 focus:border-blue-500'}),
            'slug': forms.TextInput(attrs={'class': 'block w-full p-4 text-gray-900 border border-gray-300 rounded-lg bg-gray-100 text-base focus:ring-blue-500 focus:border-blue-500'}),
            'description': forms.Textarea(attrs={
                'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full',
                'rows': 3,
                'oninput': 'this.style.height = ""; this.style.height = this.scrollHeight + "px"'  # This adjusts height dynamically
            }),
            'price': forms.NumberInput(attrs={'class': 'block w-full p-4 text-gray-900 border border-gray-300 rounded-lg bg-gray-100 text-base focus:ring-blue-500 focus:border-blue-500'}),
            'mainimage': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'subimage1': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'subimage2': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'subimage3': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'subimage4': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'subimage5': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'subimage6': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'subimage7': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'subimage8': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'desimage1': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'desimage2': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'desimage3': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'desimage4': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'desimage5': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'desimage6': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'desimage7': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'}),
            'desimage8': forms.FileInput(attrs={'class': 'bg-gray-300 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full h-10'})
        }