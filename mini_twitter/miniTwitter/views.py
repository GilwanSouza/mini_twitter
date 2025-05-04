from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tweet, CustomUser
from .forms import TweetForm, CustomUserForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

def index(request):
    tweets = Tweet.objects.select_related('user').order_by('-criado_em')
    return render(request, 'index.html', {'tweets': tweets})

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
    tweet = get_object_or_404(Tweet, id=tweet_id, autor=request.user)
    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')
        tweet.conteudo = conteudo
        tweet.save()
        return redirect('index')
    return render(request, 'editar_tweet.html', {'tweet': tweet})

@login_required
def excluir_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, autor=request.user)
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
