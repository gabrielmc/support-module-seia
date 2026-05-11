# 📦 Módulo SEIA – API em Python

Este projeto faz parte do **módulo SEIA**, desenvolvido em **Python** utilizando **FastAPI**, com foco em:

- Consultas ao banco de dados
- Processamento de arquivos CNAB
- Integração com múltiplos ambientes (DSV e HML)
- Organização em camadas (routes, services, repositories)


## ⚠️ **Observação importante**:
O projeto principal do SEIA utiliza a porta **8080** (JBoss).
Por isso, esta API roda em **outra porta**, evitando conflitos.

---

## 🧱 Estrutura do Projeto

```
module-seia/
├── app/
│ ├── core/                 # Configurações, banco e variáveis de ambiente
│ ├── models/               # Schemas (Pydantic)
│ ├── repositories/         # Acesso a dados (SQL / PostgreSQL)
│ ├── routes/               # Endpoints da API
│ ├── services/             # Regras de negócio
│ └── main.py               # Inicialização da aplicação FastAPI
│
├── .env                    # Variáveis de ambiente
├── requirements.txt        # Dependências do projeto
├── README.md
└── .gitignore
```

---

## 🐍 Pré-requisitos

- Python **3.10+**
- pip
- PostgreSQL
- Linux / Ubuntu (recomendado)

---

## 🧪 Ambiente Virtual (venv)

```bash
python3 -m venv .venv

source .venv/bin/activate
```

📌 Checklist rápido pós-fix

```bash
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 1️⃣ Criar o ambiente virtual

⚙️ Configuração de Ambiente (.env)

```bash

# Aplicação
APP_HOST=0.0.0.0
APP_PORT=9000

# Banco de Dados - Desenvolvimento (DSV)
DATABASE_DSV_HOST=localhost
DATABASE_DSV_PORT=5432
DATABASE_DSV_NAME=seia_dsv
DATABASE_DSV_USER=usuario
DATABASE_DSV_PASSWORD=senha

# Banco de Dados - Homologação (HML)
DATABASE_HML_HOST=localhost
DATABASE_HML_PORT=5432
DATABASE_HML_NAME=seia_hml
DATABASE_HML_USER=usuario
DATABASE_HML_PASSWORD=senha

# Configurações Adicionais
DEBUG=True
LOG_LEVEL=INFO
```

### 2️⃣ Authorization hash para o usuário admin:


⚙️ Antes de executar a API pela primeira vez, é necessário gerar os hashes das senhas dos usuários:
(APENAS PARA NÌVEL DE TESTE, NÃO RECOMENDADO para PRODUÇÃO)

```bash
# Gerar hashes para o usuário admin
python app/core/scripts/gerar_hashes.py
```

> O que este comando faz:
> 	Cria o diretório app/core/ se não existir
> 	Gera hashes bcrypt para todos os usuários cadastrados
> 	Salva o arquivo app/core/usuarios_hash.json com as senhas protegidas


▶️ Comando para iniciar a API:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
```
