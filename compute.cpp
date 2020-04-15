#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>
#include <iomanip>
#include <istream>

using namespace std;

string read(string name){
   std::ifstream inFile;
   inFile.open(name); //open the input file

   std::stringstream strStream;
   strStream << inFile.rdbuf(); //read the file
   std::string str = strStream.str(); //str holds the content of the file
   return str;
}


vector<string> parse_python_list(string list) {
    vector<string> viruses_vector;
    istringstream ss(list);
    do {
        string word;
        ss >> word;
        viruses_vector.push_back(word);
    } while (ss);
    return viruses_vector;
}


vector<string> make_substrings(string size, string hex_file){
    vector<string> substrings;
    for (int i = 0; i < hex_file.size() - stoi(size) - 1 ; i++){
        substrings.push_back(hex_file.substr(i,stoi(size)));
    }
    return substrings;
}


bool compare(string hex_file, string virus, string sub_size){
    if (stoi(sub_size) > hex_file.size() || stoi(sub_size) > virus.size()) {return false;}
    vector<string> hex_file_subs = make_substrings(sub_size, hex_file);
    // vector<string> virus_sub = make_substrings(sub_size, virus);
    bool any = false;
    for (int i = 0 ; i < hex_file_subs.size() ; i ++){
        // cout<<i;
        if (virus.find(hex_file_subs[i]) != std::string::npos) {
            any = true;
        }
        // if(std::find(virus_sub.begin(), virus_sub.end(), hex_file_subs[i]) != virus_sub.end()) {
        //     any = true;
        // }
    }
    return any;
}


void write(bool to_write) {
    ofstream ofs("tunnel1.txt", ofstream::trunc);
    ofs << to_write;
    ofs.close();
}

bool is_virus(string hex_file, vector<string> viruses_vector, string final_subsize) {
    for ( int i = 0 ; i < viruses_vector.size() - 1 ; i++) {
        int sub_size = 16;
        bool go_on = true;
        while (go_on) {
            if (sub_size >= stoi(final_subsize)) return true;
            bool result = compare(hex_file, viruses_vector[i], to_string(sub_size));
            cout <<  "virus n°"<<i << " sub_size = " << sub_size << " result = " << result << endl;
            if (result == false) go_on = false;
            sub_size *= 2;
        }
    }
    return false;
}

int main(){
    string viruses = read("tunnel1.txt");
    string hex_file = read("tunnel2.txt");
    string size = read("tunnel3.txt");
    vector<string> viruses_vect = parse_python_list(viruses);
    bool result = is_virus(hex_file, viruses_vect, "17");
    write(result);
    return 0;
}
