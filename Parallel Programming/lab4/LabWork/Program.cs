using System;
using CsvHelper;


namespace LabWork;

class Program
{

    public static void Print(List<double> points, char delimiter = ' ')
    {
        foreach (var item in points)
        {
            Console.Write($"{item}{delimiter}");
        }
        Console.WriteLine("\n");
    }

    public static List<double> GenerateArray(int size)
    {
        List<double> array = new List<double>(size);
        for (int i = 0; i < size; i++)
        {
            double value = Random.Shared.Next(11, 11001) / 100.0;
            array.Add(value);
        }

    return array;
    }

    public static double FindMinimumDistance(List<double> points, int threadsCount)
    {
        int n = points.Count;

        double[] result = new double[threadsCount];
        for (int i = 0; i < threadsCount; i++) result[i] = double.PositiveInfinity;
        Thread[] threads = new  Thread[threadsCount];
        int size = (int)Math.Ceiling((double)n / threadsCount);

        for (int t = 0; t < threadsCount; t++) {
            int tCopy = t;
            int start = tCopy * size;
            int end = Math.Min(start + size, n);
            // Print(points[start..end]);

            threads[tCopy] = new Thread(() => {
                double minDist = double.PositiveInfinity;
                for (int i = start; i < end; i++)
                {
                    for (int j = i + 1; j < n; j++)
                    {
                        var dist = Math.Abs(points[i] - points[j]);
                        minDist = Math.Min(dist, minDist);
                    }
                }
                result[tCopy] = minDist;
            });
            threads[t].Start();
        }

        foreach (var t in threads) t.Join();
        double globalMin = double.PositiveInfinity;
        for (int t = 0; t < threadsCount; t++)
            if (result[t] < globalMin) globalMin = result[t];
        return Math.Round(globalMin, 2);
    }

    public static void Main(string[] argv)
    {
        List<List<double>> result = new List<List<double>>();
        int[] Ms = [2, 3, 4, 5, 10];
        int[] Ns = [10, 100, 1000, 100000];
        foreach (int M in Ms)
        {
            List<double> line = [];
            foreach (int N in Ns)
            {
                List<double> array = GenerateArray(N);
                var dist = FindMinimumDistance(array, M);
                line.Add(dist);
            }
        }
    }
}