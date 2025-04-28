# 🏡Entendendo o Mercado Imobiliário de Fortaleza/CE

## 📜Sumário
1. 📌 [Sobre o Projeto](#-sobre-o-projeto)
2. ⚙️ [Tecnologias Utilizadas](#️-tecnologias-utilizadas)
3. 🚀 [Como Executar](#-como-executar)
4. 📊 [Estrutura do Projeto](#-estrutura-do-projeto)
5. 🗒️ [Licença](#️-licença)
6. 📞 [Contato](#-contato)

## 📌 Sobre o Projeto
Com um Valor Geral de Vendas (VGV) de apróximadamente 8 bilhões de reais[*](https://cbic.org.br/recorde-historico-mercado-imobiliario-de-fortaleza-e-regiao-metropolitana-alcanca-valor-geral-de-vendas-de-r-85-bilhoes-em-2024/), a cidade de Fortaleza tem um mercado imobiliário forte e crescente. Com dados obtidos através do processo de *web scraping* nos sites da Imobiliária Lopes[**](lopes.com.br) e no site Chaves na Mão[***](chavesnamao.com.br) este projeto tem o objetivo de explorar o estado atual do mercado imobiliário.

## ⚙️ Tecnologias Utilizadas
Este projeto foi desenvolvido utilizando:

- 🐍 Python 3.12+
- 📊 Streamlit (Interface)
- 🔢 Duckdb, Pandas & NumPy (Manipulação de Dados)
- 🕸️ Scrapy (Web Scraping)
- 📈 Plotly (Visualização de Dados)

## 🚀 Como Executar
Acesse a aplicação web no [Streamlit Cloud](https://pricingimoveis-fortaleza.streamlit.app/).

#### Execução
1️⃣ **Clone o repositório**
```bash
git clone https://github.com/datalopes1/pricing_imoveis.git
cd pricing_imoveis
```

2️⃣ **Crie e ative um ambiente virtual (recomendado)**
 ```bash
python -m venv .venv
source .venv/bin/activate  # Mac e Linux
.venv\Scripts\activate  # Windows
 ```

3️⃣ **Instale as dependências**
```bash
pip install -r requirements.txt
```

4️⃣ **Execute o projeto**
```bash
streamlit run src/app.py
```
## 📊 Estrutura do Projeto
```plain_text
pricing_imoveis/
│-- data/                       
|   ├── raw/                    # Dados brutos
|   ├── interim/                # Dados provisórios   
|   ├── processed/              # Dados tratados
|   ├── imv_database.db         # Banco de Dados sqlite
|-- docs/
|   ├── img/                    # Imagens utilizadas
|   ├── pricing.pdf             # Versão PDF da EDA
|-- notebooks
|   ├── pricing.ipynb           # Notebook de Análise Exploratória de Dados
|-- src/                         
|   ├── extract/                # Scripts utilizados para Web Scraping
|   ├── load/                   # Scripts de ingestão dos dados
|   ├── transform/              # Scripts de tratamento dos dados
|   ├── app.py                  # Aplicação do Streamlit
|-- .gitignore                  # Arquivos ignorados pelo Git
|-- app.py                      # Aplicação do Streamlit
|-- LICENSE.md                  # Licença
|-- poetry.lock                 # Configuração do Poetry e dependências do projeto
|-- pyproject.toml              # Versões exatas das dependências instaladas
|-- README.md                   # Documentação do projeto
|-- requirements.txt            # Lista de dependências
```

## 🗒️ Licença
Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE.md) para mais detalhes.

## 📞 Contato
- 📬 datalopes1@proton.me
- 🖱️ https://datalopes1.github.io/
- 📱 +55 88 99993-4237
