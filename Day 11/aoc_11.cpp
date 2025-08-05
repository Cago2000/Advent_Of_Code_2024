#include <iostream>
#include <fstream>
#include <unordered_map>
#include <string>
#include <sstream>

using namespace std;

pair<uint64_t, uint64_t> split_digit(uint64_t digit) {
    const string digit_str = to_string(digit);
    const uint64_t len = digit_str.length();
    if (len % 2 != 0) {
        return {digit, digit};
    }
    const uint64_t mid = len / 2;
    uint64_t left = stoull(digit_str.substr(0, mid));
    uint64_t right = stoull(digit_str.substr(mid));
    return {left, right};
}


unordered_map<int64_t, uint64_t> blink(const unordered_map<int64_t, uint64_t>& stones_count) {
    unordered_map<int64_t, uint64_t> new_stones_count;

    for (const auto& [stone, count] : stones_count) {
        if (stone == 0) {
            new_stones_count[1] += count;
            continue;
        }

        string stone_str = to_string(stone);
        if (stone_str.length() % 2 == 0) {
            auto [left_digit, right_digit] = split_digit(stone);
            new_stones_count[left_digit] += count;
            new_stones_count[right_digit] += count;
        } else {
            int64_t new_stone = stone * 2024;
            new_stones_count[new_stone] += count;
        }
    }
    return new_stones_count;
}



int main() {
    string path = "Day 11/stones.txt";
    ifstream stones_file(path);

    if (!stones_file.is_open()) {
        cerr << "Failed to open file." << endl;
        return 1;
    }

    unordered_map<int64_t, uint64_t> stones_count;

    string line;
    while (getline(stones_file, line)) {
        stringstream ss(line);
        int num;
        while (ss >> num) {
            stones_count[num]++;
        }
    }
    stones_file.close();

    int blinks = 75;
    for (int iter = 0; iter < blinks; ++iter) {
        uint64_t total_stones = 0;
        cout << "Iteration: " << iter << " | stones unique count: " << stones_count.size() << " | ";
        stones_count = blink(stones_count);
        for (auto& [stone, count] : stones_count) {
            total_stones += count;
        }

        cout << "Total stones count: " << total_stones << endl;
    }

    uint64_t total_stones = 0;
    for (auto& [stone, count] : stones_count) {
        total_stones += count;
    }
    cout << "Final total stones count: " << total_stones << endl;

    return 0;
}
