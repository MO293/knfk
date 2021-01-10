#include <iostream>
#include <fstream>
#include <typeinfo>

using namespace std;

int main(int argc, char *argv[]){ //argc - ile argumentow uzytkownik podaje, argv - argument of vector, czyli tablica argumentow
    string filename = argv[1]; //zalozenie, ze plik bedzie wykonywany z jednym argumentem
    ofstream myfile; 
    myfile.open(filename.c_str()); //tworzy plik o nazwie podanej przez uzytkownika
    myfile << "Some text\n";
    myfile << "in here\n";
    myfile.close();
    cout << "Utworzono plik o nazwie: "<<filename<<endl;
    return 0;
}
