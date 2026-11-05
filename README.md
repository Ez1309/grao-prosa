# ☕ Grão & Prosa

<p align="center">
  <img src="static/img/logo-full-dark.svg" alt="Grão & Prosa Logo" width="460">
</p>

<p align="center">
  <strong>Plataforma Web para Avaliação, Catalogação e Curadoria de Cafés Especiais</strong><br>
  Trabalho Prático da Disciplina de Programação Web — Universidade Federal de Lavras (UFLA)
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Jazzmin-Admin_Theme-333333?style=for-the-badge" alt="Jazzmin">
</p>

---

## 📌 1. Integrantes do Grupo

| Nome | GitHub |
| :--- | :---: |
| **Ezequiel Dominguez Santos** | [@Ez1309](https://github.com/Ez1309) |
| **Diovani da Cruz Mangia Maciel Junior** | [@diovanimacieljr](https://github.com/diovanimacieljr) |

---

## 📖 2. Descrição do Projeto

O **Grão & Prosa** é uma aplicação web desenvolvida em **Django** seguindo o padrão arquitetural **MVT (Model-View-Template)**. O sistema funciona como um ponto de encontro para entusiastas e especialistas em cafés especiais, permitindo o catálogo de marcas e rótulos de café, a classificação por tipos de grão e pontos de torra, além de avaliações comunitárias com resenhas, notas de 1 a 5 estrelas e filtros avançados.

O desenvolvimento foi estruturado com foco em boas práticas de engenharia de software, modelagem relacional íntegra, persistência em banco relacional containerizado (**PostgreSQL 16** via Docker) e interface administrativa customizada via **Jazzmin**.

---

## 🚀 3. Tecnologias Utilizadas

* **Linguagem & Framework:** Python 3.12 e Django 5.1
* **Persistência Relacional:** PostgreSQL 16 (via Docker) com fallback para SQLite3 local
* **Containerização:** Docker e Docker Compose
* **Ambiente Administrativo:** `django-jazzmin` (customizado com ícones FontAwesome e suporte a Light/Dark Mode)
* **Manipulação de Imagens:** `Pillow` (para uploads de capas de cafés e fotos de perfil)
* **Arquivos Estáticos:** `WhiteNoise` (para serviço eficiente de estáticos em produção/container)
* **Gestão de Configuração:** `python-decouple` (para isolamento seguro de variáveis de ambiente no `.env`)

---

## 🎯 4. Funcionalidades do Sistema

A aplicação possui um ecossistema completo de gestão e interação, integrando múltiplos módulos de negócio:

* **Modelagem Relacional de Dados (3 Apps Modularizados):**
  * **App `usuarios`:** Modelo `Perfil` estendendo o `User` nativo (`OneToOneField`) com enums `TipoPerfil` e `TipoTorra`, biografia, foto de avatar e gatilho de criação automática via *Django Signals* (`post_save`).
  * **App `catalogo`:** Modelos `Marca` (país de origem, história, site oficial) e `Cafe` (relacionamento FK, enums `TipoGrao` e `TipoTorra`, intensidade 1 a 10 com `MinValueValidator`/`MaxValueValidator`, notas sensoriais, imagem de capa, booleano de destaque e cálculo automático de `nota_media` agregada).
  * **App `avaliacoes`:** Modelo `Review` (relacionamento N:1 com `User` e `Cafe`, nota de 1 a 5, comentário, constraint `unique_together = ('usuario', 'cafe')` para impedir spam e ordenação decrescente por data).
* **Painel Administrativo Customizado (Jazzmin):**
  * Interface moderna substituindo o padrão do Django pelo tema **Jazzmin** (Bootstrap 4 / AdminLTE 3).
  * Títulos e cabeçalhos em português do Brasil e menus laterais com ícones do **FontAwesome**.
  * Alternância integrada entre **Modo Claro** e **Modo Escuro** (*Dark Mode*).
* **Filtros e Recursos Avançados no Admin:**
  * Filtros laterais multifacetados (`list_filter`) por tipo de grão, ponto de torra, marcas cadastradas, destaque e faixa de notas.
  * Hierarquia de datas (`date_hierarchy = 'data_avaliacao'`) para navegação cronológica das avaliações.
  * Busca textual dinâmica (`search_fields`) por múltiplos campos indexados.
  * Edição inline: componente `ReviewInline` (`TabularInline`) embutido na edição do Café e `PerfilInline` (`StackedInline`) na tela de Usuários.
  * Edição rápida em lote na lista (`list_editable`) para o campo de destaque.
* **Script para Povoamento do Banco de Dados:**
  * Script standalone `scripts-bd/popula_cafes.py` que injeta 5 marcas conceituadas e 25 cafés com avaliações para testes e validação imediata do ambiente.

---

## ⚙️ 5. Instruções de Instalação e Execução

### Pré-requisitos
* **Git** instalado.
* **Docker** e **Docker Compose** instalados (recomendado) **OU** Python 3.12+ com ambiente virtual.

---

### Opção A: Execução via Docker (Recomendada)

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Ez1309/grao-prosa.git
   cd grao-prosa
   ```

2. **Crie o arquivo de configuração de ambiente:**
   ```bash
   cp .env.example .env
   ```

3. **Suba os containers (Django + PostgreSQL):**
   ```bash
   docker compose up --build -d
   ```
   *(O Docker aplicará as migrações automaticamente na inicialização).*

4. **Popule o banco de dados com os dados iniciais de teste:**
   ```bash
   docker compose exec web python scripts-bd/popula_cafes.py
   ```

5. **Crie um superusuário para acessar o painel administrativo:**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

6. **Acesse a aplicação no navegador:**
   * Painel Administrativo: **[http://localhost:8000/admin/](http://localhost:8000/admin/)**

---

### Opção B: Execução Local (Sem Docker)

1. **Crie e ative um ambiente virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   # .venv\Scripts\activate   # Windows
   ```

2. **Instale as dependências:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Crie o arquivo `.env`:**
   ```bash
   cp .env.example .env
   ```
   *(No arquivo `.env`, configure `DB_ENGINE=django.db.backends.sqlite3` para utilizar o banco SQLite local).*

4. **Execute as migrações e popule o banco:**
   ```bash
   python manage.py migrate
   python scripts-bd/popula_cafes.py
   python manage.py createsuperuser
   ```

5. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```
   Acesse: **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**

---

## 📁 6. Estrutura do Projeto

```text
grao-prosa/
├── avaliacoes/              # App de Avaliações e Reviews
│   ├── migrations/          # Migrações do banco de dados
│   ├── admin.py             # Admin de Reviews e TabularInline
│   └── models.py            # Model Review (notas 1 a 5, constraints)
├── catalogo/                # App de Catálogo de Cafés e Marcas
│   ├── migrations/          # Migrações do catálogo
│   ├── admin.py             # Admin com filtros, buscas e inline de reviews
│   └── models.py            # Models Marca e Cafe (choices, nota_media)
├── usuarios/                # App de Gestão de Usuários
│   ├── migrations/          # Migrações de perfis
│   ├── admin.py             # Admin com StackedInline de perfil no User
│   └── models.py            # Model Perfil (OneToOne, signals post_save)
├── grao_prosa/              # Pacote de Configuração Central (Host MVT)
│   ├── asgi.py
│   ├── settings.py          # Configurações globais, Jazzmin, DB e WhiteNoise
│   ├── urls.py              # Roteamento central e media handlers
│   └── wsgi.py
├── scripts-bd/              # Scripts de utilidade para o banco
│   └── popula_cafes.py      # Carga de 5 marcas e 25 cafés com avaliações
├── static/                  # Arquivos estáticos globais e identidade visual
│   └── img/                 # Logotipos vetoriais SVG (Light e Dark mode)
├── templates/               # Diretório de templates HTML
├── .env.example             # Modelo das variáveis de ambiente
├── .gitignore               # Higiene de versionamento (protege dados sensíveis)
├── docker-compose.yml       # Orquestração dos containers Web e DB
├── Dockerfile               # Definição da imagem da aplicação Django
├── manage.py                # Utilitário CLI de gestão do Django
├── README.md                # Documentação técnica oficial do projeto
└── requirements.txt         # Especificação de dependências Python
```

---

## 🌿 7. Estratégia de Versionamento e Branches

O projeto segue o modelo **Git Flow** para organização colaborativa:
* **`main`:** Código estável e validado para entregas oficiais.
* **`develop`:** Branch principal de integração contínua da equipe.
* **`feature/<modulo>`:** Branches isoladas de desenvolvimento utilizadas por cada integrante:
  * `feature/infra-setup-usuarios`
  * `feature/catalogo-avaliacoes`

---

## 📄 8. Licença

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
