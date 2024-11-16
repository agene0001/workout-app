package com.example.server1;

import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.StdIn;
import edu.princeton.cs.algs4.StdOut;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.DefaultResourceLoader;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.net.URL;
import java.util.Arrays;

@Component  // or @Service
public class Autocomplete {

    private Term[] terms;

    // Initializes the data structure from the given array of terms.
    public Autocomplete(Term[] terms) {

        if (terms == null) {
            throw new IllegalArgumentException("terms cannot be null");
        }
        try {
            this.terms = terms;
            Arrays.sort(terms);
//            System.out.println(Arrays.toString(terms));
        }
        catch (NullPointerException e) {
            throw new IllegalArgumentException("terms cannot be null");
        }

    }

    // Returns all terms that start with the given prefix,
    // in descending order of weight.
    public Term[] allMatches(String prefix) {
        if (prefix == null) {
            throw new IllegalArgumentException("prefix cannot be null");
        }
        int len = prefix.length();
        int start = BinarySearchDeluxe.firstIndexOf(terms, new Term(prefix, 1),
                                                    Term.byPrefixOrder(len));
        // if start != -1
        int end = BinarySearchDeluxe.lastIndexOf(terms, new Term(prefix, 1),
                                                 Term.byPrefixOrder(len));
        if (start != -1 && end != -1) {
            if (start == end) {
                return new Term[] { terms[start] };
            }
            Term[] temp1 = Arrays.copyOfRange(terms, start, end);
            Arrays.sort(temp1, Term.byReverseWeightOrder());
            return temp1;
        }
        else {
            throw new IllegalArgumentException("No matches found");
        }
    }

    // Returns the number of terms that start with the given prefix.
    public int numberOfMatches(String prefix) {
        if (prefix == null) {
            throw new IllegalArgumentException("prefix cannot be null");
        }
        int len = prefix.length();
        int start = BinarySearchDeluxe.firstIndexOf(terms, new Term(prefix, 1),
                                                    Term.byPrefixOrder(len));
        int end = BinarySearchDeluxe.lastIndexOf(terms, new Term(prefix, 1),
                                                 Term.byPrefixOrder(len));
        if (start != 1 && end != -1) {
            return end - start + 1;
        }
        else return 0;
    }

    public static Term[] setup(String filename)  {
        try {
            Resource resource = new DefaultResourceLoader().getResource("classpath:static/automation_recipes.csv");
            URL url = resource.getURL();

            In in = new In(url);
            int n = in.readInt();
            Term[] terms = new Term[n];
            for (int i = 0; i < n; i++) {
                float weight = in.readFloat();           // read the next weight
                //            in.readChar();                         // scan past the tab
                String query = in.readLine().toLowerCase().strip();
                // read the next query
                terms[i] = new Term(query, (long) weight);    // construct the term
            }
            return terms;
        }
        catch (IOException e) {
            System.out.println(e.getMessage());
            return null;
        }

    }

    // unit testing (required)
    public static void main(String[] args) {

        // read in the terms from a file
        String filename = args[0];
        In in = new In(filename);
        int n = in.readInt();
        Term[] terms = new Term[n];
        for (int i = 0; i < n; i++) {
            float weight = in.readFloat();           // read the next weight
            in.readChar();                         // scan past the tab
            String query = in.readLine();          // read the next query
            terms[i] = new Term(query, (long) weight);    // construct the term
        }

        // read in queries from standard input and print the top k matching terms
        int k = Integer.parseInt(args[1]);
        ResourceLoader resourceLoader = new org.springframework.core.io.DefaultResourceLoader();

        Autocomplete autocomplete = new Autocomplete(terms);
        // System.out.println(Arrays.toString(terms));
        while (StdIn.hasNextLine()) {
            String prefix = StdIn.readLine();
            Term[] results = autocomplete.allMatches(prefix);
            StdOut.printf("%d matches\n", autocomplete.numberOfMatches(prefix));
            for (int i = 0; i < Math.min(k, results.length); i++)
                StdOut.println(results[i]);
        }
    }


}