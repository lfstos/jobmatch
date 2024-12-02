_FAIXA_SALARIAL_CHOICES = (
    ('1k', 'Até 1.000'),
    ('1k-2k', 'De 1.000 a 2.000'),
    ('2k-3k', 'De 2.000 a 3.000'),
    ('3k+', 'Acima de 3.000')
)
_ESCOLARIDADE_CHOICES = (
    ('Ensino Fundamental', 'Ensino Fundamental'),
    ('Ensino Medio', 'Ensino Médio'),
    ('Tecnologo', 'Tecnólogo'),
    ('Ensino Superior', 'Ensino Superior'),
    ('Pos/MBA/Mestrado', 'Pós/MBA/Mestrado'),
    ('Doutorado', 'Doutorado')
)


def get_faixa_salarial_choices():
    return _FAIXA_SALARIAL_CHOICES

def get_escolaridade_choices():
    return _ESCOLARIDADE_CHOICES