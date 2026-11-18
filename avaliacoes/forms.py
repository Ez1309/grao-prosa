from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("nota", "comentario")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nota"].widget = forms.Select(
            choices=tuple(
                (i, f"{i} {'Estrela' if i == 1 else 'Estrelas'}")
                for i in range(5, 0, -1)
            ),
            attrs={"class": "form-select"},
        )
        self.fields["comentario"].widget = forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Descreva sua percepção sensorial (aroma, corpo, acidez, retrogosto)...",
            }
        )
