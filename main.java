import java.util.Random;

public class main {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Falta el argumento n");
            return;
        }
        int n = Integer.parseInt(args[0]);

        int[][] matrixA = generateMatrix(n);
        int[][] matrixB = generateMatrix(n);

        long startTime = System.nanoTime();
        multiplyMatrices(matrixA, matrixB, n);
        long endTime = System.nanoTime();

        double elapsedSeconds = (endTime - startTime) / 1_000_000_000.0;
        
        System.out.printf(java.util.Locale.US, "%.6f\n", elapsedSeconds);
    }

    public static int[][] generateMatrix(int n) {
        Random rand = new Random();
        int[][] matrix = new int[n][n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                matrix[i][j] = rand.nextInt(10) + 1;
        return matrix;
    }

    public static int[][] multiplyMatrices(int[][] a, int[][] b, int n) {
        int[][] result = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    result[i][j] += a[i][k] * b[k][j];
                }
            }
        }
        return result;
    }
}