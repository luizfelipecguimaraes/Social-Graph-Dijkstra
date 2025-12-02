import streamlit as st
import networkx as nx
from pyvis.network import Network
import tempfile
import os

st.set_page_config(layout="wide", page_title="Grafo Social - Dijkstra")

def create_graph():
    G = nx.Graph()

    people = [
        {"name": "Luiz", "icon": "https://api.dicebear.com/9.x/avataaars/svg?seed=Nolan"},
        {"name": "Fábio", "icon": "https://api.dicebear.com/9.x/avataaars/svg?seed=Sadie"},
        {"name": "João", "icon": "https://api.dicebear.com/9.x/avataaars/svg?seed=Andrea"},
        {"name": "Giovanni", "icon": "https://api.dicebear.com/9.x/avataaars/svg?seed=Oliver"},
        {"name": "Carlos", "icon": "https://api.dicebear.com/9.x/avataaars/svg?seed=Brian"},
        {"name": "Isa", "icon": "https://api.dicebear.com/9.x/avataaars/svg?seed=Ryan"}
    ]

    for person in people:
        G.add_node(person["name"], shape="image", image=person["icon"], label=person["name"])

    relationships = [
        ("Luiz", "Fábio", 3),
        ("Isa", "João", 8),
        ("Fábio", "Giovanni", 5),
        ("João", "Carlos", 3),
        ("Giovanni", "Luiz", 5),
        ("Carlos", "Luiz", 3),
        ("Isa", "Luiz", 1),
        ("João", "Giovanni", 5)
    ]

    for f, t, w in relationships:
        G.add_edge(f, t, weight=w, title=f"Afinidade: {w}", label=str(w))

    return G


def visualize_graph(G, path_nodes=None):
    net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white") 
    
    net.from_nx(G)

    if path_nodes:
        for edge in net.edges:
            source, target = edge['from'], edge['to']
            
            in_path = False
            for i in range(len(path_nodes) - 1):
                if (path_nodes[i] == source and path_nodes[i+1] == target) or \
                   (path_nodes[i] == target and path_nodes[i+1] == source):
                    in_path = True
                    break
            
            if in_path:
                edge['color'] = "#3badb1"
                edge['width'] = 4
            else:
                edge['color'] = '#555555'
                edge['width'] = 1

    net.toggle_physics(False)
    
 
    path = os.path.join(tempfile.gettempdir(), "grafo_social.html")
    net.save_graph(path)
    return path



G = create_graph()

with st.sidebar:
    st.header("Rede Social com Grafos")
    st.markdown("""
    Projeto para simular uma "rede social" utilizando **Grafos**.
    
    **Problema:** Encontrar o caminho de maior afinidade entre duas pessoas.
    
    **Algoritmo de Dijkstra:** Cálculo do menor caminho possível entre dois pontos. 
    
    **Os Pesos:**
    * As arestas possuem o nível de intimidade entre os nós.
    * **Custo 1:** Alta intimidade.
    * **Custo 10:** Baixa intimidade.
    """)
    st.write("---")
    st.info("Selecione os pontos de partida e chegada abaixo do grafo.")

st.title("🕸️ Rede de Menor Caminho Social")

col_main, col_dummy = st.columns([1, 0.01])

with col_main:
    graph_placeholder = st.empty()
    
    st.write("---")

    c1, c2, c3 = st.columns([1, 1, 2])
    
    all_nodes = list(G.nodes())
    
    with c1:
        start_node = st.selectbox("🚩 Ponto de Partida (Origem)", all_nodes, index=0)
    
    with c2:
        end_node = st.selectbox("🏁 Objetivo (Destino)", all_nodes, index=len(all_nodes)-1)

    path = []
    cost = 0
    
    try:
        path = nx.dijkstra_path(G, source=start_node, target=end_node, weight='weight')
        cost = nx.dijkstra_path_length(G, source=start_node, target=end_node, weight='weight')
        
        with c3:
            st.success(f"**Caminho Encontrado!**")
            st.metric(label="Custo Social", value=cost)
            st.write(f"Trajeto: {' ➔ '.join(path)}")

    except nx.NetworkXNoPath:
        st.error("Não existe caminho conectando essas duas pessoas.")
        path = []

    html_file = visualize_graph(G, path_nodes=path)
    
    with graph_placeholder:
        with open(html_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        st.components.v1.html(source_code, height=500)
