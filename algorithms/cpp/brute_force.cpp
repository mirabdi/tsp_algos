#include <vector>
#include <algorithm>
#include <limits>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

class BruteForceTSP {
private:
    std::vector<std::vector<double>> g;
    std::vector<int> t;
    double c;

    double calc_cost(const std::vector<int>& cur) {
        double tot = 0.0;
        for (size_t i = 0; i < cur.size(); ++i) {
            size_t j = (i + 1) % cur.size();
            tot += g[cur[i]][cur[j]];
        }
        return tot;
    }

public:
    BruteForceTSP() {}

    void solve(const std::vector<std::vector<double>>& g_in) {
        g = g_in;
        size_t n = g.size();
        
        std::vector<int> cur(n);
        for (size_t i = 0; i < n; ++i) {
            cur[i] = i;
        }
        
        std::vector<int> perm(cur.begin() + 1, cur.end());
        
        double mn = std::numeric_limits<double>::infinity();
        std::vector<int> best = cur;
        
        do {
            std::vector<int> full = {0};
            full.insert(full.end(), perm.begin(), perm.end());
            
            double cur_cost = calc_cost(full);
            if (cur_cost < mn) {
                mn = cur_cost;
                best = full;
            }
        } while (std::next_permutation(perm.begin(), perm.end()));
        
        t = best;
        c = mn;
    }

    std::vector<int> get_tour() const {
        return t;
    }

    double get_cost() const {
        return c;
    }
};

PYBIND11_MODULE(brute_force, m) {
    py::class_<BruteForceTSP>(m, "BruteForceTSP")
        .def(py::init<>())
        .def("solve", &BruteForceTSP::solve)
        .def("get_tour", &BruteForceTSP::get_tour)
        .def("get_cost", &BruteForceTSP::get_cost);
} 