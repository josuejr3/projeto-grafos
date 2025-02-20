from numpy.testing.print_coercion_tables import print_coercion_table
from pyparsing import withAttribute

import functions
from functions import convert_cnv_to_json, create_a_dataframe, year_of_analysis, YEARS, detected_encoding
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json

# config para ver todas as colunas
pd.options.display.width = None
pd.options.display.max_columns = None
pd.set_option('display.max_rows', 3000)
pd.set_option('display.max_columns', 3000)

if __name__ == '__main__':

    # Pré processamento
    convert_uf = convert_cnv_to_json("data/processed/UFccodig.cnv", "states")
    convert_cities = convert_cnv_to_json("data/processed/Municpb.cnv", "cities")

    # Se os arquivos JSON foram criados corretamente, crie o data frame
    if not convert_uf and convert_cities:
        raise print('Não foi possível criar os arquivos base')

    entrada = 'PB'

    my_graph = nx.DiGraph()
    my_graph.add_nodes_from(YEARS)


    for y in YEARS:

        ultimos_digitos = y[2::]

        cases_paraiba = create_a_dataframe(entrada, f'data/processed/LEIVBR{ultimos_digitos}.csv')

        cities_list = set()

        for case in cases_paraiba.iterrows():
            # Serie contendo todas as informações do caso
            case_data = case[1]
            city_id = str(case_data['ID_MUNICIP'])
            if city_id not in cities_list:
                cities_list.add(city_id)


        DIR_CITIES = "src/cities.json"

        # Altera codigos por nomes das cidades
        with open(DIR_CITIES, "r", encoding=detected_encoding(DIR_CITIES)) as f:
            cities = json.load(f)

            # Substitui os codigos pelo nome da cidade
            for k, v in cities.items():
                if v in cities_list:
                    cities_list.add(k)
                    cities_list.remove(v)

        # cria da cidade e cria uma aresta que interliga a cidade ao ano
        for city in cities_list:
            my_graph.add_node(city)
            my_graph.add_edge(city, str(year_of_analysis(cases_paraiba)))


    # for node, degre in my_graph.degree():
    #     print(f"O vertice: {node} tem grau {degre}")

    color_nodes = []
    size_nodes = []

    for n in my_graph.nodes():
        color_nodes.append('orange') if n in YEARS else color_nodes.append('red')

    for n in my_graph.nodes():
        size_nodes.append(3500) if n in YEARS else size_nodes.append(1500)


    plt.figure(figsize=(40, 40))
    nx.draw_networkx(my_graph, with_labels=True, arrows=True, node_color=color_nodes, node_size=size_nodes)# pos=nx.spring_layout(my_graph, seed=150))
    plt.title('GRAFO LEISHMANIOSE NA PARAÍBA 2014-2024', size=75)
    plt.show()

