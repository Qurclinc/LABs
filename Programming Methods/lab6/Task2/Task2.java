import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Map;
import java.util.stream.*;

public class Task2 {
    public static void main(String[] args) {
        ArrayList<Abiturient> abiturients = new ArrayList<>(Arrays.asList(
            new Abiturient("School №1", 2020, "Ivanov"),
            new Abiturient("School №2", 2020, "Petrov"),
            new Abiturient("School №3", 2020, "Sidorov"),

            new Abiturient("School №1", 2021, "Smirnov"),
            new Abiturient("School №2", 2021, "Popov"),

            new Abiturient("School №3", 2022, "Egorov"),
            new Abiturient("School №1", 2022, "Kuznetsov"),
            new Abiturient("School №2", 2022, "Orlov"),
            new Abiturient("School №3", 2022, "Volkova"),

            new Abiturient("School №1", 2023, "Nikitin"),
            new Abiturient("School №2", 2023, "Abramov"),
            new Abiturient("School №3", 2023, "Fedorov"),
            new Abiturient("School №4", 2023, "Belov"),

            new Abiturient("School №2", 2024, "Pavlov"),

            new Abiturient("School №1", 2025, "Makarov")
        ));

        Map<Integer, Long> countsByYears = abiturients.stream()
        .collect(Collectors.groupingBy(Abiturient::getYear, Collectors.counting()));

        var maxCount = countsByYears.values().stream().max(Comparator.naturalOrder()).orElse(0L);
        
        System.out.printf("Наибольшее число абитуриентов %d было в годы: \n", maxCount);
        countsByYears.entrySet().stream()
        .filter(e -> e.getValue().equals(maxCount))
        .forEach(el -> {
            System.out.println(el.getKey());
        });
        
        
    }
}