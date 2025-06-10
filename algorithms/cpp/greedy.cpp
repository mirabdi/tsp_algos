#include <vector>
#include <algorithm>
#include <limits>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

class GreedyTSP {
private:
    std::vector<std::vector<double>> g;
    std::vector<int> t;
    double c;

    int find_next(int cur, const std::vector<bool>& vis) {
        int nxt = -1;
        double mn = std::numeric_limits<double>::infinity();
        
        for (size_t i = 0; i < g.size(); ++i) {
            if (!vis[i] && g[cur][i] < mn) {
                mn = g[cur][i];
                nxt = i;
            }
        }
        return nxt;
    }

public:
    GreedyTSP() {}

    void solve(const std::vector<std::vector<double>>& g_in) {
        g = g_in;
        size_t n = g.size();
        t.clear();
        t.reserve(n);
        
        std::vector<bool> vis(n, false);
        int cur = 0;
        t.push_back(cur);
        vis[cur] = true;
        
        for (size_t i = 1; i < n; ++i) {
            cur = find_next(cur, vis);
            if (cur == -1) break;
            t.push_back(cur);
            vis[cur] = true;
        }
        
        c = 0.0;
        for (size_t i = 0; i < t.size(); ++i) {
            size_t j = (i + 1) % t.size();
            c += g[t[i]][t[j]];
        }
    }

    std::vector<int> get_tour() const {
        return t;
    }

    double get_cost() const {
        return c;
    }
};

PYBIND11_MODULE(greedy, m) {
    py::class_<GreedyTSP>(m, "GreedyTSP")
        .def(py::init<>())
        .def("solve", &GreedyTSP::solve)
        .def("get_tour", &GreedyTSP::get_tour)
        .def("get_cost", &GreedyTSP::get_cost);
} 