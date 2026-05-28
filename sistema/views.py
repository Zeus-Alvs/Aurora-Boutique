from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UsuarioForm, ContatoForm, CategoriaForm, ProdutoForm, EditarUsuarioForm
from .models import Produto, Categoria, Contato, Compra
from django.contrib.auth.models import User
from core.settings import db_nosql
from datetime import datetime
import requests
from django.http import JsonResponse
from django.db.models import Sum, F

def is_admin(user):
    return user.is_superuser





def index(request):
    avaliacoes = []
    try:

        docs = db_nosql.collection('avaliacoes').limit(3).stream()
        for doc in docs:
            avaliacoes.append(doc.to_dict())
    except Exception as e:
        print(f"Erro ao ligar ao Firebase: {e}")

    return render(request, 'index.html', {'avaliacoes': avaliacoes})

def criar_conta(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro concluído! Faça seu login abaixo.', extra_tags='alerta_login')
            return redirect('login')
    else:
        form = UsuarioForm()
    return render(request, 'criar_conta.html', {'form': form})

def quem_somos(request):
    return render(request, 'quem_somos.html')

def adicionar_contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensagem enviada com sucesso!')
            return redirect('index')
    else:
        form = ContatoForm()
    return render(request, 'contato.html', {'form': form})




@login_required
def perfil(request):
    return render(request, 'perfil.html')

@login_required
def alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Senha atualizada com sucesso!')
            return redirect('perfil')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'alterar_senha.html', {'form': form})






@user_passes_test(is_admin, login_url='index')
def dashboard(request):
    return render(request, 'dashboard.html')

@user_passes_test(is_admin, login_url='index')
def listar_contatos(request):
    contatos = Contato.objects.all()
    return render(request, 'listar_contatos.html', {'contatos': contatos})

@user_passes_test(is_admin, login_url='index')
def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'listar_categorias.html', {'categorias': categorias})

@user_passes_test(is_admin, login_url='index')
def adicionar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'adicionar_categoria.html', {'form': form})

@user_passes_test(is_admin, login_url='index')
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'editar_categoria.html', {'form': form})

@user_passes_test(is_admin, login_url='index')
def excluir_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('listar_categorias')
    return render(request, 'excluir_categoria.html', {'categoria': categoria})

@user_passes_test(is_admin, login_url='index')
def excluir_contato(request, id):
    contato = get_object_or_404(Contato, id=id)
    if request.method == 'POST':
        contato.delete()
        return redirect('listar_contatos')
    return render(request, 'excluir_contato.html', {'contato': contato})

@user_passes_test(is_admin, login_url='index')
def listar_produtos(request):
    produtos = Produto.objects.select_related('categoria').all()
    return render(request, 'listar_produtos.html', {'produtos': produtos})

@user_passes_test(is_admin, login_url='index')
def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'adicionar_produto.html', {'form': form})

@user_passes_test(is_admin, login_url='index')
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'editar_produto.html', {'form': form, 'produto': produto})

@user_passes_test(is_admin, login_url='index')
def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.delete()
        return redirect('listar_produtos')
    return render(request, 'excluir_produto.html', {'produto': produto})

@user_passes_test(is_admin, login_url='index')
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

@user_passes_test(is_admin, login_url='index')
def editar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = EditarUsuarioForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form})

@user_passes_test(is_admin, login_url='index')
def excluir_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuarios')
    return render(request, 'excluir_usuario.html', {'usuario': usuario})

@login_required
def comprar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)


    if produto.quantidade > 0:

        Compra.objects.create(
            cliente=request.user,
            produto=produto,
            quantidade=1,
            preco_na_epoca=produto.preco
        )


        produto.quantidade -= 1
        produto.save()

        messages.success(request, f'Compra do produto {produto.nome} realizada com sucesso!')
    else:
        messages.error(request, 'Lamentamos, mas este produto está esgotado!')


    return redirect('perfil')


@login_required
def perfil(request):
    compras = Compra.objects.filter(cliente=request.user).order_by('-data_compra')
    return render(request, 'perfil.html', {'compras': compras})

def vitrine_produtos(request):
    produtos = Produto.objects.filter(quantidade__gt=0)
    return render(request, 'vitrine_produtos.html', {'produtos_locais': produtos})


@user_passes_test(is_admin, login_url='index')
def sincronizar_api(request):

    categoria_api, created = Categoria.objects.get_or_create(nome="Alta Joalheria (API)")

    try:

        resposta = requests.get('https://fakestoreapi.com/products/category/jewelery', timeout=5)
        if resposta.status_code == 200:
            produtos_api = resposta.json()


            for item in produtos_api:

                if not Produto.objects.filter(nome=item['title']).exists():
                    Produto.objects.create(
                        nome=item['title'],
                        preco=item['price'],
                        quantidade=15,
                        categoria=categoria_api,
                        imagem_url=item['image']
                    )
            messages.success(request, "Joias da API importadas com sucesso para o banco de dados!")
    except Exception as e:
        messages.error(request, f"Erro ao conectar com a API: {e}")

    return redirect('listar_produtos')




@user_passes_test(is_admin, login_url='index')
def listar_compras(request):
    compras = Compra.objects.select_related('cliente', 'produto').all().order_by('-data_compra')
    return render(request, 'listar_compras.html', {'compras': compras})

@user_passes_test(is_admin, login_url='index')
def excluir_compra(request, id):
    compra = get_object_or_404(Compra, id=id)
    if request.method == 'POST':

        compra.produto.quantidade += compra.quantidade
        compra.produto.save()
        compra.delete()
        return redirect('listar_compras')
    return render(request, 'excluir_compra.html', {'compra': compra})

@login_required
def avaliar_compra(request, compra_id):

    compra = get_object_or_404(Compra, id=compra_id, cliente=request.user)

    if request.method == 'POST':
        nota = request.POST.get('nota')
        comentario = request.POST.get('comentario')


        dados_avaliacao = {
            'compra_id': compra.id,
            'cliente_nome': request.user.username,
            'produto_nome': compra.produto.nome,
            'nota': int(nota),
            'comentario': comentario,
            'data_avaliacao': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


        db_nosql.collection('avaliacoes').add(dados_avaliacao)

        messages.success(request, 'Avaliação submetida com sucesso!')
        return redirect('perfil')

    return render(request, 'avaliar.html', {'compra': compra})

@user_passes_test(is_admin, login_url='index')
def listar_avaliacoes(request):
    avaliacoes = []
    try:
        docs = db_nosql.collection('avaliacoes').stream()
        for doc in docs:
            dados = doc.to_dict()
            dados['id'] = doc.id
            avaliacoes.append(dados)
    except Exception as e:
        print(f"Erro ao ligar ao Firebase: {e}")

    return render(request, 'listar_avaliacoes.html', {'avaliacoes': avaliacoes})

@user_passes_test(is_admin, login_url='index')
def excluir_avaliacao(request, id):

    if request.method == 'POST':
        db_nosql.collection('avaliacoes').document(id).delete()
        return redirect('listar_avaliacoes')
    return render(request, 'excluir_avaliacao.html', {'id': id})


@user_passes_test(is_admin, login_url='index')
def adicionar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'adicionar_usuario.html', {'form': form})

@user_passes_test(is_admin, login_url='index')
def relatorio_vendas(request):
    return render(request, 'relatorio_vendas.html')

@user_passes_test(is_admin, login_url='index')
def api_dados_vendas(request):
    # Agrupa as compras pelo nome do produto e soma o (quantidade * preco)
    vendas = Compra.objects.values('produto__nome').annotate(
        faturamento=Sum(F('quantidade') * F('preco_na_epoca'))
    )
    
    labels = []
    valores = []
    
    for venda in vendas:
        labels.append(venda['produto__nome'])
        valores.append(float(venda['faturamento']))
        
    return JsonResponse({
        'labels': labels,
        'valores': valores
    })
