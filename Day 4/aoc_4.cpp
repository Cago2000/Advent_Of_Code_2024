#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm> 
#include <unordered_map>
#include <list>

using namespace std;
vector<pair<int, int>> neighbours = {
        {-1, -1}, {0, -1}, {1, -1},
        {-1,  0},          {1,  0},
        {-1,  1}, {0,  1}, {1,  1}};

int main(){

    fstream wordsearch;
    wordsearch.open("wordsearch.txt", ios::in);
    //wordsearch.open("wordsearch_example.txt", ios::in);
    string line;
    vector<string> wordfield(0);
    int counter = 0;
    if(wordsearch.is_open())
    {
        
        while(getline(wordsearch, line))
        {
            wordfield.push_back(line);
        }
    }
    
    for(int i = 0; i < wordfield.size(); i++)
    {
        for(int j = 0; j < wordfield[i].size();j++)
        {
            if(wordfield[i][j] == 'X')
            {
                for (const auto& [a, b] : neighbours){
                    if(i+a < 0  || i+a >= wordfield.size()|| j+b < 0 || j+b >= wordfield[i].size()){continue;}
                    if(i+2*a < 0  || i+2*a >= wordfield.size()  || j+2*b < 0 || j+2*b >= wordfield[i].size()){continue;}
                    if(i+3*a < 0  || i+3*a >= wordfield.size()|| j+3*b < 0 || j+3*b >= wordfield[i].size()){continue;}
                    if(string(1, wordfield[i][j]) + wordfield[i+a][j+b] +wordfield[i+2*a][j+2*b] + wordfield[i+3*a][j+3*b] == "XMAS")
                    {
                        counter++;
                    }    
                }
                
            }
        }
    }
    cout << "Part One: XMAS count = "<< counter << endl;
    int counter2 = 0;
    vector<pair<int, int>> neighbours = {
            {-1, -1}, {-1, 1},
            {1,  -1}, {1,  1}};
    for(int i = 0; i < wordfield.size(); i++)
    {
        for(int j = 0; j < wordfield[i].size();j++)
        {
            if(wordfield[i][j] == 'A')
            {
                vector<char> characters;
                for (const auto& [a, b] : neighbours){
                    if(i+a < 0  || i+a >= wordfield.size()|| j+b < 0 || j+b >= wordfield[i].size()){continue;}
                    if(wordfield[i+a][j+b] == 'M' || wordfield[i+a][j+b] == 'S')
                    {
                        characters.push_back(wordfield[i+a][j+b]);
                    } 
                      
                }
                if(characters.size() == 4){

                    int m_counts = 0;
                    int s_counts = 0;
                    for(char c: characters)
                    {
                        if(c == 'M')
                        {
                            m_counts++;
                        }
                        else
                        {
                            s_counts++;
                        }
                    }
                    if(s_counts == m_counts && characters.at(1) != characters.at(2))
                    {
                        counter2++;
                    }           
                }
            }
        }
    }
    cout << "Part Two: X-MAS count = " << counter2 << endl;
}