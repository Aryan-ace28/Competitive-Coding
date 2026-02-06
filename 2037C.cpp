#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(NULL);

    int t;
    cin >> t;
    while(t--){
        int n;
        cin >> n;

        if(n < 5){
            cout << -1 << "\n";
            continue;
        }

        for(int i = 7; i <= n; i += 2) cout << i << " ";
        cout << "3 1 5 4 2 ";
        for(int i = 6; i <= n; i += 2) cout << i << " ";
        cout << "\n";
    }
    return 0;
}