from django import forms
from . import models

# Usuario
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = models.Usuario
        fields = ['nome', 'email', 'telefone', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Nome completo',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'seuemail@exemplo.com',
                'autocomplete': 'email',
            }),
            'telefone': forms.TextInput(attrs={
                'placeholder': '(11) 91234-5678',
                'autocomplete': 'tel',
            }),
        }
        error_messages = {
            'email': {
                'unique': "Já existe um usuário cadastrado com este e-mail.",
            },
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '').strip()
        if len(nome) < 3:
            raise forms.ValidationError(
                "O nome deve ter pelo menos 3 caracteres."
            )
        return nome

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        return email

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone', '').strip()
        return telefone

# Pet
class PetForm(forms.ModelForm):
    class Meta:
        model = models.Pet
        fields = ['nome', 'data_de_nascimento', 'raca', 'porte', 'observacao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Nome do pet',
                'autocomplete': 'name',
            }),

            'data_de_nascimento': forms.DateInput(attrs={
                'type': 'date',
                'max': '2099-12-31',
            }),

            'raca': forms.TextInput(attrs={
                'placeholder': 'Raça do pet',
            }),

            'porte': forms.Select(),

            'observacao': forms.Textarea(attrs={
                'placeholder': 'Observações sobre o pet',
                'rows': 4,
            }),
        }


    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '').strip()
        if len(nome) < 3:
            raise forms.ValidationError(
                "O nome deve ter pelo menos 3 caracteres."
            )
        return nome
    
    def clean_data_de_nascimento(self):
        data_de_nascimento = self.cleaned_data.get("data_de_nascimento")
        if data_de_nascimento and data_de_nascimento > date.today():
            raise forms.ValidationError(
                "A data de nascimento não pode ser no futuro."
            )
        return data_de_nascimento 


    