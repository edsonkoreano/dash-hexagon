import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from interface_db import interface_db

# Configuração da página
st.set_page_config(page_title="Dash acompanhamento vendas",page_icon=":bar_chart:",layout="wide")

# Título da aplicação
st.title("Acompanhamento de vendas")

# Barra lateral
st.sidebar.title("Opções")

# Configuração da conexão com o banco de dados

# Instanciar classe
db = interface_db(
    server="server-teste-bi.database.windows.net",
    database="teste_bi",
    username="edsonsabino@server-teste-bi",
    password="#capivara92"
)

# Consulta SQL
query_default="""select 
                ord.SalesOrderID
                ,ord.OrderDate
                ,ord.TotalDue
                ,prd.ProductID
                ,prd.Name as Product
                ,adr.StateProvince
                from 
                [SalesLT].[SalesOrderHeader] ord
                left join [SalesLT].[SalesOrderDetail] detail
                on ord.SalesOrderID=detail.SalesOrderID
                left join [SalesLT].[Product] prd 
                on detail.ProductID=prd.ProductID
                left join [SalesLT].[Address] adr
                on adr.AddressID = ord.ShipToAddressID
                """
query = st.sidebar.text_area("Consulta SQL", value=query_default, height=300)

# Execução da consulta
if st.sidebar.button("Executar Consulta SQL"):
    try:
        # Criação do DataFrame com o resultado
        df = db.execute_query(query)

        # Conversão da coluna OrderDate para datetime
        df['OrderDate'] = pd.to_datetime(df['OrderDate'])

        # Salvar o resultado em um arquivo
        df.to_csv("geral.csv", sep=";", index=False)

        st.success("Consulta executada com sucesso! Resultado salvo em geral.csv")
    except Exception as e:
        st.error(f"Erro ao executar consulta: {e}")

# Leitura. Se o usuário não submeter a query o programa buscará o arquivo mais recente salvo
df=pd.read_csv('geral.csv',sep=';')

# Conversão da coluna OrderDate para datetime (garantir)
df['OrderDate'] = pd.to_datetime(df['OrderDate'])

# Verificação se o arquivo foi gerado
if len(df)>0:
    # Filtros para ano e mês
    anos = df['OrderDate'].dt.year.unique().tolist()
    selected_ano = st.sidebar.selectbox("Selecione um ano", anos)

    meses = df['OrderDate'].dt.month.unique().tolist()
    selected_mes = st.sidebar.selectbox("Selecione um mês", meses)

    # Filtrar o DataFrame
    df_filtrado = df[(df['OrderDate'].dt.year == selected_ano) & 
                     (df['OrderDate'].dt.month == selected_mes)]

    # diferentes produtos
    produtos = df_filtrado['Product'].unique().tolist()

    # Buscar produtos mais representativos para default
    df_por_produto = df.groupby('Product')['TotalDue'].sum().reset_index()
    produtos_top_5=df_por_produto.nlargest(5,'TotalDue')['Product'].values

    # Multi Select box para filtrar por produto
    selected_produto = st.sidebar.multiselect('Produtos',produtos,produtos_top_5.tolist())

    # Filtrar o DataFrame por produto selecionado no multiselect
    df_filtrado = df_filtrado[df_filtrado['Product'].isin(selected_produto)]

    # Filtrar por região

    regioes = df['StateProvince'].unique().tolist()
    selected_regiao = st.sidebar.multiselect("Selecione uma região", regioes,regioes)

    # Filtragem. ano, mes, produto e regiao
    df_filtrado = df_filtrado[df_filtrado['StateProvince'].isin(selected_regiao)]

    # Métricas
    sub_col1,sub_col2, sub_col3= st.columns([2,2,1])
    with sub_col1:
        total_due_filtered = df_filtrado['TotalDue'].sum()
        st.metric("Total Produtos selcionados", f"R${total_due_filtered:,.2f}")
    with sub_col2:
        total_due = df['TotalDue'].sum()
        st.metric("Total Produtos", f"R${total_due:,.2f}")
    with sub_col3:
        percent=total_due_filtered/total_due
        st.metric("Porcentagem", f"{100*percent:,.2f}%")        
    st.divider()


    st.header("Gráfico de Barras - Soma de TotalDue por Produto selecionado")
    df_plot = df_filtrado.groupby('Product')['TotalDue'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.bar(df_plot['Product'], df_plot['TotalDue'])
    plt.xticks(rotation=90)
    st.pyplot(fig)

    st.divider()
    st.header("Gráfico de Linhas - Soma de TotalDue por Mês e Ano")
    df_plot = df_filtrado.groupby('OrderDate')['TotalDue'].sum().reset_index()

    fig, ax = plt.subplots()
    plt.plot(df_plot['OrderDate'], df_plot['TotalDue'])
    plt.xlabel('Data')
    plt.ylabel('Total Due')
    plt.xticks(rotation=45)
    st.write("a figura não pode ser materializada, pois todos os dados estão em uma única data")
    #st.pyplot(fig)


# Fechamento da conexão
db.disconnect()