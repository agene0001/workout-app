package org.backend.utils;

import java.util.Comparator;
import java.util.Objects;

public class Term implements Comparable<Term> {
    private String query;
    private double weight;

    public String getQuery() {
        return query;
    }

    public double getWeight() {
        return weight;
    }

    // Initializes a term with the given query string and weight.
    public Term(String query, double weight) {
        if (query != null || weight >= 0) {
            this.query = query;
            this.weight = weight;
        }
        else {
            throw new IllegalArgumentException("Invalid input");
        }
    }

    // Compares the two terms in descending order by weight.
    public static Comparator<Term> byReverseWeightOrder() {
        return (o1, o2) -> {
            if (o1.weight > o2.weight) {
                return -1;
            }
            else if (o1.weight < o2.weight) {
                return 1;
            }
            else {
                return 0;
            }
        };
    }

    // Compares the two terms in lexicographic order,
    // but using only the first r characters of each query.
    public static Comparator<Term> byPrefixOrder(int r) {
        return (o1, o2) -> {
            String str1 = o1.query.substring(0, Math.min(r, o1.getQuery().length()));
            String str2 = o2.query.substring(0, Math.min(r, o2.getQuery().length()));
            return str1.compareTo(str2);
        };
    }

    // Compares the two terms in lexicographic order by query.
    public int compareTo(Term that) {
        return this.query.compareTo(that.query);
    }

    // Returns a string representation of this term in the following format:
    // the weight, followed by a tab, followed by the query.
    public String toString() {
        return weight + "\t" + query + "\n";
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        Term term = (Term) o;
        return Objects.equals(query, term.query);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(query);
    }

}