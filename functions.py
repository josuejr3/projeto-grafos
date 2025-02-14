import pandas as pd
import json
import os

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

    BASE_DIR = os.path.dirname(os.path.abspath(file))
    SAVE_TO = os.path.join(BASE_DIR, (file_name_save+".json"))

    # Sempre fazer um with open para leitura e outro para escrita?

    with open(file, 'r+', encoding="utf8") as f:
        lines = f.readlines()

        for l in range(len(lines)):
            lines[l] = lines[l].split()

        print(lines)

        with open(SAVE_TO, 'w+', encoding="utf8") as a:
            json.dump(lines, a, indent=4, ensure_ascii=False)



