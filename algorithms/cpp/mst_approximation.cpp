#include <vector>
#include <queue>
#include <set>
#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

class MSTApproximation {
private:
    std::vector<std::vector<double>> g;
    std::vector<int> p;
    std::vector<double> k;
    std::vector<bool> mst;
    std::vector<int> t;
    double c;

    std::vector<int> preorder(int s) {
        std::vector<int> res;
        std::vector<bool> vis(g.size(), false);
        std::vector<int> stk = {s};
        
        while (!stk.empty()) {
            int v = stk.back();
            stk.pop_back();
            
            if (!vis[v]) {
                vis[v] = true;
                res.push_back(v);
                
                std::vector<int> ch;
                for (size_t i = 0; i < g.size(); ++i) {
                    if (p[i] == v) {
                        ch.push_back(i);
                    }
                }
                for (auto it = ch.rbegin(); it != ch.rend(); ++it) {
                    stk.push_back(*it);
                }
            }
        }
        return res;
    }

    double calc_cost() {
        double tot = 0.0;
        for (size_t i = 0; i < t.size(); ++i) {
            size_t j = (i + 1) % t.size();
            tot += g[t[i]][t[j]];
        }
        return tot;
    }

public:
    MSTApproximation() {}

    void solve(const std::vector<std::vector<double>>& g_in) {
        g = g_in;
        size_t n = g.size();
        
        k = std::vector<double>(n, std::numeric_limits<double>::infinity());
        p = std::vector<int>(n, -1);
        mst = std::vector<bool>(n, false);
        
        std::priority_queue<std::pair<double, int>, 
                          std::vector<std::pair<double, int>>,
                          std::greater<std::pair<double, int>>> pq;
        
        k[0] = 0;
        pq.push({0, 0});
        
        while (!pq.empty() && std::count(mst.begin(), mst.end(), true) < n) {
            int u = pq.top().second;
            pq.pop();
            
            if (mst[u]) {
                continue;
            }
            
            mst[u] = true;
            
            for (size_t v = 0; v < n; ++v) {
                if (!mst[v] && g[u][v] > 0 && g[u][v] < k[v]) {
                    p[v] = u;
                    k[v] = g[u][v];
                    pq.push({k[v], v});
                }
            }
        }
        
        t = preorder(0);
        c = calc_cost();
    }

    std::vector<int> get_tour() const {
        return t;
    }

    double get_cost() const {
        return c;
    }
};

PYBIND11_MODULE(mst_approximation, m) {
    py::class_<MSTApproximation>(m, "MSTApproximation")
        .def(py::init<>())
        .def("solve", &MSTApproximation::solve)
        .def("get_tour", &MSTApproximation::get_tour)
        .def("get_cost", &MSTApproximation::get_cost);
} 