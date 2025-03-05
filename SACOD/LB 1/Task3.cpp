#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

void sort(vector<vector<int>> &arr) {
    for (int i = 0; i < arr.size() - 1; i++) {
        for (int j = i; j < arr.size(); j++) {
            if (arr[i][1] > arr[j][1]) {
                swap(arr[i], arr[j]);
            }
        }
    }
    
}

int main()
{
    int nkids;
    do
    {
        std::cout << "Enter number of  kids\n";
        std::cin >> nkids;
    } while (nkids <= 0);
    vector<vector<int>> arr;
    arr.resize(nkids);
    for (int i = 0; i < nkids; i++) {
        arr[i].push_back(i + 1);
        printf("Enter age of %d child: ", i + 1);
        int age;
        do {
            std::cin >> age;
        } while (age <= 0);
        arr[i].push_back(age);
    }
    std::cout << "Kids:\n";while (num.length() != 0) {
    if ((num[num.length() - 1] - '0') >= base) {
      return true;
    }
    num = num.substr(0, num.length() - 1);
  }
  return false;
}

    for (int i = 0; i < arr.size(); i++) {
        for (int j = 0; j < arr[i].size(); j++) {
            printf("%d\t", arr[i][j]);
        }
        std::cout << "\n";
    }
    sort(arr);
    vector<vector<vector<int>>> groups;
    vector<vector<int>> cur_group;
    cur_group.push_back(arr[0]);
    std::cout << "\nGroups:\n";
    for (int i = 1; i < arr.size(); i++) {
        if (abs(arr[i][1] - cur_group.front()[1]) <= 2) {
            std::cout << cur_group.front()[1] << "\n";
            cur_group.push_back(arr[i]);
        }
        else {
            groups.push_back(cur_group);
            cur_group.clear();
            cur_group.push_back(arr[i]);
        }
    }
    if (!cur_group.empty()) {
        groups.push_back(cur_group);
    }
    for (int i = 0; i < groups.size(); i++) {
        std::cout << "Group " << i + 1 << ": ";
        for (int j = 0; j < groups[i].size(); j++) {
            printf("ID: %d, Age: %d  ", groups[i][j][0], groups[i][j][1]);
        }
        std::cout << "\n";
    }

    return 0;
}
