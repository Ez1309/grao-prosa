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
  <img src="https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap 5">
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

O **Grão & Prosa** é uma aplicação web completa desenvolvida em **Django** seguindo o padrão arquitetural **MVT (Model-View-Template)**. O sistema funciona como uma rede social e ponto de encontro para amantes e especialistas em cafés especiais (inspirado no conceito de plataformas como Untappd, Vivino e Letterboxd).

A plataforma permite catalogar marcas e rótulos de café com fichas técnicas detalhadas, explorar resenhas sensoriais da comunidade com notas de 1 a 5 estrelas, diferenciar perfis de acesso (*Consumidores Entusiastas* vs. *Especialistas Baristas* com permissões de curadoria) e navegar em uma interface moderna e acessível com suporte a **Modo Claro e Modo Escuro** persistente.

---

## 🚀 3. Tecnologias Utilizadas

* **Backend:** Python 3.12 e Django 5.1 (Arquitetura MVT)
* **Frontend:** HTML5 semântico, Bootstrap 5.3+, FontAwesome 6 e Vanilla JavaScript puro
* **Estilização & Temas:** CSS3 customizado com variáveis CSS para suporte completo a **Dark Mode** suave e **Light Mode**
* **Persistência Relacional:** PostgreSQL 16 (via Docker) com fallback automático para SQLite3 local
* **Containerização:** Docker e Docker Compose
* **Ambiente Administrativo:** `django-jazzmin` (customizado com filtros multifacetados, inlines e ícones FontAwesome)
* **Manipulação de Imagens:** `Pillow` (para uploads de capas de cafés e fotos de perfil/avatar)
* **Arquivos Estáticos:** `WhiteNoise` (para serviço otimizado de estáticos em contêiner)
* **Segurança e Variáveis de Ambiente:** `python-decouple` (isolamento de credenciais no arquivo `.env`)

---

## 🎯 4. Funcionalidades do Sistema

### 4.1. Design System e Interface Base
* **Navbar Responsiva:** Logotipo SVG oficial adaptativo (modo claro/escuro), barra de busca rápida, botão toggle de tema e menu dropdown do usuário com foto de perfil em miniatura.
* **Alternância de Tema (Light / Dark Mode):** Transição suave entre tema claro e modo escuro aveludado, com preferência gravada no `localStorage` do navegador e script anti-flicker no cabeçalho.
* **Sem Azul Padrão:** Identidade visual 100% harmonizada nos tons de café, avelã, crema e carvão suave para todos os botões, links, dropdowns e abas.
* **Mensagens de Feedback:** Alertas contextuais do Django (`django.contrib.messages`) com ícones e botão de fechar.

### 4.2. Autenticação e Gestão de Usuários (`usuarios`)
* **Login Flexível:** Autenticação primária por **E-mail** (ou Nome de Usuário) e senha, com alternância de visibilidade de senha (ícone de olho) e mensagens claras de erro.
* **Cadastro de Conta:** Formulário vertical limpo com validação em tempo real de confirmação de senha, seleção dinâmica de torra preferida do backend e criação automática de perfil `ENTUSIASTA`.
* **Logout Seguro:** Encerramento de sessão com mensagens informativas de retorno.

### 4.3. Módulo de Perfil do Usuário (`/usuarios/perfil/`)
* **Identificação e Badges:** Exibição da foto de perfil (avatar), nome, `@username`, badge de papel (*Consumidor / Entusiasta* ou *Especialista / Barista*), badge de torra favorita e data de cadastro.
* **Métricas de Atividade:** Total de avaliações postadas e média geral de notas concedidas pelo usuário.
* **Aba "Meus Cafés Avaliados":** Lista cronológica das resenhas registradas pelo usuário, notas em estrelas douradas de 1 a 5, marcas e características sensoriais.
* **Aba "Editar Perfil":** Formulário completo para atualização de nome, e-mail, biografia (com contador de até 500 caracteres), ponto de torra e upload/remoção de avatar.

### 4.4. Páginas de Erro Personalizadas
* **Tratamento de Exceções HTTP:** Templates amigáveis, responsivos e profissionais integrados aos handlers do Django para **404** (Página Não Encontrada), **403** (Acesso Negado), **500** (Erro Interno do Servidor) e **400** (Requisição Inválida).

### 4.5. Modelagem Relacional e Painel Administrativo
* **App `catalogo`:** Modelos `Marca` e `Cafe` (ponto de torra, tipo de grão, intensidade 1 a 10, notas aromáticas, capa e destaque).
* **App `avaliacoes`:** Modelo `Review` com nota de 1 a 5 estrelas, comentário e restrição de unicidade `unique_together = ('usuario', 'cafe')`.
* **Jazzmin Admin:** Painel administrativo customizado em português, com filtros laterais multifacetados, busca textual ampla, navegação por datas (`date_hierarchy`) e edição inline (`ReviewInline` e `PerfilInline`).

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

4. **Popule o banco de dados com os dados iniciais de teste (25 cafés e reviews):**
   ```bash
   docker compose exec web python scripts-bd/popula_cafes.py
   ```

5. **Crie um superusuário para o painel administrativo (opcional, caso queira credencial própria):**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

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
   *(No arquivo `.env`, mantenha `DB_ENGINE=django.db.backends.sqlite3` para utilizar o banco SQLite local).*

4. **Execute as migrações e popule o banco:**
   ```bash
   python manage.py migrate
   python scripts-bd/popula_cafes.py
   ```

5. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

---

## 🔑 6. Credenciais de Teste para Avaliação

Para facilitar a navegação e a validação do professor/avaliador, utilize as contas pré-configuradas no banco de dados populado:

| Tipo de Usuário | E-mail de Login | Usuário | Senha | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| **Entusiasta / Avaliador** | `degustador@graoeprosa.com` | `degustador` | `senha123` | Perfil completo com bio, preferências, avatar e **25 reviews cadastradas** para conferência. |
| **Administrador / Staff** | `admin@graoprosa.com` | `admin` | `admin123` | Acesso total ao painel administrativo Jazzmin em `/admin/`. |

---

## 🌐 7. Principais Rotas da Aplicação

* **Página Inicial:** [http://localhost:8000/](http://localhost:8000/)
* **Tela de Login:** [http://localhost:8000/usuarios/login/](http://localhost:8000/usuarios/login/)
* **Tela de Cadastro:** [http://localhost:8000/usuarios/cadastro/](http://localhost:8000/usuarios/cadastro/)
* **Perfil do Usuário:** [http://localhost:8000/usuarios/perfil/](http://localhost:8000/usuarios/perfil/) *(requer login)*
* **Painel Administrativo:** [http://localhost:8000/admin/](http://localhost:8000/admin/)
* **Pré-visualização das Telas de Erro:**
  * 404: [http://localhost:8000/erros/404/](http://localhost:8000/erros/404/)
  * 403: [http://localhost:8000/erros/403/](http://localhost:8000/erros/403/)
  * 500: [http://localhost:8000/erros/500/](http://localhost:8000/erros/500/)
  * 400: [http://localhost:8000/erros/400/](http://localhost:8000/erros/400/)

---

## 📁 8. Estrutura do Projeto

```text
grao-prosa/
├── avaliacoes/              # App de Avaliações e Reviews
│   ├── migrations/          # Migrações do banco de dados
│   ├── admin.py             # Admin de Reviews e TabularInline
│   └── models.py            # Model Review (notas 1 a 5, constraints de unicidade)
├── catalogo/                # App de Catálogo de Cafés e Marcas
│   ├── migrations/          # Migrações do catálogo
│   ├── admin.py             # Admin com filtros, buscas e inline de reviews
│   └── models.py            # Models Marca e Cafe (choices, nota_media agregada)
├── usuarios/                # App de Autenticação e Perfis
│   ├── migrations/          # Migrações de perfis
│   ├── admin.py             # Admin com StackedInline de perfil no User
│   ├── models.py            # Model Perfil (OneToOne, signals post_save)
│   ├── urls.py              # Rotas de login, logout, cadastro e perfil
│   └── views.py             # Lógica de login por email/username, cadastro e perfil
├── grao_prosa/              # Pacote Central do Projeto Django
│   ├── asgi.py
│   ├── settings.py          # Configurações globais, Jazzmin, DB e WhiteNoise
│   ├── urls.py              # Roteamento central, media e handlers de erro HTTP
│   ├── views.py             # Handlers customizados (404, 403, 500, 400)
│   └── wsgi.py
├── scripts-bd/              # Scripts de utilidade para o banco
│   └── popula_cafes.py      # Carga de 5 marcas e 25 cafés com avaliações
├── static/                  # Arquivos estáticos globais e identidade visual
│   ├── css/
│   │   └── style.css        # Folha de estilos customizada (Light/Dark mode)
│   ├── js/
│   │   └── theme.js         # Alternância e persistência de tema no localStorage
│   └── img/                 # Logotipos vetoriais SVG (Light e Dark mode)
├── templates/               # Diretório de templates HTML (Bootstrap 5)
│   ├── base.html            # Casca base com navbar responsiva e rodapé
│   ├── 400.html             # Página de Requisição Inválida
│   ├── 403.html             # Página de Acesso Negado
│   ├── 404.html             # Página de Página Não Encontrada
│   ├── 500.html             # Página de Erro Interno do Servidor
│   └── usuarios/            # Templates do app de usuários
│       ├── login.html       # Tela de login imersiva
│       ├── cadastro.html    # Tela de cadastro em fluxo vertical
│       └── perfil.html      # Perfil social com histórico de resenhas e edição
├── .env.example             # Modelo das variáveis de ambiente
├── .gitignore               # Higiene de versionamento (ignora media/ e segredos)
├── docker-compose.yml       # Orquestração dos containers Web e DB
├── Dockerfile               # Definição da imagem da aplicação Django
├── manage.py                # Utilitário CLI de gestão do Django
├── README.md                # Documentação técnica oficial do projeto
└── requirements.txt         # Especificação de dependências Python
```

---

## 🌿 9. Estratégia de Versionamento e Branches

O projeto segue rigorosamente o modelo **Git Flow** estabelecido nas diretrizes do edital:
* **`main`:** Versão estável do software para avaliações oficiais.
* **`develop`:** Branch principal de integração contínua da equipe.
* **`feature/<modulo>`:** Branches individuais de desenvolvimento:
  * `feature/auth-perfil-base-ui`: Casca base, temas, login/logout, cadastro, perfil social e páginas de erro *(Pessoa A)*.
  * `feature/catalogo-reviews-dashboard`: Feed, detalhes, curadoria de especialista e dashboard *(Pessoa B)*.

---

## 📄 10. Licença

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
