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

# Endereço
class EnderecoForm(forms.ModelForm):
    class Meta:
        model = models.Endereco
        fields = ['rua', 'numero', 'bairro', 'cep']
        widgets = {
            'rua': forms.TextInput(attrs={
                'placeholder': 'Rua/Avenida',
                'autocomplete': 'street-address',
            }),
            'numero': forms.NumberInput(attrs={
                'placeholder': 'Número',
                'min': 1,
            }),
            'bairro': forms.TextInput(attrs={
                'placeholder': 'Bairro',
                'autocomplete': 'address-level2',
            }),
            'cep': forms.TextInput(attrs={
                'placeholder': '00000-000',
                'maxlength': 9,
            }),
        }

    def clean_cep(self):
        cep = self.cleaned_data.get("cep", "").strip()

        cep_numeros = "".join(filter(str.isdigit, cep))

        if len(cep_numeros) != 8:
            raise forms.ValidationError("O CEP deve conter 8 dígitos.")

        return f"{cep_numeros[:5]}-{cep_numeros[5:]}"

    def clean_numero(self):
        numero = self.cleaned_data.get("numero")

        if numero is not None and numero <= 0:
            raise forms.ValidationError(
                "O número deve ser maior que zero."
            )

        return numero

class ServicoForm(forms.ModelForm):
    class Meta:
        model = models.Servico
        field = ['nome', 'descricao', 'valor']
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Nome do Serviço',
            }),
            'descricao': forms.TextInput(attrs={
                'placeholder': 'Descrição do Produto',
            }),
            'valor': forms.NumberInput(attrs={
                'placeholder': 'Valor do Serviço',
                'step': '0.01',
                'min': '0',
            }),
        }

