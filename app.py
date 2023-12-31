# BIBLIOTECAS
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import requests

# CRIAÇÃO DE CONTAINER E COLUNAS STREAMLIT
container = st.container()
col1,col2 = st.columns(2)

# ESTE CÓDIGO ARMAZENA AS INFORMAÇÕES EM CACHE
@st.cache_resource
def load_data(file):
    """
    Carregará o arquivo para análise sendo ele em CSV ou XLS/XLSX

    parametros:
        file (File): O arquivo a ser carregado.

    Retorna:
        DataFrame: Com os dados carregados.
    """
    file_extension = file.name.split(".")[-1]
    if file_extension == "csv":
        data = pd.read_csv(file)
    elif file_extension in ["xls", "xlsx"]:
        data = pd.read_excel(file)
    else:
        st.warning("Formato do arquivo incompatível. Faça upload de um arquivo Excel ou CSV.")
        return None
    return data


def select_columns(df):
    st.write("### Seleção de Colunas")
    all_columns = df.columns.tolist()
    #options_key = "_".join(all_columns)
    selected_columns = st.multiselect("Selecionar", options=all_columns)
    
    if selected_columns:
        sub_df = df[selected_columns]
        st.write("### DATAFRAME")
        st.write(sub_df.head())
    else:
        st.warning("Por favor selecione pelo menos uma coluna.")

def select_and_rename_column(df):
    st.write("### SELECIONAR E RENOMEAR COLUNAS: ")
    
    # SELECIONANDO AS COLUNAS A SEREM RENOMEADAS
    all_columns = df.columns.tolist()
    selected_columns = st.multiselect("Selecione as colunas para renomear: ", options=all_columns)
    
    # RENOMEANDO AS COLUNAS SELECIONADAS
    for column in selected_columns:
        new_column_name = st.text_input(f"Entre um novo nome para coluna: '{column}'", value=column)
        if column != new_column_name:
            df.rename(columns={column: new_column_name}, inplace=True)
            st.write(f"Coluna '{column}' renomeada como '{new_column_name}' realizado com êxito")
    
    return df    


def show_missing_values_percentage(df):
    st.write("### PERCENTUAL DE VALOR FALTANTE: ")
    
    # CALCULANDO OS VALORES FALTANTES DE CADA COLUNA
    missing_percentage = df.isnull().sum() / len(df) * 100
    
    # CRIANDO UM DATAFRAM PARA ARMAZENAR OS VALORES PERCENTUAIS FALTANTES
    missing_df = pd.DataFrame({'Coluna ': missing_percentage.index, 'Percentual Faltante ': missing_percentage.values})
    
    # EXIBINDO VALORES PERCENTUAIS FALTANTES DO DATAFRAME
    st.write("Valores Percentuais Faltantes -> ",missing_df)


# FUNÇÃO DE AGREGAÇÃO
def agg(df):
    # AAUTORIZANDOO USUÁRIO A SELECIONAR COLUNAS PARA AGREGAÇÃO
    aggregation_columns = st.multiselect("SELECIONE COLUNAS PARA AGREGAÇÃO", options=df.columns)
    
    # AUTORIZANDO O USUÁRIO A SELECIONAR UMA FUNÇÃO DE AGREGAÇÃO
    aggregation_function = st.selectbox("SELECIONE UMA FUNÇÃO DE AGREGAÇÃO:", options=["Sum", "Mean", "Median"])
    
    # AGREGANDO
    if aggregation_columns:
        if aggregation_function == "Sum":
            aggregated_values = sub_df[aggregation_columns].sum()
        elif aggregation_function == "Mean":
            aggregated_values = sub_df[aggregation_columns].mean()
        elif aggregation_function == "Median":
            aggregated_values = sub_df[aggregation_columns].median()
        
        # EXIBINDO VALOR AGREGADOS
        st.write(f"Agregados {aggregation_function} para {aggregation_columns}")
        st.write(aggregated_values)    

#REMOVENDO DUPLICATAS
def remove_duplicates(df):
    st.write("### REMOVER DUPLICATAS")
    
    # SELECINANDO COLUNAS PARA IDÊNTIFICAR DUPLICATAS
    columns = st.multiselect("SELECIONE AS COLUNAS PARA IDÊNTIFICAR AS DUPLICATAS", options=df.columns)
    
    if columns:
        # REMOVENDO DUPLICATAS DA BASE DE DADOS SELECIONADAS
        df.drop_duplicates(subset=columns, inplace=True)
        
        st.write("Duplicatas removidas com sucesso!")
        
    return df
# BUSCAR E ALTERAR O VALOR EM UMA COLUNA
def search_and_replace(df):
    st.write("### PESQUISA E ALTERAÇÃO")
    
    # SELECIONE UMA COLUNA PARA BUSCAR E ALTERAR
    column = st.selectbox("SELECIONE UMA COLUNA:", options=df.columns)
    
    if column:
        # RECEBENDO O VALOR DE BUSCA DO USUÁRIO
        search_string = st.text_input("Insira o texto a ser trocado")
        
        # RECEBENDO O VALOR DE ALTERAÇÃO DO USUÁRIO
        replace_value = st.text_input("Insira o valor de alteração")
        
        # REALIZANDO A OPERAÇÃO DE BUSCA E ALTERAÇÃO
        if search_string in df[column].values:
            df[column] = df[column].replace(search_string, replace_value)
            st.write("Procura e Troca realizada com sucesso!")
            st.write(df[column])

        else:
            st.warning("O texto inserido não está na coluna selecionada.")
        

#ALTERANDO TIPOS DE DADOS PELA COLUNA
import streamlit as st
import pandas as pd

def change_column_data_types(df):
    st.write("### ALTERANDO OS TIPOS DE DADOS PELA COLUNA")
    
    # SELECIONE AS COLUNAS PARA ALTERAÇÃO
    all_columns = df.columns.tolist()
    selected_columns = st.multiselect("Select columns to change data types", options=all_columns)
    
    # RECEBENDO NOVOS TIPOS DE DADOS DO USUÁRIO
    new_data_types = {}
    for column in selected_columns:
        st.write(f"Column: {column}")
        current_data_type = df[column].dtype
        st.write(f"Current Data Type: {current_data_type}")
        new_data_type = st.selectbox("Select new data type", options=['object', 'int', 'float', 'datetime', 'boolean'])
        new_data_types[column] = new_data_type
    
    # CRIANDO UMA CÓPIA DO DATAFRAME
    modified_df = df.copy()
    
    # ALTERANDO OS TIPOS DE DADOS SELECIONADOS
    for column, data_type in new_data_types.items():
        try:
            if data_type == 'object':
                modified_df[column] = modified_df[column].astype(str)
            elif data_type == 'int':
                modified_df[column] = pd.to_numeric(modified_df[column], errors='coerce', downcast='integer')
            elif data_type == 'float':
                modified_df[column] = pd.to_numeric(modified_df[column], errors='coerce', downcast='float')
            elif data_type == 'datetime':
                modified_df[column] = pd.to_datetime(modified_df[column], errors='coerce')
            elif data_type == 'boolean':
                modified_df[column] = modified_df[column].astype(bool)
            
            st.write(f"Coluna '{column}' os tipos de dados foram alterados para '{data_type}' com êxito!")
        except Exception as e:
            st.error(f"Ocorreu um erro ao mudar o tipo de dados da coluna '{column}': {str(e)}")
    
    return modified_df
def groupby_aggregate_data(sub_df):
    st.write("### AGRUPANDO E AGREGANDO DADOS: ")
    st.write(sub_df.head())
    
    # RECEBENDO A LISTA DAS COLUNAS DO DATAFRAME
    columns = sub_df.columns.tolist()

    # RECEBENDO CATEGORIAS DAS COLUNAS PARA AGRUPAR
    group_columns = st.multiselect("SELECIONE A CATEGORIA DAS COLUNAS PARA AGRUPAR", columns)

    # RECEBENDO VALOR NUMERICOS PARA AGREGAÇÃO
    numerical_columns = st.multiselect("SELECIONE A CATEGORIA DAS COLUNAS PARA AGRAGAÇÃO: ", columns)

    # RECEBENDO AGREGAÇÕES DO USUÁRIO
    #aggregation_functions = st.multiselect("Select aggregation functions", ['sum', 'mean', 'median', 'min', 'max'])
    
    # CRIANDO DICIONÁRIO DE AGREGAÇÃO
    #aggregation = {col: func for col in numerical_columns for func in aggregation_functions}

    # AGRUPANDO E AGREGANDO
    if group_columns and numerical_columns:
        grouped_dff = sub_df.groupby(group_columns)[numerical_columns].agg(['sum', 'mean', 'median', 'min', 'max'])
        grouped_df = grouped_dff.reset_index()  # RESETANDO O INDEX PARA EXIBIR OS VALORES
       
        st.write("### DADOS AGRUPADOS E AGREGADOS")
        st.write(grouped_df)
        #fig = px.bar(grouped_df, x=grouped_df.index, y=['sum'], barmode='group')
    else:
        st.warning("POR FAVOR SELECIONE AO MENOS UMA CATEGORIA DE UMA COLUNA, , and one aggregation function.")
  
       
def analyze_data(data):

    container = st.container()
    col1,col2 = st.columns(2)
    
    with container:
         st.write("CABEÇALHO: ",data.head())
    with col1:
         st.write("Columns in you file are ",data.columns)
    st.write("### SELECIONE AS COLUNAS PARA FAZER A ANÁLISE DE DADOS: ")
    
    with col2:
        st.write("TIPO DE DADOS: " ,data.dtypes)

        all_columns = [str(col) for col in data.columns]
        options_key = "_".join(all_columns)
        selected_columns = st.multiselect("SELECIONE AS COLUNAS", options=all_columns)    
    if selected_columns:
        sub_df = data[selected_columns]
        sub_df = select_and_rename_column(sub_df)
        st.write("### DATAFRAME: ")
        st.write(sub_df.head())

        remove_duplicates(sub_df)
        
        change_column_type_df = change_column_data_types(sub_df)
        st.write("OS TIPOS FORA ALTERADOS",change_column_type_df)
        st.write("DESCRIÇÃO")
        st.write(change_column_type_df.describe().T)
        st.write("RANKING")
        st.write(change_column_type_df.rank())

        st.subheader("ORDENAR DADOS: ")
        sort_column = st.selectbox("SELECIONE UMA COLUNA PARA ORDENAR: ", change_column_type_df.columns)
        sorted_df = change_column_type_df.sort_values(by=sort_column)
        st.write(sorted_df)

        #show_missing_values_percentage(sub_df)

        st.write(corr(change_column_type_df))
        
        show_missing_values(change_column_type_df)
        show_percent_missing(change_column_type_df)
        show_unique_values(change_column_type_df)
        show_standard_deviation(change_column_type_df)
        show_data_shape(change_column_type_df)
        show_data_correlation(change_column_type_df)
        filter_rows(change_column_type_df)
    
        groupby_aggregate_data(sub_df)        

        search_and_replace(sub_df)

    else:
        st.warning("POR FAVOR SELECIONE PELO MENOS UMA COLUNA.")

def show_file_header(data):
    st.write("CABEÇALHO: ")
    st.write(data.head())

def sort_data(data):
    # Sort the data by a selected column
    sort_column = st.selectbox("SELECIONE UMA COLUNA PARA ORDENAR OS DADOS: ", data.columns)
    sorted_df = data.sort_values(by=sort_column)
    return sorted_df

def show_sorted_data(sorted_df):
    st.write("ORDENAR DADOS: ")
    st.write(sorted_df)

def show_missing_values(data):
    #col1 = st.beta_column()
    st.write("DADOS FALTANTES: ")
    st.write(data.isnull().sum())

def show_percent_missing(data):
    st.write("PORCENTAGEM FALTANTE: ")
    st.write(data.isna().mean().mul(100))

def show_unique_values(data):
    #col2 = st.beta_column()
    st.write("VALORES ÚNICOS: ")
    st.write(data.nunique())

def show_standard_deviation(data):
    #col1 = st.beta_column()
    st.write("DESVIO PADRÃO: ")
    st.write(data.std(numeric_only=True))

def show_data_shape(data):
    #col1, col2 = st.beta_columns(2)
    st.write("NÚMERO DE LINHAS: ")
    st.write(data.shape[0])
    st.write("NÚMERO DE COLUNAS: ")
    st.write(data.shape[1])

def show_data_correlation(data):
    #col1 = st.beta_column()
    st.write("CORRELAÇÃO DE DADOS: ")
    st.write(data.corr(numeric_only=True))

def corr(data):
    st.write("CORRELAÇÃO DOS DADOS")
    st.write(data.corr(numeric_only=True).style.background_gradient(cmap='RdBu', vmin=-1, vmax=1))  

def filter_rows(data):    
    column_name = st.selectbox("SELECIONE UMA COLUNA PARA FILTRAR: ", data.columns)
    value = st.text_input("INSIRA O FILTRO: ")
    # Filter the rows based on the converted column
    if value == "":
        filtered_data = data[data[column_name].isnull()]
    elif data[column_name].dtype == 'float':
          filtered_data = data[data[column_name] >= float(value)]
    else:      
        filtered_data = data[data[column_name].astype(str).str.contains(value, case=False)]
    st.write("DADOS FILTRADOS")
    st.write(filtered_data)    

def create_chart(chart_type, data, x_column, y_column):
    container.write(" # VISUALIZAÇÃO DE DADOS # ")
    if chart_type == "Bar":
        st.header("GRÁFICO DE BARRAS")
        
        color_column = st.sidebar.selectbox("SELECIONE A COLUNA POR COR: ", data.columns,key="color_name")
        #pattern_column = st.sidebar.selectbox("Select column for pattern ", data.columns)
        if color_column:
           fig = px.bar(data, x=x_column, y=y_column,color=color_column,barmode="group")
           st.plotly_chart(fig)
        else:
           fig = px.bar(data, x=x_column, y=y_column,barmode="group")
           st.plotly_chart(fig)   

    elif chart_type == "Line":
        st.header("GRÁFICA DE LINHA")
        fig = px.line(data, x=x_column, y=y_column)
        st.plotly_chart(fig)

    elif chart_type == "Scatter":
        st.header("GRÁFICO DE DISPERSÃO")
        size_column = st.sidebar.selectbox("SELECIONE A COLUNA POR TAMANHO: ", data.columns)
        color_column = st.sidebar.selectbox("SELECIONE A COLUNA POR COR:  ", data.columns)
        if color_column:
           fig = px.scatter(data, x=x_column, y=y_column,color=color_column,size=size_column)

        else:
            fig = px.scatter(data, x=x_column, y=y_column) 
        st.plotly_chart(fig)        

    elif chart_type == "Histogram":
        st.header("GRÁFICO HISTOGRAMA")
        color_column = st.sidebar.selectbox("SELECIONE A COLUNA POR COR: ", data.columns)
        fig = px.histogram(data, x=x_column, y=y_column,color = color_column)
        st.plotly_chart(fig)
        
    elif chart_type == "Pie":
        st.header("GRÁFICO PIZZA")

        color_column = st.sidebar.selectbox("SELECIONE A COLUNA POR COR: ", data.columns)
        if color_column:
            fig = px.pie(data, names=x_column, values=y_column, color=color_column)
            st.plotly_chart(fig)
        else:
            fig = px.pie(data, names=x_column, values=y_column)
            st.plotly_chart(fig)
    
def main():
    
    # SUBINDO IMAGEM
    image = Image.open("logo-amazon.png")
    container.image(image, width=200)
    container.write(" # Análise de Dados & Visualização # ")
    
    # CAMPO DE UPLOAD DA BASE DE DADOS
    st.sidebar.image(image, width=50)
    file_option = st.sidebar.radio("FONTE DE DADOS", options=["Upload Local File", "Enter Online Dataset"])
    file = None
    data = None
    
    # CONDIÇÕES DE UPLOAD DO ARQUIVO SENDO ELE LOCAL OU ONLINE
    
    #LOCAL
    if file_option == "Upload Local File":
        file = st.sidebar.file_uploader("Faça upload de um arvivo Excel ou CSV: ", type=["csv", "excel"])
        
    #ONLINE    
    elif file_option == "Enter Online Dataset":
        online_dataset = st.sidebar.text_input("Enter the URL of the online dataset")
        if online_dataset:
            try:
                response = requests.get(online_dataset)
                if response.ok:
                    data = pd.read_csv(online_dataset)
                else:
                    st.warning("Unable to fetch the dataset from the provided link.")
            except:
                st.warning("Invalid URL or unable to read the dataset from the provided link.")
                
    # OPÇÕES EM RADIO BUTTON            
    options = st.sidebar.radio('Pages', options=['Data Analysis', 'Data visualization'])
    
    #VERIFICANDO A EXISTÊNCIA DO ARQUIVO E DAS OPÇÕES QUANDO SELECIONADAS
    if file is not None:
        data = load_data(file)

    if options == 'Data Analysis':
        if data is not None:
            analyze_data(data)
        else:
            st.warning("No file or empty file")

    elif options == 'Data visualization':
        if data is not None:
            
            # CRIAÇÃO DE UM SIDEBAR PARA OPÇÕES DO USUÁRIO
            st.sidebar.title("Chart Options")

            st.write("### SELECIONE AS COLUNAS:")
            all_columns = data.columns.tolist()
            options_key = "_".join(all_columns)
            selected_columns = st.sidebar.multiselect("SELECIONE AS COLUNAS", options=all_columns)
            if selected_columns:
                sub_df = data[selected_columns]

                chart_type = st.sidebar.selectbox("SELECIONE O TIPO DE GRÁFICO", ["Bar", "Line", "Scatter", "Histogram", "Pie"])

                x_column = st.sidebar.selectbox("COLUNA X", sub_df.columns)

                y_column = st.sidebar.selectbox("COLUNA Y", sub_df.columns)

                create_chart(chart_type, sub_df, x_column, y_column)

# INICIANDO O APP
if __name__ == "__main__":
    main()