package Task2;

import java.lang.Math;
import java.util.stream.*;

public class Task2 {
    public static void main(String[] args) {
        int result = IntStream.range(10, 100)
        .filter(w -> {
            int a = w % 10;
            int b = w / 10;
            int max = Math.max(a, b);
            int min = Math.min(a, b);
            return (w == (a + b) * (max - min));
        })
        .findFirst()
        .orElse(-1);

        System.out.printf("This number is %s\n", result);
    }
}
