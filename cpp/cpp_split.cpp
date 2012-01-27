#include <iostream>
#include <stdio.h>
#include <string.h>

using namespace std;

int main(int argc, const char *argv[])
{
    string input = "this is a test";
    cout << "Now, let's try to parse this: " << input << endl;

    char* tok = strtok((char*)input.c_str(), " ");

    while (tok != NULL){
        cout << tok << endl;
        tok = strtok(NULL, " ");
    }
    
    return 0;
}
