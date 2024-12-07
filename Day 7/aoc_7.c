#include<stdio.h>
#include <stdlib.h> 
#include <stdint.h>
#include <math.h>

typedef struct {
    uint32_t result;
    int* elements;
    int elements_size;
} Equation;

typedef struct {
    Equation* equations;
    int size;
} EquationArray;

EquationArray* init_array(int size) 
{

    EquationArray* arr = (EquationArray*) malloc(sizeof(EquationArray));
    if (arr == NULL) {
        printf("Memory allocation failed for EquationArray struct\n");
        exit(1);}
    arr->size = size;
    arr->equations = NULL;
    return arr;
}

void add_element_to_eq_array(EquationArray* arr, Equation eq) 
{
    arr->size += 1;
    Equation* new_equations = (Equation*) realloc(arr->equations, arr->size * sizeof(Equation));
    if (new_equations == NULL) {
        printf("Memory reallocation failed. Unable to add element.\n");
        exit(1);
    }
    arr->equations = new_equations;
    arr->equations[arr->size - 1] = eq;
}

EquationArray* read_txt_file(char* path)
{
    EquationArray* equation_arr = init_array(0);
    FILE* file = fopen(path, "r");
    char line[256];
    if (file != NULL) {
        while (fgets(line, sizeof(line), file)) {
            char* token = strtok(line, ": ");
            char* endptr;
            uint32_t result = (uint32_t) strtoul(token, NULL, 10);
            Equation eq;
            eq.result = result;
            eq.elements = NULL;
            eq.elements_size = 0;
            token = strtok(NULL, " ");
            while (token != NULL) {
                eq.elements_size += 1;
                eq.elements = (int*) realloc(eq.elements, eq.elements_size * sizeof(int));
                if (eq.elements == NULL) {
                    printf("Memory reallocation failed for numbers\n");
                    exit(1);
                }
                eq.elements[eq.elements_size-1] = atoi(token);
                token = strtok(NULL, " ");
            }
            add_element_to_eq_array(equation_arr, eq);
        }
        fclose(file);
    }
    return equation_arr;
}

void print_equations(EquationArray* equation_arr)
{
    for(int i = 0; i < equation_arr->size; i++)
    {
        printf("%u, ", equation_arr->equations[i].result);
        for(int j = 0; j < equation_arr->equations[i].elements_size; j++)
        {
            printf("%d ", equation_arr->equations[i].elements[j]);
        }
        printf("\n");
    }
    printf("\n");
}

char* generate_permutation(int size, char *result, int index) {
    if (index == size) {
        result[index] = '\0';
        return result;
    }
    result[index] = '+';
    char* perm1 = generate_permutation(size, result, index + 1);

    result[index] = '*';
    char* perm2 = generate_permutation(size, result, index + 1);
    return perm1;
}

int calculate_calibration_results(EquationArray* equation_arr)
{
    int sum = 0;
    for (int i = 0; i < equation_arr->size; i++) {  
        int result = 0;
        char *op_arr = (char *)malloc((equation_arr->equations[i].elements_size-1) * sizeof(char));
        generate_permutation(equation_arr->equations[i].elements_size-1, op_arr, 0);
        for(int j = 0; j < equation_arr->equations[i].elements_size-1;j++)
        {
            int val1 = equation_arr->equations[i].elements[j];
            int val2 = equation_arr->equations[i].elements[j+1];
            printf("(%d, %d), ", val1, val2);
        }
        printf("\n"); 
    }
    return sum;
}


int main()
{  
    EquationArray* equation_arr = read_txt_file("calibration_equations_example.txt");
    print_equations(equation_arr);
    calculate_calibration_results(equation_arr);
    return 0;
}