from django.db import models


class Locality(models.Model):
    country = models.IntegerField(
        'País',
        choices=(
            (1, 'Brasil'),
            (2, 'Outros'),
        ),
        default=1,
    )
    state = models.CharField(
        'Estado UF',
        max_length=2,
    )
    city = models.CharField(
        'Município',
        max_length=255,
        blank=True,
    )
    neighborhood = models.CharField(
        'Bairro',
        max_length=255,
        blank=True,
    )
    zone = models.IntegerField(
        'Zona',
        choices=(
            (1, '1 - Urbana'),
            (2, '2 - Rural'),
            (3, '3 - Periurbana'),
            (9, '9 - Ignorado'),
        ),
        default=9,
    )


class Patient(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField(
        'Data de nascimento',
        null=True,
        blank=True,
    )
    age_in_hours = models.PositiveIntegerField(
        'Idade',
    )
    gender = models.CharField(
        'Sexo',
        max_length=1,
        choices=(
            ('M', 'M - Masculino'),
            ('F', 'F - Feminino'),
            ('I', 'I - Ignorado'),
        ),
        default='I',
    )
    pregnant = models.IntegerField(
        'Gestante',
        choices=(
            (1, '1 - 1° Trimestre'),
            (2, '2 - 2° Trimestre'),
            (3, '3 - 3° Trimestre'),
            (4, '4 - Idade gestacional ignorada'),
            (5, '5 - Não'),
            (6, '6 - Não se aplica'),
            (9, '7 - Ignorado'),
        ),
        default=9,
    )
    residence = models.OneToOneField(
        Locality,
        on_delete=models.SET_NULL,
        verbose_name='Endereço de residência',
        null=True,
    )
