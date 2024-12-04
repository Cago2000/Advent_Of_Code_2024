#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm> 
#include <unordered_map>

using namespace std;

vector<int> left_locations = {};
vector<int> right_locations = {};

bool comp(int a, int b) {
    return a >= b;
}

int main(){
   fstream locations;
   locations.open("locations.txt", ios::in);
   if(locations.is_open())
   {
      string delimiter = "   ";
      int total_distance = 0;
      string line;
      int left, right;

      while(getline(locations, line))
      {
         int split_pos = line.find(delimiter);
         left = stoi(line.substr(0, split_pos));
         right = stoi(line.substr(split_pos+3, line.length()));
         left_locations.push_back(left);
         right_locations.push_back(right);
      }
      sort(left_locations.begin(), left_locations.end(), comp);
      sort(right_locations.begin(), right_locations.end(), comp);

      for(int i = 0; i < left_locations.size(); i++)
      {
         total_distance += abs(left_locations.at(i) - right_locations.at(i));
      }
      cout << total_distance << endl;
      locations.close();
   }

   //Part_Two
   unordered_map<int, int> count_map; 
   for(int i = 0; i < left_locations.size(); i++)
   {
      for(int j = 0; j < right_locations.size(); j++)
      {
         if(left_locations[i] == right_locations[j])
         {
            if(count_map.find(left_locations[i]) == count_map.end()) {
               count_map.insert(make_pair(right_locations[j], 1));
            }
            else
            {
               count_map[left_locations[i]]++;
            }
         }
      }
   }
   int sum = 0;
   for(int i = 0; i < count_map.size(); i++)
   {
      sum += left_locations[i] * count_map[left_locations[i]];
   }
   cout << "Sum of similarity score: " << sum << endl;
}