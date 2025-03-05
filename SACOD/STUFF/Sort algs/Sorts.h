#include <vector>
#include <iostream>
#include <cmath>
#include <algorithm>

// Шейкерная сортировка

/////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////

void ShakerSort(std::vector<int> &arr) {
    int n = arr.size();
    int lb = 0; // Нижняя граница
    int ub = n - 1; // Верхняя граница 
    int k = ub; //  Индекс последнего обмена
    // цикл, который производит сортировку справа налево
    while (lb < ub) { //
        for (int j = ub; j > lb; j--) {
            if (arr[j - 1] > arr[j]) {
                int tmp = arr[j - 1];
                arr[j - 1] = arr[j];
                arr[j] = tmp;
                k = j; // Запоминает индекс последнего обмена
            }
        }
        lb = k; // Сужение области сортировки
        for (int j = lb; j < ub; j++) {
            if (arr[j] > arr[j + 1]) {
                int tmp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = tmp;
                k = j; // Индекс последнего обмена
            }
        }
        ub = k; // Сужение области сортировки
    }
}


/////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////

// "Быстрая сортировка"

/////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////

int partision(std::vector<int> &arr, int lb, int ub) {
    int p = lb + (ub - lb) / 2; // Опорный элемент - средний. Здесь находится его индекс
    int pivot = arr[p];
    arr[p] = arr[lb]; // Так как опорный элемент запоминается в pivot - то можно элемент нижней границы сразу поставить на место опорного
    int i = lb + 1; // Т.к. считается, что опорный элемент лежит в arr[lb] - нужно начинать с lb + 1
    int j = ub;
    while (i <= j) {
        if (arr[i] < pivot) { // Т.к. "слева" от опорного элемента должны стоять элементы меньше опорного, то их нужно просто пропускать
            i++;
        }
        else if (arr[j] > pivot) { // Аналогично с правой частью
            j--;
        }
        else { // Если же элемент оказался не в той части, то элементы меняются местами, границы сдвигаются
            int tmp = arr[i];
            arr[i] = arr[j];
            arr[j] = tmp;
            i++;
            j--;
        }
    }
    arr[lb] = arr[j];
    arr[j] = pivot;
    return j;
}

void QuickSort(std::vector<int> &arr, int lb, int ub) {
    int p = partision(arr, lb, ub);
    if (p - 1 > lb) {
        QuickSort(arr, lb, p - 1);
    }
    else if (ub - p > 1) {
        QuickSort(arr, p + 1, ub);
    }
}


/////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////

// Сортировка Выбором

/////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////

void SelectSort(std::vector<int> &arr) {
    for (int i = 0; i < arr.size() - 1; i++) { // Первый цикл, который проходит по всему массиву
        int k = i; // Запоминается индекс первого элемента
        int min = arr[i]; // который и считается за "минимальный"
        for (int j = i + 1; j < arr.size(); j++) { // Считая что все предыдущие элементы уже отсортированы, второй обход выполняется со следующего элемента и до конца
            if (arr[j] < min) { // Если какой-то элемент меньше минимального - то он считается минимальным
                k = j; // Его индекс запоминается в k
                min = arr[j]; // А минимальным становится найденный элемент
            }
        }
        // Как только цикл выполняется до конца, то происходит обмен местами переменных. arr[k] и min это одни и те же значения
        // Потому не надо создавать третью переменную для обмена значений. Таким образом, минимальный элемент встанет в начало, а начальный на его место
        // Таким образом последовательность приходит в отсортировнный вид
        arr[k] = arr[i];
        arr[i] = min;
    }
}

/////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////

// Сортировка Вставками

/////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////

void InsertSort(std::vector<int> &arr) {
    for (int i = 1; i < arr.size(); i++) { // Первичный цикл, который проходит по массиву начиная со второго элемента
        int j = i - 1; // j - для второго цикла. он будет "погружать" элемент. 
        int tmp = arr[i]; // Сохраняется в переменную текущее значение arr[i] т.к. при вставке оно затеряется
        while (j >= 0 && arr[j] > tmp) { // j >= 0 - чтобы не выйти за границу. и пока предыдущие элементы больше текущего - выполняется смещение вперед на один элемент
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = tmp; // а затем последний который сдвинулся станет тем самым сохраненным
    }
}

/////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////

// Сортировка Шелла. Шаги Пратта, Шелла, Кнута и числами Фиббоначчи
/* ДИСКЛЕЙМЕР: Код сделан весьма специфично, и сделано все так, чтобы шелл работал с любыми шагами. Потому шаги генерируются слегка
   странно и всё такое. Особенно для метода Пратта: для сортировки используется сортировка...
   В любом случае, вы всегда можете слегка переписать код, найти лучший алгоритм генерации чисел для шагов, и изменить слегка мой алгоритм.
   Ибо он работает.


*/

/////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////


// Для выбора метода я решил сделать перечисляемый тип
enum Method {
    Knutt,
    Shell,
    Pratt,
    Fibbonacchi
};

// Вспомогательная функция которая переворачивает массив
std::vector<int> reverse(std::vector<int> &arr) {
    std::vector<int> reversed;
    for (int i = arr.size() - 1; i >= 0; i--) {
        reversed.push_back(arr[i]);
    }
    return reversed;
}

// Функция возвращает список шагов для заданного метода
std::vector<int> getSteps(Method method, int n) {
    std::vector<int> steps;
    // Для метода Шелла - просто длина массива делится на 2. Список не разворачивается.
    if (method == Shell) {
        int step = n;
        while (step > 0) {
            steps.push_back(step / 2);
            step /= 2;
        }
    }
    // Для Кнутта - берутся все шаги 3h + 1 меньшие чем n. Здесь массив разворачивается так как порядок обратный
    else if (method == Knutt) {
        int step = 1;
        do {
            steps.push_back(step);
            step = step * 3 + 1;
        } while (step <= n);
        return reverse(steps);
    }
    // Для Пратта - сделано очень глупо, согласен. Но не хотел заморачиваться над сложными формулами генерации. Потому тупой перебор + сортировка и разворот.
    else if (method == Pratt) {
        for (int i = 0; pow(2, i) < n; i++) {
            for (int j = 0; pow(2, i) * pow(3, j) < n; j++) {
                steps.push_back(pow(2, i) * pow(3, j));
            }
        }
        std::sort(steps.begin(), steps.end());
        return reverse(steps);
    }
    // Ну и числа Фиббоначчи - стандартный алгоритм, может в слегка специфичной и обфусцированной реализации
    else if (method == Fibbonacchi) {
        int k = 1;
        steps.push_back(1);
        while (k < n) {
            steps.push_back(k);
            k += steps[steps.size() - 2];
        }
        steps = reverse(steps);
        steps.resize(steps.size() - 1); // Обрезается конец т.к. иначе у нас было бы 2 единицы
        return steps;
    }
    return steps;
}


// Вообще говоря сортировка Шелла это почти как сортировка вставками, только вместо 1 там шаги разные
void ShellSort(std::vector<int> &arr, Method method) {
    int n = arr.size(); // Размер массива. можно обойтись без этой переменной. Я оставил
    int k = 0; // у меня k обозначает шаг. Для универсальности реализации.
    std::vector<int> steps = getSteps(method, n); // Список содержаший все шаги
    // Главный цикл, который требует выполнения до тех пор, пока все шаги не будут пройдены
    while (k != steps.size()) { // Если переделывать, то просто (h >= 1)
        int h = steps[k]; // h - это и есть шаг. Берётся из сформированного ранее списка
        // std::cout << "\n\n\n" << h << "\n\n\n";
        // Первй обход, начиная с шага h и до конца
        for (int i = h; i < arr.size(); i++) {
            int tmp = arr[i]; // Как и во вставках - сохраняется текущий элемент
            int j = i - h; // а вот для второго цикла j = i - h чтобы обойти все ранее стоящие элементы с заданным шагом
            // И пока j >= 0 и элемент под этим индексом больше чем исходный, происходят сдвиги с заданным шагом
            while (j >= 0 && arr[j] > tmp) {
                arr[j + h] = arr[j];
                j -= h;
            }
            arr[j + h] = tmp; // А сохраненный элемент погружается на нужное место
        }
        k++;
        // И затем эти же операции проходят для остальных шагов
    }
}

/////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////

// Сортировка "расчёской"

/////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////

void HairbrushSort(std::vector<int> &arr) {
    const double factor = 1.247; // "Фактор уменьшения". Наиболее оптимально взято значение 1.247. Константное значение. Можете в инете почитать подробнее
    double gapFactor = arr.size() / factor; // А вот шаг берется делением размера на фактор
    while (gapFactor > 1) {
        int gap = round(gapFactor); // Как раз промежуток. Каждый элемент от начала будет сравниваться с этим промежутком, пока j не дойдет до границы массива
        for (int i = 0, j = gap; j < arr.size(); i++, j++) {
            if (arr[i] > arr[j]) {
                std::swap(arr[i], arr[j]); // Перестановка элементов в случае если меньший элемент идет раньше
            }
        }
        gapFactor /= factor; // Каждый раз шаг делится на фактор
    }
}

/////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////

// Блуждающая сортировка.
// TODO: дописать как оно работает.

/////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////

void stoogeSort(std::vector<int> &arr, int l = 0, int h = -1) {
    if (h == -1) {
        h = arr.size() - 1;
    }
    if (l >= h) {
        return;
    }
    if (arr[l] > arr[h]) {
        std::swap(arr[l], arr[h]);
    }

    if (h - l + 1 > 2) {
        int t = (h - l + 1) / 3;
        stoogeSort(arr, l, h - t);
        stoogeSort(arr, l + t, h);
        stoogeSort(arr, l, h - t);
    }
}

/////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////

// Блуждающая сортировка.

/////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////




/////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////