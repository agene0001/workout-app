package com.example.server1;

import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.StdIn;
import edu.princeton.cs.algs4.StdOut;
import edu.princeton.cs.algs4.SuffixArrayX; // Import
import org.springframework.stereotype.Component;

import java.util.*;

@Component
public class Autocomplete {

    private static final int CONTAINS_SEARCH_THRESHOLD = 3; // Search "contains" if len >= this
    private static final char DELIMITER = '\u0001';

    // Keep the original terms sorted for BinarySearchDeluxe prefix search
    private final Term[] terms;

    // Fields for Suffix Array search
    private final SuffixArrayX suffixArray;
    private final String concatenatedText;
    private final int[] termStarts;
    private final Map<Integer, Term> indexToTermMap;
    private final int termCount;

    public Autocomplete(Term[] termsInput) {
        if (termsInput == null) {
            throw new IllegalArgumentException("terms array cannot be null");
        }

        this.termCount = termsInput.length;
        // 1. Store and Sort the original array for BinarySearchDeluxe
        this.terms = new Term[this.termCount];
        for(int i = 0; i < termCount; ++i){
            if(termsInput[i] == null) throw new IllegalArgumentException("Term at index " + i + " is null");
            this.terms[i] = termsInput[i]; // Defensive copy
        }
        try {
            Arrays.sort(this.terms); // Sorts by query (Term's natural order)
        } catch (NullPointerException e) {
            throw new IllegalArgumentException("Null term encountered during sorting");
        }


        // 2. Setup for Suffix Array
        StringBuilder sb = new StringBuilder();
        this.termStarts = new int[this.termCount + 1];
        this.indexToTermMap = new HashMap<>();

        for (int i = 0; i < this.termCount; i++) {
            Term currentTerm = this.terms[i]; // Use the already copied term
            if (currentTerm.getQuery().indexOf(DELIMITER) != -1) {
                throw new IllegalArgumentException("Term query contains delimiter character: " + currentTerm.getQuery());
            }
            this.termStarts[i] = sb.length();
            this.indexToTermMap.put(sb.length(), currentTerm);
            sb.append(currentTerm.getQuery());
            sb.append(DELIMITER);
        }
        this.termStarts[this.termCount] = sb.length();
        this.concatenatedText = sb.toString();
        this.suffixArray = new SuffixArrayX(this.concatenatedText);
    }

    // Binary search helper (same as before)
    private Term findTermFromConcatenatedIndex(int index) {
        int termArrIndex = Arrays.binarySearch(termStarts, index);
        if (termArrIndex < 0) {
            termArrIndex = (-termArrIndex - 1) - 1;
        }
        if (termArrIndex < 0 || termArrIndex >= this.termCount) return null;

        int termStartIndex = termStarts[termArrIndex];
        int termEndIndex = termStarts[termArrIndex + 1];
        if (index >= termStartIndex && index < termEndIndex) {
            return indexToTermMap.get(termStartIndex);
        } else {
            return null;
        }
    }


    // --- MODIFIED allMatches ---
    public Term[] allMatches(String prefix) {
        if (prefix == null) {
            throw new IllegalArgumentException("prefix cannot be null");
        }

        // Use LinkedHashSet to maintain insertion order somewhat and guarantee uniqueness
        Set<Term> uniqueResults = new LinkedHashSet<>();

        // --- Step 1: Always perform the efficient BinarySearchDeluxe prefix search ---
        int len = prefix.length();
        if (len > 0) { // Comparator needs length > 0
            Term prefixTermKey = new Term(prefix, 0); // Dummy term
            Comparator<Term> prefixComparator = Term.byPrefixOrder(len);
            int start = BinarySearchDeluxe.firstIndexOf(this.terms, prefixTermKey, prefixComparator);
            if (start != -1) {
                int end = BinarySearchDeluxe.lastIndexOf(this.terms, prefixTermKey, prefixComparator);
                for (int i = start; i <= end; i++) {
                    uniqueResults.add(this.terms[i]); // Add all prefix matches
                }
            }
        } else {
            // Handle empty prefix? Add all terms? For now, do nothing, maybe suffix search adds all?
        }


        // --- Step 2: Conditionally perform Suffix Array "contains" search ---
        if (len >= CONTAINS_SEARCH_THRESHOLD) {
            System.out.println("DEBUG: Prefix length >= " + CONTAINS_SEARCH_THRESHOLD + ", performing suffix array search for: " + prefix); // Debug
            if (prefix.indexOf(DELIMITER) != -1) {
                System.err.println("Warning: Prefix contains delimiter, suffix search may be unreliable.");
            } else {
                int lo = suffixArray.rank(prefix);
                if (lo < suffixArray.length()) { // Check if rank is valid
                    for (int i = lo; i < suffixArray.length(); i++) {
                        int originalIndexInConcat = suffixArray.index(i);

                        // Optimization: Direct substring check
                        boolean startsWith = false;
                        if (originalIndexInConcat + prefix.length() <= concatenatedText.length()) {
                            startsWith = concatenatedText.substring(originalIndexInConcat, originalIndexInConcat + prefix.length()).equals(prefix);
                            // Add case-insensitivity here if needed: .equalsIgnoreCase(prefix)
                        }

                        if (startsWith) {
                            Term term = findTermFromConcatenatedIndex(originalIndexInConcat);
                            if (term != null) {
                                uniqueResults.add(term); // Add term (Set handles duplicates)
                            }
                        } else {
                            // Suffix array is sorted, no need to check further
                            break;
                        }
                    }
                }
            }
        } else {
            System.out.println("DEBUG: Prefix length < " + CONTAINS_SEARCH_THRESHOLD + ", skipping suffix array search for: " + prefix); // Debug
        }


        // --- Step 3: Convert unique results to array and sort by weight ---
        List<Term> sortedResults = new ArrayList<>(uniqueResults);
        sortedResults.sort(Term.byReverseWeightOrder()); // Sort final list

        return sortedResults.toArray(new Term[0]);
    }

    // numberOfMatches should probably still only count prefix matches for clarity
    public int numberOfMatches(String prefix) {
        if (prefix == null) {
            throw new IllegalArgumentException("prefix cannot be null");
        }
        int len = prefix.length();
        if (len == 0) return this.terms.length; // Or 0?

        Term prefixTerm = new Term(prefix, 0);
        Comparator<Term> comparator = Term.byPrefixOrder(len);

        int start = BinarySearchDeluxe.firstIndexOf(this.terms, prefixTerm, comparator);
        if (start == -1) return 0;
        // Ensure lastIndexOf is also checked correctly
        int end = BinarySearchDeluxe.lastIndexOf(this.terms, prefixTerm, comparator);
        if (end == -1) return 0; // Should not happen if start != -1, but safe check
        return end - start + 1;
    }

    // main method (needs adapting if not run from command line)
    public static void main(String[] args) {
        // ... file reading ...
        String filename = args[0];
        In in = new In(filename);
        int n = in.readInt();
        Term[] terms = new Term[n];
        for (int i = 0; i < n; i++) {
            long weight = in.readLong();
            in.readChar(); // tab
            String query = in.readLine();
            if(query == null) query = "";
            terms[i] = new Term(query.trim(), weight);
        }
        in.close();

        Autocomplete autocomplete = new Autocomplete(terms);
        int k = Integer.parseInt(args[1]);

        while (StdIn.hasNextLine()) {
            String prefix = StdIn.readLine();
            if (prefix == null) break;

            Term[] results = autocomplete.allMatches(prefix);

            // Decide how to report counts - maybe show both?
            int prefixCount = autocomplete.numberOfMatches(prefix);
            StdOut.printf("%d prefix matches found (%d total unique results returned)\n", prefixCount, results.length);

            for (int i = 0; i < Math.min(k, results.length); i++) {
                StdOut.println(results[i]);
            }
        }
    }
}