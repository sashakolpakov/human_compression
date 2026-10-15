#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

// Exact root coordinates of det(C) times a fundamental weight.
// The independent reader verifies the complete exported set under every
// reflection. Hashes are used only for storage; equality compares all entries.
using Vector = std::array<int, 8>;
struct Hash {
    size_t operator()(const Vector &v) const {
        size_t h = 17;
        for (int x : v) h = h * 1000003u + std::hash<int>{}(x);
        return h;
    }
};
void require(bool value, const char *message) {
    if (!value) throw std::runtime_error(message);
}
int main(int argc, char **argv) {
    try {
        require(argc == 4, "usage: weight_orbits INPUT OUTPUT SECONDS");
        std::ifstream in(argv[1]);
        int n, k;
        require(bool(in >> n >> k), "missing rank and type");
        require((n == 7 || n == 8) && k >= 0 && k < n, "bad rank or type");
        int C[8][8]{}, B[8][8]{}, expected[8][8]{};
        for (int i = 0; i < n; ++i) expected[i][i] = 2;
        for (auto edge : std::vector<std::pair<int,int>>{{0,1},{0,2},{2,3},{0,4},{4,5},{5,6}})
            expected[edge.first][edge.second] = expected[edge.second][edge.first] = -1;
        if (n == 8) expected[6][7] = expected[7][6] = -1;
        for (int i = 0; i < n; ++i) for (int j = 0; j < n; ++j) {
            require(bool(in >> C[i][j]), "missing Cartan entry");
            require(C[i][j] == expected[i][j], "wrong Cartan matrix");
        }
        for (int i = 0; i < n; ++i) for (int j = 0; j < n; ++j) {
            require(bool(in >> B[i][j]), "missing inverse entry");
            require(B[i][j] > 0 && B[i][j] <= 30, "inverse entry out of range");
        }
        std::string extra;
        require(!(in >> extra), "trailing input");
        int d = n == 7 ? 2 : 1;
        for (int i = 0; i < n; ++i) for (int j = 0; j < n; ++j) {
            int value = 0;
            for (int t = 0; t < n; ++t) value += C[i][t] * B[t][j];
            require(value == (i == j ? d : 0), "inverse identity failed");
        }
        size_t used = 0;
        double seconds = std::stod(argv[3], &used);
        require(used == std::string(argv[3]).size() && seconds > 0 && seconds <= 600,
                "invalid deadline");
        auto start = std::chrono::steady_clock::now();
        auto bounded = [&](const Vector &v) {
            // Cauchy--Schwarz gives z_i^2 <= B_ii B_kk <= 900.
            for (int i = 0; i < n; ++i)
                require(v[i] * v[i] <= B[i][i] * B[k][k], "coordinate norm bound failed");
        };
        Vector initial{};
        for (int i = 0; i < n; ++i) initial[i] = B[i][k];
        bounded(initial);
        std::vector<Vector> orbit{initial};
        std::unordered_set<Vector, Hash> seen{initial};
        for (size_t cursor = 0; cursor < orbit.size(); ++cursor) {
            if ((cursor & 4095u) == 0)
                require(std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count() <= seconds,
                        "incomplete: deadline");
            const Vector x = orbit[cursor];
            for (int i = 0; i < n; ++i) if (i != k && x[i] == B[i][k])
                for (int j = 0; j < n; ++j) if (j != k && j != i)
                    require(x[j] != -B[j][k], "negative incidence triangle found");
            for (int i = 0; i < n; ++i) {
                int product = 0;
                for (int j = 0; j < n; ++j) product += C[i][j] * x[j];
                Vector y = x;
                y[i] -= product;
                bounded(y);
                if (seen.insert(y).second) orbit.push_back(y);
            }
            require(orbit.size() <= 1000000, "incomplete: storage limit");
        }
        std::sort(orbit.begin(), orbit.end());
        std::ofstream out(argv[2], std::ios::out | std::ios::trunc);
        require(bool(out), "cannot open output");
        out << "ORBIT " << n << ' ' << k << ' ' << orbit.size() << '\n';
        for (const auto &v : orbit) {
            for (int i = 0; i < n; ++i) out << (i ? " " : "") << v[i];
            out << '\n';
        }
        out.close();
        require(bool(out), "cannot finish output");
        std::cout << "COMPLETE " << n << ' ' << k << ' ' << orbit.size() << '\n';
        return 0;
    } catch (const std::exception &e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
}
