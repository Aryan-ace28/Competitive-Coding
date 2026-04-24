import streamlit as st
import subprocess, json, os, math
import plotly.graph_objects as go
import networkx as nx
import numpy as np

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="APSP Analyzer",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Syne:wght@400;700;800&display=swap');

:root {
    --bg: #0a0e1a;
    --surface: #111827;
    --surface2: #1a2235;
    --border: #1e2d4a;
    --accent: #00d4ff;
    --accent2: #ff6b6b;
    --accent3: #7cfc00;
    --accent4: #ffa500;
    --text: #e2e8f0;
    --muted: #6b7fa3;
    --fw-color: #00d4ff;
    --dij-color: #7cfc00;
    --bf-color: #ffa500;
}

.stApp { background: var(--bg); color: var(--text); font-family: 'JetBrains Mono', monospace; }
.block-container { padding: 1.5rem 2rem; max-width: 1600px; }

h1,h2,h3 { font-family: 'Syne', sans-serif; }

.header-banner {
    background: linear-gradient(135deg, #0d1b2e 0%, #0a1628 40%, #0d1b2e 100%);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: 8px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.header-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(0,212,255,0.05) 0%, transparent 70%);
    pointer-events: none;
}
.header-title { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; color: var(--accent); margin: 0; letter-spacing: -0.5px; }
.header-sub { color: var(--muted); font-size: 0.78rem; margin-top: 0.25rem; }

.algo-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}
.algo-card-fw  { border-left: 3px solid var(--fw-color); }
.algo-card-dij { border-left: 3px solid var(--dij-color); }
.algo-card-bf  { border-left: 3px solid var(--bf-color); }

.metric-row { display: flex; gap: 0.75rem; flex-wrap: wrap; margin: 1rem 0; }
.metric-box {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.6rem 1rem;
    flex: 1;
    min-width: 120px;
    text-align: center;
}
.metric-val { font-size: 1.3rem; font-weight: 700; font-family: 'Syne', sans-serif; }
.metric-lbl { font-size: 0.65rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }

.path-display {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.75rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 0.5px;
}
.path-node { display: inline-block; background: var(--surface); border: 1px solid var(--border); border-radius: 4px; padding: 2px 8px; margin: 2px; }

.neg-cycle-banner {
    background: linear-gradient(90deg, rgba(255,107,107,0.15) 0%, rgba(255,107,107,0.05) 100%);
    border: 1px solid rgba(255,107,107,0.4);
    border-left: 4px solid var(--accent2);
    border-radius: 6px;
    padding: 0.75rem 1rem;
    margin: 0.75rem 0;
    font-size: 0.85rem;
    color: var(--accent2);
}

.section-label {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--muted);
    margin-bottom: 0.5rem;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid var(--border);
}

.complexity-table { width: 100%; border-collapse: collapse; font-size: 0.78rem; }
.complexity-table th { background: var(--surface2); padding: 0.5rem 0.75rem; text-align: left; color: var(--muted); font-weight: 600; border-bottom: 1px solid var(--border); }
.complexity-table td { padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--border); }
.complexity-table tr:hover td { background: var(--surface2); }

.stSelectbox > div > div { background: var(--surface) !important; border: 1px solid var(--border) !important; color: var(--text) !important; }
.stSlider > div { color: var(--text); }

div[data-testid="stSidebarContent"] { background: #090d18 !important; border-right: 1px solid var(--border); }

.tab-header { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; margin-bottom: 1rem; }

.na-badge {
    display: inline-block;
    background: rgba(255,107,107,0.15);
    color: var(--accent2);
    border: 1px solid rgba(255,107,107,0.3);
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
}
.ok-badge {
    display: inline-block;
    background: rgba(124,252,0,0.12);
    color: var(--dij-color);
    border: 1px solid rgba(124,252,0,0.25);
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
}

.stTabs [data-baseweb="tab"] { font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────
# FIX: use abspath so the path is always correct regardless of CWD at launch
BACKEND = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))

# FIX: check binary exists before any interaction, give a clear error early
if not os.path.isfile(BACKEND):
    st.error(
        f"Backend binary not found at: `{BACKEND}`\n\n"
        "Compile it first:\n```\ng++ -O2 backend.cpp -o backend\n```"
    )
    st.stop()

GRAPH_META = {
    0: {"name": "Dense City Map",    "nodes": 6,  "type": "dense",    "neg_weights": False, "neg_cycle": False},
    1: {"name": "Sparse Road Net",   "nodes": 8,  "type": "sparse",   "neg_weights": False, "neg_cycle": False},
    2: {"name": "Negative Weights",  "nodes": 5,  "type": "directed", "neg_weights": True,  "neg_cycle": False},
    3: {"name": "Negative Cycle",    "nodes": 5,  "type": "directed", "neg_weights": True,  "neg_cycle": True},
    4: {"name": "DAG Dependencies",  "nodes": 7,  "type": "dag",      "neg_weights": False, "neg_cycle": False},
    5: {"name": "Complete K5",       "nodes": 5,  "type": "dense",    "neg_weights": False, "neg_cycle": False},
}

ALGO_COMPLEXITY = {
    "Floyd-Warshall": {
        "time":  "O(V³)",
        "space": "O(V²)",
        "neg_weights": "✓ Yes",
        "neg_cycle": "✓ Detects",
        "best_for": "Dense graphs",
        "color": "#00d4ff",
    },
    "Repeated Dijkstra": {
        "time":  "O(V·(E + V log V))",
        "space": "O(V² + E)",
        "neg_weights": "✗ No",
        "neg_cycle": "✗ N/A",
        "best_for": "Sparse, non-negative",
        "color": "#7cfc00",
    },
    "Repeated Bellman-Ford": {
        "time":  "O(V·E·V) = O(V²E)",
        "space": "O(V² + E)",
        "neg_weights": "✓ Yes",
        "neg_cycle": "✓ Detects",
        "best_for": "Neg. weights graphs",
        "color": "#ffa500",
    },
}

# ─── Helpers ──────────────────────────────────────────────────────────────────
@st.cache_data
def run_backend(graph_id: int, src: int, dst: int) -> dict:
    # FIX: added timeout=10 to prevent UI hanging if binary stalls;
    # catch TimeoutExpired and surface a clear error instead of blocking forever.
    try:
        result = subprocess.run(
            [BACKEND, str(graph_id), str(src), str(dst)],
            capture_output=True, text=True, timeout=10
        )
    except subprocess.TimeoutExpired:
        st.error("Backend timed out after 10 seconds. Check the binary.")
        return {}
    if result.returncode != 0:
        st.error(f"Backend error: {result.stderr}")
        return {}
    return json.loads(result.stdout)

def fmt_time(ns: int) -> str:
    if ns < 1000: return f"{ns} ns"
    if ns < 1_000_000: return f"{ns/1000:.2f} µs"
    return f"{ns/1_000_000:.3f} ms"

def fmt_bytes(b: int) -> str:
    if b < 1024: return f"{b} B"
    if b < 1048576: return f"{b/1024:.2f} KB"
    return f"{b/1048576:.2f} MB"

def get_node_positions(n: int, edges: list) -> dict:
    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    for e in edges:
        G.add_edge(e["u"], e["v"], weight=e["w"])
    try:
        if nx.is_directed_acyclic_graph(G):
            pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
        else:
            pos = nx.spring_layout(G, seed=42, k=1.8)
    except:
        pos = nx.spring_layout(G, seed=42, k=1.8)
    return pos

# ─── Graph Visualizer ─────────────────────────────────────────────────────────
def build_graph_figure(data: dict, highlight_path: list, highlight_algo: str,
                        neg_cycle_nodes: list, show_weights: bool = True):
    n = data["n"]
    edges = data["edges"]
    pos = get_node_positions(n, edges)

    # Normalize positions
    xs = [v[0] for v in pos.values()]
    ys = [v[1] for v in pos.values()]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    span_x = x_max - x_min or 1
    span_y = y_max - y_min or 1
    pos = {k: ((v[0]-x_min)/span_x, (v[1]-y_min)/span_y) for k, v in pos.items()}

    path_edges = set()
    if highlight_path and len(highlight_path) > 1:
        for i in range(len(highlight_path)-1):
            path_edges.add((highlight_path[i], highlight_path[i+1]))

    algo_color_map = {"Floyd-Warshall": "#00d4ff", "Repeated Dijkstra": "#7cfc00", "Repeated Bellman-Ford": "#ffa500"}
    path_color = algo_color_map.get(highlight_algo, "#00d4ff")

    traces = []

    # FIX: removed duplicate Scatter edge traces — edges are drawn solely via
    # Plotly annotations (arrowheads) below, avoiding double-rendering overhead.

    # Weight labels only (no duplicate edge lines)
    if show_weights:
        for e in edges:
            u, v, w = e["u"], e["v"], e["w"]
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            mx, my = (x0+x1)/2 + 0.02, (y0+y1)/2 + 0.02
            traces.append(go.Scatter(
                x=[mx], y=[my],
                mode="text",
                text=[f"{w}"],
                textfont=dict(
                    size=10,
                    color="#ff6b6b" if w < 0 else "#6b7fa3",
                    family="JetBrains Mono"
                ),
                hoverinfo="skip",
                showlegend=False
            ))

    # Draw nodes
    node_x = [pos[i][0] for i in range(n)]
    node_y = [pos[i][1] for i in range(n)]

    node_colors = []
    node_borders = []
    for i in range(n):
        if highlight_path and i in highlight_path:
            if i == highlight_path[0]:
                node_colors.append("#00d4ff")
                node_borders.append("#00d4ff")
            elif i == highlight_path[-1]:
                node_colors.append("#ff6b6b")
                node_borders.append("#ff6b6b")
            else:
                node_colors.append(path_color)
                node_borders.append(path_color)
        elif i in neg_cycle_nodes:
            node_colors.append("rgba(255,107,107,0.3)")
            node_borders.append("#ff6b6b")
        else:
            node_colors.append("#111827")
            node_borders.append("#1e2d4a")

    traces.append(go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        marker=dict(
            size=36, color=node_colors,
            line=dict(color=node_borders, width=2),
            symbol="circle"
        ),
        text=[str(i) for i in range(n)],
        textposition="middle center",
        textfont=dict(size=13, color="#e2e8f0", family="Syne"),
        hovertemplate=[f"Node {i}<br>Position: ({pos[i][0]:.2f}, {pos[i][1]:.2f})<extra></extra>" for i in range(n)],
        showlegend=False
    ))

    # Arrows via annotations
    annotations = []
    for e in edges:
        u, v = e["u"], e["v"]
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        is_path = (u, v) in path_edges
        neg_edge = e["w"] < 0
        color = path_color if is_path else ("#ff6b6b" if neg_edge else "#1e2d4a")
        annotations.append(dict(
            ax=x0, ay=y0, x=x1, y=y1,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True,
            arrowhead=3, arrowsize=1.2, arrowwidth=2 if is_path else 1.2,
            arrowcolor=color,
        ))

    fig = go.Figure(data=traces)
    fig.update_layout(
        annotations=annotations,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.1,1.1]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.1,1.1]),
        margin=dict(l=20, r=20, t=20, b=20),
        height=360,
        hovermode="closest",
    )
    return fig

# ─── Distance Matrix Heatmap ──────────────────────────────────────────────────
def build_matrix_heatmap(dist_matrix, n, title, color):
    z = []
    text = []
    for row in dist_matrix:
        z_row, t_row = [], []
        for val in row:
            if val is None:
                z_row.append(float('nan'))
                t_row.append("∞")
            else:
                z_row.append(val)
                t_row.append(str(val))
        z.append(z_row)
        text.append(t_row)

    fig = go.Figure(go.Heatmap(
        z=z,
        text=text,
        texttemplate="%{text}",
        colorscale=[[0, "#0a1628"], [0.5, color.replace(")", ",0.5)").replace("rgb", "rgba") if color.startswith("rgb") else color + "80"], [1, color]],
        showscale=False,
        hoverongaps=False,
        xgap=3, ygap=3,
        textfont=dict(size=11, family="JetBrains Mono", color="#e2e8f0"),
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(family="Syne", size=13, color="#e2e8f0"), x=0.5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickvals=list(range(n)), ticktext=[str(i) for i in range(n)],
                   tickfont=dict(size=10, color="#6b7fa3"), title="Destination"),
        yaxis=dict(tickvals=list(range(n)), ticktext=[str(i) for i in range(n)],
                   tickfont=dict(size=10, color="#6b7fa3"), title="Source",
                   autorange="reversed"),
        margin=dict(l=40, r=10, t=40, b=40),
        height=280,
    )
    return fig

# ─── Performance Bar Chart ────────────────────────────────────────────────────
def build_perf_chart(data):
    algos, times, spaces, colors = [], [], [], []
    mapping = [
        ("Floyd-Warshall", "fw", "#00d4ff"),
        ("Dijkstra", "dijkstra", "#7cfc00"),
        ("Bellman-Ford", "bellman_ford", "#ffa500"),
    ]
    for name, key, color in mapping:
        d = data[key]
        applicable = d.get("applicable", True)
        if applicable or key != "dijkstra":
            algos.append(name)
            times.append(d["time_ns"] / 1000)  # convert ns → µs for display
            spaces.append(d["space_bytes"] / 1024)
            colors.append(color)
        else:
            algos.append(name + " (N/A)")
            times.append(0)
            spaces.append(0)
            colors.append("#333")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Time (µs)", x=algos, y=times,
        marker_color=colors,
        marker_line=dict(color="rgba(255,255,255,0.1)", width=1),
        text=[f"{t:.3f} µs" for t in times],
        textposition="outside",
        textfont=dict(size=10, family="JetBrains Mono", color="#e2e8f0"),
        yaxis="y"
    ))
    fig.add_trace(go.Bar(
        name="Space (KB)", x=algos, y=spaces,
        marker_color=[c + "80" for c in colors],
        marker_line=dict(color="rgba(255,255,255,0.1)", width=1),
        text=[f"{s:.2f} KB" for s in spaces],
        textposition="outside",
        textfont=dict(size=10, family="JetBrains Mono", color="#e2e8f0"),
        yaxis="y2"
    ))
    fig.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="JetBrains Mono", color="#e2e8f0"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
        xaxis=dict(tickfont=dict(size=10), gridcolor="#1e2d4a"),
        yaxis=dict(title="Time (µs)", gridcolor="#1e2d4a", titlefont=dict(size=10)),
        yaxis2=dict(title="Space (KB)", overlaying="y", side="right",
                    gridcolor="rgba(0,0,0,0)", titlefont=dict(size=10)),
        margin=dict(l=40, r=60, t=20, b=60),
        height=300,
    )
    return fig

# ─── Path comparison bar chart ────────────────────────────────────────────────
def build_path_dist_chart(data):
    src, dst = data["src"], data["dst"]
    rows = []
    for name, key, color in [("Floyd-Warshall","fw","#00d4ff"), ("Dijkstra","dijkstra","#7cfc00"), ("Bellman-Ford","bellman_ford","#ffa500")]:
        d = data[key]
        if d.get("applicable", True) and d["dist"] is not None:
            dist_val = d["dist"][src][dst]
            rows.append((name, dist_val if dist_val is not None else None, color))

    fig = go.Figure()
    for name, val, color in rows:
        label = str(val) if val is not None else "∞"
        fig.add_trace(go.Bar(
            x=[name], y=[val if val is not None else 0],
            name=name,
            marker_color=color,
            text=[label], textposition="outside",
            textfont=dict(size=12, family="JetBrains Mono")
        ))

    fig.update_layout(
        title=dict(text=f"Shortest distance: node {src} → node {dst}",
                   font=dict(family="Syne", size=12, color="#e2e8f0"), x=0.5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#1e2d4a"),
        yaxis=dict(title="Distance", gridcolor="#1e2d4a"),
        showlegend=False,
        margin=dict(l=40, r=20, t=40, b=20),
        height=220,
        font=dict(family="JetBrains Mono", color="#e2e8f0"),
    )
    return fig

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#00d4ff;margin-bottom:1.2rem;letter-spacing:-0.5px;">⬡ APSP ANALYZER</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Graph Selection</div>', unsafe_allow_html=True)
    graph_options = {
        0: "0 · Dense City Map (6 nodes)",
        1: "1 · Sparse Road Net (8 nodes)",
        2: "2 · Negative Weights (5 nodes)",
        3: "3 · Negative Cycle (5 nodes)",
        4: "4 · DAG Dependencies (7 nodes)",
        5: "5 · Complete K5 (5 nodes)",
    }
    selected_graph = st.selectbox("Prebuilt Graph", options=list(graph_options.keys()),
                                   format_func=lambda x: graph_options[x], index=0)
    meta = GRAPH_META[selected_graph]

    badge_html = ""
    if meta["neg_weights"]: badge_html += '<span style="background:rgba(255,107,107,0.15);color:#ff6b6b;border:1px solid rgba(255,107,107,0.3);border-radius:3px;padding:1px 6px;font-size:0.65rem;margin-right:4px;">NEG WEIGHTS</span>'
    if meta["neg_cycle"]:   badge_html += '<span style="background:rgba(255,50,50,0.2);color:#ff4444;border:1px solid rgba(255,50,50,0.4);border-radius:3px;padding:1px 6px;font-size:0.65rem;margin-right:4px;">NEG CYCLE</span>'
    if badge_html: st.markdown(badge_html, unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Path Query</div>', unsafe_allow_html=True)
    n_nodes = meta["nodes"]
    col_src, col_dst = st.columns(2)
    with col_src:
        src_node = st.number_input("Source", min_value=0, max_value=n_nodes-1, value=0, step=1)
    with col_dst:
        dst_node = st.number_input("Target", min_value=0, max_value=n_nodes-1, value=n_nodes-1, step=1)

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Display Options</div>', unsafe_allow_html=True)
    show_weights   = st.toggle("Show edge weights", value=True)
    highlight_algo = st.radio("Highlight path for", ["Floyd-Warshall", "Repeated Dijkstra", "Repeated Bellman-Ford"], index=0)

    st.markdown('<br>', unsafe_allow_html=True)
    run_btn = st.button("▶  RUN ANALYSIS", use_container_width=True, type="primary")

# ─── Main ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
  <div class="header-title">All-Pairs Shortest Path Analyzer</div>
  <div class="header-sub">Floyd-Warshall · Repeated Dijkstra · Repeated Bellman-Ford — C++ backend with live visualization</div>
</div>
""", unsafe_allow_html=True)

algo_key_map = {
    "Floyd-Warshall": "fw",
    "Repeated Dijkstra": "dijkstra",
    "Repeated Bellman-Ford": "bellman_ford",
}
highlight_key = algo_key_map.get(highlight_algo, "fw")

data = run_backend(selected_graph, int(src_node), int(dst_node))

if not data:
    st.error("Failed to load data from C++ backend.")
    st.stop()

def get_path(key):
    return data[key]["path"] if data[key].get("path") else []

path_map = {
    "Floyd-Warshall": get_path("fw"),
    "Repeated Dijkstra": get_path("dijkstra"),
    "Repeated Bellman-Ford": get_path("bellman_ford"),
}
active_path = path_map[highlight_algo]
neg_cycle_nodes = data["fw"].get("neg_cycle_nodes", [])

# ─── Layout: Graph + Metrics ──────────────────────────────────────────────────
col_graph, col_info = st.columns([3, 2])

with col_graph:
    st.markdown('<div class="section-label">Graph Visualization</div>', unsafe_allow_html=True)
    fig_graph = build_graph_figure(data, active_path, highlight_algo, neg_cycle_nodes, show_weights)
    st.plotly_chart(fig_graph, use_container_width=True, config={"displayModeBar": False})

    if neg_cycle_nodes:
        st.markdown(f'<div class="neg-cycle-banner">⚠ Negative cycle detected — nodes involved: {", ".join(str(x) for x in neg_cycle_nodes)}. Shortest paths through these nodes are undefined (→ −∞). Path reconstruction is disabled for graphs with negative cycles.</div>', unsafe_allow_html=True)

with col_info:
    st.markdown('<div class="section-label">Algorithm Results</div>', unsafe_allow_html=True)

    # Floyd-Warshall
    fw = data["fw"]
    fw_dist = fw["dist"][src_node][dst_node]
    fw_dist_str = "−∞ (neg cycle)" if fw["has_neg_cycle"] and fw_dist is not None and fw_dist < -1e15 else ("∞" if fw_dist is None else str(fw_dist))
    st.markdown(f"""
    <div class="algo-card algo-card-fw">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
        <span style="color:#00d4ff;font-weight:700;font-size:0.9rem;font-family:Syne,sans-serif;">Floyd-Warshall</span>
        <span class="ok-badge">O(V³)</span>
      </div>
      <div class="metric-row">
        <div class="metric-box"><div class="metric-val" style="color:#00d4ff;">{fw_dist_str}</div><div class="metric-lbl">Distance {src_node}→{dst_node}</div></div>
        <div class="metric-box"><div class="metric-val" style="color:#00d4ff;">{fmt_time(fw["time_ns"])}</div><div class="metric-lbl">Compute Time</div></div>
        <div class="metric-box"><div class="metric-val" style="color:#00d4ff;">{fmt_bytes(fw["space_bytes"])}</div><div class="metric-lbl">Space Used</div></div>
      </div>
      <div style="font-size:0.72rem;color:#6b7fa3;">Path: {'→'.join(str(x) for x in fw['path']) if fw['path'] else ('N/A (neg cycle)' if fw['has_neg_cycle'] else 'No path')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Dijkstra
    dij = data["dijkstra"]
    if dij["applicable"]:
        dij_dist = dij["dist"][src_node][dst_node] if dij["dist"] else None
        dij_dist_str = "∞" if dij_dist is None else str(dij_dist)
        st.markdown(f"""
        <div class="algo-card algo-card-dij">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
            <span style="color:#7cfc00;font-weight:700;font-size:0.9rem;font-family:Syne,sans-serif;">Repeated Dijkstra</span>
            <span class="ok-badge" style="color:#7cfc00;border-color:rgba(124,252,0,0.3);background:rgba(124,252,0,0.1);">O(V·E log V)</span>
          </div>
          <div class="metric-row">
            <div class="metric-box"><div class="metric-val" style="color:#7cfc00;">{dij_dist_str}</div><div class="metric-lbl">Distance {src_node}→{dst_node}</div></div>
            <div class="metric-box"><div class="metric-val" style="color:#7cfc00;">{fmt_time(dij["time_ns"])}</div><div class="metric-lbl">Compute Time</div></div>
            <div class="metric-box"><div class="metric-val" style="color:#7cfc00;">{fmt_bytes(dij["space_bytes"])}</div><div class="metric-lbl">Space Used</div></div>
          </div>
          <div style="font-size:0.72rem;color:#6b7fa3;">Path: {'→'.join(str(x) for x in dij['path']) if dij['path'] else 'No path'}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="algo-card algo-card-dij" style="opacity:0.6;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
            <span style="color:#7cfc00;font-weight:700;font-size:0.9rem;font-family:Syne,sans-serif;">Repeated Dijkstra</span>
            <span class="na-badge">N/A — Neg. Weights</span>
          </div>
          <div style="font-size:0.78rem;color:#6b7fa3;padding:0.4rem 0;">Dijkstra requires non-negative edge weights. This graph has negative edges — algorithm not applicable.</div>
        </div>
        """, unsafe_allow_html=True)

    # Bellman-Ford
    bf = data["bellman_ford"]
    bf_dist = bf["dist"][src_node][dst_node]
    bf_dist_str = "∞" if bf_dist is None else str(bf_dist)
    st.markdown(f"""
    <div class="algo-card algo-card-bf">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
        <span style="color:#ffa500;font-weight:700;font-size:0.9rem;font-family:Syne,sans-serif;">Repeated Bellman-Ford</span>
        <span class="ok-badge" style="color:#ffa500;border-color:rgba(255,165,0,0.3);background:rgba(255,165,0,0.1);">O(V²·E)</span>
      </div>
      <div class="metric-row">
        <div class="metric-box"><div class="metric-val" style="color:#ffa500;">{bf_dist_str}</div><div class="metric-lbl">Distance {src_node}→{dst_node}</div></div>
        <div class="metric-box"><div class="metric-val" style="color:#ffa500;">{fmt_time(bf["time_ns"])}</div><div class="metric-lbl">Compute Time</div></div>
        <div class="metric-box"><div class="metric-val" style="color:#ffa500;">{fmt_bytes(bf["space_bytes"])}</div><div class="metric-lbl">Space Used</div></div>
      </div>
      <div style="font-size:0.72rem;color:#6b7fa3;">Path: {'→'.join(str(x) for x in bf['path']) if bf['path'] else ('N/A (neg cycle)' if bf['has_neg_cycle'] else 'No path')}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Distance Matrices", "⚡ Performance", "🔁 Path Reconstruction", "📐 Complexity Guide"])

with tab1:
    st.markdown('<div class="section-label" style="margin-top:0.5rem">Full Distance Matrices (all-pairs)</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        fig_fw = build_matrix_heatmap(fw["dist"], data["n"], "Floyd-Warshall", "#00d4ff")
        st.plotly_chart(fig_fw, use_container_width=True, config={"displayModeBar": False})
    with c2:
        if dij["applicable"] and dij["dist"]:
            fig_dij = build_matrix_heatmap(dij["dist"], data["n"], "Repeated Dijkstra", "#7cfc00")
            st.plotly_chart(fig_dij, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<div style="background:#111827;border:1px solid #1e2d4a;border-radius:6px;padding:2rem;text-align:center;color:#6b7fa3;height:280px;display:flex;align-items:center;justify-content:center;flex-direction:column;"><span style="font-size:1.5rem;margin-bottom:0.5rem;">✗</span><br>Dijkstra not applicable<br><span style="font-size:0.7rem;">Negative weights present</span></div>', unsafe_allow_html=True)
    with c3:
        fig_bf = build_matrix_heatmap(bf["dist"], data["n"], "Repeated Bellman-Ford", "#ffa500")
        st.plotly_chart(fig_bf, use_container_width=True, config={"displayModeBar": False})

    st.markdown(f"""
    <div style="font-size:0.72rem;color:#6b7fa3;text-align:center;margin-top:0.5rem;">
        Null cells = ∞ (no path). Color intensity ∝ distance magnitude.
        Negative diagonal values indicate <span style="color:#ff6b6b;">negative cycles</span>.
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-label" style="margin-top:0.5rem">Execution Time & Space Overhead</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 2])
    with c1:
        fig_perf = build_perf_chart(data)
        st.plotly_chart(fig_perf, use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.markdown('<div style="margin-top:1rem"></div>', unsafe_allow_html=True)
        for name, key, color in [("Floyd-Warshall","fw","#00d4ff"), ("Dijkstra","dijkstra","#7cfc00"), ("Bellman-Ford","bellman_ford","#ffa500")]:
            d = data[key]
            applicable = d.get("applicable", True)
            if applicable or key != "dijkstra":
                st.markdown(f"""
                <div style="background:#111827;border:1px solid #1e2d4a;border-left:3px solid {color};border-radius:6px;padding:0.6rem 0.9rem;margin-bottom:0.5rem;">
                  <div style="color:{color};font-size:0.8rem;font-weight:700;font-family:Syne,sans-serif;">{name}</div>
                  <div style="display:flex;gap:1rem;margin-top:0.3rem;">
                    <div><span style="color:#6b7fa3;font-size:0.65rem;">TIME</span><br><span style="font-size:0.85rem;">{fmt_time(d["time_ns"])}</span></div>
                    <div><span style="color:#6b7fa3;font-size:0.65rem;">SPACE</span><br><span style="font-size:0.85rem;">{fmt_bytes(d["space_bytes"])}</span></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#111827;border:1px solid #1e2d4a;border-radius:6px;padding:0.6rem 0.9rem;margin-top:0.5rem;">
          <div style="color:#6b7fa3;font-size:0.65rem;">GRAPH STATS</div>
          <div style="font-size:0.75rem;margin-top:0.3rem;">V = {data['n']} nodes &nbsp;|&nbsp; E = {len(data['edges'])} edges</div>
          <div style="font-size:0.72rem;color:#6b7fa3;margin-top:0.2rem;">Density: {len(data['edges'])/(data['n']*(data['n']-1)) if data['n']>1 else 0:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    fig_dist = build_path_dist_chart(data)
    st.plotly_chart(fig_dist, use_container_width=True, config={"displayModeBar": False})

with tab3:
    st.markdown('<div class="section-label" style="margin-top:0.5rem">Path Reconstruction — Node {src} → Node {dst}</div>'.format(src=src_node, dst=dst_node), unsafe_allow_html=True)

    for algo_name, key, color in [("Floyd-Warshall","fw","#00d4ff"), ("Repeated Dijkstra","dijkstra","#7cfc00"), ("Repeated Bellman-Ford","bellman_ford","#ffa500")]:
        d = data[key]
        applicable = d.get("applicable", True)
        has_neg_cycle = d.get("has_neg_cycle", False)
        path = d.get("path", [])

        with st.expander(f"{algo_name}", expanded=True):
            if not applicable:
                st.markdown(f'<div class="na-badge">NOT APPLICABLE — negative edges detected</div>', unsafe_allow_html=True)
            elif has_neg_cycle:
                # FIX: explicitly surface that path reconstruction is disabled for neg-cycle graphs
                st.markdown(f'<div class="neg-cycle-banner">⚠ Negative cycle detected — path reconstruction disabled. Distances through cycle nodes are −∞ and paths are undefined.</div>', unsafe_allow_html=True)
            elif not path:
                st.markdown(f'<span style="color:#6b7fa3;font-size:0.85rem;">No path exists from {src_node} to {dst_node}</span>', unsafe_allow_html=True)
            else:
                path_html = ""
                for i, node in enumerate(path):
                    if i > 0:
                        w = "?"
                        for e in data["edges"]:
                            if e["u"] == path[i-1] and e["v"] == node:
                                w = str(e["w"]); break
                        path_html += f'<span style="color:{color};margin:0 6px;">──{w}──▶</span>'
                    bg = color + "30"
                    border = color
                    path_html += f'<span style="background:{bg};border:1px solid {border};border-radius:5px;padding:4px 12px;font-weight:700;color:{color};">Node {node}</span>'

                dist_val = d["dist"][src_node][dst_node] if d.get("dist") else None
                dist_str = "∞" if dist_val is None else str(dist_val)

                st.markdown(f"""
                <div class="path-display" style="margin-bottom:0.75rem;">
                  {path_html}
                </div>
                <div style="font-size:0.75rem;color:#6b7fa3;">
                  Path length: <span style="color:{color};font-weight:700;">{len(path) - 1} edges</span> &nbsp;|&nbsp;
                  Total cost: <span style="color:{color};font-weight:700;">{dist_str}</span> &nbsp;|&nbsp;
                  Nodes visited: {', '.join(str(x) for x in path)}
                </div>
                """, unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-label" style="margin-top:0.5rem">Theoretical Complexity & Algorithm Comparison</div>', unsafe_allow_html=True)

    st.markdown("""
    <table class="complexity-table">
      <thead>
        <tr>
          <th>Algorithm</th><th>Time (APSP)</th><th>Space</th><th>Neg. Weights</th><th>Neg. Cycle Det.</th><th>Best For</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="color:#00d4ff;font-weight:700;">Floyd-Warshall</td>
          <td><code>O(V³)</code></td>
          <td><code>O(V²)</code></td>
          <td style="color:#7cfc00;">✓ Yes</td>
          <td style="color:#7cfc00;">✓ Yes (diag &lt; 0)</td>
          <td>Dense graphs, all-pairs</td>
        </tr>
        <tr>
          <td style="color:#7cfc00;font-weight:700;">Rep. Dijkstra</td>
          <td><code>O(V·(E + V log V))</code></td>
          <td><code>O(V² + E)</code></td>
          <td style="color:#ff6b6b;">✗ No</td>
          <td style="color:#ff6b6b;">✗ N/A</td>
          <td>Sparse, non-neg graphs</td>
        </tr>
        <tr>
          <td style="color:#ffa500;font-weight:700;">Rep. Bellman-Ford</td>
          <td><code>O(V²·E)</code></td>
          <td><code>O(V² + E)</code></td>
          <td style="color:#7cfc00;">✓ Yes</td>
          <td style="color:#7cfc00;">✓ Yes (V-th relax)</td>
          <td>Neg. weights, small graphs</td>
        </tr>
        <tr>
          <td style="color:#a78bfa;font-weight:700;">Johnson's (ref)</td>
          <td><code>O(V·E + V² log V)</code></td>
          <td><code>O(V² + E)</code></td>
          <td style="color:#7cfc00;">✓ (reweighted)</td>
          <td style="color:#7cfc00;">✓ (BF step)</td>
          <td>Sparse + neg. weights</td>
        </tr>
      </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="algo-card" style="border-left-color:#00d4ff;">
          <div style="color:#00d4ff;font-weight:700;font-family:Syne,sans-serif;margin-bottom:0.5rem;">Floyd-Warshall — Dynamic Programming</div>
          <div style="font-size:0.78rem;color:#9ab;line-height:1.6;">
            Uses DP over intermediate vertices. <code>dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])</code> for each k.<br><br>
            Detects negative cycles by checking <code>dist[i][i] &lt; 0</code> after completion. Matrix multiplication formulation
            over the (min,+) tropical semiring.<br><br>
            Optimal for <strong>dense graphs</strong> where E ≈ V² since it's cache-friendly and simple to implement.
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="algo-card" style="border-left-color:#7cfc00;margin-top:0.5rem;">
          <div style="color:#7cfc00;font-weight:700;font-family:Syne,sans-serif;margin-bottom:0.5rem;">Repeated Dijkstra — Greedy + Priority Queue</div>
          <div style="font-size:0.78rem;color:#9ab;line-height:1.6;">
            Runs a single-source Dijkstra from each vertex. Uses a min-heap for greedy shortest-path expansion.<br><br>
            <strong>Cannot handle negative edges</strong> — the greedy assumption breaks. Combine with
            Bellman-Ford (Johnson's algorithm) for sparse graphs with negative weights.<br><br>
            Best when graph is sparse (E ≪ V²) and all weights are non-negative.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="algo-card" style="border-left-color:#ffa500;">
          <div style="color:#ffa500;font-weight:700;font-family:Syne,sans-serif;margin-bottom:0.5rem;">Repeated Bellman-Ford — Relaxation</div>
          <div style="font-size:0.78rem;color:#9ab;line-height:1.6;">
            Relaxes all edges V−1 times per source node. If a (V)-th relaxation still improves a path,
            a negative cycle is reachable from that source.<br><br>
            Handles negative weights correctly. Slowest of the three for dense graphs but most general.<br><br>
            Complexity: <code>O(V · V · E) = O(V²E)</code> total for all-pairs.
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="algo-card" style="border-left-color:#a78bfa;margin-top:0.5rem;">
          <div style="color:#a78bfa;font-weight:700;font-family:Syne,sans-serif;margin-bottom:0.5rem;">When to Choose Which?</div>
          <div style="font-size:0.78rem;color:#9ab;line-height:1.6;">
            <strong style="color:#00d4ff;">Dense + any weights</strong> → Floyd-Warshall<br>
            <strong style="color:#7cfc00;">Sparse + non-negative</strong> → Repeated Dijkstra<br>
            <strong style="color:#ffa500;">Sparse + negative weights</strong> → Johnson's (BF + Dijkstra)<br>
            <strong style="color:#ffa500;">Small + negative cycle check</strong> → Repeated Bellman-Ford<br>
            <br>
            FW is the most commonly used in practice due to its simplicity and excellent cache performance.
          </div>
        </div>
        """, unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:2rem;padding-top:1rem;border-top:1px solid #1e2d4a;
            text-align:center;font-size:0.65rem;color:#6b7fa3;letter-spacing:1px;">
  APSP ANALYZER · C++ Backend (g++ -O2) · Streamlit + Plotly Frontend · 6 Prebuilt Graphs
</div>
""", unsafe_allow_html=True)
