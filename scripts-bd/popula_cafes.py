import os
import random
import sys

import django

# Adiciona o diretório raiz ao path para encontrar o módulo grao_prosa
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grao_prosa.settings")
django.setup()

from django.contrib.auth.models import User

from avaliacoes.models import Review
from catalogo.models import Cafe, Marca


def popular_banco():
    print("A iniciar o povoamento da base de dados...")

    # Criação de um utilizador de teste para vincular as avaliações
    usuario, _ = User.objects.get_or_create(
        username="degustador", defaults={"email": "degustador@graoeprosa.com"}
    )
    if _:
        usuario.set_password("senha123")
        usuario.save()

    # Criação de 5 marcas famosas
    nomes_marcas = ["Orfeu", "Dengo", "Coffee Lab", "Mitsuo Nakao", "Octavio Café"]
    marcas = []
    for nome in nomes_marcas:
        marca, _ = Marca.objects.get_or_create(
            nome=nome,
            defaults={
                "pais_origem": "Brasil",
                "historia": f"História da marca {nome}.",
            },
        )
        marcas.append(marca)

    variacoes = ["Clássico", "Intenso", "Suave", "Reserva", "Especial"]

    # Criação de 25 cafés (5 marcas x 5 variações) e respetivas avaliações
    cafes_criados = 0
    for marca in marcas:
        for var in variacoes:
            nome_cafe = f"{marca.nome} {var}"
            cafe, created = Cafe.objects.get_or_create(
                nome=nome_cafe,
                marca=marca,
                defaults={
                    "tipo_grao": random.choice(["ARABICA", "ROBUSTA", "BLEND"]),
                    "tipo_torra": random.choice(["CLARA", "MEDIA", "ESCURA"]),
                    "intensidade": random.randint(3, 9),
                    "descricao": f"Um excelente café {var.lower()} da marca {marca.nome}.",
                    "notas_aromaticas": random.choice(
                        [
                            "Caramelo e Nozes",
                            "Chocolate amargo",
                            "Frutas vermelhas",
                            "Cítrico",
                        ]
                    ),
                    "destaque": random.choice([True, False]),
                },
            )
            if created:
                cafes_criados += 1

            # Criação de uma review para testar o ReviewInline e o nota_media()
            Review.objects.get_or_create(
                usuario=usuario,
                cafe=cafe,
                defaults={
                    "nota": random.randint(3, 5),
                    "comentario": "Café com notas sensoriais muito interessantes!",
                },
            )

    print(
        f"Povoamento concluído: 5 marcas e {cafes_criados} novos cafés registados (Total: 25)."
    )


if __name__ == "__main__":
    popular_banco()
