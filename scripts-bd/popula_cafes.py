import os
import random
import shutil
import sys

import django
from django.conf import settings

# Adiciona o diretório raiz ao path para encontrar o módulo grao_prosa
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grao_prosa.settings")
django.setup()

from django.contrib.auth.models import User

from avaliacoes.models import Review
from catalogo.models import Cafe, Marca

# Dados detalhados das 9 marcas de café
MARCAS_DATA = [
    {
        "nome": "Orfeu",
        "pais_origem": "Brasil",
        "historia": (
            "Cultivado nas altas montanhas do Sul de Minas Gerais, na Fazenda Sertãozinho "
            "e Laranjal, o Café Orfeu é um dos mais premiados do país, com controle rigoroso "
            "desde o plantio até a torra de grãos e microlotes especiais."
        ),
        "site_oficial": "https://www.orfeucafes.com.br",
    },
    {
        "nome": "Coffee Lab",
        "pais_origem": "Brasil",
        "historia": (
            "Laboratório de cafés especiais fundado em São Paulo pela mestre de torra Isabela Raposeiras. "
            "Pioneiro na terceira onda do café no Brasil, foca em microlotes de pequenos produtores "
            "e torras artesanais de alta precisão sensorial."
        ),
        "site_oficial": "https://coffeelab.com.br",
    },
    {
        "nome": "Dengo",
        "pais_origem": "Brasil",
        "historia": (
            "Marca brasileira que une cacau e cafés especiais de pequenos produtores com foco em "
            "sustentabilidade, comércio justo e valorização do terroir nacional."
        ),
        "site_oficial": "https://www.dengo.com.br",
    },
    {
        "nome": "Mitsuo Nakao",
        "pais_origem": "Brasil",
        "historia": (
            "Com tradição cafeeira iniciada na imigração japonesa e sediada no Cerrado Mineiro, "
            "a família Nakao produz cafés especiais com altitude superior a 1.000 metros, "
            "focando em grãos de alta doçura e rastreabilidade total."
        ),
        "site_oficial": "https://mitsuonakao.com.br",
    },
    {
        "nome": "Octavio Café",
        "pais_origem": "Brasil",
        "historia": (
            "Um dos maiores ícones da cafeicultura de cafés especiais do Brasil, situado na tradicional "
            "região da Alta Mogiana paulista, com fazendas centenárias e controle de qualidade da semente à xícara."
        ),
        "site_oficial": "https://octaviocafe.com.br",
    },
    {
        "nome": "Baggio Café",
        "pais_origem": "Brasil",
        "historia": (
            "Com origens em 1886 com imigrantes italianos no interior paulista, a Baggio é pioneira "
            "e referência nacional em cafés gourmet de alta qualidade e cafés aromatizados sofisticados."
        ),
        "site_oficial": "https://www.baggiocafe.com.br",
    },
    {
        "nome": "Três Corações",
        "pais_origem": "Brasil",
        "historia": (
            "Líder nacional do setor de cafés, celebra as principais origens produtoras do país "
            "com a prestigiada linha Rituais, composta por cafés 100% Arábica com certificação de origem e blends fortes."
        ),
        "site_oficial": "https://www.escolhatres.com.br",
    },
    {
        "nome": "Melitta",
        "pais_origem": "Alemanha",
        "historia": (
            "Fundada em 1908 por Melitta Bentz, criadora do filtro de papel para café. Presente há décadas "
            "no cotidiano dos lares brasileiros, oferece desde cafés tradicionais até linhas gourmet de regiões nobres."
        ),
        "site_oficial": "https://www.melitta.com.br",
    },
    {
        "nome": "Pilão",
        "pais_origem": "Brasil",
        "historia": (
            "Símbolo da cultura popular brasileira do café, reconhecido historicamente como 'o café forte do Brasil', "
            "com ponto de torra escura, encorpado e sabor marcante."
        ),
        "site_oficial": "https://www.pilao.com.br",
    },
]

# Dados detalhados dos 18 cafés com suas imagens em media/cafes/
CAFES_DATA = [
    # Orfeu (5 cafés)
    {
        "nome": "Orfeu Clássico",
        "marca_nome": "Orfeu",
        "tipo_grao": Cafe.TipoGrao.ARABICA,
        "tipo_torra": Cafe.TipoTorra.MEDIA,
        "intensidade": 6,
        "notas_aromaticas": "Chocolate, caramelo e notas florais",
        "origem_grao": "Sul de Minas",
        "descricao": (
            "Um café clássico e equilibrado com aroma floral delicado e notas marcantes de chocolate e caramelo. "
            "Apresenta acidez balanceada e corpo sedoso e aveludado."
        ),
        "imagem": "cafes/Cafe_Orfeu_Classico.webp",
        "destaque": True,
    },
    {
        "nome": "Orfeu Intenso",
        "marca_nome": "Orfeu",
        "tipo_grao": Cafe.TipoGrao.ARABICA,
        "tipo_torra": Cafe.TipoTorra.ESCURA,
        "intensidade": 8,
        "notas_aromaticas": "Chocolate amargo, nozes e frutas secas",
        "origem_grao": "Sul de Minas",
        "descricao": (
            "Café encorpado e envolvente, de torra mais escura. Suas notas remetem a chocolate amargo e nozes, "
            "com baixa acidez e uma finalização densa e duradoura na boca."
        ),
        "imagem": "cafes/Cafe_Orfeu_Intenso.webp",
        "destaque": False,
    },
    {
        "nome": "Orfeu Forte",
        "marca_nome": "Orfeu",
        "tipo_grao": Cafe.TipoGrao.ARABICA,
        "tipo_torra": Cafe.TipoTorra.ESCURA,
        "intensidade": 9,
        "notas_aromaticas": "Cacau torrado e especiarias",
        "origem_grao": "Sul de Minas",
        "descricao": (
            "Combina a força de uma torra vigorosa com a sofisticação do grão 100% arábica. "
            "Entrega corpo pesado, crema abundante e retrogosto agradável e potente."
        ),
        "imagem": "cafes/Cafe_Orfeu_Forte.webp",
        "destaque": False,
    },
    {
        "nome": "Orfeu Microlote Arara",
        "marca_nome": "Orfeu",
        "tipo_grao": Cafe.TipoGrao.ARABICA,
        "tipo_torra": Cafe.TipoTorra.CLARA,
        "intensidade": 5,
        "notas_aromaticas": "Jasmim, pêssego e calda de açúcar",
        "origem_grao": "Alta Mogiana",
        "descricao": (
            "Microlote premiado da rara variedade Arara. Cultivado em altitude elevada, destaca-se pela acidez viva, "
            "aroma envolvente de jasmim e notas distintas de pêssego amarelo e caldo de cana."
        ),
        "imagem": "cafes/Cafe_Orfeu_Arara.webp",
        "destaque": True,
    },
    {
        "nome": "Orfeu Microlote Catucaí",
        "marca_nome": "Orfeu",
        "tipo_grao": Cafe.TipoGrao.ARABICA,
        "tipo_torra": Cafe.TipoTorra.MEDIA,
        "intensidade": 6,
        "notas_aromaticas": "Frutas vermelhas, mel e cítrico",
        "origem_grao": "Sul de Minas",
        "descricao": (
            "Lote especial da variedade Catucaí Amarelo. Entrega notas sensoriais expressivas de frutas silvestres, "
            "alta doçura natural remetendo a mel de floradas e acidez málica equilibrada."
        ),
        "imagem": "cafes/Cafe_Orfeu_Catucaí.webp",
        "destaque": True,
    },
    # Coffee Lab (1 café)
    {
        "nome": "Coffee Lab Wilson Vicente",
        "marca_nome": "Coffee Lab",
        "tipo_grao": Cafe.TipoGrao.ARABICA,
        "tipo_torra": Cafe.TipoTorra.CLARA,
        "intensidade": 5,
        "notas_aromaticas": "Caldo de cana, limão siciliano e mel",
        "origem_grao": "Mantiqueira de Minas",
        "descricao": (
            "Microlote artesanal de alta pontuação SCA produzido por Wilson Vicente na Mantiqueira de Minas. "
            "Torra clara milimetricamente calibrada para realçar a explosão de doçura e acidez cítrica refrescante."
        ),
        "imagem": "cafes/Cafe_Coffee_Labs_Wilson_Vicente.webp",
        "destaque": True,
    },
    # Dengo (1 café)
    {
        "nome": "Dengo Café Especial",
        "marca_nome": "Dengo",
        "tipo_grao": Cafe.TipoGrao.ARABICA,
        "tipo_torra": Cafe.TipoTorra.MEDIA,
        "intensidade": 6,
        "notas_aromaticas": "Cacau puro, melado de cana e frutas tropicais",
        "origem_grao": "Chapada Diamantina",
        "descricao": (
            "Café especial de origem brasileira que harmoniza o terroir da altitude baiana com o universo sensorial do cacau. "
            "Corpo cremoso, final doce e sustentabilidade do pequeno produtor em cada grão."
        ),
        "imagem": "cafes/Cafe_Dengo.webp",
        "destaque": True,
    },
    # Mitsuo Nakao (1 café)
    {
        "nome": "Mitsuo Nakao Especial",
        "marca_nome": "Mitsuo Nakao",
        "tipo_grao": Cafe.TipoGrao.ARABICA,
        "tipo_torra": Cafe.TipoTorra.MEDIA,
        "intensidade": 7,
        "notas_aromaticas": "Castanhas, toffee e chocolate ao leite",
        "origem_grao": "Cerrado Mineiro",
        "descricao": (
            "Grãos selecionados com rigor na região do Cerrado Mineiro. Apresenta notas marcantes de toffee, "
            "doçura limpa de caramelo, corpo aveludado e acidez branda."
        ),
        "imagem": "cafes/Cafe_Mitsuo_Nakao_Especial.webp",
        "destaque": False,
    },
    # Octavio Café (1 café)
    {
        "nome": "Octavio Café Especial Clássico Grãos",
        "marca_nome": "Octavio Café",
        "tipo_grao": Cafe.TipoGrao.ARABICA,
        "tipo_torra": Cafe.TipoTorra.MEDIA,
        "intensidade": 6,
        "notas_aromaticas": "Avelã, caramelo e chocolate belga",
        "origem_grao": "Alta Mogiana",
        "descricao": (
            "O consagrado clássico da centenária fazenda Octavio na Alta Mogiana paulista. Blend em grãos "
            "com perfil redondo, equilíbrio exemplar entre aroma de avelã tostada e doçura prolongada."
        ),
        "imagem": "cafes/Cafe_Octavio_Especial_Classico_Graos.webp",
        "destaque": True,
    },
    # Baggio Café (1 café)
    {
        "nome": "Baggio Gourmet Chocolate com Menta",
        "marca_nome": "Baggio Café",
        "tipo_grao": Cafe.TipoGrao.ARABICA,
        "tipo_torra": Cafe.TipoTorra.MEDIA,
        "intensidade": 5,
        "notas_aromaticas": "Chocolate trufado e menta fresca",
        "origem_grao": "Mogiana Paulista",
        "descricao": (
            "Café gourmet aromatizado que combina grãos 100% arábica com a sofisticação do chocolate refinado "
            "e a refrescância estimulante da menta. Uma experiência sensorial única para sobremesas e pausas especiais."
        ),
        "imagem": "cafes/Cafe_Baggio_Chocolate_com_Menta.webp",
        "destaque": True,
    },
    # Três Corações (3 cafés)
    {
        "nome": "Três Corações Rituais Cerrado Mineiro",
        "marca_nome": "Três Corações",
        "tipo_grao": Cafe.TipoGrao.ARABICA,
        "tipo_torra": Cafe.TipoTorra.MEDIA,
        "intensidade": 6,
        "notas_aromaticas": "Caramelo, nozes e frutas amarelas",
        "origem_grao": "Cerrado Mineiro",
        "descricao": (
            "Da prestigiada linha Rituais, café de Denominação de Origem Protegida do Cerrado Mineiro. "
            "Destaca-se pelo aroma intenso, doçura de caramelo e acidez cítrica brilhante."
        ),
        "imagem": "cafes/Cafe_Tres_Coracoes_Cerrado_Mineiro.jpeg",
        "destaque": False,
    },
    {
        "nome": "Três Corações Rituais Mogiana Paulista",
        "marca_nome": "Três Corações",
        "tipo_grao": Cafe.TipoGrao.ARABICA,
        "tipo_torra": Cafe.TipoTorra.MEDIA,
        "intensidade": 7,
        "notas_aromaticas": "Frutas cítricas secas, mel e cacau",
        "origem_grao": "Mogiana Paulista",
        "descricao": (
            "Oriundo das colinas da Mogiana Paulista, apresenta corpo denso e encorpado, notas adocicadas de mel "
            "e nuances cítricas com finalização longa e persistente."
        ),
        "imagem": "cafes/Cafe_Tres_Coracoes_Mogiana_Paulista.webp",
        "destaque": False,
    },
    {
        "nome": "Três Corações Dark Roast",
        "marca_nome": "Três Corações",
        "tipo_grao": Cafe.TipoGrao.BLEND,
        "tipo_torra": Cafe.TipoTorra.ESCURA,
        "intensidade": 10,
        "notas_aromaticas": "Cacau amargo e madeira nobre",
        "origem_grao": "Brasil",
        "descricao": (
            "Torra escura intensa para amantes de café forte e encorpado. Ideal para quem aprecia crema espessa, "
            "baixo teor de acidez e notas amendoadas torradas profundas."
        ),
        "imagem": "cafes/Cafe_Tres_Coracoes_Dark_Roast.jpeg",
        "destaque": False,
    },
    # Melitta (4 cafés)
    {
        "nome": "Melitta Tradicional",
        "marca_nome": "Melitta",
        "tipo_grao": Cafe.TipoGrao.BLEND,
        "tipo_torra": Cafe.TipoTorra.ESCURA,
        "intensidade": 8,
        "notas_aromaticas": "Grãos tostados e cacau clássico",
        "origem_grao": "Brasil",
        "descricao": (
            "O clássico presente na memória afetiva do brasileiro. Moagem fina e torra escura uniforme "
            "que garantem um café fresco, encorpado e com aroma inconfundível."
        ),
        "imagem": "cafes/Cafe_Melitta_Tradicional.webp",
        "destaque": False,
    },
    {
        "nome": "Melitta Descafeinado",
        "marca_nome": "Melitta",
        "tipo_grao": Cafe.TipoGrao.BLEND,
        "tipo_torra": Cafe.TipoTorra.MEDIA,
        "intensidade": 5,
        "notas_aromaticas": "Cereal tostado e suave malte",
        "origem_grao": "Brasil",
        "descricao": (
            "Todo o sabor e qualidade da torra Melitta em uma versão descafeinada por processos suaves. "
            "Perfeito para qualquer momento do dia ou da noite com equilíbrio e leveza."
        ),
        "imagem": "cafes/Cafe_Melitta_Descafeinado.webp",
        "destaque": False,
    },
    {
        "nome": "Melitta Regiões Gourmet Cerrado",
        "marca_nome": "Melitta",
        "tipo_grao": Cafe.TipoGrao.ARABICA,
        "tipo_torra": Cafe.TipoTorra.MEDIA,
        "intensidade": 7,
        "notas_aromaticas": "Nozes torradas, chocolate e caramelo",
        "origem_grao": "Cerrado Mineiro",
        "descricao": (
            "Café 100% arábica da linha Regiões Gourmet, com grãos colhidos no Cerrado Mineiro. "
            "Aroma envolvente com notas adocicadas de nozes e chocolate, com corpo sedoso."
        ),
        "imagem": "cafes/Cafe_Melitta_Gourmet_Cerrado.webp",
        "destaque": False,
    },
    {
        "nome": "Melitta Regiões Gourmet Mogiana Paulista",
        "marca_nome": "Melitta",
        "tipo_grao": Cafe.TipoGrao.ARABICA,
        "tipo_torra": Cafe.TipoTorra.CLARA,
        "intensidade": 6,
        "notas_aromaticas": "Frutas secas, mel e floral suave",
        "origem_grao": "Mogiana Paulista",
        "descricao": (
            "Variedade gourmet da tradicional região da Mogiana Paulista, com ponto de torra brando "
            "que preserva a doçura natural e notas elegantes de frutas secas e flores."
        ),
        "imagem": "cafes/Cafe_Melitta_Gourmet_Mogiana_Paulista.jpg",
        "destaque": False,
    },
    # Pilão (1 café)
    {
        "nome": "Pilão Tradicional",
        "marca_nome": "Pilão",
        "tipo_grao": Cafe.TipoGrao.ROBUSTA,
        "tipo_torra": Cafe.TipoTorra.ESCURA,
        "intensidade": 8,
        "notas_aromaticas": "Notas intensas de torra e chocolate amargo",
        "origem_grao": "Espírito Santo",
        "descricao": (
            "O autêntico 'café forte do Brasil', de torra acentuada e encorpada, entregando um café com presença inconfundível na xícara."
        ),
        "imagem": "cafes/Cafe_Pilao_Tradicional.webp",
        "destaque": False,
    },
]

# Banco de avaliações realistas para enriquecer o catálogo
COMENTARIOS_AVALIACOES = [
    (5, "Simplesmente espetacular! Notas sensoriais nítidas e uma doçura natural surpreendente na xícara."),
    (5, "Excelente café para preparar na prensa francesa ou V60. Corpo muito sedoso e aroma marcante."),
    (4, "Café equilibrado com acidez média muito agradável. Ótimo custo-benefício para o dia a dia."),
    (4, "Notas de chocolate e caramelo bem presentes, torra no ponto certo sem amargor excessivo."),
    (5, "Um dos melhores cafés que já degustei! Finalização limpa e retrogosto prolongado prazeroso."),
    (4, "Perfeito para o espresso matinal! Crema densa, boa intensidade e aroma que preenche a casa."),
    (3, "Café honesto para o cotidiano. Ponto de torra um pouco mais acentuado, ideal para misturar com leite."),
]


def sincronizar_imagens_media():
    """
    Copia as imagens-semente versionadas em scripts-bd/assets/cafes/ para settings.MEDIA_ROOT/cafes/
    caso ainda não existam. Garante que qualquer ambiente recém-clonado tenha as fotos disponíveis offline.
    """
    diretorio_origem = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "assets", "cafes"
    )
    diretorio_destino = os.path.join(settings.MEDIA_ROOT, "cafes")

    if not os.path.exists(diretorio_origem):
        print(f"[Aviso] Pasta de assets não encontrada em: {diretorio_origem}")
        return

    os.makedirs(diretorio_destino, exist_ok=True)

    copiados = 0
    for nome_arquivo in os.listdir(diretorio_origem):
        caminho_origem = os.path.join(diretorio_origem, nome_arquivo)
        caminho_destino = os.path.join(diretorio_destino, nome_arquivo)

        if os.path.isfile(caminho_origem):
            if not os.path.exists(caminho_destino) or os.path.getsize(caminho_origem) != os.path.getsize(caminho_destino):
                shutil.copy2(caminho_origem, caminho_destino)
                copiados += 1

    if copiados > 0:
        print(f"-> Sincronizadas {copiados} imagens de cafés de assets/ para media/cafes/.")
    else:
        print("-> Imagens em media/cafes/ já se encontram atualizadas.")


def popular_banco():
    print("A iniciar o povoamento da base de dados com as novas marcas, aromas e imagens reais...")

    # 0. Sincroniza arquivos de mídia locais de assets para media/
    sincronizar_imagens_media()

    # 1. Limpeza seletiva dos 25 cafés genéricos gerados pelo script antigo (placeholder sem imagens reais)
    nomes_antigos_placeholder = [
        f"{m} {v}"
        for m in ["Orfeu", "Dengo", "Coffee Lab", "Mitsuo Nakao", "Octavio Café"]
        for v in ["Clássico", "Intenso", "Suave", "Reserva", "Especial"]
    ]
    removidos, _ = Cafe.objects.filter(nome__in=nomes_antigos_placeholder).delete()
    if removidos:
        print(f"-> Removidos {removidos} cafés genéricos antigos da versão anterior.")

    # 2. Utilizadores de teste para avaliações
    usuario_degustador, _ = User.objects.get_or_create(
        username="degustador", defaults={"email": "degustador@graoeprosa.com"}
    )
    if _:
        usuario_degustador.set_password("senha123")
        usuario_degustador.save()

    usuario_barista, _ = User.objects.get_or_create(
        username="barista_cadu", defaults={"email": "cadu@graoeprosa.com"}
    )
    if _:
        usuario_barista.set_password("senha123")
        usuario_barista.save()

    avaliadores = [usuario_degustador, usuario_barista]

    # 3. Criação ou atualização das 9 Marcas
    marcas_map = {}
    for data in MARCAS_DATA:
        marca, _ = Marca.objects.update_or_create(
            nome=data["nome"],
            defaults={
                "pais_origem": data["pais_origem"],
                "historia": data["historia"],
                "site_oficial": data["site_oficial"],
            },
        )
        marcas_map[marca.nome] = marca
    print(f"-> {len(marcas_map)} marcas configuradas com sucesso.")

    # 4. Criação ou atualização dos 18 Cafés com dados completos e imagens
    cafes_registrados = 0
    total_reviews = 0

    for item in CAFES_DATA:
        marca = marcas_map[item["marca_nome"]]
        cafe, created = Cafe.objects.update_or_create(
            nome=item["nome"],
            defaults={
                "marca": marca,
                "tipo_grao": item["tipo_grao"],
                "tipo_torra": item["tipo_torra"],
                "intensidade": item["intensidade"],
                "notas_aromaticas": item["notas_aromaticas"],
                "origem_grao": item["origem_grao"],
                "descricao": item["descricao"],
                "imagem": item["imagem"],
                "destaque": item["destaque"],
            },
        )
        cafes_registrados += 1

        # 5. Adiciona avaliações para alimentar o sistema de pontuação e reviews
        # Cada café recebe de 1 a 2 avaliações realistas
        sample_comentarios = random.sample(COMENTARIOS_AVALIACOES, k=2)
        for idx, (nota, comentario) in enumerate(sample_comentarios):
            user = avaliadores[idx % len(avaliadores)]
            _, rev_created = Review.objects.update_or_create(
                usuario=user,
                cafe=cafe,
                defaults={
                    "nota": nota,
                    "comentario": comentario,
                },
            )
            if rev_created:
                total_reviews += 1

    print(
        f"\nConcluído com sucesso!\n"
        f"-> {len(marcas_map)} marcas cadastradas.\n"
        f"-> {cafes_registrados} cafés com fotos, notas sensoriais e terroirs reais.\n"
        f"-> {Review.objects.count()} avaliações registradas no catálogo."
    )


if __name__ == "__main__":
    popular_banco()
