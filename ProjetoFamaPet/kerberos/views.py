from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime
 
from .models import Usuario, Pet, Servico, Endereco, Agendamento
from .forms import UsuarioForm, PetForm, EnderecoForm, ServicoForm, AgendamentoForm
 
# Faixas de horário usadas para agrupar os agendamentos do dia
HORARIO_MANHA = ('09:00', '12:00')
HORARIO_TARDE = ('13:00', '18:00')
HORARIO_NOITE = ('19:00', '21:00')
 
 
def home(request):
    return render(request, 'home/index.html')
 
 
# ---------------------------------------------------------------------------
# Usuário
# ---------------------------------------------------------------------------
 
def listar_clientes(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuario/clientes.html', {'usuarios': usuarios})
 
 
def usuario_criar(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = UsuarioForm()
    return render(request, 'usuario/usuario_form.html', {'form': form})
 
 
def usuario_editar(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuario/usuario_form.html', {'form': form, 'usuario': usuario})
 
 
def usuario_excluir(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_clientes')
    return render(request, 'usuario/usuario_confirm_delete.html', {'usuario': usuario})
 
 
# ---------------------------------------------------------------------------
# Pet
# ---------------------------------------------------------------------------
 
def listar_pets(request):
    pets = Pet.objects.select_related('usuario').all()
    return render(request, 'pet/pets.html', {'pets': pets})
 
 
def pet_criar(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.usuario = usuario
            pet.save()
            return redirect('listar_pets')
    else:
        form = PetForm()
    return render(request, 'pet/pet_form.html', {'form': form, 'usuario': usuario})
 
 
def pet_editar(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('listar_pets')
    else:
        form = PetForm(instance=pet)
    return render(request, 'pet/pet_form.html', {'form': form, 'pet': pet})
 
 
def pet_excluir(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':
        pet.delete()
        return redirect('listar_pets')
    return render(request, 'pet/pet_confirm_delete.html', {'pet': pet})
 
 
# ---------------------------------------------------------------------------
# Endereço
# ---------------------------------------------------------------------------
 
def listar_enderecos(request):
    enderecos = Endereco.objects.all()
    return render(request, 'endereco/enderecos.html', {'enderecos': enderecos})
 
 
def endereco_criar(request):
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_enderecos')
    else:
        form = EnderecoForm()
    return render(request, 'endereco/endereco_form.html', {'form': form})
 
 
def endereco_editar(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk)
    if request.method == 'POST':
        form = EnderecoForm(request.POST, instance=endereco)
        if form.is_valid():
            form.save()
            return redirect('listar_enderecos')
    else:
        form = EnderecoForm(instance=endereco)
    return render(request, 'endereco/endereco_form.html', {'form': form, 'endereco': endereco})
 
 
def endereco_excluir(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk)
    if request.method == 'POST':
        endereco.delete()
        return redirect('listar_enderecos')
    return render(request, 'endereco/endereco_confirm_delete.html', {'endereco': endereco})
 
 
# ---------------------------------------------------------------------------
# Serviço
# ---------------------------------------------------------------------------
 
def listar_servicos(request):
    servicos = Servico.objects.all()
    return render(request, 'servico/servicos.html', {'servicos': servicos})
 
 
def servico_criar(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_servicos')
    else:
        form = ServicoForm()
    return render(request, 'servico/servico_form.html', {'form': form})
 
 
def servico_editar(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            return redirect('listar_servicos')
    else:
        form = ServicoForm(instance=servico)
    return render(request, 'servico/servico_form.html', {'form': form, 'servico': servico})
 
 
def servico_excluir(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        servico.delete()
        return redirect('listar_servicos')
    return render(request, 'servico/servico_confirm_delete.html', {'servico': servico})
 
 
# ---------------------------------------------------------------------------
# Relatório
# ---------------------------------------------------------------------------
 
def relatorio(request):
    agendamentos_qs = Agendamento.objects.prefetch_related('servicos').select_related('usuario', 'pet')
    faturamento = sum((agendamento.valor_total for agendamento in agendamentos_qs), start=0)
    contexto = {
        'relatorio': agendamentos_qs,
        'faturamento': faturamento,
    }
    return render(request, 'relatorio/relatorio.html', contexto)
 
 
# ---------------------------------------------------------------------------
# Agendamento
# ---------------------------------------------------------------------------
 
def agendamentos(request):
    data_str = request.GET.get('data')
 
    if data_str:
        try:
            data_selecionada = datetime.strptime(data_str, '%Y-%m-%d').date()
        except ValueError:
            data_selecionada = timezone.now().date()
    else:
        data_selecionada = timezone.now().date()
 
    agendamentos_qs = (
        Agendamento.objects
        .prefetch_related('servicos')
        .select_related('usuario', 'pet')
        .filter(data__date=data_selecionada)
    )
 
    contexto = {
        'agendamentos': agendamentos_qs,
        'data_selecionada': data_selecionada,
        'agendamentos_manha': agendamentos_qs.filter(data__time__gte=HORARIO_MANHA[0], data__time__lt=HORARIO_MANHA[1]),
        'agendamentos_tarde': agendamentos_qs.filter(data__time__gte=HORARIO_TARDE[0], data__time__lt=HORARIO_TARDE[1]),
        'agendamentos_noite': agendamentos_qs.filter(data__time__gte=HORARIO_NOITE[0], data__time__lte=HORARIO_NOITE[1]),
    }
 
    return render(request, 'agendamento/agendamentos.html', contexto)
 
 
def agendamento_criar(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, usuario=usuario)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.usuario = usuario
            agendamento.save()
            form.save_m2m()
            return redirect('agendamentos')
    else:
        form = AgendamentoForm(usuario=usuario)
    return render(request, 'agendamento/agendamento_form.html', {'form': form, 'usuario': usuario})
 
 
def agendamento_editar(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento, usuario=agendamento.usuario)
        if form.is_valid():
            form.save()
            return redirect('agendamentos')
    else:
        form = AgendamentoForm(instance=agendamento, usuario=agendamento.usuario)
    return render(request, 'agendamento/agendamento_form.html', {'form': form, 'agendamento': agendamento})
 
 
def agendamento_excluir(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    if request.method == 'POST':
        agendamento.delete()
        return redirect('agendamentos')
    return render(request, 'agendamento/agendamento_confirm_delete.html', {'agendamento': agendamento})
 

















































