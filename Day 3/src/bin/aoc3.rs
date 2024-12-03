use std::fs;
use regex::Regex;

fn main() {
    let file_path = "src/bin/instructions.txt";
    let contents = fs::read_to_string(file_path).unwrap();
    let pattern = Regex::new(r"(mul|do|don't)\((?:(\d+),(\d+))?\)").unwrap();
    let matches = pattern.captures_iter(&contents);
    let (mut sum, mut sum2) = (0, 0);
    let mut enabled= true;
    for digit_pair in matches {
        if &digit_pair[1] == "do"{enabled = true;}
        if &digit_pair[1] == "don't"{enabled = false;}
        if &digit_pair[1] == "mul" {
            let value = digit_pair[2].parse::<i32>().unwrap() * digit_pair[3].parse::<i32>().unwrap();
            sum2 += if enabled {value} else {0};
            sum += value;
        }
    }
    println!("Part One: Sum of all multiplications = {sum}");
    println!("Part Two: Sum of all multiplications = {sum2}");
}
