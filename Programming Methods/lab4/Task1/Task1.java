package Task1;

import java.util.stream.*;

public class Task1 {
    public static void main(String[] args) {
        int result = IntStream.range(100, 1000)
        .filter(w -> {
            int a = w % 10; // Единицы
            int b = (w / 10) % 10; // Десятки
            int c = (w / 100); // Сотни
            // System.out.printf("%d\t%d\t%d\t%d\n", a, b, c, w);
            return ((b - c == 4) && (a - b == 4));
        })
        .filter(w -> {
            StringBuilder str = new StringBuilder(Integer.toString(w)).reverse();
            int reversed_num = Integer.parseInt(str.toString());
            return (w + 792 == reversed_num);

        })
        .findFirst()
        .orElse(-1);
        System.out.printf("This number is: %s\n", result);
    }
}
