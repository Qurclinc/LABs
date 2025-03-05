import java.util.Scanner;

public class Task1 {
    public static void main(String[] args) {
        try (Scanner in = new Scanner(System.in)) {
            int a, b;
            a = in.nextInt();
            b = in.nextInt();
            int addition = a + b;
            int subtraction = a - b; 
            System.out.printf("a + b = %d\na - b = %d\n", addition, subtraction);
        }
    }
}