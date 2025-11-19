template <class T>
T QuickPow(T x, int n){
    T c = x, f;
    int k = n;
    if (k % 2 == 1) {
        f = c;
    } else {
        f = 1;
    }
    do {
        k /= 2;
        c *= c;
        if (k % 2 == 1) {
            f *= c;
        }
    } while (k != 0);
    return f;
}