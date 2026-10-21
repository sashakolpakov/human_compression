// Reuse the accepted parser and historical propagator without modifying them.
#define main retained_fallback_entry_point
#include "../../rup_fallback_work/rup.cpp"
#undef main

// The assignment is derived from the original formula alone and never changes.
bool residual(const vector<int>& clause, const vector<int>& root,
              vector<int>& result) {
    result.clear();
    for (int literal : clause) {
        int value = literal > 0 ? root[literal] : -root[-literal];
        if (value > 0) return true;
        if (value == 0) result.push_back(literal);
    }
    return false;
}

int main(int argc, char** argv) {
    try {
        if (argc != 3) throw runtime_error("usage: root_units formula.cnf proof.drup");
        ifstream input(argv[1]);
        if (!input) throw runtime_error("missing formula");
        string line, tag, kind, extra;
        int n = -1;
        long long wanted = -1;
        while (getline(input, line)) {
            if (line.empty() || line[0] == 'c') continue;
            istringstream stream(line);
            stream >> tag >> kind >> n >> wanted;
            if (!stream || tag != "p" || kind != "cnf" || n < 0 ||
                wanted < 0 || (stream >> extra))
                throw runtime_error("strict DIMACS header");
            break;
        }
        if (n < 0 || n > 10000000) throw runtime_error("missing or excessive variable count");
        vector<vector<int>> original;
        while (getline(input, line)) {
            if (line.empty() || line[0] == 'c') continue;
            original.push_back(parse_clause(line, n));
        }
        if (static_cast<long long>(original.size()) != wanted)
            throw runtime_error("exact input clause count");

        vector<int> root;
        bool original_conflict;
        {
            HistoricalChecker bootstrap(n);
            for (const auto& clause : original) bootstrap.add(clause);
            original_conflict = bootstrap.conflict({});
            root = bootstrap.assignment;
        }
        Checker active(n);
        HistoricalChecker history(n);
        vector<int> reduced;
        if (!original_conflict)
            for (const auto& clause : original)
                if (!residual(clause, root, reduced)) {
                    active.add(reduced, true);
                    history.add(reduced);
                }
        original.clear();
        original.shrink_to_fit();

        ifstream proof(argv[2]);
        if (!proof) throw runtime_error("missing proof");
        long long additions = 0, deletions = 0, root_satisfied = 0;
        long long root_satisfied_deletions = 0, conflict_skipped_deletions = 0;
        long long matched_residual_deletions = 0, unmatched_residual_deletions = 0;
        long long historical_fallbacks = 0;
        bool concluded = false;
        while (getline(proof, line)) {
            if (line.empty() || line[0] == 'c') continue;
            bool deletion = line[0] == 'd';
            // Parse fully even after a contradiction or for a deletion.
            auto clause = parse_clause(line, n, deletion);
            if (deletion) {
                ++deletions;
                if (original_conflict) ++conflict_skipped_deletions;
                else if (residual(clause, root, reduced)) ++root_satisfied_deletions;
                else if (active.erase_clause(reduced)) ++matched_residual_deletions;
                else ++unmatched_residual_deletions;
                continue;
            }
            if (!original_conflict) {
                if (residual(clause, root, reduced)) {
                    ++root_satisfied;
                } else {
                    if (!active.conflict(reduced)) {
                        ++historical_fallbacks;
                        if (!history.conflict(reduced))
                            throw runtime_error("addition fails reverse unit propagation at " +
                                                to_string(additions + 1));
                    }
                    active.add(reduced);
                    history.add(reduced);
                }
            }
            ++additions;
            // A nonempty original clause reducing to empty is insufficient.
            if (clause.empty()) concluded = true;
        }
        if (!concluded) throw runtime_error("no checked empty clause");
        auto assigned = count_if(root.begin() + 1, root.end(), [](int x) { return x != 0; });
        cout << "{\"status\":\"CHECKED_ROOT_UNIT_ACTIVE_FALLBACK_RUP_REFUTATION\",\"variables\":" << n
             << ",\"input_clauses\":" << wanted << ",\"additions\":" << additions
             << ",\"deletions\":" << deletions << ",\"original_root_variables\":" << assigned
             << ",\"original_root_conflict\":" << (original_conflict ? "true" : "false")
             << ",\"root_satisfied_additions\":" << root_satisfied
             << ",\"root_satisfied_deletions\":" << root_satisfied_deletions
             << ",\"conflict_skipped_deletions\":" << conflict_skipped_deletions
             << ",\"matched_residual_deletions\":" << matched_residual_deletions
             << ",\"unmatched_residual_deletions\":" << unmatched_residual_deletions
             << ",\"historical_fallbacks\":" << historical_fallbacks << "}\n";
        return 0;
    } catch (const exception& error) {
        cerr << error.what() << '\n';
        return 1;
    }
}
