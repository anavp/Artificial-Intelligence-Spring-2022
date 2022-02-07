/***************************************************
* AUTHOR : Anav Prasad
* Nick : graworth
****************************************************/
#include <bits/stdc++.h>

using namespace std;

#define endl "\n"
#define fastIO ios_base::sync_with_stdio(false),cin.tie(0)
#define forn(i, n) for (int i = 0; i < n; i++)
#define forsn(i, st_val, n) for (int i = st_val; i <= n; ++i)
#define forr(i, n) for (int i = n - 1; i >= 0; --i)
#define forsr(i, st_val, n) for (int i = st_val; i >= n; --i)
#define pb1(a) push_back(a)
#define pb2(a,b) push_back({a, b})
#define GET_MACRO(_1,_2,_3,NAME,...) NAME
#define pb(...) GET_MACRO(__VA_ARGS__, pb1, pb2)(__VA_ARGS__)
#define pass (void)0
#define print_var(x) cout << #x << ": " << x << "\n";
#define space " "
typedef long long int ll;
typedef unsigned long long int ull;
template <typename type> void print(const vector<vector<type> > &arr);
template <typename type> void print(const vector<type> &arr);
template <typename t1, typename t2> void print(const vector<pair<t1,t2> > &arr);
template <typename t1, typename t2> void print(const vector<vector<pair<t1,t2> > > &arr);
template <typename t1, typename t2> void print(const pair<t1, t2> &p);
template <typename t1, typename t2, typename t3> void print(const pair<t1, pair<t2, t3> > &p);
// Object	A	B	C	D	E
// Value	13	8	11	7	5
// Weight	11	4	7	4	2

const char a = 'a', b = 'b', c = 'c', d = 'd', e = 'e', f = 'f';
const int t = 23, m = 13;

int main(int argc, char *argv[]){
	fastIO;
	map<char, pair<int, int> > items;
    items.insert(pair<char, pair<int, int> > (a, pair<int,int>(13, 11)));
    items.insert(pair<char, pair<int, int> > (b, pair<int,int>(8, 4)));
    items.insert(pair<char, pair<int, int> > (c, pair<int,int>(11, 7)));
    items.insert(pair<char, pair<int, int> > (d, pair<int,int>(7, 4)));
    items.insert(pair<char, pair<int, int> > (e, pair<int,int>(5, 2)));
    int v = 0, w = 0;
    for (int i = 2; i < argc; ++i){
        if (items.find(argv[i][0]) == items.end()){
            cout << "shouldn't have happened\n";
            continue;
        }
        v += items[argv[i][0]].first;
        w += items[argv[i][0]].second;
    }
    if (argv[1][0] == 'f'){
        cout << "Value: " << v << endl;
        cout << "Weight: " << w << endl;
    }
    cout << "Error: " << max(w-m, 0) + max(t - v, 0) << endl;
	return 0;
}


template <typename type> void print(const vector<vector<type> > &arr){
	cout << "\n[";
	forn(i, arr.size()){
		cout << "[";
		forn(j, arr[i].size() - 1)
			cout << arr[i][j] << ", ";
		cout << arr[i][arr[i].size() - 1] << "]";
		if (i != arr.size() - 1)
			cout << "," << endl;
	}
	cout << "], 2D Vector\n";
}


template <typename type> void print(const vector<type> &arr){
	cout << "\n[";
	forn(i, arr.size()){
		cout << arr[i];
		if (i != arr.size() - 1)
			cout << ", ";
	}
	cout << "], 1D Vector\n";
}


template <typename t1, typename t2> void print(const vector<pair<t1,t2> > &arr){
	int n = arr.size();
	cout << "\n[";
	forn(i, n - 1){
		cout << "{" << arr[i].first << "," << arr[i].second << "}, ";
	}
	cout << "{" << arr[n - 1].first << "," << arr[n - 1].second << "}], 1D Vector of Pairs\n";
}


template <typename t1, typename t2> void print(const vector<vector<pair<t1,t2> > > &arr){
	cout << "\n[";
	forn(i, arr.size()){
		cout << "[";
		forn(j, arr[i].size()){
			cout << "{" << arr[i][j].first << "," << arr[i][j].second << "}";
			if (j != arr[i].size() - 1)
				cout << ", ";
		}
		cout << "]";
		if (i != arr.size() - 1)
			cout << "," << endl;
	}
	cout << "], 2D Vector of Pairs\n";
}


template <typename t1, typename t2> void print(const pair<t1, t2> &p){
	cout << "\n{" << p.first << "," << p.second << "}, Pair\n";
}

template <typename t1, typename t2, typename t3> void print(const pair<t1, pair<t2, t3> > &p){
    cout << "\n{" << p.first << ",{" << p.second.first << "," << p.second.second < "}}, Pair\n";
}