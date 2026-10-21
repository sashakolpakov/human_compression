// Fast active-store RUP, with the original full-history checker as exact fallback.
// Every active clause is an input or a previously checked consequence.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;

struct Checker {
    int n;
    vector<vector<int>> clauses, watch;
    vector<int> units, assignment, trail;
    vector<char> active;
    map<vector<int>, vector<int>> occurrences;
    int empty_count = 0;
    explicit Checker(int n): n(n), watch(2*n), assignment(n+1,0) {}
    int index(int x) { return 2*(abs(x)-1)+(x<0); }
    int value(int x) { return x>0 ? assignment[x] : -assignment[-x]; }
    bool assign(int x) {
        if (value(x)<0) return false;
        if (value(x)==0) { assignment[abs(x)]=x>0?1:-1; trail.push_back(x); }
        return true;
    }
    void add(vector<int> c, bool original=false) {
        sort(c.begin(),c.end());
        c.erase(unique(c.begin(),c.end()),c.end());
        for (int x:c) if (binary_search(c.begin(),c.end(),-x)) return;
        int id=clauses.size(); clauses.push_back(c); active.push_back(true);
        if (!original) occurrences[c].push_back(id);
        if (c.empty()) { ++empty_count; return; }
        if (c.size()==1) { units.push_back(id); return; }
        watch[index(c[0])].push_back(id); watch[index(c[1])].push_back(id);
    }
    bool erase_clause(vector<int> c) {
        sort(c.begin(),c.end());
        c.erase(unique(c.begin(),c.end()),c.end());
        auto found=occurrences.find(c);
        if (found==occurrences.end()) return false;
        int id=found->second.back(); found->second.pop_back();
        if (!active[id]) throw runtime_error("active occurrence invariant");
        active[id]=false;
        if (clauses[id].empty()) --empty_count;
        if (found->second.empty()) occurrences.erase(found);
        return true;
    }
    bool conflict(const vector<int>& c) {
        for (int x:trail) assignment[abs(x)]=0;
        trail.clear();
        if (empty_count) return true;
        for (int id:units) if (active[id] && !assign(clauses[id][0])) return true;
        for (int x:c) if (!assign(-x)) return true;
        for (size_t head=0; head<trail.size(); ++head) {
            int falsified=-trail[head];
            auto& pending=watch[index(falsified)];
            size_t j=0;
            while (j<pending.size()) {
                int id=pending[j];
                if (!active[id]) { pending[j]=pending.back(); pending.pop_back(); continue; }
                auto& clause=clauses[id];
                if (clause[0]!=falsified) swap(clause[0],clause[1]);
                if (clause[0]!=falsified) throw runtime_error("watch invariant");
                if (value(clause[1])>0) { ++j; continue; }
                size_t k=2;
                while (k<clause.size() && value(clause[k])<0) ++k;
                if (k<clause.size()) {
                    swap(clause[0],clause[k]);
                    watch[index(clause[0])].push_back(id);
                    pending[j]=pending.back(); pending.pop_back();
                } else {
                    if (!assign(clause[1])) return true;
                    ++j;
                }
            }
        }
        return false;
    }
};

struct HistoricalChecker {
    int n;
    vector<vector<int>> clauses, watch;
    vector<int> units, assignment, trail;
    bool empty = false;
    explicit HistoricalChecker(int n): n(n), watch(2*n), assignment(n+1,0) {}
    int index(int x) { return 2*(abs(x)-1)+(x<0); }
    int value(int x) { return x>0 ? assignment[x] : -assignment[-x]; }
    bool assign(int x) {
        if (value(x)<0) return false;
        if (value(x)==0) { assignment[abs(x)]=x>0?1:-1; trail.push_back(x); }
        return true;
    }
    void add(vector<int> c) {
        sort(c.begin(),c.end());
        c.erase(unique(c.begin(),c.end()),c.end());
        for (int x:c) if (binary_search(c.begin(),c.end(),-x)) return;
        if (c.empty()) { empty=true; return; }
        if (c.size()==1) { units.push_back(c[0]); return; }
        int id=clauses.size(); clauses.push_back(c);
        watch[index(c[0])].push_back(id); watch[index(c[1])].push_back(id);
    }
    bool conflict(const vector<int>& c) {
        for (int x:trail) assignment[abs(x)]=0;
        trail.clear();
        if (empty) return true;
        for (int x:units) if (!assign(x)) return true;
        for (int x:c) if (!assign(-x)) return true;
        for (size_t head=0; head<trail.size(); ++head) {
            int falsified=-trail[head];
            auto& pending=watch[index(falsified)];
            size_t j=0;
            while (j<pending.size()) {
                int id=pending[j]; auto& clause=clauses[id];
                if (clause[0]!=falsified) swap(clause[0],clause[1]);
                if (clause[0]!=falsified) throw runtime_error("watch invariant");
                if (value(clause[1])>0) { ++j; continue; }
                size_t k=2;
                while (k<clause.size() && value(clause[k])<0) ++k;
                if (k<clause.size()) {
                    swap(clause[0],clause[k]);
                    watch[index(clause[0])].push_back(id);
                    pending[j]=pending.back(); pending.pop_back();
                } else {
                    if (!assign(clause[1])) return true;
                    ++j;
                }
            }
        }
        return false;
    }
};

vector<int> parse_clause(const string& line, int n, bool deletion=false) {
    istringstream stream(line); string token; vector<int> out;
    if (deletion) stream>>token;
    bool ended=false;
    while (stream>>token) {
        size_t used=0; long long x=stoll(token,&used);
        if (used!=token.size() || ended || x>n || x< -static_cast<long long>(n))
            throw runtime_error("literal outside declared domain or trailing data");
        if (!x) ended=true; else out.push_back(static_cast<int>(x));
    }
    if (!ended) throw runtime_error("unterminated clause");
    return out;
}

int main(int argc,char**argv) {
    try {
        if(argc!=3) throw runtime_error("usage: rup formula.cnf proof.drat");
        ifstream input(argv[1]); string line, tag, kind, extra;
        int n=-1; long long wanted=-1, count=0;
        while(getline(input,line)) {
            if(line.empty() || line[0]=='c') continue;
            istringstream s(line); s>>tag>>kind>>n>>wanted;
            if(!s || tag!="p" || kind!="cnf" || n<0 || wanted<0 || (s>>extra))
                throw runtime_error("strict DIMACS header");
            break;
        }
        if(n<0 || n>10000000) throw runtime_error("missing or excessive variable count");
        Checker check(n); HistoricalChecker history(n);
        while(getline(input,line)) {
            if(line.empty() || line[0]=='c') continue;
            auto c=parse_clause(line,n); check.add(c,true); history.add(c); ++count;
        }
        if(count!=wanted) throw runtime_error("exact input clause count");
        ifstream proof(argv[2]); if(!proof) throw runtime_error("missing proof");
        long long additions=0,deletions=0,matched_deletions=0,fallbacks=0; bool concluded=false;
        while(getline(proof,line)) {
            if(line.empty() || line[0]=='c') continue;
            bool deletion=line[0]=='d'; auto c=parse_clause(line,n,deletion);
            if(deletion) { ++deletions; if(check.erase_clause(c)) ++matched_deletions; continue; }
            if(!check.conflict(c)) {
                ++fallbacks;
                if(!history.conflict(c)) throw runtime_error("addition fails reverse unit propagation at "+to_string(additions+1));
            }
            check.add(c); history.add(c); ++additions;
            if(c.empty()) concluded=true;
        }
        if(!concluded) throw runtime_error("no checked empty clause");
        cout<<"{\"status\":\"CHECKED_ARCHIVED_FALLBACK_RUP_REFUTATION\",\"variables\":"<<n
            <<",\"input_clauses\":"<<count<<",\"additions\":"<<additions
            <<",\"deletions\":"<<deletions<<",\"matched_deletions\":"<<matched_deletions
            <<",\"unmatched_deletions\":"<<(deletions-matched_deletions)
            <<",\"full_history_fallbacks\":"<<fallbacks<<"}\n";
        return 0;
    } catch(const exception& e) { cerr<<e.what()<<'\n'; return 1; }
}
