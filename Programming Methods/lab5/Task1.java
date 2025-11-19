import java.util.Scanner;
import java.util.stream.*;

public class Task1 {
    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            int A, B;
            System.out.print("A = ");
            A = scanner.nextInt();
            System.out.print("B = ");
            B = scanner.nextInt();
            if (A < 0 || B < 0 || A > B) {
                throw new NumberFormatException();
            }
            double sum = (double) IntStream.range(A, B + 1)
            .map(n -> n * n)
            .sum();
            System.out.printf("Average of squares sum: %.2f", sum / (B - A + 1));
        } catch (Exception e) {
            System.out.println("Error!\nNumbers must be positive and A < B\n");
        }
    }
}