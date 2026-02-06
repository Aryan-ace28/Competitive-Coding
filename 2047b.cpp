#include <bits/stdc++.h>
using namespace std;
int main(){
    int t;
    cin>>t;
    while(t--){
       int l;//length of string
       cin>>l;
       string s;
       cin>>s;
       unordered_map<char,int>mp;
       for(char c:s){
           mp[c]++;
       }
       //largest frequency
       char c=s[0];
       int maxi=0;
       for(auto p:mp){
          if(maxi<=p.second){
              c=p.first;
              maxi=p.second;
          }
       }
       char c2=c;
       int min=maxi;
       for(auto p:mp){
          if(min>=p.second && p.first!=c){
              c2=p.first;
              min=p.second;
          }
       }
       for(int i=0;i<l;i++){
           if(c2==s[i]){
               s[i]=c;
               break;
           }
       }
       cout<<s<<endl;
    }
    
    return 0;
}