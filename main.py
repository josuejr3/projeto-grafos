from matplotlib.pyplot import title
from networkx.algorithms.centrality import eigenvector_centrality
from networkx.drawing import bipartite_layout

from functions import (convert_cnv_to_json, create_a_dataframe, year_of_analysis, YEARS, detected_encoding,
                       get_code, ranking, absance_of_cases_in_year, plot_graph, plot_subgraph, weight_of_city)
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json

if __name__ == '__main__':

    # Pré processamento - ok
    convert_uf = convert_cnv_to_json("data/processed/UFccodig.cnv", "states")
    convert_cities = convert_cnv_to_json("data/processed/Municpb.cnv", "cities")

    # Se os arquivos JSON foram criados corretamente, crie o data frame
    if not convert_uf and convert_cities:
        raise print('Não foi possível criar os arquivos base')

    input_state = 'PB'

    sertao = nx.Graph()
    agreste = nx.Graph()
    mata = nx.Graph()
    borborema = nx.Graph()

    sertao.add_nodes_from(YEARS)
    agreste.add_nodes_from(YEARS)
    mata.add_nodes_from(YEARS)
    borborema.add_nodes_from(YEARS)

    for y in YEARS:

        ultimos_digitos = y[2::]
        cases_paraiba = create_a_dataframe(input_state, f'data/processed/LEIVBR{ultimos_digitos}.csv')
        cities_set = set()

        dictionary_cities = {}

        # Adiciona o código das cidades que tiveram casos no ano
        for case in cases_paraiba.iterrows():
            # Set contendo todas as informações do caso
            case_data = case[1]
            city_id = str(case_data['ID_MUNICIP'])

            if city_id not in cities_set:
                cities_set.add(city_id)
                dictionary_cities.update({city_id: {"year": y, "cases": 0}})

        # Conta quantidade de casos
        for c in dictionary_cities.keys():
            cases_in_city = cases_paraiba['ID_MUNICIP'].value_counts().get(int(c), 0)

        DIR_CITIES = "src/cities.json"

        # Altera codigos por nomes das cidades
        with open(DIR_CITIES, "r", encoding=detected_encoding(DIR_CITIES)) as f:
            cities = json.load(f)

            # Substitui os codigos pelo nome da cidade
            for k, v in cities.items():
                if v in cities_set:
                    cities_set.add(k)
                    cities_set.remove(v)

        # cria da cidade e cria uma aresta que interliga a cidade ao ano[
        with open('src/mesoregioes.json', 'r', encoding=detected_encoding(DIR_CITIES)) as f:

            regioes = json.load(f)
            for city in cities_set:

                code_of_city = get_code(city, DIR_CITIES)
                weight_c = weight_of_city(code_of_city, cases_paraiba)

                if city in regioes['SERTAO']:
                    sertao.add_node(city)
                    sertao.add_edge(city, year_of_analysis(cases_paraiba), weight=weight_c)
                elif city in regioes['AGRESTE']:
                    agreste.add_node(city)
                    agreste.add_edge(city, year_of_analysis(cases_paraiba), weight=weight_c)
                elif city in regioes['MATA']:
                    mata.add_node(city)
                    mata.add_edge(city, year_of_analysis(cases_paraiba), weight=weight_c)
                elif city in regioes['BORBOREMA']:
                    borborema.add_node(city)
                    borborema.add_edge(city, year_of_analysis(cases_paraiba), weight=weight_c)

    graph_pb = nx.Graph()
    graph_pb.add_nodes_from(YEARS)
    graph_pb.add_nodes_from(borborema.nodes)
    graph_pb.add_nodes_from(sertao.nodes)
    graph_pb.add_nodes_from(agreste.nodes)
    graph_pb.add_nodes_from(mata.nodes)
    graph_pb.add_edges_from(borborema.edges)
    graph_pb.add_edges_from(agreste.edges)
    graph_pb.add_edges_from(sertao.edges)
    graph_pb.add_edges_from(mata.edges)

    # Configuração de tamanho de vértice e cor - grafo geral
    eigenvector_centrality_graph_geral = nx.eigenvector_centrality(graph_pb)
    eigenvector_centrality_graph_geral_list = list(eigenvector_centrality_graph_geral.items())
    eigenvector_centrality_graph_geral_list.sort(key=lambda x: x[1], reverse=True)


    degree_centrality_graph_borborema = nx.degree_centrality(borborema)
    degree_centrality_graph_sertao = nx.degree_centrality(sertao)
    degree_centrality_graph_agreste = nx.degree_centrality(agreste)
    degree_centrality_graph_mata = nx.degree_centrality(mata)

    color_nodes_geral = list()
    size_nodes_geral = list()

    size_nodes_borborema = list()
    size_nodes_sertao = list()
    size_nodes_agreste = list()
    size_nodes_mata = list()
    color_nodes_borborema = list()
    color_nodes_sertao = list()
    color_nodes_agreste = list()
    color_nodes_mata = list()

    for n in graph_pb.nodes:
        if n in YEARS:
            color_nodes_geral.append("#FF0000")
            color_nodes_borborema.append("#FF0000")
            color_nodes_sertao.append("#FF0000")
            color_nodes_agreste.append("#FF0000")
            color_nodes_mata.append("#FF0000")
            size_nodes_geral.append(1000 + (15000 * eigenvector_centrality_graph_geral[n]))
        elif n in sertao.nodes:
            color_nodes_geral.append("#FFD700")
            color_nodes_sertao.append("#FFD700")
            size_nodes_geral.append(1000 +  (10000 * eigenvector_centrality_graph_geral[n]))
        elif n in agreste.nodes:
            color_nodes_geral.append("#BAD94D")
            color_nodes_agreste.append("#BAD94D")
            size_nodes_geral.append(1000 + (10000 * eigenvector_centrality_graph_geral[n]))
        elif n in borborema.nodes:
            color_nodes_geral.append("#EDA621")
            color_nodes_borborema.append("#EDA621")
            size_nodes_geral.append(1000 + (10000 * eigenvector_centrality_graph_geral[n]))
        elif n in mata.nodes:
            color_nodes_geral.append("#08CF2C")
            color_nodes_mata.append("#08CF2C")
            size_nodes_geral.append(1000 + (10000 * eigenvector_centrality_graph_geral[n]))

    # Plotagem Grafo Geral
    left = YEARS
    fig, bloco = plt.subplots(figsize=(60, 60))  # Define o tamanho total da figura
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove as margens
    nx.draw_networkx(graph_pb, pos=nx.spring_layout(graph_pb), node_size=size_nodes_geral,
                     node_color=color_nodes_geral, font_weight='bold')
    plt.show()

    # Ranking com top 5 cidades e 5 anos mais importantes através de centralidade de autovetor
    rank_cities = ranking(eigenvector_centrality_graph_geral_list, False)
    rank_years = ranking(eigenvector_centrality_graph_geral_list)

    print(f'Top 5 Cidades com mais Casos ao longo dos Anos')
    for c in rank_cities:
        print(c)
    print()
    print(f'Top 5 Anos com mais Casos ao longo dos Anos')
    for a in rank_years:
        print(a)
    print()


    # Centralidade de proximidade para identificar anos que não ocorreram a doença
    c_p_g_pb = nx.closeness_centrality(graph_pb)
    if not absance_of_cases_in_year(c_p_g_pb):
        print('Houve casos em todos os anos')
    else:
        print('No ano: ', absance_of_cases_in_year(c_p_g_pb), "não houve casos")


    a1 = nx.degree_centrality(agreste)
    b1 = nx.degree_centrality(borborema)
    m1 = nx.degree_centrality(mata)
    s1 = nx.degree_centrality(sertao)

    a1_size = list()
    b1_size = list()
    m1_size = list()
    s1_size = list()

    a1_color = list()
    b1_color = list()
    m1_color = list()
    s1_color = list()

    # Plotagem subregioes
    config_graph_agreste = plot_subgraph(agreste, a1, "#FF0000", "#BAD94D")
    a1_size = config_graph_agreste[1]
    a1_color = config_graph_agreste[0]
    plot_graph(agreste, a1_color, a1_size, 'Agreste')

    config_graph_borborema = plot_subgraph(borborema, b1, "#FF0000", "#EDA621")
    b1_size = config_graph_borborema[1]
    b1_color = config_graph_borborema[0]
    plot_graph(borborema, b1_color, b1_size, 'Borborema')

