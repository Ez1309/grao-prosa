from django import forms

from .models import Cafe, Marca


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ("nome", "pais_origem", "historia", "site_oficial")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nome"].widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex: Orfeu, Dengo, Coffee Lab...",
            }
        )
        self.fields["pais_origem"].widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex: Brasil, Colômbia, Etiópia...",
            }
        )
        self.fields["historia"].widget = forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "História, origens ou filosofia da marca produtora...",
            }
        )
        self.fields["site_oficial"].widget = forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": "https://www.marca.com.br",
            }
        )


class CafeForm(forms.ModelForm):
    class Meta:
        model = Cafe
        fields = (
            "nome",
            "marca",
            "tipo_grao",
            "tipo_torra",
            "intensidade",
            "origem_grao",
            "notas_aromaticas",
            "descricao",
            "imagem",
            "destaque",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nome"].widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex: Bourbon Amarelo, Mogiana Especial...",
            }
        )
        self.fields["marca"].widget = forms.Select(
            attrs={"class": "form-select"}
        )
        self.fields["marca"].empty_label = "Selecione a marca produtora"

        self.fields["tipo_grao"].widget = forms.Select(
            attrs={"class": "form-select"}
        )
        self.fields["tipo_torra"].widget = forms.Select(
            attrs={"class": "form-select"}
        )
        self.fields["intensidade"].widget = forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": 1,
                "max": 10,
                "placeholder": "Escala de 1 a 10",
            }
        )
        self.fields["origem_grao"].widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex: Sul de Minas, Mogiana Paulista, Cerrado...",
            }
        )
        self.fields["notas_aromaticas"].widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex: Chocolate amargo, caramelo, frutas vermelhas...",
            }
        )
        self.fields["descricao"].widget = forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Descrição sensorial detalhada, processo de colheita e secagem...",
            }
        )
        self.fields["imagem"].widget = forms.ClearableFileInput(
            attrs={"class": "form-control"}
        )
        self.fields["destaque"].widget = forms.CheckboxInput(
            attrs={"class": "form-check-input"}
        )
