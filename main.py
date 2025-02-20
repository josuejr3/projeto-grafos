from numpy.testing.print_coercion_tables import print_coercion_table
from pyparsing import withAttribute

import functions
from functions import convert_cnv_to_json, create_a_dataframe, year_of_analysis, YEARS, detected_encoding, get_code
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json

# config para ver todas as colunas
pd.options.display.width = None
pd.options.display.max_columns = None
pd.set_option('display.max_rows', 3000)
pd.set_option('display.max_columns', 3000)


def weight_of_city(city_or_code: str, database: pd.DataFrame) -> int:
    cont = 0
    for l in database.iterrows():
        line = l[1]
        if str(line['ID_MUNICIP']) == city_or_code:
            cont += 1
    return cont


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
        cities_set = set()

        # Adiciona o código das cidades que tiveram casos no ano
        for case in cases_paraiba.iterrows():
            # Set contendo todas as informações do caso
            case_data = case[1]
            city_id = str(case_data['ID_MUNICIP'])

            if city_id not in cities_set:
                cities_set.add(city_id)

        # Cria um dicionario para cada cidade que contem o ano de análise e a quantidade de casos
        dictionary_cities = {}
        for city in cities_set:
            dictionary_cities.update({city: {"year": y, "cases": 0}})

        # Retorna o total de casos de cada cidade
        for case in cases_paraiba.iterrows():
            city_cod = str(case[1]['ID_MUNICIP'])
            if city_cod in dictionary_cities.keys() and year_of_analysis(cases_paraiba):
                dictionary_cities[city_cod]["cases"] += 1

        DIR_CITIES = "src/cities.json"

        # Altera codigos por nomes das cidades
        with open(DIR_CITIES, "r", encoding=detected_encoding(DIR_CITIES)) as f:
            cities = json.load(f)

            # Substitui os codigos pelo nome da cidade
            for k, v in cities.items():
                if v in cities_set:
                    cities_set.add(k)
                    cities_set.remove(v)

        # cria da cidade e cria uma aresta que interliga a cidade ao ano
        for city in cities_set:

            # Adiciona nó da cidade
            #my_graph.add_node(city)
            # Adiciona nó ao grafo "menor"

            # Obtém e converte o código da cidade para string
            codigo_city = get_code(city, "src/cities.json")
            codigo_city = str(codigo_city)

            # Retorna o peso de uma cidade no ano
            peso_cidade= weight_of_city(codigo_city, cases_paraiba)
            # Adiciona aresta cidade-ano com o peso
            my_graph.add_edge(city, str(year_of_analysis(cases_paraiba)), weight=peso_cidade)



    # ----------------------------- DEFININDO PROPRIEDADES DE PLOTAGEM (COR E TAMANHO) ---------------------------------
    color_nodes = []
    size_nodes = []


    for n in my_graph.nodes():
        color_nodes.append('orange') if n in YEARS else color_nodes.append('red')

    for n in my_graph.nodes():
        size_nodes.append(3500) if n in YEARS else size_nodes.append(1500)


    # --------------------------------------Criando data frame menor cidades-pacientes----------------------------------
    #
    #
    # def cria_grafo_menor(file: pd.DataFrame, grafo: nx.DiGraph) -> list:
    #
    #     cidades = set()
    #
    #     for i in file.iterrows():
    #         paciente = i[1]
    #         codigo_paciente = i[0]
    #         cidade = paciente['ID_MUNICIP']
    #         cidades.add(cidade)
    #         grafo.add_node(cidade)
    #         grafo.add_node(codigo_paciente)
    #         grafo.add_edge(cidade, codigo_paciente)
    #
    #     return [cidades, grafo]

    #
    # aaa = create_a_dataframe('PB', 'data/processed/LEIVBR14.csv')
    # u = nx.DiGraph()
    # aaa = cria_grafo_menor(aaa, u)
    #
    #
    # esquerda = aaa[0]
    #
    # fig, bloco = plt.subplots(figsize=(45, 55))  # Define o tamanho total da figura
    # fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove as margens
    # nx.draw_networkx(u, with_labels=True, arrows=True, pos=nx.bipartite_layout(u, esquerda))
    # plt.show()
    #
    # o = nx.eigenvector_centrality(u)
    #
    # maior = -1
    # cidade = ""
    #
    # for m, n in o.items():
    #     if len(str(m)) == 6 and n > maior:
    #         maior = n
    #         cidade = m
    #
    # print(maior, cidade)
    #
    # print(nx.bipartite.color(u))


    # ----------------------------------------------------PLOTAGEM------------------------------------------------------
    esquerda = YEARS
    posicao = nx.bipartite_layout(my_graph, esquerda, scale=5, aspect_ratio=0.5)

    fig, bloco = plt.subplots(figsize=(45, 55))  # Define o tamanho total da figura
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove as margens

    nx.draw_networkx(my_graph, with_labels=True, arrows=True, node_color=color_nodes, node_size=size_nodes, pos=posicao, ax=bloco)# pos=nx.spring_layout(my_graph, seed=150))
    plt.title('Casos de Leishmaniose na Paraíba nos anos 2014-2024')
    plt.show()

