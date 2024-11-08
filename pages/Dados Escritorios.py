#INFORMAÇÕES

__author__ = "Guilherme Moreira"
__date__ = "01/29/2023"
__version__ = "1.0.0"
__email__ = "guilmoreira@outlook.com"
__objective__='Mapear escritórios AAI ativos'
__status__ = "Complete"



#                                           RODAR O DASHBOARD UTILIZE O CÓDIGO ABAIXO
#############################################################################################################################################
#                                                                                                                                           #
#                               python -m streamlit run aai_analise\aai_dashboard.py --server.port 8521                                     #
#                               python -m streamlit run aai_analise\aai_dashboard.py --server.port 8501                                     #                                                                                                                                             #
#                                                                                                                                           #
#############################################################################################################################################    

import streamlit as st
#from streamlit import experimental_data_editor
import datetime as dt
from datetime import timedelta
from datetime import datetime
from datetime import date
import io
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from PIL import Image
import requests
import seaborn as sns
import time
import zipfile
import base64

######################################################

# from PIL import Image
# import streamlit as st

# # You can always call this function where ever you want

# def add_logo(logo_path, width, height):
#     """Read and return a resized logo"""
#     logo = Image.open(logo_path)
#     modified_logo = logo.resize((width, height))
#     return modified_logo

# my_logo = add_logo(logo_path="aai_analise\logo.jpeg", width=100, height=100)
# st.sidebar.image(my_logo)

# # OR

# st.sidebar.image(add_logo(logo_path="aai_analise\logo.jpeg", width=50, height=60)) 

today = str(date.today())

# 2.0 Link Base de dados
z_aai ="http://dados.cvm.gov.br/dados/AGENTE_AUTON/CAD/DADOS/cad_agente_auton.zip"

# 3.0 Download Base de Dados

verify_ssl = False
aai= requests.get(z_aai,verify=verify_ssl)
aai_zip = zipfile.ZipFile(io.BytesIO(aai.content))


# 4.0 Icone e Titulo
#    #im = Image.open("assets\icon.ico")
# st.set_page_config(
#     page_title="Escritórios AAI",
#     page_icon="book",
#     layout="wide",
# )



# 5.1 Funcao_tratar_csv

@st.cache_data
def aai_csv(file):
    """Definir "pf" ou "pj" e retorna o dataframe"""
    if file == "pf":
        dados=aai_zip.open(f'cad_agente_auton_{file}.csv')
        linhas = dados.readlines()
        lines = [i.strip().decode('ISO-8859-1') for i in linhas]
        lines = [i.split(';') for i in lines]
        df = pd.DataFrame(lines[1:], columns = lines[0])
    else:
        dados=aai_zip.open(f'cad_agente_auton_{file}.csv')
        linhas = dados.readlines()
        lines = [i.strip().decode('ISO-8859-1') for i in linhas]
        lines = [i.split(';') for i in lines]
        df = pd.DataFrame(lines[1:], columns = lines[0])
        #df=df.drop_duplicates(subset='CNPJ',keep='first')

    return df

# 5.2 Chamando a função


arquivo_pj=aai_csv("pj")
#arquivo_pf=aai_csv("pf")

# 5.3 Tratando a base de dados

arquivo_pj.drop(["DENOM_COMERC",'SITE_ADMIN','TP_ENDER'],inplace=True,axis=1)
arquivo_pj.rename(columns={'DENOM_SOCIAL':'Razão Social',
                            'DT_REG':'Data Registro',
                            'DT_CANCEL':'Data Cancelamento',
                            'MOTIVO_CANCEL':'Motivo do Cancelamento',
                            'SIT':'Status Atual',
                            'DT_INI_SIT':'Início do Status',
                            'LOGRADOURO':'Logradouro',
                            'COMPL':'Complemento',
                            'BAIRRO':'Bairro',
                            'MUN':'Município',
                            'UF':'UF',
                            'EMAIL':'Email'
                            },inplace=True)


# 6.0 Configuração da página



# 6.1 Esconder Menu Streamlit
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 6.3 Titulo

st.title("Análise dos Registros")
#st.markdown("""----""")
st.write("Avaliar a base de dados cadastrais junto a CVM e sua distribuição estadual")


#################### ESTRUTURA DASHBOARD ###############################

col1, col2 = st.columns([2, 1])

default_stats='"EM FUNCIONAMENTO NORMAL"'

with col1:
    st.header("Distribuição estadual")

with col2:
    default_value="EM FUNCIONAMENTO NORMAL"
    values=list(arquivo_pj['Status Atual'].unique())
    situacao = st.selectbox(
    '**Situacao**',values
    ,index=values.index(default_value))

    #Todos os TradeDesks selecionados
    if not situacao:
        situacao="EM FUNCIONAMENTO NORMAL"

#################### ESCRITÓRIOS POR ESTADO ###############################

filtro_situacao = arquivo_pj[arquivo_pj['Status Atual']==situacao].copy()
tabeladinamica=filtro_situacao['UF'].value_counts().to_frame()
tabeladinamica=tabeladinamica.rename(columns={'count':'Escritórios'})
tabeladinamica.reset_index(inplace=True)

grafico_barra_estado = make_subplots(rows=1, cols=1,shared_yaxes=False, horizontal_spacing=0.1)

if situacao== "CANCELADA":
    
    grafico_barra_estado.add_trace(go.Bar(
        x=tabeladinamica['UF'],
        y=tabeladinamica['Escritórios'],
        orientation='v',
        name='Normal',
        marker=dict(color="red") 
    ), row=1, col=1)

else:
      
    grafico_barra_estado.add_trace(go.Bar(
        x=tabeladinamica['UF'],
        y=tabeladinamica['Escritórios'],
        orientation='v',
        name='Normal',
        marker=dict(color="green") 
    ), row=1, col=1)


######### tabela #############


# Create a table

tabela_aai = ff.create_table(tabeladinamica.head(7))

# Define CSS styles for text and background using HTML
tabela_aai_styled = tabela_aai.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    width=380,  # Adjust the width to your desired value
    height=400,
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    autosize=True,
)

# # Define CSS styles using HTML
# tabela_aai_styled.update_traces(
#     selector=dict(selector="td:hover", props=[("font-size", "18px"), ("color", "green")]),
#     rowheight=[40, 40, 40, 40],
# )

# tabela_aai_styled.update_traces(
#     cells=dict(
#         values=[[str(c) for c in row] for row in tabeladinamica],
#         align="center"  # Center-align the text within the cells
#     )
# )

#################### ESTRUTURA DASHBOARD ###############################

with col1:
    st.plotly_chart(grafico_barra_estado)


with col2:
    st.plotly_chart(tabela_aai_styled)

######################################################################################
############################################# GRAFICO DE BARRAS #######################
sit_anual=arquivo_pj.copy()
sit_anual['Início do Status']=pd.to_datetime(sit_anual['Início do Status'])
sit_anual['year']=sit_anual['Início do Status'].dt.year

count_by_year_cancelada = sit_anual[sit_anual['Status Atual']== 'CANCELADA']['year'].value_counts().reset_index().sort_values(by=['year'])
count_by_year_normal = sit_anual[sit_anual['Status Atual']== 'EM FUNCIONAMENTO NORMAL']['year'].value_counts().reset_index().sort_values(by=['year'])
count_by_year_cancelada.columns = ['year', 'Canceladas']
count_by_year_normal.columns = ['year', 'Normal']

consolidado_por_ano=pd.merge(count_by_year_normal,count_by_year_cancelada,on='year',how='inner')


#grafico_barra_status = go.Figure()
grafico_barra_status = make_subplots(rows=1, cols=1,shared_yaxes=False, horizontal_spacing=0.1)

grafico_barra_status.add_trace(go.Bar(
    x=consolidado_por_ano['year'],
    y=consolidado_por_ano['Normal'],
    orientation='v',
    name='Normal',
    marker=dict(color='green') 
), row=1, col=1)

grafico_barra_status.add_trace(go.Bar(
    x=consolidado_por_ano['year'],
    y=consolidado_por_ano['Canceladas'],
    orientation='v',
    name='Canceladas',
    marker=dict(color='red')
), row=1, col=1)

grafico_barra_status.update_layout(
    #title='Situação dos Escritórios AAI por Ano',
    xaxis=dict(title='Date'),
    xaxis2=dict(title='Date'),
    yaxis=dict(title='Count', side='right', showgrid=False, zeroline=False),
    showlegend=True  # Show the legend for distinguishing between bar and line graphs
)

# Customize layout
grafico_barra_status.update_layout(
    barmode='group',  # Bars are grouped together
    yaxis_title='Quantidade de Escritórios',
    xaxis_title='Ano',
    margin=dict(l=80, r=20, t=20, b=20),
    width=1300,  # Adjust the width to your desired value
    height=400,
    #title='Registros de Escritórios AAI por ano',
    bargap=0.2,
    xaxis=dict(
        title='Ano',
        tickmode='array', 
        tickvals=consolidado_por_ano['year'],
        tickangle=-90,
        showline=False,
        showgrid=False,
        zeroline=False,  
        titlefont=dict(family='Arial, bold'),
        fixedrange=True,
        #ticklen=0
    ),

    yaxis=dict(
        showline=False,
        showgrid=False,
        zeroline=False,  
        titlefont=dict(family='Arial, bold'),
        fixedrange=True
        #ticklen=0
    )
)



#grafico_barra_status.update_layout(autosize=False, margin=dict(t=0, b=0, l=0, r=0))
# Show the plot

######################################################################################

col3 = st.columns(1)

with col3[0]:
    st.header("Escritórios Criados e Cancelados por Ano")
    st.plotly_chart(grafico_barra_status)