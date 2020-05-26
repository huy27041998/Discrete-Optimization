#include <bits/stdc++.h>
#define MAXINT 100000000
#define ep 1e-4

using namespace std;

int n, p[100];
double x[1000],y[1000];
double cost[100000][32];
double kq = MAXINT;

double dis(int i,int j){
    return sqrt((x[i]-x[j])*(x[i]-x[j])+(y[i]-y[j])*(y[i]-y[j]));
}

int main(){
    cin>>n;
    for(int i=0;i<n;i++) cin>>x[i]>>y[i];
    for(int i=0;i<=((1<<n)-1);i++) for(int j=0;j<=n;j++) cost[i][j]=MAXINT;

    for(int i=1;i<n;i++) cost[0][i]=dis(0,i);
    for(int s=1;s<n;s++){
        int S=(1<<s)-1;
        while(1){
            for(int i=1;i<n;i++) if((S&((1<<(i-1)))) != 0){
                int S1 = S&(~(1<<(i-1)));
                for(int j=1;j<n;j++) if((S&(1<<(j-1))) == 0) {
                    cost[S][j] = min(cost[S][j], cost[S1][i] + dis(i,j));
                    //cout<<S<<' '<<S1<<' '<<i<<' '<<j<<' '<<cost[S][j]<<endl;
                 }
            }
            int t = (S | (S-1)) + 1;
            int w = t|(((((t&-t)/(S&-S)))>>1)-1);
            if(w>>(n-1) != 0) break;
            else S = w;
            //cout<<S<<endl;
        }
    }
    int S = (1<<(n-1))-1;
    int finalS = S;
    for(int i=1;i<n;i++) {
        int S1 = S&(~(1<<(i-1)));
        //kq = min(kq, cost[S1][i] + dis(0,i));
        if(kq > cost[S1][i] + dis(0,i)) {
            kq = cost[S1][i] + dis(0,i);
            p[n-1]=i;
            finalS = S1;
        }
    }

    for(int it=n-2;it>=1;it--) {
        for(int i=1;i<n;i++) if((finalS&((1<<(i-1)))) != 0) {
            int S1 = finalS&(~(1<<(i-1)));
            if(cost[S1][i] + dis(i, p[it+1]) - cost[finalS][p[it+1]] < ep) {
                p[it] = i;
                finalS = S1;
                break;
            }
        }
    }
    reverse(p,p+n);
    cout<<kq<<endl;
    for(int i=0;i<n;i++) cout<<p[i]<<' ';
    return 0;
}
