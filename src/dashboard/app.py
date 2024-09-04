import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Título da aplicação

st.markdown(
    """
    <style>
    .header {
        display: flex;
        align-items: center;
        padding: 10px;
        background-color: #FFFFE0  /* Ajuste a cor de fundo conforme necessário */
    }
    .header img {
        height: 100px;
        margin-right: 20px; /* Espaçamento entre a imagem e o título */
    }
    .header h1 {
        margin: 0; /* Remove a margem padrão do título */
    }
    </style>
    <div class="header">
        <img src="https://logopng.com.br/logos/mercado-livre-87.png" alt="Logo">
        <h2>Pesquisa de Mercado - Tênis Esportivos no Mercado Livre</h2>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('../data/ScrapeStore.db')

# Carregar os dados da tabela 'mecardolivre_products' em um DataFrame
df = pd.read_sql_query('SELECT * FROM mercadolivre_products', conn)

# Encerrar conexão com o banco de dados
conn.close()

# Sub título KPIs
st.subheader('Principais KPIs')

# Definindo o layout para KPIs
col1, col2, col3 = st.columns(3)

# KPI 1: Quantidade total de produtos
total_produtos = df.shape[0]
col1.metric(label="Total de produtos", value=total_produtos)

# KPI 2: Quantidade total de marcas
total_marcas = df['brand'].nunique()
col2.metric(label="Total de marcas únicas", value=total_marcas)

# KPI 3: Preço médio em reais (novo preço)
preco_medio = df['new_price'].mean()
col3.metric(label="Preço médio dos produtos", value=f"R$ {preco_medio:.2f}")

# Divisor
st.divider()

# Produtos mais encontrados

# Marcas mais encontradas até a página 15
st.subheader('Top 10 marcas mais encontradas no site até a página 15')
st.markdown('Distribuição da quantidade produtos por marcas')

# Definindo o layout para gráficos e tabelas
col1, col2 = st.columns([6, 6])

# Contar as ocorrências de cada marca e ordenar em ordem decrescente
qtd_marcas = df['brand'].value_counts().nlargest(10)
qtd_marcas_df = qtd_marcas.reset_index()
qtd_marcas_df.columns = ['Marca', 'Total Produtos']

# Mostrar o gráfico de barras ordenado do menor para o maior
fig_bar = px.bar(qtd_marcas_df
                 .sort_values(by='Total Produtos',ascending= True),
                 x='Total Produtos',
                 y='Marca',
                 orientation='h',
                 color_discrete_sequence=['#ffff00'],
                 height=400
                 )
col1.plotly_chart(fig_bar)

# Mostrar a tabela das marcas
col2.dataframe(qtd_marcas_df)

# Divisor
st.divider()

# Preço Médio

# Preço médio por marcas encontradas até a página 15
st.subheader('Top 10 marcas com maior preço médio até a página 15')
st.markdown('Distribuição do preço médio por marcas')

# Definindo o layout para gráficos e tabelas
col1, col2 = st.columns([6, 6])

# Calcular o preço médio por marca
df = df[df['new_price'] > 0] # Desconsiderando marcas que não valor
top_10_average_prices = df.groupby('brand')['new_price'].mean().round(2).nlargest(10)
top_10_average_prices_df = top_10_average_prices.reset_index()
top_10_average_prices_df.columns = ['Marcas', 'Preço Médio']


# Criar o gráfico de barras horizontais
fig_price_bar = px.bar(top_10_average_prices_df
                       .sort_values(by='Preço Médio',ascending= True),
                      x='Preço Médio',
                      y='Marcas',
                      orientation='h',
                      color_discrete_sequence=['#ffff00'],
                      height=400
                      )
col1.plotly_chart(fig_price_bar)

# Mostrar a tabela de preços médios
col2.dataframe(top_10_average_prices_df)

st.divider()

# Satisfação por marca


st.subheader('Top 10 marcas com melhores avaliações')
st.markdown('Distribuição média das avalições por marca')


# Satisfação por marca
df = df[df['reviews_rating_number'] > 0] # Desconsiderando marcas que não tiveram avaliação
avaliacao_marca = df.groupby('brand')['reviews_rating_number'].mean().round(3).nlargest(10)
avaliacao_marca_df = avaliacao_marca.reset_index()
avaliacao_marca_df.columns = ['Marcas', 'Avaliações Média']


# Criar o gráfico de barras horizontais
fig_avaliacoes_bar = px.bar(avaliacao_marca_df
                       .sort_values(by='Avaliações Média', ascending=False),
                      x='Marcas',
                      y='Avaliações Média',
                      orientation='v',
                      color_discrete_sequence=['#ffff00']
                      )


# Adicionar rótulos às barras
fig_avaliacoes_bar.update_traces(texttemplate='%{y}',textposition='inside')

# Define o ângulo dos rótulos do eixo x para 0 graus
fig_avaliacoes_bar.update_layout(xaxis_tickangle=0)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig_avaliacoes_bar)

