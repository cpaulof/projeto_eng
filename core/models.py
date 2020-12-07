from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, email, user_type, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Usuário deve possuir um email')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            user_type=user_type,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, user_type=None, password=None, **extra_fields):
        return self._create_user(email, user_type, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, 1, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    TIPOS = {
         1: 'Admin',
         2: 'Atracador',
         3: 'Analista'
     }

    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    user_type = models.IntegerField()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    def get_email(self):
        return self.email
    
    def get_type(self):
        return self.TIPOS[self.user_type]


class Navio(models.Model):
    nome = models.CharField(unique=True, max_length=150)
    #proprietario = 
    def __str__(self):
        return self.nome

        
class Berco(models.Model):
    nome = models.CharField(unique=True, max_length=50)
    ocupado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Solicitacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    navio = models.ForeignKey(Navio, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)
    berco = models.ForeignKey(Berco, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.data)

class RegistroSaida(models.Model):
    solicitacao = models.OneToOneField(Solicitacao, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

