#include <iostream>
#include <fstream>
#include <string>
using namespace std;
int main(){
    fstream new_file;
    new_file.open("Resources/temp/in.txt", ios::in);
    char ch;
    if(!new_file){
        cout<<"NO such file"<<endl;
    }
    else{
        string a;
        while(!new_file.eof()){
            new_file>>a;
            cout<<stod(a)<<endl;
        }
        return 0;
    }
    return 0;
}
