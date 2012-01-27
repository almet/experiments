#include <iostream>
#include <stdio.h>
#include <string.h>

using namespace std;

int main(int argc, const char *argv[])
{
    string input = "this is a test";
    cout << "Now, let's try to parse this: " << input << endl;

    char* tok = strtok((char*)input.c_str(), " ");
    string first = (string) tok;

    tok = strtok(NULL, " ");
    string second = (string) tok;

    tok = strtok(NULL, " ");
    string third = (string) tok;

    tok = strtok(NULL, " ");
    string fourth = (string) tok;

    cout << first << second << third << fourth << endl;
    
    return 0;
}
