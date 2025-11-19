package Task3;

import java.util.stream.*;
import java.lang.Math;

public class Task3 {
    public static void main(String[] args) {
        int A = 200, B = 5;
        int result = IntStream.range(1, 10000)
        .filter(w -> {
            int x = w * B;
            return (Math.sqrt(x) * Math.sqrt(x) == x) && (Math.sqrt(x) == A);
        })
        .findFirst()
        .orElse(-1);

        System.out.printf("This number is %s\n", result);
    }
}
