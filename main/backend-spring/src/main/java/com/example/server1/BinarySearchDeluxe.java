package com.example.server1;

import java.util.ArrayList;
import java.util.Arrays;
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
            return val+1;
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
                if (comparator.compare(key, a[low]) == 0 ) {
                    return low;
                }
                int ind = 1;

                int val = mid;
                int temp = comparator.compare(key, a[mid]);
                while (temp == 0 && mid - ind >= low) {
                    val = mid - ind;
                    temp = comparator.compare(key, a[val]);
                    ind++;
                }


                return val+1;
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
                int temp = comparator.compare(key, a[mid]);
                int val = mid;
                while (temp == 0 && mid + ind < a.length) {

                    val = mid + ind;
                    temp = comparator.compare(key, a[val]);
                    ind++;
                }
                return val-1;
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
            if(val == mid){
                return val;
            }
            return val-1;
        }

    }

    // unit testing (required)
    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Usage: java BinarySearchDeluxe <n>");
            return;
        }

        int n = Integer.parseInt(args[0]);
        Integer[] testArray = new Integer[5 * n];

        // Creating the sorted testArray
        for (int i = 0; i < n; i++) {
            Arrays.fill(testArray, 5 * i, 5 * (i + 1), i + 1);
        }

        // Pick a random key in the range [0, n+1]\
        for(int i=0;i<n;i++) {
            int key = i;

            // Get firstIndexOf and lastIndexOf results using BinarySearchDeluxe methods
            int computedFirst = firstIndexOf(testArray, key, Integer::compare);
            int computedLast = lastIndexOf(testArray, key, Integer::compare);

            // Compute expected results using a brute-force approach
            int expectedFirst = bruteForceFirstIndex(testArray, key);
            int expectedLast = bruteForceLastIndex(testArray, key);

            // Compare and print errors if results do not match
            if (computedFirst != expectedFirst) {
                System.out.println("Error: firstIndexOf failed for key " + key);
                System.out.println("Expected: " + expectedFirst + ", Got: " + computedFirst);
            }
            else {
                System.out.println("first index Test passed for key: " + key);
            }
            if (computedLast != expectedLast) {
                System.out.println("Error: lastIndexOf failed for key " + key);
                System.out.println("Expected: " + expectedLast + ", Got: " + computedLast);
            }
            else {
                System.out.println("last index Test passed for key: " + key);
            }
        }
    }

    // Brute force first index
    private static int bruteForceFirstIndex(Integer[] array, int key) {
        for (int i = 0; i < array.length; i++) {
            if (array[i] == key) return i;
        }
        return -1;
    }

    // Brute force last index
    private static int bruteForceLastIndex(Integer[] array, int key) {
        for (int i = array.length - 1; i >= 0; i--) {
            if (array[i] == key) return i;
        }
        return -1;
    }

}
