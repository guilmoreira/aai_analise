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
#                               python -m streamlit run aai_analise\Home.py --server.port 8501                                     #
#                               python -m streamlit run aai_analise\aai_dashboard.py --server.port 8501
#                               python -m streamlit run G:\OneDrive - Polo Capital\python_shared\aai_analise\Home.py --server.port 8501 
#                               python -m streamlit run "G:\OneDrive - Polo Capital\python_shared\aai_analise\Home.py" --server.port 8501                                                                                                                                             #
#                                                                                                                                           #
#############################################################################################################################################    



import streamlit as st
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

today = str(date.today())

# 2.0 Link Base de dados
z_aai ="http://dados.cvm.gov.br/dados/AGENTE_AUTON/CAD/DADOS/cad_agente_auton.zip"

# 3.0 Download Base de Dados

verify_ssl = False
aai= requests.get(z_aai,verify=verify_ssl)
aai_zip = zipfile.ZipFile(io.BytesIO(aai.content))


# 4.0 Icone e Titulo
   #im = Image.open("assets\icon.ico")
st.set_page_config(
    page_title="Escritórios AAI",
    page_icon="book",
    layout="wide",
    initial_sidebar_state="expanded"
)


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


#1 s.0 Configuração da página



# 6.1 Esconder Menu Streamlit
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 6.3 Titulo

# HEADER
#st.image('aai_analise\source\header.png', use_column_width=True)
#st.markdown("""----""")
st.write("Esta ferramenta tem por objetivo simplificar a consulta dos **Agentes Autônomos de Investimento (AAI)-PJ** cadastrados juntos a CVM.")

analise_geral=arquivo_pj[arquivo_pj['Status Atual']=="EM FUNCIONAMENTO NORMAL"].copy()

total_escritorios=len(analise_geral['CNPJ'].unique())
estados=len(analise_geral['UF'].unique())
mais_antigo=pd.to_datetime(analise_geral['Início do Status']).min().year

principal_estado=analise_geral['UF'].value_counts().to_frame()
principal_estado=principal_estado.rename(columns={'count':'Escritórios'})
principal_estado.reset_index(inplace=True)

estado_escr=principal_estado.iloc[0,0]
num_excr_est=principal_estado.iloc[0,1]

#wch_colour_box = (0,204,102)
caixa=(0,204,102)
letra=(0,0,0)
nome="Observations"
tam=24
vari=123

def custom_metric(name,box,letter,variavel,tamanho,i_name):
        
    wch_colour_box = box
    wch_colour_font = letter
    fontsize = 24
    valign = "left"
    iconname = i_name
    sline = name
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    i = variavel

    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                {wch_colour_box[1]}, 
                                                {wch_colour_box[2]}, 0.75); 
                            color: rgb({wch_colour_font[0]}, 
                                    {wch_colour_font[1]}, 
                                    {wch_colour_font[2]}, 0.75); 
                            font-size: {fontsize}px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            <i class='{iconname} fa-xs'></i> {i}
                            </style><BR><span style='font-size: 14px; 
                            margin-top: 0;'>{sline}</style></span></p>"""

    return st.markdown(lnk + htmlstr, unsafe_allow_html=True)

#a=custom_metric("teste",caixa,letra)

cor_caixa_esc=(89, 201, 165)
cor_caixa_estados=(0, 175, 185)
cor_caixa_antigo=(255, 253, 152)
icon_antigo="fa fa-calendar"
icon_estados="fa fa-map"
icon_escritorios="fa fa-building"

col01, col02, col03, col04 = st.columns([1,1,1,1])

with col01:
    caixa_esc=custom_metric("Total de Escritórios",cor_caixa_esc,letra,total_escritorios,tam,icon_antigo)
with col02:
    caixa_estados=custom_metric("Total de Estados",cor_caixa_estados,letra,estados,tam,icon_estados)
with col03:
    caixa_antigo=custom_metric(f"Estado com {num_excr_est} escritórios",cor_caixa_estados,letra,estado_escr,18,icon_estados)
with col04:
    caixa_antigo=custom_metric("Ano - Escritório Mais Antigo",cor_caixa_antigo,letra,mais_antigo,tam,icon_escritorios)

######################################################################################
#Busca
      

search_df=arquivo_pj[arquivo_pj['Status Atual']=='EM FUNCIONAMENTO NORMAL']
search_df=search_df[['CNPJ','Razão Social','Início do Status',
    'Logradouro', 'Complemento', 'Bairro', 'Município', 'UF', 'CEP', 'DDD',
    'TEL', 'Email']]
search_df.rename(columns={'Logradouro':'Endereço'},inplace=True)

from datetime import datetime

today_date = datetime.today()
search_df['Início do Status'] = pd.to_datetime(search_df['Início do Status'])
search_df['Anos em Operação'] = (today_date - search_df['Início do Status']).dt.days // 365

st.markdown("""----""")

st.header("Busca de Escritórios AAI")
col4, col5, col6 = st.columns([1,1, 1])

with col4:
    estado = st.multiselect(
    '**Estado**',
    list(sorted(search_df['UF'].unique())),default=["SP",'RJ'])

    #Todos os TradeDesks selecionados
    if not estado:
        estado=list("SP")

search_df_uf=search_df[search_df['UF'].isin(estado)]

with col5:
    municipio = st.multiselect(
    '**Município**',
    list(sorted(search_df_uf['Município'].unique())))

    #Todos os TradeDesks selecionados
    if not municipio:
        municipio=search_df_uf['Município'].unique()

search_df_mn=search_df_uf[search_df_uf['Município'].isin(municipio)]

with col6:
    bairro = st.multiselect(
    '**Bairro**',
    list(sorted(search_df_mn['Bairro'].unique())))

    #Todos os TradeDesks selecionados
    if not bairro:
        bairro=search_df_mn['Bairro'].unique()


search_df_bairro=search_df_mn[search_df_mn['Bairro'].isin(bairro)]

columns_aai = st.sidebar.multiselect(
    '**Dados Desejados**',
    list(sorted(search_df_bairro.columns.unique())),default=['Razão Social','UF','Município','Bairro', 'DDD', 'TEL', 'Email','CEP'])

if not columns_aai:
        columns_aai=['Razão Social','UF','Município','Bairro', 'DDD', 'TEL', 'Email']

search_df_clean=search_df_bairro[columns_aai]

#search_aai_df = ff.create_table(search_df_clean)

# Create a text input widget for filtering
filter_text = st.text_input('Encontrar um escritório específico:', '')

# Filter the DataFrame based on the text input
search_final = search_df_clean[search_df_clean['Razão Social'].str.contains(filter_text, case=False)]

st.dataframe(search_final,use_container_width=True,hide_index=True)
import base64

df=search_final

import io
import xlsxwriter

buffer = io.BytesIO()
txt="Consulta realizada na Base da CVM nesta data."
txt1='Desenvolvido por Guilherme Moreira (https://www.linkedin.com/in/guilmoreira/)'

# Create a DataFrame with one row and two columns
data_txt = {'index': [1,2], 
            'Observação': [txt,txt1]}

# Create a dataframe from the dictionary
df_txt = pd.DataFrame(data_txt)
df_txt.set_index('index', inplace=True)

# Create a Pandas Excel writer using XlsxWriter as the engine.
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    # Write each dataframe to a different worksheet.
    df.to_excel(writer, sheet_name='AAI-PJ')
    df_txt.to_excel(writer, sheet_name='OBS')


    # Close the Pandas Excel writer and output the Excel file to the buffer
    writer.close()

    st.download_button(
        label="Download Excel",
        data=buffer,
        file_name=f'escritoriosAAI-CVM_{date.today().year}_{date.today().month}_{date.today().year}.xlsx',
        mime="application/vnd.ms-excel"
    )

st.caption("Todos os dados são extraídos da base de dados da CVM conforme cadastro.")
