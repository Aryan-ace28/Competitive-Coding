#include <bits/stdc++.h>
using namespace std;

const long long INF = 1e18;

// ─── Graph Definitions ────────────────────────────────────────────────────────
struct Edge { int u, v; long long w; };

struct Graph {
    string name;
    int n;
    vector<Edge> edges;
    vector<tuple<int,int,long long>> adj_list;
};

// ─── Prebuilt Graphs ─────────────────────────────────────────────────────────
vector<Graph> get_graphs() {
    vector<Graph> graphs;

    // Graph 0: Dense city map
    {
        Graph g; g.name = "Dense City Map (6 nodes)"; g.n = 6;
        g.edges = {
            {0,1,4},{0,2,2},{1,2,5},{1,3,10},{2,4,3},
            {3,5,1},{4,3,4},{4,5,8},{0,3,15},{1,4,6},
            {2,3,7},{0,5,20},{3,4,2},{1,5,12},{2,5,9}
        };
        graphs.push_back(g);
    }
    // Graph 1: Sparse road network
    {
        Graph g; g.name = "Sparse Road Network (8 nodes)"; g.n = 8;
        g.edges = {
            {0,1,3},{1,2,4},{2,3,2},{3,4,6},{4,5,1},
            {5,6,5},{6,7,3},{0,4,10},{2,6,7}
        };
        graphs.push_back(g);
    }
    // Graph 2: Negative weights, no negative cycle
    {
        Graph g; g.name = "Negative Weights, No Cycle (5 nodes)"; g.n = 5;
        g.edges = {
            {0,1,6},{0,2,7},{1,2,8},{1,3,-4},{1,4,5},
            {2,4,-3},{3,0,2},{3,2,7},{4,3,9}
        };
        graphs.push_back(g);
    }
    // Graph 3: Negative cycle
    {
        Graph g; g.name = "Negative Cycle Present (5 nodes)"; g.n = 5;
        g.edges = {
            {0,1,1},{1,2,-3},{2,3,2},{3,1,-1},{0,4,5},{4,3,2}
        };
        graphs.push_back(g);
    }
    // Graph 4: DAG
    {
        Graph g; g.name = "DAG - Task Dependencies (7 nodes)"; g.n = 7;
        g.edges = {
            {0,1,2},{0,2,6},{1,3,5},{1,4,3},{2,4,7},{2,5,4},
            {3,6,1},{4,6,2},{5,6,3}
        };
        graphs.push_back(g);
    }
    // Graph 5: Complete K5
    {
        Graph g; g.name = "Complete Graph K5 (5 nodes)"; g.n = 5;
        g.edges = {
            {0,1,10},{0,2,3},{0,3,7},{0,4,5},
            {1,2,6},{1,3,2},{1,4,8},
            {2,3,4},{2,4,9},{3,4,1}
        };
        graphs.push_back(g);
    }

    return graphs;
}

// ─── Floyd-Warshall ───────────────────────────────────────────────────────────
struct FWResult {
    vector<vector<long long>> dist;
    vector<vector<int>> next;
    bool has_neg_cycle;
    long long time_ns;   // FIX: renamed from time_us — stores nanoseconds
    long long space_bytes;
};

FWResult floyd_warshall(const Graph& g) {
    int n = g.n;
    FWResult res;
    res.dist.assign(n, vector<long long>(n, INF));
    res.next.assign(n, vector<int>(n, -1));
    res.has_neg_cycle = false;

    for (int i = 0; i < n; i++) res.dist[i][i] = 0;
    for (auto& e : g.edges) {
        if (e.w < res.dist[e.u][e.v]) {
            res.dist[e.u][e.v] = e.w;
            res.next[e.u][e.v] = e.v;
        }
    }

    auto t0 = chrono::high_resolution_clock::now();

    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (res.dist[i][k] != INF && res.dist[k][j] != INF)
                    if (res.dist[i][k] + res.dist[k][j] < res.dist[i][j]) {
                        res.dist[i][j] = res.dist[i][k] + res.dist[k][j];
                        res.next[i][j] = res.next[i][k];
                    }

    for (int i = 0; i < n; i++)
        if (res.dist[i][i] < 0) { res.has_neg_cycle = true; break; }

    auto t1 = chrono::high_resolution_clock::now();
    res.time_ns = chrono::duration_cast<chrono::nanoseconds>(t1 - t0).count();
    res.space_bytes = (long long)n * n * (sizeof(long long) + sizeof(int));
    return res;
}

vector<int> fw_reconstruct(const FWResult& res, int src, int dst) {
    // FIX: return empty path immediately if negative cycle detected
    if (res.has_neg_cycle) return {};
    if (res.dist[src][dst] == INF) return {};
    vector<int> path = {src};
    int cur = src;
    set<int> visited;
    visited.insert(src);
    while (cur != dst) {
        cur = res.next[cur][dst];
        if (cur == -1 || visited.count(cur)) return {};
        visited.insert(cur);
        path.push_back(cur);
    }
    return path;
}

// ─── Dijkstra (repeated) ─────────────────────────────────────────────────────
struct DijkResult {
    vector<vector<long long>> dist;
    vector<vector<int>> prev;
    long long time_ns;   // FIX: renamed from time_us — stores nanoseconds
    long long space_bytes;
    bool applicable;
};

pair<vector<long long>, vector<int>> dijkstra_single(const Graph& g, int src) {
    int n = g.n;
    vector<vector<pair<int,long long>>> adj(n);
    for (auto& e : g.edges) adj[e.u].push_back({e.v, e.w});

    vector<long long> dist(n, INF);
    vector<int> prev(n, -1);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    dist[src] = 0; pq.push({0, src});

    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                prev[v] = u;
                pq.push({dist[v], v});
            }
        }
    }
    return {dist, prev};
}

DijkResult repeated_dijkstra(const Graph& g) {
    int n = g.n;
    DijkResult res;
    res.dist.assign(n, vector<long long>(n, INF));
    res.prev.assign(n, vector<int>(n, -1));

    bool has_neg = false;
    for (auto& e : g.edges) if (e.w < 0) { has_neg = true; break; }
    res.applicable = !has_neg;

    auto t0 = chrono::high_resolution_clock::now();
    if (res.applicable) {
        for (int s = 0; s < n; s++) {
            auto [d, p] = dijkstra_single(g, s);
            res.dist[s] = d;
            res.prev[s] = p;
        }
    }
    auto t1 = chrono::high_resolution_clock::now();
    res.time_ns = chrono::duration_cast<chrono::nanoseconds>(t1 - t0).count();
    // FIX: removed the incorrect *n multiplier on edge storage —
    // the adjacency list is built once per dijkstra_single call, not duplicated n times globally.
    res.space_bytes = (long long)n * n * (sizeof(long long) + sizeof(int))
                    + (long long)g.edges.size() * sizeof(Edge);
    return res;
}

vector<int> dijk_reconstruct(const DijkResult& res, int src, int dst) {
    if (res.dist[src][dst] == INF) return {};
    vector<int> path;
    int cur = dst;
    while (cur != -1) {
        path.push_back(cur);
        if (cur == src) break;
        cur = res.prev[src][cur];
    }
    reverse(path.begin(), path.end());
    if (path.empty() || path[0] != src) return {};
    return path;
}

// ─── Bellman-Ford (repeated) ──────────────────────────────────────────────────
struct BFResult {
    vector<vector<long long>> dist;
    vector<vector<int>> prev;
    bool has_neg_cycle;
    long long time_ns;   // FIX: renamed from time_us — stores nanoseconds
    long long space_bytes;
};

pair<vector<long long>, vector<int>> bellman_ford_single(const Graph& g, int src, bool& neg_cycle) {
    int n = g.n;
    vector<long long> dist(n, INF);
    vector<int> prev(n, -1);
    dist[src] = 0;
    neg_cycle = false;

    for (int iter = 0; iter < n - 1; iter++) {
        bool updated = false;
        for (auto& e : g.edges) {
            if (dist[e.u] != INF && dist[e.u] + e.w < dist[e.v]) {
                dist[e.v] = dist[e.u] + e.w;
                prev[e.v] = e.u;
                updated = true;
            }
        }
        if (!updated) break;
    }
    // Check for negative cycle
    for (auto& e : g.edges)
        if (dist[e.u] != INF && dist[e.u] + e.w < dist[e.v])
            neg_cycle = true;

    return {dist, prev};
}

BFResult repeated_bellman_ford(const Graph& g) {
    int n = g.n;
    BFResult res;
    res.dist.assign(n, vector<long long>(n, INF));
    res.prev.assign(n, vector<int>(n, -1));
    res.has_neg_cycle = false;

    auto t0 = chrono::high_resolution_clock::now();
    for (int s = 0; s < n; s++) {
        bool nc = false;
        auto [d, p] = bellman_ford_single(g, s, nc);
        res.dist[s] = d;
        res.prev[s] = p;
        if (nc) res.has_neg_cycle = true;
    }
    auto t1 = chrono::high_resolution_clock::now();
    res.time_ns = chrono::duration_cast<chrono::nanoseconds>(t1 - t0).count();
    res.space_bytes = (long long)n * n * (sizeof(long long) + sizeof(int))
                    + (long long)g.edges.size() * sizeof(Edge);
    return res;
}

vector<int> bf_reconstruct(const BFResult& res, int src, int dst) {
    // FIX: return empty path immediately if a negative cycle was detected —
    // partially relaxed distances produce an inconsistent/misleading path.
    if (res.has_neg_cycle) return {};
    if (res.dist[src][dst] == INF) return {};
    vector<int> path;
    int cur = dst;
    set<int> visited;
    while (cur != -1 && !visited.count(cur)) {
        visited.insert(cur);
        path.push_back(cur);
        if (cur == src) break;
        cur = res.prev[src][cur];
    }
    reverse(path.begin(), path.end());
    if (path.empty() || path[0] != src) return {};
    return path;
}

// ─── Negative Cycle Detection via FW ─────────────────────────────────────────
vector<int> detect_neg_cycle_nodes(const FWResult& fw, int n) {
    vector<int> bad;
    for (int i = 0; i < n; i++)
        if (fw.dist[i][i] < 0) bad.push_back(i);
    return bad;
}

// ─── Output JSON ──────────────────────────────────────────────────────────────
string vec_to_json(const vector<int>& v) {
    string s = "[";
    for (int i = 0; i < (int)v.size(); i++) {
        if (i) s += ",";
        s += to_string(v[i]);
    }
    return s + "]";
}

string matrix_to_json(const vector<vector<long long>>& m) {
    string s = "[";
    for (int i = 0; i < (int)m.size(); i++) {
        if (i) s += ",";
        s += "[";
        for (int j = 0; j < (int)m[i].size(); j++) {
            if (j) s += ",";
            if (m[i][j] == INF) s += "null";
            else s += to_string(m[i][j]);
        }
        s += "]";
    }
    return s + "]";
}

int main(int argc, char* argv[]) {
    if (argc < 2) { cerr << "Usage: backend <graph_id> [src] [dst]\n"; return 1; }
    int gid = atoi(argv[1]);
    auto graphs = get_graphs();
    if (gid < 0 || gid >= (int)graphs.size()) { cerr << "Invalid graph id\n"; return 1; }
    const Graph& g = graphs[gid];

    int src = (argc >= 3) ? atoi(argv[2]) : 0;
    int dst = (argc >= 4) ? atoi(argv[3]) : g.n - 1;

    auto fw  = floyd_warshall(g);
    auto dij = repeated_dijkstra(g);
    auto bf  = repeated_bellman_ford(g);

    auto fw_path   = fw_reconstruct(fw, src, dst);
    auto dij_path  = dij.applicable ? dijk_reconstruct(dij, src, dst) : vector<int>{};
    auto bf_path   = bf_reconstruct(bf, src, dst);

    auto neg_nodes = detect_neg_cycle_nodes(fw, g.n);

    // Edge list JSON
    string edge_json = "[";
    for (int i = 0; i < (int)g.edges.size(); i++) {
        if (i) edge_json += ",";
        edge_json += "{\"u\":" + to_string(g.edges[i].u)
                  + ",\"v\":" + to_string(g.edges[i].v)
                  + ",\"w\":" + to_string(g.edges[i].w) + "}";
    }
    edge_json += "]";

    printf("{\n");
    printf("  \"graph_name\": \"%s\",\n", g.name.c_str());
    printf("  \"n\": %d,\n", g.n);
    printf("  \"edges\": %s,\n", edge_json.c_str());
    printf("  \"src\": %d,\n", src);
    printf("  \"dst\": %d,\n", dst);

    printf("  \"fw\": {\n");
    printf("    \"dist\": %s,\n", matrix_to_json(fw.dist).c_str());
    printf("    \"has_neg_cycle\": %s,\n", fw.has_neg_cycle ? "true" : "false");
    printf("    \"neg_cycle_nodes\": %s,\n", vec_to_json(neg_nodes).c_str());
    printf("    \"path\": %s,\n", vec_to_json(fw_path).c_str());
    printf("    \"time_ns\": %lld,\n", fw.time_ns);
    printf("    \"space_bytes\": %lld\n", fw.space_bytes);
    printf("  },\n");

    printf("  \"dijkstra\": {\n");
    printf("    \"dist\": %s,\n", dij.applicable ? matrix_to_json(dij.dist).c_str() : "null");
    printf("    \"applicable\": %s,\n", dij.applicable ? "true" : "false");
    printf("    \"path\": %s,\n", vec_to_json(dij_path).c_str());
    printf("    \"time_ns\": %lld,\n", dij.time_ns);
    printf("    \"space_bytes\": %lld\n", dij.space_bytes);
    printf("  },\n");

    printf("  \"bellman_ford\": {\n");
    printf("    \"dist\": %s,\n", matrix_to_json(bf.dist).c_str());
    printf("    \"has_neg_cycle\": %s,\n", bf.has_neg_cycle ? "true" : "false");
    printf("    \"path\": %s,\n", vec_to_json(bf_path).c_str());
    printf("    \"time_ns\": %lld,\n", bf.time_ns);
    printf("    \"space_bytes\": %lld\n", bf.space_bytes);
    printf("  }\n");
    printf("}\n");

    return 0;
}