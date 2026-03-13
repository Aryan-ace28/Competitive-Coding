class Solution {
public:
    vector<vector<int>> ans;

    void solve(int i, vector<int>& a, int target, vector<int>& temp){
        if(target==0){
            ans.push_back(temp);
            return;
        }

        for(int j=i;j<a.size();j++){
            if(j>i && a[j]==a[j-1]) continue;
            if(a[j]>target) break;

            temp.push_back(a[j]);
            solve(j+1,a,target-a[j],temp);
            temp.pop_back();
        }
    }

    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
        sort(candidates.begin(),candidates.end());
        vector<int> temp;
        solve(0,candidates,target,temp);
        return ans;
    }
};