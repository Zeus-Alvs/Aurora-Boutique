from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=150)
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)
    imagem_url = models.URLField(max_length=500, blank=True, null=True)
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Contato(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField()
    assunto = models.CharField(max_length=100)
    mensagem = models.TextField()

    def __str__(self):
        return self.nome

class Compra(models.Model):
    # Relacionamento com o usuário que comprou
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    # Relacionamento com o produto comprado
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    preco_na_epoca = models.DecimalField(max_digits=10, decimal_places=2)
    data_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra {self.id} - {self.cliente.username} comprou {self.produto.nome}"