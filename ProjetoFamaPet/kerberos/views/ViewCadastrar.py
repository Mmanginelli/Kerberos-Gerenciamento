from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms.FormUsuario import UsuarioForm
from ..forms.FormPet import PetForm
from ..models.usuario import Usuario
from ..models.pet import Pet

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça seu login.')
            return redirect('login')
    else:
        form = UsuarioForm()
    
    return render(request, 'cadastro/cadastro.html', {'form': form})