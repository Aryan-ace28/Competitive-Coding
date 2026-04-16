#include<bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;

    vector<int> arr(n);
    for(int i = 0; i < n; i++){
        cin >> arr[i];
    }

    unordered_map<int,int> mp;

    int maxim = 0;
    int left = 0;

    for(int right = 0; right < n; right++){

        if(mp.find(arr[right]) != mp.end() && mp[arr[right]] >= left){
            left = mp[arr[right]] + 1;
        }

        mp[arr[right]] = right;

        maxim = max(maxim, right - left + 1);
    }

    cout << maxim;
    return 0;
}