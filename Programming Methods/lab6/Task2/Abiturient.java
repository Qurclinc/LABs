public class Abiturient {
    private String school;
    private Integer year;
    private String surname;

    public Abiturient() {
        this.school = "School №1";
        this.year = 2025;
        this.surname = "Aboba";
    }

    public Abiturient(String school, Integer year, String surname) {
        this.school = school;
        this.year = year;
        this.surname = surname;
    }

    public Abiturient(Abiturient other) {
        this.school = other.getSchool();
        this.year = other.getYear();
        this.surname = other.getSurname();
    }

    public String getSchool() { return this.school; }
    public Integer getYear() { return this.year; }
    public String getSurname() { return this.surname; }
}
