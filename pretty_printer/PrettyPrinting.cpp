#include <bits/stdc++.h>

using namespace std;

vector <string> words;
int d[1000], pre[1000], x[1000];
int L = 80;

int main(){

    // open file
    ifstream input("./text.txt");
    ofstream output("./pretty-F.txt");

    cout<<"Nhap vao gia tri L: ";
    cin>>L;
    cout<<"\n";

    // read paragraph
    while(input.peek()!=EOF){
        string paragraph;
        getline(input, paragraph);

        // process
        istringstream ss(paragraph);

        int n = 0;
        words.clear();
        do {
            string word;
            ss>>word;

            if(word.length() > 0) {
                words.push_back(word);
                n++;
            }
        } while(ss);

        d[0] = 0;
        pre[0]=0;
        for(int i=1;i<=n;i++) {
            int s = 0;
            d[i] = d[i-1] + (L-words[i-1].length())*(L-words[i-1].length());
            s = words[i-1].length();
            pre[i] = i-1;
            for(int j=i-1;j>0;j--) {
                if(s+words[j-1].length()+1 <= L) {
                    s = s+words[j-1].length()+1;
                    int tmp = d[j-1] + (L-s)*(L-s);
                    if(d[i]>tmp) {
                        d[i] = tmp;
                        pre[i] = j-1;
                    }
                } else break;
            }
        }
        // trace
        int last = n;
        int nl = 0;
        x[++nl] = last;
        while(last) {
            last = pre[last];
            x[++nl] = last;
        }

        // print
        output<<d[n]<<endl;
        reverse(x+1,x+nl+1);
        for(int i=2;i<=nl;i++) {
            for(int j=x[i-1]+1;j<=x[i];j++) {
                output<<words[j-1];
                if(j!=x[i]) output<<' ';
            }
            output<<endl;
        }
    }

    // close file
    input.close();
    output.close();
}
