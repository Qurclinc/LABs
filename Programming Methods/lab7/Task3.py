def voice_age(age: int) -> str:
    if not (0 <= age <= 100):
        return "Возраст должен быть в диапазоне от 0 до 99."
    result = ""
    if age >= 20:
        match age // 10:
            case 2: result += "двадцать "
            case 3: result += "тридцать "
            case 4: result += "сорок "
            case 5: result += "пятьдесят "
            case 6: result += "шестьдесят "
            case 7: result += "семьдесят "
            case 8: result += "восемьдесят "
            case 9: result += "девяносто "
    elif 10 <= age < 20:
        match age:
            case 10: result += "десять лет"
            case 11: result += "одиннадцать лет"
            case 12: result += "двенадцать лет"
            case 13: result += "тринадцать лет"
            case 14: result += "четырнадцать лет"
            case 15: result += "пятнадцать лет"
            case 16: result += "шестнадцать лет"
            case 17: result += "семнадцать лет"
            case 18: result += "восемнадцать лет"
            case 19: result += "девятнадцать лет"
        return result.strip()
    match age % 10:
        case 0: result += "лет"
        case 1: result += "один год"
        case 2: result += "два года"
        case 3: result += "три года"
        case 4: result += "четыре года"
        case 5: result += "пять лет"
        case 6: result += "шесть лет"
        case 7: result += "семь лет"
        case 8: result += "восемь лет"
        case 9: result += "девять лет"
    return result.strip()

def main():
    age = int(input("Введите возраст: "))
    result = voice_age(age)
    print(result.capitalize())

if __name__ == "__main__":
    main()