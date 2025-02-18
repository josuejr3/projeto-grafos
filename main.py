import functions
from functions import convert_cnv_to_json, create_a_dataframe, year_of_analysis

if __name__ == '__main__':

    # Pré processamento
    convert_uf = convert_cnv_to_json("data/processed/UFccodig.cnv", "states")
    convert_cities = convert_cnv_to_json("data/processed/Municpb.cnv", "cities")

    # Se os arquivos JSON foram criados corretamente, crie o data frame
    if not convert_uf and convert_cities:
        raise print('Não foi possível criar os arquivos base')

    # Parte de grafos
