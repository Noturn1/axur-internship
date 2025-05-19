# Projeto Axur Internship Pipeline

Este repositório automatiza o fluxo de trabalho de:

1. **Scrape** de uma página para extrair uma imagem (suporta Data URLs em Base64 ou URL remota).  
2. **Download** e decodificação da imagem para um arquivo local.  
3. **Inferência** da imagem via API HTTP (modelo `microsoft-florence-2-large`).  
4. **Submissão** do JSON de resposta ao endpoint final.

## Estrutura

├── axur_internship.py # Script principal
├── requirements.txt # Dependências Python
├── .env.example # Variáveis de ambiente (exemplo)
└── README.md # Este arquivo

## Pré-requisitos

- Python 3.8+  
- `pip`  
- Token de API no arquivo `.env` (variável `API_TOKEN`).

## Instalação

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Edite .env e defina API_TOKEN=<seu_token_aqui>
