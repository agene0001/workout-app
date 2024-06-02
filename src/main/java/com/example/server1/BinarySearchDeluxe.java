package com.example.server1;
import java.util.ArrayList;
import java.util.Comparator;

public class BinarySearchDeluxe {

    // Returns the index of the first key in the sorted array a[]
    // that is equal to the search key, or -1 if no such key.
    public static <Key> int firstIndexOf(Key[] a, Key key, Comparator<Key> comparator) {
        if (a == null || key == null || comparator == null) {
            throw new IllegalArgumentException();
        }
        int low = 0;
        int high = a.length - 1;
        int mid = (low + high) / 2;
        int cmp = comparator.compare(key, a[mid]);
        // if neg then key is smaller than a[mid]
        // if pos then key is greater than a[mid]
        if (cmp < 0) {
            return binaryHelp(a, key, comparator, low, mid - 1);
        }
        else if (cmp > 0) {
            return binaryHelp(a, key, comparator, mid + 1, high);
        }
        else {
            int ind = 1;
            int temp = comparator.compare(key, a[mid - ind]);
            int val = mid - ind;
            while (temp == 0 && val >= 0) {
                ind++;
                val = mid - ind;
                temp = comparator.compare(key, a[val]);
            }
            return val;
        }

    }

    private static <Key> int binaryHelp(Key[] a, Key key, Comparator<Key> comparator, int low,
                                        int high) {
        if (low < high) {
            int mid = (low + high) / 2;
            int cmp = comparator.compare(key, a[mid]);
            // if neg then key is smaller than a[mid]
            // if pos then key is greater than a[mid]
            // a[546]-a[547]
            if (cmp < 0) {

                return binaryHelp(a, key, comparator, low, mid - 1);
            }
            else if (cmp > 0) {

                return binaryHelp(a, key, comparator, mid + 1, high);
            }
            else {
                int ind = 1;

                int val = mid;
                if (mid - ind > 0) {
                    int temp = comparator.compare(key, a[mid - ind]);
                    while (temp == 0 && mid - ind >= 0) {
                        val = mid - ind;
                        temp = comparator.compare(key, a[val - 1]);
                        ind++;
                    }
                }
                return val;
            }

        }
        else {
            if (comparator.compare(a[low], key) == 0) {
                return low;
            }
            return -1;
        }
    }

    private static <Key> int binaryHelp1(Key[] a, Key key, Comparator<Key> comparator, int low,
                                         int high) {
        if (low < high) {
            int mid = (low + high) / 2;
            int cmp = comparator.compare(key, a[mid]);
            if (cmp < 0) {
                return binaryHelp1(a, key, comparator, low, mid - 1);
            }

            else if (cmp > 0) {

                return binaryHelp1(a, key, comparator, mid + 1, high);
            }
            else {
                int ind = 1;
                int temp = comparator.compare(key, a[mid + ind]);
                int val = mid;
                while (temp == 0 && mid + ind < a.length) {

                    ind++;
                    val = mid + ind;
                    temp = comparator.compare(key, a[val]);
                }
                return val;
            }

        }
        else {
            if (comparator.compare(a[low], key) == 0) {
                return low;
            }
        }
        return -1;

    }

    // Returns the index of the last key in the sorted array a[]
    // that is equal to the search key, or -1 if no such key.
    public static <Key> int lastIndexOf(Key[] a, Key key, Comparator<Key> comparator) {
        if (a == null || key == null || comparator == null) {
            throw new IllegalArgumentException();
        }
        int low = 0;
        int high = a.length - 1;
        int mid = (high + low) / 2;
        int cmp = comparator.compare(key, a[mid]);
        if (cmp < 0) {

            return binaryHelp1(a, key, comparator, low, mid - 1);
        }
        else if (cmp > 0) {
            return binaryHelp1(a, key, comparator, mid + 1, high);
        }
        else {
            int ind = 1;
            int temp = comparator.compare(key, a[mid + ind]);
            int val = mid;
            while (temp == 0 && val != high - 1) {

                ind++;
                val = mid + ind;
                temp = comparator.compare(key, a[val]);
            }
            return val;
        }

    }

    // unit testing (required)
    public static void main(String[] args) {

        ArrayList<Term> terms1 = new ArrayList<>();
        terms1.add(new Term("alex", 1));
        terms1.add(new Term("jamaca", 1));
        terms1.add(new Term("goo", 1));
        terms1.add(new Term("hello", 1));
        terms1.add(new Term("floow", 1));
        terms1.add(new Term("edgar", 1));
        terms1.add(new Term("emily", 1));
        terms1.add(new Term("amber", 1));
        terms1.add(new Term("carter", 1));
        terms1.add(new Term("india", 1));
        terms1.add(new Term("devin", 1));
        terms1.add(new Term("bob", 1));
        terms1.sort(Term::compareTo);
        System.out.println(terms1);
        int t = BinarySearchDeluxe.lastIndexOf(terms1.toArray(new Term[0]),
                                               new Term("e", 1),
                                               Term.byPrefixOrder(1));
        System.out.println(t);
    }
}
