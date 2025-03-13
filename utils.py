from json import JSONDecodeError
import networkx as nx
import pandas as pd
import json
import os
import chardet
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.pyplot import title
from networkx.algorithms.centrality import eigenvector_centrality
from networkx.drawing import bipartite_layout

# Constante com as variáveis representadas em cada coluna
ANALYSIS_VARIABLES = ['DT_NOTIFIC', 'NU_ANO', 'ID_MUNICIP', 'SG_UF_NOT']

YEARS = ['2015', '2016','2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']

# Diretórios necessários
DIR_CITIES = "rsc/cities.json"
MESORREGIOES = 'rsc/mesoregioes.json'
FIG_GRAFO_PARAIBA = "figures/Paraiba.png"
DIR_UFCODIG = "data/processed/UFccodig.cnv"
DIR_MUNICIP = "data/processed/Municpb.cnv"
DIR_DATA_PROCESSED = "data/processed/LEIVBR"

# Regiões e estado
SERTAO = 'SERTAO'
BORBOREMA = 'BORBOREMA'
AGRESTE = 'AGRESTE'
MATA = 'MATA'
ESTADO = 'PB'

# Cores vertices
COR_ANO = "#5F9EA0"
COR_AGRESTE = "#BAD94D"
COR_MATA = "#08CF2C"
COR_BORBOREMA = "#EDA621"
COR_SERTAO = "#FFD700"

CONSTANTE_SOMA = 3000
CONSTANTE_MULT = 50000
MUNICIPIO_ID = 'ID_MUNICIP'

def bar_chart(values: list, labels_bar: list, color: str, x: str, y: str, name: str) -> None:

    if len(labels_bar) != len(values):
        raise "Erro de tamanho entre as listas"
    plt.figure(figsize=[7,7])
    plt.bar(labels_bar, values, color=color)
    plt.xlabel(x, font='Times New Roman', fontsize=14)
    plt.ylabel(y, font='Times New Roman', fontsize=14)
    plt.savefig(f"figures/{name}.png")
    plt.show()


def pie_chart(percentage: list, labels_pie: list, list_colors: list) -> None:

    plt.figure(figsize = (7, 7))
    plt.plot(labels_pie, percentage)
    plt.pie(percentage, labels = labels_pie, autopct='%1.0f%%', colors = list_colors)
    plt.savefig(f"figures/Gráfico de Setores Regiões Notificadas.png")
    plt.show()


def cardinality(grafo: nx.Graph) -> int:
    """
    :param grafo: grafo de análise
    :return: um inteiro correspondendo a cardinalidade/quantidade de vértices do grafo
    """
    return len(grafo.nodes())

def show_ranking(rank_cities: list, rank_years: list) -> None:
    """
    :param rank_cities:
    :param rank_years:
    :return:
    """
    print(f'Top 5 Cidades com mais Casos ao longo dos Anos')
    for c in rank_cities:
        print(c)

    print()
    print(f'Top 5 Anos com mais Casos ao longo dos Anos')
    for a in rank_years:
        print(a)
    print()

    # (Grafico de barras)

# Percorre o dataframe e conta quantas vezes a cidade apareceu
def weight_of_city(city_or_code: str, database: pd.DataFrame) -> int:
    """
    Função que retorna a quantidade de casos (peso da aresta) de um municipio
    :param city_or_code: codigo da cidade
    :param database: dataframe para pesquisa
    :return:
    """
    cont = database[MUNICIPIO_ID].value_counts().get(int(city_or_code), 0)
    return cont


def config_plot_subgraph(grafo_regiao: nx.Graph, dic_size: dict, color1: str, color2: str):
    """
    Configuração de plotagem dos subgrafos - cores e tamanhos
    :param grafo_regiao: grafo da regiao
    :param dic_size: dicionario com as centralidade de grau para definição do tamanho
    :param color1: cor para os vértices de ano
    :param color2: cor para os vértices de cidade
    :return: uma lista com uma duas listas, uma para as cores e outra para os tamanhos
    """
    color_list = list()
    size_list = list()
    for n in grafo_regiao.nodes:
        color_list.append(color1) if n in YEARS else color_list.append(color2)
        size_list.append(500 + (dic_size[n] * 7500))

    return [color_list, size_list]


def plot_geral_graph(grafo: nx.Graph, list_size_nodes: list, list_color_nodes: list) -> None:
    fig, bloco = plt.subplots(figsize=(60, 60))  # Define o tamanho total da figura
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove as margens
    nx.draw_networkx(grafo, pos=nx.spring_layout(grafo, scale=100), node_size=list_size_nodes,
                     node_color=list_color_nodes, font_weight='bold', font_size=20)

    plt.savefig(FIG_GRAFO_PARAIBA, format='png', dpi=150)
    plt.show()


def plot_graph(grafo: nx.Graph, color: list, size: list, regiao: str) -> None:
    """
    Função para plotagem de grafo das regiões
    :param grafo: grafo para plotagem
    :param color: lista de cores
    :param size: lista de tamanhos
    :param regiao: nome da região que será apresentado
    :return: não retorna nada, apenas plota o grafo
    """

    fig, bloco = plt.subplots(figsize=(28, 28))
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    nx.draw_networkx(grafo, with_labels=True, pos=nx.bipartite_layout(grafo, YEARS), node_color=color,
                     font_weight='bold', node_size=size, font_size=20)
    #bloco.set_title(f'Casos de Leishmaniose na Paraíba nos anos 2015-2019 - Região - {regiao}', fontsize=45)
    edge_labels = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_edge_labels(grafo, pos=nx.bipartite_layout(grafo, YEARS), edge_labels=edge_labels, font_size=15,
                                  font_weight='bold', horizontalalignment='right', ax=bloco, bbox={"alpha": 0}, verticalalignment='center')
    plt.savefig(f"figures/{regiao}.png", format='png', dpi=150)
    plt.show()

def ranking(list_cities_and_years: list, years=True) -> list:
    """
    :param list_cities_and_years: lista de tuplas com centralidade
    :param years: True se é uma lista de anos ou False se não é
    :return: retorna uma lista com o rank das cinco cidades ou anos
    """

    classifieds_cities = list()
    classifieds_years = list()

    for member in list_cities_and_years:
        if len(classifieds_cities) < 5 and member[0] not in YEARS:
            classifieds_cities.append(member)
        elif len(classifieds_years) < 5 and member[0] in YEARS:
            classifieds_years.append(member)
        elif len(classifieds_cities) == 5 and len(classifieds_years) == 5:
            break

    if years:
        return classifieds_years
    else:
        return classifieds_cities

def absance_of_cases_in_year(dictionary_with_closeness_centrality: dict):
    """
    Função que utiliza closeness centrality para verificar ausência de casos em uma região
    :param dictionary_with_closeness_centrality: dicionário com closeness centrality de cada subgrafo de região
    :return: retorna o ano em que não houve casos ou False caso tenha ocorrido casos na região
    """

    anos_ausentes_sem_casos_notificados = list()

    for k, v in dictionary_with_closeness_centrality.items():
        if k in YEARS and v == 0.0:
            anos_ausentes_sem_casos_notificados.append(k)

    if anos_ausentes_sem_casos_notificados:
        return anos_ausentes_sem_casos_notificados
    return False

def detected_encoding(arquivo):
    """
    Função responsável por identificar encoding de arquivos
    :param arquivo: arquivo de obtenção do encoding
    :return: o tipo de encoding presente no arquivo
    """
    try:
        with open(arquivo, "rb") as f:
            resultado = chardet.detect(f.read(10000))  # Lê os primeiros 10KB para análise
        return resultado["encoding"]
    except FileNotFoundError:
        raise "Arquivo não encontrado"
    except JSONDecodeError:
        raise "Erro de codificação no arquivo JSON"

def treats_state(lista: list) -> list:
    list_formated = list()
    if len(lista) == 3:
        list_formated.append(lista[1])
        list_formated.append(lista[2])
    if len(lista) > 3:
        lista[-1] = lista[-1].replace(',', ' ')
        lista[-1] = lista[-1].strip()

        info = lista[1] + " " + lista[2]
        code = lista[-1]
        list_formated.append(info)
        list_formated.append(code)

    return list_formated

def treats_city(lista: list) -> list:
    list_formated = list()
    if lista[-1] == lista[1]:
        code = lista.pop()
        name_city = " ".join(lista[2::])
        list_formated.append(name_city)
        list_formated.append(code)
    elif '-' in lista[-1]:
        codigo = lista.pop()
        unknown_city = " ".join(lista[2::])
        list_formated.append(unknown_city)
        list_formated.append(codigo)
    return list_formated

def column_check(data_frame: str) -> bool:
    """
    Função responsável por checar se todas as colunas necessárias para a análise estão no dataframe.
    :param data_frame: o dataframe usado para verificação
    :return: um boolean informando se todas as colunas estão presentes ou não.
    """
    # low_memory = false
    df = pd.read_csv(data_frame, low_memory=False)

    for variable in ANALYSIS_VARIABLES:
        if variable not in df.columns:
            return False
    return True

def get_code(state_city: str, file: str) -> None | str:
    """
    Função que retorna um código de um município ou estado
    :param state_city: estado ou município escolhido
    :param file: arquivo JSON com dicionário
    :return: None se não existir um código ou um inteiro representando o código
    """
    state_city = state_city.upper()
    try:
        with open(file, 'r', encoding="utf8") as f:
            dictionary_codes = json.load(f)
            if state_city in dictionary_codes.keys():
                return dictionary_codes[state_city]
        return None
    except FileNotFoundError:
        print('Arquivo não encontrado.')
    except JSONDecodeError:
        print('Erro de leitura no arquivo JSON.')

def create_a_dataframe(state: str, file_path: str) -> pd.DataFrame:
    """
    Função responsável por criar o dataframe com as colunas necessárias e o estado brasileiro já definido.
    :param state: string referente ao estado desejado
    :param file_path: string com caminho do data frame sem formatação
    :return: dataframe com as colunas necessárias para a análise e do estado correspondente
    """

    # Obtém o código do estado em formato de inteiro
    state = get_code(state, "rsc/states.json")
    state = int(state)

    # Verifica se todas as colunas necessárias estão presentes
    if not column_check(file_path):
        raise "Uma das colunas necessárias não está presente no dataset"

    # pandas já informa se um das constantes não for encontrada como coluna
    unformatted_data = pd.read_csv(file_path, sep=',', usecols=ANALYSIS_VARIABLES, encoding='utf-8')

    # cria um novo objeto por copia profunda
    formatted_data = unformatted_data.copy(deep=True)
    # Seleciona somente as linhas em que a coluna "SG_UF_NOT" são do código referente ao estado escolhido
    formatted_data = formatted_data.loc[formatted_data['SG_UF_NOT'] == state]

    return formatted_data.fillna('X')

def year_of_analysis(data: pd.DataFrame) -> str:
    """
    Uma função para identificar qual o ano o arquivo está se referindo
    :param data: caminho do arquivo csv ou o próprio nome do arquivo com extensão
    :return: o ano de análise que consta no arquivo
    """
    if 'NU_ANO' in data.columns:
        year = int(data['NU_ANO'].values[0])
        return str(year)
    raise 'Ano não encontrado.'

def convert_cnv_to_json(file: str, file_name_save: str, name_code=True) -> True:
    """
    Converte um arquivo do tipo cnv para arquivo json
    :param file: caminho do arquivo cnv
    :param file_name_save: nome do arquivo final json
    :param name_code True se for nome-codigo e False se for codigo-nome
    """

    # Diretorios importantes
    BASE_DIR = os.path.abspath("rsc")
    SAVE_TO = os.path.join(BASE_DIR, (file_name_save+".json"))

    # Dicionario que com cidade/estado que será transformado em json
    save_local = dict()

    try:
        with open(file, 'r+', encoding=detected_encoding(file)) as f:
            with open(file, 'r+', encoding=detected_encoding(file)) as f:
                lines = f.readlines()
                # Lê as linhas e faz o ajuste no nome
                for l in range(len(lines)):
                    lines[l] = lines[l].split()
                    # Verifica o tamanho da linha
                    if len(lines[l]) < 3 or ';' in lines[l]:
                        continue
                    # Ajusta o último elemento (código dos dados desconhecidos)
                    elif ',' in lines[l][-1]:
                        lines[l][-1] = lines[l][-1].replace(',', '-')
                        lines[l][-1] = lines[l][-1].strip('-')
                    # Formata um municipio
                    elif (lines[l][-1] == lines[l][1]) or ('-' in lines[l][-1] and '9999' in lines[l][-1]):
                        lines[l] = treats_city(lines[l])
                    # Formata um estado
                    elif (len(lines[l]) >= 3 and len(lines[l][-1]) == 2) or ('-' in lines[l][-1] and '00' in lines[l][-1]):
                        lines[l] = treats_state(lines[l])
                    # Criação de chaves e valores para cidades ou estados
                    info_local = lines[l][0].upper()                           # Nome
                    code_local = lines[l][1]                                   # Código
                    if name_code:
                        save_local[info_local] = code_local
                    else:
                        save_local[code_local] = info_local
            with open(SAVE_TO, 'w+', encoding="utf8") as a:
                json.dump(save_local, a, indent=4, ensure_ascii=False)
            return True

    except FileNotFoundError:
        raise print('Arquivos ou pastas base para cidades e munícipios não foram encontrados.')
    except JSONDecodeError:
        raise print('Erro de leitura no arquivo JSON dos arquivos de cidades e estados.')
















