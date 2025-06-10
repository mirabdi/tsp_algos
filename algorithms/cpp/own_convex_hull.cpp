#include <vector>
#include <algorithm>
#include <cmath>
#include <queue>
#include <set>
#include <functional>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

class OwnConvexHullTSP {
private:
    std::vector<std::vector<double>> graph;
    std::vector<int> tour;
    double cost;
    size_t n;

    // Calculate cross product of vectors (p2-p1) and (p3-p1)
    double cross(const std::vector<double>& p1, 
                const std::vector<double>& p2, 
                const std::vector<double>& p3) {
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - 
               (p2[1] - p1[1]) * (p3[0] - p1[0]);
    }

    // Find the convex hull using Graham scan
    std::vector<int> find_convex_hull(const std::vector<std::vector<double>>& points) {
        if (points.size() < 3) {
            std::vector<int> res;
            for (size_t i = 0; i < points.size(); ++i) {
                res.push_back(static_cast<int>(i));
            }
            return res;
        }

        // Find point with lowest y-coordinate (and leftmost if tied)
        size_t lowest = 0;
        for (size_t i = 1; i < points.size(); ++i) {
            if (points[i][1] < points[lowest][1] || 
                (points[i][1] == points[lowest][1] && points[i][0] < points[lowest][0])) {
                lowest = i;
            }
        }

        // Sort points by polar angle with lowest point
        std::vector<size_t> indices(points.size());
        for (size_t i = 0; i < points.size(); ++i) {
            indices[i] = i;
        }

        std::sort(indices.begin(), indices.end(),
            [&](size_t i, size_t j) {
                if (i == lowest) return true;
                if (j == lowest) return false;
                
                double angle_i = atan2(points[i][1] - points[lowest][1],
                                     points[i][0] - points[lowest][0]);
                double angle_j = atan2(points[j][1] - points[lowest][1],
                                     points[j][0] - points[lowest][0]);
                
                if (angle_i != angle_j) return angle_i < angle_j;
                
                // If angles are equal, sort by distance
                double dist_i = (points[i][0] - points[lowest][0]) * (points[i][0] - points[lowest][0]) +
                              (points[i][1] - points[lowest][1]) * (points[i][1] - points[lowest][1]);
                double dist_j = (points[j][0] - points[lowest][0]) * (points[j][0] - points[lowest][0]) +
                              (points[j][1] - points[lowest][1]) * (points[j][1] - points[lowest][1]);
                return dist_i < dist_j;
            });

        // Graham scan
        std::vector<int> hull;
        hull.push_back(static_cast<int>(indices[0]));
        hull.push_back(static_cast<int>(indices[1]));

        for (size_t i = 2; i < indices.size(); ++i) {
            while (hull.size() >= 2 && 
                   cross(points[hull[hull.size()-2]], 
                        points[hull[hull.size()-1]], 
                        points[indices[i]]) <= 0) {
                hull.pop_back();
            }
            hull.push_back(static_cast<int>(indices[i]));
        }

        return hull;
    }

    // Find Minimum Spanning Tree using Prim's algorithm
    std::vector<std::pair<int, int>> find_mst(const std::vector<int>& interior_points) {
        if (interior_points.empty()) return {};

        std::vector<std::pair<int, int>> mst_edges;
        std::vector<bool> visited(n, false);
        std::priority_queue<std::pair<double, std::pair<int, int>>,
                          std::vector<std::pair<double, std::pair<int, int>>>,
                          std::greater<std::pair<double, std::pair<int, int>>>> pq;

        // Start with the first interior point
        visited[interior_points[0]] = true;

        // Add all edges from the first point
        for (size_t i = 1; i < interior_points.size(); ++i) {
            int v = interior_points[i];
            pq.push({graph[interior_points[0]][v], {interior_points[0], v}});
        }

        while (!pq.empty() && mst_edges.size() < interior_points.size() - 1) {
            auto current = pq.top();
            pq.pop();
            double weight = current.first;
            int u = current.second.first;
            int v = current.second.second;

            if (visited[v]) continue;

            visited[v] = true;
            mst_edges.push_back({u, v});

            // Add all edges from the newly visited vertex
            for (int w : interior_points) {
                if (!visited[w]) {
                    pq.push({graph[v][w], {v, w}});
                }
            }
        }

        return mst_edges;
    }

    // Find the best connection between hull and MST
    std::pair<int, int> find_best_connection(const std::vector<int>& hull, 
                                           const std::vector<int>& interior_points) {
        double min_cost = std::numeric_limits<double>::infinity();
        std::pair<int, int> best_connection;

        for (int h : hull) {
            for (int i : interior_points) {
                if (graph[h][i] < min_cost) {
                    min_cost = graph[h][i];
                    best_connection = {h, i};
                }
            }
        }
        return best_connection;
    }

    // Merge convex hull and MST to create a tour
    std::vector<int> merge_hull_and_mst(const std::vector<int>& hull, 
                                      const std::vector<std::pair<int, int>>& mst_edges,
                                      const std::vector<int>& interior_points) {
        // Create adjacency list for MST
        std::vector<std::vector<int>> mst_adj(n);
        for (const auto& edge : mst_edges) {
            mst_adj[edge.first].push_back(edge.second);
            mst_adj[edge.second].push_back(edge.first);
        }

        // Find best connection between hull and MST
        auto connection = find_best_connection(hull, interior_points);
        int hull_point = connection.first;
        int mst_point = connection.second;

        // Create the tour by following the hull and then the MST
        std::vector<int> final_tour;
        std::vector<bool> visited(n, false);

        // Add hull points
        for (int h : hull) {
            final_tour.push_back(h);
            visited[h] = true;
        }

        // Add MST points starting from the connection point
        std::vector<int> mst_tour;
        std::function<void(int)> dfs = [&](int v) {
            visited[v] = true;
            mst_tour.push_back(v);
            for (int u : mst_adj[v]) {
                if (!visited[u]) {
                    dfs(u);
                }
            }
        };
        dfs(mst_point);

        // Insert MST tour at the best position in the hull tour
        size_t best_pos = 0;
        double min_cost = std::numeric_limits<double>::infinity();
        for (size_t i = 0; i < final_tour.size(); ++i) {
            int prev = final_tour[i];
            int next = final_tour[(i + 1) % final_tour.size()];
            double cost = graph[prev][mst_tour.front()] + graph[mst_tour.back()][next] - graph[prev][next];
            if (cost < min_cost) {
                min_cost = cost;
                best_pos = i + 1;
            }
        }

        final_tour.insert(final_tour.begin() + best_pos, mst_tour.begin(), mst_tour.end());
        final_tour.push_back(final_tour[0]);  // Close the tour

        return final_tour;
    }

public:
    OwnConvexHullTSP() {}

    void solve(const std::vector<std::vector<double>>& input_graph) {
        graph = input_graph;
        n = graph.size();
        
        // Convert distance matrix to coordinates (approximate)
        std::vector<std::vector<double>> coordinates(n, std::vector<double>(2));
        for (size_t i = 0; i < n; ++i) {
            coordinates[i][0] = graph[i][0];  // Use first two distances as coordinates
            coordinates[i][1] = graph[i][1];
        }
        
        // Find convex hull
        std::vector<int> hull = find_convex_hull(coordinates);
        
        // Get interior points (points not in convex hull)
        std::set<int> hull_set(hull.begin(), hull.end());
        std::vector<int> interior_points;
        for (size_t i = 0; i < n; ++i) {
            if (hull_set.find(static_cast<int>(i)) == hull_set.end()) {
                interior_points.push_back(static_cast<int>(i));
            }
        }
        
        // Find MST for interior points
        std::vector<std::pair<int, int>> mst_edges = find_mst(interior_points);
        
        // Merge hull and MST to create tour
        tour = merge_hull_and_mst(hull, mst_edges, interior_points);
        
        // Calculate tour cost
        cost = 0.0;
        for (size_t i = 0; i < tour.size() - 1; ++i) {
            cost += graph[tour[i]][tour[i + 1]];
        }
    }

    std::vector<int> get_tour() const {
        return tour;
    }

    double get_cost() const {
        return cost;
    }
};

PYBIND11_MODULE(own_convex_hull, m) {
    py::class_<OwnConvexHullTSP>(m, "OwnConvexHullTSP")
        .def(py::init<>())
        .def("solve", &OwnConvexHullTSP::solve)
        .def("get_tour", &OwnConvexHullTSP::get_tour)
        .def("get_cost", &OwnConvexHullTSP::get_cost);
} 