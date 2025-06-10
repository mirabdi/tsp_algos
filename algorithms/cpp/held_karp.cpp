#include <vector>
#include <unordered_map>
#include <limits>
#include <stdexcept>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

namespace py = pybind11;

class HeldKarpTSP {
private:
    std::vector<std::vector<double>> g;
    std::vector<int> t;
    double c;
    size_t n;

    struct StateKey {
        uint64_t k;

        StateKey(size_t p, int m) {
            if (p > 0xFFFFFFFF) {
                throw std::runtime_error("Position too large for key");
            }
            k = (static_cast<uint64_t>(p) << 32) | static_cast<uint32_t>(m);
        }

        bool operator==(const StateKey& o) const {
            return k == o.k;
        }
    };

    struct StateKeyHash {
        std::size_t operator()(const StateKey& k) const {
            return std::hash<uint64_t>{}(k.k);
        }
    };

    double dp(size_t p, int m, 
             std::unordered_map<StateKey, double, StateKeyHash>& d,
             std::unordered_map<StateKey, size_t, StateKeyHash>& par) {
        if (m == (1 << n) - 1) {
            return g[p][0];
        }

        StateKey s(p, m);
        auto it = d.find(s);
        if (it != d.end()) {
            return it->second;
        }

        double mn = std::numeric_limits<double>::infinity();
        size_t best = 0;

        for (size_t nxt = 0; nxt < n; ++nxt) {
            if (!(m & (1 << nxt))) {
                double cur = g[p][nxt] + dp(nxt, m | (1 << nxt), d, par);
                if (cur < mn) {
                    mn = cur;
                    best = nxt;
                }
            }
        }

        d[s] = mn;
        par[s] = best;
        return mn;
    }

    void build_tour(const std::unordered_map<StateKey, size_t, StateKeyHash>& par) {
        t.clear();
        t.reserve(n);
        
        size_t p = 0;
        int m = 1;
        
        t.push_back(0);
        
        for (size_t i = 1; i < n; ++i) {
            StateKey s(p, m);
            auto it = par.find(s);
            if (it == par.end()) {
                throw std::runtime_error("Failed to reconstruct tour: state not found");
            }
            p = it->second;
            m |= (1 << p);
            t.push_back(static_cast<int>(p));
        }
        
        t.push_back(0);
    }

public:
    HeldKarpTSP() {}

    void solve(const std::vector<std::vector<double>>& g_in) {
        if (g_in.empty() || g_in.size() > 32) {
            throw std::runtime_error("Graph size must be between 1 and 32 vertices");
        }
        
        g = g_in;
        n = g.size();
        
        std::unordered_map<StateKey, double, StateKeyHash> d;
        std::unordered_map<StateKey, size_t, StateKeyHash> par;
        
        try {
            c = dp(0, 1, d, par);
            build_tour(par);
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Held-Karp algorithm failed: ") + e.what());
        }
    }

    std::vector<int> get_tour() const {
        return t;
    }

    double get_cost() const {
        return c;
    }
};

PYBIND11_MODULE(held_karp, m) {
    py::class_<HeldKarpTSP>(m, "HeldKarpTSP")
        .def(py::init<>())
        .def("solve", &HeldKarpTSP::solve)
        .def("get_tour", &HeldKarpTSP::get_tour)
        .def("get_cost", &HeldKarpTSP::get_cost);
} 