import java.lang.Exception;

public class Person {
    private String surname;
    private Integer flat;
    private Double debt;

    public Person(String surname, Integer flat, Double debt) throws Exception {
        this.surname = surname;
        if (flat < 0 | flat > 144) {
            throw new Exception("Wrong flat");
        }
        this.flat = flat;
        if (debt <= 0D) {
            throw new Exception("Non-positive debt");
        }
        this.debt = debt;
    }

    public String getSurname() { return this.surname; }
    public Integer getFlat() { return this.flat; }
    public Double getDebt() { return this.debt; }
    
    
}
