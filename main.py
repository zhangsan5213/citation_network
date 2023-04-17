#!/bin/env python
import json
import random
import numpy as np
from utils import *
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/root_doi_query', methods=['POST'])
def root_doi_query():
    message = request.get_json()
    print('The DOI for root is ' + message['root_doi'])
    nodes, edges = doi_query(message['root_doi'])
    response = {
        'nodes': nodes,
        'edges': edges
    }
    return jsonify(response)

@app.route('/node_clicked', methods=['POST'])
def node_clicked():
    message = request.get_json()
    nodes, edges = message['history_nodes'], message['history_edges']
    click_nodes, click_edges = doi_query('/'.join(message['clicked_doi'].split('/')[3:]))
    formatted_nodes, formatted_edges = format_node_edge_clicked(nodes, click_nodes, edges, click_edges)
    response = {
        'nodes': formatted_nodes,
        'edges': formatted_edges
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host="10.21.129.233", port="5555")