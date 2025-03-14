from utils import (convert_cnv_to_json, create_a_dataframe, year_of_analysis, YEARS, detected_encoding,
                   get_code, ranking, absance_of_cases_in_year, plot_graph, config_plot_subgraph, weight_of_city,
                   show_ranking, cardinality, MESORREGIOES, DIR_CITIES, SERTAO, MATA, BORBOREMA, AGRESTE,
                   MUNICIPIO_ID, COR_AGRESTE, COR_BORBOREMA, COR_MATA, COR_SERTAO, COR_ANO,
                   plot_geral_graph, ESTADO, DIR_UFCODIG, DIR_MUNICIP, DIR_DATA_PROCESSED, CONSTANTE_MULT,
                   CONSTANTE_SOMA, bar_chart, pie_chart)
import networkx as nx
import json

if __name__ == '__main__':

    # Pré processamento - convertendo arquivos cnv para JSON
    convert_uf = convert_cnv_to_json(DIR_UFCODIG, "states")
    convert_cities = convert_cnv_to_json(DIR_MUNICIP, "cities")

    # Se os arquivos JSON foram criados corretamente, crie o data frame
    if not convert_uf and convert_cities:
        raise print('Não foi possível criar os arquivos base')

    # Criando subgrafos das subregiões e adicionando a faixa de anos em cada um
    sertao = nx.Graph()
    agreste = nx.Graph()
    mata = nx.Graph()
    borborema = nx.Graph()

    for regiao in [sertao, agreste, mata, borborema]:
        regiao.add_nodes_from(YEARS)

    for year in YEARS:

        last_digits_of_year = year[2::]
        cases_paraiba = create_a_dataframe(ESTADO, f'{DIR_DATA_PROCESSED}{last_digits_of_year}.csv')
        cities_set = set()
        dictionary_cities_with_codes = {}

        # Adiciona ao dicionario de cidades com codigos as cidades com casos notificados
        for case in cases_paraiba.iterrows():
            # Set contendo todas as informações do caso
            infos_case = case[1]
            # problema com o ano de 2023
            city_id = str(int(infos_case[MUNICIPIO_ID]))

            if city_id not in cities_set:
                cities_set.add(city_id)
                dictionary_cities_with_codes.update({city_id: {"year": year, "cases": 0}})

        # Conta quantidade de casos em cada uma das cidades
        for city_with_code_dict in dictionary_cities_with_codes.keys():
            cases_in_city = cases_paraiba[MUNICIPIO_ID].value_counts().get(int(city_with_code_dict), 0)

        # Altera codigos por nomes no set de cidades
        with open(DIR_CITIES, "r", encoding=detected_encoding(DIR_CITIES)) as f:
            cities = json.load(f)

            # Substitui os codigos pelo nome da cidade
            for k, v in cities.items():
                if v in cities_set:
                    cities_set.add(k)
                    cities_set.remove(v)

        # Abre o arquivo de mesorregiões interliga o vértice da cidade com o ano de análise e adiciona ao subgrafo da
        # região específica
        with open(MESORREGIOES, 'r', encoding=detected_encoding(MESORREGIOES)) as f:

            regioes = json.load(f)
            for city in cities_set:

                # Obtém o código da cidade e a quantidade de casos notificados nela ao longo do ano
                code_of_city = get_code(city, DIR_CITIES)
                weight_of_edge_city = weight_of_city(code_of_city, cases_paraiba)

                if city in regioes[SERTAO]:
                    sertao.add_node(city)
                    sertao.add_edge(city, year_of_analysis(cases_paraiba), weight=weight_of_edge_city)
                elif city in regioes[AGRESTE]:
                    agreste.add_node(city)
                    agreste.add_edge(city, year_of_analysis(cases_paraiba), weight=weight_of_edge_city)
                elif city in regioes[MATA]:
                    mata.add_node(city)
                    mata.add_edge(city, year_of_analysis(cases_paraiba), weight=weight_of_edge_city)
                elif city in regioes[BORBOREMA]:
                    borborema.add_node(city)
                    borborema.add_edge(city, year_of_analysis(cases_paraiba), weight=weight_of_edge_city)

    # Cria o grafo do estado da Paraíba a partir dos subgrafos das regiões
    graph_pb = nx.Graph()
    graph_pb.add_nodes_from(YEARS)

    for gr in [agreste, borborema, mata, sertao]:
        graph_pb.add_nodes_from(gr.nodes())
        graph_pb.add_edges_from(gr.edges())

    # Obtendo de tamanho dos vértices do grafo da Paraíba a partir da centralidade de autovetor
    eigenvector_centrality_graph_geral = nx.eigenvector_centrality(graph_pb)
    eigenvector_centrality_graph_geral_list = list(eigenvector_centrality_graph_geral.items())
    eigenvector_centrality_graph_geral_list.sort(key=lambda x: x[1], reverse=True)

    # Obtendo o tamanho dos vértices dos grafos das regiões a partir da centralidade de grau
    degree_centrality_agreste = nx.degree_centrality(agreste)
    degree_centrality_borborema = nx.degree_centrality(borborema)
    degree_centrality_mata = nx.degree_centrality(mata)
    degree_centrality_sertao = nx.degree_centrality(sertao)

    # Cores e tamanhos do grafo e subgrafos
    graphs_attributes = {
        "paraiba": {"size": [], "color": []},
        "agreste": {"size": [], "color": []},
        "borborema": {"size": [], "color": []},
        "mata": {"size": [], "color": []},
        "sertao": {"size": [], "color": []},
    }

    region_map = {
        "sertao": (sertao, COR_SERTAO),
        "agreste": (agreste, COR_AGRESTE),
        "borborema": (borborema, COR_BORBOREMA),
        "mata": (mata, COR_MATA),
    }

    print(graph_pb)

    for node in graph_pb.nodes:
        if node in YEARS:
            color = COR_ANO
            size = CONSTANTE_SOMA + (CONSTANTE_MULT * eigenvector_centrality_graph_geral[node])
            for region in graphs_attributes.keys():
                graphs_attributes[region]["color"].append(color)
            graphs_attributes["paraiba"]["size"].append(size)
        else:
            for region, (graph, color) in region_map.items():
                if node in graph.nodes:
                    size = CONSTANTE_SOMA + (CONSTANTE_MULT * eigenvector_centrality_graph_geral[node])
                    graphs_attributes["paraiba"]["color"].append(color)
                    graphs_attributes["paraiba"]["size"].append(size)
                    graphs_attributes[region]["color"].append(color)
                    break

    # Plotagem Grafo Geral
    plot_geral_graph(graph_pb, graphs_attributes["paraiba"]["size"], graphs_attributes["paraiba"]["color"])

    # Ranking com top 5 cidades e 5 anos mais importantes através de centralidade de autovetor
    rank_cities = ranking(eigenvector_centrality_graph_geral_list, False)
    rank_years = ranking(eigenvector_centrality_graph_geral_list)

    labels_rank_autovetor = []
    values_rank_autovetor = []
    for label, value in rank_years:
        labels_rank_autovetor.append(label)
        values_rank_autovetor.append(round(value, 3))

    bar_chart(values_rank_autovetor, labels_rank_autovetor, COR_ANO, "Ano de Notificação", "Centralidade de Autovetor", "Gráfico de Barras CA")
    show_ranking(rank_cities, rank_years)

    # Centralidade de proximidade para identificar anos que não ocorreram a doença em regiões
    for name, (graph_region, color) in region_map.items():
        closeness_centrality_region = nx.closeness_centrality(graph_region)
        labels_closeness = []
        value_closeness = []

        for years_region in YEARS:
            labels_closeness.append(years_region)
            value_closeness.append(round(closeness_centrality_region[years_region], 2))

        if not absance_of_cases_in_year(closeness_centrality_region):
            print(f'A região {name.title()} apresentou casos em todos os anos')

        else:
            print(f'A região {name.title()} não apresentou casos no(s) ano(s): ', absance_of_cases_in_year(closeness_centrality_region))
            bar_chart(value_closeness, labels_closeness, color, 'Ano de Notificação', 'Centralidade de Proximidade',
                      f"Gráfico de Barras CP - {name}")

    # Tupla com infos dos subgrafos
    subgraphs = [
        (agreste, degree_centrality_agreste, COR_AGRESTE, 'Agreste'),
        (borborema, degree_centrality_borborema, COR_BORBOREMA, 'Borborema'),
        (mata, degree_centrality_mata, COR_MATA, 'Zona da Mata'),
        (sertao, degree_centrality_sertao, COR_SERTAO, 'Sertão'),
    ]

    cardinality_pb = cardinality(graph_pb) - len(YEARS)
    percentage_regions = []

    # Plotagem subgrafo e infos gráfico de setores
    for subgraph_pb, centrality, color, name in subgraphs:
        color_list_subgraph, size_list_subgraph = config_plot_subgraph(subgraph_pb, centrality, COR_ANO, color)
        plot_graph(subgraph_pb, color_list_subgraph, size_list_subgraph, name)

        percentage_region = ((cardinality(subgraph_pb) - len(YEARS)) * 100) / cardinality_pb
        percentage_regions.append(round(percentage_region, 2))

    # Plot grafico de setores
    pie_chart(percentage_regions, ['Agreste', 'Borborema', 'Zona da Mata', 'Sertão'],
              [COR_AGRESTE, COR_BORBOREMA, COR_MATA, COR_SERTAO])


    print(sertao)