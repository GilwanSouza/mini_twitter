from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tweet, CustomUser
from .forms import TweetForm, CustomUserForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    tweets = Tweet.objects.select_related('user').order_by('-criado_em')
    paginator = Paginator(tweets, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'tweets': page_obj, 'page_obj': page_obj})

def perfil_usuario(request, username):
    perfil = get_object_or_404(CustomUser, username=username)
    tweets = Tweet.objects.filter(user=perfil).order_by('-criado_em')
    return render(request, 'perfil_usuario.html', {'perfil': perfil, 'tweets': tweets})

def feed(request):
    query = request.GET.get('q')
    tweets = Tweet.objects.all()

    if query: tweets = tweets.filter(Q(texto__icontains=query))

    tweets = tweets.order_by('-criado_em')
    paginator = Paginator(tweets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'page_obj': page_obj,'request': request})

@login_required
def seguir_usuario(request, username):
    alvo = get_object_or_404(CustomUser, username=username)
    request.user.seguindo.add(alvo)
    return redirect('perfil_usuario', username=username)

@login_required
def deixar_de_seguir(request, username):
    alvo = get_object_or_404(CustomUser, username=username)
    request.user.seguindo.remove(alvo)
    return redirect('perfil_usuario', username=username)

@login_required
def curtir_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.user in tweet.curtidas.all():
        tweet.curtidas.remove(request.user)
    else:
        tweet.curtidas.add(request.user)
    return redirect('index')

@login_required
def editar_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, user=request.user)
    if request.method == 'POST':
        conteudo = request.POST.get('texto')
        tweet.conteudo = conteudo
        tweet.save()
        return redirect('index')
    return render(request, 'editar_tweet.html', {'tweet': tweet})

@login_required
def excluir_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('index')
    return render(request, 'confirmar_exclusao.html', {'tweet': tweet})

@login_required
def post_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('index')
    else:
        form = TweetForm()
    return render(request, 'post.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username or not password:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Erro no cadastro. Verifique os dados informados.')
    else:
        form = CustomUserForm()

    return render(request, 'register.html', {'form': form})
