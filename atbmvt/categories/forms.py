from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):

    name = forms.CharField(
        label="Category Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Category Name'
        })
    )

    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Category Description'
        })
    )

    image = forms.ImageField(
        label="Image",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Category
        fields = ('name', 'description', 'image')

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if Category.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Category already exists")

        return name