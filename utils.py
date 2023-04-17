#!/bin/env python

import random
import numpy as np

import pyalex
from pyalex import Works, Authors, Sources, Institutions, Concepts
pyalex.config.email = 'yanhengxu98@gmail.com'
min_average_ref = 10 # 定义年均最少引用数

def toAbstract(inverted_indices):
    words, indices = [], []
    for key in inverted_indices.keys():
        words += [key] * len(inverted_indices[key])
        indices += inverted_indices[key]
    words, indices = np.array(words), np.array(indices)
    return ' '.join(words[np.argsort(indices)].tolist())

def format_info(openalex_work):
    # 常用信息： 标题，出版时间，作者，期刊，引用数
    try:
        alex_id = openalex_work['id']
        print('Successfully extracted alex_id {}.'.format(alex_id))
        doi = openalex_work['doi']
        print('Successfully extracted doi.')
        title = openalex_work['title']
        print('Successfully extracted title.')
        pub_date = openalex_work['publication_date']
        print('Successfully extracted pub_date.')
        try:
            journal = openalex_work['primary_location']['source']['display_name']
            print('Successfully extracted journal.')
        except:
            journal = 'N/A'
            print('Journal info not available.')
        authors = [author['author']['display_name'] for author in openalex_work['authorships']]
        print('Successfully extracted authors.')
        citation_num = openalex_work['cited_by_count']
        print('Successfully extracted citation_num.')
        child = openalex_work['referenced_works']
        print('Successfully extracted child.')
        try:
            abstract = toAbstract(openalex_work['abstract_inverted_index'])
            print('Successfully extracted abstract.')
        except:
            abstract = 'Not available.'
            print('Abstract not available.')

    except Exception as e:
        print(alex_id, 'returns -1')
        return -1
    return {'id': alex_id, 'doi': doi, "title": title, 'authors': authors, 'abstract': abstract,
            'journal': journal, 'pub_date': pub_date, 'citation_num': citation_num, 'children': child}

def justify_child(nodes: dict):
    # 检索引用
    selected_nodes = []
    selected_works = []
    edge = []
    if 'referenced_works' in nodes.keys():
        results = []
        if len(nodes['referenced_works']) > 25:  # 最大检索上限25
            splits_ref = np.array_split(nodes['referenced_works'], len(nodes['referenced_works']) // 25 + 1)
            for ref in splits_ref:
                results += Works().filter(openalex_id="|".join(ref)).get()
        for alex_record in results:
            if alex_record['cited_by_count'] <= min_average_ref * (2023 - alex_record['publication_year']):
                if alex_record['publication_year'] <= 2021:
                    continue
            selected_nodes.append(format_info(alex_record))
            selected_works.append(alex_record)
            edge.append(nodes['id'] + '>' + alex_record['id'])

    return selected_nodes, selected_works, edge

def format_node_edge(nodes, edges):
    ids = [node["id"] for node in nodes]
    unique_ids = list(set([node["id"] for node in nodes]))
    new_nodes = [nodes[ids.index(unique_id)] for unique_id in unique_ids]

    for i, node in enumerate(new_nodes):
        if node["citation_num"] > 3600:
            node["highlight_type"] = 3
        elif 2500< node["citation_num"] <= 3600:
            node["highlight_type"] = 2
        else:
            node["highlight_type"] = 1
        node["index"] = i

    new_edges = []
    for edge in edges:
        temp_dict = dict()
        temp_dict["type"] = random.choice(["solid"])
        temp_dict["color"] = random.choice(["b"])
        temp_dict["from"] = unique_ids.index(edge.split(">")[0])
        temp_dict["to"] = unique_ids.index(edge.split(">")[1])
        temp_dict["from_id"] = edge.split(">")[0]
        temp_dict["to_id"] = edge.split(">")[1]
        new_edges.append(temp_dict)

    return new_nodes, new_edges

def format_node_edge_clicked(nodes, click_nodes, edges, click_edges):
    new_nodes = nodes+click_nodes
    ids = [node["id"] for node in new_nodes]
    unique_ids = list(set([node["id"] for node in new_nodes]))
    new_nodes = [new_nodes[ids.index(unique_id)] for unique_id in unique_ids]

    edges = [edge['from_id'] + '>' + edge['to_id'] for edge in edges]
    click_edges = [edge['from_id'] + '>' + edge['to_id'] for edge in click_edges]
    new_edges = edges + click_edges

    return format_node_edge(new_nodes, new_edges)

def doi_query(queried_doi):
    root = Works()['https://doi.org/' + queried_doi]
    print('doi information retrieved from openalex for', queried_doi)

    global_nodes = [format_info(root)]
    global_works = [root]
    global_edges = []

    ## 单次检索
    result = justify_child(root)
    global_nodes += result[0]
    global_works += result[1]
    global_edges += result[2]
    print('child information retrieved from openalex')

    formatted_nodes, formatted_edges = format_node_edge(global_nodes, global_edges)

    return formatted_nodes, formatted_edges