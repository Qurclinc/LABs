package Task4;

import java.util.stream.*;
import java.lang.Math;

public class Task4 {
    public static void main(String[] args) {
        int monkeys = IntStream.range(6, 1000)
        .filter(m -> {
            return (m - Math.pow((m / 5) - 3, 2) - 1 == 0);
        })
        .findFirst()
        .orElse(-1);

        System.out.printf("There were %d monkeys.\n", monkeys);
    }
}
