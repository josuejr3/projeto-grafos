from json import JSONDecodeError

import pandas as pd
import json
import os


# Constante com as variáveis representadas em cada coluna
ANALYSIS_VARIABLES = ['DT_NOTIFIC', 'NU_ANO', 'ID_MUNICIP', 'SG_UF',
                      'ANO_NASC', 'CS_SEXO', 'CS_GESTANT', 'CLASSI_FIN',
                      'EVOLUCAO', 'DT_OBITO']


# Verifica se todas as colunas necessárias estão no dataset
def column_check(data_frame: str) -> bool:

    df = pd.read_csv(data_frame)

    for variable in ANALYSIS_VARIABLES:
        if variable not in df.columns:
            return False
    return True


def get_code_state(state_analysis: str) -> int:

    try:
        with open('src/code_state.json', 'r', encoding="utf-8") as f:
            states = json.load(f)
            code_found = None
            for state in states:
                if state[1] == state_analysis:
                    code_found = int(state[-1])
                    return code_found
            return code_found

    except FileNotFoundError:
        print('Arquivo não encontrado, verifique a pasta rsc')
    except JSONDecodeError:
        print('Erro ao abrir arquivo JSON')

a = get_code_state('PB')
print(type(a))



# Função que cria e retorna o dataframe formatado com as colunas necessárias
def create_a_dataframe(state: str, file_path: str) -> pd.DataFrame:


    if not column_check(file_path):
        raise 'NAO TEM A COLUNA'

    # pandas já informa se um das constantes não for encontrada como coluna
    unformatted_data = pd.read_csv(file_path, sep=',', usecols=ANALYSIS_VARIABLES)

    # cria um novo objeto por copia profunda
    formatted_data = unformatted_data.copy(deep=True)

    return formatted_data


r = create_a_dataframe('PB', 'data/processed/LEIVBR14.csv')
print(column_check('data/processed/LEIVBR14.csv'))
print(r)


def year_of_analysis(data: str) -> int:
    """
    Uma função para identificar qual o ano o arquivo está se referindo
    :param data: caminho do arquivo csv ou o próprio nome do arquivo com extensão
    :return: o ano de análise que consta no arquivo
    """

    df = pd.read_csv(data, encoding="utf8", sep=",")

    if 'NU_ANO' in df.columns:
        return int(df['NU_ANO'].values[0])
    raise "Não há uma coluna de ano indicado"


def convert_cnv_to_json(file: str, file_name_save: str) -> None:
    """
    Converte um arquivo do tipo cnv para arquivo json
    :param file: caminho do arquivo cnv
    :param file_name_save: nome do arquivo final json
    """

    BASE_DIR = os.path.abspath("src")
    SAVE_TO = os.path.join(BASE_DIR, (file_name_save+".json"))

    # Sempre fazer um with open para leitura e outro para escrita?

    with open(file, 'r+', encoding="utf8") as f:
        lines = f.readlines()

        for l in range(len(lines)):
            lines[l] = lines[l].split()

        # Remove informações irrelevantes
        lines.pop(0)
        lines.pop(0)


        with open(SAVE_TO, 'w+', encoding="utf8") as a:
            json.dump(lines, a, indent=4, ensure_ascii=False)

convert_cnv_to_json('data/processed/UFccodig.cnv', 'code_state')