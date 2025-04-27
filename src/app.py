# ----- CONFIGURAÇÕES ----

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import duckdb

st.set_page_config(
    page_title="Mercado Imobiliário Fortaleza/CE",
    page_icon = "🏡",
    layout = "wide"
)

st.title("🏡 Análise do Mercado Imobiliário de Fortaleza/CE")
st.markdown("**Dados Extraídos de Imobiliária Lopes e Chaves na Mão**")

# ----- FUNÇÕES -----
@st.cache_data
def load_data():
    """
    Carrega os dados em um pd.DataFrame
    """
    df = pd.read_csv("data/processed/clean_data.csv")
    return df

def plot_hist(data:pd.DataFrame, x:str, color:str, title:str, xlabel:str, ylabel:str):
    """
    Cria um histograma utilizando Plotly Express
    """
    fig = px.histogram(
        data,
        x = x,
        color = color,
        histnorm='percent',
        barmode = 'overlay',
        nbins=40,
        title = title,
        labels = {x: xlabel.capitalize(), 'count': ylabel, color: color.capitalize()},
        color_discrete_sequence=['#3d405b', '#00c6c2', '#168582', '#324b4a']
    )

    fig.update_layout(
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        xaxis_title = xlabel,
        yaxis_title = ylabel,
        bargap = 0.1
    )

    return fig

def plot_scatter(data:pd.DataFrame, title:str, x:str, y:str, xlabel:str, ylabel:str):
    """
    Cria um scatter plot utilizando Plotly Express
    """
    fig = px.scatter(
        data,
        x=x,
        y=y,
        title=title,
        labels={x: xlabel, y: ylabel},
        trendline='ols',
        trendline_color_override='#9c5a5d',
        color_discrete_sequence=['#00c6c2', '#168582', '#324b4a'],
        opacity=0.30

    )
    pass

    fig.update_layout(
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
    )

    return fig

def plot_bar(data:pd.DataFrame, title:str, x:str, y:str, xlabel:str, ylabel:str):
    """
    Cria um gráfico de barras utilizando Plotly Express
    """
    fig = px.histogram(
        data,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=['#3d405b', '#00c6c2', '#168582', '#324b4a']
    )

    fig.update_layout(
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        xaxis_title=xlabel,
        yaxis_title=ylabel
    )

    return fig

def plot_bars(data:pd.DataFrame, title:str, x:str, xlabel:str, ylabel:str):
    """
    Cria um gráfico de barras utilizando Plotly Express
    """
    fig = px.histogram(
        data,
        x=x,
        histnorm='percent',
        title=title,
        color_discrete_sequence=['#3d405b', '#00c6c2', '#168582', '#324b4a']
    )

    fig.update_layout(
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        bargap=0.1
    )
    pass

    return fig

# ----- CARREGAMENTO DOS DADOS -----

df = load_data()

# ----- TABS ------

tab_dash, tab_report = st.tabs(["📊 Dashboard", "📝 Report"])

# ----- FILTROS ------
with st.sidebar:
    st.header("Filtros")

    # Filtro por Tipo de Imóvel
    tipos_unicos = df['tipo'].unique()
    tipo_selecionado = st.selectbox("Tipo de Imóvel", ['Todos'] + list(tipos_unicos))

    # Filtro por Bairro (Localização)
    bairros_unicos = df['localizacao'].unique()
    bairros_selecionados = st.multiselect("Bairro", bairros_unicos)

    # Filtro por Faixa de Preço
    preco_min, preco_max = int(df['preco'].min()), int(df['preco'].max())
    preco_range = st.slider("Faixa de Preço (R$)", preco_min, preco_max, (preco_min, preco_max))

    # Filtro por SER (se presente nos seus dados)
    if 'ser' in df.columns:
        sers_unicos = df['ser'].unique()
        ser_selecionado = st.selectbox("SER", ['Todos'] + list(sers_unicos))

# ----- FILTRAGEM DOS DADOS -----

df_filtrado = df.copy()

if tipo_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['tipo'] == tipo_selecionado]

if bairros_selecionados:
    df_filtrado = df_filtrado[df_filtrado['localizacao'].isin(bairros_selecionados)]

preco_min_selecionado, preco_max_selecionado = preco_range
df_filtrado = df_filtrado[(df_filtrado['preco'] >= preco_min_selecionado) & (df_filtrado['preco'] <= preco_max_selecionado)]

if 'ser' in df.columns and ser_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['ser'] == ser_selecionado]


# ----- DASHBOARD -----
with tab_dash:

    # KPIs
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="🏡 Total de Imóveis", value=f"{df_filtrado.shape[0]:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with col2:
        st.metric(label="💰 Volume Geral de Vendas", value=f"R$ {(df_filtrado['preco'].sum())/1000000000:,.2f} bi".replace(",", "X").replace(".", ",").replace("X", "."))
    with col3:
        st.metric(label="💸 Preço Mediano", value=f"R$ {df_filtrado['preco'].median():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            plot_hist(df_filtrado[df_filtrado['preco']<=1_000_000], 'preco', 'tipo', 
                    'Distribuição dos Preços por Tipo (até R$ 1mi)', 
                    'Preço (R$)', 'Proporção (%)'), use_container_width=True)

    with col2:
            st.plotly_chart(
            plot_scatter(df_filtrado, 'Correlação Preço x Área', 'area', 'preco', 'Área (m²)', 'Preço (R$)'),
            use_container_width=True
        )


    bairros = duckdb.sql(
        """
        SELECT
            localizacao
            , ser AS SER
            , AVG(preco)::DECIMAL(18, 2) AS preco_medio
            , COUNT(localizacao) AS qt_imoveis
        FROM df_filtrado
        GROUP BY localizacao, ser
        HAVING qt_imoveis > 20
        ORDER BY  preco_medio DESC
        LIMIT 10
        """
    ).to_df()


    st.plotly_chart(
        plot_bar(bairros, 'Bairros com Maior Preço Médio de Imóvel', 'localizacao', 'preco_medio', 'Bairro', 'Preço Médio (R$)')
    )

    col3, col4 = st.columns(2)
    with col3:
        bairros_m2 = duckdb.sql(
            """
            WITH cte AS (
                SELECT
                    localizacao
                    , preco/area AS preco_m2
                FROM df_filtrado
                GROUP BY localizacao, area, preco
            )
            SELECT 
                localizacao
                , AVG(preco_m2) AS avg_preco_m2
                , COUNT(localizacao) AS qt_imoveis 
            FROM cte
            GROUP BY localizacao
            HAVING qt_imoveis > 20
            ORDER BY 2 DESC
            LIMIT 10
            """
        )
        
        st.plotly_chart(plot_bar(bairros_m2, 'Bairros com Maior Preço de m²', 'localizacao', 'avg_preco_m2', 'Bairro', 'Preço (R$/m²)'))

    with col4:
        bairros_m2_2 = duckdb.sql(
            """
            WITH cte AS (
                SELECT
                    localizacao
                    , preco/area AS preco_m2
                FROM df_filtrado
                GROUP BY localizacao, area, preco
            )
            SELECT 
                localizacao
                , AVG(preco_m2) AS avg_preco_m2
                , COUNT(localizacao) AS qt_imoveis 
            FROM cte
            GROUP BY localizacao
            HAVING qt_imoveis > 20
            ORDER BY 2 ASC
            LIMIT 10
            """
        )    

        st.plotly_chart(plot_bar(bairros_m2_2, 'Bairros com Menor Preço de m²', 'localizacao', 'avg_preco_m2', 'Bairro', 'Preço (R$/m²)'))

    # Dados do dataframe
    st.markdown("**Dados originais**")
    st.dataframe(df_filtrado)
    
    st.markdown("---")
    st.markdown("Desenvolvido por [André Lopes](https://www.linkedin.com/in/andreluizls1/) (Abril 2025)")

with tab_report:
    st.subheader("📝 Relatório de Análise")
    st.markdown(
        """
        ### Sumário Executivo

        **Propósito**: Análise do mercado imobiliáro da cidade de Fortaleza/CE no mês de Abril de 2025.

        **Insights-chave**:

        - Os bairros mais valorizados da cidade se encontram na Secretária Regional Executiva (SER) 2.
        - O bairro Parque Iracema apresenta bom potencial para investimentos, os bairros mais valorizados são Mucuripe, Meireles e Guararapes.
        - O número de banheiros e vagas de garagem tem maior influência no preço que o número de quartos.

        ---

        ### 1. Introdução

        Com um Valor Geral de Vendas (VGV) de apróximadamente 8 bilhões de reais[*](https://cbic.org.br/recorde-historico-mercado-imobiliario-de-fortaleza-e-regiao-metropolitana-alcanca-valor-geral-de-vendas-de-r-85-bilhoes-em-2024/), a cidade de Fortaleza tem um mercado imobiliário forte e crescente. Com dados obtidos através do processo de *web scraping* nos sites da Imobiliária Lopes[**](lopes.com.br) e no site Chaves na Mão[***](chavesnamao.com.br) este projeto tem o objetivo de explorar o estado atual do mercado imobiliário.

        **Origem dos Dados:**

        - Raspagem de dados públicos realizada nos sites:
            - Imobiliária Lopes
            - Chaves na Mão

        **Escopo:** Foram exploradas as relações entre área, número de comodos e outras variáveis em relação ao preço dos imóveis.

        ----

        ### 2. Dados

        #### Dicionário dos dados
        |Coluna|Descrição|
        |---|---|
        |`id`|Identificador único de cada registro|
        |`origem`|Site de onde os dados foram coletados|
        |`tipo`|Tipo de imóvel|
        |`localizacao`|Bairro de Fortaleza/CE|
        |`ser`|Secretária Executiva Regional do bairro|
        |`prox_centro`|Bairro localizado próximo ao Centro|
        |`prox_orla`|Bairro próximo à orla maritima|
        |`area`|Área em metros quadrados|
        |`quartos`|Número de quartos|
        |`banheiros`|Número de banheiros|
        |`vagas`|Número de vagas de garagem|
        |`condo`|Valor em R$ do condomínio|
        |`preco`|Valor de anúncio em R$|
        |`timestamp_extracao`|Timestamp da extração dos dados|  

        #### Qualidade dos dados
        - Nulos e duplicados: Foram encontrados valores duplicados em 141 anúncios. 
        - *Outliers:* Foram encontrados outliers em `quartos`, `banheiros`, `vagas`, `condo` e `preco`. 

        #### Limpeza e manipulação
        - Foram criadas colunas ordinais para melhor visualizações dos dados sobre quartos, banheiros e vagas. 
        - Foram removidos os dados duplicados e valores desproporcionais. 

        ---

        ### 3. Análises e insights
        #### 3.1. Tipos de Imóveis em Oferta
        """
    )

    df = load_data()
    df = duckdb.sql(
    """
    SELECT
        *
        , CASE WHEN quartos >= 5 THEN 5 ELSE quartos END AS quartos_ord
        , CASE WHEN banheiros >= 5 THEN 5 ELSE banheiros END AS banheiros_ord
        , CASE WHEN vagas >= 5 THEN 5 ELSE vagas END AS vagas_ord
    FROM df
    """).to_df()
    df = duckdb.sql("SELECT * FROM df WHERE tipo IN ('Apartamento', 'Casa', 'Condomínio')").to_df()

    st.plotly_chart(plot_bars(df, 'Proporção por Tipo de Imóvel', 'tipo', 'Tipo', 'Proporção (%)'), use_container_width=True)

    st.markdown(
        """
        Mais da metade dos imóveis em oferta são apartamentos, seguidos por casas e condomínios. O mercado imobiliário em grandes centros urbanos costuma se concentra na venda de apartamentos para uma parcela maior da população, e casas em condomínios para a clientes de classe média alta em diante, as razões de escolha por este tipo de imóvel costumam ser semelhantes:

        - Infraestrutura compartilhada;
        - Privacidade e segurança;
        - Potencial de valorização.

        #### 3.2. Bairros com maior oferta 
        """
    )

    bairros = duckdb.sql("SELECT localizacao, COUNT(localizacao) AS count FROM df GROUP BY localizacao ORDER BY 2 DESC LIMIT 10")

    st.plotly_chart(
        plot_bar(bairros, 'Distribuição de Imóveis por Bairro', 'localizacao', 'count', 'Bairro', 'Contagem')
    )

    st.markdown(
        """
        A oferta de imóveis se concentra em bairros da Secretária Executiva Regional (SER) 2 e 7. São áreas próximas ao centro e de bairros nobres da capital cearense, por tanto privilegiadas para o mercado imobiliário. 
        """
    )

    ser = duckdb.sql("SELECT ser, COUNT(ser) AS count FROM df GROUP BY ser ORDER BY 2 DESC")

    col5, col6 = st.columns(2)
    with col5:
        st.plotly_chart(
            plot_bar(ser, 'Distribuição de Imóveis por SER', 'ser', 'count', 'Secretária Executiva Regional', 'Contagem'), use_container_width=True
        )
    with col6:
        img = 'doc/img/JktxiIv.png'
        st.image(img, use_container_width=True)

    st.markdown(
        """
        #### 3.3. Distribuição por Comodos

        Existe um padrão na oferta de imóveis novos que é de apartamentos ou casas com 2 ou 3 quartos, e 2 ou 3 banheiros, sendo a estrutura mais comum 3 quartos e 2 banheiros. Em relação à vagas de garagem é importante sempre pensar na mobilidade urbana de uma cidade de grande população como Fortaleza, é muito comum a necessidade de um transporte particular então é natural que a oferta de imóveis com nenhuma vaga de garagem seja baixa. 
        """
    )

    st.plotly_chart(
        plot_bars(df, 'Distribuição de Quartos', 'quartos_ord', 'Quartos', 'Proporção (%)'), use_container_width=True
    )

    st.plotly_chart(
        plot_bars(df, 'Distribuição de Banheiros', 'banheiros_ord', 'Banheiros', 'Proporção (%)'), use_container_width=True
    )

    st.plotly_chart(
        plot_bars(df, 'Distribuição de Vagas', 'vagas_ord', 'Vagas', 'Proporção (%)'), use_container_width=True
    )

    st.markdown(
        """
        #### 3.4. Distribuição de Preço
        """
    )

    st.plotly_chart(
        plot_bars(df, 'Distribuição por Preço de Oferta', 'preco', 'Preço (R$)', 'Proporção (%)'), use_container_width=True
    )

    st.text(
        """
        É natural valores cima do normal para dados tratando do mercado imobiliário, ofertas fora de valor ou imóveis com alto valor agregado são outliers naturais e esperados se tratando de dados sobre este ramo. Vamos visualizar os dados para imóveis até R$ 5.000.000,00 em seu valor de oferta. 
        """
    )

    st.plotly_chart(
        plot_bars(df[df['preco']<=5_000_000], 'Distribuição por Preço de Oferta (até R$ 5mi)', 'preco', 'Preço (R$)', 'Proporção (%)'), use_container_width=True
    )

    st.text("A oferta se concentra em imóves de até R$ 1mi.")
    st.markdown("#### 3.5. Preço x Tipo")
    st.plotly_chart(
        plot_hist(
            df[df['preco']<=1_000_000], 'preco', 'tipo', 'Distribuição Preço x Tipo', 'Preço (R$)', 'Proporção (%)' 
        ), use_container_width=True
    )
    st.text(
        """
        Apartamentos são os imóveis mais acessíveis, é possível encontrar eles em toda faixa de preço mas são predominantes em valores menores que R$ 500.000,00. Casas dentro e fora de condomínios também aparecem em praticamente todas as faixar de preço mas aparecem mais a partir dos R$ 300.000,00. 
        """
    )
    st.markdown("#### 3.6 Preço Médio por Bairro")

    bairros_2 = duckdb.sql(
    """
    SELECT
        localizacao
        , AVG(preco)::DECIMAL(18, 2) AS preco_medio
        , COUNT(localizacao) AS qt_imoveis
    FROM df
    GROUP BY localizacao
    HAVING qt_imoveis > 20
    ORDER BY 2 DESC
    LIMIT 10
    """
    )

    st.plotly_chart(
        plot_bar(bairros_2, 'Preço Médio por Bairro (Top 10)', 'localizacao', 'preco_medio', 'Baiirro', 'Preço (R$)'), use_container_width=True
    )
    st.text(
        """
        Os bairros com maior média de preço estão localizados próximos à orla e ao centro da cidade (especialmente nas SER 2 e 7). O Alphaville Fortaleza é localizado dentro do bairro da Sabiaguaba, e próximo também a outra área valoriza que são bairros próximos à cidade de Eusébio (como o Coaçu) que é uma cidade parte da Região Metropilitana de Fortaleza (RMF) que passa por um alto crescimento e expansão de infraestrutura e mercado imobliário.
        """
    )
    st.markdown("#### 3.7 Preço Médio por Metro Quadrado") 

    bairros_3 = duckdb.sql(
    """
    WITH cte AS (
        SELECT
            localizacao
            , preco/area AS preco_m2
        FROM df
        GROUP BY localizacao, area, preco
    )
    SELECT 
        localizacao
        , AVG(preco_m2) AS avg_preco_m2
        , COUNT(localizacao) AS qt_imoveis 
    FROM cte
    GROUP BY localizacao
    HAVING qt_imoveis > 20
    ORDER BY 2 DESC
    LIMIT 10
    """
    )
    st.plotly_chart(
        plot_bar(bairros_3, 'Preço Médio m² por Bairro (Top 10)', 'localizacao', 'avg_preco_m2', 'Bairro', 'Preço (R$/m²)')
    )
    st.text(
        """
        Mucuripe, Meireles e Guararapes se demonstram bairros com alto potencial de investimento por seu alto valor de metro quadrado, mas isso exige altos aportes, assim como o bairro de Lourdes. O Parque Iracema também possui um alto valor no preço do metro quadrado, ele está localizado na SER 6, e é próximo de bairros como Messejana, Cambeba e Cajazeiras que possuem um grande extensão territorial. 
        """
    )
    st.markdown(
        """
        #### Conclusões e recomendações
        - O tipo de imóvel mais amplamente ofertado são apartamentos, também são os imóveis mais acessíveis. Casas dentro e foram de condomínios começam a aparecer em ofertas a partir de R$ 300.000,00. 
        - Os bairros das Secretárias Executiva Regionais (SER) 2 e 7 são os mais valorizados e com maior número de imóveis ofertados. 
        - Mucuripe, Meireles e Guararapes se demonstram bairros com alto potencial de investimento por seu alto valor de metro quadrado, mas isso exige altos aportes, assim como o bairro de Lourdes. O Parque Iracema também possui um alto valor no preço do metro quadrado, ele está localizado na SER 6, e é próximo de bairros como Messejana, Cambeba e Cajazeiras que possuem um grande extensão territorial.
        - Bairros da SER 4 como Benfica e Fátima também apresentam bom potencial de investimento pela proximidade com o centro e infraestrutura urbana.  
        - As variáveis que tem maior influência no preço de imóvel são o número de banheiros, vagas de garagem e áreea. O número de quartos tem uma influência menor, sendo alguns padrões de oferta comuns imóveis com 3 quartos e 2 a 3 banheiros.
        """
    )

    st.markdown("---")
    st.markdown("Desenvolvido por [André Lopes](https://www.linkedin.com/in/andreluizls1/) (Abril 2025)")