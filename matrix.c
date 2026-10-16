#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int** allocate_matrix(int n) {
    int** matrix = (int**)malloc(n * sizeof(int*));
    for (int i = 0; i < n; i++) {
        matrix[i] = (int*)malloc(n * sizeof(int));
    }
    return matrix;
}

void free_matrix(int** matrix, int n) {
    for (int i = 0; i < n; i++) free(matrix[i]);
    free(matrix);
}

int** generate_matrix(int n) {
    int** matrix = allocate_matrix(n);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            matrix[i][j] = (rand() % 10) + 1;
    return matrix;
}

void multiply_matrices(int** matrix_a, int** matrix_b, int** result, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            result[i][j] = 0;
            for (int k = 0; k < n; k++) {
                result[i][j] += matrix_a[i][k] * matrix_b[k][j];
            }
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("Uso: %s <tamano_n>\n", argv[0]);
        return 1;
    }
    int n = atoi(argv[1]);
    srand(time(NULL));

    int** matrix_a = generate_matrix(n);
    int** matrix_b = generate_matrix(n);
    int** result = allocate_matrix(n);

    clock_t start = clock();
    multiply_matrices(matrix_a, matrix_b, result, n);
    clock_t end = clock();

    printf("%.6f\n", (double)(end - start) / CLOCKS_PER_SEC);

    free_matrix(matrix_a, n);
    free_matrix(matrix_b, n);
    free_matrix(result, n);
    return 0;
}