#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>
#include <iomanip>
#include <istream>




using namespace std;

class binascii
{
public:
static std::string b2a_hex( const std::string& input );
static std::string hexlify( const std::string& input );
static std::string a2b_hex( const std::string& input );
static std::string unhexlify( const std::string& input );
};

std::string binascii::b2a_hex( const std::string& input )
{
const static std::string HexCodes = "0123456789ABCDEF";
std::string HexString;
for ( int i = 0; i < input.length(); ++i )
{
unsigned char BinValue = input[i];
HexString += HexCodes[( BinValue >> 4 ) & 0x0F];
HexString += HexCodes[BinValue & 0x0F];
}
return HexString;
}

std::string binascii::hexlify( const std::string& input )
{
return b2a_hex( input );
}


string read(string name){
   std::ifstream inFile;
   inFile.open(name); //open the input file

   std::stringstream strStream;
   strStream << inFile.rdbuf(); //read the file
   std::string str = strStream.str(); //str holds the content of the file
   return str;
}

string get_hex_compressed(string name){
    string str = binascii::hexlify(read(name));
    string result = "";
    for (int i = 0; i < str.size() ; i++){
        if (i % 20 == 0) result += str[i];
    }
    return result;
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
    vector<string> virus_sub = make_substrings(sub_size, virus);
    bool any = false;
    for (int i = 0 ; i < hex_file_subs.size() ; i ++){
        if(std::find(virus_sub.begin(), virus_sub.end(), hex_file_subs[i]) != virus_sub.end()) {
            any = true;
        }
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
    // string viruses = read("tunnel1.txt");
    // string hex_file = read("tunnel2.txt");
    // string size = read("tunnel3.txt");
    // vector<string> viruses_vect = parse_python_list(viruses);
    // bool result = is_virus(hex_file, viruses_vect, size);
    // write(result);
    cout << get_hex_compressed("virus1.txt");
    return 0;
}
