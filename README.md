*Análise de Dados com Streamlit*

*Introdução*

Este código é uma aplicação Streamlit que permite realizar análises de dados de uma base de dados SQL. A aplicação inclui filtros para ano e mês, seleção de produto e gráficos para visualizar a soma de "TotalDue" por produto e por mês e ano.

*Código*

```
# Código omitido para brevidade
```

*Como Usar*

*Passo 1: Instalar Dependências*

Antes de executar o código, certifique-se de instalar as dependências necessárias:

```
bash
pip install streamlit pandas matplotlib pyodbc logging datetime
```

*Passo 2: Criar Base de Dados*

Crie uma base de dados SQL e insira os dados que deseja analisar. Neste caso foi criada um banco de dados no azure

*Passo 3: Configurar o Código*

1. Numa situação corriqueira seria necessário colocar informações de acesso ao banco. Neste caso, essas informações já estão escritas no código.
2. Coloque a query desejada. Por padrão jé existe uma query otimizada para esta demonstração. 


*Passo 4: Executar o Código*

Execute o código usando:

```
bash
streamlit run dash.py ou python -m streamlit run dash.py
```

*Passo 5: Utilizar a Aplicação*

1. Selecione o ano e mês desejados.
2. Selecione o produto desejado.
3. Selecione a região desejada
4. Visualize os gráficos de soma de "TotalDue" por produto, por região e por mês e ano.

*Funcionalidades*

- Filtros para ano e mês
- Seleção de produto
- Seleção de região
- Gráficos de soma de "TotalDue" por produto e por mês e ano
- Métricas de soma de "TotalDue" por produto selecionado e total

