from json import JSONDecodeError

import pandas as pd
import json
import os
import chardet

# Constante com as variáveis representadas em cada coluna
ANALYSIS_VARIABLES = ['DT_NOTIFIC', 'NU_ANO', 'ID_MUNICIP', 'SG_UF_NOT',
                      'ANO_NASC', 'CS_SEXO', 'CS_GESTANT', 'CLASSI_FIN',
                      'EVOLUCAO', 'DT_OBITO']

YEARS = ['2014', '2015', '2016', '2017', '2018', '2019', '2020',
        '2021', '2022', '2023', '2024']


# Função para identificação de tipo de codificação do arquivo
def detected_encoding(arquivo):
    with open(arquivo, "rb") as f:
        resultado = chardet.detect(f.read(10000))  # Lê os primeiros 10KB para análise
    return resultado["encoding"]



#Obtém uma lista com código - nome
def local_names(list_names: list) -> list:
    """
    Função auxiliar para formatação do nome de cidades e estados que retorna o nome formatado e o codigo
    :param list_names: Lista com os dados da cidade/estado
    :return: Lista que retorna código e nome
    """
    if list_names and len(list_names) != 3:
        code_city = list_names.pop()
        name_city = " ".join(list_names[2::])
        return [code_city, name_city]
    return [list_names[2], list_names[1]]


# Verifica se todas as colunas necessárias estão no dataset
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


def get_code(value: str, file: str) -> None | str:
    """
    Função que retorna um código de um município ou estado
    :param value: estado ou município escolhido
    :param file: arquivo JSON com dicionário
    :return: None se não existir um código ou um inteiro representando o código
    """

    value = value.upper()

    try:
        with open(file, 'r', encoding="utf8") as f:

            dictionary_codes = json.load(f)
            if value in dictionary_codes.keys():
                return int(dictionary_codes[value])
        return None
    except FileNotFoundError:
        print('Arquivo não encontrado.')
    except JSONDecodeError:
        print('Erro de leitura no arquivo JSON.')


# Função que cria e retorna o dataframe formatado com as colunas necessárias
def create_a_dataframe(state: str, file_path: str) -> pd.DataFrame:

    """
    Função responsável por criar o dataframe com as colunas necessárias e o estado brasileiro já definido.
    :param state: string referente ao estado desejado
    :param file_path: string com caminho do data frame sem formatação
    :return: dataframe com as colunas necessárias para a análise e do estado correspondente
    """

    # Obtém o código do estado em formato de inteiro
    state = get_code(state, "src/states.json")

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



def year_of_analysis(data: pd.DataFrame) -> int:
    """
    Uma função para identificar qual o ano o arquivo está se referindo
    :param data: caminho do arquivo csv ou o próprio nome do arquivo com extensão
    :return: o ano de análise que consta no arquivo
    """

    year = int(data['NU_ANO'].values[0])
    return year


def convert_cnv_to_json(file: str, file_name_save: str) -> True:
    """
    Converte um arquivo do tipo cnv para arquivo json
    :param file: caminho do arquivo cnv
    :param file_name_save: nome do arquivo final json
    """

    # caminho absoluto da pasta src
    BASE_DIR = os.path.abspath("src")
    # caminho onde o arquivo sera salvo
    SAVE_TO = os.path.join(BASE_DIR, (file_name_save+".json"))

    # dicionario que com cidade/estado que será transformado em json
    save_local = dict()

    try:
        with open(file, 'r+', encoding=detected_encoding(file)) as f:

            lines = f.readlines()
            for l in range(len(lines)):
                lines[l] = lines[l].split()

                # obtem as informações do local, codigo - nome
                info_local = local_names(lines[l])
                save_local[info_local[1].upper()] = info_local[0]

            # Remove informações de cabeçalho
            lines.pop(0)
            lines.pop(0)

            # Cria e escreve no arquivo json o dicionario com todas os estados/municipios
            with open(SAVE_TO, 'w+', encoding="utf8") as a:
                json.dump(save_local, a, indent=4, ensure_ascii=False)
            return True

    except FileNotFoundError:
        raise print('Arquivos ou pastas base para cidades e munícipios não foram encontrados.')
    except JSONDecodeError:
        raise print('Erro de leitura no arquivo JSON dos arquivos de cidades e estados.')

