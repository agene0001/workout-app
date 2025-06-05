import json

TRAIN_DATA = [
    # Re-annotated data based on the "each word becomes an entity" rule,
    # inheriting labels from original spans, or "O" if not covered.
    # Tokenization based on spaCy's default English tokenizer.
    # Example 1
    ("2 cups flour", {"entities": [
        (0, 1, "QTY"),  # "2"
        (2, 6, "UNIT"),  # "cups"
        (7, 12, "NAME")  # "flour"
    ]}),

    # Example 2
    ("1 large egg", {"entities": [
        (0, 1, "QTY"),  # "1"
        (2, 7, "UNIT"),  # "large"
        (8, 11, "NAME")  # "egg"
    ]}),

    # Example 3
    ("salt", {"entities": [
        (0, 4, "NAME")  # "salt"
    ]}),

    # Example 4
    ("1/2 cup sugar", {"entities": [
        (0, 3, "QTY"),  # "1/2"
        (4, 7, "UNIT"),  # "cup"
        (8, 13, "NAME")  # "sugar"
    ]}),

    # Example 5
    ("1 1/2 tsp vanilla extract", {"entities": [  # Original NAME: (10, 25, "NAME") for "vanilla extract"
        (0, 1, "QTY"),  # "1"        (from original QTY span 0-5)
        (2, 5, "QTY"),  # "1/2"      (from original QTY span 0-5)
        (6, 9, "UNIT"),  # "tsp"
        (10, 17, "NAME"),  # "vanilla"  (from original NAME span 10-25)
        (18, 25, "NAME")  # "extract"  (from original NAME span 10-25)
    ]}),

    # Example 6
    ("One large onion, chopped", {"entities": [  # Original PREP: (17, 24, "PREP") for "chopped"
        (0, 3, "QTY"),  # "One"
        (4, 9, "UNIT"),  # "large"
        (10, 15, "NAME"),  # "onion"
        (15, 16, "O"),  # ","
        (17, 24, "PREP")  # "chopped"
    ]}),

    # Example 7
    ("1/2 cup whole milk", {"entities": [  # Original NAME: (8, 18, "NAME") for "whole milk"
        (0, 3, "QTY"),  # "1/2"
        (4, 7, "UNIT"),  # "cup"
        (8, 13, "NAME"),  # "whole" (from original NAME span 8-18)
        (14, 18, "NAME")  # "milk"  (from original NAME span 8-18)
    ]}),

    # Example 8
    ("4 ounces cream cheese, at room temperature", {"entities": [
        # Original NAME: (9,21,"NAME") for "cream cheese", COMMENT: (23,42,"COMMENT") for "at room temperature"
        (0, 1, "QTY"),  # "4"
        (2, 8, "UNIT"),  # "ounces"
        (9, 14, "NAME"),  # "cream" (from original NAME span 9-21)
        (15, 21, "NAME"),  # "cheese" (from original NAME span 9-21)
        (21, 22, "O"),  # ","
        (23, 42, "COMMENT"),  # "at" (from original COMMENT span 23-42)
    ]}),

    # Example 9
    ("1 cup all-purpose flour", {"entities": [  # Original NAME: (6,23,"NAME") for "all-purpose flour"
        (0, 1, "QTY"),  # "1"
        (2, 5, "UNIT"),  # "cup"
        (6, 17, "NAME"),  # "all-purpose" (from original NAME span 6-23)
        (18, 23, "NAME")  # "flour" (from original NAME span 6-23)
    ]}),

    # Example 10
    ("2 tablespoons unsalted butter, melted", {"entities": [  # Original NAME: (14,29,"NAME") for "unsalted butter"
        (0, 1, "QTY"),  # "2"
        (2, 13, "UNIT"),  # "tablespoons"
        (14, 22, "NAME"),  # "unsalted" (from original NAME span 14-29)
        (23, 29, "NAME"),  # "butter" (from original NAME span 14-29)
        (29, 30, "O"),  # ","
        (31, 37, "PREP")  # "melted"
    ]}),

    # Example 11
    ("1 1/2 cups finely chopped pecans",
     {"entities": [  # Original PREP: (11,17,"PREP") for "finely", NAME: (18,32,"NAME") for "chopped pecans"
         (0, 1, "QTY"),  # "1" (from original QTY span 0-5)
         (2, 5, "QTY"),  # "1/2" (from original QTY span 0-5)
         (6, 10, "UNIT"),  # "cups"
         (11, 17, "PREP"),  # "finely"
         (18, 25, "NAME"),  # "chopped" (from original NAME span 18-32)
         (26, 32, "NAME")  # "pecans" (from original NAME span 18-32)
     ]}),

    # Example 12
    ("1 small bunch swiss chard stems removed leaves chopped",
     {"entities": [  # Original PREP: (26,54,"PREP") for "stems removed leaves chopped"
         (0, 1, "QTY"),  # "1"
         (2, 7, "UNIT"),  # "small"
         (8, 13, "UNIT"),  # "bunch"
         (14, 19, "NAME"),  # "swiss"
         (20, 25, "NAME"),  # "chard"
         (26, 54, "PREP"),  # "stems" (from original PREP span 26-54)
     ]}),

    # Example 13
    ("kosher salt", {"entities": [  # Original NAME: (0,11,"NAME") for "kosher salt"
        (0, 6, "NAME"),  # "kosher" (from original NAME span 0-11)
        (7, 11, "NAME")  # "salt" (from original NAME span 0-11)
    ]}),

    # Example 14
    ("freshly ground pepper", {"entities": [  # Original NAME: (8,21,"NAME") for "ground pepper"
        (0, 7, "PREP"),  # "freshly"
        (8, 14, "NAME"),  # "ground" (from original NAME span 8-21)
        (15, 21, "NAME")  # "pepper" (from original NAME span 8-21)
    ]}),

    # Example 15
    ("1 15-ounce can navy beans undrained", {"entities": [  # Original NAME: (15,25,"NAME") for "navy beans"
        (0, 1, "QTY"),  # "1"
        (2, 10, "COMMENT"),
        # "15-ounce" (assuming this is treated as one token by spaCy for simplicity here, or it'd be "15", "-", "ounce")
        (11, 14, "UNIT"),  # "can"
        (15, 19, "NAME"),  # "navy" (from original NAME span 15-25)
        (20, 25, "NAME"),  # "beans" (from original NAME span 15-25)
        (26, 35, "PREP")  # "undrained"
    ]}),

    # Example 16
    ("Juice of 2 lemons (about 1/4 cup)", {"entities": [
        # Original COMMENT: (18,33,"COMMENT") for "(about 1/4 cup" (missing closing parenthesis in original span)
        (0, 5, "NAME"),  # "Juice"
        (6, 8, "PREP"),  # "of"
        (9, 10, "QTY"),  # "2"
        (11, 17, "NAME"),  # "lemons"
        (18, 33, "COMMENT"),  # "(" (from original COMMENT 18-33)
    ]}),

    # Example 17
    ("About 32 frozen turkey meatballs", {"entities": [  # Original NAME: (16,32,"NAME") for "turkey meatballs"
        (0, 5, "COMMENT"),  # "About"
        (6, 8, "QTY"),  # "32"
        (9, 15, "PREP"),  # "frozen"
        (16, 22, "NAME"),  # "turkey" (from original NAME 16-32)
        (23, 32, "NAME")  # "meatballs" (from original NAME 16-32)
    ]}),

    # Example 18
    ("1 tablespoon mayonnaise", {"entities": [
        (0, 1, "QTY"),  # "1"
        (2, 12, "UNIT"),  # "tablespoon"
        (13, 23, "NAME")  # "mayonnaise"
    ]}),

    # Example 19
    ("2 chipotle peppers in adobo sauce",
     {"entities": [  # Original NAME1: (2,18,"NAME") for "chipotle peppers", NAME2: (22,33,"NAME") for "adobo sauce"
         (0, 1, "QTY"),  # "2"
         (2, 10, "NAME"),  # "chipotle" (from NAME1 2-18)
         (11, 18, "NAME"),  # "peppers" (from NAME1 2-18)
         (19, 21, "O"),  # "in"
         (22, 27, "NAME"),  # "adobo" (from NAME2 22-33)
         (28, 33, "NAME")  # "sauce" (from NAME2 22-33)
     ]}),

    # Example 20
    ("3 tablespoons chopped fresh cilantro", {"entities": [  # Original NAME: (22,36,"NAME") for "fresh cilantro"
        (0, 1, "QTY"),  # "3"
        (2, 13, "UNIT"),  # "tablespoons"
        (14, 21, "PREP"),  # "chopped"
        (22, 27, "PREP"),  # "fresh" (from NAME 22-36)
        (28, 36, "NAME")  # "cilantro" (from NAME 22-36)
    ]}),

    # Example 21
    ("1/2 pint blueberries", {"entities": [
        (0, 3, "QTY"),  # "1/2"
        (4, 8, "UNIT"),  # "pint"
        (9, 20, "NAME")  # "blueberries"
    ]}),

    # Example 22
    ("One 15-ounce loaf challah bread, broken into 2-inch chunks", {"entities": [
        # Original: (0,3,"COMMENT") for "One", (4,12,"COMMENT") for "15-ounce", (13,17,"COMMENT") for "loaf", (18,31,"NAME") for "challah bread", (33,58,"PREP") for "broken into 2-inch chunks"
        (0, 3, "QTY"),  # "One"
        (4, 12, "COMMENT"),  # "15-ounce" (tokenized as one by spaCy typically)
        (13, 17, "COMMENT"),  # "loaf"
        (18, 25, "NAME"),  # "challah" (from NAME 18-31)
        (26, 31, "NAME"),  # "bread" (from NAME 18-31)
        (31, 32, "O"),  # ","
        (33, 58, "PREP"),  # "broken" (from PREP 33-58)
    ]}),

    # Example 23
    ("1 pound bucatoni, cooked al dente", {"entities": [  # Original PREP: (18,33,"PREP") for "cooked al dente"
        (0, 1, "QTY"),  # "1"
        (2, 7, "UNIT"),  # "pound"
        (8, 16, "NAME"),  # "bucatoni"
        (16, 17, "O"),  # ","
        (18, 33, "PREP"),  # "cooked" (from PREP 18-33)
    ]}),

    # Example 24
    ("Alfredo Dipping Sauce",
     {"entities": [  # Original NAME1: (0,7,"NAME") for "Alfredo", NAME2: (8,21,"NAME") for "Dipping Sauce"
         (0, 7, "NAME"),  # "Alfredo"
         (8, 15, "NAME"),  # "Dipping" (from NAME2 8-21)
         (16, 21, "NAME")  # "Sauce" (from NAME2 8-21)
     ]}),

    # Example 25
    ("1 lemon", {"entities": [
        (0, 1, "QTY"),  # "1"
        (2, 7, "NAME")  # "lemon"
    ]}),

    # Example 26
    ("2 cups grated sharp Cheddar",
     {"entities": [  # Original PREP1: (7,13,"PREP") for "grated", PREP2: (14,19,"PREP") for "sharp"
         (0, 1, "QTY"),  # "2"
         (2, 6, "UNIT"),  # "cups"
         (7, 13, "PREP"),  # "grated"
         (14, 19, "PREP"),  # "sharp"
         (20, 27, "NAME")  # "Cheddar"
     ]}),

    # Example 27
    ("1 unbaked Pam's Pie Crust, recipe follows",
     {"entities": [  # Original NAME1: (10,15,"NAME") for "Pam's", NAME2: (16,25,"NAME") for "Pie Crust"
         (0, 1, "QTY"),  # "1"
         (2, 9, "PREP"),  # "unbaked"
         (10, 15, "NAME"),  # "Pam's"
         (16, 19, "NAME"),  # "Pie" (from NAME2 16-25)
         (20, 25, "NAME"),  # "Crust" (from NAME2 16-25)
         (25, 26, "O"),  # ","
         (27, 41, "COMMENT"),  # "recipe" (from COMMENT 27-41)
     ]}),

    # Example 28
    ("20 large (size 16-20) shrimp, peeled and deveined with tail on", {"entities": [
        # Original PREP: (30,62,"PREP") for "peeled and deveined with tail on"
        (0, 2, "QTY"),  # "20"
        (3, 8, "UNIT"),  # "large"
        (9, 21, "COMMENT"),  # "(size 16-20)"
        (22, 28, "NAME"),  # "shrimp"
        (28, 29, "O"),  # ","
        (30, 62, "PREP"),  # "peeled" (from PREP 30-62)
    ]}),

    # Example 29
    ("4 slices lemon, for garnish", {"entities": [
        (0, 1, "QTY"),  # "4"
        (2, 8, "PREP"),  # "slices"
        (9, 14, "NAME"),  # "lemon"
        (14, 15, "O"),  # ","
        (16, 27, "COMMENT"),  # "for" (from COMMENT 16-27)
    ]}),

    # Example 30
    ("1 teaspoon chili paste, or to taste and tolerance", {"entities": [
        # Original NAME: (11,22,"NAME") for "chili paste", COMMENT: (24,49,"COMMENT") for "or to taste and tolerance"
        (0, 1, "QTY"),  # "1"
        (2, 10, "UNIT"),  # "teaspoon"
        (11, 16, "NAME"),  # "chili" (from NAME 11-22)
        (17, 22, "NAME"),  # "paste" (from NAME 11-22)
        (22, 23, "O"),  # ","
        (24, 49, "COMMENT"),  # "or" (from COMMENT 24-49) - *Unusual*
    ]}),

    # Example 31
    ("8 garlic cloves, crushed and finely minced", {"entities": [
        # Original NAME: (2,15,"NAME") for "garlic cloves", PREP: (17,42,"PREP") for "crushed and finely minced"
        (0, 1, "QTY"),  # "8"
        (2, 8, "NAME"),  # "garlic" (from NAME 2-15)
        (9, 15, "NAME"),  # "cloves" (from NAME 2-15)
        (15, 16, "O"),  # ","
        (17, 42, "PREP"),  # "crushed" (from PREP 17-42)
    ]}),

    # Example 32
    ("1/2 cup finely diced angelica, or citron", {"entities": [
        # Original PREP: (8,14,"PREP") for "finely", NAME: (15,29,"NAME") for "diced angelica" (assuming "diced" is part of name here due to original label)
        (0, 3, "QTY"),  # "1/2"
        (4, 7, "UNIT"),  # "cup"
        (8, 14, "PREP"),  # "finely"
        (15, 20, "NAME"),  # "diced" (from NAME 15-29)
        (21, 29, "NAME"),  # "angelica" (from NAME 15-29)
        (29, 30, "O"),  # ","
        (31, 40, "ALT_NAME")  # "citron" (tokenized as one, your original span was exact)
    ]}),

    # Example 33
    ("2 to 3 packages popping rock candy, such as Pop Rocks", {"entities": [
        # Original NAME: (16,34,"NAME") for "popping rock candy", COMMENT: (36,53,"COMMENT") for "such as Pop Rocks"
        (0, 1, "QTY"),  # "2" (from QTY 0-6)
        (2, 6, "COMMENT"),  # "3" (from QTY 0-6)
        (7, 15, "UNIT"),  # "packages"
        (16, 23, "NAME"),  # "popping" (from NAME 16-34)
        (24, 28, "NAME"),  # "rock" (from NAME 16-34)
        (29, 34, "NAME"),  # "candy" (from NAME 16-34)
        (34, 35, "O"),  # ","
        (36, 53, "COMMENT"),  # "such" (from COMMENT 36-53)
    ]}),

    # Example 34
    ("Olives, for garnish", {"entities": [
        (0, 6, "NAME"),  # "Olives"
        (6, 7, "O"),  # ","
        (8, 19, "COMMENT"),  # "for" (from COMMENT 8-19)
    ]}),

    # Example 35
    ("Ice", {"entities": [
        (0, 3, "NAME")  # "Ice"
    ]}),

    # Example 36
    (".5 ounces dry vermouth", {"entities": [  # Original NAME: (10,22,"NAME") for "dry vermouth"
        (0, 2, "QTY"),  # ".5"
        (3, 9, "UNIT"),  # "ounces"
        (10, 13, "NAME"),  # "dry" (from NAME 10-22)
        (14, 22, "NAME")  # "vermouth" (from NAME 10-22)
    ]}),

    # Example 37
    ("Olive or lemon twist for garnish", {"entities": [
        # Original ALT_NAME: (6,20,"ALT_NAME") for "or lemon twist", COMMENT: (21,32,"COMMENT") for "for garnish"
        (0, 5, "NAME"),  # "Olive"
        (6, 20, "ALT_NAME"),  # "or" (from ALT_NAME 6-20) - *Unusual*
        (21, 32, "COMMENT"),  # "for" (from COMMENT 21-32)
    ]}),

    # Example 38
    ("3 scallions, thinly sliced white and green, separated", {"entities": [
        # Original PREP: (13,53,"PREP") for "thinly sliced white and green, separated"
        (0, 1, "QTY"),  # "3"
        (2, 11, "NAME"),  # "scallions"
        (11, 12, "O"),  # ","
        (13, 53, "PREP"),  # "thinly" (from PREP 13-53)
    ]}),

    # Example 39
    ("1 pound peeled and cleaned medium shrimp", {"entities": [
        # Original PREP: (8,26,"PREP") for "peeled and cleaned", NAME: (27,40,"NAME") for "medium shrimp"
        (0, 1, "QTY"),  # "1"
        (2, 7, "UNIT"),  # "pound"
        (8, 14, "PREP"),  # "peeled" (from PREP 8-26)
        (15, 18, "PREP"),  # "and" (from PREP 8-26) - *Unusual*
        (19, 26, "PREP"),  # "cleaned" (from PREP 8-26)
        (27, 33, "NAME"),  # "medium" (from NAME 27-40)
        (34, 40, "NAME")  # "shrimp" (from NAME 27-40)
    ]}),

    # Example 40
    ("1 tablespoon Shao Hsing rice cooking wine, or pale dry sherry", {"entities": [
        # Original NAME1: (13,28,"NAME") for "Shao Hsing rice", NAME2: (29,41,"NAME") for "cooking wine", ALT_NAME: (43,61,"ALT_NAME") for "or pale dry sherry"
        (0, 1, "QTY"),  # "1"
        (2, 12, "UNIT"),  # "tablespoon"
        (13, 23, "NAME"),  # "Shao" (from NAME1 13-28)
        (24, 28, "NAME"),  # "rice" (from NAME1 13-28)
        (29, 36, "NAME"),  # "cooking" (from NAME2 29-41)
        (37, 41, "NAME"),  # "wine" (from NAME2 29-41)
        (43, 61, "ALT_NAME"),  # "or" (from ALT_NAME 43-61) - *Unusual*
    ]}),

    # Example 41
    ("3/4 cup roasted salted cashews (4 ounces)", {"entities": [
        # Original PREP: (8,22,"PREP") for "roasted salted", NAME: (23,30,"NAME") for "cashews"
        (0, 3, "QTY"),  # "3/4"
        (4, 7, "UNIT"),  # "cup"
        (8, 15, "PREP"),  # "roasted" (from PREP 8-22)
        (16, 22, "NAME"),  # "salted" (from PREP 8-22)
        (23, 30, "NAME"),  # "cashews"
        (31, 41, "COMMENT"),  # "("
    ]}),

    # ... (previous examples from your first chunk would be here) ...

    # Example from new chunk (index depends on how many were before)
    ("3.5 ounces vodka or gin", {"entities": [
        # Original NAME: (11,16,"NAME") for "vodka", ALT_NAME: (17,23,"ALT_NAME") for "or gin"
        (0, 3, "QTY"),  # "3.5"
        (4, 10, "UNIT"),  # "ounces"
        (11, 16, "NAME"),  # "vodka"
        (17, 23, "ALT_NAME"),  # "or" (from original ALT_NAME 17-23) - *Unusual*
    ]}),

    # Example
    ("1/2 ounce dry vermouth", {"entities": [
        # Original NAME: (10,22,"NAME") for "dry vermouth"
        (0, 3, "QTY"),  # "1/2"
        (4, 9, "UNIT"),  # "ounce"
        (10, 13, "NAME"),  # "dry" (from original NAME 10-22)
        (14, 22, "NAME")  # "vermouth" (from original NAME 10-22)
    ]}),

    # Example
    ("2 1/2 ounces gin", {"entities": [
        # Original QTY: (0,5,"QTY") for "2 1/2"
        (0, 1, "QTY"),  # "2" (from original QTY 0-5)
        (2, 5, "QTY"),  # "1/2" (from original QTY 0-5)
        (6, 12, "UNIT"),  # "ounces"
        (13, 16, "NAME")  # "gin"
    ]}),

    # Example
    ("1 can (15 ounces) black beans, rinsed and drained", {"entities": [
        # Original QTY1:(0,1,"QTY") "1", UNIT1:(2,5,"UNIT") "can", QTY2:(7,9,"QTY") "15", UNIT2:(10,16,"UNIT") "ounces"
        # NAME:(18,29,"NAME") "black beans", PREP:(31,49,"PREP") "rinsed and drained"
        (0, 1, "QTY"),  # "1"
        (2, 5, "UNIT"),  # "can"
        (6, 17, "COMMENT"),  # "("
        (18, 23, "NAME"),  # "black" (from NAME 18-29)
        (24, 29, "NAME"),  # "beans" (from NAME 18-29)
        (29, 30, "O"),  # ","
        (31, 49, "PREP"),  # "rinsed" (from PREP 31-49)
    ]}),

    # Example
    ("1 large yellow squash about 8 ounces quartered lengthwise and sliced", {"entities": [
        # Original NAME:(8,21,"NAME") "yellow squash", COMMENT:(22,36,"COMMENT") "about 8 ounces", PREP:(37,68,"PREP") "quartered lengthwise and sliced"
        (0, 1, "QTY"),  # "1"
        (2, 7, "UNIT"),  # "large"
        (8, 14, "NAME"),  # "yellow" (from NAME 8-21)
        (15, 21, "NAME"),  # "squash" (from NAME 8-21)
        (22, 36, "COMMENT"),  # "about" (from COMMENT 22-36)
        (37, 68, "PREP"),  # "quartered" (from PREP 37-68)
    ]}),

    # Example
    ("Salt and pepper to taste", {"entities": [
        # Original NAME1:(0,4,"NAME") "Salt", NAME2:(5,8,"O") - wait, "and" is not ent, NAME3:(9,15,"NAME") "pepper", COMMENT:(16,24,"COMMENT") "to taste"
        (0, 4, "NAME"),  # "Salt"
        (5, 8, "O"),  # "and" - (your original had (5,8,"NAME") which would be "and")
        (9, 15, "NAME"),  # "pepper"
        (16, 24, "COMMENT"),  # "to" (from COMMENT 16-24)
    ]}),  # Corrected "and" to "O" as per common sense, unless you explicitly labeled "and" as NAME.

    # Example
    ("chopped parsley", {"entities": [
        # Original NAME: (0,15,"NAME") for "chopped parsley"
        (0, 7, "PREP"),  # "chopped" (from NAME 0-15)
        (8, 15, "NAME")  # "parsley" (from NAME 0-15)
    ]}),

    # Example
    ("2 tablespoons unsalted butter melted cooled plus more for brushing", {"entities": [
        # Original NAME:(14,29,"NAME") "unsalted butter", PREP:(30,43,"PREP") "melted cooled", COMMENT:(44,66,"COMMENT") "plus more for brushing"
        (0, 1, "QTY"),  # "2"
        (2, 13, "UNIT"),  # "tablespoons"
        (14, 22, "NAME"),  # "unsalted" (from NAME 14-29)
        (23, 29, "NAME"),  # "butter" (from NAME 14-29)
        (30, 43, "PREP"),  # "melted" (from PREP 30-43)
        (44, 66, "COMMENT"),  # "plus" (from COMMENT 44-66)
    ]}),

    # Example
    ("20 clams, cleaned", {"entities": [
        (0, 2, "QTY"),  # "20"
        (3, 8, "NAME"),  # "clams"
        (8, 9, "O"),  # ","
        (10, 17, "PREP")  # "cleaned"
    ]}),

    # Example
    ("20 mussels, de-bearded and cleaned", {"entities": [
        # Original PREP:(12,34,"PREP") "de-bearded and cleaned"
        (0, 2, "QTY"),  # "20"
        (3, 10, "NAME"),  # "mussels"
        (10, 11, "O"),  # ","
        (12, 34, "PREP"),  # "de-bearded" (from PREP 12-34)
    ]}),

    # Example
    ("40 small calamari rings, cleaned", {"entities": [
        # Original NAME: (9,23,"NAME") for "calamari rings"
        (0, 2, "QTY"),  # "40"
        (3, 8, "UNIT"),  # "small"
        (9, 17, "NAME"),  # "calamari" (from NAME 9-23)
        (18, 23, "NAME"),  # "rings" (from NAME 9-23)
        (23, 24, "O"),  # ","
        (25, 32, "PREP")  # "cleaned"
    ]}),

    # Example
    ("40 small rings of calamari, cleaned", {"entities": [
        # Original NAME: (9,26,"NAME") for "rings of calamari" - this is odd, "of" usually not NAME.
        (0, 2, "QTY"),  # "40"
        (3, 8, "UNIT"),  # "small"
        (9, 14, "NAME"),  # "rings" (from NAME 9-26)
        (15, 17, "NAME"),  # "of" (from NAME 9-26) - *Highly Unusual*
        (18, 26, "NAME"),  # "calamari" (from NAME 9-26)
        (26, 27, "O"),  # ","
        (28, 35, "PREP")  # "cleaned"
    ]}),

    # Example
    ("4 cups (960 ml) vegetable or chicken broth", {"entities": [
        # Original ALT_NAME:(16,25,"ALT_NAME") "vegetable", NAME:(29,42,"NAME") "chicken broth" (assuming "chicken" was meant as ALT_NAME and "broth" as NAME)
        (0, 1, "QTY"),  # "4"
        (2, 6, "UNIT"),  # "cups"
        (7, 15, "COMMENT"),  # "("
        (16, 25, "NAME"),  # "vegetable"
        (26, 36, "ALT_NAME"),  # "or"
        (37, 42, "NAME")  # "broth" (from original NAME for "chicken broth", so "broth" gets NAME)
    ]}),

    # Example
    ("16 tiger shrimp, peeled and deveined", {"entities": [
        # Original NAME:(3,15,"NAME") "tiger shrimp", PREP:(17,36,"PREP") "peeled and deveined"
        (0, 2, "QTY"),  # "16"
        (3, 8, "NAME"),  # "tiger" (from NAME 3-15)
        (9, 15, "NAME"),  # "shrimp" (from NAME 3-15)
        (15, 16, "O"),  # ","
        (17, 36, "PREP"),  # "peeled" (from PREP 17-36)
    ]}),

    # Example
    ("1/4 cup extra-virgin olive oil", {"entities": [
        # Original NAME:(8,30,"NAME") "extra-virgin olive oil"
        (0, 3, "QTY"),  # "1/4"
        (4, 7, "UNIT"),  # "cup"
        (8, 20, "NAME"),  # "extra-virgin" (from NAME 8-30)
        (21, 26, "NAME"),  # "olive" (from NAME 8-30)
        (27, 30, "NAME")  # "oil" (from NAME 8-30)
    ]}),

    # Example
    ("2 teaspoons chopped garlic", {"entities": [
        # Original NAME:(12,26,"NAME") "chopped garlic"
        (0, 1, "QTY"),  # "2"
        (2, 11, "UNIT"),  # "teaspoons"
        (12, 19, "NAME"),  # "chopped" (from NAME 12-26)
        (20, 26, "NAME")  # "garlic" (from NAME 12-26)
    ]}),

    # Example
    ("1/4 cup italian parsley leaves, divided", {"entities": [
        # Original NAME1:(8,23,"NAME") "italian parsley", NAME2:(24,30,"NAME") "leaves"
        (0, 3, "QTY"),  # "1/4"
        (4, 7, "UNIT"),  # "cup"
        (8, 15, "NAME"),  # "italian" (from NAME1 8-23)
        (16, 23, "NAME"),  # "parsley" (from NAME1 8-23)
        (24, 30, "NAME"),  # "leaves"
        (30, 31, "O"),  # ","
        (32, 39, "PREP")  # "divided"
    ]}),

    # Example
    ("1/8 teaspoon sea salt", {"entities": [
        # Original NAME:(13,21,"NAME") "sea salt"
        (0, 3, "QTY"),  # "1/8"
        (4, 12, "UNIT"),  # "teaspoon"
        (13, 16, "NAME"),  # "sea" (from NAME 13-21)
        (17, 21, "NAME")  # "salt" (from NAME 13-21)
    ]}),

    # Example
    ("1/4 teaspoon crushed red pepper", {"entities": [
        # Original NAME1:(13,20,"NAME") "crushed", NAME2:(21,31,"NAME") "red pepper"
        (0, 3, "QTY"),  # "1/4"
        (4, 12, "UNIT"),  # "teaspoon"
        (13, 20, "NAME"),  # "crushed"
        (21, 24, "NAME"),  # "red" (from NAME2 21-31)
        (25, 31, "NAME")  # "pepper" (from NAME2 21-31)
    ]}),

    # Example
    ("1 cup Pinot Grigio wine", {"entities": [
        # Original NAME:(6,23,"NAME") "Pinot Grigio wine"
        (0, 1, "QTY"),  # "1"
        (2, 5, "UNIT"),  # "cup"
        (6, 11, "NAME"),  # "Pinot" (from NAME 6-23)
        (12, 18, "NAME"),  # "Grigio" (from NAME 6-23)
        (19, 23, "NAME")  # "wine" (from NAME 6-23)
    ]}),

    # Example
    ("2 cups tomato sauce", {"entities": [
        # Original NAME:(7,19,"NAME") "tomato sauce"
        (0, 1, "QTY"),  # "2"
        (2, 6, "UNIT"),  # "cups"
        (7, 13, "NAME"),  # "tomato" (from NAME 7-19)
        (14, 19, "NAME")  # "sauce" (from NAME 7-19)
    ]}),

    # Example
    ("1 (1-pound) box dried spaghetti", {"entities": [
        # Original NAME:(12,31,"NAME") "box dried spaghetti" - this is unusual for box to be NAME. Assuming it's a descriptor or unit.
        # If "box" is unit for "1", and "dried spaghetti" is name.
        # Original (0,1,"QTY"), (3,10,"COMMENT"), (12,31,"NAME")
        (0, 1, "QTY"),  # "1"
        (2, 11, "COMMENT"),  # "("
        (12, 15, "COMMENT"),  # "box" (from NAME 12-31) - *If box is UNIT this is wrong*
        (16, 21, "NAME"),  # "dried" (from NAME 12-31)
        (22, 31, "NAME")  # "spaghetti" (from NAME 12-31)
    ]}),  # This one highly depends on your original intent for "box". If (12,15,"UNIT"), then "box" becomes UNIT.

    # Example
    ("1 (200 g) large leek, cleaned, sliced ¼-inch-(.6 cm) thick", {"entities": [
        # Original COMMENT:(3,9,"COMMENT") "200 g)", UNIT:(10,15,"UNIT") "large", NAME:(16,20,"NAME") "leek", PREP:(22,58,"PREP") "cleaned, sliced ¼-inch-(.6 cm) thick"
        (0, 1, "QTY"),  # "1"
        (3, 9, "COMMENT"),  # "200" (from COMMENT 3-9)
        (10, 15, "UNIT"),  # "large"
        (16, 20, "NAME"),  # "leek"
        (20, 21, "O"),  # ","
        (22, 58, "PREP"),  # "cleaned" (from PREP 22-58)
    ]}),

    # Example
    ("6 cups (335 g) fresh kale, chopped, stems removed", {"entities": [
        # Original COMMENT:(8,14,"COMMENT") "335 g)", NAME:(15,25,"NAME") "fresh kale", PREP:(27,49,"PREP") "chopped, stems removed"
        (0, 1, "QTY"),  # "6"
        (2, 6, "UNIT"),  # "cups"
        (8, 14, "COMMENT"),  # "335" (from COMMENT 8-14)
        (15, 20, "PREP"),  # "fresh" (from NAME 15-25)
        (21, 25, "NAME"),  # "kale" (from NAME 15-25)
        (25, 26, "O"),  # ","
        (27, 49, "PREP"),  # "chopped" (from PREP 27-49)
    ]}),

    # Re-annotated data based on the "each word becomes an entity" rule,
    # inheriting labels from original spans, or "O" if not covered.
    # Tokenization based on spaCy's default English tokenizer.

    # ... (all previous examples from your first and second chunks would be here) ...

    # Example from new chunk (index depends on how many were before)
    ("1 small bunch swiss chard or mustard greens stems removed leaves chopped", {
        # Original NAME1: (14,25,"NAME") "swiss chard", ALT_NAME: (26,43,"ALT_NAME") "or mustard greens", PREP: (44,72,"PREP") "stems removed leaves chopped"
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 7, "UNIT"),  # "small"
            (8, 13, "UNIT"),  # "bunch"
            (14, 19, "NAME"),  # "swiss" (from NAME1 14-25)
            (20, 25, "NAME"),  # "chard" (from NAME1 14-25)
            (26, 43, "ALT_NAME"),  # "or" (from ALT_NAME 26-43) - *Unusual*
            (44, 72, "PREP")]  # "stems" (from PREP 44-72)
    }),

    # Example
    ("4 cups (960 ml) vegetable broth", {"entities": [
        # Original COMMENT:(8,15,"COMMENT") "(960 ml)", NAME:(16,31,"NAME") "vegetable broth"
        (0, 1, "QTY"),  # "4"
        (2, 6, "UNIT"),  # "cups"
        (7, 15, "COMMENT"),  # "("
        (16, 25, "NAME"),  # "vegetable" (from NAME 16-31)
        (26, 31, "NAME")  # "broth" (from NAME 16-31)
    ]}),

    # Example
    ("4 Japanese eggplants, cut in half lengthwise", {"entities": [
        # Original NAME:(2,20,"NAME") "Japanese eggplants", PREP:(22,44,"PREP") "cut in half lengthwise"
        (0, 1, "QTY"),  # "4"
        (2, 10, "NAME"),  # "Japanese" (from NAME 2-20)
        (11, 20, "NAME"),  # "eggplants" (from NAME 2-20)
        (20, 21, "O"),  # ","
        (22, 44, "PREP"),  # "cut" (from PREP 22-44)
    ]}),

    # Example
    ("4 Japanese eggplant, halved lengthwise", {"entities": [
        # Original NAME:(2,19,"NAME") "Japanese eggplant", PREP:(21,38,"PREP") "halved lengthwise"
        (0, 1, "QTY"),  # "4"
        (2, 10, "NAME"),  # "Japanese" (from NAME 2-19)
        (11, 19, "NAME"),  # "eggplant" (from NAME 2-19)
        (19, 20, "O"),  # ","
        (21, 38, "PREP"),  # "halved" (from PREP 21-38)
    ]}),

    # Example
    ("4 Japanese eggplant, sliced lengthwise", {"entities": [
        # Original NAME:(2,19,"NAME") "Japanese eggplant", PREP:(21,38,"PREP") "sliced lengthwise"
        (0, 1, "QTY"),  # "4"
        (2, 10, "NAME"),  # "Japanese" (from NAME 2-19)
        (11, 19, "NAME"),  # "eggplant" (from NAME 2-19)
        (19, 20, "O"),  # ","
        (21, 38, "PREP"),  # "sliced" (from PREP 21-38)
    ]}),

    # Example
    ("1-ounce Rose's lime juice", {
        "entities": [
            # Original NAME1:(8,14,"NAME") "Rose's", NAME2:(15,25,"NAME") "lime juice"
            # Original QTY:(0,1,"QTY") "1", UNIT:(2,7,"UNIT") "ounce"
            (0, 1, "QTY"),  # "1"
            (1, 2, "O"),  # "-" - spaCy might treat "1-ounce" as one token or "1", "-", "ounce"
            (2, 7, "UNIT"),  # "ounce"
            (8, 14, "NAME"),  # "Rose's"
            (15, 19, "NAME"),  # "lime" (from NAME2 15-25)
            (20, 25, "NAME")  # "juice" (from NAME2 15-25)
        ]  # Note: "1-ounce" tokenization can vary. If "1-ounce" is one token (0,7,"UNIT"), then it's (0,7,"UNIT")
        # I'm proceeding as if "1" is QTY and "ounce" is UNIT.
    }),

    # Example
    ("Lemon or lime twist for garnish", {
        "entities": [
            # Original ALT_NAME:(6,19,"ALT_NAME") "or lime twist", COMMENT:(20,31,"COMMENT") "for garnish"
            (0, 5, "NAME"),  # "Lemon
            (6, 13, "ALT_NAME"),  # "lime" (from ALT_NAME 6-19)
            (14, 19, "NAME"),  # "twist" (from ALT_NAME 6-19)
            (20, 31, "COMMENT"),  # "for" (from COMMENT 20-31)
        ]
    }),

    # Example
    ("2 ounces mandarin-orange-flavored vodka", {
        "entities": [
            # Original NAME:(9,39,"NAME") "mandarin-orange-flavored vodka"
            (0, 1, "QTY"),  # "2"
            (2, 8, "UNIT"),  # "ounces"
            (9, 33, "NAME"),  # "mandarin-orange-flavored" (from NAME 9-39, tokenized as one)
            (34, 39, "NAME")  # "vodka" (from NAME 9-39)
        ]
    }),

    # Example
    ("5 tablespoons passion fruit liqueur (reccomended: Alize)", {
        "entities": [
            # Original NAME:(14,35,"NAME") "passion fruit liqueur", COMMENT:(36,56,"COMMENT") "(reccomended: Alize)"
            (0, 1, "QTY"),  # "5"
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, "NAME"),  # "passion" (from NAME 14-35)
            (22, 27, "NAME"),  # "fruit" (from NAME 14-35)
            (28, 35, "NAME"),  # "liqueur" (from NAME 14-35)
            (36, 56, "COMMENT"),  # "("
        ]
    }),

    # Example
    ("2 pounds milk chocolate, tempered", {
        "entities": [
            # Original NAME:(9,23,"NAME") "milk chocolate"
            (0, 1, "QTY"),  # "2"
            (2, 8, "UNIT"),  # "pounds"
            (9, 13, "NAME"),  # "milk" (from NAME 9-23)
            (14, 23, "NAME"),  # "chocolate" (from NAME 9-23)
            (23, 24, "O"),  # ","
            (25, 33, "PREP")  # "tempered"
        ]
    }),

    # Example
    ("Icing (confectioners') sugar, for sprinkling", {
        "entities": [
            # Original COMMENT1:(6,22,"COMMENT") "(confectioners')", NAME2:(23,28,"NAME") "sugar", COMMENT2:(30,44,"COMMENT") "for sprinkling"
            (0, 5, "NAME"),  # "Icing"
            (6, 22, "COMMENT"),  # "("
            (23, 28, "NAME"),  # "sugar"
            (30, 44, "COMMENT"),  # "for" (from COMMENT2 30-44)
        ]
    }),

    # Example
    ("1 head broccoli", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 6, "UNIT"),  # "head"
            (7, 15, "NAME")  # "broccoli"
        ]
    }),

    # Example
    ("Fresh berries and whipped topping, for serving", {
        "entities": [
            # Original NAME1:(0,13,"NAME") "Fresh berries", NAME2:(18,33,"NAME") "whipped topping", PREP:(35,46,"PREP") "for serving"
            (0, 5, "PREP"),  # "Fresh" (from NAME1 0-13)
            (6, 13, "NAME"),  # "berries" (from NAME1 0-13)
            (14, 17, "O"),  # "and"
            (18, 25, "NAME"),  # "whipped" (from NAME2 18-33)
            (26, 33, "NAME"),  # "topping" (from NAME2 18-33)
            (33, 34, "O"),  # ","
            (35, 46, "PREP"),  # "for" (from PREP 35-46) - *Unusual*
        ]
    }),

    # Example
    ("3 cups lemonade", {
        "entities": [
            (0, 1, "QTY"),  # "3"
            (2, 6, "UNIT"),  # "cups"
            (7, 15, "NAME")  # "lemonade"
        ]
    }),

    # Example
    ("4 egg yolks", {
        "entities": [
            # Original NAME:(2,11,"NAME") "egg yolks"
            (0, 1, "QTY"),  # "4"
            (2, 5, "NAME"),  # "egg" (from NAME 2-11)
            (6, 11, "NAME")  # "yolks" (from NAME 2-11)
        ]
    }),

    # Example
    ("1 (15-ounce) box unroll and bake pie crusts (recommended: Pillsbury)", {
        "entities": [
            # Original COMMENT1:(0,1,"COMMENT") "1", QTY:(3,5,"QTY") "15", UNIT:(6,11,"UNIT") "ounce" (Your comment "(15-ounce)" implies (3,11) was maybe one COMMENT or QTY/UNIT combined)
            # COMMENT2:(13,16,"COMMENT") "box", PREP:(17,32,"PREP") "unroll and bake", NAME:(33,43,"NAME") "pie crusts", COMMENT3:(44,68,"COMMENT") "(recommended: Pillsbury)"
            (0, 1, "COMMENT"),  # "1" - Your original says this is COMMENT
            (2, 3, "O"),  # "("
            (3, 5, "QTY"),  # "15"
            (6, 11, "UNIT"),  # "ounce"
            (11, 12, "O"),  # ")"
            (13, 16, "COMMENT"),  # "box" - Your original says this is COMMENT
            (17, 23, "PREP"),  # "unroll" (from PREP 17-32)
            (24, 27, "PREP"),  # "and" (from PREP 17-32) - *Unusual*
            (28, 32, "PREP"),  # "bake" (from PREP 17-32)
            (33, 36, "NAME"),  # "pie" (from NAME 33-43)
            (37, 43, "NAME"),  # "crusts" (from NAME 33-43)
            (44, 67, "COMMENT"),  # "("
        ]
        # This annotation is very sensitive to how "15-ounce" is tokenized and what your original intent for its label was.
    }),

    # Example
    ("1 (4.3-ounce) box lemon pudding mix (recommended: Jell-O cook and serve)", {
        "entities": [
            # Original COMMENT1:(0,1,"COMMENT") "1", QTY:(3,6,"QTY") "4.3", UNIT:(7,12,"UNIT") "ounce", COMMENT2:(14,17,"COMMENT") "box"
            # NAME:(18,35,"NAME") "lemon pudding mix", COMMENT3:(36,72,"COMMENT") "(recommended: Jell-O cook and serve)"
            (0, 1, "COMMENT"),  # "1"
            (2, 3, "O"),  # "("
            (3, 6, "QTY"),  # "4.3"
            (7, 12, "UNIT"),  # "ounce"
            (12, 13, "O"),  # ")"
            (14, 17, "COMMENT"),  # "box"
            (18, 23, "NAME"),  # "lemon" (from NAME 18-35)
            (24, 31, "NAME"),  # "pudding" (from NAME 18-35)
            (32, 35, "NAME"),  # "mix" (from NAME 18-35)
            (36, 72, "COMMENT"),  # "("
        ]
    }),

    # Example
    ("6 ounces bittersweet chocolate", {
        "entities": [
            # Original NAME:(9,30,"NAME") "bittersweet chocolate"
            (0, 1, "QTY"),  # "6"
            (2, 8, "UNIT"),  # "ounces"
            (9, 20, "NAME"),  # "bittersweet" (from NAME 9-30)
            (21, 30, "NAME")  # "chocolate" (from NAME 9-30)
        ]
    }),

    # Example
    ("2 teaspoons finely shredded orange peel", {
        "entities": [
            # Original PREP1:(12,18,"PREP") "finely", PREP2:(19,27,"PREP") "shredded", NAME:(28,39,"NAME") "orange peel"
            (0, 1, "QTY"),  # "2"
            (2, 11, "UNIT"),  # "teaspoons"
            (12, 18, "PREP"),  # "finely"
            (19, 27, "PREP"),  # "shredded"
            (28, 34, "NAME"),  # "orange" (from NAME 28-39)
            (35, 39, "NAME")  # "peel" (from NAME 28-39)
        ]
    }),

    # Example
    ("Four 6-ounce swordfish steaks", {
        "entities": [
            # Original NAME:(13,29,"NAME") "swordfish steaks"
            (0, 4, "QTY"),  # "Four"
            (5, 12, "COMMENT"),  # "6-ounce" (tokenized as one usually)
            (13, 22, "NAME"),  # "swordfish" (from NAME 13-29)
            (23, 29, "NAME")  # "steaks" (from NAME 13-29)
        ]
    }),

    # Example
    ("2 ripe mangoes, peeled and cut into large wedges", {
        "entities": [
            # Original PREP1:(2,6,"PREP") "ripe", NAME:(7,14,"NAME") "mangoes", PREP2:(16,48,"PREP") "peeled and cut into large wedges"
            (0, 1, "QTY"),  # "2"
            (2, 6, "PREP"),  # "ripe"
            (7, 14, "NAME"),  # "mangoes"
            (14, 15, "O"),  # ","
            (16, 48, "PREP"),  # "peeled" (from PREP2 16-48)
        ]
    }),

    # Example
    ("2 bunches scallions, trimmed", {
        "entities": [
            (0, 1, "QTY"),  # "2"
            (2, 9, "UNIT"),  # "bunches"
            (10, 19, "NAME"),  # "scallions"
            (19, 20, "O"),  # ","
            (21, 28, "PREP")  # "trimmed"
        ]
    }),

    # Example
    ("2 Cornish game hens (1 1/2 to 1 3/4 pounds each)", {
        "entities": [
            # Original NAME:(2,19,"NAME") "Cornish game hens", COMMENT:(20,47,"COMMENT") "(1 1/2 to 1 3/4 pounds each)"
            (0, 1, "QTY"),  # "2"
            (2, 9, "NAME"),  # "Cornish" (from NAME 2-19)
            (10, 14, "NAME"),  # "game" (from NAME 2-19)
            (15, 19, "NAME"),  # "hens" (from NAME 2-19)
            (20, 48, "COMMENT"),  # "("
        ]
    }),

    # Example
    ("2 to 3 pounds boneless chicken cut into chunks (I prefer thigh meat)", {
        "entities": [
            # Original QTY:(0,6,"QTY") "2 to 3", NAME:(14,30,"NAME") "boneless chicken", PREP:(31,46,"PREP") "cut into chunks"
            # COMMENT:(47,68,"COMMENT") "(I prefer thigh meat)"
            (0, 1, "QTY"),  # "2" (from QTY 0-6)
            (2, 4, "QTY"),  # "to" (from QTY 0-6) - *Unusual*
            (5, 6, "QTY"),  # "3" (from QTY 0-6)
            (7, 13, "UNIT"),  # "pounds"
            (14, 22, "NAME"),  # "boneless" (from NAME 14-30)
            (23, 30, "NAME"),  # "chicken" (from NAME 14-30)
            (31, 34, "PREP"),  # "cut" (from PREP 31-46)
            (35, 39, "PREP"),  # "into" (from PREP 31-46) - *Unusual*
            (40, 46, "PREP"),  # "chunks" (from PREP 31-46)
            (47, 68, "COMMENT"),  # "("
        ]
    }),

    # Example
    ("Sambal oelek, to taste (hot chili paste from Asian grocery section)", {
        "entities": [
            # Original NAME:(0,12,"NAME") "Sambal oelek", COMMENT1:(14,22,"COMMENT") "to taste"
            # COMMENT2:(23,66,"COMMENT") "(hot chili paste from Asian grocery section)"
            (0, 6, "NAME"),  # "Sambal" (from NAME 0-12)
            (7, 12, "NAME"),  # "oelek" (from NAME 0-12)
            (12, 13, "O"),  # ","
            (14, 16, "COMMENT"),  # "to" (from COMMENT1 14-22)
            (17, 22, "COMMENT"),  # "taste" (from COMMENT1 14-22)
            (23, 67, "COMMENT"),  # "("
        ]
    }),

    # Example
    ("1 large bunch collard or other greens, chopped fairly finely and after removing center ribs (frozen, drained greens can be used as a substitute)",
     {
         "entities": [
             # Original NAME:(14,21,"NAME") "collard", ALT_NAME:(22,37,"ALT_NAME") "or other greens",
             # PREP:(39,91,"PREP") "chopped fairly finely and after removing center ribs"
             # COMMENT:(92,144,"COMMENT") "(frozen, drained greens can be used as a substitute)"
             (0, 1, "QTY"),  # "1"
             (2, 7, "UNIT"),  # "large"
             (8, 13, "UNIT"),  # "bunch"
             (14, 21, "NAME"),  # "collard"
             (22, 37, "ALT_NAME"),  # "or" (from ALT_NAME 22-37) - *Unusual*
             (37, 38, "O"),  # ","
             (39, 91, "PREP"),  # "chopped" (from PREP 39-91)
             (92, 144, "COMMENT"),  # "("
         ]
     }),

    # Example
    ("2 tablespoons reserved spice mixture, from above", {
        "entities": [
            # Original PREP:(14,22,"PREP") "reserved", NAME:(23,36,"NAME") "spice mixture", COMMENT:(38,48,"COMMENT") "from above"
            (0, 1, "QTY"),  # "2"
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 22, "PREP"),  # "reserved"
            (23, 28, "NAME"),  # "spice" (from NAME 23-36)
            (29, 36, "NAME"),  # "mixture" (from NAME 23-36)
            (36, 37, "O"),  # ","
            (38, 48, "COMMENT"),  # "from" (from COMMENT 38-48)
        ]
    }),

    # Example
    ("1/2 cup finely chopped green onions", {
        "entities": [
            # Original PREP:(8,22,"PREP") "finely chopped", NAME:(23,35,"NAME") "green onions"
            (0, 3, "QTY"),  # "1/2"
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "finely" (from PREP 8-22)
            (15, 22, "PREP"),  # "chopped" (from PREP 8-22)
            (23, 28, "NAME"),  # "green" (from NAME 23-35)
            (29, 35, "NAME")  # "onions" (from NAME 23-35)
        ]
    }),

    # Example
    ("2 quarts broth (chicken, pork or veggie)", {
        "entities": [
            # Original COMMENT:(15,39,"COMMENT") "(chicken, pork or veggie)"
            (0, 1, "QTY"),  # "2"
            (2, 8, "UNIT"),  # "quarts"
            (9, 14, "NAME"),  # "broth"
            (15, 40, "COMMENT"),  # "("
        ]
    }),

    # Example
    ("1 leek, washed and halved", {
        "entities": [
            # Original PREP:(8,25,"PREP") "washed and halved"
            (0, 1, "QTY"),  # "1"
            (2, 6, "NAME"),  # "leek"
            (6, 7, "O"),  # ","
            (8, 25, "PREP"),  # "washed" (from PREP 8-25)
        ]
    }),

    # Example
    ("1 leek thinly sliced", {
        "entities": [
            # Original PREP:(7,20,"PREP") "thinly sliced"
            (0, 1, "QTY"),  # "1"
            (2, 6, "NAME"),  # "leek"
            (7, 20, "PREP"),  # "thinly" (from PREP 7-20)
        ]
    }),

    # Example
    ("2 cups chicken or beef stock", {
        "entities": [
            # Original NAME1:(7,14,"NAME") "chicken", ALT_NAME:(15,22,"ALT_NAME") "or beef", NAME2:(23,28,"NAME") "stock"
            (0, 1, "QTY"),  # "2"
            (2, 6, "UNIT"),  # "cups"
            (7, 14, "NAME"),  # "chicken"
            (15, 22, "ALT_NAME"),  # "or" (from ALT_NAME 15-22) - *Unusual*
            (23, 28, "NAME")  # "stock"
        ]
    }),

    # Example
    ("1 tablespoon chopped, fresh chives, plus 1 teaspoon for the sauce", {
        "entities": [
            # Original PREP:(13,20,"PREP") "chopped,", NAME:(22,34,"NAME") "fresh chives" (assuming fresh chives is name)
            # COMMENT:(36,65,"COMMENT") "plus 1 teaspoon for the sauce"
            (0, 1, "QTY"),  # "1"
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 20, "PREP"),  # "chopped" (your original span included comma)
            (20, 21, "PREP"),  # "," (from PREP 13-20) - *Highly Unusual*
            (22, 27, "PREP"),  # "fresh" (from NAME 22-34)
            (28, 34, "NAME"),  # "chives" (from NAME 22-34)
            (34, 35, "O"),  # ","
            (36, 65, "COMMENT"),  # "plus" (from COMMENT 36-65)
        ]
    }),

    # Example
    ("1 tablespoon chopped, fresh thyme leaves, plus 1 teaspoon for the sauce", {
        "entities": [
            # Original PREP:(13,20,"PREP") "chopped,", NAME:(22,40,"NAME") "fresh thyme leaves"
            # COMMENT:(42,71,"COMMENT") "plus 1 teaspoon for the sauce"
            (0, 1, "QTY"),  # "1"
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 20, "PREP"),  # "chopped" (original included comma)
            (20, 21, "PREP"),  # "," (from PREP 13-20) - *Highly Unusual*
            (22, 27, "PREP"),  # "fresh" (from NAME 22-40)
            (28, 33, "NAME"),  # "thyme" (from NAME 22-40)
            (34, 40, "NAME"),  # "leaves" (from NAME 22-40)
            (40, 41, "O"),  # ","
            (42, 71, "COMMENT"),  # "plus" (from COMMENT 42-71)
        ]
    }),

    # Example
    ("1 tablespoon chopped, fresh Italian parsley, plus 1 teaspoon for the sauce", {
        "entities": [
            # Original PREP:(13,20,"PREP") "chopped,", NAME:(22,43,"NAME") "fresh Italian parsley"
            # COMMENT:(45,74,"COMMENT") "plus 1 teaspoon for the sauce"
            (0, 1, "QTY"),  # "1"
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 20, "PREP"),  # "chopped" (original included comma)
            (20, 21, "PREP"),  # "," (from PREP 13-20) - *Highly Unusual*
            (22, 27, "PREP"),  # "fresh" (from NAME 22-43)
            (28, 35, "NAME"),  # "Italian" (from NAME 22-43)
            (36, 43, "NAME"),  # "parsley" (from NAME 22-43)
            (45, 74, "COMMENT"),  # "plus" (from COMMENT 45-74)
        ]
    }),

    # Example
    ("1 tablespoon freshly ground black pepper", {
        "entities": [
            # Original PREP:(13,27,"PREP") "freshly ground", NAME:(28,40,"NAME") "black pepper"
            (0, 1, "QTY"),  # "1"
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 20, "PREP"),  # "freshly" (from PREP 13-27)
            (21, 27, "PREP"),  # "ground" (from PREP 13-27)
            (28, 33, "NAME"),  # "black" (from NAME 28-40)
            (34, 40, "NAME")  # "pepper" (from NAME 28-40)
        ]
    }),

    # Example
    ("1/2 pound ground pork (Don't get lean pork, the fat is good for juicy and flavorful dumplings)", {
        "entities": [
            # Original PREP:(10,21,"PREP") "ground pork" (assuming ground is prep, pork is name) - or if (10,21,"NAME")
            # COMMENT:(22,94,"COMMENT") "(Don't get lean pork, the fat is good for juicy and flavorful dumplings)"
            (0, 3, "QTY"),  # "1/2"
            (4, 9, "UNIT"),  # "pound"
            (10, 16, "PREP"),  # "ground" (from PREP 10-21)
            (17, 21, "PREP"),
            # "pork" (from PREP 10-21) - *If "pork" is NAME, this is wrong. Depends on original label for (10,21)*
            (22, 94, "COMMENT"),  # "("
        ]
        # This is highly dependent on how "ground pork" was originally labeled. If (10,21,"NAME"), then "ground" and "pork" become NAME.
    }),

    # Example
    ("1 tablespoon (42 grams) honey", {
        "entities": [
            # Original COMMENT:(13,23,"COMMENT") "(42 grams)"
            (0, 1, "QTY"),  # "1"
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 14, "O"),  # "("
            (14, 16, "COMMENT"),  # "42" (from COMMENT 13-23)
            (17, 22, "COMMENT"),  # "grams" (from COMMENT 13-23)
            (22, 23, "O"),  # ")"
            (24, 29, "NAME")  # "honey"
        ]
    }),

    # Example
    ("Sea salt and freshly ground black pepper", {
        "entities": [
            # Original NAME1:(0,8,"NAME") "Sea salt", PREP:(13,27,"PREP") "freshly ground", NAME2:(28,40,"NAME") "black pepper"
            (0, 3, "NAME"),  # "Sea" (from NAME1 0-8)
            (4, 8, "NAME"),  # "salt" (from NAME1 0-8)
            (9, 12, "O"),  # "and"
            (13, 20, "PREP"),  # "freshly" (from PREP 13-27)
            (21, 27, "PREP"),  # "ground" (from PREP 13-27)
            (28, 33, "NAME"),  # "black" (from NAME2 28-40)
            (34, 40, "NAME")  # "pepper" (from NAME2 28-40)
        ]
    }),

    # Example
    ("2 cups leftover spaghetti with olives and tomato sauce, recipe follows", {
        "entities": [
            # Original PREP1:(7,15,"PREP") "leftover", NAME1:(16,25,"NAME") "spaghetti", PREP2:(26,30,"PREP") "with"
            # NAME2:(31,37,"NAME") "olives", PREP3:(38,41,"PREP") "and", NAME3:(42,54,"NAME") "tomato sauce" (your notes say tomato here)
            # COMMENT:(56,70,"COMMENT") "recipe follows"
            (0, 1, "QTY"),  # "2"
            (2, 6, "UNIT"),  # "cups"
            (7, 15, "PREP"),  # "leftover"
            (16, 25, "NAME"),  # "spaghetti"
            (26, 54, "ALT_NAME"),  # "with"
            (54, 55, "O"),  # ","
            (56, 70, "COMMENT"),  # "recipe" (from COMMENT 56-70)
        ]
    }),

    # Example
    ("1/2 tablespoon red pepper flakes, plus more if desired", {
        "entities": [
            # Original NAME:(15,32,"NAME") "red pepper flakes", COMMENT:(34,54,"COMMENT") "plus more if desired"
            (0, 3, "QTY"),  # "1/2"
            (4, 14, "UNIT"),  # "tablespoon"
            (15, 18, "NAME"),  # "red" (from NAME 15-32)
            (19, 25, "NAME"),  # "pepper" (from NAME 15-32)
            (26, 32, "NAME"),  # "flakes" (from NAME 15-32)
            (32, 33, "O"),  # ","
            (34, 54, "COMMENT"),  # "plus" (from COMMENT 34-54)
        ]
    }),

    # Example
    ("1/2 small bulb of fennel, halved, cored and thinly sliced into half-moons (about 1 cup)", {
        "entities": [
            # Original UNIT1:(4,9,"UNIT") "small", NAME:(10,24,"NAME") "bulb of fennel" (assuming "bulb of fennel")
            # PREP:(26,73,"PREP") "halved, cored and thinly sliced into half-moons"
            # COMMENT:(74,87,"COMMENT") "(about 1 cup)"
            (0, 3, "QTY"),  # "1/2"
            (4, 9, "UNIT"),  # "small"
            (10, 14, "NAME"),  # "bulb" (from NAME 10-24)
            (15, 17, "NAME"),  # "of" (from NAME 10-24) - *Highly Unusual*
            (18, 24, "NAME"),  # "fennel" (from NAME 10-24)
            (24, 25, "O"),  # ","
            (26, 73, "PREP"),  # "halved" (from PREP 26-73)
            (74, 87, "COMMENT"),  # "("
        ]
    }),

    # Example
    ("3/4 cup sliced almonds, coarsely chopped", {
        "entities": [
            # Original PREP1:(8,14,"PREP") "sliced", NAME:(15,22,"NAME") "almonds", PREP2:(24,40,"PREP") "coarsely chopped"
            (0, 3, "QTY"),  # "3/4"
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "sliced"
            (15, 22, "NAME"),  # "almonds"
            (22, 23, "O"),  # ","
            (24, 32, "PREP"),  # "coarsely" (from PREP2 24-40)
            (33, 40, "PREP")  # "chopped" (from PREP2 24-40)
        ]
    }),

    # Example
    ("1/2 teaspoon ground caraway", {
        "entities": [
            # Original PREP:(13,19,"PREP") "ground", NAME:(20,27,"NAME") "caraway"
            (0, 3, "QTY"),  # "1/2"
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 19, "PREP"),  # "ground"
            (20, 27, "NAME")  # "caraway"
        ]
    }),

    # Example
    ("6 slices center cut bacon", {
        "entities": [
            # Original PREP:(2,19,"PREP") "slices center cut"
            (0, 1, "QTY"),  # "6"
            (2, 8, "PREP"),  # "slices" (from PREP 2-19)
            (9, 15, "PREP"),  # "center" (from PREP 2-19)
            (16, 19, "PREP"),  # "cut" (from PREP 2-19)
            (20, 25, "NAME")  # "bacon"
        ]
    }),

    # Example
    ("16 cups, plus 1 cup water", {
        "entities": [
            # Original COMMENT:(9,25,"COMMENT") "plus 1 cup water"
            (0, 2, "QTY"),  # "16"
            (3, 7, "UNIT"),  # "cups"
            (7, 8, "O"),  # ","
            (9, 13, "COMMENT"),  # "plus" (from COMMENT 9-25)
            (14, 15, "COMMENT"),  # "1" (from COMMENT 9-25)
            (16, 19, "COMMENT"),  # "cup" (from COMMENT 9-25)
            (20, 25, "COMMENT")  # "water" (from COMMENT 9-25)
        ]
    }),

    # Example
    ("4 carrots", {"entities": [(0, 1, "QTY"), (2, 9, "NAME")]}),
    # Example
    ("3 onions", {"entities": [(0, 1, "QTY"), (2, 8, "NAME")]}),
    # Example
    ("2 large leeks", {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "NAME")]}),

    # Example
    ("4 celery stalks", {
        "entities": [
            # Original NAME:(2,15,"NAME") "celery stalks"
            (0, 1, "QTY"),  # "4"
            (2, 8, "NAME"),  # "celery" (from NAME 2-15)
            (9, 15, "NAME")  # "stalks" (from NAME 2-15)
        ]
    }),

    # Example
    ("1 whole turkey breast, approximately 1 1/2 to 2 pounds", {
        "entities": [
            # Original PREP:(2,7,"PREP") "whole", NAME:(8,21,"NAME") "turkey breast"
            # COMMENT:(23,54,"COMMENT") "approximately 1 1/2 to 2 pounds"
            (0, 1, "QTY"),  # "1"
            (2, 7, "PREP"),  # "whole"
            (8, 14, "NAME"),  # "turkey" (from NAME 8-21)
            (15, 21, "NAME"),  # "breast" (from NAME 8-21)
            (21, 22, "O"),  # ","
            (23, 54, "COMMENT"),  # "approximately" (from COMMENT 23-54)
        ]
    }),

    # Example
    ("2/3 tablespoon marjoram", {
        "entities": [
            (0, 3, "QTY"),  # "2/3"
            (4, 14, "UNIT"),  # "tablespoon"
            (15, 23, "NAME")  # "marjoram"
        ]
    }),

    # Example
    ("Generous pinch coarsely ground black pepper", {
        "entities": [
            # Original QTY:(0,8,"QTY") "Generous", COMMENT:(9,14,"COMMENT") "pinch" (pinch as comment is odd, usually unit/qty part)
            # PREP:(15,30,"PREP") "coarsely ground", NAME:(31,43,"NAME") "black pepper"
            (0, 8, "QTY"),  # "Generous"
            (9, 14, "COMMENT"),  # "pinch"
            (15, 23, "PREP"),  # "coarsely" (from PREP 15-30)
            (24, 30, "PREP"),  # "ground" (from PREP 15-30)
            (31, 36, "NAME"),  # "black" (from NAME 31-43)
            (37, 43, "NAME")  # "pepper" (from NAME 31-43)
        ]
    }),

    # Example
    ("1/4 cup sliced almonds, toasted, for garnish", {
        "entities": [
            # Original PREP1:(8,14,"PREP") "sliced", NAME:(15,22,"NAME") "almonds", PREP2:(24,31,"PREP") "toasted"
            # COMMENT:(33,44,"COMMENT") "for garnish"
            (0, 3, "QTY"),  # "1/4"
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "sliced"
            (15, 22, "NAME"),  # "almonds"
            (22, 23, "O"),  # ","
            (24, 31, "PREP"),  # "toasted"
            (31, 32, "O"),  # ","
            (33, 44, "COMMENT"),  # "for" (from COMMENT 33-44)
        ]
    }),

    # Example
    ("7 ounces (1 3/4 sticks) butter, softened, plus 1 tablespoon for greasing the loaf pan", {
        "entities": [
            # Original COMMENT1:(9,23,"COMMENT") "(1 3/4 sticks)", NAME:(24,30,"NAME") "butter", PREP:(32,40,"PREP") "softened"
            # COMMENT2:(42,85,"COMMENT") "plus 1 tablespoon for greasing the loaf pan"
            (0, 1, "QTY"),  # "7"
            (2, 8, "UNIT"),  # "ounces"
            (9, 10, "O"),  # "("
            (10, 11, "COMMENT"),  # "1" (from COMMENT1 9-23)
            (12, 15, "COMMENT"),  # "3/4" (from COMMENT1 9-23)
            (16, 22, "COMMENT"),  # "sticks" (from COMMENT1 9-23)
            (22, 23, "O"),  # ")"
            (24, 30, "NAME"),  # "butter"
            (30, 31, "O"),  # ","
            (32, 40, "PREP"),  # "softened"
            (40, 41, "O"),  # ","
            (42, 85, "COMMENT"),  # "plus" (from COMMENT2 42-85)
        ]
    }),

    # Example
    ("2/3 cup sliced almonds, toasted", {
        "entities": [
            # Original PREP1:(8,14,"PREP") "sliced", NAME:(15,22,"NAME") "almonds", PREP2:(24,31,"PREP") "toasted"
            (0, 3, "QTY"),  # "2/3"
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "sliced"
            (15, 22, "NAME"),  # "almonds"
            (22, 23, "O"),  # ","
            (24, 31, "PREP")  # "toasted"
        ]
    }),

    # Example
    ("1 cup shredded smoked gouda", {
        "entities": [
            # Original PREP:(6,14,"PREP") "shredded", NAME:(15,27,"NAME") "smoked gouda"
            (0, 1, "QTY"),  # "1"
            (2, 5, "UNIT"),  # "cup"
            (6, 14, "PREP"),  # "shredded"
            (15, 21, "NAME"),  # "smoked" (from NAME 15-27)
            (22, 27, "NAME")  # "gouda" (from NAME 15-27)
        ]
    }),

    # Example
    ("1 bunch watercress, stemmed", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 7, "UNIT"),  # "bunch"
            (8, 18, "NAME"),  # "watercress"
            (18, 19, "O"),  # ","
            (20, 27, "PREP")  # "stemmed"
        ]
    }),

    # Example
    ("1 head radicchio, chopped", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 6, "UNIT"),  # "head"
            (7, 16, "NAME"),  # "radicchio"
            (16, 17, "O"),  # ","
            (18, 25, "PREP")  # "chopped"
        ]
    }),

    # Example
    ("1 teaspoon chopped oregano leaves", {
        "entities": [
            # Original PREP:(11,18,"PREP") "chopped", NAME:(19,33,"NAME") "oregano leaves"
            (0, 1, "QTY"),  # "1"
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 18, "PREP"),  # "chopped"
            (19, 26, "NAME"),  # "oregano" (from NAME 19-33)
            (27, 33, "NAME")  # "leaves" (from NAME 19-33)
        ]
    }),

    # Example
    ("1 large loaf of Cuban bread, cut into 4 equal pieces crosswise", {
        "entities": [
            # Original UNIT1:(2,7,"UNIT") "large", NAME:(8,27,"NAME") "loaf of Cuban bread", PREP:(29,62,"PREP") "cut into 4 equal pieces crosswise"
            (0, 1, "QTY"),  # "1"
            (2, 7, "UNIT"),  # "large"
            (8, 12, "NAME"),  # "loaf" (from NAME 8-27)
            (13, 15, "NAME"),  # "of" (from NAME 8-27) - *Highly Unusual*
            (16, 21, "NAME"),  # "Cuban" (from NAME 8-27)
            (22, 27, "NAME"),  # "bread" (from NAME 8-27)
            (27, 28, "O"),  # ","
            (29, 62, "PREP"),  # "cut" (from PREP 29-62)
        ]
    }),

    # Example
    ("1 teaspoon freshly ground canela (cinnamon)", {
        "entities": [
            # Original PREP:(11,18,"PREP") "freshly", NAME:(19,32,"NAME") "ground canela" (assuming ground canela, or ground is PREP)
            # COMMENT:(33,43,"COMMENT") "(cinnamon)"
            (0, 1, "QTY"),  # "1"
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 18, "PREP"),  # "freshly"
            (19, 25, "NAME"),  # "ground" (from NAME 19-32)
            (26, 32, "NAME"),  # "canela" (from NAME 19-32)
            (33, 43, "COMMENT"),  # "("
        ]
    }),

    # Example
    ("2 tablespoons ground cumin", {
        "entities": [
            # Original NAME:(14,26,"NAME") "ground cumin"
            (0, 1, "QTY"),  # "2"
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 20, "NAME"),  # "ground" (from NAME 14-26)
            (21, 26, "NAME")  # "cumin" (from NAME 14-26)
        ]
    }),

    # Example
    ("1 teaspoon oregano, dried", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 18, "NAME"),  # "oregano"
            (18, 19, "O"),  # ","
            (20, 25, "PREP")  # "dried"
        ]
    }),

    # Example
    ("1 avocado, peeled and cubed", {
        "entities": [
            # Original PREP:(11,27,"PREP") "peeled and cubed"
            (0, 1, "QTY"),  # "1"
            (2, 9, "NAME"),  # "avocado"
            (9, 10, "O"),  # ","
            (11, 17, "PREP"),  # "peeled" (from PREP 11-27)
            (18, 21, "PREP"),  # "and" (from PREP 11-27) - *Unusual*
            (22, 27, "PREP")  # "cubed" (from PREP 11-27)
        ]
    }),

    # Example
    ("1 ear corn, kernels removed and roasted until some of the kernels start to brown", {
        "entities": [
            # Original PREP:(12,80,"PREP") "kernels removed and roasted until some of the kernels start to brown"
            (0, 1, "QTY"),  # "1"
            (2, 5, "UNIT"),  # "ear"
            (6, 10, "NAME"),  # "corn"
            (10, 11, "O"),  # ","
            (12, 80, "PREP"),  # "kernels" (from PREP 12-80)
        ]
    }),

    # Example
    ("12 cornichons", {"entities": [(0, 2, "QTY"), (3, 13, "NAME")]}),

    # Example
    ("12 slider buns", {"entities": [
        # Original NAME1:(3,9,"NAME") "slider", NAME2:(10,14,"NAME") "buns"
        (0, 2, "QTY"),  # "12"
        (3, 9, "NAME"),  # "slider"
        (10, 14, "NAME")  # "buns"
    ]}),

    # Example
    ("About 1 pound (500g) farmed ground New Zealand venison (any cut will do but the most cost effective is from the leg)",
     {
         "entities": [
             # Original COMMENT1:(0,5,"COMMENT") "About", QTY:(6,7,"QTY") "1", UNIT:(8,13,"UNIT") "pound",
             # COMMENT2:(14,20,"COMMENT") "(500g)", PREP:(21,34,"PREP") "farmed ground" (assuming farmed ground)
             # NAME:(35,54,"NAME") "New Zealand venison", COMMENT3:(55,116,"COMMENT") "(any cut...)"
             (0, 5, "COMMENT"),  # "About"
             (6, 7, "QTY"),  # "1"
             (8, 13, "UNIT"),  # "pound"
             (14, 15, "O"),  # "("
             (15, 19, "COMMENT"),  # "500g" (from COMMENT2 14-20, tokenized as one)
             (19, 20, "O"),  # ")"
             (21, 27, "PREP"),  # "farmed" (from PREP 21-34)
             (28, 34, "PREP"),  # "ground" (from PREP 21-34)
             (35, 38, "NAME"),  # "New" (from NAME 35-54)
             (39, 46, "NAME"),  # "Zealand" (from NAME 35-54)
             (47, 54, "NAME"),  # "venison" (from NAME 35-54)
             (55, 116, "COMMENT"),  # "("
         ]
     }),

    # Example
    ("1 thumb fresh ginger, peeled and grated", {
        "entities": [
            # Original COMMENT:(2,7,"COMMENT") "thumb", NAME:(8,20,"NAME") "fresh ginger", PREP:(22,39,"PREP") "peeled and grated"
            (0, 1, "QTY"),  # "1"
            (2, 7, "COMMENT"),  # "thumb"
            (8, 13, "PREP"),  # "fresh" (from NAME 8-20)
            (14, 20, "NAME"),  # "ginger" (from NAME 8-20)
            (20, 21, "O"),  # ","
            (22, 39, "PREP"),  # "peeled" (from PREP 22-39)
        ]
    }),

    # Example (Duplicate 1)
    ("1 teaspoon ground cumin", {"entities": [
        # Original NAME:(11,23,"NAME") "ground cumin"
        (0, 1, "QTY"), (2, 10, "UNIT"), (11, 17, "NAME"), (18, 23, "NAME")
    ]}),
    # Example (Duplicate 2)
    ("1 tablespoon cumin", {"entities": [
        (0, 1, "QTY"), (2, 12, "UNIT"), (13, 18, "NAME")
    ]}),

    # Example
    ("1 sprig thyme", {
        "entities": [
            # Original PREP:(2,7,"PREP") "sprig"
            (0, 1, "QTY"),  # "1"
            (2, 7, "PREP"),  # "sprig"
            (8, 13, "NAME")  # "thyme"
        ]
    }),

    # Example
    ("3 shallots, slice thin", {
        "entities": [
            # Original PREP:(12,22,"PREP") "slice thin"
            (0, 1, "QTY"),  # "3"
            (2, 10, "NAME"),  # "shallots"
            (10, 11, "O"),  # ","
            (12, 17, "PREP"),  # "slice" (from PREP 12-22)
            (18, 22, "PREP")  # "thin" (from PREP 12-22)
        ]
    }),

    # Example
    ("5 1/2 pounds bones and trimmings from white fish", {
        "entities": [
            # Original QTY:(0,5,"QTY") "5 1/2", PREP:(13,37,"PREP") "bones and trimmings from", NAME:(38,48,"NAME") "white fish"
            (0, 1, "QTY"),  # "5" (from QTY 0-5)
            (2, 5, "QTY"),  # "1/2" (from QTY 0-5)
            (6, 12, "UNIT"),  # "pounds"
            (13, 48, "PREP"),  # "bones" (from PREP 13-37)
        ]
    }),

    # Example
    ("1 pound large shrimp, peeled and deveined, tails left on", {
        "entities": [
            # Original NAME:(8,20,"NAME") "large shrimp", PREP:(22,56,"PREP") "peeled and deveined, tails left on"
            (0, 1, "QTY"),  # "1"
            (2, 7, "UNIT"),  # "pound"
            (8, 13, "NAME"),  # "large" (from NAME 8-20)
            (14, 20, "NAME"),  # "shrimp" (from NAME 8-20)
            (20, 21, "O"),  # ","
            (22, 56, "PREP"),  # "peeled" (from PREP 22-56)
        ]
    }),

    # Example
    ("1 tablespoon toasted fennel seed", {
        "entities": [
            # Original PREP:(13,20,"PREP") "toasted", NAME:(21,32,"NAME") "fennel seed"
            (0, 1, "QTY"),  # "1"
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 20, "PREP"),  # "toasted"
            (21, 27, "NAME"),  # "fennel" (from NAME 21-32)
            (28, 32, "NAME")  # "seed" (from NAME 21-32)
        ]
    }),

    # Example (Duplicate)
    ("1 head fennel", {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 13, "NAME")]}),

    # Example
    ("1/2 pound clam base", {
        "entities": [
            # Original NAME:(10,19,"NAME") "clam base"
            (0, 3, "QTY"),  # "1/2"
            (4, 9, "UNIT"),  # "pound"
            (10, 14, "NAME"),  # "clam" (from NAME 10-19)
            (15, 19, "NAME")  # "base" (from NAME 10-19)
        ]
    }),

    # Example
    ("3 (46-ounce) cans clam juice", {
        "entities": [
            # Original COMMENT:(2,12,"COMMENT") "(46-ounce)", NAME:(18,28,"NAME") "clam juice"
            (0, 1, "QTY"),  # "3"
            (2, 3, "O"),  # "("
            (3, 11, "COMMENT"),  # "46-ounce" (from COMMENT 2-12, tokenized as one)
            (11, 12, "O"),  # ")"
            (13, 17, "UNIT"),  # "cans"
            (18, 22, "NAME"),  # "clam" (from NAME 18-28)
            (23, 28, "NAME")  # "juice" (from NAME 18-28)
        ]
    }),

    # Example (Duplicate)
    ("7 onions", {"entities": [(0, 1, "QTY"), (2, 8, "NAME")]}),

    # Example
    ("4 small clams or 3 large clams", {
        "entities": [
            (0, 1, "QTY"),         # "4"
            (2, 7, "UNIT"),        # "small"
            (8, 13, "NAME"),       # "clams"
            # "or" (14,16) is O or implicitly handled by the presence of ALT_QTY/ALT_UNIT
            (17, 18, "ALT_QTY"),   # "3"
            (19, 24, "ALT_UNIT"),  # "large"
            (25, 30, "ALT_NAME")   # "clams" (specifies the item for the alternative QTY/UNIT)
        ]
    }),

    # Example
    ("2 ounces crabmeat or 3 crab legs", {
        "entities": [
            (0, 1, "QTY"),         # "2"
            (2, 8, "UNIT"),        # "ounces"
            (9, 17, "NAME"),       # "crabmeat"
            # "or" (18,20) is O or implicitly handled
            (21, 22, "ALT_QTY"),   # "3" (quantity for the alternative item)
            (23, 32, "ALT_NAME"),  # "crab"
        ]
    }),

    # Example (Duplicate)
    ("2 tablespoons chopped oregano leaves",
     {"entities": [  # PREP:(14,21,"PREP") "chopped", NAME:(22,36,"NAME") "oregano leaves"
         (0, 1, "QTY"), (2, 13, "UNIT"), (14, 21, "PREP"), (22, 29, "NAME"), (30, 36, "NAME")
     ]}),

    # Example
    ("4 quenelle scoops of coconut ice cream (If coconut ice cream is not available, fold toasted coconut, 1 tablespoon Malabu Rum, with softened vanilla ice cream)",
     {
         "entities": [
             # Original PREP:(2,20,"PREP") "quenelle scoops of", NAME:(21,38,"NAME") "coconut ice cream"
             # COMMENT:(39,158,"COMMENT") "(If coconut...ice cream)"
             (0, 1, "QTY"),  # "4"
             (2, 10, "PREP"),  # "quenelle" (from PREP 2-20)
             (11, 17, "PREP"),  # "scoops" (from PREP 2-20)
             (18, 20, "PREP"),  # "of" (from PREP 2-20) - *Unusual*
             (21, 28, "NAME"),  # "coconut" (from NAME 21-38)
             (29, 32, "NAME"),  # "ice" (from NAME 21-38)
             (33, 38, "NAME"),  # "cream" (from NAME 21-38)
             (39, 158, "COMMENT"),  # "("
         ]
     }),

    # Example
    ("Juice of one lemon", {
        "entities": [
            # Original NAME1:(0,5,"NAME") "Juice", PREP:(6,8,"PREP") "of", QTY:(9,12,"QTY") "one", NAME2:(13,18,"NAME") "lemon"
            (0, 5, "NAME"),  # "Juice"
            (6, 8, "PREP"),  # "of"
            (9, 12, "QTY"),  # "one"
            (13, 18, "NAME")  # "lemon"
        ]
    }),

    # Example
    ("3 tablespoons small diced quava", {
        "entities": [
            # Original PREP:(14,19,"PREP") "small", NAME:(20,31,"NAME") "diced quava" (assuming "diced quava" based on label)
            (0, 1, "QTY"),  # "3"
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 19, "PREP"),  # "small"
            (20, 25, "NAME"),  # "diced" (from NAME 20-31)
            (26, 31, "NAME")  # "quava" (from NAME 20-31)
        ]
    }),

    # Example
    ("3 tablespoons small diced pineapple", {
        "entities": [
            # Original PREP:(14,19,"PREP") "small", NAME:(20,35,"NAME") "diced pineapple"
            (0, 1, "QTY"),  # "3"
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 19, "PREP"),  # "small"
            (20, 25, "NAME"),  # "diced" (from NAME 20-35)
            (26, 35, "NAME")  # "pineapple" (from NAME 20-35)
        ]
    }),

    # Example
    ("3 tablespoons small diced mango", {
        "entities": [
            # Original PREP:(14,19,"PREP") "small", NAME:(20,31,"NAME") "diced mango"
            (0, 1, "QTY"),  # "3"
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 19, "PREP"),  # "small"
            (20, 25, "NAME"),  # "diced" (from NAME 20-31)
            (26, 31, "NAME")  # "mango" (from NAME 20-31)
        ]
    }),

    # Example
    ("3 tablespoons small diced papayas", {
        "entities": [
            # Original PREP:(14,19,"PREP") "small", NAME:(20,33,"NAME") "diced papayas"
            (0, 1, "QTY"),  # "3"
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 19, "PREP"),  # "small"
            (20, 25, "NAME"),  # "diced" (from NAME 20-33)
            (26, 33, "NAME")  # "papayas" (from NAME 20-33)
        ]
    }),

    # Example
    ("12 cold, freshly opened oysters", {
        "entities": [
            # Original PREP:(3,23,"PREP") "cold, freshly opened"
            (0, 2, "QTY"),  # "12"
            (3, 7, "PREP"),  # "cold" (from PREP 3-23)
            (7, 8, "PREP"),  # "," (from PREP 3-23) - *Highly Unusual*
            (9, 16, "PREP"),  # "freshly" (from PREP 3-23)
            (17, 23, "PREP"),  # "opened" (from PREP 3-23)
            (24, 31, "NAME")  # "oysters"
        ]
    }),

    # Example
    ("About 4 ounces top-quality smoked salmon, sliced extremely thinly", {
        "entities": [
            # Original COMMENT:(0,5,"COMMENT") "About", PREP1:(15,26,"PREP") "top-quality", NAME:(27,40,"NAME") "smoked salmon"
            # PREP2:(42,65,"PREP") "sliced extremely thinly"
            (0, 5, "COMMENT"),  # "About"
            (6, 7, "QTY"),  # "4"
            (8, 14, "UNIT"),  # "ounces"
            (15, 26, "PREP"),  # "top-quality" (tokenized as one)
            (27, 33, "NAME"),  # "smoked" (from NAME 27-40)
            (34, 40, "NAME"),  # "salmon" (from NAME 27-40)
            (40, 41, "O"),  # ","
            (42, 65, "PREP"),  # "sliced" (from PREP2 42-65)
        ]
    }),

    # Example (Duplicate)
    ("12 cold, freshly opened oysters", {"entities": [  # PREP:(3,23,"PREP")
        (0, 2, "QTY"), (3, 7, "PREP"), (7, 8, "PREP"), (9, 16, "PREP"), (17, 23, "PREP"), (24, 31, "NAME")
    ]}),

    # Example
    ("1 fresh jalapeno, diced, half seeded and deveined", {
        "entities": [
            # Original PREP1:(2,7,"PREP") "fresh", NAME:(8,16,"NAME") "jalapeno", PREP2:(18,49,"PREP") "diced, half seeded and deveined"
            (0, 1, "QTY"),  # "1"
            (2, 7, "PREP"),  # "fresh"
            (8, 16, "NAME"),  # "jalapeno"
            (16, 17, "O"),  # ","
            (18, 49, "PREP"),  # "diced" (from PREP2 18-49)
        ]
    }),

    # Example
    ("1 tablespoon plus 1 teaspoon garlic powder", {
        "entities": [
            # Original COMMENT:(13,28,"COMMENT") "plus 1 teaspoon", NAME:(29,42,"NAME") "garlic powder"
            (0, 1, "QTY"),  # "1"
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 28, "COMMENT"),  # "plus" (from COMMENT 13-28)
            (29, 35, "NAME"),  # "garlic" (from NAME 29-42)
            (36, 42, "NAME")  # "powder" (from NAME 29-42)
        ]
    }),

    # Example
    ("1/4 cup kimchi, drained and coarsely chopped", {
        "entities": [
            # Original PREP:(16,44,"PREP") "drained and coarsely chopped"
            (0, 3, "QTY"),  # "1/4"
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "NAME"),  # "kimchi"
            (14, 15, "O"),  # ","
            (16, 44, "PREP"),  # "drained" (from PREP 16-44)
        ]
    }),

    # Example
    ("1/4 cup apple cider", {
        "entities": [
            # Original NAME:(8,19,"NAME") "apple cider"
            (0, 3, "QTY"),  # "1/4"
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "NAME"),  # "apple" (from NAME 8-19)
            (14, 19, "NAME")  # "cider" (from NAME 8-19)
        ]
    }),

    # Example
    ("2 Roma tomatoes", {
        "entities": [
            # Original NAME:(2,15,"NAME") "Roma tomatoes"
            (0, 1, "QTY"),  # "2"
            (2, 6, "NAME"),  # "Roma" (from NAME 2-15)
            (7, 15, "NAME")  # "tomatoes" (from NAME 2-15)
        ]
    }),

    # Example
    ("1/4 cup fresh squeezed orange juice", {
        "entities": [
            # Original PREP:(8,22,"PREP") "fresh squeezed", NAME:(23,35,"NAME") "orange juice"
            (0, 3, "QTY"),  # "1/4"
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "PREP"),  # "fresh" (from PREP 8-22)
            (14, 22, "PREP"),  # "squeezed" (from PREP 8-22)
            (23, 29, "NAME"),  # "orange" (from NAME 23-35)
            (30, 35, "NAME")  # "juice" (from NAME 23-35)
        ]
    }),

    # Example
    ("1/4 cup beer", {
        "entities": [
            (0, 3, "QTY"),  # "1/4"
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "NAME")  # "beer"
        ]
    }),

    # Re-annotated data based on the REFINED rules:
    # - NAME entities are broken into word-level NAME entities.
    # - COMMENT, PREP, ALT_NAME entities are kept as single, original spans.
    # - QTY, UNIT are generally single words; if an original span was multi-word, it's broken down.
    # - Commas and other non-entity words become "O" (and are thus not listed in the 'entities' list).
    # Tokenization based on spaCy's default English tokenizer.

    ("One 8-inch sub roll or long roll, split", {  # Corrected based on likely intent for "sub roll"
        "entities": [
            (0, 3, "QTY"),  # "One"
            (4, 10, "COMMENT"),  # "8-inch"
            (11, 14, "NAME"),  # "sub"
            (15, 19, "NAME"),  # "roll"
            (20, 32, "ALT_NAME"),  # "or long roll"
            # Comma at 32 is "O"
            (34, 39, "PREP")  # "split"
        ]
    }),

    # Example 2
    ("6 feet all-natural hog casings", {
        "entities": [
            (0, 1, "QTY"),  # "6"
            (2, 6, "COMMENT"),  # "feet"
            (7, 18, "PREP"),  # "all-natural" (Kept as original span)
            (19, 22, "NAME"),  # "hog" (from original NAME "hog casings" 19-30)
            (23, 30, "NAME")  # "casings" (from original NAME "hog casings" 19-30)
        ]
    }),

    # Example 3
    ("2 cups shredded mozzarella", {
        "entities": [
            (0, 1, "QTY"),  # "2"
            (2, 6, "UNIT"),  # "cups"
            (7, 15, "PREP"),  # "shredded" (Kept as original span)
            (16, 26, "NAME")  # "mozzarella"
        ]
    }),

    # Example 4
    # My re-annotation should then be:
    ("One 24-ounce jar marinara sauce", {  # Corrected based on your original for 24-ounce
        "entities": [
            (0, 3, "COMMENT"),  # "One"
            (4, 6, "QTY"),  # "24"
            (7, 12, "UNIT"),  # "ounce"
            (13, 16, "COMMENT"),  # "jar"
            (17, 25, "NAME"),  # "marinara"
            (26, 31, "NAME")  # "sauce"
        ]
    }),

    # Example 5
    ("One 16-ounce box mezzi rigatoni or mezze penne", {
        "entities": [
            (0, 3, "COMMENT"),  # "One"
            (4, 6, "QTY"),  # "16"
            (7, 12, "UNIT"),  # "ounce"
            (13, 16, "COMMENT"),  # "box"
            (17, 22, "NAME"),  # "mezzi" (from original NAME "mezzi rigatoni" 17-31)
            (23, 31, "NAME"),  # "rigatoni" (from original NAME "mezzi rigatoni" 17-31)
            (32, 46, "ALT_NAME")  # "or mezze penne" (Kept as original span)
        ]
    }),

    # Example 6
    (".5 oz simple syrup", {
        "entities": [
            (0, 2, "QTY"),  # ".5"
            (3, 5, "UNIT"),  # "oz"
            (6, 12, "NAME"),  # "simple" (from original NAME "simple syrup" 6-18)
            (13, 18, "NAME")  # "syrup" (from original NAME "simple syrup" 6-18)
        ]
    }),

    # Example 7
    ("1 large carrot, chopped", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 7, "UNIT"),  # "large"
            (8, 14, "NAME"),  # "carrot"
            # Comma at 14 is "O"
            (16, 23, "PREP")  # "chopped" (Kept as original span)
        ]
    }),

    # Example 8
    ("1 cup half-and-half", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 5, "UNIT"),  # "cup"
            (6, 19, "NAME")  # "half-and-half" (spaCy usually tokenizes this as one, so it remains one NAME entity)
            # If spaCy tokenized it as "half", "-", "and", "-", "half", then it would be:
            # (6,10,"NAME"), (10,11,"NAME"), (11,14,"NAME"), (14,15,"NAME"), (15,19,"NAME")
            # For simplicity, assuming "half-and-half" is one token here.
        ]
    }),

    # Example 9
    ("3/4 cup shredded part-skim mozzarella cheese", {
        "entities": [
            (0, 3, "QTY"),  # "3/4"
            (4, 7, "UNIT"),  # "cup"
            (8, 26, "PREP"),
            # "shredded part-skim" (Kept as original span. Your original span was (8,26,"PREP") for "shredded part-skim")
            # If (8,16,"PREP") for "shredded" and (17,26,"PREP") for "part-skim", it'd be two PREP entities.
            # Assuming (8,26,"PREP") was for the whole phrase.
            (27, 37, "NAME"),  # "mozzarella" (from original NAME "mozzarella cheese" 27-44)
            (38, 44, "NAME")  # "cheese" (from original NAME "mozzarella cheese" 27-44)
        ]
    }),

    # Example 10
    ("1 small shallot, peeled, trimmed and halved", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 7, "UNIT"),  # "small"
            (8, 15, "NAME"),  # "shallot"
            # Comma at 15 is "O"
            (17, 43, "PREP")  # "peeled, trimmed and halved" (Kept as original span)
        ]
    }),

    # Example 11
    ("1 small garlic clove, peeled, trimmed and halved", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 7, "UNIT"),  # "small"
            (8, 14, "NAME"),  # "garlic" (from original NAME "garlic clove" 8-20)
            (15, 20, "NAME"),  # "clove" (from original NAME "garlic clove" 8-20)
            # Comma at 20 is "O"
            (22, 48, "PREP"),  # "peeled, trimmed and halved" (Kept as original span)
        ]
    }),

    # Example 12
    ("1/2 teaspoon saffron threads", {
        "entities": [
            (0, 3, "QTY"),  # "1/2"
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 20, "NAME"),  # "saffron" (from original NAME "saffron threads" 13-28)
            (21, 28, "NAME")  # "threads" (from original NAME "saffron threads" 13-28)
        ]
    }),

    # Example 13
    ("1 (5 to 6 pound) leg of lamb, trimmed of excess fat", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 16, "COMMENT"),  # "(5 to 6 pound)" (Kept as original span)
            (17, 20, "NAME"),  # "leg" (from original NAME "leg of lamb" 17-28)
            (21, 23, "NAME"),  # "of" (from original NAME "leg of lamb" 17-28) - *Unusual for "of" to be NAME*
            (24, 28, "NAME"),  # "lamb" (from original NAME "leg of lamb" 17-28)
            # Comma at 28 is "O"
            (30, 51, "PREP")  # "trimmed of excess fat" (Kept as original span)
        ]
    }),

    # Example 14
    ("1 tablespoon fresh oregano, chopped fine", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 18, "PREP"),  # "fresh" (Kept as original PREP span. This implies "fresh" itself is the prep)
            (19, 26, "NAME"),  # "oregano"
            # Comma at 26 is "O"
            (28, 40, "PREP")  # "chopped fine" (Kept as original span)
        ]
    }),

    # Example 15
    ("Pinch cayenne", {
        "entities": [
            (0, 5, "COMMENT"),  # "Pinch" (Original label was COMMENT)
            (6, 13, "NAME")  # "cayenne"
        ]
    }),  # Your alternative "(0,5,"QTY")" would make "Pinch" a QTY. I'm following the first one.

    # Example 16
    ("8 ounces tomatillo, papery husks removed, cut into 1/4-inch dice", {
        "entities": [
            (0, 1, "QTY"),  # "8"
            (2, 8, "UNIT"),  # "ounces"
            (9, 18, "NAME"),  # "tomatillo"
            # Comma at 18 is "O"
            (20, 64, "PREP")  # "papery husks removed, cut into 1/4-inch dice" (Kept as original span)
            # This is a very long PREP span.
        ]
    }),

    # Example 17
    ("2 tablespoons pitted and finely chopped kalamata olives", {
        "entities": [
            (0, 1, "QTY"),  # "2"
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 39, "PREP"),  # "pitted and finely chopped" (Kept as original span)
            (40, 48, "NAME"),  # "kalamata" (from original NAME "kalamata olives" 40-55)
            (49, 55, "NAME")  # "olives" (from original NAME "kalamata olives" 40-55)
        ]
    }),

    # Example 18
    ("1 tablespoon each vegetable and sesame oil", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 17, "COMMENT"),  # "each" (Kept as original span)
            (18, 27, "NAME"),  # "vegetable" (from original NAME "vegetable and sesame oil" 18-42)
            (28, 38, "ALT_NAME"),  # "sesame" (from original NAME "vegetable and sesame oil" 18-42)
            (39, 42, "NAME")  # "oil" (from original NAME "vegetable and sesame oil" 18-42)
        ]
    }),

    # Example 19
    ("1 tablespoon plus 2 teaspoons cornstarch", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 29, "COMMENT"),  # "plus 2 teaspoons" (Kept as original span)
            (30, 40, "NAME")  # "cornstarch"
        ]
    }),

    # Example 20
    ("1 tablespoon plus 1 teaspoon soy sauce", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 28, "COMMENT"),  # "plus 1 teaspoon" (Kept as original span)
            (29, 32, "NAME"),  # "soy" (from original NAME "soy sauce" 29-38)
            (33, 38, "NAME")  # "sauce" (from original NAME "soy sauce" 29-38)
        ]
    }),

    # Example 21
    ("Pinch crushed red pepper", {
        "entities": [
            (0, 5, "COMMENT"),  # "Pinch" (Original label was COMMENT)
            (6, 13, "NAME"),  # "crushed" (from original NAME "crushed red pepper" 6-24)
            (14, 17, "NAME"),  # "red" (from original NAME "crushed red pepper" 6-24)
            (18, 24, "NAME")  # "pepper" (from original NAME "crushed red pepper" 6-24)
        ]
    }),

    # Example 22
    ("Pinch sugar", {
        "entities": [
            (0, 5, "COMMENT"),  # "Pinch" (Original label was COMMENT)
            (6, 11, "NAME")  # "sugar"
        ]
    }),

    # Example 23
    ("1 tablespoon plus 1 teaspoon vegetable oil", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 28, "COMMENT"),  # "plus 1 teaspoon" (Kept as original span)
            (29, 38, "NAME"),  # "vegetable" (from original NAME "vegetable oil" 29-42)
            (39, 42, "NAME")  # "oil" (from original NAME "vegetable oil" 29-42)
        ]
    }),

    # Example 24
    ("1 medium carrot, thinly sliced", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 8, "UNIT"),  # "medium"
            (9, 15, "NAME"),  # "carrot"
            # Comma at 15 is "O"
            (17, 30, "PREP")  # "thinly sliced" (Kept as original span)
        ]
    }),

    # Example 25
    ("1 bunch scallions, sliced, white and green parts kept separate", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 7, "UNIT"),  # "bunch"
            (8, 17, "NAME"),  # "scallions"
            # Comma at 17 is "O"
            (19, 25, "PREP"),  # "sliced" (Kept as original span)
            # Comma at 25 is "O"
            (27, 62, "COMMENT")  # "white and green parts kept separate" (Kept as original span)
        ]
    }),

    # Example 26
    ("2 teaspoons green peppercorns* (See Cook's Note", {  # Assuming asterisk is part of name or comment
        "entities": [
            (0, 1, "QTY"),  # "2"
            (2, 11, "UNIT"),  # "teaspoons"
            (12, 17, "NAME"),  # "green" (from original NAME "green peppercorns*" 12-30)
            (18, 30, "NAME"),  # "peppercorns*" (from original NAME "green peppercorns*" 12-30, includes *)
            (31, 47, "COMMENT")  # "(See Cook's Note" (Kept as original span, note it's missing closing parenthesis)
        ]
    }),

    # Example 27
    ("1 cup seeded and chopped plum tomatoes", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 5, "UNIT"),  # "cup"
            (6, 24, "PREP"),  # "seeded and chopped" (Kept as original span)
            (25, 29, "NAME"),  # "plum" (from original NAME "plum tomatoes" 25-38)
            (30, 38, "NAME")  # "tomatoes" (from original NAME "plum tomatoes" 25-38)
        ]
    }),

    # Example 28
    ("2 quarts water", {
        "entities": [
            (0, 1, "QTY"),  # "2"
            (2, 8, "UNIT"),  # "quarts"
            (9, 14, "NAME")  # "water"
        ]
    }),

    # Example 29
    ("1/4 cup half-and-half", {
        "entities": [
            (0, 3, "QTY"),  # "1/4"
            (4, 7, "UNIT"),  # "cup"
            (8, 21, "NAME")  # "half-and-half" (tokenized as one, so remains one NAME)
        ]
    }),

    # Example 30
    ("1 teaspoon Szechwan peppercorns or 1/2 teaspoon cardamom seeds", {
        "entities": [
            (0, 1, "QTY"),         # "1"
            (2, 10, "UNIT"),       # "teaspoon" (for Szechwan peppercorns)
            (11, 19, "NAME"),      # "Szechwan"
            (20, 31, "NAME"),      # "peppercorns"
            # "or" (32,34) is O or implicitly handled
            (35, 38, "ALT_QTY"),   # "1/2" (quantity for the alternative)
            (39, 47, "ALT_UNIT"),  # "teaspoon" (unit for the alternative)
            (48, 62, "ALT_NAME"),  # "cardamom" (alternative ingredient name part)
        ]
    }),

    # Example 31
    ("2 ducks, about 5 pounds each, cavities cleaned, excess fat trimmed, rinsed and patted dry", {
        "entities": [
            (0, 1, "QTY"),  # "2"
            (2, 7, "NAME"),  # "ducks"
            # Comma at 7 is "O"
            (9, 28, "COMMENT"),  # "about 5 pounds each" (Kept as original span)
            # Comma at 28 is "O"
            (30, 89, "PREP")  # "cavities cleaned, excess fat trimmed, rinsed and patted dry" (Kept as original span)
        ]
    }),

    # Example 32
    ("1/2 teaspoon sumac", {
        "entities": [
            (0, 3, "QTY"),  # "1/2"
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 18, "NAME")  # "sumac"
        ]
    }),

    # Example 33
    ("1 medium red onion", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 8, "UNIT"),  # "medium"
            (9, 12, "NAME"),  # "red"
            (13, 18, "NAME")  # "onion"
        ]
    }),

    # Example 34
    ("1 3-pound chicken, butterflied and lightly pounded for even thickness", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 9, "COMMENT"),  # "3-pound" (Kept as original span)
            (10, 17, "NAME"),  # "chicken"
            # Comma at 17 is "O"
            (19, 69, "PREP"),  # "butterflied" (Original span was (19,30,"PREP"))
        ]
    }),

    # Example 35
    ("1 head garlic, cloves separated and peeled", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 6, "UNIT"),  # "head"
            (7, 13, "NAME"),  # "garlic"
            # Comma at 13 is "O"
            (15, 35, "PREP")  # "cloves separated and peeled" (Kept as original span)
        ]
    }),

    # Example 36 (Duplicate)
    ("7 cups water", {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 12, "NAME")]}),

    # Example 37
    ("1 1/4 ounces cornstarch", {
        "entities": [
            (0, 5, "QTY"),  # "1" (from original QTY "1 1/4" 0-5)\
            (6, 12, "UNIT"),  # "ounces"
            (13, 23, "NAME")  # "cornstarch"
        ]
    }),

    # Example 38
    ("1 1/2 cups cornstarch", {
        "entities": [
            (0, 5, "QTY"),  # "1" (from original QTY "1 1/2" 0-5)
            (6, 10, "UNIT"),  # "cups"
            (11, 21, "NAME")  # "cornstarch"
        ]
    }),

    # Example 39
    ("1 egg plus 2 egg yolks", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 5, "NAME"),  # "egg"
            (6, 22, "COMMENT")  # "plus 2 egg yolks" (Kept as original span)
        ]
    }),

    # Example 40
    ("1/3 cup cornstarch", {
        "entities": [
            (0, 3, "QTY"),  # "1/3"
            (4, 7, "UNIT"),  # "cup"
            (8, 18, "NAME")  # "cornstarch"
        ]
    }),

    # Example 41
    ("Pinch of salt", {
        "entities": [
            (0, 5, "COMMENT"),  # "Pinch" (Original label was COMMENT)
            (6, 8, "PREP"),  # "of" (Kept as original PREP span)
            (9, 13, "NAME")  # "salt"
        ]
    }),

    # Example 42
    ("1 8-ounce package cream cheese, at room temperature", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 9, "COMMENT"),  # "8-ounce" (Kept as original span)
            (10, 17, "UNIT"),  # "package"
            (18, 23, "NAME"),  # "cream" (from original NAME "cream cheese" 18-30)
            (24, 30, "NAME"),  # "cheese" (from original NAME "cream cheese" 18-30)
            # Comma at 30 is "O"
            (32, 51, "COMMENT")  # "at room temperature" (Kept as original span)
        ]
    }),

    # Example 43
    ("1 8-ounce can crushed pineapple, drained", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 9, "COMMENT"),  # "8-ounce" (Kept as original span)
            (10, 13, "UNIT"),  # "can"
            (14, 21, "NAME"),
            # "crushed" (from original NAME "crushed pineapple" 14-31) - *If "crushed" is PREP, this changes*
            (22, 31, "NAME"),  # "pineapple" (from original NAME "crushed pineapple" 14-31)
            # Comma at 31 is "O"
            (33, 40, "PREP")  # "drained" (Kept as original span)
        ]
    }),

    # Example 44
    ("1 1/2 cups finely grated peeled carrots (use the small holes of a box grater)", {
        "entities": [
            (0, 5, "QTY"),  # "1" (from original QTY "1 1/2" 0-5)
            (6, 10, "UNIT"),  # "cups"
            (11, 31, "PREP"),  # "finely grated peeled" (Kept as original span)
            (32, 39, "NAME"),  # "carrots"
            (40, 77, "COMMENT")  # "(use the small holes of a box grater)" (Kept as original span)
        ]
    }),

    # Example 45
    ("1 tablespoon plus 1 teaspoon baking powder", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 28, "COMMENT"),  # "plus 1 teaspoon" (Kept as original span)
            (29, 35, "NAME"),  # "baking" (from original NAME "baking powder" 29-42)
            (36, 42, "NAME")  # "powder" (from original NAME "baking powder" 29-42)
        ]
    }),

    # Example 46
    ("2 cups pecan halves", {
        "entities": [
            (0, 1, "QTY"),  # "2"
            (2, 6, "UNIT"),  # "cups"
            (7, 12, "NAME"),  # "pecan"
            (13, 19, "PREP")  # "halves" (Original label was PREP for "halves")
            # If "pecan halves" was one NAME (7,19,"NAME"), then "halves" would be NAME too.
        ]
    }),

    # Example 47
    ("1 tablespoon molasses", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 21, "NAME")  # "molasses"
        ]
    }),

    # Example 48
    ("3 cups old-fashioned rolled oats", {
        "entities": [
            (0, 1, "QTY"),  # "3"
            (2, 6, "UNIT"),  # "cups"
            (7, 20, "PREP"),  # "old-fashioned" (Original span for "old-fashioned rolled" was (7,27,"PREP"))
            (21, 27, "PREP"),  # "rolled" (from original PREP (7,27,"PREP"))
            (28, 32, "NAME")  # "oats"
        ]
    }),

    # Example 49
    ("4 ounces or 1/2 cup water", {
        "entities": [
            (0, 1, "QTY"),         # "4"
            (2, 8, "UNIT"),        # "ounces"
            # "or" (9,11) is O or implicitly handled
            (12, 15, "ALT_QTY"),   # "1/2" (alternative quantity for water)
            (16, 19, "ALT_UNIT"),  # "cup" (alternative unit for water)
            (20, 25, "NAME")       # "water"
        ]
    }),

    # Example 50
    ("2 green mangoes, peeled and julienned", {
        "entities": [
            (0, 1, "QTY"),  # "2"
            (2, 7, "NAME"),  # "green" (from original NAME "green mangoes" 2-15)
            (8, 15, "NAME"),  # "mangoes" (from original NAME "green mangoes" 2-15)
            # Comma at 15 is "O"
            (17, 37, "PREP")  # "peeled and julienned" (Kept as original span)
        ]
    }),

    # Example 51
    ("1 long red chile, seeded and julienned", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 6, "COMMENT"),  # "long" (Original label was COMMENT)
            (7, 10, "NAME"),  # "red" (from original NAME "red chile" 7-16)
            (11, 16, "NAME"),  # "chile" (from original NAME "red chile" 7-16)
            # Comma at 16 is "O"
            (18, 38, "PREP")  # "seeded and julienned" (Kept as original span)
        ]
    }),

    # Example 52
    ("1 cup Dashi, recipe follows (or 1 teaspoon instant dashi powder, such as Ajinomoto’s Hondashi, dissolved in 1 cup water)",
     {
         "entities": [
             (0, 1, "QTY"),  # "1"
             (2, 5, "UNIT"),  # "cup"
             (6, 11, "NAME"),  # "Dashi"
             # Comma at 11 is "O"
             (13, 27, "COMMENT"),  # "recipe follows" (Kept as original span)
             (28, 120, "COMMENT")  # "(or 1 teaspoon ... water)" (Kept as original span)
         ]
     }),

    # Example 53
    ("1/2 cup grated daikon radish, or to taste, lightly squeezed to remove excess liquid", {
        "entities": [
            (0, 3, "QTY"),  # "1/2"
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "grated" (Kept as original span)
            (15, 21, "NAME"),  # "daikon" (from original NAME "daikon radish" 15-28)
            (22, 28, "NAME"),  # "radish" (from original NAME "daikon radish" 15-28)
            # Comma at 28 is "O"
            (30, 41, "COMMENT"),  # "or to taste" (Kept as original span)
            # Comma at 41 is "O"
            (43, 83, "PREP")  # "lightly squeezed to remove excess liquid" (Kept as original span)
        ]
    }),

    # Example 54
    ("1 pound peeled and deveined large shrimp (see Cook’s Note), rinsed in cold water and thoroughly dried", {
        "entities": [
            (0, 1, "QTY"),  # "1"
            (2, 7, "UNIT"),  # "pound"
            (8, 27, "PREP"),  # "peeled and deveined" (Kept as original span)
            (28, 33, "NAME"),  # "large" (from original NAME "large shrimp" 28-40)
            (34, 40, "NAME"),  # "shrimp" (from original NAME "large shrimp" 28-40)
            (41, 58, "COMMENT"),  # "(see Cook’s Note)" (Kept as original span)
            # Comma at 58 is "O"
            (60, 101, "PREP")  # "rinsed in cold water and thoroughly dried" (Kept as original span)
        ]
    }),

    # Example 55
    ("1 3/4 cups seltzer", {
        "entities": [
            (0, 5, "QTY"),  # "1" (from original QTY "1 3/4" 0-5)
            (6, 10, "UNIT"),  # "cups"
            (11, 18, "NAME")  # "seltzer"
        ]
    }),
    # Re-annotated data based on the FINAL REFINED rules:
    # - NAME entities are broken into word-level NAME entities.
    # - COMMENT, PREP, ALT_NAME, QTY entities are kept as single, original spans.
    # - UNIT entities are single words.
    # - Commas and other non-entity words become "O" (and are thus not listed in the 'entities' list).
    # Tokenization based on spaCy's default English tokenizer.

    # Example 1
    ("1 tablespoon toasted sesame seeds, for garnish", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 20, "PREP"),  # "toasted" (Kept as original PREP span)
            (21, 27, "NAME"),  # "sesame" (from original NAME "sesame seeds" 21-33)
            (28, 33, "NAME"),  # "seeds" (from original NAME "sesame seeds" 21-33)
            # Comma at 33 is "O"
            (35, 46, "COMMENT")  # "for garnish" (Kept as original COMMENT span)
        ]
    }),

    # Example 2
    ("1 clove garlic, peeled and crushed, left whole", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "NAME"),  # "clove"
            (8, 14, "NAME"),  # "garlic"
            # Comma at 14 is "O"
            (16, 46, "PREP")  # "peeled and crushed, left whole" (Kept as original PREP span)
        ]
    }),

    # Example 3
    ("1 heaping tablespoon cornstarch", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 9, "PREP"),  # "heaping" (Kept as original PREP span)
            (10, 20, "UNIT"),  # "tablespoon"
            (21, 31, "NAME")  # "cornstarch"
        ]
    }),

    ("2 1/2 pounds boneless, skinless chicken thighs, cut into 1-inch cubes", {  # More standard token-aligned split
        "entities": [
            (0, 5, "QTY"),
            (6, 12, "UNIT"),
            (13, 22, "NAME"),  # "boneless," (token)
            (23, 31, "NAME"),  # "skinless" (token)
            (32, 39, "NAME"),  # "chicken"
            (40, 46, "NAME"),  # "thighs"
            (48, 69, "PREP")
        ]
    }),

    # Example 5
    ("Pinch freshly ground white pepper", {
        "entities": [
            (0, 5, "COMMENT"),  # "Pinch" (Kept as original COMMENT span)
            (6, 20, "PREP"),  # "freshly ground" (Kept as original PREP span)
            (21, 26, "NAME"),  # "white" (from original NAME "white pepper" 21-33)
            (27, 33, "NAME")  # "pepper" (from original NAME "white pepper" 21-33)
        ]
    }),

    # Example 6
    ("1/2 pound thick flank steak, weighed after trimming, cut into strips 2 1/2 inches by 1/4 inch", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 9, "UNIT"),  # "pound"
            (10, 15, "PREP"),  # "thick" (Kept as original PREP span)
            (16, 21, "NAME"),  # "flank" (from original NAME "flank steak" 16-27)
            (22, 27, "NAME"),  # "steak" (from original NAME "flank steak" 16-27)
            # Comma at 27 is "O"
            (29, 51, "COMMENT"),  # "weighed after trimming" (Kept as original COMMENT span)
            # Comma at 51 is "O"
            (53, 93, "PREP")  # "cut into strips 2 1/2 inches by 1/4 inch" (Kept as original PREP span)
        ]
    }),

    # Example 7
    ("1 (3-pound) chicken", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 11, "COMMENT"),  # "(3-pound)" (Kept as original COMMENT span)
            (12, 19, "NAME")  # "chicken"
        ]
    }),

    # Example 8
    ("4 cups broccoli florets, pre-cooked", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept as original QTY span)
            (2, 6, "UNIT"),  # "cups"
            (7, 15, "NAME"),  # "broccoli" (from original NAME "broccoli florets" 7-23)
            (16, 23, "NAME"),  # "florets" (from original NAME "broccoli florets" 7-23)
            # Comma at 23 is "O"
            (25, 35, "PREP")  # "pre-cooked" (Kept as original PREP span)
        ]
    }),

    # Example 9
    ("1 pound boneless, skinless chicken thighs, cut into 1/2-inch pieces", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "pound"
            (8, 16, "PREP"),  # "boneless," (Kept as original PREP span, includes comma) - *This is unusual for PREP*
            (18, 26, "PREP"),  # "skinless" (Kept as original PREP span)
            (27, 34, "NAME"),  # "chicken" (from original NAME "chicken thighs" 27-41)
            (35, 41, "NAME"),  # "thighs" (from original NAME "chicken thighs" 27-41)
            # Comma at 41 is "O"
            (43, 67, "PREP")  # "cut into 1/2-inch pieces" (Kept as original PREP span)
        ]
    }),

    # Example 10
    ("1 tablespoon peanut oil, plus more as needed", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 19, "NAME"),  # "peanut" (from original NAME "peanut oil" 13-23)
            (20, 23, "NAME"),  # "oil" (from original NAME "peanut oil" 13-23)
            # Comma at 23 is "O"
            (25, 44, "COMMENT")  # "plus more as needed" (Kept as original COMMENT span)
        ]
    }),

    # Example 11
    ("10 ounces assorted wild mushrooms, such as oyster, shitake, chanterelles, wood ear, or porcini", {
        "entities": [
            (0, 2, "QTY"),  # "10" (Kept as original QTY span)
            (3, 9, "UNIT"),  # "ounces"
            (10, 18, "PREP"),  # "assorted" (Kept as original PREP span)
            (19, 23, "NAME"),  # "wild" (from original NAME "wild mushrooms" 19-33)
            (24, 33, "NAME"),  # "mushrooms" (from original NAME "wild mushrooms" 19-33)
            # Comma at 33 is "O"
            (35, 94, "COMMENT")
            # "such as oyster, shitake, chanterelles, wood ear, or porcini" (Kept as original COMMENT span)
        ]
    }),

    # Example 12
    ("3 (2 1/2 to 3 pound) farm-raised pheasants*, innards removed, wing tips and necks trimmed (See Cook's Note)", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 20, "COMMENT"),  # "(2 1/2 to 3 pound)" (Kept as original COMMENT span)
            (21, 32, "PREP"),  # "farm-raised" (Kept as original PREP span)
            (33, 44, "NAME"),  # "pheasants*" (from original NAME "pheasants*" 33-43, includes *)
            # Comma at 43 is "O"
            (45, 89, "PREP"),  # "innards removed, wing tips and necks trimmed" (Kept as original PREP span)
            (90, 107, "COMMENT")  # "(See Cook's Note)" (Kept as original COMMENT span)
        ]
    }),

    # Example 13
    ("1/4 pound cured and smoked country ham, finely chopped (or chopped in a food processor)", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept as original QTY span)
            (4, 9, "UNIT"),  # "pound"
            (10, 15, "PREP"),  # "cured" (Kept as original PREP span)
            (16, 19, "O"),  # "and"
            (20, 26, "NAME"),
            # "smoked" (from original NAME "smoked country ham" 20-38) - *If "smoked" is PREP this needs to change*
            (27, 34, "NAME"),  # "country" (from original NAME "smoked country ham" 20-38)
            (35, 38, "NAME"),  # "ham" (from original NAME "smoked country ham" 20-38)
            # Comma at 38 is "O"
            (40, 54, "PREP"),  # "finely chopped" (Kept as original PREP span)
            (55, 87, "COMMENT")  # "(or chopped in a food processor)" (Kept as original COMMENT span)
        ]
        # Original had (20,38,"NAME") for "smoked country ham". If "smoked" is PREP, original should be (20,26,"PREP")
    }),

    # Example 14
    ("1 1/4 pounds ground chuck", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/4" (Kept as original QTY span)
            (6, 12, "UNIT"),  # "pounds"
            (13, 19, "NAME"),  # "ground" (Kept as original PREP span)
            (20, 25, "NAME")  # "chuck"
        ]
    }),

    # Example 15
    ("1 teaspoon seafood seasoning, such as Old Bay", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 18, "NAME"),  # "seafood" (from original NAME "seafood seasoning" 11-28)
            (19, 28, "NAME"),  # "seasoning" (from original NAME "seafood seasoning" 11-28)
            # Comma at 28 is "O"
            (30, 45, "COMMENT")  # "such as Old Bay" (Kept as original COMMENT span)
        ]
    }),

    # Example 16
    ("2 to 3 ounces rice wine vinegar", {
        "entities": [
            (0, 6, "QTY"),  # "2 to 3" (Kept as original QTY span)
            (7, 13, "UNIT"),  # "ounces"
            (14, 18, "NAME"),  # "rice" (from original NAME "rice wine vinegar" 14-31)
            (19, 23, "NAME"),  # "wine" (from original NAME "rice wine vinegar" 14-31)
            (24, 31, "NAME")  # "vinegar" (from original NAME "rice wine vinegar" 14-31)
        ]
    }),

    # Example 17
    ("10 ounces medium or wide egg noodles", {
        "entities": [
            (0, 2, "QTY"),  # "10" (Kept as original QTY span)
            (3, 9, "UNIT"),  # "ounces"
            (10, 16, "NAME"),  # "medium" (Kept as original PREP span)
            (17, 24, "ALT_NAME"),  # "or wide" (Kept as original ALT_NAME span)
            (25, 28, "NAME"),  # "egg" (from original NAME "egg noodles" 25-36)
            (29, 36, "NAME")  # "noodles" (from original NAME "egg noodles" 25-36)
        ]
    }),

    # Example 18
    ("1 tablespoon (15 g) white sugar", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 19, "COMMENT"),  # "(15 g)" (Kept as original COMMENT span)
            (20, 25, "NAME"),  # "white" (from original NAME "white sugar" 20-31)
            (26, 31, "NAME")  # "sugar" (from original NAME "white sugar" 20-31)
        ]
    }),

    # Example 19
    ("1 pod star anise", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "PREP"),  # "pod" (Kept as original PREP span)
            (6, 10, "NAME"),  # "star" (from original NAME "star anise" 6-16)
            (11, 16, "NAME")  # "anise" (from original NAME "star anise" 6-16)
        ]
    }),

    # Example 20
    ("1/4 cup sliced and drained pickled jalapenos, chopped", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 34, "PREP"),  # "sliced and drained pickled" (Kept as original PREP span)
            (35, 44, "NAME"),  # "jalapenos"
            # Comma at 44 is "O"
            (46, 53, "PREP")  # "chopped" (Kept as original PREP span)
        ]
    }),

    # Example 21
    ("1/2 teaspoon ground cumin", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 19, "NAME"),  # "ground" (from original NAME "ground cumin" 13-25)
            (20, 25, "NAME")  # "cumin" (from original NAME "ground cumin" 13-25)
        ]
    }),

    # Example 22
    ("1 bunch arugula", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "bunch"
            (8, 15, "NAME")  # "arugula"
        ]
    }),

    # Example 23
    ("1 (8-ounce) chicken breast, grilled or poached and cut into small cubes or shredded", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 11, "COMMENT"),  # "(8-ounce)" (Kept as original COMMENT span)
            (12, 19, "NAME"),  # "chicken" (from original NAME "chicken breast" 12-26)
            (20, 26, "NAME"),  # "breast" (from original NAME "chicken breast" 12-26)
            # Comma at 26 is "O"
            (28, 83, "PREP")  # "grilled or poached and cut into small cubes or shredded" (Kept as original PREP span)
        ]
    }),

    # Example 24
    ("1 pound (453 grams) peeled and deveined large shrimp, tail on", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "pound"
            (8, 19, "COMMENT"),  # "(453 grams)" (Kept as original COMMENT span)
            (20, 39, "PREP"),  # "peeled and deveined" (Kept as original PREP span)
            (40, 45, "NAME"),  # "large" (Original label was UNIT)
            (46, 52, "NAME"),  # "shrimp"
            # Comma at 52 is "O"
            (54, 61, "PREP")  # "tail on" (Kept as original PREP span)
        ]
    }),

    # Example 25
    ("1 cup (175 grams) halved grape or cherry tomatoes", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 17, "COMMENT"),  # "(175 grams)" (Kept as original COMMENT span)
            (18, 24, "PREP"),  # "halved" (Kept as original PREP span)
            (25, 30, "NAME"),  # "grape"
            (31, 40, "ALT_NAME"),  # "or cherry tomatoes" (Kept as original ALT_NAME span)
            (41, 49, "NAME")  # " tomatoes" (Kept as original ALT_NAME span)
        ]
    }),

    # Example 26
    ("1 cup Clamato", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 13, "NAME")  # "Clamato"
        ]
    }),

    # Example 27
    ("1/4 seedless watermelon, rind removed, peeled and cut into 1-inch pieces, flesh reserved", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept as original QTY span)
            (4, 12, "NAME"),  # "seedless" (from original NAME "seedless watermelon" 4-23)
            (13, 23, "NAME"),  # "watermelon" (from original NAME "seedless watermelon" 4-23)
            # Comma at 23 is "O"
            (25, 72, "PREP"),  # "rind removed, peeled and cut into 1-inch pieces" (Kept as original PREP span)
            # Comma at 72 is "O"
            (74, 88, "COMMENT")  # "flesh reserved" (Kept as original COMMENT span)
        ]
    }),

    # Example 28
    ("One 15-ounce can chickpeas", {
        "entities": [
            (0, 3, "QTY"),  # "One" (Kept as original QTY span)
            (4, 12, "COMMENT"),  # "15-ounce" (Kept as original COMMENT span)
            (13, 16, "UNIT"),  # "can"
            (17, 26, "NAME")  # "chickpeas"
        ]
    }),

    # Example 29
    ("1/3 cup plus 1 tablespoon tahini", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 25, "COMMENT"),  # "plus 1 tablespoon" (Kept as original COMMENT span)
            (26, 32, "NAME")  # "tahini"
        ]
    }),

    # Example 30
    ("4 heads garlic, roasted; paper skin removed and cored", {  # Semicolon acts as separator
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "heads"
            (8, 14, "NAME"),  # "garlic"
            # Comma at 14 is "O"
            (16, 53, "PREP")  # "roasted; paper skin removed and cored" (Kept as original PREP span)
        ]
    }),

    # Example 31
    ("1 red onion, peeled and sliced into 3 parts width wise", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "NAME"),  # "red" (from original NAME "red onion" 2-11)
            (6, 11, "NAME"),  # "onion" (from original NAME "red onion" 2-11)
            # Comma at 11 is "O"
            (13, 54, "PREP")  # "peeled and sliced into 3 parts width wise" (Kept as original PREP span)
        ]
    }),

    # Example 32
    ("1 tablespoon basil, minced", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 18, "NAME"),  # "basil"
            # Comma at 18 is "O"
            (20, 26, "PREP")  # "minced" (Kept as original PREP span)
        ]
    }),

    # Example 33
    ("8 oz duck or rabbit confit, medium to large pieces removed from bones", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept as original QTY span)
            (2, 4, "UNIT"),  # "oz"
            (5, 9, "NAME"),  # "duck"
            (10, 26, "ALT_NAME"),  # "or rabbit confit" (Kept as original ALT_NAME span)
            # Comma at 26 is "O"
            (28, 69, "PREP")  # "medium to large pieces removed from bones" (Kept as original PREP span)
        ]
    }),

    # Example 34
    ("15 steaks", {
        "entities": [
            (0, 2, "QTY"),  # "15" (Kept as original QTY span)
            (3, 9, "NAME")  # "steaks"
        ]
    }),

    # Example 35
    ("Flaky sea salt", {
        "entities": [
            (0, 5, "PREP"),  # "Flaky" (Kept as original PREP span)
            (6, 9, "NAME"),  # "sea" (from original NAME "sea salt" 6-14)
            (10, 14, "NAME")  # "salt" (from original NAME "sea salt" 6-14)
        ]
    }),

    # Example 36
    ("2 boneless rib-eye steaks", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 10, "NAME"),  # "boneless" (Kept as original PREP span)
            (11, 18, "NAME"),  # "rib-eye" (from original NAME "rib-eye steaks" 11-25) (tokenized as one)
            (19, 25, "NAME")  # "steaks" (from original NAME "rib-eye steaks" 11-25)
        ]
    }),

    # Example 37
    ("1 tablespoon annatto seeds", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 20, "NAME"),  # "annatto" (from original NAME "annatto seeds" 13-26)
            (21, 26, "NAME")  # "seeds" (from original NAME "annatto seeds" 13-26)
        ]
    }),

    # Example 38
    ("4 cups peeled and grated sweet potatoes", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept as original QTY span)
            (2, 6, "UNIT"),  # "cups"
            (7, 24, "PREP"),  # "peeled and grated" (Kept as original PREP span)
            (25, 30, "NAME"),  # "sweet" (from original NAME "sweet potatoes" 25-39)
            (31, 39, "NAME")  # "potatoes" (from original NAME "sweet potatoes" 25-39)
        ]
    }),

    # Example 39
    ("2 ounces sliced pastrami, finely chopped", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 8, "UNIT"),  # "ounces"
            (9, 15, "PREP"),  # "sliced" (Kept as original PREP span)
            (16, 24, "NAME"),  # "pastrami"
            # Comma at 24 is "O"
            (26, 40, "PREP")  # "finely chopped" (Kept as original PREP span)
        ]
    }),

    # Example 40
    ("2 teaspoons toasted and ground coriander seed", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 11, "UNIT"),  # "teaspoons"
            (12, 19, "PREP"),  # "toasted" (Kept as original PREP span)
            (20, 23, "O"),  # "and"
            (24, 30, "NAME"),  # "ground" (from original NAME "ground coriander seed" 24-45)
            (31, 40, "NAME"),  # "coriander" (from original NAME "ground coriander seed" 24-45)
            (41, 45, "NAME")  # "seed" (from original NAME "ground coriander seed" 24-45)
        ]
    }),

    # Example 41
    ("3 ancho chiles, stemmed, seeded and sliced", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 7, "NAME"),  # "ancho" (from original NAME "ancho chiles" 2-14)
            (8, 14, "NAME"),  # "chiles" (from original NAME "ancho chiles" 2-14)
            # Comma at 14 is "O"
            (16, 42, "PREP")  # "stemmed, seeded and sliced" (Kept as original PREP span)
        ]
    }),

    # Example 42
    ("3 cascabel chiles, stemmed, seeded and sliced", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 10, "NAME"),  # "cascabel" (from original NAME "cascabel chiles" 2-17)
            (11, 17, "NAME"),  # "chiles" (from original NAME "cascabel chiles" 2-17)
            # Comma at 17 is "O"
            (19, 45, "PREP")  # "stemmed, seeded and sliced" (Kept as original PREP span)
        ]
    }),

    # Example 43
    ("3 dried arbol chiles, stemmed, seeded and sliced", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 7, "PREP"),  # "dried" (Kept as original PREP span)
            (8, 13, "NAME"),  # "arbol" (from original NAME "arbol chiles" 8-20)
            (14, 20, "NAME"),  # "chiles" (from original NAME "arbol chiles" 8-20)
            # Comma at 20 is "O"
            (22, 48, "PREP")  # "stemmed, seeded and sliced" (Kept as original PREP span)
        ]
    }),

    # Example 44
    ("2 tablespoons whole cumin seeds", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 19, "PREP"),  # "whole" (Kept as original PREP span)
            (20, 25, "NAME"),  # "cumin" (from original NAME "cumin seeds" 20-31)
            (26, 31, "NAME")  # "seeds" (from original NAME "cumin seeds" 20-31)
        ]
    }),

    # Example 45
    ("One 9-ounce package fresh fettuccine", {
        "entities": [
            (0, 3, "QTY"),  # "One" (Kept as original QTY span)
            (4, 11, "COMMENT"),  # "9-ounce" (Kept as original COMMENT span)
            (12, 19, "UNIT"),  # "package"
            (20, 25, "PREP"),  # "fresh" (Kept as original PREP span)
            (26, 36, "NAME")  # "fettuccine"
        ]
    }),

    # Example 46
    ("4 pounds spinach, stems removed, washed and dried", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept as original QTY span)
            (2, 8, "UNIT"),  # "pounds"
            (9, 16, "NAME"),  # "spinach"
            # Comma at 16 is "O"
            (18, 49, "PREP")  # "stems removed, washed and dried" (Kept as original PREP span)
        ]
    }),

    # Example 47
    ("1/2 pound dried cannellini beans, black-eyed peas, soaked overnight in cold water and drained", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 9, "UNIT"),  # "pound"
            (10, 15, "PREP"),  # "dried" (Kept as original PREP span)
            (16, 26, "NAME"),  # "cannellini" (from original NAME "cannellini beans" 16-32)
            (27, 32, "NAME"),  # "beans" (from original NAME "cannellini beans" 16-32)
            # Comma at 32 is "O"
            (34, 49, "ALT_NAME"),  # "black-eyed peas" (Kept as original ALT_NAME span)
            # Comma at 49 is "O"
            (51, 93, "PREP")  # "soaked overnight in cold water and drained" (Kept as original PREP span)
        ]
    }),

    # Example 48
    ("1/2 teaspoon Four-Spice Power (recipe follows)", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 23, "NAME"),  # "Four-Spice" (from original NAME "Four-Spice Power" 13-29, assuming hyphenated token)
            (24, 29, "NAME"),  # "Power" (from original NAME "Four-Spice Power" 13-29)
            (30, 46, "COMMENT")  # "(recipe follows)" (Kept as original COMMENT span)
        ]
    }),

    # Example 49
    ("1 pound and 10 ounces sour cherries, pre-pitted weight; or 6 cups frozen or jarred", {
        "entities": [
            # Primary Item
            (0, 1, "QTY"),         # "1"
            (2, 7, "UNIT"),        # "pound"
            # "and" (8,11) is O
            (12, 14, "ALT_QTY"),   # "10" (additive quantity for the sour cherries)
            (15, 21, "ALT_UNIT"),  # "ounces" (additive unit for the sour cherries)
            (22, 26, "NAME"),      # "sour"
            (27, 35, "NAME"),      # "cherries"
            # Comma at 35 is O
            (37, 47, "COMMENT"),   # "pre-pitted" (treating as part of the weight comment)
            (48, 54, "COMMENT"),   # "weight"
            # Semicolon at 54 is O
            # Alternative Item/Form (implicitly sour cherries)
            # "or" (56,58) is O
            (59, 60, "ALT_QTY"),   # "6" (quantity for the alternative form)
            (61, 65, "ALT_UNIT"),  # "cups" (unit for the alternative form)
            (66, 82, "ALT_NAME")   # "or jarred" (alternative preparation for the alternative form)
            # OR: (73,75,"O") "or", (76,82,"PREP") "jarred" if "or" is not part of ALT_NAME
        ]
    }),

    # Example 50
    ("Beaten egg, for glaze", {
        "entities": [
            (0, 6, "PREP"),  # "Beaten" (Kept as original PREP span)
            (7, 10, "NAME"),  # "egg"
            # Comma at 10 is "O"
            (12, 21, "COMMENT")  # "for glaze" (Kept as original COMMENT span)
        ]
    }),

    # Example 51
    ("7 ounces (200 grams) spicy or mild genoa salami, thinly sliced or shaved", {
        "entities": [
            (0, 1, "QTY"),  # "7" (Kept as original QTY span)
            (2, 8, "UNIT"),  # "ounces"
            (9, 20, "COMMENT"),  # "(200 grams)" (Kept as original COMMENT span)
            (21, 26, "NAME"),  # "spicy" (Kept as original PREP span)
            (27, 34, "ALT_NAME"),  # "or mild" (Kept as original ALT_NAME span)
            (35, 40, "NAME"),  # "genoa" (from original NAME "genoa salami" 35-47)
            (41, 47, "NAME"),  # "salami" (from original NAME "genoa salami" 35-47)
            # Comma at 47 is "O"
            (49, 72, "PREP")  # "thinly sliced or shaved" (Kept as original PREP span)
        ]
    }),

    # Example 52
    ("2 cups of white grits", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 6, "UNIT"),  # "cups"
            (7, 9, "PREP"),  # "of" (Kept as original PREP span)
            (10, 15, "NAME"),  # "white" (from original NAME "white grits" 10-21)
            (16, 21, "NAME")  # "grits" (from original NAME "white grits" 10-21)
        ]
    }),

    # Example 53
    ("4 slices cooked and crumbled bacon", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept as original QTY span)
            (2, 28, "PREP"),  # "slices cooked and crumbled" (Kept as original PREP span)
            (29, 34, "NAME")  # "bacon"
        ]
    }),

    # Example 54
    ("1 tablespoon minced seeded red jalapenos", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 26, "PREP"),  # "minced seeded" (Kept as original PREP span)
            (27, 30, "NAME"),  # "red" (from original NAME "red jalapenos" 27-40)
            (31, 40, "NAME")  # "jalapenos" (from original NAME "red jalapenos" 27-40)
        ]
    }),

    # Example 55
    ("1 tablespoon basil leaves, torn", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 18, "NAME"),  # "basil" (from original NAME "basil leaves" 13-25)
            (19, 25, "NAME"),  # "leaves" (from original NAME "basil leaves" 13-25)
            # Comma at 25 is "O"
            (27, 31, "PREP")  # "torn" (Kept as original PREP span)
        ]
    }),

    # Example 56
    ("1/2 large watermelon", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 9, "UNIT"),  # "large"
            (10, 20, "NAME")  # "watermelon"
        ]
    }),

    # Example 57
    ("1 pound fresh or frozen cranberries", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "pound"
            (8, 23, "PREP"),  # "fresh" (Kept as original PREP span)
            (24, 35, "NAME")  # "cranberries"
        ]
    }),

    # Example 58
    ("10 large basil leaves", {
        "entities": [
            (0, 2, "QTY"),  # "10" (Kept as original QTY span)
            (3, 8, "UNIT"),  # "large"
            (9, 14, "NAME"),  # "basil" (from original NAME "basil leaves" 9-21)
            (15, 21, "NAME")  # "leaves" (from original NAME "basil leaves" 9-21)
        ]
    }),

    # Example 59
    ("3 tablespoons best quality cocoa powder", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 26, "PREP"),  # "best quality" (Kept as original PREP span)
            (27, 32, "NAME"),  # "cocoa" (from original NAME "cocoa powder" 27-39)
            (33, 39, "NAME")  # "powder" (from original NAME "cocoa powder" 27-39)
        ]
    }),

    # Example 60
    ("1 cup very cold heavy cream", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 15, "PREP"),
            # "very cold" (Kept as original PREP span, your original was (6,10,"PREP") "very" and (11,15,"PREP") "cold")
            # Sticking to your new rule to NOT split PREP: (6,15,"PREP")
            (16, 21, "NAME"),  # "heavy" (from original NAME "heavy cream" 16-27)
            (22, 27, "NAME")  # "cream" (from original NAME "heavy cream" 16-27)
        ]
    }),

    # Example 61
    ("3 cups lightly packed basil leaves", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 6, "UNIT"),  # "cups"
            (7, 21, "PREP"),  # "lightly packed" (Kept as original PREP span)
            (22, 27, "NAME"),  # "basil" (from original NAME "basil leaves" 22-34)
            (28, 34, "NAME")  # "leaves" (from original NAME "basil leaves" 22-34)
        ]
    }),

    # Example 62
    ("1 pound linguine", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "pound"
            (8, 16, "NAME")  # "linguine"
        ]
    }),

    # Example 63
    ("1 ounce tequila", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "ounce"
            (8, 15, "NAME")  # "tequila"
        ]
    }),

    # Example 64
    ("1 tablespoon tomatoes, peeled, seeded and small dice", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 12, "UNIT"),  # "tablespoons" (Typo in original? "tablespoon" is 2-12)
            (13, 21, "NAME"),  # "tomatoes"
            # Comma at 21 is "O"
            (23, 52, "PREP")  # "peeled, seeded and small dice" (Kept as original PREP span)
        ]
    }),

    # Example 65
    ("12 ounces lump crab meat", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept as original QTY span)
            (3, 9, "UNIT"),  # "ounces"
            (10, 14, "NAME"),  # "lump" (from original NAME "lump crab meat" 10-24)
            (15, 19, "NAME"),  # "crab" (from original NAME "lump crab meat" 10-24)
            (20, 24, "NAME")  # "meat" (from original NAME "lump crab meat" 10-24)
        ]
    }),

    # Example 66
    ("3 cups bread crumbs", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 6, "UNIT"),  # "cups"
            (7, 12, "NAME"),  # "bread" (from original NAME "bread crumbs" 7-19)
            (13, 19, "NAME")  # "crumbs" (from original NAME "bread crumbs" 7-19)
        ]
    }),

    # Example 67
    ("6 (5 to 6-ounce) tuna paillards, 1/2-inch thick", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept as original QTY span)
            (2, 16, "COMMENT"),  # "(5 to 6-ounce)" (Kept as original COMMENT span)
            (17, 21, "NAME"),  # "tuna" (from original NAME "tuna paillards" 17-31)
            (22, 31, "NAME"),  # "paillards" (from original NAME "tuna paillards" 17-31)
            # Comma at 31 is "O"
            (33, 47, "COMMENT")  # "1/2-inch thick" (Kept as original COMMENT span)
        ]
    }),

    # Example 68
    ("1 pound spinach, picked and washed (loosely packed)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "pound"
            (8, 15, "NAME"),  # "spinach"
            # Comma at 15 is "O"
            (17, 34, "PREP"),  # "picked and washed" (Kept as original PREP span)
            (35, 51, "COMMENT")  # "(loosely packed)" (Kept as original COMMENT span)
        ]
    }),

    # Example 69
    ("1/2 cup pitted and chopped kalamata olives", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 26, "PREP"),  # "pitted and chopped" (Kept as original PREP span)
            (27, 35, "NAME"),  # "kalamata" (from original NAME "kalamata olives" 27-42)
            (36, 42, "NAME")  # "olives" (from original NAME "kalamata olives" 27-42)
        ]
    }),

    ("2 (1 pound) halibut steaks, 1 1/4-inch thick, from tail end of fish", {  # Corrected attempt
        "entities": [
            (0, 1, "QTY"),
            (2, 11, "COMMENT"),  # "(1 pound)"
            (12, 19, "NAME"),  # "halibut"
            (20, 26, "NAME"),  # "steaks" (If "halibut steaks" is the name) OR (20,26,"UNIT") if "steaks" is a unit
            # Comma at 26
            (28, 44, "COMMENT"),  # "1 1/4-inch thick"
            # Comma at 46
            (46, 67, "COMMENT")  # "from tail end of fish"
        ]
    }),

    # Example 71
    ("2 1/3 cups warm water, 100 to 110 degrees F", {
        "entities": [
            (0, 5, "QTY"),  # "2 1/3" (Kept as original QTY span)
            (6, 10, "UNIT"),  # "cups"
            (11, 15, "PREP"),  # "warm" (Kept as original PREP span)
            (16, 21, "NAME"),  # "water"
            # Comma at 21 is "O"
            (23, 43, "COMMENT")  # "100 to 110 degrees F" (Kept as original COMMENT span)
        ]
    }),

    # Example 72
    ("2 tablespoons (three .75-ounce packets) active dry yeast, such as Fleischmann's", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 39, "COMMENT"),  # "(three .75-ounce packets)" (Kept as original COMMENT span)
            (40, 46, "NAME"),  # "active" (Original label (40,50,"PREP") "active dry")
            (47, 50, "NAME"),  # "dry" (from original PREP "active dry" 40-50)
            (51, 56, "NAME"),  # "yeast"
            (56, 79, "COMMENT")  # ", such as Fleischmann's" (Kept as original COMMENT span, includes comma)
        ]
    }),

    # Example 73
    ("3 tablespoons zaatar, optional", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 20, "NAME"),  # "zaatar"
            # Comma at 20 is "O"
            (22, 30, "COMMENT")  # "optional" (Kept as original COMMENT span)
        ]
    }),

    # Example 74
    ("1 cup unsalted butter, room temperature and cut into small pieces", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 14, "NAME"),  # "unsalted" (from original NAME "unsalted butter" 6-21)
            (15, 21, "NAME"),  # "butter" (from original NAME "unsalted butter" 6-21)
            # Comma at 21 is "O"
            (23, 39, "COMMENT"),  # "room temperature" (Kept as original COMMENT span)
            (40, 43, "O"),  # "and"
            (44, 65, "PREP")  # "cut into small pieces" (Kept as original PREP span)
        ]
    }),

    # Example 75
    ("1 large egg yolk beaten with 1 tablespoon water, for egg wash", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "large"
            (8, 11, "NAME"),  # "egg" (from original NAME "egg yolk" 8-16)
            (12, 16, "NAME"),  # "yolk" (from original NAME "egg yolk" 8-16)
            (17, 47, "PREP"),  # "beaten with 1 tablespoon water" (Kept as original PREP span)
            # Comma at 47 is "O"
            (49, 61, "COMMENT")  # "for egg wash" (Kept as original COMMENT span)
        ]
    }),

    # Example 76
    ("1 tablespoon active dry yeast", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 19, "NAME"),  # "active" (from original PREP "active dry" 13-23)
            (20, 23, "NAME"),  # "dry" (from original PREP "active dry" 13-23)
            (24, 29, "NAME")  # "yeast"
        ]
    }),

    # Example 77
    ("1 3/4 cups warm (110 degrees F) water", {
        "entities": [
            (0, 5, "QTY"),  # "1 3/4" (Kept as original QTY span)
            (6, 10, "UNIT"),  # "cups"
            (11, 15, "PREP"),  # "warm" (Kept as original PREP span)
            (16, 31, "COMMENT"),  # "(110 degrees F)" (Kept as original COMMENT span)
            (32, 37, "NAME")  # "water"
        ]
    }),

    # Example 78
    ("3/4 cup warm water (100 degrees F to 110 degrees F)", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "PREP"),  # "warm" (Kept as original PREP span)
            (13, 18, "NAME"),  # "water"
            (19, 51, "COMMENT")  # "(100 degrees F to 110 degrees F)" (Kept as original COMMENT span)
        ]
    }),

    # Example 79
    ("1 cup shredded and chopped rotisserie chicken meat", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 26, "PREP"),  # "shredded and chopped" (Kept as original PREP span)
            (27, 37, "NAME"),  # "rotisserie" (from original NAME "rotisserie chicken meat" 27-50)
            (38, 45, "NAME"),  # "chicken" (from original NAME "rotisserie chicken meat" 27-50)
            (46, 50, "NAME")  # "meat" (from original NAME "rotisserie chicken meat" 27-50)
        ]
    }),

    # Example 80
    ("2 grams ground coriander", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "grams"
            (8, 14, "NAME"),  # "ground" (from original NAME "ground coriander" 8-24)
            (15, 24, "NAME")  # "coriander" (from original NAME "ground coriander" 8-24)
        ]
    }),

    # Example 81
    ("3 grams garlic powder", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "grams"
            (8, 14, "NAME"),  # "garlic" (from original NAME "garlic powder" 8-21)
            (15, 21, "NAME")  # "powder" (from original NAME "garlic powder" 8-21)
        ]
    }),

    # Example 82
    ("10 pounds beef top round", {
        "entities": [
            (0, 2, "QTY"),  # "10" (Kept as original QTY span)
            (3, 9, "UNIT"),  # "pounds"
            (10, 14, "NAME"),  # "beef" (from original NAME "beef top round" 10-24)
            (15, 18, "NAME"),  # "top" (from original NAME "beef top round" 10-24)
            (19, 24, "NAME")  # "round" (from original NAME "beef top round" 10-24)
        ]
    }),

    # Example 83
    ("85 grams nonfat milk powder", {
        "entities": [
            (0, 2, "QTY"),  # "85" (Kept as original QTY span)
            (3, 8, "UNIT"),  # "grams"
            (9, 15, "NAME"),  # "nonfat" (from original NAME "nonfat milk powder" 9-27)
            (16, 20, "NAME"),  # "milk" (from original NAME "nonfat milk powder" 9-27)
            (21, 27, "NAME")  # "powder" (from original NAME "nonfat milk powder" 9-27)
        ]
    }),

    # Example 84
    ("66 grams kosher salt", {
        "entities": [
            (0, 2, "QTY"),  # "66" (Kept as original QTY span)
            (3, 8, "UNIT"),  # "grams"
            (9, 15, "NAME"),  # "kosher" (from original NAME "kosher salt" 9-20)
            (16, 20, "NAME")  # "salt" (from original NAME "kosher salt" 9-20)
        ]
    }),

    # Example 85
    ("1 tablespoon (15 milliliters) milk or water, for an egg wash", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 29, "COMMENT"),  # "(15 milliliters)" (Kept as original COMMENT span)
            (30, 34, "NAME"),  # "milk"
            (35, 43, "ALT_NAME"),  # "or water" (Kept as original ALT_NAME span)
            # Comma at 43 is "O"
            (45, 60, "COMMENT")  # "for an egg wash" (Kept as original COMMENT span)
        ]
    }),

    # Example 86
    ("1 whole ripe pineapple, cut in 1/2 lengthwise and flesh removed (making 2 'boats'), core removed and fruit diced",
     {
         "entities": [
             (0, 1, "QTY"),  # "1" (Kept as original QTY span)
             (2, 7, "PREP"),  # "whole" (Original PREP was (2,12,"PREP") "whole ripe")
             (8, 12, "PREP"),  # "ripe" (from original PREP "whole ripe" 2-12)
             (13, 22, "NAME"),  # "pineapple"
             # Comma at 22 is "O"
             (24, 63, "PREP"),  # "cut in 1/2 lengthwise and flesh removed" (Kept as original PREP span)
             (64, 82, "COMMENT"),  # "(making 2 'boats')" (Kept as original COMMENT span)
             # Comma at 82 is "O"
             (84, 112, "PREP"),  # "core removed" (Kept as original PREP span)
         ]
     }),

    # Example 87
    ("Large flake sea salt", {
        "entities": [
            (0, 5, "PREP"),  # "Large" (Original PREP was (0,5,"PREP") "Large")
            (6, 11, "PREP"),  # "flake" (Original PREP was (6,11,"PREP") "flake")
            (12, 15, "NAME"),  # "sea" (from original NAME "sea salt" 12-20)
            (16, 20, "NAME")  # "salt" (from original NAME "sea salt" 12-20)
        ]
    }),

    # Example 88
    ("4 tablespoons peeled and grated fresh ginger", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept as original QTY span)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 37, "PREP"),  # "peeled and grated fresh" (Kept as original PREP span)
            (38, 44, "NAME")  # "ginger"
        ]
    }),

    # Example 89
    ("1 tablespoon dry rubbed sage", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 16, "PREP"),  # "dry" (from original PREP "dry rubbed" 13-23)
            (17, 23, "PREP"),  # "rubbed" (from original PREP "dry rubbed" 13-23)
            (24, 28, "NAME")  # "sage"
        ]
    }),

    # Example 90
    ("16 thin slices prosciutto", {
        "entities": [
            (0, 2, "QTY"),  # "16" (Kept as original QTY span)
            (3, 7, "PREP"),  # "thin" (from original PREP "thin slices" 3-14)
            (8, 14, "PREP"),  # "slices" (from original PREP "thin slices" 3-14)
            (15, 25, "NAME")  # "prosciutto"
        ]
    }),

    # Example 91
    ("12 paper thin slices prosciutto", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept as original QTY span)
            (3, 8, "PREP"),  # "paper" (Kept as original PREP span)
            (9, 20, "PREP"),  # "thin" (from original PREP "thin slices" 9-20)
            (21, 31, "NAME")  # "prosciutto"
        ]
    }),

    # Example 92
    ("6 sage leaves", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept as original QTY span)
            (2, 6, "NAME"),  # "sage"
            (7, 13, "NAME")  # "leaves"
        ]
    }),

    # Example 93
    ("12 slices thinly sliced prosciutto (about 6 ounces)", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept as original QTY span)
            (3, 9, "PREP"),  # "slices" (Kept as original PREP span)
            (10, 23, "PREP"),
            # "thinly sliced" (Kept as original PREP span. Your original had (10,16,"PREP") "thinly", this implies one span)
            (24, 34, "NAME"),  # "prosciutto"
            (35, 51, "COMMENT")  # "(about 6 ounces)" (Kept as original COMMENT span)
        ]
    }),

    # Re-annotated data based on the FINAL REFINED rules:
    # - NAME entities are broken into word-level NAME entities.
    # - COMMENT, PREP, ALT_NAME, QTY entities are kept as single, original spans.
    # - UNIT entities are single words.
    # - Commas and other non-entity words become "O" (and are thus not listed in the 'entities' list).
    # Tokenization based on spaCy's default English tokenizer.

    # Example 1
    ("1 Japanese eggplant sliced on an angle in half-inch thick slices", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 10, "NAME"),  # "Japanese" (from original NAME "Japanese eggplant" 2-19)
            (11, 19, "NAME"),  # "eggplant" (from original NAME "Japanese eggplant" 2-19)
            (20, 64, "PREP")  # "sliced on an angle in half-inch thick slices" (Kept as original PREP span)
        ]
    }),

    # Example 2
    ("1 small zucchini sliced on an angle in half-inch thick slices", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "small"
            (8, 16, "NAME"),  # "zucchini"
            (17, 61, "PREP")  # "sliced on an angle in half-inch thick slices" (Kept as original PREP span)
        ]
    }),

    # Correcting Example 3 assuming "confectioners'" is one token
    ("3 3/4 to 4 cups confectioners' sugar (use more for stiffer icing, less for thinner)", {
        "entities": [
            (0, 10, "QTY"),
            (11, 15, "UNIT"),
            (16, 30, "NAME"),  # "confectioners'" (token)
            (31, 36, "NAME"),  # "sugar" (token)
            (37, 83, "COMMENT")
        ]
    }),

    # Example 4
    ("Your favorite sprinkles or other edible candy, for decorating", {
        "entities": [
            (0, 13, "COMMENT"),  # "Your favorite" (Kept as original COMMENT span)
            (14, 23, "NAME"),  # "sprinkles"
            (24, 45, "ALT_NAME"),  # "or other edible candy" (Kept as original ALT_NAME span)
            # Comma at 45 is "O"
            (47, 61, "COMMENT")  # "for decorating" (Kept as original COMMENT span)
        ]
    }),

    # Example 5
    ("1 vanilla bean pod, split and seeds scraped", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 9, "NAME"),  # "vanilla" (from original NAME "vanilla bean pod" 2-18)
            (10, 14, "NAME"),  # "bean" (from original NAME "vanilla bean pod" 2-18)
            (15, 18, "NAME"),  # "pod" (from original NAME "vanilla bean pod" 2-18)
            # Comma at 18 is "O"
            (20, 43, "PREP")  # "split and seeds scraped" (Kept as original PREP span)
        ]
    }),

    # Example 6
    ("Edible gold foil, optional", {
        "entities": [
            (0, 6, "PREP"),  # "Edible" (Kept as original PREP span)
            (7, 11, "NAME"),  # "gold" (from original NAME "gold foil" 7-16)
            (12, 16, "NAME"),  # "foil" (from original NAME "gold foil" 7-16)
            # Comma at 16 is "O"
            (18, 26, "COMMENT")  # "optional" (Kept as original COMMENT span)
        ]
    }),

    # Example 7
    ("2 pieces naan, warmed and torn into pieces", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 8, "COMMENT"),  # "pieces"
            (9, 13, "NAME"),  # "naan"
            # Comma at 13 is "O"
            (15, 42, "PREP"),  # "warmed" (Kept as original PREP span)
        ]
    }),

    # Example 8
    ("1/2 cup chopped fresh cilantro, plus more for topping", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "PREP"),  # "chopped" (Kept as original PREP span)
            (16, 21, "PREP"),  # "fresh" (Kept as original PREP span)
            (22, 30, "NAME"),  # "cilantro"
            # Comma at 30 is "O"
            (32, 53, "COMMENT")  # "plus more for topping" (Kept as original COMMENT span)
        ]
    }),

    # Example 9
    ("1 cup frozen sliced okra, thawed", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "PREP"),  # "frozen" (from original PREP "frozen sliced" 6-19)
            (13, 19, "PREP"),  # "sliced" (from original PREP "frozen sliced" 6-19)
            (20, 24, "NAME"),  # "okra"
            # Comma at 24 is "O"
            (26, 32, "PREP")  # "thawed" (Kept as original PREP span)
        ]
    }),

    # Example 10
    ("2 tablespoons gochujang (Korean chile paste)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 23, "NAME"),  # "gochujang"
            (24, 44, "COMMENT")  # "(Korean chile paste)" (Kept as original COMMENT span)
        ]
    }),

    # Example 11
    ("3 tablespoons chopped roasted salted peanuts", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, "PREP"),  # "chopped" (Kept as original PREP span)
            (22, 29, "PREP"),
            # "roasted" (Kept as original PREP span, original had (22,29,"PREP") and (30,44,"NAME") for "salted peanuts")
            # If "salted" is PREP and "peanuts" is NAME:
            (30, 36, "NAME"),  # "salted" (Assuming "salted" was a separate PREP based on comment "all PREP")
            (37, 44, "NAME")  # "peanuts" (Original was (30,44,"NAME") "salted peanuts")
        ]
    }),
    ("3 tablespoons chopped roasted salted peanuts", {  # Assuming "salted" is PREP, "peanuts" is NAME
        "entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 21, "PREP"),  # "chopped"
            (22, 29, "PREP"),  # "roasted"
            (30, 36, "NAME"),  # "salted"
            (37, 44, "NAME")  # "peanuts"
        ]
    }),

    # Example 12
    ("1/4 cup creme fraiche", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "NAME"),  # "creme" (from original NAME "creme fraiche" 8-21)
            (14, 21, "NAME")  # "fraiche" (from original NAME "creme fraiche" 8-21)
        ]
    }),

    # Example 13
    ("1 jar (at least 6 ounces) jalapeno jelly", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "COMMENT"),  # "jar"
            (6, 25, "COMMENT"),  # "(at least 6 ounces)" (Kept as original COMMENT span)
            (26, 34, "NAME"),  # "jalapeno" (from original NAME "jalapeno jelly" 26-40)
            (35, 40, "NAME")  # "jelly" (from original NAME "jalapeno jelly" 26-40)
        ]
    }),

    # Example 14
    ("Dill-and-Caper Creme Fraiche Sauce, for serving, recipe follows",
     {  # Corrected based on likely tokenization and your comment
         "entities": [
             (0, 14, "NAME"),
             (15, 20, "NAME"),
             (21, 28, "NAME"),
             (29, 34, "NAME"),
             (36, 47, "COMMENT"),  # "for serving"
             (49, 63, "COMMENT")  # "recipe follows"
         ]
     }),

    # Example 15
    ("1 tablespoons creme fraiche", {  # Note: "tablespoons"
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 19, "NAME"),  # "creme" (from original NAME "creme fraiche" 14-27)
            (20, 27, "NAME")  # "fraiche" (from original NAME "creme fraiche" 14-27)
        ]
    }),

    # Example 16
    ("2 jalapenos, seeded and diced fine, plus whole or sliced, for serving", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 11, "NAME"),  # "jalapenos"
            # Comma at 11 is "O"
            (13, 34, "PREP"),  # "seeded and diced fine" (Kept as original PREP span)
            # Comma at 34 is "O"
            (36, 69, "COMMENT")  # "plus whole or sliced, for serving" (Kept as original COMMENT span)
        ]
    }),

    # Example 17
    ("1/4 cup store-bought salsa verde", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 20, "PREP"),  # "store-bought" (Kept as original PREP span)
            (21, 26, "NAME"),  # "salsa" (from original NAME "salsa verde" 21-32)
            (27, 32, "NAME")  # "verde" (from original NAME "salsa verde" 21-32)
        ]
    }),

    # Example 18

    ("2 green onions, green and pale green part, thinly sliced", {  # Assuming "thinly sliced" is one PREP
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "NAME"),
            (8, 14, "NAME"),
            (16, 41, "COMMENT"),
            (43, 49, "PREP"),  # "thinly"
            (50, 56, "PREP")  # "sliced" (If they were separate PREP)
        ]  # Based on your (43,56,"PREP") for "thinly sliced", I'll keep it as one.
    }),

    # Example 19
    ("1/2 teaspoon fleur de sel", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 18, "NAME"),  # "fleur" (from original NAME "fleur de sel" 13-25)
            (19, 21, "NAME"),  # "de" (from original NAME "fleur de sel" 13-25) - *Unusual for "de" to be NAME*
            (22, 25, "NAME")  # "sel" (from original NAME "fleur de sel" 13-25)
        ]
    }),

    # Example 20
    ("3 tablespoons high-quality caramel sauce, plus more for topping", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 26, "PREP"),  # "high-quality" (Kept as original PREP span)
            (27, 34, "NAME"),  # "caramel" (from original NAME "caramel sauce" 27-40)
            (35, 40, "NAME"),  # "sauce" (from original NAME "caramel sauce" 27-40)
            # Comma at 40 is "O"
            (42, 63, "COMMENT")  # "plus more for topping" (Kept as original COMMENT span)
        ]
    }),

    # Example 21
    ("1/3 cup frisee", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "NAME")  # "frisee"
        ]
    }),

    # Example 22
    ("1 teaspoon minced fresh dill", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 17, "PREP"),  # "minced" (from original PREP "minced fresh" 11-23)
            (18, 23, "PREP"),  # "fresh" (from original PREP "minced fresh" 11-23)
            (24, 28, "NAME")  # "dill"
        ]
    }),

    # Example 23
    ("1/2 cup minced scallions, white and green parts (4 scallions)", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "minced" (Kept as original PREP span)
            (15, 24, "NAME"),  # "scallions"
            # Comma at 24 is "O"
            (26, 47, "COMMENT"),  # "white and green parts" (Kept as original COMMENT span)
            (48, 61, "COMMENT")  # "(4 scallions)" (Kept as original COMMENT span)
        ]
    }),

    # Example 24 (Duplicate)
    ("1/2 cup minced fresh dill", {"entities": [
        (0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (15, 20, "PREP"), (21, 25, "NAME")
    ]}),

    # Example 25
    ("2 pounds fingerling or baby potatoes, scrubbed and halved lengthwise", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 8, "UNIT"),  # "pounds"
            (9, 19, "NAME"),  # "fingerling"
            (20, 36, "ALT_NAME"),  # "or baby potatoes" (Kept as original ALT_NAME span)
            # Comma at 36 is "O"
            (38, 68, "PREP"),  # "scrubbed" (Kept as original PREP span)
        ]
    }),

    # Example 26
    ("1 cup whole-milk ricotta (about 10 ounces)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 16, "NAME"),  # "whole-milk" (from original NAME "whole-milk ricotta" 6-24)
            (17, 24, "NAME"),  # "ricotta" (from original NAME "whole-milk ricotta" 6-24)
            (25, 41, "COMMENT")  # "(about 10 ounces)" (Kept as original COMMENT span)
        ]
    }),

    # Example 27
    ("4 large zucchinis (about 3 pounds)", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "large"
            (8, 17, "NAME"),  # "zucchinis"
            (18, 34, "COMMENT")  # "(about 3 pounds)" (Kept as original COMMENT span)
        ]
    }),

    # Example 28
    ("1/2 cup crumbled Gorgonzola", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 16, "PREP"),  # "crumbled" (Kept as original PREP span)
            (17, 27, "NAME")  # "Gorgonzola"
        ]
    }),

    # Example 29

    # Example 30 (Alternative based on your note "chopped walnuts is a name")
    ("1/2 cup roughly chopped walnuts", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "PREP"),  # "roughly" (Kept as original PREP span)
            (16, 23, "NAME"),  # "chopped" (from original NAME "chopped walnuts" 16-31)
            (24, 31, "NAME")  # "walnuts" (from original NAME "chopped walnuts" 16-31)
        ]
    }),

    # Example 31
    ("1/4 pound gorgonzola dolce", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept as original QTY span)
            (4, 9, "UNIT"),  # "pound"
            (10, 20, "NAME"),  # "gorgonzola" (from original NAME "gorgonzola dolce" 10-26)
            (21, 26, "NAME")  # "dolce" (from original NAME "gorgonzola dolce" 10-26)
        ]
    }),

    # Example 32
    ("1/4 teaspoon red pepper flakes, optional", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept as original QTY span)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 16, "NAME"),  # "red" (from original NAME "red pepper flakes" 13-30)
            (17, 23, "NAME"),  # "pepper" (from original NAME "red pepper flakes" 13-30)
            (24, 30, "NAME"),  # "flakes" (from original NAME "red pepper flakes" 13-30)
            # Comma at 30 is "O"
            (32, 40, "COMMENT")  # "optional" (Kept as original COMMENT span)
        ]
    }),

    # Example 33
    ("Frozen (not in syrup) raspberries", {
        "entities": [
            (0, 6, "PREP"),  # "Frozen" (Kept as original PREP span)
            (7, 21, "COMMENT"),  # "(not in syrup)" (Kept as original COMMENT span)
            (22, 33, "NAME")  # "raspberries"
        ]
    }),

    # Example 34
    ("1/2 ounce Framboise", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 9, "UNIT"),  # "ounce"
            (10, 19, "NAME")  # "Framboise"
        ]
    }),

    # Example 35
    ("1/2 ounce Grand Marnier", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 9, "UNIT"),  # "ounce"
            (10, 15, "NAME"),  # "Grand" (from original NAME "Grand Marnier" 10-23)
            (16, 23, "NAME")  # "Marnier" (from original NAME "Grand Marnier" 10-23)
        ]
    }),

    # Example 36
    ("3/4 cup toasted and chopped pecans", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "PREP"),  # "toasted" (Kept as original PREP span)
            (16, 19, "O"),  # "and"
            (20, 27, "NAME"),
            # "chopped" (from original NAME "chopped pecans" 20-34) - *If "chopped" is PREP, this changes*
            (28, 34, "NAME")  # "pecans" (from original NAME "chopped pecans" 20-34)
        ]
    }),

    # Example 37
    ("1/3 cup plus 3 tablespoons Parmesan", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 26, "COMMENT"),  # "plus 3 tablespoons" (Kept as original COMMENT span)
            (27, 35, "NAME")  # "Parmesan"
        ]
    }),

    # Example 38
    ("2 pounds zucchini (each about 8 inches long and 1 1/2 inches in diameter work best)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 8, "UNIT"),  # "pounds"
            (9, 17, "NAME"),  # "zucchini"
            (18, 83, "COMMENT")
            # "(each about 8 inches long and 1 1/2 inches in diameter work best)" (Kept as original COMMENT span)
        ]
    }),

    # Example 39
    ("6 thin slices prosciutto, halved", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept as original QTY span)
            (2, 6, "PREP"),  # "thin" (from original PREP "thin slices" 2-13)
            (7, 13, "PREP"),  # "slices" (from original PREP "thin slices" 2-13)
            (14, 24, "NAME"),  # "prosciutto"
            # Comma at 24 is "O"
            (26, 32, "PREP")  # "halved" (Kept as original PREP span)
        ]
    }),

    # Example 40
    ("24 very thin slices prosciutto", {
        "entities": [
            (0, 2, "QTY"),  # "24" (Kept as original QTY span)
            (3, 7, "PREP"),  # "very" (from original PREP "very thin slices" 3-19)
            (8, 12, "PREP"),  # "thin" (from original PREP "very thin slices" 3-19)
            (13, 19, "PREP"),  # "slices" (from original PREP "very thin slices" 3-19)
            (20, 30, "NAME")  # "prosciutto"
        ]
    }),

    # Example 41
    ("1/2 honeydew melon", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 12, "NAME"),  # "honeydew" (from original NAME "honeydew melon" 4-18)
            (13, 18, "NAME")  # "melon" (from original NAME "honeydew melon" 4-18)
        ]
    }),

    # Example 42
    ("1 eggplant cut into 8 (1/4-inch) slices", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 10, "NAME"),  # "eggplant"
            (11, 39, "PREP")  # "cut into 8 (1/4-inch) slices" (Kept as original PREP span)
        ]
    }),

    # Example 43
    ("1 yellow squash cut into 8 (1/2-inch) slices", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 8, "NAME"),  # "yellow" (from original NAME "yellow squash" 2-15)
            (9, 15, "NAME"),  # "squash" (from original NAME "yellow squash" 2-15)
            (16, 44, "PREP")  # "cut into 8 (1/2-inch) slices" (Kept as original PREP span)
        ]
    }),

    # Example 44
    ("1/4 cup finely chopped dried dates", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 22, "PREP"),
            # "finely chopped" (from original PREP "finely chopped dried" 8-28) - This is if "dried" is separate
            (23, 28, "PREP"),  # "dried" (from original PREP "finely chopped dried" 8-28)
            (29, 34, "NAME")  # "dates"
        ]
    }),

    # Example 45
    ("Couscous with Dried Dates, recipe follows", {
        "entities": [
            (0, 8, "NAME"),  # "Couscous"
            (9, 13, "PREP"),  # "with" (Kept as original PREP span)
            (14, 19, "NAME"),  # "Dried" (from original NAME "Dried Dates" 14-25)
            (20, 25, "NAME"),  # "Dates" (from original NAME "Dried Dates" 14-25)
            # Comma at 25 is "O"
            (27, 41, "COMMENT")  # "recipe follows" (Kept as original COMMENT span)
        ]
    }),

    # Example 46
    ("1/2 cup pitted and chopped briny olives", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 26, "PREP"),
            # "pitted and chopped" (Kept as original PREP span. Original was (8,32,"PREP") for "pitted and chopped briny")
            (27, 32, "PREP"),  # "briny" (from original PREP "pitted and chopped briny" 8-32)
            (33, 39, "NAME")  # "olives"
        ]
    }),

    # Example 47
    ("1/4 cup dry sherry", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 11, "PREP"),  # "dry" (Kept as original PREP span)
            (12, 18, "NAME")  # "sherry"
        ]
    }),

    # Example 48

    ("4 ounces cremini mushrooms, stemmed and sliced 1/4 inch thick", {  # Corrected based on your original spans
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"),
            (9, 16, "NAME"), (17, 26, "NAME"),  # cremini mushrooms
            (28, 46, "PREP"),  # "stemmed and sliced" (Kept as one PREP as per your original (28,46,"PREP"))
            (47, 61, "COMMENT")  # "1/4 inch thick"
        ]
    }),

    # Example 49
    ("4 ounces shiitake mushrooms, stemmed and sliced 1/4 inch thick", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept as original QTY span)
            (2, 8, "UNIT"),  # "ounces"
            (9, 17, "NAME"),  # "shiitake" (from original NAME "shiitake mushrooms" 9-27)
            (18, 27, "NAME"),  # "mushrooms" (from original NAME "shiitake mushrooms" 9-27)
            # Comma at 27 is "O"
            (29, 47, "PREP"),  # "stemmed and sliced" (Kept as original PREP span)
            (48, 62, "COMMENT")  # "1/4 inch thick" (Kept as original COMMENT span)
        ]
    }),

    # Example 50
    ("Two 15-ounce cans cannellini beans, drained and rinsed", {
        "entities": [
            (0, 3, "QTY"),  # "Two" (Kept as original QTY span)
            (4, 12, "COMMENT"),  # "15-ounce" (Kept as original COMMENT span)
            (13, 17, "UNIT"),  # "cans"
            (18, 28, "NAME"),  # "cannellini" (from original NAME "cannellini beans" 18-34)
            (29, 34, "NAME"),  # "beans" (from original NAME "cannellini beans" 18-34)
            # Comma at 34 is "O"
            (36, 54, "PREP")  # "drained and rinsed" (Kept as original PREP span)
        ]
    }),

    # Example 51
    ("1 cup fresh flat-leaf parsley leaves, finely chopped, plus more for garnish, optional", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 11, "PREP"),  # "fresh" (Kept as original PREP span)
            (12, 21, "NAME"),  # "flat-leaf" (from original NAME "flat-leaf parsley leaves" 12-36)
            (22, 29, "NAME"),  # "parsley" (from original NAME "flat-leaf parsley leaves" 12-36)
            (30, 36, "NAME"),  # "leaves" (from original NAME "flat-leaf parsley leaves" 12-36)
            # Comma at 36 is "O"
            (38, 52, "PREP"),  # "finely chopped" (Kept as original PREP span)
            # Comma at 52 is "O"
            (54, 85, "COMMENT")  # "plus more for garnish, optional" (Kept as original COMMENT span)
        ]
    }),

    # Example 52
    ("2 red onions, 1 cut into 1/4-inch dice and 1 sliced for garnish", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 5, "NAME"),  # "red" (from original NAME "red onions" 2-12)
            (6, 12, "NAME"),  # "onions" (from original NAME "red onions" 2-12)
            # Comma at 12 is "O"
            (14, 63, "COMMENT")  # "1 cut into 1/4-inch dice and 1 sliced for garnish" (Kept as original COMMENT span)
        ]
    }),

    # Example 53
    ("1/2 bunch fresh dill, finely chopped", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 9, "UNIT"),  # "bunch"
            (10, 15, "PREP"),  # "fresh" (Kept as original PREP span)
            (16, 20, "NAME"),  # "dill"
            # Comma at 20 is "O"
            (22, 36, "PREP")  # "finely chopped" (Kept as original PREP span)
        ]
    }),

    # Example 54
    ("Zest of 1/2 lemon", {
        "entities": [
            (0, 4, "NAME"),  # "Zest"
            (5, 7, "PREP"),  # "of" (Kept as original PREP span)
            (8, 11, "QTY"),  # "1/2" (Kept as original QTY span)
            (12, 17, "NAME")  # "lemon"
        ]
    }),

    # Example 55
    ("4 Whole-Wheat Pitas, recipe follows, or 4 seeded hamburger buns", {
        "entities": [
            # Primary Item
            (0, 1, "QTY"),         # "4"
            (2, 13, "NAME"),       # "Whole-Wheat"
            (14, 19, "NAME"),      # "Pitas"
            # Comma at 19 is O
            (21, 35, "COMMENT"),   # "recipe follows"
            # Comma at 35 is O
            (37,39,'ALT_NAME'),
            (40, 41, "ALT_QTY"),   # "4" (quantity for the alternative item)
            (42, 48, "PREP"),      # "seeded" (preparation/description of the alternative item)
            (49, 58, "ALT_NAME"),  # "hamburger" (alternative ingredient name part)
            (59, 63, "ALT_NAME")   # "buns" (alternative ingredient name part)
        ]
    }),

    # Example 56
    ("2 mint tea bags", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 6, "NAME"),  # "mint" (from original NAME "mint tea" 2-10)
            (7, 10, "NAME"),  # "tea" (from original NAME "mint tea" 2-10)
            (11, 15, "UNIT")  # "bags"
        ]
    }),

    # Example 58
    ("1/2 bunch fresh mint, finely chopped", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 9, "UNIT"),  # "bunch"
            (10, 15, "PREP"),  # "fresh" (Kept as original PREP span)
            (16, 20, "NAME"),  # "mint"
            # Comma at 20 is "O"
            (22, 36, "PREP")  # "finely chopped" (Kept as original PREP span)
        ]
    }),

    # Example 59
    ("1 tablespoon chopped mint leaves", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 20, "PREP"),  # "chopped" (Kept as original PREP span)
            (21, 25, "NAME"),  # "mint" (from original NAME "mint leaves" 21-32)
            (26, 32, "NAME")  # "leaves" (from original NAME "mint leaves" 21-32)
        ]
    }),

    # Example 60
    ("4 (6-ounce) bluefish fillets, skin on", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept as original QTY span)
            (2, 11, "COMMENT"),  # "(6-ounce)" (Kept as original COMMENT span)
            (12, 20, "NAME"),  # "bluefish" (from original NAME "bluefish fillets" 12-28)
            (21, 28, "NAME"),  # "fillets" (from original NAME "bluefish fillets" 12-28)
            # Comma at 28 is "O"
            (30, 37, "COMMENT")  # "skin on" (Kept as original COMMENT span)
        ]
    }),

    # Example 61
    ("1 teaspoon toasted and crushed coriander seeds", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 30, "PREP"),  # "toasted and crushed" (Kept as original PREP span)
            (31, 40, "NAME"),  # "coriander" (from original NAME "coriander seeds" 31-46)
            (41, 46, "NAME")  # "seeds" (from original NAME "coriander seeds" 31-46)
        ]
    }),

    # Example 62
    ("1 cup chicken stock, plus more as needed", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 13, "NAME"),  # "chicken" (from original NAME "chicken stock" 6-19)
            (14, 19, "NAME"),  # "stock" (from original NAME "chicken stock" 6-19)
            # Comma at 19 is "O"
            (21, 40, "COMMENT")  # "plus more as needed" (Kept as original COMMENT span)
        ]
    }),

    # Example 63
    ("Two 15.5-ounce cans pinto beans, drained and rinsed", {
        "entities": [
            (0, 3, "QTY"),  # "Two" (Kept as original QTY span)
            (4, 14, "COMMENT"),  # "15.5-ounce" (Kept as original COMMENT span)
            (15, 19, "UNIT"),  # "cans"
            (20, 25, "NAME"),  # "pinto" (from original NAME "pinto beans" 20-31)
            (26, 31, "NAME"),  # "beans" (from original NAME "pinto beans" 20-31)
            # Comma at 31 is "O"
            (33, 51, "PREP")  # "drained and rinsed" (Kept as original PREP span)
        ]
    }),

    # Example 64
    ("1/2 teaspoon coriander", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 22, "NAME")  # "coriander"
        ]
    }),

    # Example 65
    ("Three 15-ounce cans black-eyed peas, rinsed", {
        "entities": [
            (0, 5, "QTY"),  # "Three" (Kept as original QTY span)
            (6, 14, "COMMENT"),  # "15-ounce" (Kept as original COMMENT span)
            (15, 19, "UNIT"),  # "cans"
            (20, 30, "NAME"),  # "black-eyed" (from original NAME "black-eyed peas" 20-35)
            (31, 35, "NAME"),  # "peas" (from original NAME "black-eyed peas" 20-35)
            # Comma at 35 is "O"
            (37, 43, "PREP")  # "rinsed" (Kept as original PREP span)
        ]
    }),

    # Example 66
    ("2 T-bone steaks, each about 1 1/2 pounds and 1 1/2 to 2 inches thick", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 8, "NAME"),  # "T-bone" (from original NAME "T-bone steaks" 2-15)
            (9, 15, "UNIT"),  # "steaks" (Original label was UNIT)
            # Comma at 15 is "O"
            (17, 68, "COMMENT")  # "each about 1 1/2 pounds and 1 1/2 to 2 inches thick" (Kept as original COMMENT span)
        ]
    }),

    # Example 67
    ("Finely grated zest and juice from 1 lime", {
        "entities": [
            (0, 6, "PREP"),  # "Finely" (Original PREP (0,6))
            (7, 13, "PREP"),  # "grated" (Original PREP (7,13))
            (14, 28, "NAME"),  # "zest"
            (29, 33, "PREP"),  # "from" (Original PREP (29,33))
            (34, 35, "QTY"),  # "1" (Kept as original QTY span)
            (36, 40, "NAME")  # "lime"
        ]
    }),

    # Example 68
    ("1 cup (240 ml) ice cubes", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 14, "COMMENT"),  # "(240 ml)" (Kept as original COMMENT span)
            (15, 18, "NAME"),  # "ice" (from original NAME "ice cubes" 15-24)
            (19, 24, "NAME")  # "cubes" (from original NAME "ice cubes" 15-24)
        ]
    }),

    # Example 69
    ("*Note: Regular limes work fine. #NotBougie", {
        "entities": [
            (0, 42, "COMMENT")  # Kept as original COMMENT span
        ]
    }),

    # Example 70
    ("1 1/2 teaspoons confectioners? sugar", {  # Question mark likely a typo for apostrophe
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept as original QTY span)
            (6, 15, "UNIT"),  # "teaspoons"
            # Let's assume original was (16,30,"NAME") for "confectioners? sugar" and "?" is part of first token.
            (16, 29, "NAME"),  # "confectioners?"
            (31, 36, "NAME")  # "sugar"
        ]
    }),
    ("1 1/2 teaspoons confectioners' sugar", {  # Assuming corrected typo and "confectioners'" is one token
        "entities": [
            (0, 5, "QTY"),
            (6, 15, "UNIT"),
            (16, 30, "NAME"),  # "confectioners'" (from original "confectioners' sugar")
            (31, 36, "NAME")  # "sugar" (from original "confectioners' sugar")
        ]
    }),

    # Example 71
    ("1/2 cup freshly squeezed Key lime juice*", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "PREP"),  # "freshly" (from original PREP "freshly squeezed" 8-24)
            (16, 24, "PREP"),  # "squeezed" (from original PREP "freshly squeezed" 8-24)
            (25, 28, "NAME"),  # "Key" (from original NAME "Key lime juice*" 25-40)
            (29, 33, "NAME"),  # "lime" (from original NAME "Key lime juice*" 25-40)
            (34, 40, "NAME")  # "juice*" (from original NAME "Key lime juice*" 25-40, includes *)
        ]
    }),

    # Example 72
    ("1 teaspoon grated Key lime zest*, plus more for topping", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 17, "PREP"),  # "grated" (Kept as original PREP span)
            (18, 21, "NAME"),  # "Key" (from original NAME "Key lime zest*" 18-32)
            (22, 26, "NAME"),  # "lime" (from original NAME "Key lime zest*" 18-32)
            (27, 32, "NAME"),  # "zest*" (from original NAME "Key lime zest*" 18-32, includes *)
            # Comma at 32 is "O"
            (34, 55, "COMMENT")  # "plus more for topping" (Kept as original COMMENT span)
        ]
    }),

    # Example 74
    ("Jazz apricot can be substituted for the apricots, honey, and jalapenos", {
        "entities": [
            (0, 70, "COMMENT")  # Kept as original COMMENT span
        ]
    }),

    # Example 75
    ("1 (15 1/4-ounce) can apricots, drained and finely chopped", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 16, "COMMENT"),  # "(15 1/4-ounce)" (Kept)
            (17, 20, "UNIT"),  # "can"
            (21, 29, "NAME"),  # "apricots"
            # Comma at 29 is "O"
            (31, 57, "PREP")  # "drained and finely chopped" (Kept)
        ]
    }),

    # Example 76
    ("1/4 cup seeded and finely chopped jalapenos", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 33, "PREP"),  # "seeded and finely chopped" (Kept)
            (34, 43, "NAME")  # "jalapenos"
        ]
    }),

    # Example 77
    ("1/2 cup whipped topping, plus more for topping", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "NAME"),  # "whipped" (Kept)
            (16, 23, "NAME"),  # "topping"
            # Comma at 23 is "O"
            (25, 46, "COMMENT")  # "plus more for topping" (Kept)
        ]
    }),

    # Example 78
    ("2 shots espresso, or 1/2 cup very strong coffee", {
        "entities": [
            # Primary Item
            (0, 1, "QTY"),         # "2"
            (2, 7, "COMMENT"),     # "shots" (Not an allowed UNIT from your list for this context)
            (8, 16, "NAME"),       # "espresso"
            # Comma at 16 is O
            (18,20,'ALT_NAME'),
            # Alternative Item
            (21, 24, "ALT_QTY"),   # "1/2" (quantity for the alternative item)
            (25, 28, "ALT_UNIT"),  # "cup" (unit for the alternative item)
            (29, 33, "PREP"),      # "very" (part of "very strong")
            (34, 40, "PREP"),      # "strong" (preparation/description of the alternative item)
            (41, 47, "ALT_NAME")   # "coffee" (alternative ingredient name)
        ]
    }),

    # Example 79 (Duplicate)
    ("1 cup ice cubes", {"entities": [
        (0, 1, "QTY"), (2, 5, "UNIT"),
        (6, 9, "NAME"), (10, 15, "NAME")]}),  # ice cubes

    # Example 80
    ("6 large tortillas", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 7, "UNIT"),  # "large"
            (8, 17, "NAME")  # "tortillas"
        ]
    }),

    # Example 81
    ("1 tablespoon dark rum", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 17, "NAME"),  # "dark" (from original NAME "dark rum" 13-21)
            (18, 21, "NAME")  # "rum" (from original NAME "dark rum" 13-21)
        ]
    }),
    # Re-annotated data based on the FINAL REFINED rules:
    # - NAME entities are broken into word-level NAME entities.
    # - COMMENT, PREP, ALT_NAME, QTY entities are kept as single, original spans.
    # - UNIT entities are single words.
    # - Commas and other non-entity words become "O" (and are thus not listed in the 'entities' list).
    # Tokenization based on spaCy's default English tokenizer.

    # Example 1
    ("2 tablespoons pine nuts, toasted, to garnish", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 18, "NAME"),  # "pine" (from original NAME "pine nuts" 14-23)
            (19, 23, "NAME"),  # "nuts" (from original NAME "pine nuts" 14-23)
            # Comma at 23 is "O"
            (25, 32, "PREP"),  # "toasted" (Kept as original PREP span)
            # Comma at 32 is "O"
            (34, 44, "COMMENT")  # "to garnish" (Kept as original COMMENT span)
        ]
    }),

    # Example 2
    ("3 small eggplants (1 to 1 1/2 pounds) to make about 1 1/4 cups when roasted, pulped and sieved", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "small"
            (8, 17, "NAME"),  # "eggplants"
            (18, 94, "COMMENT")
            # "(1 to 1 1/2 pounds) to make about 1 1/4 cups when roasted, pulped and sieved" (Kept as original COMMENT span)
        ]
    }),

    # Example 3
    ("1 cup Greek yogurt", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 11, "NAME"),  # "Greek" (from original NAME "Greek yogurt" 6-18)
            (12, 18, "NAME")  # "yogurt" (from original NAME "Greek yogurt" 6-18)
        ]
    }),

    # Example 4
    ("1/4 teaspoon saffron threads, soaked in 2 tablespoons warm water", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept as original QTY span)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 20, "NAME"),  # "saffron" (from original NAME "saffron threads" 13-28)
            (21, 28, "NAME"),  # "threads" (from original NAME "saffron threads" 13-28)
            # Comma at 28 is "O"
            (30, 64, "PREP")  # "soaked in 2 tablespoons warm water" (Kept as original PREP span)
        ]
    }),

    # Example 5
    ("3 cups peeled and shredded carrots", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 6, "UNIT"),  # "cups"
            (7, 26, "PREP"),  # "peeled and shredded" (Kept as original PREP span)
            (27, 34, "NAME")  # "carrots"
        ]
    }),

    # Example 6
    ("4 cups reduced-fat milk", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept as original QTY span)
            (2, 6, "UNIT"),  # "cups"
            (7, 18, "PREP"),  # "reduced-fat" (Kept as original PREP span)
            (19, 23, "NAME")  # "milk"
        ]
    }),

    # Example 7
    ("1 ounce whisky", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "ounce"
            (8, 14, "NAME")  # "whisky"
        ]
    }),

    # Example 8
    ("2 pellets achiote", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 9, "NAME"),  # "pellets" (from original NAME "pellets achiote" 2-17)
            (10, 17, "NAME")  # "achiote" (from original NAME "pellets achiote" 2-17)
        ]
    }),

    # Example 9
    ("1/2 cup crushed biscotti", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "PREP"),  # "crushed" (Kept as original PREP span)
            (16, 24, "NAME")  # "biscotti"
        ]
    }),

    # Example 10
    ("1/2 teaspoon orange zest", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 19, "NAME"),  # "orange" (from original NAME "orange zest" 13-24)
            (20, 24, "NAME")  # "zest" (from original NAME "orange zest" 13-24)
        ]
    }),

    # Example 11
    ("3 tablespoons salted butter, at room temperature", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 20, "NAME"),  # "salted" (from original NAME "salted butter" 14-27)
            (21, 27, "NAME"),  # "butter" (from original NAME "salted butter" 14-27)
            # Comma at 27 is "O"
            (29, 48, "COMMENT")  # "at room temperature" (Kept as original COMMENT span)
        ]
    }),

    # Example 12
    ("1/2 cup chicken fat", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "NAME"),  # "chicken"
            (16, 19, "NAME")  # "fat"
        ]
    }),

    # Example 13
    ("2 tablespoons plus 2 teaspoons schmaltz (rendered chicken fat)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 30, "COMMENT"),  # "plus 2 teaspoons" (Kept as original COMMENT span)
            (31, 39, "NAME"),  # "schmaltz"
            (40, 62, "COMMENT")  # "(rendered chicken fat)" (Kept as original COMMENT span)
        ]
    }),

    # Example 14
    ("1 pound frozen peeled and deveined jumbo shrimp (16/20)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "pound"
            (8, 34, "PREP"),  # "frozen peeled and deveined" (Kept as original PREP span)
            (35, 40, "NAME"),  # "jumbo" (from original NAME "jumbo shrimp" 35-47)
            (41, 47, "NAME"),  # "shrimp" (from original NAME "jumbo shrimp" 35-47)
            (48, 55, "COMMENT")  # "(16/20)" (Kept as original COMMENT span)
        ]
    }),

    # Example 15
    ("4 (4-ounce) sole fillets, hake, flounder or other white fish", {
        "entities": [
            # Primary Item
            (0, 1, "QTY"),         # "4"
            (2, 11, "COMMENT"),    # "(4-ounce)" (Describes the sole fillets)
            (12, 16, "NAME"),      # "sole"
            (17, 24, "NAME"),      # "fillets"
            # Comma at 24 is O
            # Alternatives
            (26, 30, "ALT_NAME"),  # "hake"
            # Comma at 30 is O
            (32, 40, "ALT_NAME"),  # "flounder"
            (41, 60, "ALT_NAME")   # "or other white fish" (The entire phrase as one ALT_NAME)
        ]
    }),

    # Example 16
    ("1 1/2 cups rainbow nonpareils, large and small mixed", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept as original QTY span)
            (6, 10, "UNIT"),  # "cups"
            (11, 18, "NAME"),  # "rainbow" (from original NAME "rainbow nonpareils" 11-29)
            (19, 29, "NAME"),  # "nonpareils" (from original NAME "rainbow nonpareils" 11-29)
            # Comma at 29 is "O"
            (31, 52, "COMMENT")  # "large and small mixed" (Kept as original COMMENT span)
        ]
    }),

    # Example 17
    ("1 cup diced firm tofu", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 11, "PREP"),  # "diced" (from original PREP "diced firm" 6-16)
            (12, 16, "PREP"),  # "firm" (from original PREP "diced firm" 6-16)
            (17, 21, "NAME")  # "tofu"
        ]
    }),

    # Example 18
    ("4 ounces rum, such as Mount Gay", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept as original QTY span)
            (2, 8, "UNIT"),  # "ounces"
            (9, 12, "NAME"),  # "rum"
            # Comma at 12 is "O"
            (14, 31, "COMMENT")  # "such as Mount Gay" (Kept as original COMMENT span)
        ]
    }),

    # Example 19
    ("1/2 cup small dice of mixed yellow, green and red bell pepper, for garnish", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "PREP"),  # "small" (from original PREP "small dice of" 8-21)
            (14, 18, "PREP"),  # "dice" (from original PREP "small dice of" 8-21)
            (19, 21, "PREP"),
            # "of" (from original PREP "small dice of" 8-21) - *Unusual, but following "keep PREP as is"*

            (22, 49, "ALT_NAME"),  # "red" (from original NAME 22-61)
            (50, 61, "NAME"),  # "bell" (from original NAME 22-61)
            # Comma at 61 is "O"
            (63, 74, "COMMENT")  # "for garnish" (Kept as original COMMENT span)
        ]
    }),

    # Example 20
    ("1 pound orzo", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "pound"
            (8, 12, "NAME")  # "orzo"
        ]
    }),

    # Example 21
    ("1 cup pearled farro", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 13, "PREP"),  # "pearled" (Kept as original PREP span)
            (14, 19, "NAME")  # "farro"
        ]
    }),

    # Example 22
    ("1 small bulb fennel, trimmed, halved and thinly sliced", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "small"
            (8, 12, "NAME"),  # "bulb" (from original NAME "bulb fennel" 8-19)
            (13, 19, "NAME"),  # "fennel" (from original NAME "bulb fennel" 8-19)
            # Comma at 19 is "O"
            (21, 54, "PREP")  # "trimmed, halved and thinly sliced" (Kept as original PREP span)
        ]
    }),

    # Example 23 (Duplicate: 1 cup Greek yogurt)
    ("1 cup Greek yogurt", {"entities": [
        (0, 1, "QTY"), (2, 5, "UNIT"),
        (6, 11, "NAME"), (12, 18, "NAME")  # Greek, yogurt
    ]}),

    # Example 24
    ("1/4 cup toasted pine nuts* see Cook's Note", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "PREP"),  # "toasted" (Kept as original PREP span)
            (16, 20, "NAME"),  # "pine" (from original NAME "pine nuts*" 16-26)
            (21, 26, "NAME"),  # "nuts*" (from original NAME "pine nuts*" 16-26, includes *)
            (27, 42, "COMMENT")  # "see Cook's Note" (Kept as original COMMENT span)
        ]
    }),

    # Example 25
    ("1 pear", {"entities": [
        (0, 1, "QTY"),  # "1" (Kept as original QTY span)
        (2, 6, "NAME")  # "pear"
    ]}),

    # Example 26
    ("4 pounds wings, separated into wingettes and drumettes, tips discarded", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept as original QTY span)
            (2, 8, "UNIT"),  # "pounds"
            (9, 14, "NAME"),  # "wings"
            # Comma at 14 is "O"
            (16, 54, "PREP"),  # "separated into wingettes and drumettes" (Kept as original PREP span)
            # Comma at 54 is "O"
            (56, 70, "COMMENT")  # "tips discarded" (Kept as original COMMENT span)
        ]
    }),

    # Example 27
    ("5 tablespoons whole Greek yogurt", {
        "entities": [
            (0, 1, "QTY"),  # "5" (Kept as original QTY span)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 19, "NAME"),  # "whole"
            (20, 25, "NAME"),  # "Greek" (from original NAME "Greek yogurt" 20-32)
            (26, 32, "NAME")  # "yogurt" (from original NAME "Greek yogurt" 20-32)
        ]
    }),

    # Example 28
    ("1 teaspoon black mustard seeds", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 16, "NAME"),  # "black" (from original NAME "black mustard seeds" 11-30)
            (17, 24, "NAME"),  # "mustard" (from original NAME "black mustard seeds" 11-30)
            (25, 30, "NAME")  # "seeds" (from original NAME "black mustard seeds" 11-30)
        ]
    }),

    # Example 29
    ("Small handful fresh cilantro, leaves and soft stems rustically ripped into bite-size pieces", {
        "entities": [
            (0, 5, "UNIT"),  # "Small" (Original label was UNIT)
            (6, 13, "COMMENT"),  # "handful" (Original label was COMMENT)
            (14, 19, "PREP"),  # "fresh" (Kept as original PREP span)
            (20, 28, "NAME"),  # "cilantro"
            # Comma at 28 is "O"
            (30, 91, "PREP")
            # "leaves and soft stems rustically ripped into bite-size pieces" (Kept as original PREP span)
        ]
    }),

    # Example 30
    ("Big pinch ground cardamom", {
        "entities": [
            (0, 3, "QTY"),  # "Big" (Kept as original QTY span)
            (4, 9, "COMMENT"),  # "pinch" (Kept as original COMMENT span)
            (10, 16, "NAME"),  # "ground" (from original NAME "ground cardamom" 10-25)
            (17, 25, "NAME")  # "cardamom" (from original NAME "ground cardamom" 10-25)
        ]
    }),  # Using your corrected version for this one.

    # Example 31
    ("Big pinch chaat masala", {
        "entities": [
            (0, 3, "QTY"),  # "Big" (Kept as original QTY span)
            (4, 9, "COMMENT"),  # "pinch" (Kept as original COMMENT span)
            (10, 15, "NAME"),  # "chaat" (from original NAME "chaat masala" 10-22)
            (16, 22, "NAME")  # "masala" (from original NAME "chaat masala" 10-22)
        ]
    }),

    # Example 32
    ("3 large ears corn, husks and silk removed", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "large"
            (8, 12, "UNIT"),  # "ears"
            (13, 17, "NAME"),  # "corn"
            # Comma at 17 is "O"
            (19, 41, "PREP")  # "husks and silk removed" (Kept as original PREP span)
        ]
    }),

    # Example 33
    ("Olive oil", {"entities": [
        (0, 5, "NAME"),  # "Olive" (from original NAME "Olive oil" 0-9)
        (6, 9, "NAME")  # "oil" (from original NAME "Olive oil" 0-9)
    ]}),

    # Example 34
    ("1 pound peeled and deveined large shrimp", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "pound"
            (8, 27, "PREP"),  # "peeled and deveined" (Kept as original PREP span)
            (28, 33, "NAME"),  # "large" (Original label was UNIT)
            (34, 40, "NAME")  # "shrimp"
        ]
    }),

    # Example 35
    ("4 ounces dark rum", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept as original QTY span)
            (2, 8, "UNIT"),  # "ounces"
            (9, 13, "NAME"),  # "dark" (from original NAME "dark rum" 9-17)
            (14, 17, "NAME")  # "rum" (from original NAME "dark rum" 9-17)
        ]
    }),

    ("1 package (10 oz.) frozen chopped spinach, thawed and squeezed dry", {  # Corrected for spinach as NAME
        "entities": [
            (0, 1, "QTY"),
            (2, 9, "UNIT"),
            (10, 18, "COMMENT"),
            (19, 25, "PREP"),  # "frozen"
            (26, 33, "PREP"),  # "chopped"
            (34, 41, "NAME"),  # "spinach"
            (43, 66, "PREP")  # "thawed and squeezed dry"
        ]
    }),

    # Example 37
    ("1/2 pound turnips, diced", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 9, "UNIT"),  # "pound"
            (10, 17, "NAME"),  # "turnips"
            # Comma at 17 is "O"
            (19, 24, "PREP")  # "diced" (Kept as original PREP span)
        ]
    }),

    # Example 38
    ("2 pounds goat head, organs and feet (2 pounds lamb meat may be substituted)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 8, "UNIT"),  # "pounds"
            (9, 13, "NAME"),  # "goat" (from original NAME "goat head" 9-18)
            (14, 18, "NAME"),  # "head" (from original NAME "goat head" 9-18)
            # Comma at 18 is "O"
            (20, 75, "COMMENT"),  # "organs" (Original label was COMMENT)
        ]
    }),

    # Example 39
    ("1 1/4 teaspoons black mustard seeds", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/4" (Kept as original QTY span)
            (6, 15, "UNIT"),  # "teaspoons"
            (16, 21, "NAME"),  # "black" (from original NAME "black mustard seeds" 16-35)
            (22, 29, "NAME"),  # "mustard" (from original NAME "black mustard seeds" 16-35)
            (30, 35, "NAME")  # "seeds" (from original NAME "black mustard seeds" 16-35)
        ]
    }),

    # Example 40
    ("2 cups loosely packed fresh morels", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 6, "UNIT"),  # "cups"
            (7, 27, "PREP"),  # "loosely" (from original PREP "loosely packed fresh" 7-27)
            (28, 34, "NAME")  # "morels"
        ]
    }),

    # Example 41
    ("1 cup peeled and diced kiwi (about 2 or 3 whole kiwi)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "PREP"),  # "peeled" (Original was (6,12,"PREP"), then (17,27,"NAME") "diced kiwi")
            # This means "and diced" were not part of PREP. "diced" is part of NAME.
            (13, 16, "O"),  # "and"
            (17, 22, "NAME"),  # "diced" (from original NAME "diced kiwi" 17-27)
            (23, 27, "NAME"),  # "kiwi" (from original NAME "diced kiwi" 17-27)
            (28, 53, "COMMENT")  # "(about 2 or 3 whole kiwi)" (Kept as original COMMENT span)
        ]
    }),

    # Example 42
    ("1 cup diced pineapple (fresh or canned in juice)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 11, "NAME"),  # "diced" (from original NAME "diced pineapple" 6-21)
            (12, 21, "NAME"),  # "pineapple" (from original NAME "diced pineapple" 6-21)
            (22, 48, "COMMENT")  # "(fresh or canned in juice)" (Kept as original COMMENT span)
        ]
    }),

    # Example 43
    ("1/2 cup 151-proof rum", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 17, "PREP"),  # "151-proof" (Kept as original PREP span)
            (18, 21, "NAME")  # "rum"
        ]
    }),

    # Example 44
    ("1 cup macadamia nuts, toasted and coarsely ground", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 15, "NAME"),  # "macadamia" (from original NAME "macadamia nuts" 6-20)
            (16, 20, "NAME"),  # "nuts" (from original NAME "macadamia nuts" 6-20)
            # Comma at 20 is "O"
            (22, 49, "PREP")  # "toasted and coarsely ground" (Kept as original PREP span)
        ]
    }),

    # Example 45
    ("2 1/2 cups lightly crushed potato chips with ridges", {
        "entities": [
            (0, 5, "QTY"),  # "2 1/2" (Kept as original QTY span)
            (6, 10, "UNIT"),  # "cups"
            (11, 26, "PREP"),  # "lightly" (from original PREP "lightly crushed" 11-26)
            (27, 33, "NAME"),  # "potato" (from original NAME "potato chips" 27-39)
            (34, 39, "NAME"),  # "chips" (from original NAME "potato chips" 27-39)
            (40, 51, "COMMENT")  # "with ridges" (Kept as original COMMENT span)
        ]
    }),

    # Example 46
    ("Nonstick cooking spray, for the parchment", {
        "entities": [
            (0, 8, "NAME"),  # "Nonstick" (from original NAME "Nonstick cooking spray" 0-22)
            (9, 16, "NAME"),  # "cooking" (from original NAME "Nonstick cooking spray" 0-22)
            (17, 22, "NAME"),  # "spray" (from original NAME "Nonstick cooking spray" 0-22)
            # Comma at 22 is "O"
            (24, 41, "COMMENT")  # "for the parchment" (Kept as original COMMENT span)
        ]
    }),

    # Example 47
    ("4 ounces kombu", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept as original QTY span)
            (2, 8, "UNIT"),  # "ounces"
            (9, 14, "NAME")  # "kombu"
        ]
    }),

    # Example 48
    ("2 cups cooked and cooled Carolina Gold rice (from 3/4 cup uncooked rice)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 6, "UNIT"),  # "cups"
            (7, 24, "PREP"),  # "cooked and cooled" (Kept as original PREP span)
            (25, 33, "NAME"),  # "Carolina" (from original NAME "Carolina Gold rice" 25-43)
            (34, 38, "NAME"),  # "Gold" (from original NAME "Carolina Gold rice" 25-43)
            (39, 43, "NAME"),  # "rice" (from original NAME "Carolina Gold rice" 25-43)
            (44, 71, "COMMENT")  # "(from 3/4 cup uncooked rice)" (Kept as original COMMENT span)
        ]
    }),

    # Example 49
    ("Canola or vegetable oil, for frying", {
        "entities": [
            (0, 6, "NAME"),  # "Canola"
            (7, 19, "ALT_NAME"),  # "or vegetable oil" (Kept as original ALT_NAME span)
            (20, 23, "NAME"),  # " oil" (Kept as original ALT_NAME span)
            # Comma at 23 is "O"
            (25, 35, "COMMENT")  # "for frying" (Kept as original COMMENT span)
        ]
    }),

    # Example 50
    ("1/4 cup spiced rum", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "NAME"),  # "spiced" (from original NAME "spiced rum" 8-18)
            (15, 18, "NAME")  # "rum" (from original NAME "spiced rum" 8-18)
        ]
    }),

    # Example 51
    ("About 1/3 cup EVOO", {
        "entities": [
            (0, 5, "COMMENT"),  # "About" (Kept as original COMMENT span)
            (6, 9, "QTY"),  # "1/3" (Kept as original QTY span)
            (10, 13, "UNIT"),  # "cup"
            (14, 18, "NAME")  # "EVOO"
        ]
    }),

    # Example 52
    ("Generous handful of fresh cilantro leaves, chopped", {
        "entities": [
            (0, 8, "QTY"),  # "Generous" (Kept as original QTY span)
            (9, 16, "UNIT"),  # "handful"
            (17, 19, "PREP"),  # "of" (Kept as original PREP span. Original (17,25,"PREP") "of fresh")
            (20, 25, "PREP"),  # "fresh" (from original PREP "of fresh" 17-25)
            (26, 34, "NAME"),  # "cilantro" (from original NAME "cilantro leaves" 26-41)
            (35, 41, "NAME"),  # "leaves" (from original NAME "cilantro leaves" 26-41)
            # Comma at 41 is "O"
            (43, 50, "PREP")  # "chopped" (Kept as original PREP span)
        ]
    }),

    # Example 53
    ("1 pound haricot verts, blanched and shocked", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "pound"
            (8, 15, "NAME"),  # "haricot" (from original NAME "haricot verts" 8-21)
            (16, 21, "NAME"),  # "verts" (from original NAME "haricot verts" 8-21)
            # Comma at 21 is "O"
            (23, 43, "PREP")  # "blanched and shocked" (Kept as original PREP span)
        ]
    }),

    # Example 54
    ("12 scallops", {"entities": [
        (0, 2, "QTY"),  # "12" (Kept as original QTY span)
        (3, 11, "NAME")  # "scallops"
    ]}),

    # Example 55
    ("1/2 cup walnut pieces", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "NAME"),  # "walnut"
            (15, 21, "PREP")  # "pieces" (Kept as original PREP span)
        ]
    }),

    # Example 56
    ("1/3 cup minced scallion, including green", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "minced" (Kept as original PREP span)
            (15, 23, "NAME"),  # "scallion"
            # Comma at 23 is "O"
            (25, 40, "COMMENT")  # "including green" (Kept as original COMMENT span)
        ]
    }),

    # Example 57
    ("1/2 pound cooked shrimp or other shellfish", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 9, "UNIT"),  # "pound"
            (10, 16, "PREP"),  # "cooked" (Kept as original PREP span)
            (17, 23, "NAME"),  # "shrimp"
            (24, 42, "ALT_NAME")  # "or other shellfish" (Kept as original ALT_NAME span)
        ]
    }),

    # Example 58
    ("1/2 pound mixed baby greens", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 9, "UNIT"),  # "pound"
            (10, 15, "PREP"),  # "mixed" (Kept as original PREP span)
            (16, 20, "NAME"),  # "baby" (from original NAME "baby greens" 16-27)
            (21, 27, "NAME")  # "greens" (from original NAME "baby greens" 16-27)
        ]
    }),

    # Example 59
    ("1 pound package instant polenta", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "pound"
            (8, 15, "COMMENT"),  # "package" (Original label was COMMENT)
            (16, 23, "PREP"),  # "instant" (Kept as original PREP span)
            (24, 31, "NAME")  # "polenta"
        ]
    }),

    # Example 60
    ("Vegetable oil, for greasing pan", {
        "entities": [
            (0, 9, "NAME"),  # "Vegetable" (from original NAME "Vegetable oil" 0-13)
            (10, 13, "NAME"),  # "oil" (from original NAME "Vegetable oil" 0-13)
            # Comma at 13 is "O"
            (15, 31, "COMMENT")  # "for greasing pan" (Kept as original COMMENT span)
        ]
    }),

    # Example 61
    ("1 pound cavatelli or any short pasta (penne, paccheri, ziti…)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "pound"
            (8, 17, "NAME"),  # "cavatelli"
            (18, 61, "ALT_NAME")  # "or any short pasta (penne, paccheri, ziti…)" (Kept as original ALT_NAME span)
        ]
    }),

    # Example 62
    ("1 teaspoon prepared horseradish", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 19, "PREP"),  # "prepared" (Kept as original PREP span)
            (20, 31, "NAME")  # "horseradish"
        ]
    }),

    # Example 63
    ("6 frozen parathas (see Cook's Note)", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept as original QTY span)
            (2, 8, "PREP"),  # "frozen" (Kept as original PREP span)
            (9, 17, "NAME"),  # "parathas"
            (18, 35, "COMMENT")  # "(see Cook's Note)" (Kept as original COMMENT span)
        ]
    }),

    # Example 64
    ("6 ears fresh corn on the cob, shucked", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept as original QTY span)
            (2, 6, "UNIT"),  # "ears"
            (7, 12, "PREP"),  # "fresh" (Kept as original PREP span)
            (13, 17, "NAME"),  # "corn"
            (18, 28, "COMMENT"),  # "on the cob" (Kept as original COMMENT span)
            # Comma at 28 is "O"
            (30, 37, "PREP")  # "shucked" (Kept as original PREP span)
        ]
    }),

    # Example 65
    ("15 ounces drained canned chestnuts packed in water", {
        "entities": [
            (0, 2, "QTY"),  # "15" (Kept as original QTY span)
            (3, 9, "UNIT"),  # "ounces"
            (10, 17, "PREP"),  # "drained" (from original PREP "drained canned" 10-24)
            (18, 24, "PREP"),  # "canned" (from original PREP "drained canned" 10-24)
            (25, 34, "NAME"),  # "chestnuts"
            (35, 50, "PREP")  # "packed in water" (Kept as original PREP span)
        ]
    }),

    # Example 66
    ("1/2 cup stemmed and halved porcini mushrooms", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 26, "PREP"),  # "stemmed and halved" (Kept as original PREP span)
            (27, 34, "NAME"),  # "porcini" (from original NAME "porcini mushrooms" 27-44)
            (35, 44, "NAME")  # "mushrooms" (from original NAME "porcini mushrooms" 27-44)
        ]
    }),

    # Example 67
    ("1 tablespoon Essence, recipe follows", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 20, "NAME"),  # "Essence"
            # Comma at 20 is "O"
            (22, 36, "COMMENT")  # "recipe follows" (Kept as original COMMENT span)
        ]
    }),

    # Example 68
    ("1 cup diced roasted, seeded and peeled Anaheim chilies", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 38, "PREP"),  # "diced roasted, seeded and peeled" (Kept as original PREP span)
            (39, 46, "NAME"),  # "Anaheim" (from original NAME "Anaheim chilies" 39-54)
            (47, 54, "NAME")  # "chilies" (from original NAME "Anaheim chilies" 39-54)
        ]
    }),

    # Example 69
    ("1/4 cup plus 2 tablespoons jarred grated horseradish (with liquid)", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 26, "COMMENT"),  # "plus 2 tablespoons" (Kept as original COMMENT span)
            (27, 33, "PREP"),  # "jarred" (from original PREP "jarred grated" 27-40)
            (34, 40, "PREP"),  # "grated" (from original PREP "jarred grated" 27-40)
            (41, 52, "NAME"),  # "horseradish"
            (53, 66, "COMMENT")  # "(with liquid)" (Kept as original COMMENT span)
        ]
    }),  # Duplicate from previous list has (27,40,"PREP") for "jarred grated". I'll use this new split.

    # Example 70
    ("One 3-pound corned beef brisket (uncooked), in brine", {
        "entities": [
            (0, 3, "QTY"),  # "One" (Kept as original QTY span)
            (4, 11, "COMMENT"),  # "3-pound" (Kept as original COMMENT span)
            (12, 18, "NAME"),  # "corned" (from original NAME "corned beef brisket" 12-31)
            (19, 23, "NAME"),  # "beef" (from original NAME "corned beef brisket" 12-31)
            (24, 31, "NAME"),  # "brisket" (from original NAME "corned beef brisket" 12-31)
            (32, 43, "COMMENT"),  # "(uncooked)," (Kept as original COMMENT span, includes comma)
            (44, 52, "PREP")  # "in brine" (Kept as original PREP span)
        ]
    }),

    # Example 72
    ("1/2 medium yellow medium onion, grated", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 10, "UNIT"),  # "medium"
            (11, 17, "NAME"),  # "yellow"
            (18, 24, "COMMENT"),  # "medium" (Original label was COMMENT for the second "medium")
            (25, 30, "NAME"),  # "onion"
            # Comma at 30 is "O"
            (32, 38, "PREP")  # "grated" (Kept as original PREP span)
        ]
    }),

    # Example 73
    ("1 can (26 ounces) Campbell's® Condensed Cream of Mushroom Soup (Regular or 98% Fat Free)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "can"
            (6, 17, "COMMENT"),  # "(26 ounces)" (Kept as original COMMENT span)
            (18, 28, "NAME"),  # "Campbell's®" (from original NAME 18-57)
            (30, 39, "NAME"),  # "Condensed" (from original NAME 18-57)
            (40, 45, "NAME"),  # "Cream" (from original NAME 18-57)
            (46, 48, "NAME"),  # "of" (from original NAME 18-57) - *Unusual*
            (49, 57, "NAME"),  # "Mushroom" (from original NAME 18-57)
            (58, 88, "COMMENT")
            # "Soup (Regular or 98% Fat Free)" (Kept as original COMMENT span, "Soup" is part of it)
        ]
    }),

    # Example 74
    ("2 bags (16 ounces each) frozen vegetable combination (broccoli, cauliflower, carrots), cooked and drained", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 6, "UNIT"),  # "bags"
            (7, 23, "COMMENT"),  # "(16 ounces each)" (Kept as original COMMENT span)
            (24, 30, "NAME"),  # "frozen" (Kept as original PREP span)
            (31, 40, "NAME"),  # "vegetable" (from original NAME "vegetable combination" 31-52)
            (41, 52, "NAME"),  # "combination" (from original NAME "vegetable combination" 31-52)
            (53, 85, "COMMENT"),  # "(broccoli, cauliflower, carrots)" (Kept as original COMMENT span)
            # Comma at 85 is "O"
            (87, 105, "PREP")  # "cooked and drained" (Kept as original PREP span)
        ]
    }),

    # Example 75
    ("2 to 3 packages pre-prepared won ton wrappers", {
        "entities": [
            (0, 1, "QTY"),  # "2 to 3" (Kept as original QTY span)
            (2, 6, "COMMENT"),  # "2 to 3" (Kept as original QTY span)
            (7, 15, "UNIT"),  # "packages"
            (16, 28, "PREP"),  # "pre-prepared" (Kept as original PREP span)
            (29, 32, "NAME"),  # "won" (from original NAME "won ton wrappers" 29-45)
            (33, 36, "NAME"),  # "ton" (from original NAME "won ton wrappers" 29-45)
            (37, 45, "NAME")  # "wrappers" (from original NAME "won ton wrappers" 29-45)
        ]
    }),

    # Example 76
    ("Few drops of truffle oil", {
        "entities": [
            (0, 3, "QTY"),  # "Few" (Kept as original QTY span)
            (4, 9, "UNIT"),  # "drops"
            (10, 12, "PREP"),  # "of" (Kept as original PREP span)
            (13, 20, "NAME"),  # "truffle" (from original NAME "truffle oil" 13-24)
            (21, 24, "NAME")  # "oil" (from original NAME "truffle oil" 13-24)
        ]
    }),

    # Example 77 (Duplicate)
    ("6 cups mixed baby greens", {"entities": [
        (0, 1, "QTY"), (2, 6, "UNIT"), (7, 12, "PREP"),
        (13, 17, "NAME"), (18, 24, "NAME")]}),  # mixed, baby, greens

    # Example 78
    ("16 oz. ginger ale", {
        "entities": [
            (0, 2, "QTY"),  # "16" (Kept as original QTY span)
            (3, 6, "UNIT"),  # "oz." (includes period)
            (7, 13, "NAME"),  # "ginger" (from original NAME "ginger ale" 7-17)
            (14, 17, "NAME")  # "ale" (from original NAME "ginger ale" 7-17)
        ]
    }),

    ("1 tablespoons peeled and finely chopped ginger", {  # Assuming (32,38,"NAME") for "ginger" was intended
        "entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 39, "PREP"),  # "peeled and finely chopped"
            (40, 38, "NAME")  # "ginger"
        ]
    }),

    # Example 80
    ("16 ounces leftover Oil Poached Flounder, recipe follows, flaked", {
        "entities": [
            (0, 2, "QTY"),  # "16" (Kept as original QTY span)
            (3, 9, "UNIT"),  # "ounces"
            (10, 18, "PREP"),  # "leftover" (Kept as original PREP span)
            (19, 22, "NAME"),  # "Oil"
            (23, 30, "PREP"),  # "Poached" (Original label was PREP)
            (31, 39, "NAME"),  # "Flounder" (Your previous entity here was missing)
            # Comma at 39 is "O"
            (41, 55, "COMMENT"),  # "recipe follows" (Kept as original COMMENT span)
            # Comma at 55 is "O"
            (57, 63, "PREP")  # "flaked" (Kept as original PREP span)
        ]
    }),

    # Example 81

    ("1/2 wet cured, smoked ham, about 5 to 7 1/2 pounds", {  # Corrected with "smoked" as PREP if that was intent
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "PREP"),  # "wet"
            (8, 14, "PREP"),  # "cured," (includes comma if it's part of the token)
            (15, 21, "NAME"),  # "smoked" (if "smoked" is PREP)
            (22, 25, "NAME"),  # "ham"
            (27, 50, "COMMENT")
        ]
    }),

    # Example 82
    ("Prepared horseradish", {"entities": [
        (0, 8, "PREP"),  # "Prepared" (Kept as original PREP span)
        (9, 20, "NAME")  # "horseradish"
    ]}),

    # Example 83
    ("Prepared mustard", {"entities": [
        (0, 8, "PREP"),  # "Prepared" (Kept as original PREP span)
        (9, 16, "NAME")  # "mustard"
    ]}),

    # Example 84
    ("1 cup coarsely ground or chopped pistachios, for serving", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 5, "UNIT"),  # "cup"
            (6, 14, "PREP"),  # "coarsely" (Kept as original PREP span)
            (15, 21, "NAME"),  # "ground" (Original label was NAME for "ground")
            (22, 32, "ALT_NAME"),  # "or chopped" (Kept as original ALT_NAME span)
            (33, 43, "NAME"),  # "pistachios"
            # Comma at 43 is "O"
            (45, 56, "COMMENT")  # "for serving" (Kept as original COMMENT span)
        ]
    }),

    # Example 85
    ("1 1/2 cups polenta", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept as original QTY span)
            (6, 10, "UNIT"),  # "cups"
            (11, 18, "NAME")  # "polenta"
        ]
    }),

    # Example 86
    ("1 box cous cous (approximately 16 ounces)", {
        "entities": [
            (0, 5, "COMMENT"),  # "1 box" (Original label was COMMENT)
            (6, 10, "NAME"),  # "cous" (from original NAME "cous cous" 6-15)
            (11, 15, "NAME"),  # "cous" (from original NAME "cous cous" 6-15)
            (16, 41, "COMMENT")  # "(approximately 16 ounces)" (Kept as original COMMENT span)
        ]
    }),

    # Example 87
    ("Ramekin for molding", {
        "entities": [
            (0, 7, "NAME"),  # "Ramekin"
            (8, 19, "COMMENT")  # "for molding" (Kept as original COMMENT span)
        ]
    }),

    # Example 88
    ("1 1/4 pounds haricots verts or green beans, trimmed", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/4" (Kept as original QTY span)
            (6, 12, "UNIT"),  # "pounds"
            (13, 21, "NAME"),  # "haricots" (from original NAME "haricots verts" 13-27)
            (22, 27, "NAME"),  # "verts" (from original NAME "haricots verts" 13-27)
            (28, 43, "ALT_NAME"),
            # "or green beans" (Kept as original ALT_NAME span, your original included comma here)
            # Comma was part of ALT_NAME in your example, so it stays. If not, then (28,42,"ALT_NAME") and comma is O.
            (44, 51, "PREP")  # "trimmed" (Kept as original PREP span)
        ]
    }),

    ("8 cups seeded and diced heirloom tomatoes", {  # Assuming "seeded and diced" is PREP
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),
            (7, 23, "PREP"),  # "seeded and diced" (If this was one PREP originally)
            (24, 32, "NAME"),  # "heirloom"
            (33, 41, "NAME")  # "tomatoes"
        ]
    }),

    # Example 90
    ("1 salmon filet (about 3 pounds), pin bones removed and halved horizontally", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 8, "NAME"),  # "salmon"
            (9, 14, "NAME"),  # "filet"
            (15, 31, "COMMENT"),  # "(about 3 pounds)" (Kept as original COMMENT span)
            # Comma at 31 is "O"
            (33, 74, "PREP")  # "pin bones removed and halved horizontally" (Kept as original PREP span)
        ]
    }),

    # Example 91
    ("1 1/2 teaspoons liquid smoke", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept as original QTY span)
            (6, 15, "UNIT"),  # "teaspoons"
            (16, 22, "NAME"),  # "liquid" (from original NAME "liquid smoke" 16-28)
            (23, 28, "NAME")  # "smoke" (from original NAME "liquid smoke" 16-28)
        ]
    }),

    # Example 92
    ("1 tablespoon (9.3 grams) instant yeast", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 24, "COMMENT"),  # "(9.3 grams)" (Kept as original COMMENT span)
            (25, 32, "PREP"),  # "instant" (Kept as original PREP span)
            (33, 38, "NAME")  # "yeast"
        ]
    }),

    # Example 93
    ("3 pounds skin-on, bone-in chicken parts (breasts halved crosswise)", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 8, "UNIT"),  # "pounds"
            (9, 17, "NAME"),  # "skin-on," (from original NAME "skin-on, bone-in" 9-25, includes comma)
            (18, 25, "NAME"),  # "bone-in" (from original NAME "skin-on, bone-in" 9-25)
            (26, 33, "NAME"),  # "chicken" (from original NAME "chicken parts" 26-39)
            (34, 39, "NAME"),  # "parts" (from original NAME "chicken parts" 26-39)
            (40, 66, "COMMENT")  # "(breasts halved crosswise)" (Kept as original COMMENT span)
        ]
    }),

    # Example 94
    ("1 1/2 cups polenta (not quick-cooking)", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept as original QTY span)
            (6, 10, "UNIT"),  # "cups"
            (11, 18, "NAME"),  # "polenta"
            (19, 38, "COMMENT")  # "(not quick-cooking)" (Kept as original COMMENT span)
        ]
    }),

    # Example 95
    ("3 oranges, juiced", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 9, "NAME"),  # "oranges"
            # Comma at 9 is "O"
            (11, 17, "PREP")  # "juiced" (Kept as original PREP span)
        ]
    }),

    # Example 96
    ("3 tablespoons freshly grated Parmesan, plus 1/4 cup freshly grated", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, "PREP"),  # "freshly" (from original PREP "freshly grated" 14-28)
            (22, 28, "PREP"),  # "grated" (from original PREP "freshly grated" 14-28)
            (29, 37, "NAME"),  # "Parmesan"
            # Comma at 37 is "O"
            (39, 66, "COMMENT")  # "plus 1/4 cup freshly grated" (Kept as original COMMENT span)
        ]
    }),

    # Example 97
    ("Minced fresh flat-leaf parsley leaves", {
        "entities": [
            (0, 6, "PREP"),  # "Minced" (Kept as original PREP span)
            (7, 12, "PREP"),  # "fresh" (Kept as original PREP span)
            (13, 22, "NAME"),  # "flat-leaf" (from original NAME "flat-leaf parsley leaves" 13-37)
            (23, 30, "NAME"),  # "parsley" (from original NAME "flat-leaf parsley leaves" 13-37)
            (31, 37, "NAME")  # "leaves" (from original NAME "flat-leaf parsley leaves" 13-37)
        ]
    }),

    # Example 98
    ("2 marshmallows, for garnish", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 14, "NAME"),  # "marshmallows"
            # Comma at 14 is "O"
            (16, 27, "COMMENT")  # "for garnish" (Kept as original COMMENT span)
        ]
    }),

    # Example 99
    ("1/3 cup soybean or safflower oil", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "NAME"),  # "soybean"
            (16, 28, "ALT_NAME"),  # "or safflower oil" (Kept as original ALT_NAME span)
            (29, 32, "NAME")  # "oil" (Kept as original ALT_NAME span)
        ]
    }),

    # Example 100
    ("3 large russet potatoes scrubbed", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "large"
            (8, 14, "NAME"),  # "russet" (from original NAME "russet potatoes" 8-23)
            (15, 23, "NAME"),  # "potatoes" (from original NAME "russet potatoes" 8-23)
            (24, 32, "PREP")  # "scrubbed" (Kept as original PREP span)
        ]
    }),

    # Example 101
    ("2 tablespoons, 5 or 6 sprigs, fresh thyme, leaves stripped and chopped", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept as original QTY span)
            (2, 13, "UNIT"),  # "tablespoons"
            # Comma at 13 is "O"
            (15, 28, "COMMENT"),  # "5 or 6 sprigs" (Kept as original COMMENT span)
            # Comma at 28 is "O"
            (30, 35, "PREP"),  # "fresh" (Kept as original PREP span)
            (36, 41, "NAME"),  # "thyme"
            # Comma at 41 is "O"
            (43, 70, "PREP")  # "leaves stripped and chopped" (Kept as original PREP span)
        ]
    }),

    # Example 102
    ("1 teaspoon ground toasted cardamom", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 17, "NAME"),  # "ground" (from original NAME "ground toasted cardamom" 11-34)
            (18, 25, "NAME"),  # "toasted" (from original NAME "ground toasted cardamom" 11-34)
            (26, 34, "NAME")  # "cardamom" (from original NAME "ground toasted cardamom" 11-34)
        ]
    }),

    # Example 103
    ("1/2 cup finely chopped fresh flat-leaf parsley, or a combination of parsley and fresh mint", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "finely" (from original PREP "finely chopped fresh" 8-28)
            (15, 22, "PREP"),  # "chopped" (from original PREP "finely chopped fresh" 8-28)
            (23, 28, "PREP"),  # "fresh" (from original PREP "finely chopped fresh" 8-28)
            (29, 38, "NAME"),  # "flat-leaf" (from original NAME "flat-leaf parsley" 29-46)
            (39, 46, "NAME"),  # "parsley" (from original NAME "flat-leaf parsley" 29-46)
            # Comma at 46 is "O"
            (48, 90, "ALT_NAME")  # "or a combination of parsley and fresh mint" (Kept as original ALT_NAME span)
        ]
    }),

    # Example 104
    ("1/2 cup panko or homemade breadcrumbs", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "NAME"),  # "panko"
            (14, 25, "ALT_NAME"),  # "or homemade breadcrumbs" (Kept as original ALT_NAME span)
            (26, 37, "NAME")  # " breadcrumbs" (Kept as original ALT_NAME span)
        ]
    }),

    # Example 105
    ("1 pound thinly sliced serrano ham (about 24 slices)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept as original QTY span)
            (2, 7, "UNIT"),  # "pound"
            (8, 14, "PREP"),  # "thinly" (from original PREP "thinly sliced" 8-21)
            (15, 21, "PREP"),  # "sliced" (from original PREP "thinly sliced" 8-21)
            (22, 29, "NAME"),  # "serrano" (from original NAME "serrano ham" 22-33)
            (30, 33, "NAME"),  # "ham" (from original NAME "serrano ham" 22-33)
            (34, 51, "COMMENT")  # "(about 24 slices)" (Kept as original COMMENT span)
        ]
    }),

    # Example 106
    ("3 bunches (about 1 pound) baby turnips (ping pong ball size), greens and soft stems reserved",
     {  # Strict interpretation of your original (39,92,"COMMENT")
         "entities": [
             (0, 1, "QTY"),
             (2, 9, "UNIT"),
             (10, 25, "COMMENT"),
             (26, 30, "NAME"),  # "baby"
             (31, 38, "NAME"),  # "turnips"
             (39, 92, "COMMENT")  # "(ping pong ball size), greens and soft stems reserved"
         ]
     }),

    # Example 107
    ("3/4 cup toasted pecans finely chopped", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "PREP"),  # "toasted" (Kept as original PREP span)
            (16, 22, "NAME"),  # "pecans"
            (23, 37, "PREP"),  # "finely" (Original PREP (23,29))
        ]
    }),

    # Example 108
    ("3 tablespoons ginger wine (recommended: Stone's Ginger Wine)", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept as original QTY span)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 20, "NAME"),  # "ginger" (from original NAME "ginger wine" 14-25)
            (21, 25, "NAME"),  # "wine" (from original NAME "ginger wine" 14-25)
            (26, 60, "COMMENT")  # "(recommended: Stone's Ginger Wine)" (Kept as original COMMENT span)
        ]
    }),

    # Example 109
    ("1/4 cup finely chopped glace baby ginger", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept as original QTY span)
            (4, 7, "UNIT"),  # "cup"
            (8, 22, "PREP"),  # "finely" (from original PREP "finely chopped" 8-22)
            (23, 28, "NAME"),  # "glace" (from original NAME "glace baby ginger" 23-40)
            (29, 33, "NAME"),  # "baby" (from original NAME "glace baby ginger" 23-40)
            (34, 40, "NAME")  # "ginger" (from original NAME "glace baby ginger" 23-40)
        ]
    }),

    # Example 110
    ("3/4 pound total (1/4 pound each) thinly sliced Italian meats: sliced sopressata, capicola and Genoa salami", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept as original QTY span)
            (4, 9, "UNIT"),  # "pound"
            (10, 32, "COMMENT"),  # "total" (Kept as original COMMENT span)
            (33, 46, "PREP"),  # "thinly" (Kept as original PREP span)
            (47, 60, "NAME"),  # "Italian"
            (60, 106, "COMMENT")
            # ": sliced sopressata, capicola and Genoa salami" (Kept as original COMMENT span, includes colon)
        ]
    }),

    # Example 111
    ("1 jar, 16 ounces, roasted red peppers, drained and sliced", {
        "entities": [
            (0, 5, "COMMENT"),  # "1 jar" (Kept as original COMMENT span)
            # Comma at 5 is "O"
            (7, 9, "QTY"),  # "16" (Kept as original QTY span)
            (10, 16, "UNIT"),  # "ounces"
            # Comma at 16 is "O"
            (18, 25, "PREP"),  # "roasted" (Kept as original PREP span)
            (26, 29, "NAME"),  # "red" (from original NAME "red peppers" 26-37)
            (30, 37, "NAME"),  # "peppers" (from original NAME "red peppers" 26-37)
            # Comma at 37 is "O"
            (39, 57, "PREP")  # "drained and sliced" (Kept as original PREP span)
        ]
    }),
    # Re-annotated data based on the FINAL REFINED rules:
    # - NAME entities are broken into word-level NAME entities.
    # - COMMENT, PREP, ALT_NAME, QTY entities are kept as single, original spans.
    # - UNIT entities are single words.
    # - Commas and other non-entity words become "O" (and are thus not listed in the 'entities' list).
    # Tokenization based on spaCy's default English tokenizer.

    # ... (all previous examples from your earlier chunks would be here) ...

    # Example 1
    ("2/3 pound total Italian table cheeses, 1/3 pound each of 2 varieties: sharp provolone, Pepato, Fontina, Parmigian-Reggiano",
     {
         "entities": [
             (0, 3, "QTY"),  # "2/3" (Kept)
             (4, 9, "UNIT"),  # "pound"
             (10, 15, "COMMENT"),  # "total" (Kept)
             (16, 23, "NAME"),  # "Italian" (from original NAME 16-23)
             (24, 29, "NAME"),  # "table" (from original NAME 24-29)
             (30, 37, "NAME"),  # "cheeses" (from original NAME 30-37)
             # Comma at 37 is "O"
             (39, 68, "COMMENT"),  # "1/3 pound each of 2 varieties" (Kept)
             (68, 122, "COMMENT")  # ": sharp provolone, Pepato, Fontina, Parmigian-Reggiano" (Kept, includes colon)
         ]
     }),

    # Example 2
    ("1 Granny Smith apple", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "NAME"),  # "Granny" (from original NAME 2-8)
            (9, 14, "NAME"),  # "Smith" (from original NAME 9-14)
            (15, 20, "NAME")  # "apple" (from original NAME 15-20)
        ]
    }),

    # Example 3
    ("1 1/4 ounce packet unflavored powdered gelatin", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/4" (Kept)
            (6, 11, "UNIT"),  # "ounce"
            (12, 18, "COMMENT"),  # "packet" (Original label was COMMENT)
            (19, 29, "PREP"),  # "unflavored" (from original PREP 19-38 "unflavored powdered")
            (30, 38, "PREP"),  # "powdered" (from original PREP 19-38 "unflavored powdered")
            (39, 46, "NAME")  # "gelatin"
        ]
    }),

    # Example 4
    ("2 oranges", {"entities": [
        (0, 1, "QTY"),  # "2" (Kept)
        (2, 9, "NAME")  # "oranges"
    ]}),

    # Example 5
    ("1 tablespoon finely chopped fines herbes (chervil, parsley, tarragon, and chives)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 19, "PREP"),  # "finely" (Kept)
            (20, 27, "PREP"),  # "chopped" (Kept)
            (28, 33, "NAME"),  # "fines" (from original NAME 28-33)
            (34, 40, "NAME"),  # "herbes" (from original NAME 34-40)
            (41, 80, "COMMENT")  # "(chervil, parsley, tarragon, and chives)" (Kept)
        ]
    }),

    # Example 6 (Duplicate) - Assuming it refers to "1 1/2 pounds peeled and deveined large shrimp"
    ("1 1/2 pounds peeled and deveined large shrimp", {"entities": [
        (0, 5, "QTY"), (6, 12, "UNIT"),
        (13, 32, "PREP"),  # "peeled"
        (33, 38, "UNIT"),  # "large"
        (39, 45, "NAME")  # "shrimp"
    ]}),

    # Example 7
    ("1 1/2 pounds medium peeled and deveined shrimp, tails removed", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 19, "UNIT"),  # "medium"
            (20, 39, "PREP"),  # "peeled" (Kept)
            (40, 46, "NAME"),  # "shrimp"
            # Comma at 46 is "O"
            (48, 61, "PREP")  # "tails removed" (Kept)
        ]
    }),

    # Example 8
    ("6 cups zucchini noodles, from 2 medium zucchinis (about 1 pound)", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 15, "NAME"),  # "zucchini" (from original NAME 7-15)
            (16, 23, "NAME"),  # "noodles" (from original NAME 16-23)
            # Comma at 23 is "O"
            (25, 64, "COMMENT")  # "from 2 medium zucchinis (about 1 pound)" (Kept)
        ]
    }),

    # Example 9
    ("2 (12-ounce) boneless rib eye steaks", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 12, "COMMENT"),  # "(12-ounce)" (Kept)
            (13, 21, "NAME"),  # "boneless" (Kept)
            (22, 25, "NAME"),  # "rib" (from original NAME 22-25)
            (26, 29, "NAME"),  # "eye" (from original NAME 26-29)
            (30, 36, "NAME")  # "steaks" (Original label was UNIT)
        ]
    }),

    # Example 10
    ("2 cups small-diced, peeled russet potatoes (1 large russet)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 18, "PREP"),  # "small-diced," (Kept, includes comma)
            (20, 26, "PREP"),  # "peeled" (Kept)
            (27, 33, "NAME"),  # "russet" (from original NAME 27-33)
            (34, 42, "NAME"),  # "potatoes" (from original NAME 34-42)
            (43, 59, "COMMENT")  # "(1 large russet)" (Kept)
        ]
    }),

    # Example 11
    ("4 cups small-diced zucchini (green/yellow) (5 small zucchini)", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 18, "PREP"),  # "small-diced" (Kept)
            (19, 27, "NAME"),  # "zucchini"
            (28, 42, "COMMENT"),  # "(green/yellow)" (Kept)
            (43, 60, "COMMENT")  # "(5 small zucchini)" (Kept)
        ]
    }),

    # Example 12
    ("1 tablespoon finely chopped rosemary or thyme leaves", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 19, "PREP"),  # "finely" (Kept)
            (20, 27, "PREP"),  # "chopped" (Kept)
            (28, 36, "NAME"),  # "rosemary"
            (37, 52, "ALT_NAME")  # "or thyme leaves" (Kept)
        ]
    }),

    # Example 13
    ("12 ounces macaroni (or your choice of pasta)", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 9, "UNIT"),  # "ounces"
            (10, 18, "NAME"),  # "macaroni"
            (19, 44, "COMMENT")  # "(or your choice of pasta)" (Kept)
        ]
    }),

    # Example 14
    ("2 tablespoons ghee", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 18, "NAME")  # "ghee"
        ]
    }),

    # Example 15
    ("1 (8-ounce) package frozen artichoke hearts, thawed", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 11, "COMMENT"),  # "(8-ounce)" (Kept)
            (12, 19, "UNIT"),  # "package"
            (20, 26, "NAME"),  # "frozen" (Kept)
            (27, 36, "NAME"),  # "artichoke" (from original NAME 27-36)
            (37, 43, "NAME"),  # "hearts" (from original NAME 37-43)
            # Comma at 43 is "O"
            (45, 51, "PREP")  # "thawed" (Kept)
        ]
    }),

    # Example 16
    ("1/3 cup olive oil, plus extra for drizzling", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "NAME"),  # "olive" (from original NAME 8-13)
            (14, 17, "NAME"),  # "oil" (from original NAME 14-17)
            # Comma at 17 is "O"
            (19, 43, "COMMENT")  # "plus extra for drizzling" (Kept)
        ]
    }),

    # Example 17
    ("5 cups (5 ounces) baby arugula", {
        "entities": [
            (0, 1, "QTY"),  # "5" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 17, "COMMENT"),  # "(5 ounces)" (Kept)
            (18, 22, "NAME"),  # "baby" (from original NAME 18-22)
            (23, 30, "NAME")  # "arugula" (from original NAME 23-30)
        ]
    }),

    # Example 18
    ("1 pound cherry or grape tomatoes, halved through the stem", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 14, "NAME"),  # "cherry"
            (15, 23, "ALT_NAME"),  # "or grape tomatoes" (Kept)
            (24, 32, "NAME"),  # "tomatoes" (Kept)
            # Comma at 32 is "O"
            (34, 57, "PREP")  # "halved through the stem" (Kept)
        ]
    }),

    # Example 19
    ("4 fillets walleye or other white flaky fish such as black bass or tilapia (about 1 pound 1 ounce)", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 9, "NAME"),  # "fillets"
            (10, 17, "NAME"),  # "walleye"
            (18, 73, "ALT_NAME"),  # "or other white flaky fish such as black bass or tilapia" (Kept)
            (74, 97, "COMMENT")  # "(about 1 pound 1 ounce)" (Kept)
        ]
    }),

    # Example 20
    ("2 lemons juiced and zested", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "NAME"),  # "lemons"
            (9, 26, "PREP"),  # "juiced" (Kept)
        ]
    }),

    # Example 21
    ("1 cup (250 milliliters) dry white wine", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 23, "COMMENT"),  # "(250 milliliters)" (Kept)
            (24, 27, "PREP"),  # "dry" (Kept)
            (28, 33, "NAME"),  # "white" (from original NAME 28-33)
            (34, 38, "NAME")  # "wine" (from original NAME 34-38)
        ]
    }),

    # Example 22
    ("2 cups broccoli florets", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 15, "NAME"),  # "broccoli" (from original NAME 7-15)
            (16, 23, "NAME")  # "florets" (from original NAME 16-23)
        ]
    }),

    # Example 23
    ("1 tablespoon herbs de Provence", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 18, "NAME"),  # "herbs" (from original NAME 13-18)
            (19, 21, "NAME"),  # "de" (from original NAME 19-21) - *Unusual to label 'de' as NAME*
            (22, 30, "NAME")  # "Provence" (from original NAME 22-30)
        ]
    }),

    # Example 24
    ("3 slices bacon, thinly sliced crosswise", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 8, "PREP"),  # "slices" (Original label was PREP)
            (9, 14, "NAME"),  # "bacon"
            # Comma at 14 is "O"
            (16, 22, "PREP"),  # "thinly" (Kept)
            (23, 29, "PREP"),  # "sliced" (Kept)
            (30, 39, "PREP")  # "crosswise" (Kept)
        ]
    }),

    # Example 25
    ("2 (14-ounce) pork tenderloins, each halved crosswise", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 12, "COMMENT"),  # "(14-ounce)" (Kept)
            (13, 17, "NAME"),  # "pork" (from original NAME 13-17)
            (18, 29, "NAME"),  # "tenderloins" (from original NAME 18-29)
            # Comma at 29 is "O"
            (31, 52, "PREP")  # "each halved crosswise" (Kept)
        ]
    }),

    # Example 26
    ("Store-bought dinner rolls or biscuits, for serving", {
        "entities": [
            (0, 12, "PREP"),  # "Store-bought" (Kept)
            (13, 19, "NAME"),  # "dinner" (from original NAME 13-19)
            (20, 25, "NAME"),  # "rolls" (from original NAME 20-25)
            (26, 38, "ALT_NAME"),  # "or biscuits," (Kept, includes comma)
            (39, 50, "COMMENT")  # "for serving" (Kept)
        ]
    }),

    # Example 27
    ("1/4 cup chopped roasted cashews for garnish", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "PREP"),  # "chopped" (Kept)
            (16, 23, "NAME"),  # "roasted" (Kept)
            (24, 31, "NAME"),  # "cashews"
            (32, 43, "COMMENT")  # "for garnish" (Kept)
        ]
    }),

    # Example 28
    ("1 jar (15 ounces) Patak's® Korma Curry Cooking Sauce", {
        "entities": [
            (0, 5, "COMMENT"),  # "1 jar" (Kept, your previous QTY+UNIT)
            (7, 9, "QTY"),  # "15" (Kept) - This was your new entity. Your prev. COMMENT covered this.
            (10, 16, "UNIT"),  # "ounces"
            # Comma here "O"
            (18, 25, "NAME"),  # "Patak's®" (from original NAME 18-52)
            (27, 32, "NAME"),  # "Korma" (from original NAME 18-52)
            (33, 38, "NAME"),  # "Curry" (from original NAME 18-52)
            (39, 46, "NAME"),  # "Cooking" (from original NAME 18-52)
            (47, 52, "NAME")  # "Sauce" (from original NAME 18-52)
        ]
    }),

    # Example 29
    ("1 1/2 pounds coarsely ground turkey (dark meat)", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 21, "PREP"),  # "coarsely" (Kept)
            (22, 28, "PREP"),  # "ground" (Kept)
            (29, 35, "NAME"),  # "turkey"
            (36, 47, "COMMENT")  # "(dark meat)" (Kept)
        ]
    }),

    # Example 30
    ("3 large, ripe tomatoes, seeded and cut into 1/2-inch cubes", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 7, "UNIT"),  # "large"
            # Comma at 7 is "O"
            (9, 13, "PREP"),  # "ripe" (Kept)
            (14, 22, "NAME"),  # "tomatoes"
            # Comma at 22 is "O"
            (24, 58, "PREP"),  # "seeded" (Kept)
        ]
    }),

    # Example 31
    ("3/4 pound tomatillos, husked, washed, cored and diced", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 20, "NAME"),  # "tomatillos"
            # Comma at 20 is "O"
            (22, 28, "PREP"),  # "husked" (Kept)
            # Comma at 28 is "O"
            (30, 36, "PREP"),  # "washed" (Kept)
            # Comma at 36 is "O"
            (38, 53, "PREP"),  # "cored" (Kept)
        ]
    }),

    # Example 32
    ("1 cup (77 g) pineapple chunks", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "COMMENT"),  # "(77 g)" (Kept)
            (13, 22, "NAME"),  # "pineapple"
            (23, 29, "NAME")  # "chunks" (Original label was PREP)
        ]
    }),

    # Example 33
    ("12 cups cubed crustless, stale sourdough or peasant bread", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 7, "UNIT"),  # "cups"
            (8, 13, "PREP"),  # "cubed" (Kept)
            (14, 23, "PREP"),  # "crustless" (Kept, original had comma after it as PREP, assuming comma is O)
            # Comma at 23 is "O"
            (25, 30, "PREP"),  # "stale" (Kept)
            (31, 40, "NAME"),  # "sourdough"
            (41, 57, "ALT_NAME")  # "or peasant bread" (Kept)
        ]
    }),

    # Example 34
    ("1 tablespoon coriander seeds, toasted and crushed", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 22, "NAME"),  # "coriander" (from original NAME 13-22)
            (23, 28, "NAME"),  # "seeds" (from original NAME 23-28)
            # Comma at 28 is "O"
            (30, 49, "PREP"),  # "toasted" (Kept)
        ]
    }),

    # Example 35
    ("One 13-rib pork loin, membrane between the rib bones slit to allow the pork to curl around and stand up", {
        "entities": [
            (0, 3, "QTY"),  # "One" (Kept)
            (4, 10, "COMMENT"),  # "13-rib" (Kept)
            (11, 15, "NAME"),  # "pork" (from original NAME 11-15)
            (16, 20, "NAME"),  # "loin" (from original NAME 16-20)
            # Comma at 20 is "O"
            (22, 103, "COMMENT")
            # "membrane between the rib bones slit to allow the pork to curl around and stand up" (Kept)
        ]
    }),

    # Example 36
    ("1 cup, plus 1 teaspoon, granulated sugar", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            # Comma at 5 is "O"
            (7, 23, "COMMENT"),  # "plus 1 teaspoon," (Kept, includes comma)
            (24, 40, "NAME"),  # "granulated" (Kept)
        ]
    }),

    # Example 37
    ("1/2 cup plus 1 teaspoon vegetable shortening", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 23, "COMMENT"),  # "plus 1 teaspoon" (Kept)
            (24, 33, "NAME"),  # "vegetable" (from original NAME 24-33)
            (34, 44, "NAME")  # "shortening" (from original NAME 34-44)
        ]
    }),

    # Example 38
    ("1 tablespoon brandy", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 19, "NAME")  # "brandy"
        ]
    }),

    # Example 39
    ("1 large head escarole, washed and hand torn", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "large"
            (8, 12, "UNIT"),  # "head"
            (13, 21, "NAME"),  # "escarole"
            # Comma at 21 is "O"
            (23, 43, "PREP"),  # "washed" (Kept)
        ]
    }),

    # Example 40
    ("6 salami slices", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 8, "NAME"),  # "salami"
            (9, 15, "PREP")  # "slices" (Original label was PREP)
        ]
    }),

    # Example 41
    ("6 pieces soppressata, cut into batons", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 8, "UNIT"),  # "pieces"
            (9, 20, "NAME"),  # "soppressata"
            # Comma at 20 is "O"
            (22, 37, "PREP")  # "cut into batons" (Kept)
        ]
    }),

    # Example 42
    ("6 trout fillets", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 15, "NAME"),  # "trout"
        ]
    }),

    # Example 43
    ("1 medium white or yellow onion", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "UNIT"),  # "medium"
            (9, 14, "NAME"),  # "white"
            (15, 24, "ALT_NAME"),  # "or yellow" (Kept)
            (25, 30, "NAME")  # "onion"
        ]
    }),

    # Example 44
    ("1 1/2 cups plus 3 tablespoons buttermilk", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 29, "COMMENT"),  # "plus 3 tablespoons" (Kept)
            (30, 40, "NAME")  # "buttermilk"
        ]
    }),

    # Example 45
    ("2 skinless walleye fillets (about 4 ounces/113 grams each), halved crosswise", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 10, "PREP"),  # "skinless" (Kept)
            (11, 26, "NAME"),  # "walleye"
            (27, 58, "COMMENT"),  # "(about 4 ounces/113 grams each)" (Kept)
            # Comma at 58 is "O"
            (60, 76, "PREP")  # "halved crosswise" (Kept)
        ]
    }),

    # Example 46
    ("1 tablespoon triple sec", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 19, "NAME"),  # "triple" (from original NAME 13-19)
            (20, 23, "NAME")  # "sec" (from original NAME 20-23)
        ]
    }),

    # Example 47
    ("2 to 3 teaspoons seeded, ribbed and minced jalapeno pepper", {
        "entities": [
            (0, 1, "QTY"),  # "2 to 3" (Kept)
            (2, 6, "COMMENT"),  # "2 to 3" (Kept)
            (7, 16, "UNIT"),  # "teaspoons"
            (17, 23, "PREP"),  # "seeded" (Kept)
            # Comma at 23 is "O"
            (25, 42, "PREP"),  # "ribbed" (Original PREP (25,31))
            (43, 51, "NAME"),  # "jalapeno" (from original NAME 43-51)
            (52, 58, "NAME")  # "pepper" (from original NAME 52-58)
        ]
    }),

    # Example 48
    ("1/2 cup roasted and chopped Hatch green chile, homemade from fresh or store-bought, such as 505 Southwestern Green Chile, plus more for garnish",
     {
         "entities": [
             (0, 3, "QTY"),  # "1/2" (Kept)
             (4, 7, "UNIT"),  # "cup"
             (8, 27, "PREP"),  # "roasted" (Kept from (8,15,"PREP"))
             (28, 33, "NAME"),  # "Hatch" (from original NAME 28-33)
             (34, 39, "NAME"),  # "green" (from original NAME 34-39)
             (40, 45, "NAME"),  # "chile" (from original NAME 40-45)
             # Comma at 45 is "O"
             (47, 91, "COMMENT"),  # "homemade from fresh or store-bought, such as" (Kept)
             (92, 120, "ALT_NAME"),  # "505 Southwestern Green Chile" (Kept as one NAME as per original)
             # Comma at 120 is "O"
             (122, 143, "COMMENT")  # "plus more for garnish" (Kept)
         ]
     }),

    # Example 49
    ("1 1/2 cups yellow cornmeal", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 17, "NAME"),  # "yellow" (from original NAME 11-17)
            (18, 26, "NAME")  # "cornmeal" (from original NAME 18-26)
        ]
    }),

    # Example 50
    ("4 cups thawed and drained frozen cherries", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 25, "PREP"),  # "thawed" (from original PREP (7,13))
            (26, 32, "NAME"),  # "frozen" (from original PREP (26,32))
            (33, 41, "NAME")  # "cherries"
        ]
    }),

    # Example 51
    ("2 cups pineapple chunks", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 23, "NAME"),  # "pineapple"
        ]
    }),

    # Example 52
    ("1/4 pound Proscuitto di Parma, julienned", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 20, "NAME"),  # "Proscuitto" (from original NAME 10-20)
            (21, 23, "NAME"),  # "di" (from original NAME 21-23) - *Unusual NAME*
            (24, 29, "NAME"),  # "Parma" (from original NAME 24-29)
            # Comma at 29 is "O"
            (31, 40, "PREP")  # "julienned" (Kept)
        ]
    }),

    # Example 53
    ("8 large black mission figs or 12 green figs", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 7, "UNIT"),  # "large"
            (8, 13, "NAME"),  # "black" (from original NAME 8-13)
            (14, 21, "NAME"),  # "mission" (from original NAME 14-21)
            (22, 26, "NAME"),  # "figs" (from original NAME 22-26)
            (27, 43, "ALT_NAME")  # "or 12 green figs" (Kept)
        ]
    }),

    # Example 54
    ("2 cups peeled, seeded, and chopped vine-ripened tomatoes", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 34, "PREP"),  # "peeled" (Kept)
            # Comma at 21 is "O" (assuming original had "and" as O)
            (35, 47, "PREP"),  # "vine-ripened" (Kept)
            (48, 56, "NAME")  # "tomatoes"
        ]
    }),

    # Example 55
    ("2 cups roasted, peeled, and seeded red and yellow bell peppers", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 34, "PREP"),  # "roasted" (Kept)
            (35, 38, "NAME"),  # "red"
            (43, 49, "ALT_NAME"),  # "yellow"
            (50, 54, "NAME"),  # "bell"
            (55, 62, "NAME")  # "peppers"
        ]
    }),

    # Example 56
    ("1 papaya, chopped", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "NAME"),  # "papaya"
            # Comma at 8 is "O"
            (10, 17, "PREP")  # "chopped" (Kept)
        ]
    }),

    # Example 57
    ("1 red onion, sliced", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "NAME"),  # "red" (from original NAME "red onion" 2-11)
            (6, 11, "NAME"),  # "onion" (from original NAME "red onion" 2-11)
            # Comma at 11 is "O"
            (13, 19, "PREP")  # "sliced" (Kept)
        ]
    }),

    # Example 58
    ("1 1/4 cups wheat starch, plus more for dusting", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/4" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 16, "NAME"),  # "wheat" (from original NAME "wheat starch" 11-23)
            (17, 23, "NAME"),  # "starch" (from original NAME "wheat starch" 11-23)
            # Comma at 23 is "O"
            (25, 46, "COMMENT")  # "plus more for dusting" (Kept)
        ]
    }),

    # Example 59
    ("1 pound peeled and deveined small shrimp (51/60), tails removed", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 27, "PREP"),  # "peeled" (from original PREP "peeled and deveined" 8-27, "and" is O)
            (28, 33, "NAME"),  # "small"
            (34, 40, "NAME"),  # "shrimp"
            (41, 48, "COMMENT"),  # "(51/60)" (Kept)
            # Comma at 48 is "O"
            (50, 63, "PREP")  # "tails removed" (Kept)
        ]
    }),

    # Example 60
    ("3 1/2 cups rye flour", {
        "entities": [
            (0, 5, "QTY"),  # "3 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 14, "NAME"),  # "rye" (from original NAME "rye flour" 11-20)
            (15, 20, "NAME")  # "flour" (from original NAME "rye flour" 11-20)
        ]
    }),

    # Example 61
    ("1 pound dried cherries", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 22, "NAME"),  # "dried" (Kept)
        ]
    }),

    # Example 62
    ("3/4 cup, plus 2 tablespoons honey", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            # Comma at 7 is "O"
            (9, 27, "COMMENT"),  # "plus 2 tablespoons" (Kept)
            (28, 33, "NAME")  # "honey"
        ]
    }),

    # Example 63
    ("1/2 cup 1/4-inch strips red bell pepper", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 16, "PREP"),  # "1/4-inch" (Kept)
            (17, 23, "PREP"),  # "strips" (Kept)
            (24, 27, "NAME"),  # "red" (from original NAME "red bell pepper" 24-39)
            (28, 32, "NAME"),  # "bell" (from original NAME "red bell pepper" 24-39)
            (33, 39, "NAME")  # "pepper" (from original NAME "red bell pepper" 24-39)
        ]
    }),

    # Example 64
    ("3/4 cup 1/2-inch strips snow peas", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 16, "PREP"),  # "1/2-inch" (Kept)
            (17, 23, "PREP"),  # "strips" (Kept)
            (24, 28, "NAME"),  # "snow" (from original NAME "snow peas" 24-33)
            (29, 33, "NAME")  # "peas" (from original NAME "snow peas" 24-33)
        ]
    }),

    # Example 65
    ("5 cups peeled and chopped firm, ripe mangoes", {
        "entities": [
            (0, 1, "QTY"),  # "5" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 30, "PREP"),  # "peeled" (Kept from (7,13))
            # Comma at 30 is "O"
            (32, 36, "PREP"),  # "ripe" (Kept from (32,36))
            (37, 44, "NAME")  # "mangoes"
        ]
    }),

    # Example 66
    ("1 large or 2 small ripe mangoes, peeled, fruit sliced from the pit, and diced", {
        "entities": [
            (0, 1, "QTY"),         # "1"
            (2, 7, "UNIT"),        # "large" (size unit for the primary)
            # "or" (8,10) is O
            (11, 12, "ALT_QTY"),   # "2" (alternative quantity)
            (13, 18, "ALT_UNIT"),  # "small" (alternative size unit)
            (19, 23, "PREP"),      # "ripe"
            (24, 31, "NAME"),      # "mangoes"
            # Comma at 31 is O
            (33, 39, "PREP"),      # "peeled"
            # Comma at 39 is O
            (41, 46, "PREP"),      # "fruit" (can be part of "fruit sliced..." PREP) - or NAME if you consider "fruit" a sub-component
            (47, 53, "PREP"),      # "sliced"
            (54, 66, "PREP"),      # "from the pit"
            # Comma at 66 is O
            # "and" (68,71) is O
            (72, 77, "PREP")       # "diced"
        ]
    }),

    ("1 package (14 ounces) Pepperidge Farm® Herb Seasoned Stuffing", {  # Assuming original end span was 66
        "entities": [
            (0, 1, "QTY"),
            (2, 9, "UNIT"),
            (10, 21, "COMMENT"),
            (22, 61, "NAME"),
        ]
    }),

    # Example 68
    ("1 tablespoon plus 1 teaspoon McCormick® Grill Mates® Molasses Bacon Seasoning, divided", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 28, "COMMENT"),  # "plus 1 teaspoon" (Kept)
            (29, 39, "NAME"),  # "McCormick®" (from original NAME 29-77)
            (40, 45, "NAME"),  # "Grill" (from original NAME 29-77)
            (46, 52, "NAME"),  # "Mates®" (from original NAME 29-77)
            (53, 61, "NAME"),  # "Molasses" (from original NAME 29-77)
            (62, 67, "NAME"),  # "Bacon" (from original NAME 29-77)
            (68, 77, "NAME"),  # "Seasoning" (from original NAME 29-77)
            # Comma at 77 is "O"
            (79, 86, "COMMENT")  # "divided" (Kept)
        ]
    }),

    # Example 69
    ("3 pounds canned hominy, drained", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 15, "PREP"),  # "canned" (Kept)
            (16, 22, "NAME"),  # "hominy"
            # Comma at 22 is "O"
            (24, 31, "PREP")  # "drained" (Kept)
        ]
    }),

    # Example 70
    ("Chopped green onion, for garnish", {
        "entities": [
            (0, 7, "PREP"),  # "Chopped" (Kept)
            (8, 13, "NAME"),  # "green" (from original NAME 8-13)
            (14, 19, "NAME"),  # "onion" (from original NAME 14-19)
            # Comma at 19 is "O"
            (21, 32, "COMMENT")  # "for garnish" (Kept)
        ]
    }),

    # Example 71
    ("1 pound peeled and deveined shrimp", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 27, "PREP"),  # "peeled" (Kept from original (8,14,"PREP"))
            (28, 34, "NAME")  # "shrimp"
        ]
    }),

    # Example 72
    ("2 grapefruits", {"entities": [
        (0, 1, "QTY"),  # "2" (Kept)
        (2, 13, "NAME")  # "grapefruits"
    ]}),

    # Example 73
    ("2 jars Spanish olives", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "COMMENT"),  # "jars"
            (7, 14, "NAME"),  # "Spanish" (from original NAME 7-14)
            (15, 21, "NAME")  # "olives" (from original NAME 15-21)
        ]
    }),

    # Example 74
    ("2 bags frozen green peas", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "bags"
            (7, 13, "NAME"),  # "frozen" (Kept)
            (14, 19, "NAME"),  # "green" (from original NAME 14-19)
            (20, 24, "NAME")  # "peas" (from original NAME 20-24)
        ]
    }),

    # Example 75
    ("1 1/2 pounds (about 4 1/2 cups) frozen peas", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 31, "COMMENT"),  # "(about 4 1/2 cups)" (Kept)
            (32, 38, "NAME"),  # "frozen" (Kept)
            (39, 43, "NAME")  # "peas"
        ]
    }),

    # Example 76
    ("3 pomegranates, peeled and seeded", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 14, "NAME"),  # "pomegranates"
            # Comma at 14 is "O"
            (16, 33, "PREP"),  # "peeled" (Kept from original (16,22,"PREP"))
        ]
    }),

    # Example 77
    ("3 cups plain croutons", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 12, "PREP"),  # "plain" (Kept)
            (13, 21, "NAME")  # "croutons"
        ]
    }),

    # Example 78
    ("1 knob of ginger, peeled and chopped", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 9, "COMMENT"),  # "knob"
            (10, 16, "NAME"),  # "ginger"
            # Comma at 16 is "O"
            (18, 36, "PREP"),  # "peeled" (Kept from original (18,24,"PREP"))
        ]
    }),

    # Example 79
    ("1 tablespoon Old Bay seasoning", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 16, "NAME"),  # "Old" (from original NAME 13-16)
            (17, 20, "NAME"),  # "Bay" (from original NAME 17-20)
            (21, 30, "NAME")  # "seasoning" (from original NAME 21-30)
        ]
    }),

    # Example 80
    ("1/2 cup shredded and chopped iceberg lettuce", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 28, "PREP"),  # "shredded" (from original PREP (8,16))
            (29, 36, "NAME"),  # "iceberg" (from original NAME 29-36)
            (37, 44, "NAME")  # "lettuce" (from original NAME 37-44)
        ]
    }),

    # Example 81
    ("10 tomatillos, husked", {
        "entities": [
            (0, 2, "QTY"),  # "10" (Kept)
            (3, 13, "NAME"),  # "tomatillos"
            # Comma at 13 is "O"
            (15, 21, "PREP")  # "husked" (Kept)
        ]
    }),

    # Example 82
    ("1 clove", {"entities": [
        (0, 1, "QTY"),  # "1" (Kept)
        (2, 7, "NAME")  # "clove"
    ]}),

    # Example 83
    ("2 medium bowls", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "medium"
            (9, 14, "NAME")  # "bowls"
        ]
    }),

    # Example 84
    ("4 ounces Monterey Jack cheese, shredded", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 17, "NAME"),  # "Monterey" (from original NAME 9-17)
            (18, 22, "NAME"),  # "Jack" (from original NAME 18-22)
            (23, 29, "NAME"),  # "cheese" (from original NAME 23-29)
            # Comma at 29 is "O"
            (31, 39, "PREP")  # "shredded" (Kept)
        ]
    }),

    # Example 85
    ("16 ounces Chihuahua or Oaxaca cheese, shredded", {
        "entities": [
            (0, 2, "QTY"),  # "16" (Kept)
            (3, 9, "UNIT"),  # "ounces"
            (10, 19, "NAME"),  # "Chihuahua"
            (20, 29, "ALT_NAME"),  # "or Oaxaca cheese" (Kept)
            (30, 36, "NAME"),  # "or Oaxaca cheese" (Kept)
            # Comma at 36 is "O"
            (38, 46, "PREP")  # "shredded" (Kept)
        ]
    }),

    # Example 86
    ("2 cups seeded and cubed watermelon", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 23, "PREP"),  # "seeded" (Kept from original (7,13))
            (24, 34, "NAME")  # "watermelon"
        ]
    }),

    # Example 87
    ("6 ounces club soda", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 13, "NAME"),  # "club" (from original NAME 9-13)
            (14, 18, "NAME")  # "soda" (from original NAME 14-18)
        ]
    }),

    # Example 88
    ("1 bottle white wine, such as Sancerre or Sauvignon Blanc", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "COMMENT"),  # "bottle"
            (9, 14, "NAME"),  # "white" (from original NAME 9-14)
            (15, 19, "NAME"),  # "wine" (from original NAME 15-19)
            # Comma at 19 is "O"
            (21, 56, "COMMENT")  # "such as Sancerre or Sauvignon Blanc" (Kept)
        ]
    }),

    # Example 89
    ("2 oz. of club soda", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 5, "UNIT"),  # "oz."
            (6, 8, "PREP"),  # "of" (Kept)
            (9, 13, "NAME"),  # "club" (from original NAME 9-13)
            (14, 18, "NAME")  # "soda" (from original NAME 14-18)
        ]
    }),

    # Example 90
    ("1 cup cut fruit from in store service deli", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 9, "PREP"),  # "cut" (Kept)
            (10, 15, "NAME"),  # "fruit"
            (16, 42, "COMMENT")  # "from in store service deli" (Kept)
        ]
    }),

    # Example 91
    ("1 single-serve cup fruit flavored custard style low fat yogurt", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 14, "COMMENT"),  # "single-serve" (Original label was UNIT)
            (15, 18, "UNIT"),  # "cup" (Original label was UNIT)
            (19, 47, "COMMENT"),  # "fruit" (Original label was NAME)
            (48, 62, "NAME"),  # "low" (Original label was PREP)
        ]
    }),

    # Example 92
    ("1 pint mascarpone", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 6, "UNIT"),  # "pint"
            (7, 17, "NAME")  # "mascarpone"
        ]
    }),

    # Example 93
    ("1/3 teaspoon clove", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 18, "NAME")  # "clove"
        ]
    }),

    # Example 94
    ("3 ounces sushi-quality ahi tuna loin, sinews removed", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 22, "PREP"),  # "sushi-quality" (Kept)
            (23, 26, "NAME"),  # "ahi"
            (27, 31, "NAME"),  # "tuna"
            (32, 36, "NAME"),  # "loin"
            # Comma at 36 is "O"
            (38, 52, "PREP")  # "sinews removed" (Kept)
        ]
    }),

    # Example 95
    ("1/2 cup drained and canned hominy", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 26, "PREP"),  # "drained" (from original PREP (8,15))
            (27, 33, "NAME")  # "hominy"
        ]
    }),

    # Example 96
    ("5 medium or 12 baby onions", {
        "entities": [
            (0, 1, "QTY"),  # "5" (Kept)
            (2, 8, "UNIT"),  # "medium"
            (9, 19, "ALT_NAME"),  # "or 12 baby onions" (Kept)
            (20, 26, "NAME")  # "or 12 baby onions" (Kept)
            # The word "onions" is part of the ALT_NAME here. If it was a separate NAME entity originally, it would be split.
        ]
    }),

    # Example 97
    ("1/4 pound of bacon- cubed", {  # bacon- is one token.
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 12, "PREP"),  # "of" (Kept)
            (13, 19, "NAME"),  # "bacon-" (token includes hyphen)
            (20, 25, "PREP")  # "cubed" (Kept)
        ]
    }),

    # Example 98
    ("2 tablespoons canola or other neutral oil, or olive oil", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 20, "NAME"),  # "canola"
            (21, 37, "ALT_NAME"),  # "or other neutral oil" (Kept)
            (38, 41, "NAME"),  # "or other neutral oil" (Kept)
            # Comma at 41 is "O"
            (43, 55, "ALT_NAME")  # "or olive oil" (Kept)
        ]
    }),

    # Example 99
    ("1 clove garlic", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 14, "NAME")  # "garlic"
        ]
    }),

    # Example 100
    ("2 large or 3 medium onions, cut into eighths", {
        "entities": [
            # Primary Item description
            (0, 1, "QTY"),         # "2"
            (2, 7, "UNIT"),        # "large"
            # "or" (8,10) is O
            # Alternative description for the same item
            (11, 12, "ALT_QTY"),   # "3" (alternative quantity for onions)
            (13, 19, "ALT_UNIT"),  # "medium" (alternative size unit for onions)
            # Core Item Name
            (20, 26, "NAME"),      # "onions"
            # Comma at 26 is O
            # Preparation
            (28, 44, "PREP")       # "cut into eighths"
        ]
    }),

    # Example 101
    ("4 mediumtolarge potatoes, peeled and cut into 1inch chunks", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 15, "UNIT"),  # "mediumtolarge" (tokenized as one)
            (16, 24, "NAME"),  # "potatoes"
            # Comma at 24 is "O"
            (26, 58, "PREP"),  # "peeled" (Kept from original (26,32,"PREP"))
        ]
    }),

    # Example 102
    ("1/4 teaspoon store-bought or homemade garam masala, recipe follows", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 25, "PREP"),  # "store-bought" (Kept)
            (26, 37, "ALT_NAME"),  # "or homemade" (Kept)
            (38, 43, "NAME"),  # "garam" (from original NAME "garam masala" 38-50)
            (44, 50, "NAME"),  # "masala" (from original NAME "garam masala" 38-50)
            # Comma at 50 is "O"
            (52, 66, "COMMENT")  # "recipe follows" (Kept)
        ]
    }),

    # Example 103
    ("Whipped cream, optional", {
        "entities": [
            (0, 13, "NAME"),  # "cream"
            # Comma at 13 is "O"
            (15, 23, "COMMENT")  # "optional" (Kept)
        ]
    }),

    # Example 104
    ("3 large cinnamon sticks (if you have the kind you get at Indian stores, it's about 3 tablespoons of cinnamon bark bits)",
     {
         "entities": [
             (0, 1, "QTY"),  # "3" (Kept)
             (2, 7, "UNIT"),  # "large"
             (8, 23, "NAME"),  # "cinnamon" (from original NAME "cinnamon sticks" 8-23)
             (24, 119, "COMMENT")  # "(if you have...bark bits)" (Kept)
         ]
     }),

    # Example 105
    ("4 (6-ounce) skirt steaks", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 11, "COMMENT"),  # "(6-ounce)" (Kept)
            (12, 17, "NAME"),  # "skirt" (from original NAME "skirt steaks" 12-24)
            (18, 24, "NAME")  # "steaks" (from original NAME "skirt steaks" 12-24)
        ]
    }),

    # Example 106
    ("3 endive", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 8, "NAME")  # "endive"
        ]
    }),

    # Example 107
    ("2 tablespoons chopped fresh tarragon leaves", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, "PREP"),  # "chopped" (Kept)
            (22, 27, "PREP"),  # "fresh" (Kept)
            (28, 36, "NAME"),  # "tarragon" (from original NAME "tarragon leaves" 28-43)
            (37, 43, "NAME")  # "leaves" (from original NAME "tarragon leaves" 28-43)
        ]
    }),

    # Example 108
    ("1/4 cup (5 or 6) sun-dried tomatoes in oil, drained", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 16, "COMMENT"),  # "(5 or 6)" (Kept)
            (17, 26, "NAME"),  # "sun-dried" (Kept)
            (27, 35, "NAME"),  # "tomatoes"
            (36, 42, "PREP"),  # "in oil" (Kept)
            # Comma at 42 is "O"
            (44, 51, "PREP")  # "drained" (Kept)
        ]
    }),

    # Example 109
    ("Topping suggestions: shredded cheese, fresh mozzarella cheese, fresh basil leaves, sliced tomatoes, marinara sauce, prosciutto, sliced olives, roasted red bell peppers, lettuce leaves, arugula, ketchup, pesto.",
     {
         "entities": [
             (0, 20, "COMMENT"),  # "Topping suggestions:" (Kept)
             (21, 209, "COMMENT")  # "shredded cheese...pesto." (Kept, includes final period)
         ]
     }),

    # Example 110
    ("1 cup golden raisins, packed tightly", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "NAME"),  # "golden" (from original NAME "golden raisins" 6-20)
            (13, 20, "NAME"),  # "raisins" (from original NAME "golden raisins" 6-20)
            # Comma at 20 is "O"
            (22, 36, "PREP")  # "packed tightly" (Kept)
        ]
    }),

    # Example 111
    ("1 cup chopped and cooked shredded chicken", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 24, "PREP"),  # "chopped" (Kept from original (6,13,"PREP"))
            (25, 41, "NAME"),  # "shredded" (Kept from original (25,33,"PREP"))=
        ]
    }),

    # Example 112
    ("1 cup well drained and chopped marinated artichoke hearts", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 40, "PREP"),  # "well" (Kept from original (6,10,"PREP"))\
            (41, 50, "NAME"),  # "artichoke" (from original NAME "artichoke hearts" 41-57)
            (51, 57, "NAME")  # "hearts" (from original NAME "artichoke hearts" 41-57)
        ]
    }),

    # Example 113
    ("1/2 teaspoon crushed or ground red pepper or pepperoncini", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 20, "NAME"),  # "crushed" (Original label was NAME)
            (21, 30, "ALT_NAME"),  # "or ground" (Kept)
            (31, 34, "NAME"),  # "red" (Original label was NAME)
            (35, 41, "NAME"),  # "pepper" (Original label was NAME)
            (42, 57, "ALT_NAME")  # "or pepperoncini" (Kept)
        ]
    }),

    # Example 114
    ("1 teaspoon (about a 1/3 palm full) red chili flakes or ground pepperoncini", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 34, "COMMENT"),  # "(about a 1/3 palm full)" (Kept)
            (35, 38, "NAME"),  # "red" (Original label was NAME)
            (39, 44, "NAME"),  # "chili" (Original label was NAME)
            (45, 51, "NAME"),  # "flakes" (Original label was NAME)
            (52, 74, "ALT_NAME")  # "or ground pepperoncini" (Kept)
        ]
    }),

    # Example 115
    ("1 jicama, peeled and diced", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "NAME"),  # "jicama"
            # Comma at 8 is "O"
            (10, 26, "PREP"),  # "peeled" (Kept)
        ]
    }),

    # Example 116
    ("3 tomatillos, husks removed and diced", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 12, "NAME"),  # "tomatillos"
            # Comma at 12 is "O"
            (14, 37, "PREP"),  # "husks removed" (Kept)
        ]
    }),

    # Example 117
    ("3 pickling cucumbers, peeled, seeded, and diced", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 10, "NAME"),  # "pickling" (from original NAME "pickling cucumbers" 2-20)
            (11, 20, "NAME"),  # "cucumbers" (from original NAME "pickling cucumbers" 2-20)
            # Comma at 20 is "O"
            (22, 47, "PREP"),  # "peeled" (Kept)
        ]
    }),

    # Example 118
    ("4 ripe tomatoes, seeded and diced", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "PREP"),  # "ripe" (Kept)
            (7, 15, "NAME"),  # "tomatoes"
            # Comma at 15 is "O"
            (17, 33, "PREP"),  # "seeded" (Kept from original (17,23,"PREP"))
        ]
    }),

    # Example 119
    ("1 slice bread, crusts removed, soaked and squeezed", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "COMMENT"),  # "slice"
            (8, 13, "NAME"),  # "bread"
            # Comma at 13 is "O"
            (15, 50, "PREP"),  # "crusts removed" (Kept)
        ]
    }),

    # Example 120
    ("1 tablespoon seeded and minced jalapeno", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 30, "PREP"),  # "seeded" (Kept from original (13,19,"PREP"))
            (31, 39, "NAME")  # "jalapeno"
        ]
    }),

    # Example 121
    ("1 jalapeno pepper, seeded and minced", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 10, "NAME"),  # "jalapeno" (from original NAME "jalapeno pepper" 2-17)
            (11, 17, "NAME"),  # "pepper" (from original NAME "jalapeno pepper" 2-17)
            # Comma at 17 is "O"
            (19, 36, "PREP"),  # "seeded" (Kept from original (19,25,"PREP"))
        ]
    }),

    # Example 122
    ("6 parsnips (about 1 1/2 pounds) peeled and thinly sliced", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 10, "NAME"),  # "parsnips"
            (11, 31, "COMMENT"),  # "(about 1 1/2 pounds)" (Kept)
            (32, 56, "PREP"),  # "peeled" (Kept from original (32,38,"PREP"))
        ]
    }),

    # Example 123
    ("Sprinkling fine sea salt", {
        "entities": [
            (0, 10, "COMMENT"),  # "Sprinkling" (Original label was UNIT)
            (11, 15, "PREP"),  # "fine" (Kept)
            (16, 19, "NAME"),  # "sea" (from original NAME "sea salt" 16-24)
            (20, 24, "NAME")  # "salt" (from original NAME "sea salt" 16-24)
        ]
    }),

    # Example 124
    ("2 ounces mushroom stems", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 17, "NAME"),  # "mushroom" (from original NAME "mushroom stems" 9-23)
            (18, 23, "NAME")  # "stems" (from original NAME "mushroom stems" 9-23)
        ]
    }),

    # Example 125
    ("14 oz. can fat-free or regular sweetened condensed milk", {
        "entities": [
            (0, 2, "QTY"),  # "14" (Kept)
            (3, 6, "UNIT"),  # "oz."
            (7, 10, "UNIT"),  # "can" (Original label was UNIT)
            (11, 19, "NAME"),  # "fat-free" (Kept)
            (20, 30, "ALT_NAME"),  # "or regular" (Kept)
            (31, 40, "NAME"),  # "sweetened" (Kept from original (31,40,"PREP"))
            (41, 50, "NAME"),  # "condensed" (from original NAME "condensed milk" 41-55)
            (51, 55, "NAME")  # "milk" (from original NAME "condensed milk" 41-55)
        ]
    }),

    # Example 126
    ("6 oz. reduced-fat or regular creamy peanut butter", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 5, "UNIT"),  # "oz."
            (6, 17, "NAME"),  # "reduced-fat" (Kept)
            (18, 28, "ALT_NAME"),  # "or regular" (Kept)
            (29, 35, "NAME"),  # "creamy" (Kept from original (29,35,"PREP"))
            (36, 42, "NAME"),  # "peanut" (from original NAME "peanut butter" 36-49)
            (43, 49, "NAME")  # "butter" (from original NAME "peanut butter" 36-49)
        ]
    }),

    # Example 127
    ("2 naval or other large oranges", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 7, "NAME"),  # "naval"
            (8, 22, "ALT_NAME"),  # "or other large oranges" (Kept)
            (23, 30, "ALT_NAME")  # "or other large oranges" (Kept)
        ]
    }),

    # Example 128
    ("Four 6-ounce flounder fillets", {
        "entities": [
            (0, 4, "QTY"),  # "Four" (Kept)
            (5, 12, "COMMENT"),  # "6-ounce" (Kept)
            (13, 29, "NAME"),  # "flounder"
        ]
    }),

    # Example 130
    ("1/2 cup rinsed and drained canned chickpeas", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 33, "PREP"),  # "rinsed" (Kept from original (8,14,"PREP"))
            (34, 43, "NAME")  # "chickpeas"
        ]
    }),

    # Example 131
    ("2 cups (208 grams) farro, rinsed", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 18, "COMMENT"),  # "(208 grams)" (Kept)
            (19, 24, "NAME"),  # "farro"
            # Comma at 24 is "O"
            (26, 32, "PREP")  # "rinsed" (Kept)
        ]
    }),

    # Example 132
    ("1/2 cup coarsely chopped or torn fresh mint leaves", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 38, "PREP"),  # "coarsely" (Kept from original (8,16,"PREP"))
            (39, 43, "NAME"),  # "mint" (from original NAME "mint leaves" 39-50)
            (44, 50, "NAME")  # "leaves" (from original NAME "mint leaves" 39-50)
        ]
    }),

    # Example 133
    ("2 tablespoons peeled and grated ginger", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 31, "PREP"),  # "peeled" (Kept from original (14,20,"PREP"))
            (32, 38, "NAME")  # "ginger"
        ]
    }),

    # ... (all previous examples from your earlier chunks would be here) ...

    # Example 1
    ("1/2 pear, peeled, cored and grated on the large holes of a box grater", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 8, "NAME"),  # "pear"
            # Comma at 8 is "O"
            (10, 16, "PREP"),  # "peeled" (Kept)
            # Comma at 16 is "O"
            (18, 69, "PREP"),  # "cored" (Kept from original (18,23,"PREP"))
        ]
    }),

    # Example 2
    ("Serving suggestion: Steamed rice", {
        "entities": [
            (0, 18, "COMMENT"),  # "Serving suggestion:" (Kept)
            # Space at 18, Colon at 18 is part of COMMENT.
            (20, 27, "NAME"),  # "Steamed" (from original NAME "Steamed rice" 20-32)
            (28, 32, "NAME")  # "rice" (from original NAME "Steamed rice" 20-32)
        ]
    }),

    # Example 3
    ("5 large leaves fresh basil, chopped", {
        "entities": [
            (0, 1, "QTY"),  # "5" (Kept)
            (2, 7, "UNIT"),  # "large"
            (8, 14, "COMMENT"),  # "leaves" (Original label was COMMENT)
            (15, 20, "PREP"),  # "fresh" (Kept)
            (21, 26, "NAME"),  # "basil"
            # Comma at 26 is "O"
            (28, 35, "PREP")  # "chopped" (Kept)
        ]
    }),

    # Example 4
    ("3 pounds sweetbread", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 19, "NAME")  # "sweetbread"
        ]
    }),

    # Example 5
    ("4 Hass avocados", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "NAME"),  # "Hass" (from original NAME 2-6)
            (7, 15, "NAME")  # "avocados" (from original NAME 7-15)
        ]
    }),

    # Example 6
    ("3 pounds cleaned and cut Kobe beef into 3-inch long strips", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 24, "PREP"),  # "cleaned" (Kept from original (9,16,"PREP"))
            (25, 29, "NAME"),  # "Kobe" (from original NAME 25-29)
            (30, 34, "NAME"),  # "beef" (from original NAME 30-34)
            (35, 58, "PREP")  # "into 3-inch long strips" (Kept)
        ]
    }),

    ("1 1/2 tablespoons active, dry, granulated, yeast", {  # Assuming comma is O after granulated
        "entities": [
            (0, 5, "QTY"),
            (6, 17, "UNIT"),
            (18, 24, "PREP"),  # "active"
            # Comma (24,25) "O"
            (26, 29, "PREP"),  # "dry"
            # Comma (29,30) "O"
            (31, 41, "PREP"),  # "granulated"
            # Comma (41,42) "O"
            (43, 48, "NAME")
        ]
    }),

    # Example 8
    ("2 tablespoons cleaned and roughly chopped cilantro leaves", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 33, "PREP"),  # "cleaned" (Kept from original (14,21,"PREP"))
            (34, 41, "PREP"),  # "chopped" (Kept from original (34,41,"PREP"))
            (42, 50, "NAME"),  # "cilantro" (from original NAME 42-50)
            (51, 57, "NAME")  # "leaves" (from original NAME 51-57)
        ]
    }),

    # Example 9
    ("9 ounces/250 g mincemeat (just over half a jar), or make your own, recipe follows", {
        "entities": [
            (0, 1, "QTY"),  # "9" (Kept)
            (2, 12, "UNIT"),  # "ounces/250" (Kept)
            (13, 14, "COMMENT"),  # "g"
            (15, 24, "NAME"),  # "mincemeat"
            (25, 47, "COMMENT"),  # "(just over half a jar)" (Kept)
            # Comma at 47 is "O"
            (49, 81, "COMMENT")  # "or make your own, recipe follows" (Kept)
        ]
    }),

    # Example 10
    ("5 grapefruit (or 15 of just one fruit)", {
        "entities": [
            (0, 1, "QTY"),  # "5" (Kept)
            (2, 12, "NAME"),  # "grapefruit"
            (13, 37, "COMMENT")  # "(or 15 of just one fruit)" (Kept)
        ]
    }),

    # Example 11
    ("1 (8-ounce) block Emmentaler Swiss cheese", {
        "entities": [
            (0, 1, "COMMENT"),  # "1" (Original label was COMMENT)
            (3, 4, "QTY"),  # "8" (Kept)
            (5, 10, "UNIT"),  # "ounce"
            (12, 17, "COMMENT"),  # "block" (Original label was COMMENT)
            (18, 28, "NAME"),  # "Emmentaler" (from original NAME 18-28)
            (29, 34, "NAME"),  # "Swiss" (from original NAME 29-34)
            (35, 41, "NAME")  # "cheese" (from original NAME 35-41)
        ]
    }),

    # Example 12
    ("1/2 pound sliced, thick-deli-cut or rotisserie turkey breast, chopped", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 16, "PREP"),  # "sliced" (Kept, original has comma after)
            # Comma at 16 is "O"
            (18, 32, "PREP"),  # "thick-deli-cut" (Kept)
            (33, 46, "ALT_NAME"),  # "or rotisserie" (Kept)
            (47, 53, "NAME"),  # "turkey" (from original NAME 47-53)
            (54, 60, "NAME"),  # "breast" (from original NAME 54-60)
            # Comma at 60 is "O"
            (62, 69, "PREP")  # "chopped" (Kept)
        ]
    }),

    # Example 13
    ("1 cup drained and finely diced roasted red peppers", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 30, "PREP"),  # "drained and finely diced" (Kept, this was your original single PREP span)
            (31, 38, "NAME"),  # "roasted" (from original NAME "roasted red peppers" 31-50)
            (39, 42, "NAME"),  # "red" (from original NAME "roasted red peppers" 31-50)
            (43, 50, "NAME")  # "peppers" (from original NAME "roasted red peppers" 31-50)
        ]
    }),

    # Example 14
    ("2 teaspoons freshly ground black pepper, not super fine and not coarse, somewhere in between", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 11, "UNIT"),  # "teaspoons"
            (12, 19, "PREP"),  # "freshly" (from original PREP "freshly ground" 12-26)
            (20, 26, "PREP"),  # "ground" (from original PREP "freshly ground" 12-26)
            (27, 32, "NAME"),  # "black" (from original NAME "black pepper" 27-39)
            (33, 39, "NAME"),  # "pepper" (from original NAME "black pepper" 27-39)
            # Comma at 39 is "O"
            (41, 92, "COMMENT")  # "not super fine and not coarse, somewhere in between" (Kept)
        ]
    }),

    ("2 pounds prawns, shelled, tails removed, heads on",
     {  # Assuming "tails removed" and "heads on" are separate PREPs
         "entities": [
             (0, 1, "QTY"),
             (2, 8, "UNIT"),
             (9, 15, "NAME"),
             (17, 24, "PREP"),  # "shelled"
             (26, 39, "PREP"),  # "tails removed" (Original note said this was correct span for one part)
             (41, 49, "PREP")  # "heads on" (Assuming this was the other part of the PREP)
         ]
     }),

    # Example 16
    ("1 medium jicama, peeled and cut into cubes about 3/8-inch thick (about 2 cups)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "UNIT"),  # "medium"
            (9, 15, "NAME"),  # "jicama"
            # Comma at 15 is "O"
            (17, 63, "PREP"),  # "peeled" (Kept)
            (64, 78, "COMMENT")  # "(about 2 cups)" (Kept)
        ]
    }),

    # Example 17
    ("3 red or green jalapeno peppers or other small chiles of your choice, thinly sliced", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 5, "NAME"),  # "red"
            (6, 14, "ALT_NAME"),  # "or green jalapeno" (Kept)
            (15, 31, "NAME"),  # "peppers"
            (32, 68, "ALT_NAME"),  # "or other small chiles of your choice" (Kept)
            # Comma at 68 is "O"
            (70, 83, "PREP")  # "thinly sliced" (Kept)
        ]
    }),

    # Example 18
    ("4 cups mixed red and green seedless grapes", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 12, "PREP"),  # "mixed" (from original PREP "mixed red and green" 7-26)
            (13, 16, "PREP"),  # "red" (from original PREP "mixed red and green" 7-26)
            (17, 20, "PREP"),  # "and" (from original PREP "mixed red and green" 7-26) - *Unusual*
            (21, 26, "PREP"),  # "green" (from original PREP "mixed red and green" 7-26)
            (27, 35, "NAME"),  # "seedless" (from original NAME "seedless grapes" 27-42)
            (36, 42, "NAME")  # "grapes" (from original NAME "seedless grapes" 27-42)
        ]
    }),

    # Example 19
    ("1/4 cup diced onion", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "PREP"),  # "diced" (Kept)
            (14, 19, "NAME")  # "onion"
        ]
    }),

    # Example 20
    ("1/4 cup shelled, roasted and salted pistachios, ground", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "PREP"),  # "shelled" (Kept from original (8,15,"PREP"))
            # Comma at 15 is "O"
            (17, 24, "NAME"),  # "roasted" (from original NAME "roasted and salted pistachios" 17-46)
            (25, 28, "NAME"),  # "and" (from original NAME 17-46) - *Unusual*
            (29, 35, "NAME"),  # "salted" (from original NAME 17-46)
            (36, 46, "NAME"),  # "pistachios" (from original NAME 17-46)
            # Comma at 46 is "O"
            (48, 54, "PREP")  # "ground" (Kept)
        ]
    }),

    # Example 21
    ("1/2 cup cooked quinoa", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "cooked" (Kept)
            (15, 21, "NAME")  # "quinoa"
        ]
    }),

    # Example 22
    ("2 tablespoons peeled and minced fresh ginger", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 37, "PREP"),  # "peeled and minced fresh" (Kept)
            (38, 44, "NAME")  # "ginger"
        ]
    }),

    # Example 23
    ("1/4 cabbage (about 1/2 pound)", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 11, "NAME"),  # "cabbage"
            (12, 28, "COMMENT")  # "(about 1/2 pound)" (Kept)
        ]
    }),

    # Example 24
    ("1/4 pound ground lean sirloin", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 16, "PREP"),  # "ground" (from original PREP "ground lean" 10-21)
            (17, 21, "PREP"),  # "lean" (from original PREP "ground lean" 10-21)
            (22, 29, "NAME")  # "sirloin"
        ]
    }),

    # Example 25
    ("2 cups prepared and crumbled cornbread", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 15, "PREP"),  # "prepared" (from original PREP "prepared and crumbled" 7-28)
            (16, 19, "PREP"),  # "and" (from original PREP "prepared and crumbled" 7-28) - *Unusual*
            (20, 28, "PREP"),  # "crumbled" (from original PREP "prepared and crumbled" 7-28)
            (29, 38, "NAME")  # "cornbread"
        ]
    }),

    ("1/2 teaspoon store-bought or homemade garam masala, recipe follows", {  # Corrected for Garam Masala tokens
        "entities": [
            (0, 3, "QTY"), (4, 12, "UNIT"), (13, 25, "PREP"),
            (26, 37, "ALT_NAME"),
            (38, 43, "NAME"),  # "garam"
            (44, 50, "NAME"),  # "masala"
            (52, 66, "COMMENT")
        ]
    }),

    # Example 27
    ("1 (1-inch thumb) ginger", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 16, "COMMENT"),  # "(1-inch thumb)" (Kept)
            (17, 23, "NAME")  # "ginger"
        ]
    }),

    # Example 28
    ("1 cup store bought BBQ sauce", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 11, "PREP"),  # "store" (from original PREP "store bought" 6-18)
            (12, 18, "PREP"),  # "bought" (from original PREP "store bought" 6-18)
            (19, 22, "NAME"),  # "BBQ" (from original NAME "BBQ sauce" 19-28)
            (23, 28, "NAME")  # "sauce" (from original NAME "BBQ sauce" 19-28)
        ]
    }),

    # Example 29 (Duplicate)
    ("1 pound peeled and deveined large shrimp", {"entities": [
        (0, 1, "QTY"), (2, 7, "UNIT"),
        (8, 27, "PREP"),  # peeled and deveined
        (28, 33, "NAME"), (34, 40, "NAME")
    ]}),

    # Example 30
    ("4 (12-ounce) steaks, your choice", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 12, "COMMENT"),  # "(12-ounce)" (Kept)
            (13, 19, "NAME"),  # "steaks"
            # Comma at 19 is "O"
            (21, 32, "COMMENT")  # "your choice" (Kept)
        ]
    }),

    # Example 31
    ("1 peach, diced", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "NAME"),  # "peach"
            # Comma at 7 is "O"
            (9, 14, "PREP")  # "diced" (Kept)
        ]
    }),

    # Example 32
    ("1 cup steel-cut oatmeal", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 15, "PREP"),  # "steel-cut" (Kept)
            (16, 23, "NAME")  # "oatmeal"
        ]
    }),

    # Example 33
    ("4 1/2 pounds bone-in short ribs, cut into 4-inch pieces", {
        "entities": [
            (0, 5, "QTY"),  # "4 1/2" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 20, "NAME"),  # "bone-in" (Kept)
            (21, 26, "NAME"),  # "short" (from original NAME "short ribs" 21-31)
            (27, 31, "NAME"),  # "ribs" (from original NAME "short ribs" 21-31)
            # Comma at 31 is "O"
            (33, 55, "PREP")  # "cut into 4-inch pieces" (Kept)
        ]
    }),

    # Example 34
    ("2 pounds (16- to 20-count) peeled and deveined shrimp (2 1/2 pounds in the shell)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 26, "COMMENT"),  # "(16- to 20-count)" (Kept)
            (27, 46, "PREP"),  # "peeled" (from original PREP "peeled and deveined" 27-46)
            (47, 53, "NAME"),  # "shrimp"
            (54, 81, "COMMENT")  # "(2 1/2 pounds in the shell)" (Kept)
        ]
    }),

    # Example 35
    ("3/4 pound fatback", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 17, "NAME")  # "fatback"
        ]
    }),

    # Example 36
    ("1/2 pound thinly-sliced rare deli roast beef", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 23, "PREP"),  # "thinly-sliced" (from original PREP "thinly-sliced rare" 10-28)
            (24, 28, "PREP"),  # "rare" (from original PREP "thinly-sliced rare" 10-28)
            (29, 33, "NAME"),  # "deli" (from original NAME "deli roast beef" 29-44)
            (34, 39, "NAME"),  # "roast" (from original NAME "deli roast beef" 29-44)
            (40, 44, "NAME")  # "beef" (from original NAME "deli roast beef" 29-44)
        ]
    }),

    # Example 37
    ("3/4 cup sliced and drained pickled beets", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 26, "PREP"),  # "sliced and drained pickled" (Kept)
            (27, 40, "NAME")  # "beets"
        ]
    }),

    ("2 cups (12 ounces) fresh or frozen, thawed, and drained blueberries", {  # Assuming commas are O
        "entities": [
            (0, 1, "QTY"), (2, 6, "UNIT"), (7, 18, "COMMENT"),
            (19, 24, "PREP"), (25, 34, "ALT_NAME"),
            # Comma at 34 O
            (36, 42, "PREP"),  # "thawed"
            # Comma at 42 O
            # "and" at 44 O
            (48, 55, "PREP"),  # "drained"
            (56, 67, "NAME")
        ]
    }),

    # Example 39
    ("1 1/4 cups plus 1 tablespoon 63 degrees F. water (.67 pound)", {  # If original (11,42) was one comment
        "entities": [
            (0, 5, "QTY"), (6, 10, "UNIT"),
            (11, 42, "COMMENT"),  # "plus 1 tablespoon 63 degrees F."
            (43, 48, "NAME"),
            (49, 60, "COMMENT")
        ]
    }),

    # Example 40
    ("1 teaspoon minus 1/16 teaspoon instant dry yeast (2.8 grams)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 30, "COMMENT"),  # "minus 1/16 teaspoon" (Kept)
            (31, 38, "PREP"),  # "instant" (from original PREP "instant dry" 31-42)
            (39, 42, "PREP"),  # "dry" (from original PREP "instant dry" 31-42)
            (43, 48, "NAME"),  # "yeast"
            (49, 60, "COMMENT")  # "(2.8 grams)" (Kept)
        ]
    }),

    # Example 41
    ("1 (8 1/2-ounce) can whole kernel corn", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 15, "COMMENT"),  # "(8 1/2-ounce)" (Kept)
            (16, 19, "UNIT"),  # "can"
            (20, 25, "PREP"),  # "whole" (Kept)
            (26, 32, "NAME"),  # "kernel" (from original NAME "kernel corn" 26-37)
            (33, 37, "NAME")  # "corn" (from original NAME "kernel corn" 26-37)
        ]
    }),

    # Example 42
    ("1 (2-ounce) jar diced pimentos", {
        # Original entities: (0,1,"COMMENT") "1", (3,4,"QTY") "2", (5,10,"UNIT") "ounce", (12,15,"COMMENT") "jar", (16,30,"NAME") "diced pimentos"
        "entities": [
            (0, 1, "COMMENT"),  # "1"
            (3, 4, "QTY"),  # "2"
            (5, 10, "UNIT"),  # "ounce"
            (12, 15, "COMMENT"),  # "jar"
            (16, 21, "NAME"),  # "diced" (from NAME 16-30)
            (22, 30, "NAME")  # "pimentos" (from NAME 16-30)
        ]
    }),

    # Example 43
    ("1 1/2-pound store-bought pizza or focaccia dough", {  # Corrected to match text end
        "entities": [
            (0, 5, "QTY"),
            (6, 11, "UNIT"),
            (12, 24, "PREP"),
            (25, 30, "NAME"),
            (31, 48, "ALT_NAME")  # "or focaccia dough" (ending at 47 for "dough")
        ]
    }),

    # Example 44
    ("3 small or 2 large ripe bananas, halved lengthwise", {
        "entities": [
            # Primary Item description
            (0, 1, "QTY"),         # "3"
            (2, 7, "UNIT"),        # "small"
            (8,10,'ALT_NAME'),
            (11, 12, "ALT_QTY"),   # "2" (alternative quantity for bananas)
            (13, 18, "ALT_UNIT"),  # "large" (alternative size unit for bananas)
            # State
            (19, 23, "PREP"),      # "ripe"
            # Core Item Name
            (24, 31, "NAME"),      # "bananas"
            # Comma at 31 is O
            # Preparation
            (33, 39, "PREP"),      # "halved"
            (40, 50, "PREP")       # "lengthwise" (or combine "halved lengthwise" into one PREP (33,50))
        ]
    }),

    # Example 45
    ("2 tablespoons brown sugar", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 19, "NAME"),  # "brown" (from original NAME "brown sugar" 14-25)
            (20, 25, "NAME")  # "sugar" (from original NAME "brown sugar" 14-25)
        ]
    }),

    # Example 46
    ("1 green bell pepper, julienne", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "NAME"),  # "green" (from original NAME "green bell pepper" 2-19)
            (8, 12, "NAME"),  # "bell" (from original NAME "green bell pepper" 2-19)
            (13, 19, "NAME"),  # "pepper" (from original NAME "green bell pepper" 2-19)
            # Comma at 19 is "O"
            (21, 29, "PREP")  # "julienne" (Kept)
        ]
    }),

    # Example 47
    ("1 red bell pepper, julienne", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "NAME"),  # "red" (from original NAME "red bell pepper" 2-17)
            (6, 10, "NAME"),  # "bell" (from original NAME "red bell pepper" 2-17)
            (11, 17, "NAME"),  # "pepper" (from original NAME "red bell pepper" 2-17)
            # Comma at 17 is "O"
            (19, 27, "PREP")  # "julienne" (Kept)
        ]
    }),

    # Example 48
    ("4 cedar planks", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 7, "NAME"),  # "cedar"
            (8, 14, "NAME")  # "planks"
        ]
    }),

    # Example 49
    ("2 carrots, peeled and julienne", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 9, "NAME"),  # "carrots"
            # Comma at 9 is "O"
            (11, 30, "PREP"),  # "peeled" (Kept from original (11,17,"PREP"))
        ]
    }),

    # Example 50
    ("5 pounds fresh skinless snapper fillet, cut into cubes", {
        "entities": [
            (0, 1, "QTY"),  # "5" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 14, "PREP"),  # "fresh" (from original PREP "fresh skinless" 9-23)
            (15, 23, "PREP"),  # "skinless" (from original PREP "fresh skinless" 9-23)
            (24, 31, "NAME"),  # "snapper"
            (32, 38, "NAME"),  # "fillet"
            # Comma at 38 is "O"
            (40, 54, "PREP")  # "cut into cubes" (Kept)
        ]
    }),

    # Example 51
    ("1 cup chopped and seeded tomatoes", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 24, "PREP"),  # "chopped" (from original PREP "chopped and seeded" 6-24)
            (25, 33, "NAME")  # "tomatoes"
        ]
    }),

    # Example 52
    ("2 1/2 cups half and half", {
        "entities": [
            (0, 5, "QTY"),  # "2 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 24, "NAME"),  # "half" (from original NAME "half and half" 11-24)
        ]
    }),

    # Example 53
    ("1 pound fresh squid tubes, cleaned and sliced into rings", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 13, "PREP"),  # "fresh" (Kept)
            (14, 19, "NAME"),  # "squid" (from original NAME "squid tubes" 14-25)
            (20, 25, "NAME"),  # "tubes" (from original NAME "squid tubes" 14-25)
            # Comma at 25 is "O"
            (27, 56, "PREP")  # "cleaned and sliced into rings" (Kept)
        ]
    }),

    # Example 54
    ("1 cup pitted and chopped plums", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "PREP"),  # "pitted" (from original PREP "pitted and chopped" 6-24)
            (13, 16, "PREP"),  # "and" (from original PREP "pitted and chopped" 6-24) - *Unusual*
            (17, 24, "PREP"),  # "chopped" (from original PREP "pitted and chopped" 6-24)
            (25, 30, "NAME")  # "plums"
        ]
    }),

    # Example 55
    ("3 peaches", {"entities": [
        (0, 1, "QTY"),  # "3" (Kept)
        (2, 9, "NAME")  # "peaches"
    ]}),

    # Example 56

    ("1 1/2-pound store-bought pizza or focaccia dough", {  # Corrected end for "dough"
        "entities": [
            (0, 5, "QTY"),
            (6, 11, "UNIT"),
            (12, 24, "PREP"),
            (25, 30, "NAME"),
            (31, 47, "ALT_NAME")
        ]
    }),

    # Example 57
    ("1/4 cup sunflower or canola oil", {  # If "or canola oil" was one ALT_NAME span
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 17, "NAME"),  # "sunflower"
            (18, 31, "ALT_NAME"),  # "or canola" (If ALT_NAME was only this)
            (32, 35, "NAME")  # "oil"
            # If "or canola oil" was (18,35, "ALT_NAME") -> (18,35,"ALT_NAME")
        ]
    }),

    # Example 58
    ("1 1/2 cups prepared pancake batter", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 19, "PREP"),  # "prepared" (Kept)
            (20, 27, "NAME"),  # "pancake" (from original NAME "pancake batter" 20-34)
            (28, 34, "NAME")  # "batter" (from original NAME "pancake batter" 20-34)
        ]
    }),

    # Example 59
    ("4 canned whole peeled tomatoes, roughly chopped", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "PREP"),  # "canned" (from original PREP "canned whole peeled" 2-21)
            (9, 14, "PREP"),  # "whole" (from original PREP "canned whole peeled" 2-21)
            (15, 21, "PREP"),  # "peeled" (from original PREP "canned whole peeled" 2-21)
            (22, 30, "NAME"),  # "tomatoes"
            # Comma at 30 is "O"
            (32, 47, "PREP"),  # "roughly" (from original PREP "roughly chopped" 32-47)
        ]
    }),

    # Example 60
    ("8 slices store-bought or homemade pound cake (3/4 inch thick)", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "PREP"),  # "slices" (Original (2,21,"PREP") "slices store-bought")
            (9, 21, "PREP"),  # "store-bought" (from original PREP (2,21))
            (22, 33, "ALT_NAME"),  # "or homemade" (Kept)
            (34, 39, "NAME"),  # "pound" (from original NAME "pound cake" 34-44)
            (40, 44, "NAME"),  # "cake" (from original NAME "pound cake" 34-44)
            (45, 61, "COMMENT")  # "(3/4 inch thick)" (Kept)
        ]
    }),

    # Example 61
    ("2 teaspoons smoked paprika", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 11, "UNIT"),  # "teaspoons"
            (12, 18, "NAME"),  # "smoked" (Kept)
            (19, 26, "NAME")  # "paprika"
        ]
    }),

    # Example 62
    ("2 tablespoons bottled hoisin sauce", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, "PREP"),  # "bottled" (Kept)
            (22, 28, "NAME"),  # "hoisin" (from original NAME "hoisin sauce" 22-34)
            (29, 34, "NAME")  # "sauce" (from original NAME "hoisin sauce" 22-34)
        ]
    }),

    # Example 63
    ("1/2 cup (4 ounces) shredded", {  # NAME is missing
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 18, "COMMENT"),  # "(4 ounces)" (Kept)
            (19, 27, "PREP")  # "shredded" (Kept)
            # No NAME entity
        ]
    }),

    # Example 64
    ("1/4 cup pepperoncini", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 20, "NAME")  # "pepperoncini"
        ]
    }),

    # Example 65
    ("Dash green hot sauce", {
        "entities": [
            (0, 4, "COMMENT"),  # "Dash" (from original NAME "Dash green hot sauce" 0-20)
            (5, 10, "NAME"),  # "green" (from original NAME 0-20)
            (11, 14, "NAME"),  # "hot" (from original NAME 0-20)
            (15, 20, "NAME")  # "sauce" (from original NAME 0-20)
        ]
    }),

    # Example 66
    ("12 roasted pearl onions", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 10, "PREP"),  # "roasted" (Kept)
            (11, 16, "NAME"),  # "pearl" (from original NAME "pearl onions" 11-23)
            (17, 23, "NAME")  # "onions" (from original NAME "pearl onions" 11-23)
        ]
    }),

    # Example 67
    ("72 round wonton skins (approximately 3-inches in diameter)", {
        "entities": [
            (0, 2, "QTY"),  # "72" (Kept)
            (3, 8, "PREP"),  # "round" (Kept)
            (9, 15, "NAME"),  # "wonton" (from original NAME "wonton skins" 9-21)
            (16, 21, "NAME"),  # "skins" (from original NAME "wonton skins" 9-21)
            (22, 58, "COMMENT")  # "(approximately 3-inches in diameter)" (Kept)
        ]
    }),

    # Example 68
    ("2 cups sliced red cabbage (about 1/3 head)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 13, "PREP"),  # "sliced" (Kept)
            (14, 17, "NAME"),  # "red" (from original NAME "red cabbage" 14-25)
            (18, 25, "NAME"),  # "cabbage" (from original NAME "red cabbage" 14-25)
            (26, 42, "COMMENT")  # "(about 1/3 head)" (Kept)
        ]
    }),

    # Example 69
    ("Four 6- to 8-ounce halved bone-in chicken breasts with skin", {
        "entities": [
            (0, 4, "QTY"),  # "Four" (Kept)
            (5, 18, "COMMENT"),  # "6- to 8-ounce" (Kept)
            (19, 25, "PREP"),  # "halved" (Kept)
            (26, 33, "NAME"),  # "bone-in" (from original NAME "bone-in chicken breasts" 26-49)
            (34, 41, "NAME"),  # "chicken" (from original NAME "bone-in chicken breasts" 26-49)
            (42, 49, "NAME"),  # "breasts" (from original NAME "bone-in chicken breasts" 26-49)
            (50, 59, "COMMENT")  # "with skin" (Kept)
        ]
    }),

    # Example 70
    ("1 1/2 pounds small baby red or tricolor creamer potatoes, quartered", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 18, "UNIT"),  # "small"
            (19, 23, "NAME"),  # "baby" (from original NAME "baby red" 19-27, if "red" is separate NAME/PREP)
            (24, 27, "NAME"),  # "red" (from original NAME "baby red" 19-27)
            (28, 47, "ALT_NAME"),  # "or tricolor creamer" (Kept)
            (48, 56, "NAME"),  # "potatoes"
            # Comma at 56 is "O"
            (58, 67, "PREP")  # "quartered" (Kept)
        ]
    }),

    # Example 71
    ("3 pounds assorted root vegetables, peeled (see Tip) and cut into 1/8-inch-thick slices", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 17, "PREP"),  # "assorted" (Kept)
            (18, 22, "NAME"),  # "root" (from original NAME "root vegetables" 18-33)
            (23, 33, "NAME"),  # "vegetables" (from original NAME "root vegetables" 18-33)
            # Comma at 33 is "O"
            (35, 86, "COMMENT"),  # "peeled" (Kept)
        ]
    }),

    # Example 72
    ("1 1/2 cups crushed graham crackers (about 10 crackers)", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 18, "PREP"),  # "crushed" (Kept)
            (19, 25, "NAME"),  # "graham" (from original NAME "graham crackers" 19-34)
            (26, 34, "NAME"),  # "crackers" (from original NAME "graham crackers" 19-34)
            (35, 54, "COMMENT")  # "(about 10 crackers)" (Kept)
        ]
    }),

    # Example 73
    ("3/4 pound hot or sweet Italian sausages, cut into chunks", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 22, "PREP"),  # "hot" (Kept)
            (23, 30, "NAME"),  # "Italian" (from original NAME "Italian sausages" 23-39)
            (31, 39, "NAME"),  # "sausages" (from original NAME "Italian sausages" 23-39)
            # Comma at 39 is "O"
            (41, 56, "PREP")  # "cut into chunks" (Kept)
        ]
    }),

    # Example 74
    ("4 small or 2 family-size tea bags (recommended: Lipton)", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 7, "UNIT"),  # "small"
            (8, 24, "ALT_NAME"),  # "or 2 family-size" (Kept)
            (25, 28, "NAME"),  # "tea" (from original NAME "tea bags" 25-33)
            (29, 33, "NAME"),  # "bags" (from original NAME "tea bags" 25-33)
            (34, 55, "COMMENT")  # "(recommended: Lipton)" (Kept)
        ]
    }),

    # Example 75
    ("1 cup crumbled queso fresco", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 14, "PREP"),  # "crumbled" (Kept)
            (15, 20, "NAME"),  # "queso" (from original NAME "queso fresco" 15-27)
            (21, 27, "NAME")  # "fresco" (from original NAME "queso fresco" 15-27)
        ]
    }),

    # Example 76
    ("1/4 cup sliced pickled pepperoncini, plus 2 teaspoons liquid from the jar", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "sliced" (from original PREP "sliced pickled" 8-22)
            (15, 22, "PREP"),  # "pickled" (from original PREP "sliced pickled" 8-22)
            (23, 35, "NAME"),  # "pepperoncini"
            # Comma at 35 is "O"
            (37, 73, "COMMENT")  # "plus 2 teaspoons liquid from the jar" (Kept)
        ]
    }),

    # Example 77
    ("2 striploin steaks (about 225 grams each)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 11, "NAME"),  # "striploin" (from original NAME "striploin steaks" 2-18)
            (12, 18, "NAME"),  # "steaks" (from original NAME "striploin steaks" 2-18)
            (19, 41, "COMMENT")  # "(about 225 grams each)" (Kept)
        ]
    }),

    # Example 78
    ("Four 8-ounce top-round steaks, pounded to about 1/4-inch thick", {
        "entities": [
            (0, 4, "QTY"),  # "Four" (Kept)
            (5, 12, "COMMENT"),  # "8-ounce" (Kept)
            (13, 22, "NAME"),  # "top-round" (from original NAME "top-round steaks" 13-29)
            (23, 29, "NAME"),  # "steaks" (from original NAME "top-round steaks" 13-29)
            # Comma at 29 is "O"
            (31, 62, "PREP")  # "pounded to about 1/4-inch thick" (Kept)
        ]
    }),

    # Example 79
    ("5 drops pink gel food coloring", {
        "entities": [
            (0, 1, "QTY"),  # "5" (Kept)
            (2, 7, "COMMENT"),  # "drops" (Original label was COMMENT)
            (8, 12, "NAME"),  # "pink" (from original NAME "pink gel food coloring" 8-30)
            (13, 16, "NAME"),  # "gel" (from original NAME "pink gel food coloring" 8-30)
            (17, 21, "NAME"),  # "food" (from original NAME "pink gel food coloring" 8-30)
            (22, 30, "NAME")  # "coloring" (from original NAME "pink gel food coloring" 8-30)
        ]
    }),

    # Example 80
    ("1/3 recipe sugar dough, recipe follows", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept)
            (4, 10, "COMMENT"),  # "recipe"
            (11, 16, "NAME"),  # "sugar" (from original NAME "sugar dough" 11-22)
            (17, 22, "NAME"),  # "dough" (from original NAME "sugar dough" 11-22)
            # Comma at 22 is "O"
            (24, 38, "COMMENT")  # "recipe follows" (Kept)
        ]
    }),

    # Example 81
    ("One 10.5-ounce pound cake, cut into 1/2-inch slices", {
        "entities": [
            (0, 3, "QTY"),  # "One" (Kept)
            (4, 14, "COMMENT"),  # "10.5-ounce" (Kept)
            (15, 25, "NAME"),  # "pound" (from original NAME "pound cake" 15-25)
            # Comma at 25 is "O"
            (27, 51, "PREP")  # "cut into 1/2-inch slices" (Kept)
        ]
    }),

    # Example 82
    ("4 sheets of yaki-nori, cut in half", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 11, "COMMENT"),  # "sheets"
            (12, 21, "NAME"),  # "yaki-nori"
            # Comma at 21 is "O"
            (23, 34, "PREP")  # "cut in half" (Kept)
        ]
    }),

    # Example 83
    ("1 banana, sliced", {"entities": [
        (0, 1, "QTY"),  # "1" (Kept)
        (2, 8, "NAME"),  # "banana"
        # Comma at 8 is "O"
        (10, 16, "PREP")  # "sliced" (Kept)
    ]}),

    # Example 84
    ("1 (28-ounce) can whole peeled tomatoes, hand-crushed", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "COMMENT"),  # "(28-ounce)" (Kept)
            (13, 16, "UNIT"),  # "can"
            (17, 22, "PREP"),  # "whole" (from original PREP "whole peeled" 17-29)
            (23, 29, "PREP"),  # "peeled" (from original PREP "whole peeled" 17-29)
            (30, 38, "NAME"),  # "tomatoes"
            # Comma at 38 is "O"
            (40, 52, "PREP")  # "hand-crushed" (Kept)
        ]
    }),

    # Example 85
    ("One 32-ounce can San Marzano tomatoes, blended", {
        "entities": [
            (0, 3, "QTY"),  # "One" (Kept)
            (4, 12, "COMMENT"),  # "32-ounce" (Kept)
            (13, 16, "UNIT"),  # "can"
            (17, 20, "NAME"),  # "San" (from original NAME "San Marzano tomatoes" 17-37)
            (21, 28, "NAME"),  # "Marzano" (from original NAME "San Marzano tomatoes" 17-37)
            (29, 37, "NAME"),  # "tomatoes" (from original NAME "San Marzano tomatoes" 17-37)
            # Comma at 37 is "O"
            (39, 46, "PREP")  # "blended" (Kept)
        ]
    }),

    # Example 86
    ("Aromatic sachet (parsley, rosemary, thyme, bay leaf and black peppercorn, tied in cheesecloth)", {
        "entities": [
            (0, 8, "NAME"),  # "Aromatic" (from original NAME "Aromatic sachet" 0-15)
            (9, 15, "NAME"),  # "sachet" (from original NAME "Aromatic sachet" 0-15)
            (16, 94, "COMMENT")
            # "(parsley, rosemary, thyme, bay leaf and black peppercorn, tied in cheesecloth)" (Kept)
        ]
    }),

    # Example 87
    ("1 tablespoon instant espresso or coffee powder", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 20, "NAME"),  # "instant" (from original NAME "instant espresso" 13-29)
            (21, 29, "NAME"),  # "espresso" (from original NAME "instant espresso" 13-29)
            (30, 46, "ALT_NAME")  # "or coffee powder" (Kept)
        ]
    }),

    # Example 88
    ("One 12-ounce container frozen whipped topping, such as Cool Whip, thawed", {
        "entities": [
            (0, 3, "QTY"),  # "One" (Kept)
            (4, 12, "COMMENT"),  # "12-ounce" (Kept)
            (13, 22, "UNIT"),  # "container"
            (23, 29, "PREP"),  # "frozen" (from original PREP "frozen whipped" 23-37)
            (30, 45, "NAME"),  # "topping"
            # Comma at 45 is "O"
            (47, 65, "COMMENT"),  # "such as Cool Whip," (Kept, includes comma)
            (66, 72, "PREP")  # "thawed" (Kept)
        ]
    }),

    # Example 89
    ("2 medium or 1 large onion, finely chopped", {
        "entities": [
            # Primary Item description
            (0, 1, "QTY"),         # "2"
            (2, 8, "UNIT"),        # "medium"
            (9,11,'ALT_NAME'),
            # Alternative description for the same item
            (12, 13, "ALT_QTY"),   # "1" (alternative quantity for onion)
            (14, 19, "ALT_UNIT"),  # "large" (alternative size unit for onion)
            # Core Item Name
            (20, 25, "NAME"),      # "onion"
            # Comma at 25 is O
            # Preparation
            (27, 41, "PREP")       # "finely chopped" (as one preparation phrase)
        ]
    }),

    # Example 90
    ("1/2 cup powdered or dry milk", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 16, "PREP"),  # "powdered" (Kept)
            (17, 23, "ALT_NAME"),  # "or dry" (Kept)
            (24, 28, "NAME")  # "milk"
        ]
    }),

    # Example 91
    ("2 teaspoons liquid whitener for icing", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 11, "UNIT"),  # "teaspoons"
            (12, 18, "NAME"),  # "liquid" (from original NAME "liquid whitener" 12-27)
            (19, 27, "NAME"),  # "whitener" (from original NAME "liquid whitener" 12-27)
            (28, 37, "COMMENT")  # "for icing" (Kept)
        ]
    }),

    # Example 92
    ("1 cup shredded romaine lettuce", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 14, "PREP"),  # "shredded" (Kept)
            (15, 22, "NAME"),  # "romaine" (from original NAME "romaine lettuce" 15-30)
            (23, 30, "NAME")  # "lettuce" (from original NAME "romaine lettuce" 15-30)
        ]
    }),

    # Example 93
    ("1 habanero, seeded, minced", {  # Assuming comma is O
        "entities": [
            (0, 1, "QTY"),
            (2, 10, "NAME"),
            (12, 18, "PREP"),  # "seeded"
            # Comma (18,19) O
            (20, 26, "PREP")  # "minced"
        ]
    }),

    # Example 94
    ("4 cups mixed greens, such as romaine, Boston, and green leaf lettuces, or mesclun", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 19, "NAME"),  # "greens"
            # Comma at 19 is "O"
            (21, 81, "COMMENT")  # "such as romaine, Boston, and green leaf lettuces, or mesclun" (Kept)
        ]
    }),

    # Example 95
    ("1 medium tomato", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "UNIT"),  # "medium"
            (9, 15, "NAME")  # "tomato"
        ]
    }),

    # Example 96
    ("1 tablespoon minced pickled", {  # Name is missing
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 19, "PREP"),  # "minced" (from original PREP "minced pickled" 13-27)
            (20, 27, "PREP")  # "pickled" (from original PREP "minced pickled" 13-27)
        ]
    }),

    # Example 97
    ("2 chicken breasts from a rotisserie chicken, skin removed, shredded", {  # Assuming comma is O
        "entities": [
            (0, 1, "QTY"),
            (2, 9, "NAME"), (10, 17, "NAME"),
            (18, 43, "COMMENT"),
            (45, 57, "PREP"),  # "skin removed"
            # Comma (57,58) O
            (59, 67, "PREP")  # "shredded"
        ]
    }),

    # Example 98
    ("1 1/4 cups shredded three-cheese Mexican blend", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/4" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 19, "PREP"),  # "shredded" (Kept)
            (20, 32, "NAME"),  # "three-cheese" (from original NAME "three-cheese Mexican blend" 20-46)
            (33, 40, "NAME"),  # "Mexican" (from original NAME "three-cheese Mexican blend" 20-46)
            (41, 46, "NAME")  # "blend" (from original NAME "three-cheese Mexican blend" 20-46)
        ]
    }),

    # Example 99
    ("1 rib celery, very thinly sliced on the bias", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "COMMENT"),  # "rib"
            (6, 12, "NAME"),  # "celery"
            # Comma at 12 is "O"
            (14, 44, "PREP"),  # "very thinly" (from original PREP "very thinly sliced on the bias" 14-44)
        ]
    }),

    # Example 100
    ("3 pounds day-old, cooked jasmine rice", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 16, "PREP"),  # "day-old," (Kept, includes comma, from original (9,24,"PREP") "day-old, cooked")
            (18, 24, "PREP"),  # "cooked" (from original PREP "day-old, cooked" 9-24)
            (25, 32, "NAME"),  # "jasmine" (from original NAME "jasmine rice" 25-37)
            (33, 37, "NAME")  # "rice" (from original NAME "jasmine rice" 25-37)
        ]
    }),

    # Example 101
    ("1 turnip, halved", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "NAME"),  # "turnip"
            # Comma at 8 is "O"
            (10, 16, "PREP")  # "halved" (Kept)
        ]
    }),

    # Example 102
    ("3 (3-pound) tri-tip steaks", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 11, "COMMENT"),  # "(3-pound)" (Kept)
            (12, 19, "NAME"),  # "tri-tip" (from original NAME "tri-tip steaks" 12-26)
            (20, 26, "NAME")  # "steaks" (from original NAME "tri-tip steaks" 12-26)
        ]
    }),

    # Example 103
    ("1 jalapeno", {"entities": [
        (0, 1, "QTY"),  # "1" (Kept)
        (2, 10, "NAME")  # "jalapeno"
    ]}),

    # Example 104
    ("1/4 cup hummus", {"entities": [
        (0, 3, "QTY"),  # "1/4" (Kept)
        (4, 7, "UNIT"),  # "cup"
        (8, 14, "NAME")  # "hummus"
    ]}),

    # Example 105
    ("1 pound dried farfalle", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 13, "PREP"),  # "dried" (Kept)
            (14, 22, "NAME")  # "farfalle"
        ]
    }),

    # Example 106
    ("8 ounces Colby-style cheese, such as Orb Weaver, coarsely grated (about 2 cups; or use aged, but not sharp, cheddar)",
     {
         "entities": [
             (0, 1, "QTY"),  # "8" (Kept)
             (2, 8, "UNIT"),  # "ounces"
             (9, 20, "NAME"),  # "Colby-style" (from original NAME "Colby-style cheese" 9-27)
             (21, 27, "NAME"),  # "cheese" (from original NAME "Colby-style cheese" 9-27)
             # Comma at 27 is "O"
             (29, 47, "COMMENT"),  # "such as Orb Weaver," (Kept, includes comma)
             (49, 64, "PREP"),  # "coarsely grated" (Kept)
             (65, 107, "COMMENT")  # "(about 2 cups; or use aged, but not sharp, cheddar)" (Kept)
         ]
     }),

    # Example 107
    ("1/2 cup crumbled Gorgonzola dolce or other mild blue cheese", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 16, "PREP"),  # "crumbled" (Kept)
            (17, 27, "NAME"),  # "Gorgonzola" (from original NAME "Gorgonzola dolce" 17-33)
            (28, 33, "NAME"),  # "dolce" (from original NAME "Gorgonzola dolce" 17-33)
            (34, 59, "ALT_NAME")  # "or other mild blue cheese" (Kept)
        ]
    }),

    # Example 108
    ("1 pound dried fusilli", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 13, "PREP"),  # "dried" (Kept)
            (14, 21, "NAME")  # "fusilli"
        ]
    }),

    # Example 109
    ("2 chickens", {"entities": [
        (0, 1, "QTY"),  # "2" (Kept)
        (2, 10, "NAME")  # "chickens"
    ]}),

    # Example 110
    ("2 cups mixed berry sparkling water, chilled (recommended: Arrowhead)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 18, "NAME"),  # "berry" (from original NAME "berry sparkling water" 13-34)
            (19, 34, "NAME"),  # "sparkling" (from original NAME "berry sparkling water" 13-34)
            # Comma at 34 is "O"
            (36, 43, "PREP"),  # "chilled" (Kept)
            (44, 68, "COMMENT")  # "(recommended: Arrowhead)" (Kept)
        ]
    }),

    # Example 111
    ("6 cups mixed greens, washed and dried", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 19, "NAME"),  # "greens"
            # Comma at 19 is "O"
            (21, 37, "PREP")  # "washed and dried" (Kept)
        ]
    }),

    # Example 112
    ("1 whole habanero, for garnish", {  # Using original text for habanero
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "PREP"),
            (8, 16, "NAME"),  # "habanero"
            (18, 29, "COMMENT")  # "for garnish"
        ]
    }),

    # Example 113
    ("2 loaves Irish brown bread", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "COMMENT"),  # "loaves"
            (9, 14, "NAME"),  # "Irish" (from original NAME "Irish brown bread" 9-26)
            (15, 20, "NAME"),  # "brown" (from original NAME "Irish brown bread" 9-26)
            (21, 26, "NAME")  # "bread" (from original NAME "Irish brown bread" 9-26)
        ]
    }),

    # Example 114
    ("1 medium-sized ripe tomato", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 14, "UNIT"),  # "medium-sized" (Original label was UNIT)
            (15, 19, "PREP"),  # "ripe" (Kept)
            (20, 26, "NAME")  # "tomato"
        ]
    }),

    # Example 115
    ("2 medium-sized onions", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 14, "UNIT"),  # "medium-sized" (Original label was UNIT)
            (15, 21, "NAME")  # "onions"
        ]
    }),

    # Example 116
    ("8 ounces taleggio or brie cheese, rind removed, cubed (about 1 1/2 cups)", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 17, "NAME"),  # "taleggio"
            (18, 25, "ALT_NAME"),  # "or brie cheese" (Kept)
            (26, 32, "NAME"),  # "or brie cheese" (Kept)
            # Comma at 32 is "O"
            (34, 53, "PREP"),  # "rind removed" (from original PREP "rind removed, cubed" 34-53, comma handling)
            (54, 72, "COMMENT")  # "(about 1 1/2 cups)" (Kept)
        ]
    }),

    # Example 117
    ("4 (6-ounce) mackerel fillets, with skin", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 11, "COMMENT"),  # "(6-ounce)" (Kept)
            (12, 28, "NAME"),  # "mackerel"
            # Comma at 28 is "O"
            (30, 39, "COMMENT")  # "with skin" (Kept)
        ]
    }),

    # Example 118
    ("1 cup sliced cepes, chanterelles or oyster mushrooms (optional)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "PREP"),  # "sliced" (Kept)
            (13, 18, "NAME"),  # "cepes"
            # Comma at 18 is "O"
            (20, 52, "ALT_NAME"),  # "chanterelles or oyster mushrooms" (Kept)
            (53, 63, "COMMENT")  # "(optional)" (Kept)
        ]
    }),

    # Example 119
    ("1 mountain yam (about 2 pounds)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 10, "NAME"),  # "mountain" (from original NAME "mountain yam" 2-14)
            (11, 14, "NAME"),  # "yam" (from original NAME "mountain yam" 2-14)
            (15, 31, "COMMENT")  # "(about 2 pounds)" (Kept)
        ]
    }),

    # Example 120
    ("1 medium tomato, halved and sliced 1/4 inch thick", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "UNIT"),  # "medium"
            (9, 15, "NAME"),  # "tomato"
            # Comma at 15 is "O"
            (17, 49, "PREP")  # "halved and sliced 1/4 inch thick" (Kept)
        ]
    }),

    # Example 121
    ("3 1/2 cups breadcrumbs (preferably panko)", {
        "entities": [
            (0, 5, "QTY"),  # "3 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 22, "NAME"),  # "breadcrumbs"
            (23, 41, "COMMENT")  # "(preferably panko)" (Kept)
        ]
    }),

    # Example 122

    ("6 small, ripe, but slightly firm peaches", {  # Assuming commas in PREP are O
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"),
            (9, 13, "PREP"),  # "ripe"
            # Comma at 13 O
            (15, 18, "PREP"),  # but
            (19, 27, "PREP"),  # slightly
            (28, 32, "PREP"),  # firm
            (33, 40, "NAME")
        ]
    }),

    # Example 123
    ("2 cups tomato-basil sauce, such as Giada De Laurentiis for Target Sauce", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 19, "NAME"),  # "tomato-basil" (from original NAME "tomato-basil sauce" 7-25)
            (20, 25, "NAME"),  # "sauce" (from original NAME "tomato-basil sauce" 7-25)
            # Comma at 25 is "O"
            (27, 71, "COMMENT")  # "such as Giada De Laurentiis for Target Sauce" (Kept)
        ]
    }),

    # Example 124
    ("1/4 teaspoon chile de arbol", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 18, "NAME"),  # "chile" (from original NAME "chile de arbol" 13-27)
            (19, 21, "NAME"),  # "de" (from original NAME "chile de arbol" 13-27) - *Unusual*
            (22, 27, "NAME")  # "arbol" (from original NAME "chile de arbol" 13-27)
        ]
    }),

    # Example 125
    ("4 ounces marzipan", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 17, "NAME")  # "marzipan"
        ]
    }),

    # Example 126
    ("12 leaves Little Gem lettuce", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 9, "COMMENT"),  # "leaves"
            (10, 16, "NAME"),  # "Little" (from original NAME "Little Gem lettuce" 10-28)
            (17, 20, "NAME"),  # "Gem" (from original NAME "Little Gem lettuce" 10-28)
            (21, 28, "NAME")  # "lettuce" (from original NAME "Little Gem lettuce" 10-28)
        ]
    }),

    # Example 127
    ("48 pepperoni slices", {
        "entities": [
            (0, 2, "QTY"),  # "48" (Kept)
            (3, 12, "NAME"),  # "pepperoni" (from original NAME "pepperoni slices" 3-19)
            (13, 19, "NAME")  # "slices" (from original NAME "pepperoni slices" 3-19)
        ]
    }),

    # Example 128
    ("18 slices mozzarella", {
        "entities": [
            (0, 2, "QTY"),  # "18" (Kept)
            (3, 9, "PREP"),  # "slices" (Original label was PREP)
            (10, 20, "NAME")  # "mozzarella"
        ]
    }),

    # Example 129
    ("1/2 cup diced tomato", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "NAME"),  # "diced" (from original NAME "diced tomato" 8-20)
            (14, 20, "NAME")  # "tomato" (from original NAME "diced tomato" 8-20)
        ]
    }),

    # Example 130
    ("2 cups diced tomato", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 12, "NAME"),  # "diced" (from original NAME "diced tomato" 7-19)
            (13, 19, "NAME")  # "tomato" (from original NAME "diced tomato" 7-19)
        ]
    }),

    # Example 131
    ("1/3 cup diced, peeled Fuji apple", {  # Assuming comma O
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (8, 13, "PREP"),  # "diced"
            # Comma (13,14) O
            (15, 21, "PREP"),  # "peeled"
            (22, 26, "NAME"), (27, 32, "NAME")  # Fuji apple
        ]
    }),

    # Example 132
    ("1 medium, skinny zucchini, cut into thin slices", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "UNIT"),  # "medium"
            # Comma at 8 is "O"
            (10, 16, "PREP"),  # "skinny" (Kept)
            (17, 25, "NAME"),  # "zucchini"
            # Comma at 25 is "O"
            (27, 47, "PREP")  # "cut into thin slices" (Kept)
        ]
    }),

    # Example 133
    ("20 to 25 sand dab (flounder) fillets", {
        "entities": [
            (0, 8, "QTY"),  # "20 to 25" (Kept)
            (9, 13, "NAME"),  # "sand" (from original NAME "sand dab" 9-17)
            (14, 17, "NAME"),  # "dab" (from original NAME "sand dab" 9-17)
            (18, 28, "COMMENT"),  # "(flounder)" (Kept)
            (29, 36, "NAME")  # "fillets"
        ]
    }),

    # Example 134
    ("Tomato slices", {
        "entities": [
            (0, 6, "NAME"),  # "Tomato"
            (7, 13, "PREP")  # "slices" (Original label was PREP)
        ]
    }),

    # Example 135
    ("Toasted hamburger buns, English muffins or egg bread", {
        "entities": [
            (0, 7, "PREP"),  # "Toasted" (Kept)
            (8, 17, "NAME"),  # "hamburger" (from original NAME "hamburger buns" 8-22)
            (18, 22, "NAME"),  # "buns" (from original NAME "hamburger buns" 8-22)
            # Comma at 22 is "O"
            (24, 52, "ALT_NAME")  # "English muffins or egg bread" (Kept)
        ]
    }),

    # Example 136
    ("2 soft-shell crawfish", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 12, "PREP"),  # "soft-shell" (Kept)
            (13, 21, "NAME")  # "crawfish"
        ]
    }),

    # Example 137
    ("3 cups of day old French bread, cubed", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 9, "PREP"),  # "of" (Kept from original (7,17,"PREP") "of day old")
            (10, 13, "PREP"),  # "day" (from original PREP "of day old" 7-17)
            (14, 17, "PREP"),  # "old" (from original PREP "of day old" 7-17)
            (18, 24, "NAME"),  # "French" (from original NAME "French bread" 18-30)
            (25, 30, "NAME"),  # "bread" (from original NAME "French bread" 18-30)
            # Comma at 30 is "O"
            (32, 37, "PREP")  # "cubed" (Kept)
        ]
    }),

    # Example 138
    ("1/2 large, juicy lemon, peel and pith removed", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "large"
            # Comma at 9 is "O"
            (11, 16, "PREP"),  # "juicy" (Kept)
            (17, 22, "NAME"),  # "lemon"
            # Comma at 22 is "O"
            (24, 45, "PREP")  # "peel and pith removed" (Kept)
        ]
    }),

    # Example 139
    ("2 ounces pepper-infused vodka", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 23, "NAME"),  # "pepper-infused" (Kept)
            (24, 29, "NAME")  # "vodka"
        ]
    }),

    # Example 140
    ("1/2 cup shredded Asiago, mozzarella, and Parmesan", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 16, "PREP"),  # "shredded" (Kept)
            (17, 23, "NAME"),  # "Asiago"
            # Comma at 23 is "O"
            (25, 49, "ALT_NAME")  # "mozzarella, and Parmesan" (Kept, includes comma and "and")
        ]
    }),

    # Example 141
    ("1 tablespoon (15 grams) prepared dashi", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 23, "COMMENT"),  # "(15 grams)" (Kept)
            (24, 32, "PREP"),  # "prepared" (Kept)
            (33, 38, "NAME")  # "dashi"
        ]
    }),

    # Example 142
    ("4 rib-eye steaks, approximately 1 1/2 to 2 pounds total", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 9, "NAME"),  # "rib-eye" (from original NAME "rib-eye steaks" 2-16)
            (10, 16, "NAME"),  # "steaks" (from original NAME "rib-eye steaks" 2-16)
            # Comma at 16 is "O"
            (18, 55, "COMMENT")  # "approximately 1 1/2 to 2 pounds total" (Kept)
        ]
    }),

    # Example 143
    ("1/2 teaspoon TripleSec", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 22, "NAME")  # "TripleSec"
        ]
    }),

    # Example 144
    ("1 strip (1/4 x 3/4inch) of serrano chile", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "COMMENT"),  # "strip"
            (8, 23, "COMMENT"),  # "(1/4 x 3/4inch)" (Kept)
            (24, 26, "PREP"),  # "of" (Kept)
            (27, 34, "NAME"),  # "serrano" (from original NAME "serrano chile" 27-40)
            (35, 40, "NAME")  # "chile" (from original NAME "serrano chile" 27-40)
        ]
    }),

    # Example 145
    ("1 large yam", {"entities": [
        (0, 1, "QTY"),  # "1" (Kept)
        (2, 7, "UNIT"),  # "large"
        (8, 11, "NAME")  # "yam"
    ]}),

    # Example 146
    ("1 medium firm tomato sliced 1/16 inch thick", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "UNIT"),  # "medium"
            (9, 13, "PREP"),  # "firm" (Kept)
            (14, 20, "NAME"),  # "tomato"
            (21, 43, "PREP")  # "sliced 1/16 inch thick" (Kept)
        ]
    }),

    # Example 147
    ("3/4 cup brewed strong coffee, cooled", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "NAME"),  # "brewed" (from original PREP "brewed strong" 8-21)
            (15, 21, "PREP"),  # "strong" (from original PREP "brewed strong" 8-21)
            (22, 28, "NAME"),  # "coffee"
            # Comma at 28 is "O"
            (30, 36, "PREP")  # "cooled" (Kept)
        ]
    }),

    # Example 148
    ("6 large, fresh basil leaves, torn", {  # Assuming fresh is PREP, basil leaves is NAME
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"),
            (9, 14, "PREP"),  # "fresh"
            (15, 20, "NAME"),  # "basil"
            (21, 27, "NAME"),  # "leaves"
            (29, 33, "PREP")  # "torn"
        ]
    }),

    # Example 149
    ("1 part Sriracha and 3 parts mayonnaise (or Sriracha mayo), for serving", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 6, "COMMENT"),  # "part"
            (7, 15, "NAME"),  # "Sriracha"
            (20, 38, "ALT_NAME"),  # "3 parts mayonnaise" (Kept)
            (39, 70, "COMMENT")  # "(or Sriracha mayo), for serving" (Kept, original had comma inside)
        ]
    }),

    # Example 150
    ("2 cups cooked brown or white rice", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 13, "PREP"),  # "cooked" (Kept)
            (14, 19, "NAME"),  # "brown"
            (20, 28, "ALT_NAME"),  # "or white" (Kept)
            (29, 33, "NAME")  # "rice"
        ]
    }),

    # Example 151
    ("1/2 to 1 pound pasta of your choice, cooked", {
        "entities": [
            (0, 3, "QTY"),  # "1/2 to 1" (Kept)
            (4, 8, "COMMENT"),  # "1/2 to 1" (Kept)
            (9, 14, "UNIT"),  # "pound"
            (15, 20, "NAME"),  # "pasta"
            (21, 36, "COMMENT"),  # "of your choice," (Kept, includes comma)
            (37, 43, "PREP")  # "cooked" (Kept)
        ]
    }),

    # Example 152

    ("8 cups 1-inch baguette cubes, stale or toasted (about 8 1/2 ounces)", {  # Corrected for "baguette cubes"
        "entities": [
            (0, 1, "QTY"), (2, 6, "UNIT"), (7, 13, "PREP"),
            (14, 22, "NAME"),  # "baguette"
            (23, 28, "NAME"),  # "cubes"
            (30, 67, "COMMENT"),
        ]
    }),

    # Example 153
    ("1/2 cup finely crumbled blue cheese", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "finely" (from original PREP "finely crumbled" 8-23)
            (15, 23, "PREP"),  # "crumbled" (from original PREP "finely crumbled" 8-23)
            (24, 28, "NAME"),  # "blue" (from original NAME "blue cheese" 24-35)
            (29, 35, "NAME")  # "cheese" (from original NAME "blue cheese" 24-35)
        ]
    }),

    # Example 154
    ("2 cups 1-percent milk", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 21, "NAME"),  # "1-percent" (Kept)
        ]
    }),

    # Example 155
    ("8 to 12 ounces lox", {
        "entities": [
            (0, 1, "QTY"),  # "8 to 12" (Kept)
            (2, 7, "QTY"),  # "8 to 12" (Kept)
            (8, 14, "UNIT"),  # "ounces"
            (15, 18, "NAME")  # "lox"
        ]
    }),

    # Example 156
    ("1 English cucumber", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 9, "NAME"),  # "English" (from original NAME "English cucumber" 2-18)
            (10, 18, "NAME")  # "cucumber" (from original NAME "English cucumber" 2-18)
        ]
    }),

    # Example 157
    ("2 tablespoons everything bagel spice", {  # If original (14,30) was for "everything bagel spice"
        "entities": [
            (0, 1, "QTY"), (2, 13, "UNIT"),
            (14, 24, "COMMENT"),  # everything
            (25, 30, "NAME"),  # bagel
            (31, 36, "NAME")  # spice
        ]
    }),

    # Example 158
    ("2 teaspoon MSG", {"entities": [
        (0, 1, "QTY"),
        (2, 10, "UNIT"),      # Fixed: 'teaspoon' (char 2 to 10)
        (11, 14, "NAME")       # Fixed: 'MSG' (char 11 to 14)
    ]}),

    # Example 159
    ("Celery sticks and/or baguette slices", {
        "entities": [
            (0, 6, "NAME"),  # "Celery"
            (7, 13, "PREP"),  # "sticks" (Original label was PREP)
            (14, 36, "ALT_NAME")  # "and/or baguette slices" (Kept)
        ]
    }),

    # Example 160
    ("2 ounces rum, such as Smith and Cross", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 12, "NAME"),  # "rum"
            # Comma at 12 is "O"
            (14, 37, "COMMENT")  # "such as Smith and Cross" (Kept)
        ]
    }),

    # Example 161
    ("2 ounces half-and-half", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 22, "NAME")  # "half-and-half" (tokenized as one)
        ]
    }),

    # Example 162
    ("4 pears, peeled and chopped into roughly 1-inch pieces", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 7, "NAME"),  # "pears"
            # Comma at 7 is "O"
            (9, 54, "PREP")  # "peeled and chopped into roughly 1-inch pieces" (Kept)
        ]
    }),

    # Example 163
    ("1 3/4 cup cajeta or caramel", {
        "entities": [
            (0, 5, "QTY"),  # "1 3/4" (Kept)
            (6, 9, "UNIT"),  # "cup"
            (10, 16, "NAME"),  # "cajeta"
            (17, 27, "ALT_NAME")  # "or caramel" (Kept)
        ]
    }),

    # Example 164
    ("1 envelope unflavored gelatin, or one-quarter of a 1-ounce package", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 10, "COMMENT"),  # "envelope"
            (11, 21, "PREP"),  # "unflavored" (Kept)
            (22, 29, "NAME"),  # "gelatin"
            # Comma at 29 is "O"
            (31, 66, "COMMENT")  # "or one-quarter of a 1-ounce package" (Kept as original COMMENT, not ALT_NAME)
        ]
    }),

    # Example 165
    ("12 natural licorice sticks, cinnamon sticks, or bamboo skewers, each 6-inches long", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 10, "PREP"),  # "natural" (Kept)
            (11, 19, "NAME"),  # "licorice"
            (20, 26, "NAME"),  # "sticks"
            # Comma at 26 is "O"
            (28, 62, "ALT_NAME"),  # "cinnamon sticks, or bamboo skewers" (Kept)
            # Comma at 62 is "O"
            (64, 82, "COMMENT")  # "each 6-inches long" (Kept)
        ]
    }),

    # Example 166
    ("Approximately 40 store-bought caramels", {
        "entities": [
            (0, 13, "COMMENT"),  # "Approximately" (Kept)
            (14, 16, "QTY"),  # "40" (Kept)
            (17, 29, "PREP"),  # "store-bought" (Kept)
            (30, 38, "NAME")  # "caramels"
        ]
    }),

    # Example 167
    ("2 cups 2-percent or whole milk", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 16, "NAME"),  # "2-percent" (Kept)
            (17, 25, "ALT_NAME"),  # "or whole" (Kept)
            (26, 30, "NAME")  # "milk"
        ]
    }),

    # Example 168
    ("4 tablespoons chopped toasted walnuts, optional", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, "PREP"),  # "chopped" (from original PREP "chopped toasted" 14-29)
            (22, 37, "NAME"),  # "toasted" (from original PREP "chopped toasted" 14-29)
            # Comma at 37 is "O"
            (39, 47, "COMMENT")  # "optional" (Kept)
        ]
    }),

    # Example 169
    ("6 radishes, quartered", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 10, "NAME"),  # "radishes"
            # Comma at 10 is "O"
            (12, 21, "PREP")  # "quartered" (Kept)
        ]
    }),

    # Example 170
    ("STEVIA EXTRACT IN THE RAW® CUP FOR CUP", {
        "entities": [
            (0, 38, "NAME"),  # "STEVIA" (from original NAME "STEVIA EXTRACT IN THE RAW® CUP FOR CUP" 0-38)
        ]
    }),

    # Example 171
    ("1/3 cup chocolate-hazelnut spread", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 26, "NAME"),  # "chocolate-hazelnut" (from original NAME "chocolate-hazelnut spread" 8-33)
            (27, 33, "NAME")  # "spread" (from original NAME "chocolate-hazelnut spread" 8-33)
        ]
    }),

    # Example 173
    ("1/2 cup firmly packed light brown sugar", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "firmly" (from original PREP "firmly packed light brown" 8-27)
            (15, 21, "PREP"),  # "packed" (from original PREP 8-27)
            (22, 27, "PREP"),  # "light" (from original PREP 8-27) - Your original implied "brown" was part of PREP too.
            # If (8,27,"PREP") was for "firmly packed light brown", then "brown" is PREP
            (28, 33, "NAME"),  # "brown" (from original NAME "brown sugar" 28-39)
            (34, 39, "NAME")  # "sugar" (from original NAME "brown sugar" 28-39)
        ]
    }),

    # Example 174
    ("8 ounces processed cheese such as Velveeta, cut into 1/2-inch pieces", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 18, "PREP"),  # "processed" (Kept)
            (19, 25, "NAME"),  # "cheese"
            (26, 43, "COMMENT"),  # "such as Velveeta," (Kept, includes comma)
            (44, 68, "PREP")  # "cut into 1/2-inch pieces" (Kept)
        ]
    }),

    # Example 175
    ("2 tablespoons oil of your choice", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 17, "NAME"),  # "oil"
            (18, 32, "COMMENT")  # "of your choice" (Kept)
        ]
    }),

    # Example 176
    ("1 tablespoon Thai yellow or red curry paste, or 1 tablespoon Madras curry powder", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 17, "NAME"),  # "Thai" (from original NAME "Thai yellow" 13-24)
            (18, 24, "NAME"),  # "yellow" (from original NAME "Thai yellow" 13-24)
            (25, 37, "ALT_NAME"),  # "or red curry" (Kept)
            (38, 43, "NAME"),  # "paste"
            # Comma at 43 is "O"
            (45, 80, "ALT_NAME")  # "or 1 tablespoon Madras curry powder" (Kept)
        ]
    }),

    # Example 177 (Duplicate)
    ("5 radishes", {"entities": [(0, 1, "QTY"), (2, 10, "NAME")]}),

    # Example 178 (Duplicate)
    ("Whipped cream, for garnish", {"entities": [(0, 13, "NAME"), (15, 26, "COMMENT")]}),

    # Example 179
    ("One 26.5-ounce jar chocolate-hazelnut spread", {
        "entities": [
            (0, 3, "COMMENT"),  # "One" (Kept)
            (4, 8, "QTY"),  # "26.5-ounce" (from original COMMENT (4,18) - span for text "26.5-ounce jar")
            (9, 14, "UNIT"),  # "26.5-ounce" (from original COMMENT (4,18) - span for text "26.5-ounce jar")
            # This means "jar" was part of comment. If not, (4,14) COMMENT, (15,18) UNIT
            (15, 18, "COMMENT"),  # "jar" (from original COMMENT (4,18))
            (19, 37, "NAME"),  # "chocolate-hazelnut" (from original NAME "chocolate-hazelnut spread" 19-44)
            (38, 44, "NAME")  # "spread" (from original NAME "chocolate-hazelnut spread" 19-44)
        ]
    }),

    # Example 180
    ("1 loaf ciabatta", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 6, "COMMENT"),  # "loaf"
            (7, 15, "NAME")  # "ciabatta"
        ]
    }),

    # Example 181
    ("2 pounds, 4 ounces/ 1 kg ling fillets", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            # Comma at 8 is "O"
            (10, 24, "COMMENT"),  # "4 ounces/ 1 kg" (Kept, your original span was 10-24)
            (25, 37, "NAME"),  # "ling"
        ]
    }),

    # Example 182
    ("1/2 cup thinly sliced radishes", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 21, "PREP"),  # "thinly" (from original PREP "thinly sliced" 8-21)
            (22, 30, "NAME")  # "radishes"
        ]
    }),

    # Example 183
    ("Two 3-inch-long cinnamon sticks", {
        "entities": [
            (0, 3, "QTY"),  # "Two" (Kept)
            (4, 15, "COMMENT"),  # "3-inch-long" (Original label was UNIT)
            (16, 24, "NAME"),  # "cinnamon" (from original NAME "cinnamon sticks" 16-31)
            (25, 31, "NAME")  # "sticks" (from original NAME "cinnamon sticks" 16-31)
        ]
    }),

    # Example 184
    ("3 sticks, plus 1 tablespoon unsalted butter", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 8, "COMMENT"),  # "sticks"
            # Comma at 8 is "O"
            (10, 27, "COMMENT"),  # "plus 1 tablespoon" (Kept)
            (28, 36, "NAME"),  # "unsalted" (from original NAME "unsalted butter" 28-43)
            (37, 43, "NAME")  # "butter" (from original NAME "unsalted butter" 28-43)
        ]
    }),

    # Example 185
    ("2 large mangos, peeled, pitted and cut into 1-inch pieces", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 7, "UNIT"),  # "large"
            (8, 14, "NAME"),  # "mangos"
            # Comma at 14 is "O"
            (16, 57, "PREP")  # "peeled, pitted and cut into 1-inch pieces" (Kept)
        ]
    }),

    # Example 186
    ("1 pound (21-25 count) peeled and deveined prawns", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 21, "COMMENT"),  # "(21-25 count)" (Kept)
            (22, 41, "PREP"),  # "peeled" (from original PREP "peeled and deveined" 22-41)
            (42, 48, "NAME")  # "prawns"
        ]
    }),

    # Example 187
    ("1 1/2 cups (500 grams) assorted preserves or chocolate spreads (see Cook's Note)", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 22, "COMMENT"),  # "(500 grams)" (Kept)
            (23, 31, "PREP"),  # "assorted" (Kept)
            (32, 41, "NAME"),  # "preserves"
            (42, 62, "ALT_NAME"),  # "or chocolate spreads" (Kept)
            (63, 80, "COMMENT")  # "(see Cook's Note)" (Kept)
        ]
    }),

    # Example 188
    ("5 large cans tomato paste", {
        "entities": [
            (0, 1, "QTY"),  # "5" (Kept)
            (2, 7, "UNIT"),  # "large"
            (8, 12, "UNIT"),  # "cans"
            (13, 19, "NAME"),  # "tomato" (from original NAME "tomato paste" 13-25)
            (20, 25, "NAME")  # "paste" (from original NAME "tomato paste" 13-25)
        ]
    }),

    # Example 189
    ("2 1/2 cups chocolate-coated toffee pieces", {
        "entities": [
            (0, 5, "QTY"),  # "2 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 27, "PREP"),  # "chocolate-coated" (Kept)
            (28, 34, "NAME"),  # "toffee"
            (35, 41, "PREP")  # "pieces" (Original label was PREP)
        ]
    }),

    # Example 190
    ("8 large pieces oxtail (about 3 pounds total)", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 7, "UNIT"),  # "large"
            (8, 14, "COMMENT"),  # "pieces" (Original label was COMMENT)
            (15, 21, "NAME"),  # "oxtail"
            (22, 43, "COMMENT")  # "(about 3 pounds total)" (Kept)
        ]
    }),

    # Example 191
    ("Fig preserves", {"entities": [
        (0, 3, "NAME"),  # "Fig" (from original NAME "Fig preserves" 0-13)
        (4, 13, "NAME")  # "preserves" (from original NAME "Fig preserves" 0-13)
    ]}),

    # Example 192
    ("4 steaks (1-1 1/2 inches thick)", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "NAME"),  # "steaks"
            (9, 31, "COMMENT")  # "(1-1 1/2 inches thick)" (Kept)
        ]
    }),

    # Example 193
    ("Pan juices from steak", {
        "entities": [
            (0, 21, "COMMENT"),  # "Pan" (from original NAME "Pan juices" 0-10)
        ]
    }),

    # Example 194
    ("1 medium bay leaf", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "UNIT"),  # "medium"
            (9, 12, "NAME"),  # "bay" (from original NAME "bay leaf" 9-17)
            (13, 17, "NAME")  # "leaf" (from original NAME "bay leaf" 9-17)
        ]
    }),

    # Example 195
    ("1 (12 ounce) bottle beer (preferably a lager)", {  # If original (2,19,"COMMENT") was for "(12 ounce) bottle"
        "entities": [
            (0, 1, "QTY"),
            (2, 19, "COMMENT"),  # "(12 ounce) bottle"
            (20, 24, "NAME"),
            (25, 45, "COMMENT")
        ]
    }),

    # Example 196
    ("1 beer", {'entities': [
        (0, 1, 'QTY'),  # "1" (Kept)
        (2, 6, 'NAME')  # "beer"
    ]}),

    # Example 197
    ("1 Thai chili", {"entities": [
        (0, 1, "QTY"),  # "1" (Kept)
        (2, 6, "NAME"),  # "Thai" (from original NAME "Thai chili" 2-12)
        (7, 12, "NAME")  # "chili" (from original NAME "Thai chili" 2-12)
    ]}),

    # Example 198
    ("1/4 pound block semisweet or dark chocolate, to shave with a vegetable peeler", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 15, "COMMENT"),  # "block" (Kept)
            (16, 25, "NAME"),  # "semisweet"
            (26, 33, "ALT_NAME"),  # "or dark chocolate" (Kept)
            (34, 43, "NAME"),  # " chocolate" (Kept)
            # Comma at 43 is "O"
            (45, 77, "COMMENT")  # "to shave with a vegetable peeler" (Kept, your original had (43,77) including comma)
        ]
    }),

    # Example 199
    ("4 squab, rib cage removed", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 7, "NAME"),  # "squab"
            # Comma at 7 is "O"
            (9, 25, "PREP")  # "rib cage removed" (Kept)
        ]
    }),

    # Example 200
    ("8 no-calorie sweetener packets", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 12, "PREP"),  # "no-calorie" (Kept)
            (13, 22, "NAME"),  # "sweetener"
            (23, 30, "UNIT")  # "packets" (Original label was COMMENT)
        ]
    }),

    # Example 201
    ("1 pound broccolini, trimmed into florets", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 18, "NAME"),  # "broccolini"
            # Comma at 18 is "O"
            (20, 40, "PREP")  # "trimmed into florets" (Kept)
        ]
    }),

    # Example 202
    ("2 tablespoons golden or dark raisins", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 20, "NAME"),  # "golden"
            (21, 28, "ALT_NAME"),  # "or dark" (Kept)
            (29, 36, "NAME")  # "raisins"
        ]
    }),

    # Example 203
    ("4 (1 to 1 1/2-inch thick) bone-in pork chops", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 25, "COMMENT"),  # "(1 to 1 1/2-inch thick)" (Kept)
            (26, 33, "NAME"),  # "bone-in" (Kept)
            (34, 38, "NAME"),  # "pork" (from original NAME "pork chops" 34-44)
            (39, 44, "NAME")  # "chops" (from original NAME "pork chops" 34-44)
        ]
    }),

    # Example 204
    ("One 4-ounce/110 g tenderloin fillet", {
        "entities": [
            (0, 3, "QTY"),  # "One" (Kept)
            (4, 17, "COMMENT"),  # "4-ounce/110 g" (Kept)
            (18, 28, "NAME"),  # "tenderloin" (from original NAME "tenderloin fillet" 18-35)
            (29, 35, "NAME")  # "fillet" (from original NAME "tenderloin fillet" 18-35)
        ]
    }),

    # Example 205
    ("1 teaspoon quatre-epices, more to taste, or smoked paprika", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 24, "NAME"),  # "quatre-epices"
            # Comma at 24 is "O"
            (26, 40, "COMMENT"),  # "more to taste," (Kept, includes comma)
            (41, 58, "ALT_NAME")  # "or smoked paprika" (Kept)
        ]
    }),

    # Example 206
    ("1 cup sliced, Sauteed shiitakes", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "PREP"),  # "sliced" (Kept from original (6,12,"PREP"))
            # Comma at 12 is "O"
            (14, 21, "PREP"),  # "Sauteed" (Original label was PREP, kept. Note capitalization)
            (22, 31, "NAME")  # "shiitakes"
        ]
    }),

    # Example 207
    ("1 baguette", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 10, "NAME")  # "baguette"
        ]
    }),

    # Example 208
    ("Salami, sliced diagonally", {
        "entities": [
            (0, 6, "NAME"),  # "Salami"
            # Comma at 6 is "O"
            (8, 14, "PREP"),  # "sliced" (from original PREP "sliced diagonally" 8-25)
            (15, 25, "PREP")  # "diagonally" (from original PREP "sliced diagonally" 8-25)
        ]
    }),

    # Example 209
    ("3/4 cup apricot jam", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "NAME"),  # "apricot" (from original NAME "apricot jam" 8-19)
            (16, 19, "NAME")  # "jam" (from original NAME "apricot jam" 8-19)
        ]
    }),

    # Example 210
    ("Use 4 cups packed leaves to 2 cups pure olive oil", {
        "entities": [
            (0, 49, "COMMENT")  # Kept as original COMMENT span
        ]
    }),

    # Example 211
    ("1/4 cup pickled jalapeños (mild preferred)", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "PREP"),  # "pickled" (Kept)
            (16, 25, "NAME"),  # "jalapeños"
            (26, 42, "COMMENT")  # "(mild preferred)" (Kept)
        ]
    }),

    # Example 212
    ("12 thin slices provolone", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 14, "PREP"),  # "thin" (from original PREP "thin slices" 3-14)
            (15, 24, "NAME")  # "provolone"
        ]
    }),

    # Example 213
    ("1 1/2 cup diced dried apricot", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 9, "UNIT"),  # "cup"
            (10, 15, "PREP"),  # "diced" (from original NAME "diced dried apricot" 10-29)
            (16, 21, "NAME"),  # "dried" (from original NAME "diced dried apricot" 10-29)
            (22, 29, "NAME")  # "apricot" (from original NAME "diced dried apricot" 10-29)
        ]
    }),

    # Example 214
    ("2 dried bay leaves", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 7, "PREP"),  # "dried" (Kept)
            (8, 11, "NAME"),  # "bay" (from original NAME "bay leaves" 8-18)
            (12, 18, "NAME")  # "leaves" (from original NAME "bay leaves" 8-18)
        ]
    }),

    # Example 215
    ("8 ounces farmer's cheese, crumbled", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 17, "NAME"),  # "farmer's" (from original NAME "farmer's cheese" 9-24)
            (18, 24, "NAME"),  # "cheese" (from original NAME "farmer's cheese" 9-24)
            # Comma at 24 is "O"
            (26, 34, "PREP")  # "crumbled" (Kept)
        ]
    }),

    # Example 216
    ("7 ounces mam ca loc (fermented mud fish)", {
        "entities": [
            (0, 1, "QTY"),  # "7" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 12, "NAME"),  # "mam" (from original NAME "mam ca loc" 9-19)
            (13, 15, "NAME"),  # "ca" (from original NAME "mam ca loc" 9-19)
            (16, 19, "NAME"),  # "loc" (from original NAME "mam ca loc" 9-19)
            (20, 40, "COMMENT")  # "(fermented mud fish)" (Kept)
        ]
    }),

    # Example 217
    ("1/2 cup strawberries, sliced", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 20, "NAME"),  # "strawberries"
            # Comma at 20 is "O"
            (22, 28, "PREP")  # "sliced" (Kept)
        ]
    }),

    # Example 218
    ("1 teaspoon hot relish (recommended: Amish or Indian)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 14, "PREP"),  # "hot" (Kept)
            (15, 21, "NAME"),  # "relish"
            (22, 52, "COMMENT")  # "(recommended: Amish or Indian)" (Kept)
        ]
    }),

    # Example 219
    ("1/2 teaspoon hot paprika", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 16, "PREP"),  # "hot" (Kept)
            (17, 24, "NAME")  # "paprika"
        ]
    }),

    # Example 220
    ("5 oblong fruit-flavored gum or candies, such as Mike and Ike", {
        "entities": [
            (0, 1, "QTY"),  # "5" (Kept)
            (2, 8, "PREP"),  # "oblong" (from original PREP "oblong fruit-flavored" 2-23)
            (9, 23, "PREP"),  # "fruit-flavored" (from original PREP "oblong fruit-flavored" 2-23)
            (24, 27, "NAME"),  # "gum"
            (28, 38, "ALT_NAME"),  # "or candies" (Kept, original had comma after, assuming comma O)
            # Comma at 38 is "O"
            (40, 60, "COMMENT")  # "such as Mike and Ike" (Kept)
        ]
    }),

    # Example 221
    ("1/2 cup mini-marshmallows", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 25, "NAME")  # "mini-marshmallows" (tokenized as one)
        ]
    }),

    # Example 222
    ("1 (19.4 oz.) package Pillsbury Funfetti Chocolate Fudge Brownie Mix, seasonal variety of choice", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "COMMENT"),  # "(19.4 oz.)" (Kept)
            (13, 20, "UNIT"),  # "package"
            (21, 67, "NAME"),  # "Pillsbury" (from original NAME 21-67)
            # Comma at 67 (if Mix ends at 66) is "O"
            (69, 95, "COMMENT")  # "seasonal variety of choice" (Kept)
        ]
    }),

    # Re-annotated data based on the FINAL REFINED rules:
    # - NAME entities are broken into word-level NAME entities.
    # - COMMENT, PREP, ALT_NAME, QTY entities are kept as single, original spans.
    # - UNIT entities are single words.
    # - Commas and other non-entity words become "O" (and are thus not listed in the 'entities' list).
    # Tokenization based on spaCy's default English tokenizer.

    # ... (all previous examples from your earlier chunks would be here) ...

    # Example 1
    ("1/4 cup thinly sliced fresh basil leaves, cilantro, or parsley (optional)",
     {  # If ALT_NAME was "cilantro, or parsley"
         "entities": [
             (0, 3, "QTY"), (4, 7, "UNIT"), (8, 21, "PREP"), (22, 27, "PREP"),
             (28, 33, "NAME"), (34, 40, "NAME"),
             (42, 62, "ALT_NAME"),  # "cilantro, or parsley"
             (63, 73, "COMMENT")
         ]
     }),

    # Example 2
    ("2 pounds, about 10 Roma tomatoes, cored and chopped", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            # Comma at 8 is "O"
            (10, 18, "COMMENT"),  # "about 10" (Kept)
            (19, 23, "NAME"),  # "Roma" (from original NAME "Roma tomatoes" 19-32)
            (24, 32, "NAME"),  # "tomatoes" (from original NAME "Roma tomatoes" 19-32)
            # Comma at 32 is "O"
            (34, 51, "PREP")  # "cored and chopped" (Kept)
        ]
    }),

    # Example 3
    ("2 tablespoons fresh basil leaves, chiffonade", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 19, 'PREP'),  # "fresh" (Kept)
            (20, 25, "NAME"),  # "basil" (from original NAME "basil leaves" 20-32)
            (26, 32, "NAME"),  # "leaves" (from original NAME "basil leaves" 20-32)
            # Comma at 32 is "O"
            (34, 44, "PREP")  # "chiffonade" (Kept)
        ]
    }),

    # Example 4
    ("1 cup demi-glace", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 16, "NAME")  # "demi-glace" (tokenized as one)
        ]
    }),

    # Example 5
    ("1 cup cubed provolone (1/2-inch)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 11, "PREP"),  # "cubed" (Kept)
            (12, 21, "NAME"),  # "provolone"
            (22, 32, "COMMENT")  # "(1/2-inch)" (Kept)
        ]
    }),

    # Example 6
    ("1 pound smoked fresh mozzarella cheese, sliced",
     {  # If (21,38,"NAME") mozzarella cheese and (40,46,"PREP") sliced
         "entities": [
             (0, 1, "QTY"), (2, 7, "UNIT"), (8, 14, "PREP"), (15, 20, "PREP"),
             (21, 31, "NAME"), (32, 38, "NAME"),  # mozzarella cheese
             (40, 46, "PREP")  # sliced
         ]
     }),

    # Example 7
    ("1 large or 2 small plantains", {
        "entities": [
            # Primary Item description
            (0, 1, "QTY"),         # "1"
            (2, 7, "UNIT"),        # "large"
            (8,10,'ALT_NAME'),
            # Alternative description for the same item
            (11, 12, "ALT_QTY"),   # "2" (alternative quantity for plantains)
            (13, 18, "ALT_UNIT"),  # "small" (alternative size unit for plantains)
            # Core Item Name
            (19, 28, "NAME")       # "plantains"
        ]
    }),

    # Example 8
    ("1/4 cup Hot Country Ham Jus, recipe follows", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 11, "NAME"),  # "Hot" (from original NAME "Hot Country Ham Jus" 8-27)
            (12, 19, "NAME"),  # "Country" (from original NAME 8-27)
            (20, 23, "NAME"),  # "Ham" (from original NAME 8-27)
            (24, 27, "NAME"),  # "Jus" (from original NAME 8-27)
            # Comma at 27 is "O"
            (29, 43, "COMMENT")  # "recipe follows" (Kept)
        ]
    }),

    # Example 9
    ("1/4 pound pickled tongue", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 17, "PREP"),  # "pickled" (Kept)
            (18, 24, "NAME")  # "tongue"
        ]
    }),

    # Example 10

    ("1 1/2 cups finely diced strawberries", {  # If "diced strawberries" was NAME
        "entities": [
            (0, 5, "QTY"), (6, 10, "UNIT"), (11, 17, "PREP"),  # finely
            (18, 23, "NAME"), (24, 36, "NAME")  # diced, strawberries
        ]
    }),

    # Example 11
    ("16 ounces premade pancake batter", {
        "entities": [
            (0, 2, "QTY"),  # "16" (Kept)
            (3, 9, "UNIT"),  # "ounces"
            (10, 17, "PREP"),  # "premade" (Kept)
            (18, 25, "NAME"),  # "pancake" (from original NAME "pancake batter" 18-32)
            (26, 32, "NAME")  # "batter" (from original NAME "pancake batter" 18-32)
        ]
    }),

    # Example 12
    ("4 cups sliced mozzarella de Buffalo", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 13, "PREP"),  # "sliced" (Kept)
            (14, 24, "NAME"),  # "mozzarella" (from original NAME "mozzarella de Buffalo" 14-35)
            (25, 27, "NAME"),  # "de" (from original NAME 14-35) - *Unusual*
            (28, 35, "NAME")  # "Buffalo" (from original NAME 14-35)
        ]
    }),

    # Example 13
    ("1 teaspoon tobarashi (Japanese 7-spice)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 20, "NAME"),  # "tobarashi"
            (21, 39, "COMMENT")  # "(Japanese 7-spice)" (Kept)
        ]
    }),

    # Example 14
    ("6 ounces aji-mirin", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 18, "NAME")  # "aji-mirin" (tokenized as one)
        ]
    }),

    # Example 15
    ("6 to 12 basil leaves, for garnish", {
        "entities": [
            (0, 1, "QTY"),  # "6 to 12" (Kept)
            (2, 7, "COMMENT"),  # "6 to 12" (Kept)
            (8, 13, "NAME"),  # "basil"
            (14, 20, "UNIT"),  # "leaves"
            # Comma at 20 is "O"
            (22, 33, "COMMENT")  # "for garnish" (Kept)
        ]
    }),

    # Example 16
    ("3 fresh bay leaves", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 7, "PREP"),  # "fresh" (Kept)
            (8, 11, "NAME"),  # "bay" (from original NAME "bay leaves" 8-18)
            (12, 18, "NAME")  # "leaves" (from original NAME "bay leaves" 8-18)
        ]
    }),

    # Example 17
    ("3 cups Pimm's No. 1 Cup, available at liquor stores", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 23, "NAME"),  # "Pimm's" (from original NAME "Pimm's No. 1 Cup" 7-23)
            # Comma at 23 is "O"
            (25, 51, "COMMENT")  # "available at liquor stores" (Kept)
        ]
    }),

    # Example 18
    ("1 tablespoon store-bought or homemade caper tapenade", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 37, "PREP"),  # "store-bought" (Kept)
            (38, 43, "NAME"),  # "caper" (from original NAME "caper tapenade" 38-52)
            (44, 52, "NAME")  # "tapenade" (from original NAME "caper tapenade" 38-52)
        ]
    }),

    # Example 19
    ("1 tablespoon roughly chopped capers", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 20, "PREP"),  # "roughly" (from original PREP "roughly chopped" 13-28)
            (21, 28, "PREP"),  # "chopped" (from original PREP "roughly chopped" 13-28)
            (29, 35, "NAME")  # "capers"
        ]
    }),

    # Example 20
    ("1/2 cup roughly chopped fresh fennel, fronds reserved for garnish", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "PREP"),  # "roughly" (from original PREP "roughly chopped fresh" 8-29)
            (16, 23, "PREP"),  # "chopped" (from original PREP "roughly chopped fresh" 8-29)
            (24, 29, "PREP"),  # "fresh" (from original PREP "roughly chopped fresh" 8-29)
            (30, 36, "NAME"),  # "fennel"
            # Comma at 36 is "O"
            (38, 65, "COMMENT")  # "fronds reserved for garnish" (Kept)
        ]
    }),

    # Example 21
    ("1 tablespoon chopped fennel fronds", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 20, "PREP"),  # "chopped" (Kept)
            (21, 27, "NAME"),  # "fennel" (from original NAME "fennel fronds" 21-34)
            (28, 34, "NAME")  # "fronds" (from original NAME "fennel fronds" 21-34)
        ]
    }),

    # Example 22
    ("1/4 cup packed fresh basil leaves, torn", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "packed" (Kept from original (8,14,"PREP"))
            (15, 20, "PREP"),  # "fresh" (from original NAME "fresh basil leaves" 15-33)
            (21, 26, "NAME"),  # "basil" (from original NAME "fresh basil leaves" 15-33)
            (27, 33, "NAME"),  # "leaves" (from original NAME "fresh basil leaves" 15-33)
            # Comma at 33 is "O"
            (35, 39, "PREP")  # "torn" (Kept)
        ]
    }),

    # Example 23
    ("1/4 cup lightly packed fresh culantro leaves and tender stems", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "PREP"),  # "lightly" (from original PREP "lightly packed fresh" 8-28)
            (16, 22, "PREP"),  # "packed" (from original PREP "lightly packed fresh" 8-28)
            (23, 28, "PREP"),  # "fresh" (from original PREP "lightly packed fresh" 8-28)
            (29, 37, "NAME"),  # "culantro" (from original NAME "culantro leaves" 29-44)
            (38, 44, "NAME"),  # "leaves" (from original NAME "culantro leaves" 29-44)
            (45, 61, "ALT_NAME")  # "tender stems" (Kept)
        ]
    }),

    # Example 24
    ("1/4 cups whole, hulled strawberries", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 8, "UNIT"),  # "cups"
            (9, 22, "PREP"),  # "whole" (from original PREP "whole, hulled" 9-22, includes comma)
            (23, 35, "NAME")  # "strawberries"
        ]
    }),

    # Example 25
    ("4 cups Mama's Cornbread", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 13, "COMMENT"),  # "Mama's" (from original NAME "Mama's Cornbread" 7-23)
            (14, 23, "NAME")  # "Cornbread" (from original NAME "Mama's Cornbread" 7-23)
        ]
    }),

    # Example 26
    ("1/2 ounce grated or finely sliced mozzarella cheese", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "ounce"
            (10, 33, "PREP"),  # "grated" (Kept)
            (34, 44, "NAME"),  # "mozzarella" (from original NAME "mozzarella cheese" 34-51)
            (45, 51, "NAME")  # "cheese" (from original NAME "mozzarella cheese" 34-51)
        ]
    }),

    # Example 27
    ("1/2 cup silver or gold tequila", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "NAME"),  # "silver"
            (15, 22, "ALT_NAME"),  # "or gold" (Kept)
            (23, 30, "NAME")  # "tequila"
        ]
    }),

    # Example 28
    ("1/2 baguette, toasted and cut into 4 pieces", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "NAME"),  # "baguette"
            # Comma at 12 is "O"
            (14, 43, "PREP")  # "toasted and cut into 4 pieces" (Kept)
        ]
    }),

    # Example 29
    ("1 bunch fresh savory leaves", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "bunch"
            (8, 13, "PREP"),  # "fresh" (Kept)
            (14, 20, "NAME"),  # "savory" (from original NAME "savory leaves" 14-27)
            (21, 27, "NAME")  # "leaves" (from original NAME "savory leaves" 14-27)
        ]
    }),

    # Example 30
    ("1/4 cup picked fennel fronds", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "picked" (Kept)
            (15, 21, "NAME"),  # "fennel" (from original NAME "fennel fronds" 15-28)
            (22, 28, "NAME")  # "fronds" (from original NAME "fennel fronds" 15-28)
        ]
    }),

    # Example 31
    ("1/4 pound liver, blood vessels removed (we used rabbit liver for the episode, but you can use turkey and/or chicken livers)",
     {
         "entities": [
             (0, 3, "QTY"),  # "1/4" (Kept)
             (4, 9, "UNIT"),  # "pound"
             (10, 15, "NAME"),  # "liver"
             # Comma at 15 is "O"
             (17, 38, "PREP"),  # "blood vessels removed" (Kept)
             (39, 123, "COMMENT")
             # "(we used rabbit liver for the episode, but you can use turkey and/or chicken livers)" (Kept)
         ]
     }),

    # Example 32
    ("10 prunes, pitted", {
        "entities": [
            (0, 2, "QTY"),  # "10" (Kept)
            (3, 9, "NAME"),  # "prunes"
            # Comma at 9 is "O"
            (11, 17, "PREP")  # "pitted" (Kept)
        ]
    }),

    # Example 33
    ("1/4 cup pickled relish", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "PREP"),  # "pickled" (Kept)
            (16, 22, "NAME")  # "relish"
        ]
    }),

    # Example 34
    ("1 pound ball dough from market or your favorite pizza parlor or EZ Pizza Dough", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 12, "NAME"),  # "ball" (from original NAME "ball dough" 8-18)
            (13, 18, "NAME"),  # "dough" (from original NAME "ball dough" 8-18)
            (19, 78, "COMMENT")  # "from market or your favorite pizza parlor or EZ Pizza Dough" (Kept)
        ]
    }),

    # Example 35
    ("8 medium eggs", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "NAME"),  # "medium" (from original NAME "medium eggs" 2-13)
            (9, 13, "NAME")  # "eggs" (from original NAME "medium eggs" 2-13)
        ]
    }),

    # Example 36
    ("4 eggs", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "NAME")  # "eggs"
        ]
    }),

    # Example 37
    ("4 large eggs", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 7, "UNIT"),  # "large"
            (8, 12, 'NAME')  # "eggs"
        ]
    }),

    # Example 38
    ("1/2 teaspoon ground pepperoncini or crushed red pepper flakes", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 19, "NAME"),  # "ground" (from original NAME "ground pepperoncini" 13-32)
            (20, 32, "NAME"),  # "pepperoncini" (from original NAME "ground pepperoncini" 13-32)
            (33, 61, "ALT_NAME")  # "crushed red pepper flakes" (Kept)
        ]
    }),

    # Example 39
    ("1/4 cup grated Parm", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "NAME"),  # "grated" (from original NAME "grated Parm" 8-19)
            (15, 19, "NAME")  # "Parm" (from original NAME "grated Parm" 8-19)
        ]
    }),

    # Example 40

    ("2/3 cup (165 milliliters) lager or light flavored ale", {  # If comment was (9,25) to include )
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (9, 24, "COMMENT"),  # "(165 milliliters)"
            (26, 31, "NAME"),
            (32, 53, "ALT_NAME")
        ]
    }),

    # Example 41
    ("1/2 teaspoon pure vanilla extract", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 17, "NAME"),  # "pure" (from original NAME "pure vanilla extract" 13-33)
            (18, 25, "NAME"),  # "vanilla" (from original NAME "pure vanilla extract" 13-33)
            (26, 33, "NAME")  # "extract" (from original NAME "pure vanilla extract" 13-33)
        ]
    }),

    # Example 42
    ("2 large bundles, 1 pound, spinach leaves", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 7, "UNIT"),  # "large" (from original UNIT "large bundles" 2-15)
            # Comma at 15 is "O"
            (8, 24, "COMMENT"),  # "1 pound" (Kept)
            # Comma at 24 is "O"
            (26, 33, "NAME"),  # "spinach" (from original NAME "spinach leaves" 26-40)
            (34, 40, "NAME")  # "leaves" (from original NAME "spinach leaves" 26-40)
        ]
    }),

    # Example 43
    ("8 ounces (1 cup) bourbon", {  # If comment was (9,16) for (1 cup)
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"),
            (9, 16, "COMMENT"),  # "(1 cup)"
            (17, 24, "NAME")
        ]
    }),

    # Example 44
    ("Two (4.5-ounce) cans chopped green chiles, drained", {
        "entities": [
            (0, 3, "QTY"),  # "Two" (Kept)
            (4, 15, "COMMENT"),  # "4.5-ounce" (Original COMMENT (5,14))
            (16, 20, "UNIT"),  # "cans"
            (21, 28, "NAME"),  # "chopped" (from original NAME "chopped green chiles" 21-41)
            (29, 34, "NAME"),  # "green" (from original NAME "chopped green chiles" 21-41)
            (35, 41, "NAME"),  # "chiles" (from original NAME "chopped green chiles" 21-41)
            # Comma at 41 is "O"
            (43, 50, "COMMENT")  # "drained" (Original COMMENT (43,50) not PREP)
        ]
    }),

    # Example 45
    ("2 tablespoons flavoring of your choice (orange, almond, or raspberry liqueur, etc.)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 23, "NAME"),  # "flavoring" (from original NAME "flavoring of your choice" 14-38)
            (24, 26, "NAME"),  # "of" (from original NAME 14-38) - *Unusual*
            (27, 31, "NAME"),  # "your" (from original NAME 14-38) - *Unusual*
            (32, 38, "NAME"),  # "choice" (from original NAME 14-38)
            (39, 83, "COMMENT")  # "orange, almond, or raspberry liqueur, etc.)" (Kept, original span (40,83))
        ]
    }),

    # Example 46
    ("8 cups crumbled (1/4-inch pieces), toasted cornbread", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 15, "PREP"),  # "crumbled" (Kept)
            (16, 33, "COMMENT"),  # "1/4-inch pieces" (Original COMMENT (17,32))
            # Comma at 33 is "O"
            (35, 42, "NAME"),  # "toasted" (from original NAME "toasted cornbread" 35-52)
            (43, 52, "NAME")  # "cornbread" (from original NAME "toasted cornbread" 35-52)
        ]
    }),

    # Example 47
    ("1/2 teaspoon your favorite hot sauce", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 26, "COMMENT"),  # "your" (from original NAME "your favorite hot sauce" 13-36) - *Unusual*
            (27, 30, "NAME"),  # "hot" (from original NAME 13-36)
            (31, 36, "NAME")  # "sauce" (from original NAME 13-36)
        ]
    }),

    # Example 48
    ("4 to 8 lemon wedges", {
        "entities": [
            (0, 1, "QTY"),  # "4 to 8" (Kept)
            (2, 6, "QTY"),  # "4 to 8" (Kept)
            (7, 12, "NAME"),  # "lemon" (from original NAME "lemon wedges" 7-19)
            (13, 19, "NAME")  # "wedges" (from original NAME "lemon wedges" 7-19)
        ]
    }),

    # Example 49
    ("8 ounces tomatillos, husked and cut into quarters", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 19, "NAME"),  # "tomatillos"
            # Comma at 19 is "O"
            (21, 49, "COMMENT")  # "husked and cut into quarters" (Kept as original COMMENT span)
        ]
    }),

    # Example 50
    ("8 ounces nduja", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 14, "NAME")  # "nduja"
        ]
    }),

    # Example 51
    ("3 quinces, peeled and cubed (about 4 cups)", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 9, "NAME"),  # "quinces"
            # Comma at 9 is "O"
            (11, 42, "COMMENT")  # "peeled and cubed (about 4 cups)" (Kept as original COMMENT span)
        ]
    }),

    # Example 52

    ("3/4 cup, plus 3 tablespoons olive oil", {  # If (9,27,"COMMENT") was "plus 3 tablespoons"
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (9, 27, "COMMENT"),
            (28, 33, "NAME"), (34, 37, "NAME")
        ]
    }),

    # Example 53
    ("8 frankfurters", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 14, "NAME")  # "frankfurters"
        ]
    }),

    ("1 teaspoon plus a pinch paprika", {  # If (11,23,"COMMENT") was for "plus a pinch"
        "entities": [
            (0, 1, "QTY"), (2, 10, "UNIT"),
            (11, 23, "COMMENT"),
            (24, 31, "NAME")
        ]
    }),

    # Example 55
    ("1/2 teaspoon sweet paprika", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 18, "NAME"),  # "sweet" (from original NAME "sweet paprika" 13-26)
            (19, 26, "NAME")  # "paprika" (from original NAME "sweet paprika" 13-26)
        ]
    }),

    # Example 56
    ("1 pound tripe, soaked overnight, cut into large pieces", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 13, "NAME"),  # "tripe"
            # Comma at 13 is "O"
            (15, 54, "COMMENT")  # "soaked overnight, cut into large pieces" (Kept as original COMMENT span)
        ]
    }),

    # Example 57
    ("4 medium to large lamb foreshanks", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "UNIT"),  # "medium"
            (9, 17, "PREP"),  # "to" # Your original had (18,33,"NAME") for "lamb foreshanks"
            (18, 22, "NAME"),  # "lamb" (from original NAME "lamb foreshanks" 18-33)
            (23, 33, "NAME")  # "foreshanks" (from original NAME "lamb foreshanks" 18-33)
        ]
    }),

    # Example 58
    ("10 oz. 7-Up", {
        "entities": [
            (0, 2, "QTY"),  # "10" (Kept)
            (3, 6, "UNIT"),  # "oz."
            (7, 11, "NAME")  # "7-Up" (tokenized as one)
        ]
    }),

    # Example 59
    ("2 pappadams", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 11, "NAME")  # "pappadams"
        ]
    }),

    # Example 60
    ("1 sprig fresh thyme", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "PREP"),  # "sprig" (Kept)
            (8, 13, "PREP"),  # "fresh" (Kept)
            (14, 19, "NAME")  # "thyme"
        ]
    }),

    # Example 61
    ("1/2 pound store bought celery", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 22, "PREP"),  # "store" (from original NAME "store bought celery" 10-29)
            (23, 29, "NAME")  # "celery" (from original NAME "store bought celery" 10-29)
        ]
    }),

    # Example 62
    ("2 1/2 pounds mahi-mahi, cut into 1/2-inch cubes", {
        "entities": [
            (0, 5, "QTY"),  # "2 1/2" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 22, "NAME"),  # "mahi-mahi" (tokenized as one)
            # Comma at 22 is "O"
            (24, 47, "COMMENT")  # "cut into 1/2-inch cubes" (Kept as original COMMENT span)
        ]
    }),

    # Example 63
    ("1/2 teaspoon rose water*", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 17, "NAME"),  # "rose" (from original NAME "rose water" 13-23)
            (18, 23, "NAME"),  # "water" (from original NAME "rose water" 13-23)
            (23, 24, "COMMENT")  # "*" (Original label was COMMENT)
        ]
    }),

    # Example 64
    ("4 poussin, 1 1/2 pounds each", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 9, "NAME"),  # "poussin"
            # Comma at 9 is "O"
            (11, 28, "COMMENT")  # "1 1/2 pounds each" (Kept)
        ]
    }),

    # Example 65
    ("1/2 teaspoon plus of Nori granules with ginger, (Maine Coast Sea Vegetables)", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 20, "COMMENT"),  # "plus" (This was not in your original spans, so "O")
            (21, 25, "NAME"),  # "Nori" (from original NAME "Nori granules with ginger" 21-46)
            (26, 34, "NAME"),  # "granules" (from original NAME 21-46)
            (35, 46, "PREP"),  # "with" (from original NAME 21-46) - *Unusual*
            # Comma at 46 is "O"
            (48, 75, "COMMENT")  # "(Maine Coast Sea Vegetables)" (Kept)
        ]
    }),

    # Example 66

    ("7 ounces (two 100-gram blocks) or about 1 cup achiote paste",
     {  # If original (10,45,"COMMENT") was for everything up to "cup"
         "entities": [
             (0, 1, "QTY"), (2, 8, "UNIT"),
             (9, 45, "COMMENT"),  # "two 100-gram blocks) or about 1 cup"
             (46, 53, "NAME"), (54, 59, "NAME")  # achiote paste
         ]
     }),

    # Example 67
    ("1/4 cup cold-brew coffee, such as Stumptown", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 17, "NAME"),  # "cold-brew" (from original NAME "cold-brew coffee" 8-24)
            (18, 24, "NAME"),  # "coffee" (from original NAME "cold-brew coffee" 8-24)
            # Comma at 24 is "O"
            (26, 43, "COMMENT")  # "such as Stumptown" (Kept)
        ]
    }),

    # Example 68
    ("2 - 8 ounce skin on wild Striped Bass fillets", {
        "entities": [
            (0, 1, "QTY"),  # "2 - 8" (Kept, includes hyphen and spaces as per original)
            (2, 5, "PREP"),  # "2 - 8" (Kept, includes hyphen and spaces as per original)
            (6, 11, "UNIT"),  # "ounce"
            (12, 16, "NAME"),  # "skin" (from original NAME "skin on wild Striped Bass fillets" 12-45)
            (17, 19, "NAME"),  # "on" (from original NAME 12-45) - *Unusual*
            (20, 24, "NAME"),  # "wild" (from original NAME 12-45)
            (25, 32, "NAME"),  # "Striped" (from original NAME 12-45)
            (33, 37, "NAME"),  # "Bass" (from original NAME 12-45)
            (38, 45, "NAME")  # "fillets" (from original NAME 12-45)
        ]
    }),

    # Example 69
    ('1 1/2 pounds mahi-mahi fillets, cut into "fingers" about 3 inches in length', {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 22, "NAME"),  # "mahi-mahi" (from original NAME "mahi-mahi fillets" 13-30)
            (23, 30, "NAME"),  # "fillets" (from original NAME "mahi-mahi fillets" 13-30)
            # Comma at 30 is "O"
            (32, 75, "COMMENT")  # 'cut into "fingers" about 3 inches in length' (Kept)
        ]
    }),

    # Example 70
    ("1 large clove", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, 'UNIT'),  # "large"
            (8, 13, "NAME")  # "clove"
        ]
    }),

    # Example 71
    ("Two 10- to 12-pound turkeys", {  # If 10- to 12-pound was COMMENT
        "entities": [
            (0, 3, "QTY"),
            (4, 19, "COMMENT"),  # "10- to 12-pound"
            (20, 27, "NAME")
        ]
    }),

    # Example 72
    ("1/2 pound spiny lobster, cooked and chopped", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 15, "NAME"),  # "spiny" (from original NAME "spiny lobster" 10-23)
            (16, 23, "NAME"),  # "lobster" (from original NAME "spiny lobster" 10-23)
            # Comma at 23 is "O"
            (25, 43, "COMMENT")  # "cooked and chopped" (Kept as original COMMENT span)
        ]
    }),

    # Example 73
    ("1 tablespoon lecithin (found in health food stores)", {  # If comment includes ()
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"), (13, 21, "NAME"),
            (22, 50, "COMMENT")  # "(found in health food stores)"
        ]
    }),

    # Example 74
    ("2 teaspoons vanilla extract", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 11, "UNIT"),  # "teaspoons"
            (12, 19, "NAME"),  # "vanilla" (from original NAME "vanilla extract" 12-27)
            (20, 27, "NAME")  # "extract" (from original NAME "vanilla extract" 12-27)
        ]
    }),

    # Example 75
    ("6 tablespoons confectioners’ sugar", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 28, "NAME"),  # "confectioners’" (from original NAME "confectioners’ sugar" 14-34)
            (29, 34, "NAME")  # "sugar" (from original NAME "confectioners’ sugar" 14-34)
        ]
    }),

    # Example 76
    ("14 ounces (400 grams) 1 small tin pineapple, use about 3 to 4 tablespoons of the juice", {
        "entities": [
            # Original (0,21,"COMMENT") "14 ounces (400 grams)"
            (0, 2, "QTY"),
            (3, 9, "UNIT"),
            (10, 21, "COMMENT"),
            (22, 33, "COMMENT"),  # "1" (Kept)
            (34, 43, "NAME"),  # "pineapple"
            # Comma at 43 is "O"
            (45, 86, "COMMENT")  # "use about 3 to 4 tablespoons of the juice" (Kept)
        ]
    }),

    # Example 77
    ("1/4 pound (1 stick) butter, room temperature", {  # If comment was (10,19) to include ()
        "entities": [
            (0, 3, "QTY"), (4, 9, "UNIT"),
            (10, 19, "COMMENT"),  # "(1 stick)"
            (20, 26, "NAME"),
            (28, 44, "PREP")
        ]
    }),

    # Example 78

    ("8 slices (2 medium eggplants, ends trimmed and cut crosswise into 1/2-inch thick slices)",
     {  # If (30,88) was comment including )
         "entities": [
             (0, 8, "COMMENT"),
             (10, 11, "QTY"), (12, 18, "UNIT"), (19, 28, "NAME"),
             (30, 88, "COMMENT")
         ]
     }),

    # Example 79
    ("8 cups 1/2-inch cubes Cornbread, recipe follows", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 15, "PREP"),  # "1/2-inch" (from original PREP "1/2-inch cubes" 7-21)
            (16, 21, "PREP"),  # "cubes" (from original PREP "1/2-inch cubes" 7-21)
            (22, 31, "NAME"),  # "Cornbread"
            # Comma at 31 is "O"
            (33, 47, "COMMENT")  # "recipe follows" (Kept)
        ]
    }),

    # Example 80
    ("1/4 cup, a generous handful, grated Parmigiano or Romano", {  # If "or Romano" was ALT_NAME
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (9, 27, "COMMENT"),
            (29, 35, "PREP"), (36, 46, "NAME"),
            (47, 56, "ALT_NAME")  # "or Romano"
        ]
    }),

    # Example 81
    ("1 cup M&Ms or chocolate chips", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"), (6, 10, "NAME"),
            (11, 29, "ALT_NAME")  # If your rule is "DONT SPLIT ALT_NAME"
        ]
    }),

    # Example 82
    ("2 large ears or fresh corn", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 7, "UNIT"),  # "large" (from original UNIT "large ears" 2-12)
            (8, 12, "UNIT"),  # "ears" (from original UNIT "large ears" 2-12)
            (13, 15, "O"),  # "or"
            (16, 21, "PREP"),  # "fresh" (from original NAME "fresh corn" 16-26)
            (22, 26, "NAME")  # "corn" (from original NAME "fresh corn" 16-26)
        ]
    }),

    # Example 83
    ("1/4 cup plus 1 tablespoon agave", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 25, "COMMENT"),  # "plus 1 tablespoon" (Kept)
            (26, 31, "NAME")  # "agave"
        ]
    }),

    # Example 84
    ("8 slices baguette, 1/2-inch thick, cut on an angle", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "PREP"),  # "slices" (Original label was PREP)
            (9, 17, "NAME"),  # "baguette"
            # Comma at 17 is "O"
            (19, 33, "COMMENT"),  # "1/2-inch thick" (Kept)
            # Comma at 33 is "O"
            (35, 50, "PREP")  # "cut on an angle" (Kept)
        ]
    }),

    # Example 85
    ("1/3 cup grated anejo or romano cheese", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (15, 20, "NAME"), \
            (21, 37, "ALT_NAME")  # "romano cheese"
        ]
    }),

    # Example 86
    ("1 cup faro", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 10, "NAME")  # "faro"
        ]
    }),

    # Example 87
    ("1/2 cup grated carrot", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "grated" (from original NAME "grated carrot" 8-21)
            (15, 21, "NAME")  # "carrot" (from original NAME "grated carrot" 8-21)
        ]
    }),

    # Example 88
    ("2 bunches of celery", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 9, "UNIT"),  # "bunches" (from original UNIT "bunches of" 2-12)
            (10, 12, "O"),  # "of" (from original UNIT "bunches of" 2-12) - *Unusual for "of" to be UNIT*
            (13, 19, "NAME")  # "celery"
        ]
    }),

    # Example 89
    ("1 can or jar clams in juice", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "can"
            (6, 12, "COMMENT"),  # "jar" (Original label was ALT_NAME)
            (13, 18, "NAME"),  # "clams" (from original NAME "clams in juice" 13-27)
            (19, 27, "PREP"),  # "in" (from original NAME "clams in juice" 13-27) - *Unusual*
        ]
    }),

    # Example 90
    ("2 inner stalks celery, diced", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 14, "PREP"),  # "inner" (from original UNIT "inner stalks" 2-14)
            (15, 21, "NAME"),  # "celery"
            # Comma at 21 is "O"
            (23, 28, "PREP")  # "diced" (Kept)
        ]
    }),

    # Example 91
    ("1 small carrot, diced", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "small"
            (8, 14, "NAME"),  # "carrot"
            # Comma at 14 is "O"
            (16, 21, "PREP")  # "diced" (Kept)
        ]
    }),

    # Example 92
    ("1 cinnamon stick", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 10, "NAME"),  # "cinnamon" (from original NAME "cinnamon stick" 2-16)
            (11, 16, "NAME")  # "stick" (from original NAME "cinnamon stick" 2-16)
        ]
    }),

    # Example 93
    ("1 pound ditaloni or tubetti", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 16, "NAME"),  # "ditaloni"
            (17, 27, "ALT_NAME"),  # "or"
        ]
    }),

    # Example 94
    ("3 cups tawny port", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 12, "NAME"),  # "tawny" (from original NAME "tawny port" 7-17)
            (13, 17, "NAME")  # "port" (from original NAME "tawny port" 7-17)
        ]
    }),

    # Example 95

    ("12 each Jumbo shrimp, peeled, deveined, tails intact", {  # If commas are O and preps are separate
        "entities": [
            (0, 2, "QTY"), (3, 7, "UNIT"), (8, 13, "NAME"), (14, 20, "NAME"),
            (22, 28, "PREP"),  # "peeled"
            # Comma O
            (30, 38, "PREP"),  # "deveined"
            # Comma O
            (40, 52, "COMMENT")
        ]
    }),

    # Example 96

    ("2 Tablespoons (30 ml) honey or other sweetener, to taste", {  # If original COMMENT was (14,22) for "(30 ml)"
        "entities": [
            (0, 1, "QTY"), (2, 13, "UNIT"),
            (14, 21, "COMMENT"),  # "(30 ml)"
            (22, 27, "NAME"), (28, 46, "ALT_NAME"),
            (48, 56, "COMMENT")
        ]
    }),

    # Example 97
    ("6 crepes (see above for recipe)", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 8, "NAME"),  # "crepes"
            (9, 31, "COMMENT")  # "(see above for recipe)" (Kept)
        ]
    }),

    # Example 98
    ("1 (14-ounce) can, hearts of palm, drained", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "COMMENT"),  # "(14-ounce)" (Kept)
            (13, 16, "UNIT"),  # "can"
            # Comma at 16 is "O"
            (18, 24, "NAME"),  # "hearts" (from original NAME "hearts of palm" 18-32)
            (25, 27, "NAME"),  # "of" (from original NAME "hearts of palm" 18-32) - *Unusual*
            (28, 32, "NAME"),  # "palm" (from original NAME "hearts of palm" 18-32)
            # Comma at 32 is "O"
            (34, 41, "PREP")  # "drained" (Kept)
        ]
    }),

    # Example 99
    ("One 3-inch cinnamon stick", {
        "entities": [
            (0, 3, "QTY"),  # "One" (Kept)
            (4, 10, "COMMENT"),  # "3-inch" (from original NAME "3-inch cinnamon stick" 4-25)
            (11, 19, "NAME"),  # "cinnamon" (from original NAME "3-inch cinnamon stick" 4-25)
            (20, 25, "NAME")  # "stick" (from original NAME "3-inch cinnamon stick" 4-25)
        ]
    }),

    # Example 100
    ("1 cup chopped brisket", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 13, "NAME"),  # "chopped" (from original NAME "chopped brisket" 6-21)
            (14, 21, "NAME")  # "brisket" (from original NAME "chopped brisket" 6-21)
        ]
    }),

    # Example 101
    ("3 leaf ends of celery stalks", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 14, "PREP"),  # "leaf" (from original NAME "leaf ends of celery stalks" 2-28)
            (15, 21, "NAME"),  # "celery" (from original NAME 2-28)
            (22, 28, "NAME")  # "stalks" (from original NAME 2-28)
        ]
    }),

    # Example 102
    ("1/4 cup shredded Romano", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 16, "NAME"),  # "shredded" (from original NAME "shredded Romano" 8-23)
            (17, 23, "NAME")  # "Romano" (from original NAME "shredded Romano" 8-23)
        ]
    }),

    # Example 103
    ("1/2 cup persimmon pulp", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 17, "NAME"),  # "persimmon" (from original NAME "persimmon pulp" 8-22)
            (18, 22, "NAME")  # "pulp" (from original NAME "persimmon pulp" 8-22)
        ]
    }),

    # Example 104
    ("1 cup sauerkraut heated to 135 degrees F", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 16, "NAME"),  # "sauerkraut"
            (17, 40, "PREP")  # "heated to 135 degrees F" (Kept)
        ]
    }),

    # Example 105
    ("Six 1/2- to 5/8-inch-thick slices rye bread", {
        "entities": [
            (0, 3, "QTY"),  # "Six" (Kept)
            (4, 26, "COMMENT"),  # "1/2- to 5/8-inch-thick" (Kept)
            (27, 33, "PREP"),  # "slices" (Original label was PREP)
            (34, 37, "NAME"),  # "rye" (from original NAME "rye bread" 34-43)
            (38, 43, "NAME")  # "bread" (from original NAME "rye bread" 34-43)
        ]
    }),

    # Example 106
    ("1 small pomegrante, peeled, seeds removed and separated", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "small"
            (8, 18, "NAME"),  # "pomegrante"
            # Comma at 18 is "O"
            (20, 55, "PREP")  # "peeled, seeds removed and separated" (Kept)
        ]
    }),

    # Example 107
    ("1/2 cup cilantro - chopped", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 16, "NAME"),  # "cilantro"
            (17, 18, "O"),  # "-"
            (19, 26, "PREP")  # "chopped" (Kept)
        ]
    }),

    # Example 108
    ("2 teaspoons garlic - minced", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 11, "UNIT"),  # "teaspoons"
            (12, 18, "NAME"),  # "garlic"
            (19, 20, "O"),  # "-"
            (21, 27, "PREP")  # "minced" (Kept)
        ]
    }),

    # Example 109
    ("1 pinch cayenne pepper", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "COMMENT"),  # "pinch" (Original label was COMMENT)
            (8, 15, "NAME"),  # "cayenne" (from original NAME "cayenne pepper" 8-22)
            (16, 22, "NAME")  # "pepper" (from original NAME "cayenne pepper" 8-22)
        ]
    }),

    # Example 110
    ("One 10-ounce can diced tomatoes and green chiles", {
        "entities": [
            (0, 3, "QTY"),  # "One" (Kept)
            (4, 12, "COMMENT"),  # "10-ounce" (Kept)
            (13, 16, "UNIT"),  # "can"
            (17, 22, "NAME"),  # "diced" (from original NAME "diced tomatoes and green chiles" 17-48)
            (23, 31, "NAME"),  # "tomatoes" (from original NAME 17-48)
            (32, 48, "ALT_NAME"),  # "and" (from original NAME 17-48) - *Unusual*
        ]
    }),

    # Example 111
    ("1 bunch fresh pea shoots", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "bunch"
            (8, 13, "PREP"),  # "fresh" (from original NAME "fresh pea shoots" 8-24)
            (14, 17, "NAME"),  # "pea" (from original NAME "fresh pea shoots" 8-24)
            (18, 24, "NAME")  # "shoots" (from original NAME "fresh pea shoots" 8-24)
        ]
    }),

    # Example 112
    ("1 tablespoon, plus 2 teaspoons Essence, recipe follows", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            # Comma at 12 is "O"
            (14, 30, "COMMENT"),  # "plus 2 teaspoons" (Kept)
            (31, 38, "NAME"),  # "Essence"
            # Comma at 38 is "O"
            (40, 54, "COMMENT")  # "recipe follows" (Kept)
        ]
    }),

    # Example 113
    ("3 tablespoons agave or honey", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 19, "NAME"),  # "agave"
            (20, 28, "ALT_NAME")  # "honey" (Original label was ALT_NAME)
        ]
    }),

    # Example 114
    ("1 clean, big stone", {  # If original NAME "clean, big stone" means comma part of first token
        "entities": [
            (0, 1, "QTY"),
            (2, 8, "PREP"),  # "clean,"
            (9, 12, "NAME"),  # "big"
            (13, 18, "NAME")  # "stone"
        ]
    }),

    # Example 115
    ("1 (14-ounce) can, crushed tomatoes", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "COMMENT"),  # "(14-ounce)" (Kept)
            (13, 16, "UNIT"),  # "can"
            # Comma at 16 is "O"
            (18, 25, "NAME"),  # "crushed" (from original NAME "crushed tomatoes" 18-34)
            (26, 34, "NAME")  # "tomatoes" (from original NAME "crushed tomatoes" 18-34)
        ]
    }),

    # Example 116
    ("1/2 cup dry white wine or chicken broth", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 11, "NAME"),  # "dry" (from original NAME "dry white wine" 8-22)
            (12, 17, "NAME"),  # "white" (from original NAME "dry white wine" 8-22)
            (18, 22, "NAME"),  # "wine" (from original NAME "dry white wine" 8-22)
            (23, 39, "ALT_NAME")  # "chicken broth" (Kept)
        ]
    }),

    # Example 117
    ("2 tablespoons crushed, dried neem (curry) leaves", {  # Assuming commas and parens are O
        "entities": [
            (0, 1, "QTY"), (2, 13, "UNIT"),
            (14, 22, "PREP"),  # crushed
            # Comma O
            (23, 28, "PREP"),  # dried
            (29, 33, "NAME"),  # neem
            # ( O
            (34, 41, "ALT_NAME"),  # curry
            # ) O
            (42, 48, "NAME")  # leaves
        ]
    }),

    # Example 118
    ("6 plain or sesame bagels, split", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 7, "NAME"),  # "plain"
            (8, 17, "ALT_NAME"),  # "or"
            (18, 24, "NAME"),  # "bagels" (from original ALT_NAME "sesame bagels" 11-24)
            # Comma at 24 is "O"
            (26, 31, "PREP")  # "split" (Kept)
        ]
    }),

    # Example 119
    ("1 tablespoon plus 2 teaspoons hot sauce", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 29, "COMMENT"),  # "plus 2 teaspoons" (Kept)
            (30, 33, "NAME"),  # "hot" (from original NAME "hot sauce" 30-39)
            (34, 39, "NAME")  # "sauce" (from original NAME "hot sauce" 30-39)
        ]
    }),

    # Example 120
    ("375 grams water 80 degrees F (27 degrees C)", {
        "entities": [
            (0, 3, "QTY"),  # "375" (Kept)
            (4, 9, "UNIT"),  # "grams"
            (10, 15, "NAME"),  # "water"
            (16, 43, "COMMENT")  # "80 degrees F (27 degrees C)" (Kept)
        ]
    }),

    # Example 121
    ("2 cups diced tomato", {  # "diced tomato" as NAME
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 12, "NAME"),  # "diced" (from original NAME "diced tomato" 7-19)
            (13, 19, "NAME")  # "tomato" (from original NAME "diced tomato" 7-19)
        ]
    }),

    # Example 122
    ("1 cup crushed tomatoes", {  # "crushed tomatoes" as NAME
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 13, "NAME"),  # "crushed" (from original NAME "crushed tomatoes" 6-22)
            (14, 22, "NAME")  # "tomatoes" (from original NAME "crushed tomatoes" 6-22)
        ]
    }),

    # Example 123
    ("16 ounces whole peeled tomatoes, broken into pieces, and their juices", {
        "entities": [
            (0, 2, "QTY"),  # "16" (Kept)
            (3, 9, "UNIT"),  # "ounces"
            (10, 15, "PREP"),  # "whole" (from original NAME "whole peeled tomatoes" 10-31)
            (16, 22, "NAME"),  # "peeled" (from original NAME "whole peeled tomatoes" 10-31)
            (23, 31, "NAME"),  # "tomatoes" (from original NAME "whole peeled tomatoes" 10-31)
            # Comma at 31 is "O"
            (33, 51, "PREP"),  # "broken into pieces" (Kept)
            # Comma at 51 is "O"
            (53, 69, "COMMENT")  # "and their juices" (Kept)
        ]
    }),

    # Example 124
    ("1 cup plus 2 teaspoons water", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 22, "COMMENT"),  # "plus 2 teaspoons" (Kept)
            (23, 28, "NAME")  # "water"
        ]
    }),

    # Example 125
    ("1/4 cup soft butter", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "NAME"),  # "soft" (from original NAME "soft butter" 8-19)
            (13, 19, "NAME")  # "butter" (from original NAME "soft butter" 8-19)
        ]
    }),

    # Example 126
    ("2 tablespoons grated Romano", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 20, "PREP"),  # "grated" (from original NAME "grated Romano" 14-27)
            (21, 27, "NAME")  # "Romano" (from original NAME "grated Romano" 14-27)
        ]
    }),

    # Example 127
    ("1/2 pound totani (flying squid), cleaned, cut into strips (see Cook's Note)", {  # If (33,57,"PREP") was one
        "entities": [
            (0, 3, "QTY"), (4, 9, "UNIT"), (10, 16, "NAME"), (17, 32, "COMMENT"),
            (33, 57, "PREP"),  # cleaned, cut into strips
            (59, 74, "COMMENT")  # (see Cook's Note) - end is 76 for `)`
        ]
    }),

    # Example 128
    ("4 loosely packed cups torn, soft lettuces, such as red oak and lolla rossa", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 16, "COMMENT"),  # "loosely packed" (Kept)
            (17, 21, "UNIT"),  # "cups"
            (22, 26, "PREP"),  # "torn" (Kept)
            # Comma at 26 is "O"
            (28, 32, "COMMENT"),  # "soft" (from original NAME "soft lettuces" 28-41)
            (33, 41, "NAME"),  # "lettuces" (from original NAME "soft lettuces" 28-41)
            # Comma at 41 is "O"
            (43, 74, "COMMENT")  # "such as red oak and lolla rossa" (Kept)
        ]
    }),

    # Example 129

    ("1 large bunch or 1 1/2 pounds large, leafy Swiss chard", {  # Assuming comma is O
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "UNIT"), (14, 29, "COMMENT"),
            (30, 35, "COMMENT"),  # large
            # Comma O
            (37, 42, "NAME"),  # leafy
            (43, 48, "NAME"),  # Swiss
            (49, 54, "NAME")  # chard
        ]
    }),

    # Example 130
    ("3/4 pound regular or pencil asparagus, trimmed of rough ends, a small bundle", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 17, "NAME"),  # "regular"
            (18, 27, "ALT_NAME"),  # "pencil" (from original ALT_NAME "pencil asparagus" 21-37)
            (28, 37, "NAME"),  # "asparagus" (from original ALT_NAME "pencil asparagus" 21-37)
            # Comma at 37 is "O"
            (39, 60, "PREP"),  # "trimmed of rough ends" (Kept)
            # Comma at 60 is "O"
            (62, 76, "COMMENT")  # "a small bundle" (Kept)
        ]
    }), \
 \
    # Example 131
    ("1 bunch or 6 scallions", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "bunch"
            (8, 12, "COMMENT"),  # "or 6" (Kept, original label COMMENT)
            (13, 22, "NAME")  # "scallions"
        ]
    }),

    # Example 132
    ("2 bunches thick asparagus (about 2 pounds)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 9, "UNIT"),  # "bunches"
            (10, 15, "NAME"),  # "thick" (from original NAME "thick asparagus" 10-25)
            (16, 25, "NAME"),  # "asparagus" (from original NAME "thick asparagus" 10-25)
            (26, 42, "COMMENT")  # "(about 2 pounds)" (Kept)
        ]
    }),

    # Example 133
    ("6 tablespoons light mayonnaise, divided", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 19, "NAME"),  # "light" (from original NAME "light mayonnaise" 14-30)
            (20, 30, "NAME"),  # "mayonnaise" (from original NAME "light mayonnaise" 14-30)
            # Comma at 30 is "O"
            (32, 39, "PREP")  # "divided" (Kept)
        ]
    }),

    # Example 134
    ("1 pound dried ziti", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 13, "NAME"),  # "dried" (from original NAME "dried ziti" 8-18)
            (14, 18, "NAME")  # "ziti" (from original NAME "dried ziti" 8-18)
        ]
    }),

    # Example 135

    ("1 vanilla bean, split lengthwise, seeds scraped out (pod reserved)",
     {  # If PREP was just "split lengthwise" and "seeds scraped out"
         "entities": [
             (0, 1, "QTY"), (2, 9, "NAME"), (10, 14, "NAME"),
             (16, 32, "PREP"),  # split lengthwise
             # Comma O
             (34, 51, "PREP"),  # seeds scraped out
             (52, 66, "COMMENT")
         ]
     }),

    # Example 136
    ("1 1/4 cups Guinness", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/4" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 19, "NAME")  # "Guinness"
        ]
    }),

    # Example 137
    ("2 teaspoons ground cinnamon", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 11, "UNIT"),  # "teaspoons"
            (12, 18, "NAME"),  # "ground" (from original NAME "ground cinnamon" 12-27)
            (19, 27, "NAME")  # "cinnamon" (from original NAME "ground cinnamon" 12-27)
        ]
    }),

    # Example 138
    ("One 28-ounce can peeled whole tomatoes", {
        "entities": [
            (0, 3, "QTY"),  # "One" (Kept)
            (4, 12, "COMMENT"),  # "28-ounce" (Kept)
            (13, 16, "UNIT"),  # "can"
            (17, 23, "NAME"),  # "peeled" (from original NAME "peeled whole tomatoes" 17-38)
            (24, 29, "NAME"),  # "whole" (from original NAME "peeled whole tomatoes" 17-38)
            (30, 38, "NAME")  # "tomatoes" (from original NAME "peeled whole tomatoes" 17-38)
        ]
    }),

    # Example 139
    ("4 tablespoons baconnaise", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 24, "NAME")  # "baconnaise"
        ]
    }),

    # Example 140
    ("12-ounce jar Buffalo sauce", {
        "entities": [
            (0, 8, "QTY"),  # "12-ounce" (Kept)
            (9, 12, "COMMENT"),  # "jar"
            (13, 20, "NAME"),  # "Buffalo" (from original NAME "Buffalo sauce" 13-26)
            (21, 26, "NAME")  # "sauce" (from original NAME "Buffalo sauce" 13-26)
        ]
    }),

    # Example 141
    ("5 bay leaves", {
        "entities": [
            (0, 1, "QTY"),  # "5" (Kept)
            (2, 5, "NAME"),  # "bay" (from original NAME "bay leaves" 2-12)
            (6, 12, "NAME")  # "leaves" (from original NAME "bay leaves" 2-12)
        ]
    }),

    # Example 142
    ("1 cup diced fresh tomatoes", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 11, "NAME"),  # "diced" (from original NAME "diced fresh tomatoes" 6-26)
            (12, 17, "PREP"),  # "fresh" (from original NAME "diced fresh tomatoes" 6-26)
            (18, 26, "NAME")  # "tomatoes" (from original NAME "diced fresh tomatoes" 6-26)
        ]
    }),

    # Example 143
    ("1 cup plain breadcrumbs", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 11, "NAME"),  # "plain" (from original NAME "plain breadcrumbs" 6-23)
            (12, 23, "NAME")  # "breadcrumbs" (from original NAME "plain breadcrumbs" 6-23)
        ]
    }),

    # Example 144
    ("1/4 cup ground cinnamon", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "NAME"),  # "ground" (from original NAME "ground cinnamon" 8-23)
            (15, 23, "NAME")  # "cinnamon" (from original NAME "ground cinnamon" 8-23)
        ]
    }),

    # Example 145
    ("12 ounces fresh spinach and cheese tortellini", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 9, "UNIT"),  # "ounces"
            (10, 15, "PREP"),  # "fresh" (from original NAME "fresh spinach and cheese tortellini" 10-45)
            (16, 23, "NAME"),  # "spinach" (from original NAME 10-45)
            (24, 45, "ALT_NAME"),  # "and" (from original NAME 10-45) - *Unusual*
        ]
    }),

    # Example 146
    ("3 tablespoons grenadine", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 23, "NAME")  # "grenadine"
        ]
    }),

    # Example 147
    ("1/2 cup unsulphured molasses", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 19, "NAME"),  # "unsulphured" (from original NAME "unsulphured molasses" 8-28)
            (20, 28, "NAME")  # "molasses" (from original NAME "unsulphured molasses" 8-28)
        ]
    }),

    # Example 148
    ("1 1/2 teaspoons ground turmeric", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 15, "UNIT"),  # "teaspoons"
            (16, 22, "NAME"),  # "ground" (from original NAME "ground turmeric" 16-31)
            (23, 31, "NAME")  # "turmeric" (from original NAME "ground turmeric" 16-31)
        ]
    }),

    # Example 149
    ("8 thin slices, prosciutto ham", {  # Assuming comma is O
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "PREP"), (7, 13, "PREP"),  # thin, slices
            # Comma O
            (15, 25, "NAME"), (26, 29, "NAME")  # prosciutto, ham
        ]
    }),

    # Example 150
    ("1/3 cup smooth sunflower seed butter", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "smooth" (from original NAME "smooth sunflower seed butter" 8-36)
            (15, 24, "NAME"),  # "sunflower" (from original NAME 8-36)
            (25, 29, "NAME"),  # "seed" (from original NAME 8-36)
            (30, 36, "NAME")  # "butter" (from original NAME 8-36)
        ]
    }),

    # Example 151
    ("1/2 bunch asparagus, trimmed and cut into bite-size pieces", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "bunch"
            (10, 19, "NAME"),  # "asparagus"
            # Comma at 19 is "O"
            (21, 58, "PREP")  # "trimmed and cut into bite-size pieces" (Kept)
        ]
    }),

    # Example 152
    ("1 cup strong coffee", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "NAME"),  # "strong" (from original NAME "strong coffee" 6-19)
            (13, 19, "NAME")  # "coffee" (from original NAME "strong coffee" 6-19)
        ]
    }),
    # Re-annotated data based on the FINAL REFINED rules:
    # - NAME entities are broken into word-level NAME entities.
    # - COMMENT, PREP, ALT_NAME, QTY entities are kept as single, original spans.
    # - UNIT entities are single words.
    # - Parentheses are NOT entities themselves unless they are part of a COMMENT/PREP/ALT_NAME/QTY span.
    # - Commas and other unspanned words become "O" (and are thus not listed in the 'entities' list).
    # Tokenization based on spaCy's default English tokenizer.

    # ... (all previous examples from your earlier chunks would be here) ...

    # Example 1
    ("About 14 ounces burgel (cracked wheat)", {
        "entities": [
            (0, 5, "COMMENT"),  # "About" (Kept)
            (6, 8, "QTY"),  # "14" (Kept)
            (9, 15, "UNIT"),  # "ounces"
            (16, 22, "NAME"),  # "burgel"
            (23, 38, "COMMENT")  # "(cracked wheat)" (Kept)
        ]
    }),

    # Example 2
    ("1 pound boneless, skinless, chicken breasts, sliced into strips", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 17, "NAME"),  # "boneless" (from original NAME "boneless, skinless, chicken breasts" 8-43)
            (18, 26, "NAME"),  # "skinless" (from original NAME 8-43)
            (28, 35, "NAME"),  # "chicken" (from original NAME 8-43)
            (36, 43, "NAME"),  # "breasts" (from original NAME 8-43)
            # Comma at 43 is "O"
            (45, 63, "PREP")  # "sliced into strips" (Kept)
        ]
    }),

    # Example 3
    ("7 cups cantaloupe chunks", {
        "entities": [
            (0, 1, "QTY"),  # "7" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 17, "NAME"),  # "cantaloupe" (from original NAME "cantaloupe chunks" 7-24)
            (18, 24, "NAME")  # "chunks" (from original NAME "cantaloupe chunks" 7-24)
        ]
    }),

    # Example 4
    ("4 ounces, 1/2 cup, Spanish peanuts", {  # If comma after cup is O
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"),
            (10, 17, "COMMENT"),  # "1/2 cup"
            # Comma O
            (19, 26, "NAME"), (27, 34, "NAME")
        ]
    }),

    # Example 5
    ("1 teaspoon dried crushed red pepper", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 16, "NAME"),  # "dried" (from original NAME "dried crushed red pepper" 11-35)
            (17, 24, "NAME"),  # "crushed" (from original NAME 11-35)
            (25, 28, "NAME"),  # "red" (from original NAME 11-35)
            (29, 35, "NAME")  # "pepper" (from original NAME 11-35)
        ]
    }),

    # Example 6
    ("1 cup pea shoots or tendrils", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 9, "NAME"),  # "pea" (from original NAME "pea shoots" 6-16)
            (10, 16, "NAME"),  # "shoots" (from original NAME "pea shoots" 6-16)
            (17, 28, "ALT_NAME")  # "tendrils" (Kept)
        ]
    }),

    # Example 7
    ("1 recipe tart shell (recipe follows)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "COMMENT"),  # "recipe"
            (9, 13, "NAME"),  # "tart" (from original NAME "tart shell" 9-19)
            (14, 19, "NAME"),  # "shell" (from original NAME "tart shell" 9-19)
            (20, 36, "COMMENT")  # "(recipe follows)" (Kept)
        ]
    }),

    # Example 8

    ("1 (28-ounce) and 1 (14-ounce) can whole tomatoes, both thoroughly drained",
     {  # If original (2,29,"COMMENT") was for "(28-ounce) and 1 (14-ounce)"
         "entities": [
             (0, 1, "QTY"),
             (2, 29, "COMMENT"),
             (30, 33, "UNIT"),
             (34, 39, "NAME"), (40, 48, "NAME"),
             (50, 73, "COMMENT")
         ]
     }),

    # Example 9
    ("1 package active dry or fresh yeast", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 9, "UNIT"),  # "package"
            (10, 16, "NAME"),  # "active" (from original NAME "active dry" 10-20)
            (17, 20, "NAME"),  # "dry" (from original NAME "active dry" 10-20)
            (21, 23, "O"),  # "or"
            (24, 29, "ALT_NAME"),  # "fresh yeast" (Kept)
            (30, 35, "NAME")  # "fresh yeast" (Kept)
        ]
    }),

    # Example 10
    ("2 tablespoons chopped fresh ogo (seaweed)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 27, "PREP"),  # "chopped" (from original NAME "chopped fresh ogo (seaweed)" 14-41)
            (28, 31, "NAME"),  # "ogo" (from original NAME 14-41)
            (32, 41, "COMMENT"),  # "(" (from original NAME 14-41) - *Unusual*
        ]
    }),

    # Example 11
    ("6 ounces dried lo mein noodles", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 14, "NAME"),  # "dried" (from original NAME "dried lo mein noodles" 9-30)
            (15, 17, "NAME"),  # "lo" (from original NAME 9-30)
            (18, 22, "NAME"),  # "mein" (from original NAME 9-30)
            (23, 30, "NAME")  # "noodles" (from original NAME 9-30)
        ]
    }),

    # Example 12
    ("3 to 4 tablespoons wasabi aioli, recipe follows", {
        "entities": [
            (0, 1, "QTY"),  # "3 to 4" (Kept, as per your original)
            (2, 6, "ALT_QTY"),  # "3 to 4" (Kept, as per your original)
            (7, 18, "UNIT"),  # "tablespoons"
            (19, 25, "NAME"),  # "wasabi" (from original NAME "wasabi aioli" 19-31)
            (26, 31, "NAME"),  # "aioli" (from original NAME "wasabi aioli" 19-31)
            # Comma at 31 is "O"
            (33, 47, "COMMENT")  # "recipe follows" (Kept)
        ]
    }),

    # Example 13
    ("2 (14 ounce/400 g each) live crabs, blue swimmer or mud crab", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 23, "COMMENT"),  # "(14 ounce/400 g each)" (Kept)
            (24, 28, "NAME"),  # "live" (from original NAME "live crabs" 24-34)
            (29, 34, "NAME"),  # "crabs" (from original NAME "live crabs" 24-34)
            # Comma at 34 is "O"
            (36, 48, "ALT_NAME"),  # "blue swimmer" (Kept, from original (36,60) "blue swimmer or mud crab")
            (49, 60, "ALT_NAME"),  # "or"
        ]
    }),

    # Example 14
    ("1 pound yellowtail fillet, sliced into 1-inch-thick strips", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 18, "NAME"),  # "yellowtail" (from original NAME "yellowtail fillet" 8-25)
            (19, 25, "NAME"),  # "fillet" (from original NAME "yellowtail fillet" 8-25)
            # Comma at 25 is "O"
            (27, 58, "PREP")  # "sliced into 1-inch-thick strips" (Kept)
        ]
    }),

    # Example 15
    ("2 cans pop, such as Dr. Pepper", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cans"
            (7, 10, "NAME"),  # "pop"
            # Comma at 10 is "O"
            (12, 30, "COMMENT")  # "such as Dr. Pepper" (Kept)
        ]
    }),

    # Example 16
    ("1 cup frozen peas and carrots, thawed", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "NAME"),  # "frozen" (from original NAME "frozen peas and carrots" 6-29)
            (13, 17, "NAME"),  # "peas" (from original NAME 6-29)
            (18, 21, "NAME"),  # "and" (from original NAME 6-29) - *Unusual*
            (22, 29, "NAME"),  # "carrots" (from original NAME 6-29)
            # Comma at 29 is "O"
            (31, 37, "PREP")  # "thawed" (Kept)
        ]
    }),

    # Example 17
    ("1 cup sliced bamboo shoots", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "PREP"),  # "sliced" (from original NAME "sliced bamboo shoots" 6-26)
            (13, 19, "NAME"),  # "bamboo" (from original NAME 6-26)
            (20, 26, "NAME")  # "shoots" (from original NAME 6-26)
        ]
    }),

    # Example 18
    ("4 ounces yam noodles (shirataki)", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 12, "NAME"),  # "yam" (from original NAME "yam noodles" 9-20)
            (13, 20, "NAME"),  # "noodles" (from original NAME "yam noodles" 9-20)
            (21, 32, "COMMENT")  # "(shirataki)" (Kept)
        ]
    }),

    # Example 19

    ("1/4 cup, (2 ounces) very warm water ( 105 to 115 degrees F)", {  # If (10,19,"COMMENT") was for "(2 ounces)"
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (9, 19, "COMMENT"),  # "(2 ounces)"
            (20, 29, "COMMENT"), (30, 35, "NAME"),  # very warm water
            (36, 59, "COMMENT")
        ]
    }),

    # Example 20
    ("1 French baguette", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "NAME"),  # "French" (from original NAME "French baguette" 2-17)
            (9, 17, "NAME")  # "baguette" (from original NAME "French baguette" 2-17)
        ]
    }),

    # Example 21
    ("2/3 cup ras el hanout", {
        "entities": [
            (0, 3, "QTY"),  # "2/3" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 11, "NAME"),  # "ras" (from original NAME "ras el hanout" 8-21)
            (12, 14, "NAME"),  # "el" (from original NAME 8-21) - *Unusual*
            (15, 21, "NAME")  # "hanout" (from original NAME 8-21)
        ]
    }),

    # Example 22
    ("1 whole head or 6 cloves of garlic", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "COMMENT"),  # "whole" (from original UNIT "whole head" 8-12, typo in your span?)
            (8, 12, "UNIT"),  # "head" (from original UNIT "whole head" 8-12)
            (13, 24, "ALT_NAME"),  # "6 cloves" (Kept)
            (25, 27, "PREP"),  # "of" (from original NAME "of garlic" 25-34) - *Unusual*
            (28, 34, "NAME")  # "garlic" (from original NAME "of garlic" 25-34)
        ]
    }),

    # Example 23
    ("1 cup diced rutabaga", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 11, "NAME"),  # "diced" (from original NAME "diced rutabaga" 6-20)
            (12, 20, "NAME")  # "rutabaga" (from original NAME "diced rutabaga" 6-20)
        ]
    }),

    # Example 24
    ("6 spiny lobster", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 7, "NAME"),  # "spiny" (from original NAME "spiny lobster" 2-15)
            (8, 15, "NAME")  # "lobster" (from original NAME "spiny lobster" 2-15)
        ]
    }),

    # Example 25
    ("6 spiny lobster tails, split lengthwise", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 7, "NAME"),  # "spiny" (from original NAME "spiny lobster tails" 2-21)
            (8, 15, "NAME"),  # "lobster" (from original NAME 2-21)
            (16, 21, "NAME"),  # "tails" (from original NAME 2-21)
            # Comma at 21 is "O"
            (23, 39, "PREP")  # "split lengthwise" (Kept)
        ]
    }),

    # Example 26 ("1 pound medium-thick asparagus, stalks peeled and trimmed")
    # Original: (8, 20, "COMMENT") for "medium-thick asparagus"
    # Original: (21,30,"NAME") for "asparagus" -- This conflicts.
    # Assuming (8,20, "COMMENT") for "medium-thick", and (21,30,"NAME") for "asparagus".
    ("1 pound medium-thick asparagus, stalks peeled and trimmed", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 20, "COMMENT"),  # "medium-thick" (Kept)
            (21, 30, "NAME"),  # "asparagus"
            # Comma at 30 is "O"
            (32, 57, "PREP")  # "stalks peeled and trimmed" (Kept)
        ]
    }),

    # Example 27
    ("3/4 cup, plus 2 tablespoons/200 g butter", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            # Comma at 7 is "O"
            (9, 33, "COMMENT"),  # "plus 2 tablespoons/200 g" (Kept)
            (34, 40, "NAME")  # "butter"
        ]
    }),

    ("1 1/2 pounds (4 pieces) filet of sole", {  # If space is not a token
        "entities": [
            (0, 5, "QTY"), (6, 12, "UNIT"), (13, 22, "COMMENT"),
            (24, 29, "NAME"), (30, 32, "NAME"), (33, 37, "NAME")  # filet of sole (adjusting for no space token)
            # The character offsets I generate assume spaCy tokenization where spaces are not tokens.
            # For (24,37,"NAME") "filet of sole": filet(24,29), of(30,32), sole(33,37)
        ]
    }),

    # Example 29
    ("150 grams (about 1 1/2 cups) ice cubes (preferably made from filtered water)", {
        "entities": [
            (0, 3, "QTY"),  # "150" (Kept)
            (4, 9, "UNIT"),  # "grams"
            (10, 27, "COMMENT"),  # "(about 1 1/2 cups)" (Kept)
            (29, 32, "NAME"),  # "ice" (from original NAME "ice cubes" 29-38)
            (33, 38, "NAME"),  # "cubes" (from original NAME "ice cubes" 29-38)
            (39, 76, "COMMENT")  # "(preferably made from filtered water)" (Kept)
        ]
    }),

    # Example 30
    ("1 cup freshly grated Parmigiano Reggiano cheese", {  # Assuming typo, 'chees'
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 13, "PREP"),  # "freshly" (from original NAME 6-46)
            (14, 20, "NAME"),  # "grated" (from original NAME 6-46)
            (21, 31, "NAME"),  # "Parmigiano" (from original NAME 6-46)
            (32, 40, "NAME"),  # "Reggiano" (from original NAME 6-46)
            (41, 47, "NAME")  # "chees" (from original NAME 6-46)
        ]
    }),

    # Example 31
    ("2 cups cooked, drained ground beef", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 22, "PREP"),  # "drained" (from NAME 7-34)
            (23, 29, "NAME"),  # "ground" (from NAME 7-34)
            (30, 34, "NAME")  # "beef" (from NAME 7-34)
        ]
    }),

    # Example 32
    ("2 tablespoons freshly grated Parmigiano-Reggiano cheese", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, 'PREP'),  # "freshly" (from original PREP 14-28 "freshly grated")
            (22, 28, 'NAME'),  # "grated" (from original PREP 14-28)
            (29, 48, "NAME"),  # "Parmigiano-Reggiano" (from original NAME "Parmigiano-Reggiano cheese" 29-55)
            (49, 55, "NAME")  # "cheese" (from original NAME "Parmigiano-Reggiano cheese" 29-55)
        ]
    }),

    # Example 33
    ("1 cup cut-up cooked asparagus (in 1- to 2-inch pieces)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 19, "PREP"),  # "cut-up" (from original NAME "cut-up cooked asparagus" 6-29)
            (20, 29, "NAME"),  # "asparagus" (from original NAME 6-29)
            (30, 54, "COMMENT")  # "(in 1- to 2-inch pieces)" (Kept)
        ]
    }),

    # Example 34
    ("8 ounces The Morning After Red Eye Gravy, recipe follows", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 34, "COMMENT"),  # "The" (from original NAME "The Morning After Red Eye Gravy" 9-40)\
            (35, 40, "NAME"),  # "Gravy" (from original NAME 9-40)
            # Comma at 40 is "O"
            (42, 56, "COMMENT")  # "recipe follows" (Kept)
        ]
    }),

    # Example 35
    ("1 pound andouille, cut crosswise into 1/2-inch slices", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 17, "NAME"),  # "andouille"
            # Comma at 17 is "O"
            (19, 53, "PREP")  # "cut crosswise into 1/2-inch slices" (Kept)
        ]
    }),

    # Example 36
    ("3 ounces 70 percent dark chocolate, broken into pieces", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 19, "PREP"),  # "70" (from original NAME "70 percent dark chocolate" 9-34)
            (20, 24, "NAME"),  # "dark" (from original NAME 9-34)
            (25, 34, "NAME"),  # "chocolate" (from original NAME 9-34)
            # Comma at 34 is "O"
            (36, 54, "PREP")  # "broken into pieces" (Kept)
        ]
    }),

    # Example 37
    ("8 ounces sweetened dark chocolate chunks, chopped small", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 18, "NAME"),  # "sweetened" (from original NAME "sweetened dark chocolate chunks" 9-40)
            (19, 23, "NAME"),  # "dark" (from original NAME 9-40)
            (24, 33, "NAME"),  # "chocolate" (from original NAME 9-40)
            (34, 40, "PREP"),  # "chunks" (from original NAME 9-40)
            # Comma at 40 is "O"
            (42, 49, "PREP"),  # "chopped" (from original PREP "chopped small" 42-55)
            (50, 55, "PREP")  # "small" (from original PREP "chopped small" 42-55)
        ]
    }),

    # Example 38 (Duplicate)
    ("1 pound andouille, cut crosswise into 1/2-inch slices", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 17, "NAME"), (19, 53, "PREP")
        ]
    }),

    # Example 39
    ("8 ounces frozen phyllo sheets, thawed and torn into pieces", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 15, "NAME"),  # "frozen" (from original NAME "frozen phyllo sheets" 9-29)
            (16, 22, "NAME"),  # "phyllo" (from original NAME 9-29)
            (23, 29, "NAME"),  # "sheets" (from original NAME 9-29)
            # Comma at 29 is "O"
            (31, 58, "PREP")  # "thawed and torn into pieces" (Kept)
        ]
    }),

    # Example 40
    ("1/2 teaspoon each allspice, nutmeg, and ginger", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon" (from original UNIT "teaspoon each" 4-17)
            (13, 17, "UNIT"),  # "each" (from original UNIT "teaspoon each" 4-17)
            (18, 26, "NAME"),  # "allspice"
            # Comma at 26 is "O"
            (28, 34, "ALT_NAME"),  # "nutmeg" (Original ALT_NAME (28,46) "nutmeg, and ginger")
            (36, 46, "ALT_NAME")  # "ginger" (If this was part of ALT_NAME (28,46))
        ]
    }),

    # Example 41
    ("1 brie triangle, chilled", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 6, "NAME"),  # "brie" (from original NAME "brie triangle" 2-15)
            (7, 15, "NAME"),  # "triangle" (from original NAME "brie triangle" 2-15)
            # Comma at 15 is "O"
            (17, 24, "PREP")  # "chilled" (Kept)
        ]
    }),

    # Example 42
    ("1 cup toasted walnut halves", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 13, "NAME"),  # "toasted" (from original NAME "toasted walnut halves" 6-27)
            (14, 20, "NAME"),  # "walnut" (from original NAME 6-27)
            (21, 27, "PREP")  # "halves" (from original NAME 6-27)
        ]
    }),

    # Example 43
    ("2 small, soft apples, such as McIntosh, chopped", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 7, "UNIT"),  # "small" (from original NAME "small, soft apples" 2-20)
            (9, 13, "NAME"),  # "soft" (from NAME 2-20)
            (14, 20, "NAME"),  # "apples" (from NAME 2-20)
            # Comma at 20 is "O"
            (22, 38, "COMMENT"),  # "such as McIntosh" (Kept)
            # Comma at 38 is "O"
            (40, 47, "PREP")  # "chopped" (Kept)
        ]
    }),

    # Example 44
    ("12 ounces (2 1/2 pints) firm fresh raspberries", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 9, "UNIT"),  # "ounces"
            (10, 23, "COMMENT"),  # "(2 1/2 pints)" (Kept)
            (24, 28, "PREP"),  # "firm" (from original NAME "firm fresh raspberries" 24-46)
            (29, 34, "PREP"),  # "fresh" (from original NAME 24-46)
            (35, 46, "NAME")  # "raspberries" (from original NAME 24-46)
        ]
    }),

    # Example 45
    ("1 tablespoon light-in-color oil, such as canola, safflower or peanut oil", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 27, "NAME"),  # "light-in-color" (from original NAME "light-in-color oil" 13-31)
            (28, 31, "NAME"),  # "oil" (from original NAME "light-in-color oil" 13-31)
            # Comma at 31 is "O"
            (33, 72, "ALT_NAME")  # "such as canola, safflower or peanut oil" (Kept)
        ]
    }),

    # Example 46
    ("3 1/2 ounces best-quality dark chocolate, bittersweet or semisweet, as preferred", {
        "entities": [
            (0, 5, "QTY"),  # "3 1/2" (Kept)
            (6, 12, "UNIT"),  # "ounces"
            (13, 25, "COMMENT"),  # "best-quality" (from original NAME "best-quality dark chocolate" 13-40)
            (26, 30, "NAME"),  # "dark" (from original NAME 13-40)
            (31, 40, "NAME"),  # "chocolate" (from original NAME 13-40)
            # Comma at 40 is "O"
            (42, 66, "ALT_NAME"),  # "bittersweet or semisweet" (Kept)
            # Comma at 66 is "O"
            (68, 80, "COMMENT")  # "as preferred" (Kept)
        ]
    }),

    # Example 47
    ("1 cup soft tofu, drained", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 10, "NAME"),  # "soft" (from original NAME "soft tofu" 6-15)
            (11, 15, "NAME"),  # "tofu" (from original NAME "soft tofu" 6-15)
            # Comma at 15 is "O"
            (17, 24, "PREP")  # "drained" (Kept)
        ]
    }),

    # Example 48 (Duplicate)

    # Example 49
    ("1 (15-ounce) can peach halves, juice reserved and peaches chopped", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "COMMENT"),  # "(15-ounce)" (Kept)
            (13, 16, "UNIT"),  # "can"
            (17, 22, "NAME"),  # "peach" (from original NAME "peach halves" 17-29)
            (23, 29, "NAME"),  # "halves" (from original NAME "peach halves" 17-29)
            # Comma at 29 is "O"
            (31, 65, "COMMENT")  # "juice reserved and peaches chopped" (Kept)
        ]
    }),

    # Example 50
    ("3 cups young, full-bodied red wine, such as Burgundy, Beaujolais, Cotes du Rhone, or Chianti", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 25, "PREP"),  # "young" (from original NAME "young, full-bodied red wine" 7-34)
            (26, 29, "NAME"),  # "red" (from NAME 7-34)
            (30, 34, "NAME"),  # "wine" (from NAME 7-34)
            # Comma at 34 is "O"
            (36, 92, "COMMENT")  # "such as Burgundy, Beaujolais, Cotes du Rhone, or Chianti" (Kept)
        ]
    }),

    # Example 51
    ("1/4 cup freshly grated Parmigiano-Reggiano", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "PREP"),  # "freshly" (from original NAME "freshly grated Parmigiano-Reggiano" 8-42)
            (16, 22, "NAME"),  # "grated" (from original NAME 8-42)
            (23, 42, "NAME")  # "Parmigiano-Reggiano" (from original NAME 8-42, tokenized as one)
        ]
    }),

    # Example 52
    ("1/3 cup plus 1 tablespoon lukewarm water", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 34, "COMMENT"),  # "plus 1 tablespoon" (Kept)
            (35, 40, "NAME")  # "water" (from original NAME "lukewarm water" 26-40)
        ]
    }),

    # Example 53
    ("1 double piecrust, such as Ina Garten's Perfect Pie Crust, recipe follows, or store-bought", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "NAME"),  # "double" (from original NAME "double piecrust" 2-17)
            (9, 17, "NAME"),  # "piecrust" (from original NAME "double piecrust" 2-17)
            # Comma at 17 is "O"
            (19, 90, "ALT_NAME"),
            # "such as Ina Garten's Perfect Pie Crust, recipe follows," (Kept, original includes comma)
        ]
    }),

    # Example 54
    ("12 tablespoons freshly ground coffee", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 14, "UNIT"),  # "tablespoons"
            (15, 22, "PREP"),  # "freshly" (from original NAME "freshly ground coffee" 15-36)
            (23, 29, "NAME"),  # "ground" (from original NAME 15-36)
            (30, 36, "NAME")  # "coffee" (from original NAME 15-36)
        ]
    }),

    # Example 55
    ("3 cups full-bodied dry white wine, such as white Burgundy, or a California Chardonnay", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 18, "PREP"),  # "full-bodied" (from original NAME "full-bodied dry white wine" 7-33)
            (19, 22, "NAME"),  # "dry" (from original NAME 7-33)
            (23, 28, "NAME"),  # "white" (from original NAME 7-33)
            (29, 33, "NAME"),  # "wine" (from original NAME 7-33)
            # Comma at 33 is "O"
            (35, 85, "COMMENT")  # "such as white Burgundy, or a California Chardonnay" (Kept)
        ]
    }),

    # Example 57
    ("2 tablespoons fat, reserved from the confit", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 17, "NAME"),  # "fat"
            # Comma at 17 is "O"
            (19, 43, "COMMENT")  # "reserved from the confit" (Kept)
        ]
    }),

    # Example 58
    ("1/4 cup prepared ranch dressing", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 16, "PREP"),  # "prepared" (Kept)
            (17, 22, "NAME"),  # "ranch" (from original NAME "ranch dressing" 17-31)
            (23, 31, "NAME")  # "dressing" (from original NAME "ranch dressing" 17-31)
        ]
    }),

    # Example 59
    ("25 grams (1/3 cup) medium-ground coffee", {
        "entities": [
            (0, 2, "QTY"),  # "25" (Kept)
            (3, 8, "UNIT"),  # "grams"
            (9, 18, "COMMENT"),  # "(1/3 cup)" (Kept)
            (19, 32, "NAME"),  # "medium-ground" (from original NAME "medium-ground coffee" 19-39)
            (33, 39, "NAME")  # "coffee" (from original NAME "medium-ground coffee" 19-39)
        ]
    }),

    # Example 60
    ("2 pounds well washed spinach", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 20, "PREP"),  # "well" (from original NAME "well washed spinach" 9-28)
            (21, 28, "NAME")  # "spinach" (from original NAME 9-28)
        ]
    }),

    # Example 61
    ("1/2 cup (a generous splash) dry white wine", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 27, "COMMENT"),  # "(a generous splash)" (Kept)
            (28, 31, "NAME"),  # "dry" (from original NAME "dry white wine" 28-42)
            (32, 37, "NAME"),  # "white" (from original NAME 28-42)
            (38, 42, "NAME")  # "wine" (from original NAME 28-42)
        ]
    }),

    # Example 62
    ("3/4 teaspoon tumeric", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 20, "NAME")  # "tumeric"
        ]
    }),

    # Example 63
    ("1 pound medium shell pasta", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 14, "NAME"),  # "medium" (from original NAME "medium shell pasta" 8-26)
            (15, 20, "NAME"),  # "shell" (from original NAME 8-26)
            (21, 26, "NAME")  # "pasta" (from original NAME 8-26)
        ]
    }),

    # Example 64
    ("1 1/4 pounds firm, slightly underripe fresh figs, rinsed, stems removed and halved", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/4" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 37, "PREP"),  # "firm" (from original NAME "firm, slightly underripe fresh figs" 13-48)
            (38, 43, "PREP"),  # "fresh" (from NAME 13-48)
            (44, 48, "NAME"),  # "figs" (from NAME 13-48)
            # Comma at 48 is "O"
            (50, 82, "PREP"),  # "rinsed" (from original PREP "rinsed, stems removed and halved" 50-82)
        ]
    }),

    # Example 65
    ("2 dashes bitters, (recommended: Angostura)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "COMMENT"),  # "dashes"
            (9, 16, "NAME"),  # "bitters"
            # Comma at 16 is "O"
            (18, 41, "COMMENT")  # "(recommended: Angostura)" (Kept)
        ]
    }),

    # Example 66
    ("1 small fowl (chicken, duck, Cornish hen - your favorite)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "small"
            (8, 12, "NAME"),  # "fowl"
            (13, 57, "COMMENT")  # "(chicken, duck, Cornish hen - your favorite)" (Kept)
        ]
    }),

    # Example 67
    ("6 tablespoons cocoa, Dutch processed", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 19, "NAME"),  # "cocoa"
            # Comma at 19 is "O"
            (21, 36, "COMMENT")  # "Dutch processed" (Kept)
        ]
    }),

    # Example 68
    ("4 sticks (1 pound butter) minus 1 heaping tablespoon, cut into chips and softened", {
        "entities": [
            (0, 8, "COMMENT"),  # "4" (Kept)
            (10, 11, "QTY"),  # "(1 pound butter)" (Kept, your original was (9,52) for whole phrase)
            (12, 17, "UNIT"),  # "(1 pound butter)" (Kept, your original was (9,52) for whole phrase)
            (18, 24, "UNIT"),  # "(1 pound butter)" (Kept, your original was (9,52) for whole phrase)
            (26, 52, "COMMENT"),  # "minus" (from original COMMENT (9,52))
            # Comma at 52 is "O"
            (54, 81, "PREP")  # "cut into chips and softened" (Kept)
        ]
    }),

    # Example 69
    ("4 tablespoons store bought peach, cranberry or mango chutney", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 26, "COMMENT"),  # "store" (from original NAME "store bought peach" 14-32)
            (27, 32, "NAME"),  # "peach" (from original NAME 14-32)
            # Comma at 32 is "O"
            (34, 43, "ALT_NAME"),  # "cranberry" (Kept, from original (34,60) "cranberry or mango chutney")
            (44, 60, "ALT_NAME"),  # "or" (from ALT_NAME 34-60) - *Unusual*
        ]
    }),

    # Example 70
    ("1 pound ground pork, chicken or turkey breast", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 14, "NAME"),  # "ground" (from original NAME "ground pork" 8-19)
            (15, 19, "NAME"),  # "pork" (from original NAME "ground pork" 8-19)
            # Comma at 19 is "O"
            (21, 28, "ALT_NAME"),  # "chicken" (from original ALT_NAME "chicken or turkey breast" 21-45)
            (29, 45, "ALT_NAME"),  # "or" (from ALT_NAME 21-45) - *Unusual*
        ]
    }),

    # Example 71
    ("1 pound fresh tagliatelle", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 13, "PREP"),  # "fresh" (from original NAME "fresh tagliatelle" 8-25)
            (14, 25, "NAME")  # "tagliatelle" (from original NAME "fresh tagliatelle" 8-25)
        ]
    }),

    # Example 72
    ("1 1/2 pounds rock shrimp, rinsed and picked through for shells", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 17, "NAME"),  # "rock" (from original NAME "rock shrimp" 13-24)
            (18, 24, "NAME"),  # "shrimp" (from original NAME "rock shrimp" 13-24)
            # Comma at 24 is "O"
            (26, 62, "PREP")  # "rinsed and picked through for shells" (Kept)
        ]
    }),

    # Example 73
    ("1/2 (8 ounces) multi-grain loaf, cut into 3/4-inch cubes", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 14, "COMMENT"),  # "(8 ounces)" (Kept)
            (15, 26, "NAME"),  # "multi-grain" (from original NAME "multi-grain loaf" 15-31)
            (27, 31, "NAME"),  # "loaf" (from original NAME "multi-grain loaf" 15-31)
            # Comma at 31 is "O"
            (33, 56, "PREP")  # "cut into 3/4-inch cubes" (Kept)
        ]
    }),

    # Example 74
    ("1/2 cup dried wood ear, re-hydrated and julienned (definitely fresh if available)", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "NAME"),  # "dried" (from original NAME "dried wood ear" 8-22)
            (14, 18, "NAME"),  # "wood" (from original NAME "dried wood ear" 8-22)
            (19, 22, "NAME"),  # "ear" (from original NAME "dried wood ear" 8-22)
            # Comma at 22 is "O"
            (24, 49, "PREP"),  # "re-hydrated and julienned" (Kept)
            (50, 81, "COMMENT")  # "(definitely fresh if available)" (Kept)
        ]
    }),

    # Example 75
    ("4 large, sturdy romaine-heart leaves, cut into 4-inch lengths (to resemble taco shells)", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 7, "NAME"),  # "large" (from original NAME "large, sturdy romaine-heart leaves" 2-36)
            (9, 15, "NAME"),  # "sturdy" (from NAME 2-36)
            (16, 29, "NAME"),  # "romaine-heart" (from NAME 2-36)
            (30, 36, "NAME"),  # "leaves" (from NAME 2-36)
            # Comma at 36 is "O"
            (38, 61, "PREP"),  # "cut into 4-inch lengths" (Kept)
            (62, 87, "COMMENT")  # "(to resemble taco shells)" (Kept)
        ]
    }),

    # Example 76
    ("1 cup small (about 1/4 inch) watermelon cubes", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 11, "NAME"),  # "small" (from original NAME "small (about 1/4 inch)watermelon cubes" 6-44)
            (12, 28, "COMMENT"),  # "(" (from NAME 6-44) - *Unusual*
            (29, 39, "NAME"),  # "watermelon" (from NAME 6-44)
            (40, 45, "NAME")  # "cubes" (from NAME 6-44, typo in original span end for "cubes")
        ]
    }),

    # Example 77
    ("1 cup freshly grated Parmigiano Reggiano cheese", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 13, "PREP"),  # "freshly" (from original NAME 6-47)
            (14, 20, "NAME"),  # "grated" (from original NAME 6-47)
            (21, 31, "NAME"),  # "Parmigiano" (from original NAME 6-47)
            (32, 40, "NAME"),  # "Reggiano" (from original NAME 6-47)
            (41, 47, "NAME")  # "cheese" (from original NAME 6-47)
        ]
    }),

    # Example 78
    ("1/2 cup homemade or store-bought ranch dressing", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 16, "ALT_NAME"),  # "homemade" (from original ALT_NAME "homemade or store-bought" 8-32)
            (17, 32, "ALT_NAME"),  # "or" (from ALT_NAME 8-32) - *Unusual*
            (33, 38, "NAME"),  # "ranch" (from original NAME "ranch dressing" 33-47)
            (39, 47, "NAME")  # "dressing" (from original NAME "ranch dressing" 33-47)
        ]
    }),

    # Example 79

    ("8 to 12 ounces skinless, boneless, chicken breasts, cut into 3/4 inch cubes", {  # If commas O
        "entities": [
            (0, 1, "QTY"),  # "8 to 12" (Kept)
            (2, 7, "PREP"),  # "8 to 12" (Kept)
            (8, 14, "UNIT"),
            (15, 23, "NAME"), (23, 24, "O"), (25, 33, "NAME"), (33, 34, "O"), (35, 42, "NAME"), (43, 50, "NAME"),
            (52, 75, "PREP")
        ]
    }),

    # Example 80
    ("1/2 cup of a mustard vinaigrette", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "O"),  # "of" - This was not part of your original NAME span for "mustard vinaigrette"

            (13, 20, "NAME"),  # "mustard" (from original NAME "mustard vinaigrette" 13-32)
            (21, 32, "NAME")  # "vinaigrette" (from original NAME "mustard vinaigrette" 13-32)
        ]
    }),

    # Example 81

    ("1 tablespoon toasted and ground cumin seed", {  # If toasted/ground are PREP
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"),
            (13, 31, "PREP"),  # toasted
            (32, 37, "NAME"), (38, 42, "NAME")  # cumin seed
        ]
    }),

    # Example 82
    ("2 tablespoons cooked and crispy wontons, for garnish", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 24, "PREP"),  # "cooked" (from original NAME "cooked and crispy wontons" 25-39, span issue)

            (25, 31, "NAME"),  # "crispy"
            (32, 39, "NAME"),  # "wontons"
            # Comma at 39 is "O"
            (41, 52, "COMMENT")  # "for garnish" (Kept)
        ]
    }),

    # Example 83
    ("12 thin slices, prosciutto", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 7, "PREP"),  # "thin" (from original PREP "thin slices" 3-14)
            (8, 14, "PREP"),  # "slices" (from original PREP "thin slices" 3-14)
            # Comma at 14 is "O"
            (16, 26, "NAME")  # "prosciutto"
        ]
    }),

    # Example 84
    ("1 clove of garlic, minced (about 1/2 teaspoon)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "NAME"),  # "clove" (from original NAME "clove of garlic" 2-17)
            (8, 10, "NAME"),  # "of" (from original NAME 2-17) - *Unusual*
            (11, 17, "NAME"),  # "garlic" (from original NAME 2-17)
            # Comma at 17 is "O"
            (19, 25, "PREP"),  # "minced" (Kept)
            (26, 46, "COMMENT")  # "(about 1/2 teaspoon)" (Kept)
        ]
    }),

    # Example 85

    ("1/2 cup peeled, steamed, and mashed taro root", {  # Cleaner interpretation
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (8, 14, "PREP"),  # peeled
            # Comma O
            (16, 23, "PREP"),  # steamed
            # Comma O, "and" O
            (29, 35, "PREP"),  # mashed
            (36, 40, "NAME"), (41, 45, "NAME")  # taro root
        ]
    }),

    # Example 86
    ("3 or 4 anchovy filets, minced", {
        "entities": [
            (0, 1, "QTY"),  # "3 or 4" (Kept)
            (2, 6, "COMMENT"),  # "3 or 4" (Kept)
            (7, 14, "NAME"),  # "anchovy" (from original NAME "anchovy filets" 7-21)
            (15, 21, "NAME"),  # "filets" (from original NAME "anchovy filets" 7-21)
            # Comma at 21 is "O"
            (23, 29, "PREP")  # "minced" (Kept)
        ]
    }),

    # Example 87
    ("1/2 cup prepared or bottled ranch dressing", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 27, "PREP"),  # "prepared" (Kept from (8,16,"PREP"))
            (28, 33, "NAME"),  # "ranch"
            (34, 42, "NAME")  # "dressing"
        ]
    }),

    # Example 88
    ("3/4 cup warm water (105 to 115 degrees F)", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "COMMENT"),  # "warm" (from original NAME "warm water" 13-18 - typo in span?)
            # Assuming (8,12,"NAME") for "warm" and (13,18,"NAME") for "water"
            (13, 18, "NAME"),  # "water"
            (19, 41, "COMMENT")  # "(105 to 115 degrees F)" (Kept)
        ]
    }),

    # Example 89
    ("1 package (10 ounces) frozen peas and carrots", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 9, "UNIT"),  # "package"
            (10, 21, "COMMENT"),  # "(10 ounces)" (Kept)
            (22, 28, "NAME"),  # "frozen" (from original NAME "frozen peas and carrots" 22-45)
            (29, 33, "NAME"),  # "peas" (from original NAME 22-45)
            (34, 37, "NAME"),  # "and" (from original NAME 22-45) - *Unusual*
            (38, 45, "NAME")  # "carrots" (from original NAME 22-45)
        ]
    }),

    # Example 90
    ("1 1/4 ounces (36 grams) trimoline", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/4" (Kept)
            (6, 12, "UNIT"),  # "ounces"
            (13, 23, "COMMENT"),  # "(36 grams)" (Kept)
            (24, 33, "NAME")  # "trimoline"
        ]
    }),

    # Example 91
    ("3/4 cup (1 1/2 sticks) cold, unsalted butter, cut into small chunks", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 22, "COMMENT"),  # "(1 1/2 sticks)" (Kept)
            (23, 27, "PREP"),  # "cold" (Kept)
            # Comma at 27 is "O"
            (29, 37, "NAME"),  # "unsalted" (from original NAME "unsalted butter" 29-44)
            (38, 44, "NAME"),  # "butter" (from original NAME "unsalted butter" 29-44)
            # Comma at 44 is "O"
            (46, 67, "PREP")  # "cut into small chunks" (Kept)
        ]
    }),

    # Example 92
    ("3 1/2 to 4 cups cooked and cooled barley", {
        "entities": [
            (0, 5, "QTY"),  # "3 1/2 to 4" (Kept)
            (6, 10, "QTY"),  # "3 1/2 to 4" (Kept)
            (11, 15, "UNIT"),  # "cups"
            (16, 22, "NAME"),  # "cooked" (from original NAME "cooked and cooled barley" 16-40)
            (23, 26, "NAME"),  # "and" (from original NAME 16-40) - *Unusual*
            (27, 33, "NAME"),  # "cooled" (from original NAME 16-40)
            (34, 40, "NAME")  # "barley" (from original NAME 16-40)
        ]
    }),

    # Example 93
    ("4 pieces, about 4 inches long, lemongrass stalks", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 29, "COMMENT"),  # "pieces" (Original label was UNIT)
            # Comma at 29 is "O"
            (31, 41, "NAME"),  # "lemongrass" (from original NAME "lemongrass stalks" 31-48)
            (42, 48, "NAME")  # "stalks" (from original NAME "lemongrass stalks" 31-48)
        ]
    }),

    # Example 94

    ("1 #10 can, filled with water*", {  # If "filled with" is PREP
        "entities": [
            (0, 1, "QTY"), (2, 5, "COMMENT"), (6, 9, "UNIT"),
            (11, 17, "PREP"), (18, 22, "PREP"),  # filled, with
            (23, 29, "NAME")  # water*
        ]
    }),

    # Example 95
    ("1/3 cup homemade or purchased marinara sauce", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 29, "COMMENT"),  # "homemade or purchased" (Kept as original COMMENT span, not ALT_NAME)
            (30, 38, "NAME"),  # "marinara" (from original NAME "marinara sauce" 30-44)
            (39, 44, "NAME")  # "sauce" (from original NAME "marinara sauce" 30-44)
        ]
    }),

    # Example 96

    ("1 tablespoon Raita, recipe follows, plus more for serving", {  # If (20,57) was one comment
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"), (13, 18, "NAME"),
            (20, 57, "COMMENT")
        ]
    }),

    # Example 97
    ("1 tablespoon crushed coffee beans (crushed with a rolling pin or the bottom of a heavy pot)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 20, "NAME"),  # "crushed" (from original NAME "crushed coffee beans" 13-33)
            (21, 27, "NAME"),  # "coffee" (from original NAME 13-33)
            (28, 33, "NAME"),  # "beans" (from original NAME 13-33)
            (34, 91, "COMMENT")  # "(crushed with a rolling pin or the bottom of a heavy pot)" (Kept)
        ]
    }),

    # Example 98
    ("2 cups whole, 2 percent fat, or 1 percent fat milk", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 12, "NAME"),  # "whole" (Kept from original (7,28,"ALT_NAME") "whole, 2 percent fat,")
            (14, 27, "ALT_NAME"),  # "2" (from ALT_NAME 7-28)
            (29, 45, "ALT_NAME"),  # "or"
            (46, 50, "NAME")  # "milk" (from original NAME 32-50)
        ]
    }),

    # Example 99
    ("1 can whole water chestnuts", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "can"
            (6, 11, "NAME"),  # "whole" (from original NAME "whole water chestnuts" 6-27)
            (12, 17, "NAME"),  # "water" (from original NAME 6-27)
            (18, 27, "NAME")  # "chestnuts" (from original NAME 6-27)
        ]
    }),

    # Example 100
    ("1 (28-ounce) can fire-roasted diced or crushed tomatoes", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "COMMENT"),  # "(28-ounce)" (Kept)
            (13, 16, "UNIT"),  # "can"
            (17, 35, "NAME"),  # "fire-roasted" (Original ALT_NAME was (17,35) "fire-roasted diced")
            (36, 46, "ALT_NAME"),  # "or"
            (47, 55, "NAME")  # "tomatoes" (from original NAME "crushed tomatoes" 39-55)
        ]
    }),

    # Example 101

    ("1/4 cup roasted, unsalted peanuts, roughly chopped", {  # If commas in NAME are O
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (8, 15, "NAME"), (15, 16, "O"), (17, 25, "NAME"), (26, 33, "NAME"),
            (35, 50, "PREP")
        ]
    }),

    # Example 102
    ("4 large, ripe, unpeeled bananas", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 7, "UNIT"),  # "large"
            # Comma at 7 is "O"
            (9, 23, "COMMENT"),  # "ripe, unpeeled" (Kept, includes comma)
            (24, 31, "NAME")  # "bananas"
        ]
    }),

    # Example 103
    ("1/3 cup lowfat plain yogurt", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "NAME"),  # "lowfat" (from original NAME "lowfat plain yogurt" 8-27)
            (15, 20, "NAME"),  # "plain" (from original NAME "lowfat plain yogurt" 8-27)
            (21, 27, "NAME")  # "yogurt" (from original NAME "lowfat plain yogurt" 8-27)
        ]
    }),

    # Example 104
    ("1 1/2 cups warm water (about 110˚ F)", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 15, "COMMENT"),  # "warm" (from original NAME "warm water" 11-21)
            (16, 21, "NAME"),  # "water" (from original NAME "warm water" 11-21)
            (22, 36, "COMMENT")  # "(about 110˚ F)" (Kept)
        ]
    }),

    # Example 105 - Your "4 to 6" was previously QTY.
    # If you want "4" QTY and "to 6" ALT_NAME:
    ("4 to 6 orange slices, for garnish", {
        "entities": [
            (0, 1, "QTY"),  # "4"
            (2, 6, "ALT_QTY"),  # "to 6" (New rule: "to 8" as prep or alt_name)
            (7, 13, "NAME"),  # "orange" (from original NAME "orange slices" 7-20)
            (14, 20, "NAME"),  # "slices" (from original NAME "orange slices" 7-20)
            # Comma at 20 is "O"
            (22, 33, "COMMENT")  # "for garnish" (Kept)
        ]
    }),  # This follows your new specific instruction for ranges.

    # Example 106
    ("1 cup non-carbonated spring water", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 20, "NAME"),  # "non-carbonated" (from original NAME "non-carbonated spring water" 6-33)
            (21, 27, "NAME"),  # "spring" (from original NAME 6-33)
            (28, 33, "NAME")  # "water" (from original NAME 6-33)
        ]
    }),

    # Example 107
    ('4 teaspoons 151 "proof" rum', {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 11, "UNIT"),  # "teaspoons"
            (12, 15, "NAME"),  # "151" (from original NAME '151 "proof" rum' 12-27)
            (16, 23, "NAME"),  # '"proof"' (from original NAME 12-27, includes quotes)
            (24, 27, "NAME")  # "rum" (from original NAME 12-27)
        ]
    }),

    # Example 108
    ("1 loaf, 24 inches or longer, crusty bread", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 6, "PREP"),  # "loaf" (Kept)
            # Comma at 6 is "O"
            (8, 27, "COMMENT"),  # "24 inches or longer" (Kept)
            # Comma at 27 is "O"
            (29, 35, "NAME"),  # "crusty" (from original NAME "crusty bread" 29-41)
            (36, 41, "NAME")  # "bread" (from original NAME "crusty bread" 29-41)
        ]
    }),

    # Example 109 (Corresponds to original error: EXAMPLE 1112)
    ("3/4 cup pre-cooked dark Puy lentils", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 18, "PREP"),  # "pre-cooked" (from original NAME "pre-cooked dark Puy lentils" 8-35)
            (19, 23, "NAME"),  # "dark" (from original NAME 8-35)
            (24, 27, "NAME"),  # "Puy" (from original NAME 8-35)
            (28, 35, "NAME")  # "lentils" (from original NAME 8-35)
        ]
    }),

    # Example 110
    ("1/4 cup millet", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "NAME")  # "millet"
        ]
    }),

    # Example 111
    ("1 sour pickle, cut into 8 slices, plus 1 tablespoon pickle juice from the jar", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 6, "NAME"),  # "sour" (from original NAME "sour pickle" 2-13)
            (7, 13, "NAME"),  # "pickle" (from original NAME "sour pickle" 2-13)
            # Comma at 13 is "O"
            (15, 32, "PREP"),  # "cut into 8 slices" (Kept)
            # Comma at 32 is "O"
            (34, 73, "COMMENT")  # "plus 1 tablespoon pickle juice from the jar" (Kept)
        ]
    }),

    ("4 to 5 cups, 2 bundles, dandelion greens, stemmed and chopped", {  # If "to 5" is ALT_NAME
        "entities": [
            (0, 1, "QTY"),  # "4"
            (2, 6, "ALT_QTY"),  # "to 5" (if that's the desired parsing for range)
            (7, 11, "UNIT"), (13, 22, "COMMENT"),
            (24, 33, "NAME"), (34, 40, "NAME"),
            (42, 61, "PREP")
        ]
    }),

    # Example 113
    ("1 1/2 pounds malanga, peeled and cut into 1/2-inch dice", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 20, "NAME"),  # "malanga"
            # Comma at 20 is "O"
            (22, 55, "PREP")  # "peeled and cut into 1/2-inch dice" (Kept)
        ]
    }),

    # Example 114
    ("3 1/2 cups brewed coffee", {
        "entities": [
            (0, 5, "QTY"),  # "3 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 17, "NAME"),  # "brewed" (from original NAME "brewed coffee" 11-24)
            (18, 24, "NAME")  # "coffee" (from original NAME "brewed coffee" 11-24)
        ]
    }),

    # Example 115 (Corresponds to original error: EXAMPLE 1118)
    ("10 cups, plus 4 cups water", {
        "entities": [
            (0, 2, "QTY"),  # "10" (Kept)
            (3, 7, "UNIT"),  # "cups"
            # Comma at 7 is "O"
            (9, 20, "COMMENT"),  # "plus 4 cups" (Kept)
            (21, 26, "NAME")  # "water"
        ]
    }),

    # Example 116
    ("4 cups unsalted raw macadamias", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 15, "NAME"),  # "unsalted" (from original NAME "unsalted raw macadamias" 7-30)
            (16, 19, "NAME"),  # "raw" (from original NAME 7-30)
            (20, 30, "NAME")  # "macadamias" (from original NAME 7-30)
        ]
    }),

    # Example 117 (Corresponds to original error: EXAMPLE 1120)
    ("3/4 cup homemade or purchased marinara sauce, recipe follows", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 29, "ALT_NAME"),  # "homemade or purchased" (Kept)
            (30, 38, "NAME"),  # "marinara" (from original NAME "marinara sauce" 30-44)
            (39, 44, "NAME"),  # "sauce" (from original NAME "marinara sauce" 30-44)
            # Comma at 44 is "O"
            (46, 60, "COMMENT")  # "recipe follows" (Kept)
        ]
    }),
    # Re-annotated data based on the FINAL REFINED rules:
    # - NAME entities are broken into word-level NAME entities.
    # - COMMENT, PREP, ALT_NAME, QTY entities are kept as single, original spans.
    # - UNIT entities are single words.
    # - Parentheses are NOT entities themselves unless they are part of a COMMENT/PREP/ALT_NAME/QTY span.
    # - Commas and other unspanned words become "O" (and are thus not listed in the 'entities' list).
    # - Ranges like "X to Y" for QTY: If your original QTY span was "X to Y", it's kept.
    #   If your original was "X" QTY and "to Y" ALT_NAME/COMMENT, that specific instruction will be followed.
    # - "or" in ALT_NAME: Kept as part of the ALT_NAME span if it was originally included.
    # Tokenization based on spaCy's default English tokenizer.

    # ... (all previous examples from your earlier chunks would be here) ...

    # Example 1
    ("6 habaneros, sliced", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 11, "NAME"),  # "habaneros"
            # Comma at 11 is "O"
            (13, 19, "PREP")  # "sliced" (Kept)
        ]
    }),

    # Example 2
    ("1 pig's foot with shank attached", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "NAME"),  # "pig's" (from original NAME "pig's foot" 2-12)
            (8, 12, "NAME"),  # "foot" (from original NAME "pig's foot" 2-12)
            (13, 32, 'COMMENT')  # "with shank attached" (Kept)
        ]
    }),

    # Example 3
    ("1 recipe Stuffing, recipe follows", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "COMMENT"),  # "recipe"
            (9, 17, "NAME"),  # "Stuffing"
            # Comma at 17 is "O"
            (19, 33, "COMMENT")  # "recipe follows" (Kept)
        ]
    }),

    # Example 4 (Corresponds to original error: EXAMPLE 1124)
    ("2 cups champagne", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 16, "NAME")  # "champagne"
        ]
    }),

    # Example 5
    ("4 whole cinnamon sticks", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 7, "NAME"),  # "whole" (from original NAME "whole cinnamon sticks" 2-23)
            (8, 16, "NAME"),  # "cinnamon" (from original NAME 2-23)
            (17, 23, "NAME")  # "sticks" (from original NAME 2-23)
        ]
    }),

    # Example 6 (Corresponds to original error: EXAMPLE 1126)
    ("1/2 cup chopped pitted good quality olives", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 35, "PREP"),  # "chopped" (from original NAME "chopped pitted good quality olives" 8-42)
            (36, 42, "NAME")  # "olives" (from original NAME 8-42)
        ]
    }),

    # Example 7 (Corresponds to original error: EXAMPLE 1127)

    ("22 ounces dried, refrigerated or frozen naengmyeon noodles (see Cook’s Note)",
     {  # If "noodles" is NAME, comment is just parens content
         "entities": [
             (0, 2, "QTY"), (3, 9, "UNIT"), (10, 39, "PREP"),
             (40, 50, "NAME"),  # naengmyeon
             (51, 58, "NAME"),  # noodles (Token "noodles" is 51-58)
             (59, 76, "COMMENT")  # "(see Cook’s Note)" (Token "(" is 59-60, ")" is 75-76)
         ]
     }),

    # Example 8
    ("2/3 cup warm water (105 to 110 degrees F)", {
        "entities": [
            (0, 3, "QTY"),  # "2/3" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "COMMENT"),  # "warm" (Kept as original COMMENT span)
            (13, 18, "NAME"),  # "water"
            (19, 41, "COMMENT")  # "(105 to 110 degrees F)" (Kept)
        ]
    }),

    # Example 9
    ("2 large free-range or organic eggs, beaten", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 7, "UNIT"),  # "large"
            (8, 29, "ALT_NAME"),  # "free-range or organic" (Kept)
            (30, 34, "NAME"),  # "eggs"
            # Comma at 34 is "O"
            (36, 42, "PREP")  # "beaten" (Kept)
        ]
    }),

    # Example 10
    ("1 1/2 cup fine quality semi-sweet chocolate, chopped", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 9, "UNIT"),  # "cup"
            (10, 14, "PREP"),  # "fine" (from original PREP "fine quality" 10-22)
            (15, 22, "PREP"),  # "quality" (from original PREP "fine quality" 10-22)
            (23, 33, "NAME"),  # "semi-sweet" (from original NAME "semi-sweet chocolate" 23-43)
            (34, 43, "NAME"),  # "chocolate" (from original NAME "semi-sweet chocolate" 23-43)
            # Comma at 43 is "O"
            (45, 52, "PREP")  # "chopped" (Kept)
        ]
    }),

    ("1/3 cup or so mustard vinaigrette (2 teaspoons mustard, 1 tablespoon red wine vinegar and 1/3 cup olive oil, whisked together)",
     {  # If original comment included parens
         "entities": [
             (0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "COMMENT"),
             (14, 21, "NAME"), (22, 33, "NAME"),
             (34, 125, "COMMENT")
         ]
     }),

    # Example 12
    ("1 cup strawberry smoothie (recommended: Naked Juice)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 16, "NAME"),  # "strawberry" (from original NAME "strawberry smoothie" 6-25)
            (17, 25, "NAME"),  # "smoothie" (from original NAME "strawberry smoothie" 6-25)
            (26, 52, "COMMENT")  # "(recommended: Naked Juice)" (Kept)
        ]
    }),

    # Example 13
    ("4 small strip steaks 1 to 1 1/2-inches thick", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 7, "UNIT"),  # "small"
            (8, 13, "NAME"),  # "strip" (from original NAME "strip steaks" 8-20)
            (14, 20, "NAME"),  # "steaks" (from original NAME "strip steaks" 8-20)
            (21, 44, "COMMENT")  # "1 to 1 1/2-inches thick" (Kept)
        ]
    }),

    # Example 14
    ("4 slices or wedges ruby grapefruit", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "PREP"),  # "slices" (Kept)
            (9, 18, "ALT_NAME"),  # "or wedges" (Kept)
            (19, 23, "NAME"),  # "ruby" (from original NAME "ruby grapefruit" 19-34)
            (24, 34, "NAME")  # "grapefruit" (from original NAME "ruby grapefruit" 19-34)
        ]
    }),

    # Example 15
    ("10 lollipops", {
        "entities": [
            (0, 2, "QTY"),  # "10" (Kept)
            (3, 12, "NAME")  # "lollipops"
        ]
    }),

    # Example 16

    ("1 tablespoon, a palm full, grill seasoning blend (recommended: Montreal Steak Seasoning by McCormick)",
     {  # If comment included parens
         "entities": [
             (0, 1, "QTY"), (2, 12, "UNIT"), (14, 26, "COMMENT"),
             (27, 32, "NAME"), (33, 42, "NAME"), (43, 48, "NAME"),
             (49, 100, "COMMENT")
         ]
     }),

    # Example 17
    ("8 cups warm water (105 to 115 degrees F)", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 11, "COMMENT"),  # "warm" (Kept as original COMMENT)
            (12, 17, "NAME"),  # "water"
            (18, 40, "COMMENT")  # "(105 to 115 degrees F)" (Kept)
        ]
    }),

    # Example 18

    ("1/2 cup grated, good quality Parmesan cheese", {  # If commas in PREP are O
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (8, 14, "PREP"),  # grated
            # Comma O
            (16, 20, "PREP"), (21, 28, "PREP"),  # good, quality
            (29, 37, "NAME"), (38, 44, "NAME")
        ]
    }),

    # Example 19
    ("Three 6 1/2-ounce cans minced or whole clams", {
        "entities": [
            (0, 5, "QTY"),  # "Three" (Kept)
            (6, 17, "COMMENT"),  # "6 1/2-ounce" (Kept)
            (18, 22, "UNIT"),  # "cans"
            (23, 29, "PREP"),  # "minced" (Kept)
            (30, 38, "ALT_NAME"),  # "or whole" (Kept)
            (39, 44, "NAME")  # "clams"
        ]
    }),

    # Example 20

    ("3 ounces pitted, brined, black olives", {  # If commas in PREP are O
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"),
            (9, 15, "PREP"),  # pitted
            # Comma O
            (17, 23, "PREP"),  # brined
            # Comma O
            (25, 30, "NAME"), (31, 37, "NAME")
        ]
    }),

    # Example 21
    ("4 petrale fillets, with skin on", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 9, "NAME"),  # "petrale" (from original NAME "petrale fillets" 2-17)
            (10, 17, "NAME"),  # "fillets" (from original NAME "petrale fillets" 2-17)
            # Comma at 17 is "O"
            (19, 31, "COMMENT")  # "with skin on" (Kept)
        ]
    }),

    # Example 22
    ("3/4 cup warm water (180 milliliters)", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "COMMENT"),  # "warm" (Kept original COMMENT)
            (13, 18, "NAME"),  # "water"
            (19, 35, "COMMENT")  # "(180 milliliters)" (Kept)
        ]
    }),

    # Example 23
    ("4 medium sized yucas, peeled and cut into 1 1/2-inch pieces, or 1 pack frozen yuca", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "UNIT"),  # "medium"
            (9, 14, "PREP"),  # "sized" (Kept)
            (15, 20, "NAME"),  # "yucas"
            # Comma at 20 is "O"
            (22, 59, "PREP"),  # "peeled and cut into 1 1/2-inch pieces" (Kept)
            # Comma at 59 is "O"
            (61, 82, "ALT_NAME")  # "or 1 pack frozen yuca" (Kept)
        ]
    }),

    # Example 24
    ("2 cups channa dal, see Cook's Note*", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 13, "NAME"),  # "channa" (from original NAME "channa dal" 7-17)
            (14, 17, "NAME"),  # "dal" (from original NAME "channa dal" 7-17)
            # Comma at 17 is "O"
            (19, 35, "COMMENT")  # "see Cook's Note*" (Kept)
        ]
    }),

    # Example 25
    ("1 large poblano chile pepper", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "large"
            (8, 15, "NAME"),  # "poblano" (from original NAME "poblano chile pepper" 8-28)
            (16, 21, "NAME"),  # "chile" (from original NAME 8-28)
            (22, 28, "NAME")  # "pepper" (from original NAME 8-28)
        ]
    }),

    # Example 26

    ("3 1/4 cups whole, 2 percent fat, or 1 percent fat milk", {  # If commas in ALT_NAME are O
        "entities": [
            (0, 5, "QTY"), (6, 10, "UNIT"),
            (11, 16, "NAME"),  # "whole"
            # Comma O
            (18, 31, "ALT_NAME"),
            # Comma O, "or" O
            (36, 49, "ALT_NAME"), (50, 54, "NAME")  # 1 percent fat milk
        ]
    }),

    # Example 27
    ("1 tablespoon brewed coffee", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 19, "NAME"),  # "brewed" (from original NAME "brewed coffee" 13-26)
            (20, 26, "NAME")  # "coffee" (from original NAME "brewed coffee" 13-26)
        ]
    }),

    # Example 28
    ("1/2 cup finely chopped cornicho", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "finely" (from original PREP "finely chopped" 8-22)
            (15, 22, "PREP"),  # "chopped" (from original PREP "finely chopped" 8-22)
            (23, 31, "NAME")  # "cornicho"
        ]
    }),

    # Example 29
    ("4 (10-ounce fillets)", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 11, "COMMENT"),  # "(10-ounce" (Kept, original span ended before closing parenthesis)
            (12, 19, "NAME")  # "fillets"
            # ")" at 19 is "O"
        ]
    }),

    # Example 30

    ("1 teaspoon gochugaru or more if desired, optional", {  # If optional is separate COMMENT
        "entities": [
            (0, 1, "QTY"), (2, 10, "UNIT"), (11, 20, "NAME"),
            (21, 49, "COMMENT"),  # "or more if desired,"
        ]
    }),

    # Example 31 (Duplicate)
    ("1 clove of garlic, minced (about 1/2 teaspoon)", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "NAME"), (8, 10, "NAME"), (11, 17, "NAME"),  # clove of garlic
            (19, 25, "PREP"), (26, 46, "COMMENT")
        ]
    }),

    # Example 32
    ("1 tablespoon dill pickle brine, plus pickle slices, for serving", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 17, "NAME"),  # "dill" (from original NAME "dill pickle brine" 13-30)
            (18, 24, "NAME"),  # "pickle" (from original NAME 13-30)
            (25, 30, "NAME"),  # "brine" (from original NAME 13-30)
            # Comma at 30 is "O"
            (32, 63, "COMMENT")  # "plus pickle slices, for serving" (Kept)
        ]
    }),

    # Example 33 (Duplicate)
    ("8 to 12 ounces skinless, boneless, chicken breasts, cut into 3/4 inch cubes", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "ALT_QTY"),
            (8, 14, "UNIT"),
            (15, 23, "NAME"), (23, 24, "O"), (25, 33, "NAME"), (33, 34, "O"), (35, 42, "NAME"), (43, 50, "NAME"),
            # skinless, boneless, chicken breasts
            (52, 75, "PREP")
        ]
    }),

    # Example 34
    ("1/3 cup double-strength hot brewed coffee", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 23, "PREP"),  # "double-strength" (Kept from original (8,27) "double-strength hot")
            (24, 27, "PREP"),  # "hot" (from original PREP (8,27))
            (28, 34, "NAME"),  # "brewed" (from original NAME "brewed coffee" 28-41)
            (35, 41, "NAME")  # "coffee" (from original NAME "brewed coffee" 28-41)
        ]
    }),

    # Example 35
    ("12 medium, peeled asparagus", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 9, "UNIT"),  # "medium"
            # Comma at 9 is "O"
            (11, 17, "PREP"),  # "peeled" (Kept)
            (18, 27, "NAME")  # "asparagus"
        ]
    }),

    # Example 36
    ("1/2 cup grated or finely ground Parmigiano-Reggiano", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "NAME"),  # "grated" (Kept)
            (15, 31, "ALT_NAME"),  # "or finely ground" (Kept)
            (32, 51, "NAME")  # "Parmigiano-Reggiano" (tokenized as one)
        ]
    }),

    # Example 37
    ("4 cups store-bought meringues, lightly crushed", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 19, "PREP"),  # "store-bought" (Kept)
            (20, 29, "NAME"),  # "meringues"
            # Comma at 29 is "O"
            (31, 38, "PREP"),  # "lightly" (from original PREP "lightly crushed" 31-46)
            (39, 46, "PREP")  # "crushed" (from original PREP "lightly crushed" 31-46)
        ]
    }),

    # Example 38
    ("1/2 cup quick cook oats", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "NAME"),  # "quick" (from original NAME "quick cook oats" 8-23)
            (14, 18, "NAME"),  # "cook" (from original NAME 8-23)
            (19, 23, "NAME")  # "oats" (from original NAME 8-23)
        ]
    }),

    # Example 39
    ("9 ounces minced beef and pork, equal amounts", {
        "entities": [
            (0, 1, "QTY"),  # "9" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 15, "PREP"),  # "minced" (Kept)
            (16, 29, "NAME"),  # "beef"
            # Comma at 29 is "O"
            (31, 44, "COMMENT")  # "equal amounts" (Kept)
        ]
    }),

    # Example 40
    ("4 medium soft-shell crabs, cleaned and rinsed", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "UNIT"),  # "medium"
            (9, 19, "NAME"),  # "soft-shell" (from original NAME "soft-shell crabs" 9-25)
            (20, 25, "NAME"),  # "crabs" (from original NAME "soft-shell crabs" 9-25)
            # Comma at 25 is "O"
            (27, 45, "PREP"),  # "cleaned" (from original PREP "cleaned and rinsed" 27-45)
        ]
    }),

    # Example 41
    ("2 1/4 pounds 90% lean ground beef (such as sirloin)", {
        "entities": [
            (0, 5, "QTY"),  # "2 1/4" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 21, "NAME"),  # "90% lean" (Kept)
            (22, 28, "NAME"),  # "ground" (from original NAME "ground beef" 22-33)
            (29, 33, "NAME"),  # "beef" (from original NAME "ground beef" 22-33)
            (34, 51, "COMMENT")  # "(such as sirloin)" (Kept)
        ]
    }),

    # Example 42
    ("8 mahi mahi fillets, 5 to 6 ounces each", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 11, "NAME"),  # "mahi" (from original NAME "mahi mahi fillets" 2-19)
            (12, 19, "NAME"),  # "fillets" (from original NAME 2-19)
            # Comma at 19 is "O"
            (21, 39, "COMMENT")  # "5 to 6 ounces each" (Kept)
        ]
    }),

    # Example 43
    ("1/4 cup (25 grams) gochugaru (Korean red pepper flakes)", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 18, "COMMENT"),  # "(25 grams)" (Kept)
            (19, 28, "NAME"),  # "gochugaru"
            (29, 55, "COMMENT")  # "(Korean red pepper flakes)" (Kept)
        ]
    }),

    # Example 44
    ("12 tablespoons (1 1/2 sticks) cold, unsalted butter", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 14, "UNIT"),  # "tablespoons"
            (15, 29, "COMMENT"),  # "(1 1/2 sticks)" (Kept)
            (30, 34, "PREP"),  # "cold" (Kept)
            # Comma at 34 is "O"
            (36, 44, "NAME"),  # "unsalted" (from original NAME "unsalted butter" 36-51)
            (45, 51, "NAME")  # "butter" (from original NAME "unsalted butter" 36-51)
        ]
    }),

    # Example 45
    ("1/4 pound sliced American cheese", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 16, "PREP"),  # "sliced" (Kept)
            (17, 25, "NAME"),  # "American" (from original NAME "American cheese" 17-32)
            (26, 32, "NAME")  # "cheese" (from original NAME "American cheese" 17-32)
        ]
    }),

    # Example 46
    ("1 tablespoon brine, reserved from pimento jar", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 18, "NAME"),  # "brine"
            # Comma at 18 is "O"
            (20, 45, "COMMENT")  # "reserved from pimento jar" (Kept)
        ]
    }),

    # Example 47
    ("One 17-ounce package gnocchi", {
        "entities": [
            (0, 3, "QTY"),  # "One" (Kept)
            (4, 12, "COMMENT"),  # "17-ounce" (Kept)
            (13, 20, "UNIT"),  # "package"
            (21, 28, "NAME")  # "gnocchi"
        ]
    }),

    # Example 48
    ("4 4-inch cinnamon sticks, broken", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "COMMENT"),  # "4-inch" (Kept)
            (9, 17, "NAME"),  # "cinnamon" (from original NAME "cinnamon sticks" 9-24)
            (18, 24, "NAME"),  # "sticks" (from original NAME "cinnamon sticks" 9-24)
            # Comma at 24 is "O"
            (26, 32, "PREP")  # "broken" (Kept)
        ]
    }),

    # Example 49
    ("1/4 cup finely chopped good-quality ham", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "finely" (Kept)
            (15, 22, "NAME"),  # "chopped" (Original label was NAME)
            (23, 35, "PREP"),  # "good-quality" (Kept)
            (36, 39, "NAME")  # "ham"
        ]
    }),

    # Example 50 (Corresponds to original error: EXAMPLE 1168)
    ("3 or 4 anchovy fillets", {
        "entities": [
            (0, 6, "QTY"),  # "3 or 4" (Kept)
            (7, 14, "NAME"),  # "anchovy"
            (15, 22, "NAME")  # "fillets"
        ]
    }),

    # Example 51
    ("1 cup sliced-on-the-diagonal asparagus", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 28, "PREP"),  # "sliced-on-the-diagonal" (Kept)
            (29, 38, "NAME")  # "asparagus"
        ]
    }),

    # Example 52
    ("2 1/4 pounds lean, trimmed stewing beef, such as round eye, and/or pork tenderloin", {
        "entities": [
            (0, 5, "QTY"),  # "2 1/4" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 26, "PREP"),  # "lean" (Kept from original (13,26,"PREP") "lean, trimmed")
            (27, 34, "NAME"),  # "stewing" (from original NAME "stewing beef" 27-39)
            (35, 39, "NAME"),  # "beef" (from original NAME "stewing beef" 27-39)
            # Comma at 39 is "O"
            (41, 58, "COMMENT"),  # "such as round eye," (Kept, includes comma)
            (60, 82, "ALT_NAME")  # "and/or pork tenderloin" (Kept)
        ]
    }),

    # Example 53
    ("Generous handful (approx. 2 ounces) of plain tortilla chips", {
        "entities": [
            (0, 16, "COMMENT"),  # "Generous handful" (Your original label was COMMENT for this part)
            # Token '(' at 17 is O
            (18, 25, "COMMENT"),  # "approx. " (The part of the comment before QTY/UNIT)
            (26, 27, "QTY"),  # "2" (Specifically made QTY)
            (28, 34, "UNIT"),  # "ounces" (Specifically made UNIT)
            # Token ')' at 34 is O
            (36, 38, "PREP"),  # "of" (Kept as original PREP span)
            (39, 44, "NAME"),  # "plain"
            (45, 53, "NAME"),  # "tortilla"
            (54, 59, "NAME")  # "chips"
        ]
    }),

    # Example 54
    ("8 cups Brine, recipe follows", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 12, "NAME"),  # "Brine"
            # Comma at 12 is "O"
            (14, 28, "COMMENT")  # "recipe follows" (Kept)
        ]
    }),

    # Example 55
    ("2 to 3 bunches rainbow chard, stemmed and leaves sliced into 1- to 2-inch ribbons", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Original (0,1,"QTY"))
            (2, 6, "ALT_QTY"),  # "to 3" (Original (2,6,"ALT_NAME"))
            (7, 14, "UNIT"),  # "bunches"
            (15, 22, "NAME"),  # "rainbow" (from original NAME "rainbow chard" 15-28)
            (23, 28, "NAME"),  # "chard" (from original NAME "rainbow chard" 15-28)
            # Comma at 28 is "O"
            (30, 81, "PREP")  # "stemmed and leaves sliced into 1- to 2-inch ribbons" (Kept)
        ]
    }),

    # Example 56

    ("1/2 cup julienne cut sun dried tomatoes packed in oil, drained", {  # If "packed in oil, drained" was one PREP
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 16, "PREP"), (17, 20, "PREP"),
            (21, 24, "NAME"), (25, 30, "NAME"), (31, 39, "NAME"),
            (40, 62, "PREP")  # "packed in oil, drained"
        ]
    }),

    # Example 57
    ("4 tablespoons blended oil", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, "NAME"),
            # "blended" (from original NAME "blended oil" 14-25. Original NAME was (14,25,"PREP") for "blended")
            # Assuming (14,21,"PREP") and (22,25,"NAME") if "blended" is PREP for oil.
            (22, 25, "NAME")  # "oil"
        ]
    }),

    # Example 58
    ("2 pounds fresh spinach, washed and tough stems removed", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 14, "PREP"),  # "fresh" (Kept)
            (15, 22, "NAME"),  # "spinach"
            # Comma at 22 is "O"
            (24, 54, "PREP")  # "washed and tough stems removed" (Kept)
        ]
    }),

    # Example 59
    ("2.2 pounds (1 kilogram) good quality beef or Charolais beef, cut into 2-inch pieces.", {
        "entities": [
            (0, 3, "QTY"),  # "2.2" (Kept)
            (4, 10, "UNIT"),  # "pounds"
            (11, 23, "COMMENT"),  # "(1 kilogram)" (Kept)
            (24, 36, "PREP"),  # "good quality" (Kept)
            (37, 41, "NAME"),  # "beef"
            (42, 59, "ALT_NAME"),  # "or Charolais beef" (Kept)
            # Comma at 59 is "O"
            (61, 83, "PREP")  # "cut into 2-inch pieces" (Kept, period at end is O)
        ]
    }),

    # Example 60
    ("1 medium Bermuda onion, thinly sliced", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "UNIT"),  # "medium"
            (9, 16, "NAME"),  # "Bermuda" (from original NAME "Bermuda onion" 9-22)
            (17, 22, "NAME"),  # "onion" (from original NAME "Bermuda onion" 9-22)
            # Comma at 22 is "O"
            (24, 37, "PREP")
            # "thinly sliced" (Kept, from original (24,30,"PREP") "thinly" & (31,37,"PREP") "sliced" if separated by you)
        ]
    }),

    # Example 61
    ("2 teaspoons fat free ranch salad dressing", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 11, "UNIT"),  # "teaspoons"
            (12, 15, "PREP"),  # "fat" (from original PREP "fat free" 12-20)
            (16, 20, "PREP"),  # "free" (from original PREP "fat free" 12-20)
            (21, 26, "NAME"),  # "ranch" (from original NAME "ranch salad dressing" 21-41)
            (27, 32, "NAME"),  # "salad" (from original NAME 21-41)
            (33, 41, "NAME")  # "dressing" (from original NAME 21-41)
        ]
    }),

    # Example 62
    ("1 (28-ounce) can whole or crushed San Marzano tomatoes", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "COMMENT"),  # "(28-ounce)" (Kept)
            (13, 16, "UNIT"),  # "can"
            (17, 22, "NAME"),  # "whole" (from original ALT_NAME "whole or crushed" 17-33)
            (23, 33, "ALT_NAME"),  # "or" (from ALT_NAME 17-33) - *Unusual*
            (34, 37, "NAME"),  # "San" (from original NAME "San Marzano tomatoes" 34-54)
            (38, 45, "NAME"),  # "Marzano" (from original NAME 34-54)
            (46, 54, "NAME")  # "tomatoes" (from original NAME 34-54)
        ]
    }),

    # Example 63
    ("6 thin pretzel sticks, halved", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 6, "PREP"),  # "thin" (Kept)
            (7, 21, "NAME"),  # "pretzel"
            # Comma at 21 is "O"
            (23, 29, "PREP")  # "halved" (Kept)
        ]
    }),

    # Example 64
    ("1/2 cup cooked spinach, kept warm", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "cooked" (Kept)
            (15, 22, "NAME"),  # "spinach"
            # Comma at 22 is "O"
            (24, 33, "COMMENT")  # "kept warm" (Kept)
        ]
    }),

    # Example 65
    ("1 large pot 3/4 full with water, boiling", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "large"
            (8, 11, "NAME"),  # "pot"
            (12, 31, "COMMENT"),  # "3/4 full with water" (Kept)
            # Comma at 31 is "O"
            (33, 40, "PREP")  # "boiling" (Kept)
        ]
    }),

    # Example 66
    ("1 1/2 teaspoons turmeric, half a palmful", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 15, "UNIT"),  # "teaspoons"
            (16, 24, "NAME"),  # "turmeric"
            # Comma at 24 is "O"
            (26, 40, "COMMENT")  # "half a palmful" (Kept)
        ]
    }),

    # Example 67
    ("2 tablespoons, ginger diced small", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            # Comma at 13 is "O"
            (15, 21, "NAME"),  # "ginger"
            (22, 27, "PREP"),  # "diced" (from original PREP "diced small" 22-33)
            (28, 33, "PREP")  # "small" (from original PREP "diced small" 22-33)
        ]
    }),

    # Example 68 (Corrected based on "4 to 8 lemon wedges" rule: 4 QTY, to 8 ALT_NAME)
    ("5 medium or 12 baby carrots", {
        "entities": [
            (0, 1, "QTY"),  # "5"
            (2, 8, "UNIT"),  # "medium"
            (9, 19, "ALT_NAME"),  # "or"
            (20, 27, "NAME")  # "carrots"
        ]
    }),

    # Example 70
    ("3 1/2 ounces unsweetened chocolate, chopped into chunks, such as Valrhona", {
        "entities": [
            (0, 5, "QTY"),  # "3 1/2" (Kept)
            (6, 12, "UNIT"),  # "ounces"
            (13, 24, "NAME"),  # "unsweetened" (from original NAME "unsweetened chocolate" 13-34)
            (25, 34, "NAME"),  # "chocolate" (from original NAME "unsweetened chocolate" 13-34)
            # Comma at 34 is "O"
            (36, 55, "PREP"),  # "chopped into chunks" (Kept)
            # Comma at 55 is "O"
            (57, 73, "COMMENT")  # "such as Valrhona" (Kept)
        ]
    }),

    # Example 71
    ("1 tablespoon flavor enhancer seasoning, such as Accent", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 19, "NAME"),  # "flavor" (from original NAME "flavor enhancer seasoning" 13-38)
            (20, 28, "NAME"),  # "enhancer" (from original NAME 13-38)
            (29, 38, "NAME"),  # "seasoning" (from original NAME 13-38)
            # Comma at 38 is "O"
            (40, 54, "COMMENT")  # "such as Accent" (Kept)
        ]
    }),

    # Example 72
    ("1/2 tablespoon whole allspice", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 14, "UNIT"),  # "tablespoon"
            (15, 20, "PREP"),  # "whole" (Kept)
            (21, 29, "NAME")  # "allspice"
        ]
    }),

    # Example 73
    ("1/2 cup thinly sliced spring onion or scallions", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "thinly" (from original PREP "thinly sliced" 8-21)
            (15, 21, "PREP"),  # "sliced" (from original PREP "thinly sliced" 8-21)
            (22, 28, "NAME"),  # "spring" (from original NAME "spring onion" 22-34)
            (29, 34, "NAME"),  # "onion" (from original NAME "spring onion" 22-34)
            (35, 47, "ALT_NAME")  # "or scallions" (Kept)
        ]
    }),

    # Example 74
    ("1 cup (about 5 ounces) frozen gandules (pigeon peas)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 22, "COMMENT"),  # "(about 5 ounces)" (Kept)
            (23, 38, "NAME"),  # "frozen" (Kept)
            (39, 52, "COMMENT")  # "(pigeon peas)" (Kept)
        ]
    }),

    # Example 75


    # Example 76
    ("1/4 cup mild honey", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "PREP"),  # "mild" (Kept)
            (13, 18, "NAME")  # "honey"
        ]
    }),

    # Example 77
    ("4 slices of naruto kamaboko (Japanese white fish cake with a pink swirl in the center; optional)", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 11, "PREP"),  # "slices" (Original label PREP)
            (12, 18, "NAME"),  # "naruto" (from original NAME "naruto kamaboko" 12-27)
            (19, 27, "NAME"),  # "kamaboko" (from original NAME "naruto kamaboko" 12-27)
            (28, 96, "COMMENT")  # "(Japanese...optional)" (Kept)
        ]
    }),

    # Example 78
    ("2/3 cup store-bought or homemade granola", {
        "entities": [
            (0, 3, "QTY"),  # "2/3" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 32, "COMMENT"),  # "store-bought" (from original ALT_NAME "store-bought or homemade" 8-32)
            (33, 40, "NAME")  # "granola"
        ]
    }),

    # Example 79
    ("1/3 pound (about 30 cloves) garlic cloves", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 27, "COMMENT"),  # "(about 30 cloves)" (Kept)
            (28, 34, "NAME"),  # "garlic" (from original NAME "garlic cloves" 28-41)
            (35, 41, "NAME")  # "cloves" (from original NAME "garlic cloves" 28-41)
        ]
    }),

    # Example 80
    ("2 cups peeled, cooked and pureed sweet potatoes, cooled", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 32, "PREP"),  # "peeled" (Kept from original PREP (7,32) "peeled, cooked and pureed")
            (33, 38, "NAME"),  # "sweet" (from original NAME "sweet potatoes" 33-47)
            (39, 47, "NAME"),  # "potatoes" (from original NAME "sweet potatoes" 33-47)
            # Comma at 47 is "O"
            (49, 55, "PREP")  # "cooled" (Kept)
        ]
    }),

    # Example 81
    ("1/2 teaspoon pickle relish", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 19, "NAME"),  # "pickle" (from original NAME "pickle relish" 13-26)
            (20, 26, "NAME")  # "relish" (from original NAME "pickle relish" 13-26)
        ]
    }),

    # Example 82
    ("1 cup chardonnay", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 16, "NAME")  # "chardonnay"
        ]
    }),

    # Example 83
    ("20 grams (3 tablespoons) paillettes de feuilletine", {
        "entities": [
            (0, 2, "QTY"),  # "20" (Kept)
            (3, 8, "UNIT"),  # "grams"
            (9, 24, "COMMENT"),  # "(3 tablespoons)" (Kept)
            (25, 35, "NAME"),  # "paillettes" (from original NAME "paillettes de feuilletine" 25-50)
            (36, 38, "NAME"),  # "de" (from original NAME 25-50) - *Unusual*
            (39, 50, "NAME")  # "feuilletine" (from original NAME 25-50)
        ]
    }),

    # Example 84
    ("4 ounces thinly sliced soppresatta", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 22, "PREP"),  # "thinly" (from original PREP "thinly sliced" 9-22)
            (23, 34, "NAME")  # "soppresatta"
        ]
    }),

    # Example 85
    ("2 foot long loaves seeded semolina bread", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "PREP"),  # "foot"
            (7, 11, "PREP"),  # "long" (Kept)
            (12, 18, "PREP"),  # "loaves"
            (19, 25, "PREP"),  # "seeded" (Kept)
            (26, 34, "NAME"),  # "semolina" (from original NAME "semolina bread" 26-40)
            (35, 40, "NAME")  # "bread" (from original NAME "semolina bread" 26-40)
        ]
    }),

    # Example 86
    ("2 cups chopped, blanched, drained spinach (about 6 cups fresh or 1 pound frozen and defrosted)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 33, "PREP"),  # "chopped" (from original PREP "chopped, blanched, drained" 7-33, includes commas)
            (34, 41, "NAME"),  # "spinach"
            (42, 94, "COMMENT")  # "(about 6 cups fresh or 1 pound frozen and defrosted)" (Kept)
        ]
    }),

    # Example 87
    ("1/3 cup ouzo (Greek-style anise liqueur)", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "NAME"),  # "ouzo"
            (13, 40, "COMMENT")  # "(Greek-style anise liqueur)" (Kept)
        ]
    }),

    # Example 88
    ("1 1/2 pounds zoodles (spiralized zucchini noodles, from about 3 medium zucchinis; see Cook's Note)", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 20, "NAME"),  # "zoodles"
            (21, 98, "COMMENT")  # "(spiralized zucchini ... Cook's Note)" (Kept)
        ]
    }),

    # Example 89
    ("Four 3/4-inch-thick boneless pork chops, cut into 1/4-inch-thick slices", {
        "entities": [
            (0, 4, "QTY"),  # "Four" (Kept)
            (5, 19, "COMMENT"),  # "3/4-inch-thick" (Kept)
            (20, 28, "NAME"),  # "boneless" (Kept)
            (29, 33, "NAME"),  # "pork" (from original NAME "pork chops" 29-39)
            (34, 39, "NAME"),  # "chops" (from original NAME "pork chops" 29-39)
            # Comma at 39 is "O"
            (41, 71, "PREP")  # "cut into 1/4-inch-thick slices" (Kept)
        ]
    }),

    # Example 91
    ("1/2 head or more purple cabbage, sliced", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 8, "UNIT"),  # "head"
            (9, 16, "COMMENT"),  # "or more" (Kept)
            (17, 23, "NAME"),  # "purple" (from original NAME "purple cabbage" 17-31)
            (24, 31, "NAME"),  # "cabbage" (from original NAME "purple cabbage" 17-31)
            # Comma at 31 is "O"
            (33, 39, "PREP")  # "sliced" (Kept)
        ]
    }),

    # Example 92
    ("1 small vidalia onion, chopped", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "small"
            (8, 15, "NAME"),  # "vidalia" (from original NAME "vidalia onion" 8-21)
            (16, 21, "NAME"),  # "onion" (from original NAME "vidalia onion" 8-21)
            # Comma at 21 is "O"
            (23, 30, "PREP")  # "chopped" (Kept)
        ]
    }),

    # Example 94
    ("1/4 cup dark or spiced rum", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "NAME"),  # "dark or spiced" (Kept, original was (8,22,"ALT_NAME"))
            (13, 22, "ALT_NAME"),  # "dark or spiced" (Kept, original was (8,22,"ALT_NAME"))
            (23, 26, "NAME")  # "rum"
        ]
    }),

    # Example 95
    ("1/2 pound steamed clams (Manila or Littleneck)", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 17, "PREP"),  # "steamed" (Kept)
            (18, 23, "NAME"),  # "clams"
            (24, 45, "COMMENT")  # "(Manila or Littleneck)" (Kept)
        ]
    }),

    # Example 96
    ("1 cup whole, pitted medjool dates", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 19, "PREP"),  # "whole" (Kept from original (6,19,"PREP") "whole, pitted")
            (20, 27, "NAME"),  # "medjool" (from original NAME "medjool dates" 20-33)
            (28, 33, "NAME")  # "dates" (from original NAME "medjool dates" 20-33)
        ]
    }),

    # Example 97
    ("2 tablespoons plus 1/2 teaspoon Creole seasoning", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 31, "COMMENT"),  # "plus 1/2 teaspoon" (Kept)
            (32, 38, "NAME"),  # "Creole" (from original NAME "Creole seasoning" 32-48)
            (39, 48, "NAME")  # "seasoning" (from original NAME "Creole seasoning" 32-48)
        ]
    }),

    # Example 98
    ("3 tablespoons, olive oil", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            # Comma at 13 is "O"
            (15, 20, "NAME"),  # "olive" (from original NAME "olive oil" 15-24)
            (21, 24, "NAME")  # "oil" (from original NAME "olive oil" 15-24)
        ]
    }),

    # Example 99
    ("1 bundle farm spinach, trimmed, washed and dried, coarsely chopped", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "COMMENT"),  # "bundle"
            (9, 13, "PREP"),  # "farm" (Kept)
            (14, 21, "NAME"),  # "spinach"
            # Comma at 21 is "O"
            (23, 66, "PREP"), ]
    }),

    # Example 100
    ("1 level teaspoon freshly and roughly ground cardamom", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "PREP"),  # "level" (Kept)
            (8, 16, "UNIT"),  # "teaspoon"
            (17, 36, "PREP"),  # "freshly" (from original PREP "freshly and roughly ground" 17-43)
            (37, 52, "NAME")  # "cardamom"
        ]
    }),

    # Example 101
    ("6 pita breads or 3 large lavash, heated on the grill", {
        "entities": [
            # Primary Item
            (0, 1, "QTY"),         # "6"
            (2, 6, "NAME"),        # "pita"
            (7, 13, "NAME"),       # "breads"
            (14,16,'ALT_NAME'),
            # Alternative Item
            (17, 18, "ALT_QTY"),   # "3"
            (19, 24, "ALT_UNIT"),  # "large"
            (25, 31, "ALT_NAME"),  # "lavash"
            # Comma at 31 is O
            # Preparation
            (33, 52, "PREP")       # "heated on the grill"
        ]
    }),

    # Example 102
    ("1 1/2 cups julienned celeriac (about 1 small celery root, peeled)", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 20, "PREP"),  # "julienned" (Kept)
            (21, 29, "NAME"),  # "celeriac"
            (30, 64, "COMMENT")  # "(about 1 small celery root, peeled)" (Kept)
        ]
    }),

    # Example 103
    ("2 tablespoons fine-ground coffee", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 25, "PREP"),  # "fine-ground" (Kept)
            (26, 32, "NAME")  # "coffee"
        ]
    }),

    # Example 104
    ("1 pkg (1.25 oz each) 30% less sodium taco seasoning mix", {  # If (6,19) was comment
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"), (6, 19, "COMMENT"),
            (21, 23, "PREP"), (25, 29, "PREP"), (30, 36, "PREP"),
            # 30% less sodium (adjusting for typo in original sodium span)
            (37, 41, "NAME"), (42, 51, "NAME"), (52, 55, "NAME")
            # taco seasoning mix (adjusting for typo in original mix span)
        ]
    }),

    # Example 105
    ("2 pounds fresh spinach, washed and dried, stems removed and large leaves torn", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 14, "PREP"),  # "fresh" (Kept)
            (15, 22, "NAME"),  # "spinach"
            # Comma at 22 is "O"
            (24, 77, "PREP")  # "washed and dried, stems removed and large leaves torn" (Kept)
        ]
    }),

    # Example 106
    ("12 to 16 skewers (if wooden, soak in water for 15 to 20 minutes)", {
        "entities": [
            (0, 2, "QTY"),  # "12 to 16" (Kept)
            (3, 8, "ALT_QTY"),  # "12 to 16" (Kept)
            (9, 16, "NAME"),  # "skewers"
            (17, 64, "COMMENT")  # "(if wooden, soak in water for 15 to 20 minutes)" (Kept)
        ]
    }),

    # Example 107
    ("2 cups good quality mayonnaise", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 11, "PREP"),  # "good" (from original PREP "good quality" 7-19)
            (12, 19, "PREP"),  # "quality" (from original PREP "good quality" 7-19)
            (20, 30, "NAME")  # "mayonnaise"
        ]
    }),

    # Example 108
    ("1/2 cup nonfat or 1 percent lowfat milk", {  # If "nonfat" was one ALT_NAME and "or 1 percent lowfat" another
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (8, 14, "NAME"),  # nonfat
            (15, 34, "ALT_NAME"),  # "or 1 percent lowfat" (if this was the span)
            (35, 39, "NAME")
        ]
    }),

    # Example 109
    ("4 toothpicks", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 12, "NAME")  # "toothpicks"
        ]
    }),

    # Example 110
    ("4 ounces hot or mild sucuk (Turkish dry sausage), casing removed, sliced into 1/8-inch-thick pieces", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (28, 35, "NAME"),  # "Turkish" (from "Turkish dry sausage")
            (36, 39, "NAME"),  # "dry" (from "Turkish dry sausage")
            (40, 47, "NAME"),  # "sausage" (from "Turkish dry sausage")
            (50, 99, "PREP")  # "casing removed, sliced into 1/8-inch-thick pieces" (Kept)
        ]
    }),

    # Example 111
    ("1 lemon juiced and zested", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "NAME"),  # "lemon"
            (8, 25, "PREP")]  # "juiced" (from original PREP "juiced and zested" 8-25)
    }),

    # Example 112
    ("8 ounces cylindrical tteok (Korean rice cakes)", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 20, "PREP"),  # "cylindrical" (Kept)
            (21, 26, "NAME"),  # "tteok"
            (27, 46, "COMMENT")  # "(Korean rice cakes)" (Kept)
        ]
    }),

    # Example 113
    ("1/2 cup pimento-stuffed olives, halved, plus 1 tablespoon brine from the jar", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 23, "NAME"),  # "pimento-stuffed" (from original NAME "pimento-stuffed olives" 8-30)
            (24, 30, "NAME"),  # "olives" (from original NAME "pimento-stuffed olives" 8-30)
            # Comma at 30 is "O"
            (32, 38, "PREP"),  # "halved" (Kept)
            # Comma at 38 is "O"
            (40, 76, "COMMENT")  # "plus 1 tablespoon brine from the jar" (Kept)
        ]
    }),

    # Example 114

    ("2 cups thick, high-quality full-fat plain yogurt", {  # If commas are O
        "entities": [
            (0, 1, "QTY"), (2, 6, "UNIT"),
            (7, 12, "PREP"),  # thick
            # Comma O
            (14, 26, "PREP"),  # high-quality
            (27, 35, "NAME"),  # full-fat
            (36, 41, "NAME"), (42, 48, "NAME")  # plain yogurt
        ]
    }),

    # Example 115
    ("6 slices thick-cut good quality bacon", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 8, "PREP"),  # "slices" (from original PREP "slices thick-cut good quality" 2-31)
            (9, 18, "PREP"),  # "thick-cut" (from original PREP 2-31)
            (19, 31, "PREP"),  # "good" (from original PREP 2-31)
            (32, 37, "NAME")  # "bacon"
        ]
    }),

    # Example 116
    ("1/2 cup pitted oil-cured olives", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "pitted" (from original PREP "pitted oil-cured" 8-24)
            (15, 24, "PREP"),  # "oil-cured" (from original PREP "pitted oil-cured" 8-24)
            (25, 31, "NAME")  # "olives"
        ]
    }),

    # Example 117
    ("1/2 cup dark raisins", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "NAME"),  # "dark" (from original NAME "dark raisins" 8-20)
            (13, 20, "NAME")  # "raisins" (from original NAME "dark raisins" 8-20)
        ]
    }),

    # Example 118
    ("1 date or 1 prune, finely chopped", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 6, "NAME"),  # "date"
            (7, 17, "ALT_NAME"),  # "or 1 prune" (Kept)
            # Comma at 17 is "O"
            (19, 33, "PREP")  # "finely chopped" (Kept, original span (19,25) "finely", (26,33) "chopped")
        ]
    }),

    # Example 119 (Duplicate)
    ("1/2 cup pimento-stuffed olives", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (8, 23, "NAME"), (24, 30, "NAME")  # pimento-stuffed, olives
        ]
    }),

    # Example 120
    ("One 14-ounce can whole, diced or crushed fire-roasted tomatoes", {
        "entities": [
            (0, 3, "QTY"),  # "One" (Kept)
            (4, 12, "COMMENT"),  # "14-ounce" (Kept)
            (13, 16, "UNIT"),  # "can"
            (17, 22, "NAME"),  # "whole" (Kept from original (17,22,"ALT_NAME"))
            # Comma at 22 is "O"
            (24, 29, "ALT_NAME"),  # "diced" (Kept from original (24,29,"ALT_NAME"))
            (30, 40, "ALT_NAME"),  # "or crushed" (Kept from original (30,40,"ALT_NAME"))
            (41, 53, "NAME"),  # "fire-roasted" (from original NAME "fire-roasted tomatoes" 41-62)
            (54, 62, "NAME")  # "tomatoes" (from original NAME "fire-roasted tomatoes" 41-62)
        ]
    }),

    # Example 121
    ("3 tablespoons coffee liqueur", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 20, "NAME"),  # "coffee" (from original NAME "coffee liqueur" 14-28)
            (21, 28, "NAME")  # "liqueur" (from original NAME "coffee liqueur" 14-28)
        ]
    }),

    # Example 122

    # Example 123
    ("8 ounces dark chocolate in the 60 to 80 percent range, chopped into chunks, such as Valrhona", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 13, "NAME"),  # "dark" (from original NAME "dark chocolate" 9-23)
            (14, 23, "NAME"),  # "chocolate" (from original NAME "dark chocolate" 9-23)
            (24, 53, "COMMENT"),  # "in the 60 to 80 percent range" (Kept)
            # Comma at 53 is "O"
            (55, 74, "PREP"),  # "chopped into chunks" (Kept)
            # Comma at 74 is "O"
            (76, 92, "COMMENT")  # "such as Valrhona" (Kept)
        ]
    }),

    # Re-annotated data based on the FINAL REFINED rules:
    # - NAME entities are broken into word-level NAME entities.
    # - COMMENT, PREP, ALT_NAME, QTY entities are kept as single, original spans.
    #   - QTY entities like "4 to 8": If your original was "4" QTY and "to 8" ALT_NAME, that is followed.
    #     If original was "4 to 8" QTY, that is kept.
    # - UNIT entities are single words.
    # - Parentheses and Commas (that are not part of a kept COMMENT/PREP/ALT_NAME/QTY span)
    #   are "O" (and thus not listed in the 'entities' list).
    # - "or" in ALT_NAME is kept if it was part of your original ALT_NAME span.
    # Tokenization based on spaCy's default English tokenizer.

    # ... (all previous examples from your earlier chunks would be here) ...

    # Example 1

    ("14 ounces gingersnap cookies (about 46 cookies)", {  # If comment included parens
        "entities": [
            (0, 2, "QTY"), (3, 9, "UNIT"), (10, 20, "NAME"), (21, 28, "NAME"),
            (29, 47, "COMMENT")
        ]
    }),

    # Example 2
    ("2 cups chopped, peeled, seeded tomatoes and their juice", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 30, "PREP"),  # "chopped, peeled, seeded" (Kept as original PREP span, includes commas)
            (31, 39, "NAME"),  # "tomatoes"
            (40, 55, "COMMENT")  # "and their juice" (Kept as original COMMENT span)
        ]
    }),

    # Example 3
    ("1 cauliflower head, cored and roughly chopped", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 13, "NAME"),  # "cauliflower"
            (14, 18, "UNIT"),  # "head"
            # Comma at 18 is "O"
            (20, 45, "PREP")  # "cored and roughly chopped" (Kept as original PREP span)
        ]
    }),

    # Example 4
    ("1/2 cup drained and chopped water chestnuts", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 27, "PREP"),  # "drained and chopped" (Kept as original PREP span)
            (28, 33, "NAME"),  # "water" (from original NAME "water chestnuts" 28-43)
            (34, 43, "NAME")  # "chestnuts" (from original NAME "water chestnuts" 28-43)
        ]
    }),

    # Example 5
    ("2 Anjou or Bartlett pears, peeled, cored, and diced", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 7, "NAME"),  # "Anjou" (Kept from original (2,7))
            (8, 19, "ALT_NAME"),  # "or Bartlett" (Kept from original (8,19))
            (20, 25, "NAME"),  # "pears"
            # Comma at 25 is "O"
            (27, 51, "PREP")  # "peeled, cored, and diced" (Kept as original PREP span, includes commas and "and")
        ]
    }),

    # Example 6
    ("1 small can, 1/2 cup drained, mandarin sections, chopped", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "small" (from original UNIT (2,7))
            (8, 11, "UNIT"),  # "can" (from original UNIT (8,11))
            # Comma at 11 is "O"
            (13, 28, "COMMENT"),
            # "1/2 cup drained" (Kept, original included comma after drained, or was (13,28) for content?)
            # Comma at 28 is "O"
            (30, 38, "NAME"),  # "mandarin"
            (39, 47, "NAME"),  # "sections" (Original label was UNIT)
            # Comma at 47 is "O"
            (49, 56, "PREP")  # "chopped" (Kept)
        ]
    }),

    # Example 7
    ("5 long and mild red chiles, whole and undamaged", {
        "entities": [
            (0, 1, "QTY"),  # "5" (Kept)
            (2, 6, "PREP"),  # "long" (from original PREP (2,15) "long and mild")
            (7, 10, "PREP"),  # "and" (from PREP (2,15)) - *Unusual*
            (11, 15, "NAME"),  # "mild" (from PREP (2,15))
            (16, 19, "NAME"),  # "red" (from original NAME "red chiles" 16-26)
            (20, 26, "NAME"),  # "chiles" (from original NAME "red chiles" 16-26)
            # Comma at 26 is "O"
            (28, 47, "PREP"),  # "whole" (Kept)
        ]
    }),

    # Example 8
    ("Four 1/4-inch-thick slices canned luncheon meat, such as Spam", {
        "entities": [
            (0, 4, "QTY"),  # "Four" (Kept)
            (5, 19, "COMMENT"),  # "1/4-inch-thick" (Kept)
            (20, 26, "PREP"),  # "slices" (Original label PREP)
            (27, 33, "PREP"),
            # "canned" (from original PREP "canned luncheon meat" 34,47 - typo in original, assumed 27-47 for "canned luncheon meat" and canned is PREP, luncheon meat NAME)
            (34, 42, "NAME"),  # "luncheon"
            (43, 47, "NAME"),  # "meat"
            # Comma at 47 is "O"
            (49, 61, "COMMENT")  # "such as Spam" (Kept)
        ]
    }),

    # Example 9
    ("1 (15-ounce) can pre-cooked quail eggs*", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "COMMENT"),  # "(15-ounce)" (Kept)
            (13, 16, "UNIT"),  # "can"
            (17, 27, "PREP"),  # "pre-cooked" (Kept)
            (28, 33, "NAME"),  # "quail" (from original NAME "quail eggs*" 28-39)
            (34, 39, "NAME")  # "eggs*" (from original NAME "quail eggs*" 28-39, includes *)
        ]
    }),

    # Example 10
    ("2 cups uncooked long-grain white rice", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 15, "PREP"),  # "uncooked" (Kept)
            (16, 26, "NAME"),  # "long-grain" (Kept)
            (27, 32, "NAME"),  # "white" (from original NAME "white rice" 27-37)
            (33, 37, "NAME")  # "rice" (from original NAME "white rice" 27-37)
        ]
    }),

    # Example 11
    ("1/2 cup dried red lentils, picked over and rinsed", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "NAME"),  # "dried" (Kept)
            (14, 17, "NAME"),  # "red" (from original NAME "red lentils" 14-25)
            (18, 25, "NAME"),  # "lentils" (from original NAME "red lentils" 14-25)
            # Comma at 25 is "O"
            (27, 49, "PREP")  # "picked over and rinsed" (Kept)
        ]
    }),

    # Example 12

    ("3/4 cup sucralose (no calorie sweetener)", {  # If comment includes parens
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 17, "NAME"),
            (18, 40, "COMMENT")
        ]
    }),

    # Example 13 (Duplicate)
    ("1 cup good quality mayonnaise", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"), (6, 10, "PREP"), (11, 18, "PREP"), (19, 29, "NAME")  # good, quality
        ]
    }),

    # Example 14
    ("3 to 3 1/2 ounces enokis", {
        "entities": [
            (0, 1, "QTY"),  # "3" (from original QTY "3 to 3 1/2" 0-10)
            (2, 10, "ALT_QTY"),  # "to 3 1/2" (following "X to Y" rule for ranges)
            (11, 17, "UNIT"),  # "ounces"
            (18, 24, "NAME")  # "enokis"
        ]
    }),

    # Example 15
    ("1 taco shell", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 6, "NAME"),  # "taco" (from original NAME "taco shell" 2-12)
            (7, 12, "NAME")  # "shell" (from original NAME "taco shell" 2-12)
        ]
    }),

    # Example 16
    ("One 12-ounce bottle or can chilled hard cider (1 1/2 cups)", {
        "entities": [
            (0, 3, "COMMENT"),  # "One" (Kept)
            (4, 6, "QTY"),  # "12-ounce" (Kept)
            (7, 12, "UNIT"),  # "12-ounce" (Kept)
            (13, 26, "COMMENT"),  # "bottle"
            (27, 34, "PREP"),  # "chilled" (Kept)
            (35, 39, "NAME"),  # "hard" (from original NAME "hard cider" 35-45)
            (40, 45, "NAME"),  # "cider" (from original NAME "hard cider" 35-45)
            (46, 58, "COMMENT"),  # "1 1/2 cups" (from original COMMENT "(1 1/2 cups)" 46-58)
        ]
    }),

    # Example 17
    ("1 oyster", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "NAME")  # "oyster"
        ]
    }),

    # Example 18
    ("3 limes, 2 juiced and 1 cut into small wedges", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 7, "NAME"),  # "limes"
            # Comma at 7 is "O"
            (9, 45, "COMMENT")  # "2 juiced and 1 cut into small wedges" (Kept)
        ]
    }),

    # Example 19
    ("1/2 cup raw almond pieces", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 11, "PREP"),  # "raw" (Kept)
            (12, 18, "NAME"),  # "almond"
            (19, 25, "PREP")  # "pieces" (Original label PREP)
        ]
    }),

    # Example 20
    ("1 tablespoon plus 1 glass chilled Sutter Home Sauvignon Blanc", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 25, "COMMENT"),  # "plus 1 glass" (Kept)
            (26, 33, "PREP"),  # "chilled" (Kept)
            (34, 40, "NAME"),  # "Sutter" (from original NAME "Sutter Home Sauvignon Blanc" 34-61)
            (41, 45, "NAME"),  # "Home" (from original NAME 34-61)
            (46, 55, "NAME"),  # "Sauvignon" (from original NAME 34-61)
            (56, 61, "NAME")  # "Blanc" (from original NAME 34-61)
        ]
    }),

    # Example 21
    ("1 pheasant", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 10, "NAME")  # "pheasant"
        ]
    }),

    # Example 22
    ("1 1/2 cups vin santo", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 14, "NAME"),  # "vin" (from original NAME "vin santo" 11-20)
            (15, 20, "NAME")  # "santo" (from original NAME "vin santo" 11-20)
        ]
    }),

    ("32 ounces frozen, shredded hash browns, thawed, drained if needed", {  # If "frozen, shredded" was one PREP
        "entities": [
            (0, 2, "QTY"), (3, 9, "UNIT"),
            (10, 26, "PREP"),  # "frozen, shredded"
            (27, 31, "NAME"), (32, 38, "NAME"),
            (40, 46, "PREP"), (48, 65, "COMMENT")
        ]
    }),

    # Example 24
    ("3 medium-size cloves garlic, finely chopped", {  # If "finely chopped" is one PREP
        "entities": [
            (0, 1, "QTY"), (2, 13, "UNIT"), (14, 20, "NAME"), (21, 27, "NAME"),
            (29, 43, "PREP")  # "finely chopped"
        ]
    }),

    # Example 25
    ("3 cups cooked long-grain white rice", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 13, "PREP"),  # "cooked" (Kept)
            (14, 24, "NAME"),  # "long-grain" (Kept)
            (25, 30, "NAME"),  # "white" (from original NAME "white rice" 25-35)
            (31, 35, "NAME")  # "rice" (from original NAME "white rice" 25-35)
        ]
    }),

    # Example 26
    ("5 pounds 80-percent beef 20-percent pork ground meat blend", {
        "entities": [
            (0, 1, "QTY"),  # "5" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 58, "NAME"),  # "80-percent" (Kept)
        ]
    }),

    # Example 27
    ("2 iceberg heads, cut into chunks", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 9, "NAME"),  # "iceberg"
            (10, 15, "UNIT"),  # "heads"
            # Comma at 15 is "O"
            (17, 32, "PREP")  # "cut into chunks" (Kept)
        ]
    }),

    # Example 28
    ("1/4 cup sliced pimiento-stuffed olives", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "sliced" (Kept)
            (15, 31, "NAME"),  # "pimiento-stuffed" (from original NAME "pimiento-stuffed olives" 15-38)
            (32, 38, "NAME")  # "olives" (from original NAME "pimiento-stuffed olives" 15-38)
        ]
    }),

    # Example 29

    ("1/4 cup tricolor peppercorns (or any peppercorns)", {  # If comment includes parens
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 16, "NAME"), (17, 28, "NAME"),
            (29, 49, "COMMENT")
        ]
    }),

    # Example 30
    ("8 tortillas cut into quarters", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 11, "NAME"),  # "tortillas"
            (12, 29, "PREP")  # "cut into quarters" (Kept)
        ]
    }),

    # Example 31
    ("1 (28-ounce) can crushed tomatoes", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "COMMENT"),  # "(28-ounce)" (Kept)
            (13, 16, "UNIT"),  # "can"
            (17, 24, "NAME"),  # "crushed" (from original NAME "crushed tomatoes" 17-33)
            (25, 33, "NAME")  # "tomatoes" (from original NAME "crushed tomatoes" 17-33)
        ]
    }),

    # Example 32
    ("1 1/2 pounds skinless striped bass, cut into 2-inch chunks", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 21, "PREP"),  # "skinless" (Kept)
            (22, 29, "NAME"),  # "striped" (from original NAME "striped bass" 22-34)
            (30, 34, "NAME"),  # "bass" (from original NAME "striped bass" 22-34)
            # Comma at 34 is "O"
            (36, 58, "PREP")  # "cut into 2-inch chunks" (Kept)
        ]
    }),

    # Example 33
    ("7 ounces, or 1 1/2 cups, almond and sugar powder", {
        "entities": [
            (0, 1, "QTY"),  # "7" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            # Comma at 8 is "O"
            (10, 23, "COMMENT"),  # "or 1 1/2 cups," (Kept, includes comma)
            (25, 48, "NAME"),  # "almond" (from original NAME "almond and sugar powder" 25-48)
        ]
    }),

    # Example 34
    ("3 ounces turkey or chicken broth", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 15, "NAME"),  # "turkey"
            (16, 26, "ALT_NAME"),  # "or chicken" (Kept)
            (27, 32, "NAME")  # "broth"
        ]
    }),

    # Example 35
    ("1 (8-ounce) box tortellini", {
        "entities": [
            (0, 1, "COMMENT"),  # "1" (Original label was COMMENT)
            (3, 4, "QTY"),  # "8" (Kept from original (3,4,"QTY"))
            (5, 10, "UNIT"),  # "ounce" (from original (5,10,"UNIT"))
            (12, 15, "COMMENT"),  # "box" (Original label was COMMENT)
            (16, 26, "NAME")  # "tortellini"
        ]
    }),

    # Example 36

    ("3 tablespoons no-sugar-added oil (olive or canola) and vinegar dressing",
     {  # If comment included parens, and "and" is O
         "entities": [
             (0, 1, "QTY"), (2, 13, "UNIT"), (14, 28, "PREP"), (29, 32, "NAME"),
             (33, 50, "COMMENT"),  # (olive or canola)
             (51, 71, "ALT_NAME"),
         ]
     }),

    # Example 37
    ("1/2 tablespoon celery seed, ground", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 14, "UNIT"),  # "tablespoon"
            (15, 21, "NAME"),  # "celery" (from original NAME "celery seed" 15-26)
            (22, 26, "NAME"),  # "seed" (from original NAME "celery seed" 15-26)
            # Comma at 26 is "O"
            (28, 34, "PREP")  # "ground" (Kept)
        ]
    }),

    # Example 38
    ("1 (28-ounce) can crushed Italian tomatoes, any brand", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "COMMENT"),  # "(28-ounce)" (Kept)
            (13, 16, "UNIT"),  # "can"
            (17, 24, "NAME"),  # "crushed" (from original NAME "crushed Italian tomatoes" 17-41)
            (25, 32, "NAME"),  # "Italian" (from original NAME 17-41)
            (33, 41, "NAME"),  # "tomatoes" (from original NAME 17-41)
            # Comma at 41 is "O"
            (43, 52, "COMMENT")  # "any brand" (Kept)
        ]
    }),

    # Example 39
    ("1/4 teaspoon crushed red chile flakes", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 20, "NAME"),  # "crushed" (Kept)
            (21, 24, "NAME"),  # "red" (from original NAME "red chile flakes" 21-37)
            (25, 30, "NAME"),  # "chile" (from original NAME 21-37)
            (31, 37, "NAME")  # "flakes" (from original NAME 21-37)
        ]
    }),

    # Example 40
    ("1/2 teaspoon dried marjoram", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 18, "NAME"),  # "dried" (from original NAME "dried marjoram" 13-27)
            (19, 27, "NAME")  # "marjoram" (from original NAME "dried marjoram" 13-27)
        ]
    }),

    # Example 41
    ("2 cups mixed raspberries and blueberries, for topping", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 12, "NAME"),  # "mixed" (from original NAME "mixed raspberries and blueberries" 7-40)
            (13, 40, "NAME"),  # "raspberries" (from original NAME 7-40)
            # Comma at 40 is "O"
            (42, 53, "COMMENT")  # "for topping" (Kept)
        ]
    }),

    ("2 1/2 pounds thick, meaty, pork country ribs", {  # If commas in PREP are O
        "entities": [
            (0, 5, "QTY"), (6, 12, "UNIT"),
            (13, 18, "PREP"),  # thick
            # Comma O
            (20, 25, "PREP"),  # meaty
            # Comma O
            (27, 31, "NAME"), (32, 39, "NAME"), (40, 44, "NAME")
        ]
    }),

    # Example 43

    ("Two 8-ounce blocks tempeh, cut into 1/2-inch-thick strips", {  # If (4,12,"COMMENT") was for "8-ounce"
        "entities": [
            (0, 3, "QTY"),
            (4, 11, "COMMENT"),  # "8-ounce"
            (12, 18, "COMMENT"), (19, 25, "NAME"), (27, 57, "PREP")
        ]
    }),

    # Example 44
    ("2 bunches fresh parsley", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 9, "UNIT"),  # "bunches"
            (10, 15, "PREP"),  # "fresh" (from original NAME "fresh parsley" 10-23)
            (16, 23, "NAME")  # "parsley" (from original NAME "fresh parsley" 10-23)
        ]
    }),

    # Example 45
    ("8 large or jumbo eggs", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 7, "UNIT"),  # "large"
            (8, 16, "ALT_NAME"),  # "or jumbo" (Kept)
            (17, 21, "NAME")  # "eggs"
        ]
    }),

    # Example 46
    ("2 packages frozen phyllo dough, thawed", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 10, "UNIT"),  # "packages"
            (11, 17, "NAME"),  # "frozen" (Kept)
            (18, 24, "NAME"),  # "phyllo" (from original NAME "phyllo dough" 18-30)
            (25, 30, "NAME"),  # "dough" (from original NAME "phyllo dough" 18-30)
            # Comma at 30 is "O"
            (32, 38, "PREP")  # "thawed" (Kept)
        ]
    }),

    # Example 47
    ("8 chopsticks", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 12, "NAME")  # "chopsticks"
        ]
    }),

    # Example 48
    ("1 1/2 cups frozen or fresh baby peas", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 17, "NAME"),  # "frozen" (from original ALT_NAME "frozen or fresh" 11-26)
            (18, 20, "ALT_NAME"),  # "or" (from ALT_NAME 11-26) - *Unusual*
            (21, 26, "ALT_NAME"),  # "fresh" (from ALT_NAME 11-26)
            (27, 31, "NAME"),  # "baby" (from original NAME "baby peas" 27-36)
            (32, 36, "NAME")  # "peas" (from original NAME "baby peas" 27-36)
        ]
    }),

    # Example 49

    ("1 carambola (starfruit), discolored edges removed, julienned",
     {  # If comment included parens, and julienned is separate PREP
         "entities": [
             (0, 1, "QTY"), (2, 11, "NAME"), (12, 23, "COMMENT"),
             (25, 49, "PREP"),  # "discolored edges removed"
             # Comma at 49 O
             (51, 60, "PREP")  # "julienned"
         ]
     }),

    # Example 50
    ("1 pound each halibut and bass fillets, cut in large chunks", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 12, "COMMENT"),  # "each" (Kept)
            (13, 20, "NAME"),  # "halibut" (from original NAME "halibut and bass fillets" 13-37)
            (21, 24, "NAME"),  # "and" (from original NAME 13-37) - *Unusual*
            (25, 29, "NAME"),  # "bass" (from original NAME 13-37)
            (30, 37, "NAME"),  # "fillets" (from original NAME 13-37)
            # Comma at 37 is "O"
            (39, 58, "PREP")  # "cut in large chunks" (Kept)
        ]
    }),

    # Example 51
    ("One 28-ounce can or carton chopped tomatoes", {
        "entities": [
            (0, 3, "QTY"),  # "One" (Kept)
            (4, 12, "COMMENT"),  # "28-ounce" (Kept)
            (13, 16, "UNIT"),  # "can"
            (17, 26, "ALT_NAME"),  # "or carton" (Kept)
            (27, 34, "NAME"),  # "chopped" (from original NAME "chopped tomatoes" 27-43)
            (35, 43, "NAME")  # "tomatoes" (from original NAME "chopped tomatoes" 27-43)
        ]
    }),

    # Example 52
    ("1/2 teaspoon anise seed", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 18, "NAME"),  # "anise" (from original NAME "anise seed" 13-23)
            (19, 23, "NAME")  # "seed" (from original NAME "anise seed" 13-23)
        ]
    }),

    # Example 53
    ("1/2 cup of Talavera Muscat", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 10, "PREP"),  # "of" (Original label was UNIT, but "of" is usually PREP or O)
            # If original was (8,10,"UNIT"), it stays UNIT. Assuming PREP is more logical for "of".
            (11, 19, "NAME"),  # "Talavera" (from original NAME "Talavera Muscat" 11-26)
            (20, 26, "NAME")  # "Muscat" (from original NAME "Talavera Muscat" 11-26)
        ]
    }),

    # Example 54
    ("4 ounces, 1 stick of butter, cut up into small pieces and frozen", {
        "entities": [
            (0, 1, "QTY"),         # "4"
            (2, 8, "UNIT"),        # "ounces"
            # Comma at 8 is O
            (10, 11, "ALT_QTY"),   # "1" (alternative quantity for the butter)
            (12, 17, "COMMENT"),   # "stick" (form descriptor, not a standard UNIT from your list for measuring)
            # "of" (18,20) is O (or could be part of the "stick" comment if desired)
            (21, 27, "NAME"),      # "butter"
            # Comma at 27 is O
            (29, 32, "PREP"),      # "cut"
            (33, 35, "PREP"),      # "up"
            (36, 40, "PREP"),      # "into"
            (41, 46, "PREP"),      # "small"
            (47, 53, "PREP"),      # "pieces"
            # "and" (54,57) is O (connecting PREP phrases)
            (58, 64, "PREP")       # "frozen"
        ]
    }),

    # Example 55
    ("For serving: shredded Cheddar and flour tortillas", {
        "entities": [
            (0, 12, "COMMENT"),  # "For serving:" (Kept)
            (13, 21, "NAME"),  # "shredded" (from original NAME "shredded Cheddar" 13-29)
            (22, 29, "NAME"),  # "Cheddar" (from original NAME "shredded Cheddar" 13-29)
        ]
    }),

    # Example 56
    ("1 (28-ounce) can diced tomatoes in juice", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "COMMENT"),  # "(28-ounce)" (Kept)
            (13, 16, "UNIT"),  # "can"
            (17, 22, "NAME"),  # "diced" (from original NAME "diced tomatoes" 17-31)
            (23, 31, "NAME"),  # "tomatoes" (from original NAME "diced tomatoes" 17-31)
            (32, 40, "COMMENT")  # "in juice" (Kept)
        ]
    }),

    # Example 57
    ("2 cups grated cheese, a combination of Monterey Jack and cheddar is nice", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 20, "NAME"),  # "grated" (Kept)
            # Comma at 20 is "O"
            (22, 72, "COMMENT")  # "a combination of Monterey Jack and cheddar is nice" (Kept)
        ]
    }),

    # Example 58
    ("7 tablespoons cold, unsalted butter, diced", {
        "entities": [
            (0, 1, "QTY"),  # "7" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 18, "PREP"),  # "cold" (Kept)
            # Comma at 18 is "O"
            (20, 28, "NAME"),  # "unsalted" (from original NAME "unsalted butter" 20-35)
            (29, 35, "NAME"),  # "butter" (from original NAME "unsalted butter" 20-35)
            # Comma at 35 is "O"
            (37, 42, "PREP")  # "diced" (Kept)
        ]
    }),

    # Example 59
    ("2 medium celery root, peeled and chopped (about 2 1/4 pounds or 4 cups chopped)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "medium"
            (9, 15, "NAME"),  # "celery" (from original NAME "celery root" 9-20)
            (16, 20, "NAME"),  # "root" (from original NAME "celery root" 9-20)
            # Comma at 20 is "O"
            (22, 40, "PREP"),  # "peeled" (Kept from original (22,28,"PREP"))
            (41, 79, "COMMENT")
        ]
    }),

    # Example 60

    ("1/2 cup (125 milliliters) 35% cream", {  # If comment included parens
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 25, "COMMENT"),
            (26, 29, "NAME"), (30, 35, "NAME")
        ]
    }),

    # Example 61
    ("2 pounds french fries", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 15, "NAME"),  # "french" (from original NAME "french fries" 9-21)
            (16, 21, "NAME")  # "fries" (from original NAME "french fries" 9-21)
        ]
    }),

    # Example 62
    ("1 stick cold, unsalted butter", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "PREP"),  # "stick"
            # Comma at 12 is "O"
            (14, 22, "NAME"),  # "unsalted" (from original NAME "unsalted butter" 14-29)
            (23, 29, "NAME")  # "butter" (from original NAME "unsalted butter" 14-29)
        ]
    }),

    # Example 63
    ("Orange slice, for garnish", {
        "entities": [
            (0, 6, "NAME"),  # "Orange"
            (7, 12, "PREP"),  # "slice" (Original label PREP)
            # Comma at 12 is "O"
            (14, 25, "COMMENT")  # "for garnish" (Kept)
        ]
    }),

    # Example 64
    ("4 small lamb shanks", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 7, "UNIT"),  # "small"
            (8, 12, "NAME"),  # "lamb" (from original NAME "lamb shanks" 8-19)
            (13, 19, "NAME")  # "shanks" (from original NAME "lamb shanks" 8-19)
        ]
    }),

    # Example 65

    ("4 teaspoons tobiko (flying fish roe)", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 11, "UNIT"), (12, 18, "NAME"),
            (19, 36, "COMMENT")
        ]
    }),

    # Example 66
    ("1/4 cup 100% grape or apple juice", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "PREP"),  # "100%" (Kept)
            (13, 18, "NAME"),  # "grape"
            (19, 27, "ALT_NAME"),  # "apple" (from original ALT_NAME "or apple" 19-27 - your original was just "apple")
            (28, 33, "NAME")  # "juice"
        ]
    }),

    # Example 67
    ("1 tablespoon cumin - toasted and ground", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 18, "NAME"),  # "cumin"
            (19, 20, "O"),  # "-"
            (21, 39, "PREP")
            # "toasted and ground" (Kept, original was (21,28) "toasted", (29,32) "and", (33,39) "ground")
        ]
    }),

    # Example 68
    ("2 to 3 small ribs celery, from the heart with leafy tops, chopped", {
        "entities": [
            (0, 6, "QTY"),  # "2 to 3" (Kept)
            (7, 12, "UNIT"),  # "small"
            (13, 17, "PREP"),  # "ribs" (Original label PREP)
            (18, 24, "NAME"),  # "celery"
            # Comma at 24 is "O"
            (26, 56, "COMMENT"),  # "from the heart with leafy tops" (Kept)
            # Comma at 56 is "O"
            (58, 65, "PREP")  # "chopped" (Kept)
        ]
    }),

    # Example 69
    ("6 ounces low-sodium or unsalted tortilla chips (about 7 cups)", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 19, "NAME"),  # "low-sodium" (from original ALT_NAME "low-sodium or unsalted" 9-31)
            (20, 31, "ALT_NAME"),  # "or" (from ALT_NAME 9-31) - *Unusual*
            (32, 40, "NAME"),  # "tortilla" (from original NAME "tortilla chips" 32-46)
            (41, 46, "NAME"),  # "chips" (from original NAME "tortilla chips" 32-46)
            (47, 61, "COMMENT"),  # "about 7 cups" (from original COMMENT (47,61))
        ]
    }),

    ("3 cups plus 3 tablespoons (500 grams) blanched, whole, almonds",
     {  # If original COMMENT was (7,37) and PREP was (38,53) including commas
         "entities": [
             (0, 1, "QTY"), (2, 6, "UNIT"), (7, 37, "COMMENT"),
             (38, 53, "PREP"),  # "blanched, whole,"
             # Comma O
             (55, 62, "NAME")
         ]
     }),

    # Example 71
    ("1 conch, meat cut into small dice", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "NAME"),  # "conch"
            # Comma at 7 is "O"
            (9, 33, "PREP")  # "meat cut into small dice" (Kept)
        ]
    }),

    # Example 72
    ("6 heaping tablespoons dried wasabi", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 9, "PREP"),  # "heaping" (Kept)
            (10, 21, "UNIT"),  # "tablespoons"
            (22, 34, "NAME")  # "wasabi"
        ]
    }),

    # Example 73
    ("8 ounces each, watermelon puree, strawberry puree, fresh lemonade, iced coffee", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 14, "COMMENT"),  # "each," (Kept, includes comma)
            (15, 25, "NAME"),  # "watermelon" (from original NAME "watermelon puree" 15-31)
            (26, 31, "NAME"),  # "puree" (from original NAME "watermelon puree" 15-31)
            # Comma at 31 is "O"
            (33, 43, "ALT_NAME"),  # "strawberry" (Original ALT_NAME (33,43))
            (44, 49, "ALT_NAME"),  # "puree" (Original ALT_NAME (44,49))
            # Comma at 49 is "O"
            (51, 56, "ALT_NAME"),  # "fresh" (Original ALT_NAME (51,56))
            (57, 65, "ALT_NAME"),  # "lemonade" (Original ALT_NAME (57,65))
            # Comma at 65 is "O"
            (67, 71, "ALT_NAME"),  # "iced" (Original ALT_NAME (67,71))
            (72, 78, "ALT_NAME")  # "coffee" (Original ALT_NAME (72,78))
        ]
    }),

    # Example 74
    ("1 cup crushed pecans", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 13, "NAME"),  # "crushed" (from original NAME "crushed pecans" 6-20)
            (14, 20, "NAME")  # "pecans" (from original NAME "crushed pecans" 6-20)
        ]
    }),

    # Example 75
    ("6 ounces ground pork, cooked", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 15, "NAME"),  # "ground" (from original NAME "ground pork" 9-20)
            (16, 20, "NAME"),  # "pork" (from original NAME "ground pork" 9-20)
            # Comma at 20 is "O"
            (22, 28, "PREP")  # "cooked" (Kept)
        ]
    }),

    # Example 76

    ("1/3 to 1/2 cup oil, for shallow frying", {  # Most consistent with other "X to Y"
        "entities": [
            (0, 3, "QTY"),  # 1/3
            (4, 10, "ALT_QTY"),  # "to 1/2 cup" (as it modifies the first QTY, and "cup" is part of it)
            (11, 14, "NAME"),  # oil
            (20, 38, "COMMENT")
        ]
    }),

    # Example 77
    ("2 tablespoons fresh or dried chives", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 28, "PREP"),  # "fresh"
            (29, 35, "NAME")  # "chives"
        ]
    }),

    # Example 78
    ("1/2 pound whole butter, reserving 2 tablespoons, small dice", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 15, "PREP"),  # "whole" (Kept)
            (16, 22, "NAME"),  # "butter"
            # Comma at 22 is "O"
            (24, 47, "COMMENT"),  # "reserving 2 tablespoons" (Kept)
            # Comma at 47 is "O"
            (49, 59, "PREP")  # "small dice" (Kept)
        ]
    }),

    # Example 79
    ("2 sticks unsalted butter, softened", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "sticks"
            (9, 17, "NAME"),  # "unsalted" (from original NAME "unsalted butter" 9-24)
            (18, 24, "NAME"),  # "butter" (from original NAME "unsalted butter" 9-24)
            # Comma at 24 is "O"
            (26, 34, "PREP")  # "softened" (Kept)
        ]
    }),

    # Example 80
    ("1 cup mascarpone, at room temperature", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 16, "NAME"),  # "mascarpone"
            # Comma at 16 is "O"
            (18, 37, "COMMENT")  # "at room temperature" (Kept)
        ]
    }),

    # Example 81
    ("1 (8-ounce) container vanilla flavored yogurt", {
        "entities": [
            (0, 1, "COMMENT"),  # "1" (Original label COMMENT)
            (3, 4, "QTY"),  # "8" (Original QTY)
            (5, 10, "UNIT"),  # "ounce" (Original UNIT)
            (12, 21, "COMMENT"),  # "container" (Original COMMENT (5,21) was for "(8-ounce) container")
            # This is tricky again. If (2,11) was COMMENT for "(8-ounce)" and (12,21) COMMENT for "container"
            (22, 29, "NAME"),  # "vanilla" (from original NAME "vanilla flavored yogurt" 22-45)
            (30, 38, "NAME"),  # "flavored" (from original NAME 22-45)
            (39, 45, "NAME")  # "yogurt" (from original NAME 22-45)
        ]
    }),

    # Example 82
    ("1 pound fresh or frozen strawberries, halved", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 23, "PREP"),  # "fresh"
            (24, 36, "NAME"),  # "strawberries"
            # Comma at 36 is "O"
            (38, 44, "PREP")  # "halved" (Kept)
        ]
    }),

    # Example 83
    ("1/2 pound calabaza pumpkin (Caribbean pumpkin), peeled and cut into large dice (substitute with kabocha squash, butternut squash, sweet potatoes or carrots)",
     {
         "entities": [
             (0, 3, "QTY"),  # "1/2" (Kept)
             (4, 9, "UNIT"),  # "pound"
             (10, 18, "NAME"),  # "calabaza" (from original NAME "calabaza pumpkin" 10-26)
             (19, 26, "NAME"),  # "pumpkin" (from original NAME "calabaza pumpkin" 10-26)
             (27, 46, "COMMENT"),  # "Caribbean pumpkin" (from original COMMENT (27,46))
             # Comma at 46 is "O"
             (48, 78, "PREP"),  # "peeled and cut into large dice" (Kept)
             (79, 156, "COMMENT"),  # "substitute with...carrots" (from original COMMENT (79,156))
         ]
     }),

    # Example 84
    ("1 1/2 cups dried figs, roughly chopped", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 21, "NAME"),  # "figs"
            # Comma at 21 is "O"
            (23, 38, "PREP"),  # "roughly" (from original PREP "roughly chopped" 23-38)
        ]
    }),

    # Example 85
    ("8 ounces of firm cream cheese ( 1 package), room temperature", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 11, "PREP"),  # "of" (Kept from original (9,16,"PREP") "of firm")
            (12, 16, "PREP"),  # "firm" (from original PREP "of firm" 9-16)
            (17, 22, "NAME"),  # "cream" (from original NAME "cream cheese" 17-29)
            (23, 29, "NAME"),  # "cheese" (from original NAME "cream cheese" 17-29)
            (30, 60, "COMMENT"),  # " 1 package" (from original COMMENT (30,60) "( 1 package), room temperature")
        ]
    }),

    # Example 86
    ("1 pound fresh filleted herring, skin off (about 6)", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "PREP"), (14, 22, "PREP"), (23, 30, "NAME"),
            (32, 40, "PREP"), (41, 50, "COMMENT")
        ]
    }),

    # Example 87

    ('6 large, fresh poblano chiles (sometimes called "pasilla" chiles)', {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (9, 14, "PREP"), (15, 22, "NAME"), (23, 29, "NAME"),
            (30, 65, "COMMENT")
        ]
    }),

    # Example 88

    ("2 each lapchong, fine diced (may substitute with sausage)", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 6, "UNIT"), (7, 15, "NAME"),
            (17, 21, "PREP"), (22, 27, "PREP"),
            (28, 57, "COMMENT")
        ]
    }),

    # Example 89
    ("1 red bell pepper fine diced", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "NAME"),  # "red" (from original NAME "red bell pepper" 2-17)
            (6, 10, "NAME"),  # "bell" (from original NAME 2-17)
            (11, 17, "NAME"),  # "pepper" (from original NAME 2-17)
            (18, 22, "PREP"),  # "fine" (from original PREP "fine diced" 18-28)
            (23, 28, "PREP")  # "diced" (from original PREP "fine diced" 18-28)
        ]
    }),

    # Example 90
    ("8 ounces raw breakfast sausage", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 12, "PREP"),  # "raw" (Kept)
            (13, 22, "NAME"),  # "breakfast" (from original NAME "breakfast sausage" 13-30)
            (23, 30, "NAME")  # "sausage" (from original NAME "breakfast sausage" 13-30)
        ]
    }),

    # Example 91
    ("1 teaspoon plus a pinch paprika", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 24, "COMMENT"),  # "plus a pinch" (Kept)
            (25, 32, "NAME")  # "paprika"
        ]
    }),

    # Example 92
    ("Tartar sauce", {
        "entities": [
            (0, 6, "NAME"),  # "Tartar" (from original NAME "Tartar sauce" 0-12)
            (7, 12, "NAME")  # "sauce" (from original NAME "Tartar sauce" 0-12)
        ]
    }),

    # Example 93
    ("1/3 cup good olive oil", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "PREP"),  # "good" (Kept)
            (13, 18, "NAME"),  # "olive" (from original NAME "olive oil" 13-22)
            (19, 22, "NAME")  # "oil" (from original NAME "olive oil" 13-22)
        ]
    }),

    # Example 94
    ("Rustic Tomatillo and Avocado Salsa", {
        "entities": [
            (0, 6, "NAME"),  # "Rustic" (from original NAME "Rustic Tomatillo and Avocado Salsa" 0-34)
            (7, 16, "NAME"),  # "Tomatillo" (from original NAME 0-34)
            (17, 20, "NAME"),  # "and" (from original NAME 0-34) - *Unusual*
            (21, 28, "NAME"),  # "Avocado" (from original NAME 0-34)
            (29, 34, "NAME")  # "Salsa" (from original NAME 0-34)
        ]
    }),

    # Example 95
    ("1 tablespoon pre-made dressing, such as honey Dijon, Italian or sesame", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 21, "PREP"),  # "pre-made" (Kept)
            (22, 30, "NAME"),  # "dressing"
            # Comma at 30 is "O"
            (32, 70, "COMMENT")  # "such as honey Dijon, Italian or sesame" (Kept)
        ]
    }),

    # Example 96
    ("1/4 cup white vinegar or water", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "NAME"),  # "white" (from original NAME "white vinegar" 8-21)
            (14, 21, "NAME"),  # "vinegar" (from original NAME "white vinegar" 8-21)
            (22, 30, "ALT_NAME")  # "or water" (Kept)
        ]
    }),

    # Example 97

    ("2 cups (8 oz.) shredded Cheddar cheese", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 6, "UNIT"), (7, 14, "COMMENT"), (15, 23, "NAME"),
            (24, 31, "NAME"), (32, 38, "NAME")
        ]
    }),

    # Example 98
    ("1/2 lb. lean ground beef", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "lb."
            (8, 12, "NAME"),  # "lean" (Kept)
            (13, 19, "NAME"),  # "ground" (from original NAME "ground beef" 13-24)
            (20, 24, "NAME")  # "beef" (from original NAME "ground beef" 13-24)
        ]
    }),

    # Example 99
    ("1/2 cup dried pitted dates", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "NAME"),  # "dried" (from original NAME "dried pitted dates" 8-26)
            (14, 20, "NAME"),  # "pitted" (from original NAME 8-26)
            (21, 26, "NAME")  # "dates" (from original NAME 8-26)
        ]
    }),

    # Example 100
    ("1/2 cup diced red pepper", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "PREP"),  # "diced" (Kept)
            (14, 17, "NAME"),  # "red" (from original NAME "red pepper" 14-24)
            (18, 24, "NAME")  # "pepper" (from original NAME "red pepper" 14-24)
        ]
    }),

    # Example 101
    ("1 jar apricot jam", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "COMMENT"),  # "jar" (Original label COMMENT)
            (6, 13, "NAME"),  # "apricot" (from original NAME "apricot jam" 6-17)
            (14, 17, "NAME")  # "jam" (from original NAME "apricot jam" 6-17)
        ]
    }),

    # Example 102
    ("1/2 cup finely chopped cornichon", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "finely" (Kept)
            (15, 22, "PREP"),  # "chopped" (Kept)
            (23, 32, "NAME")  # "cornichon"
        ]
    }),

    # Example 103
    ("1 1/4 cups peeled, cored, and diced apples", {  # If PREP included commas/and
        "entities": [
            (0, 5, "QTY"), (6, 10, "UNIT"), (11, 35, "PREP"), (36, 42, "NAME")
        ]
    }),

    # Example 104
    ("2 ounces whole blanched hazelnuts, toasted", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 14, "PREP"),  # "whole" (from original PREP "whole blanched" 9-23)
            (15, 23, "PREP"),  # "blanched" (from original PREP "whole blanched" 9-23)
            (24, 33, "NAME"),  # "hazelnuts"
            # Comma at 33 is "O"
            (35, 42, "PREP")  # "toasted" (Kept)
        ]
    }),

    # Example 105
    ("12 ounces ricotta", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 9, "UNIT"),  # "ounces"
            (10, 17, "NAME")  # "ricotta"
        ]
    }),

    # Example 106
    ("1/2 cup nicoise olives, pitted", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "NAME"),  # "nicoise" (from original NAME "nicoise olives" 8-22)
            (16, 22, "NAME"),  # "olives" (from original NAME "nicoise olives" 8-22)
            # Comma at 22 is "O"
            (24, 30, "PREP")  # "pitted" (Kept)
        ]
    }),

    # Example 107
    ("1 tablespoon crystal hot sauce", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 20, "NAME"),  # "crystal" (from original NAME "crystal hot sauce" 13-30)
            (21, 24, "NAME"),  # "hot" (from original NAME "crystal hot sauce" 13-30)
            (25, 30, "NAME")  # "sauce" (from original NAME "crystal hot sauce" 13-30)
        ]
    }),

    # Example 108
    ("1/2 pound small, blue-potatoes, such as Peruvian fingerling, scrubbed", {  # If "blue-potatoes" is one NAME
        "entities": [
            (0, 3, "QTY"), (4, 9, "UNIT"), (10, 15, "PREP"),
            (17, 30, "NAME"),  # "blue-potatoes"
            (32, 59, "COMMENT"), (61, 69, "PREP")
        ]
    }),
    # Re-annotated data based on the FINAL REFINED rules:
    # - NAME entities are broken into word-level NAME entities.
    # - COMMENT, PREP, ALT_NAME, QTY entities are kept as single, original spans.
    #   - QTY entities like "4 to 8": "4" is QTY, "to 8" is ALT_NAME (as per your specific instruction for ranges).
    # - UNIT entities are single words.
    # - Parentheses and Commas (that are not part of a kept COMMENT/PREP/ALT_NAME/QTY span)
    #   are "O" (and thus not listed in the 'entities' list).
    # - "or" in ALT_NAME is kept if it was part of your original ALT_NAME span.
    # Tokenization based on spaCy's default English tokenizer.

    # ... (all previous examples from your earlier chunks would be here) ...

    # Example 1
    ("1/2 pound small, red-skinned potatoes", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 15, "PREP"),  # "small" (Kept)
            # Comma at 15 is "O"
            (17, 28, "NAME"),  # "red-skinned" (from original NAME "red-skinned potatoes" 17-37)
            (29, 37, "NAME")  # "potatoes" (from original NAME "red-skinned potatoes" 17-37)
        ]
    }),

    # Example 2
    ("1/2 pound small, white-skinned waxy-style potatoes", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 15, "PREP"),  # "small" (Kept)
            # Comma at 15 is "O"
            (17, 30, "NAME"),  # "white-skinned" (from original NAME "white-skinned waxy-style potatoes" 17-50)
            (31, 41, "NAME"),  # "waxy-style" (from original NAME 17-50)
            (42, 50, "NAME")  # "potatoes" (from original NAME 17-50)
        ]
    }),

    # Example 4
    ("4 ounces sliced Italian fontina cheese", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 15, "PREP"),  # "sliced" (Kept)
            (16, 23, "NAME"),  # "Italian" (from original NAME "Italian fontina cheese" 16-38)
            (24, 31, "NAME"),  # "fontina" (from original NAME 16-38)
            (32, 38, "NAME")  # "cheese" (from original NAME 16-38)
        ]
    }),

    # Example 5
    ("Hot sauce", {
        "entities": [
            (0, 9, "NAME"),  # "Hot" (from original NAME "Hot sauce" 0-9)
        ]
    }),

    # Example 6
    ("1 tablespoon dry sherry", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 16, "NAME"),  # "dry" (from original NAME "dry sherry" 13-23)
            (17, 23, "NAME")  # "sherry" (from original NAME "dry sherry" 13-23)
        ]
    }),

    # Example 7
    ("1/4 cup fresh Italian parsley, chopped", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "PREP"),  # "fresh" (Kept)
            (14, 21, "NAME"),  # "Italian" (from original NAME "Italian parsley" 14-29)
            (22, 29, "NAME"),  # "parsley" (from original NAME "Italian parsley" 14-29)
            # Comma at 29 is "O"
            (31, 38, "PREP")  # "chopped" (Kept)
        ]
    }),

    # Example 8
    ("1/3 cup dried porcinis", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "NAME"),  # "dried" (from original NAME "dried porcinis" 8-22, implies "dried" is NAME)
            (14, 22, "NAME")  # "porcinis" (from original NAME "dried porcinis" 8-22)
        ]
    }),

    # Example 9

    ("1/2 cup chopped, fresh parsley", {  # If original PREP (8,22) for "chopped, fresh"
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (8, 22, "PREP"),  # "chopped, fresh"
            (23, 30, "NAME")
        ]
    }),

    # Example 10 ("8 to10" vs "8 to 10") - Assuming "8 to 10" was intended.
    ("8 to 10 large prawns, shells and veins removed", {
        "entities": [
            (0, 1, "QTY"),  # "8" (From original QTY (0,6) "8 to10" - changed to "8 to 10" for clarity)
            (2, 7, "ALT_QTY"),  # "to 10" (Following "X to Y" rule)
            (8, 13, "UNIT"),  # "large"
            (14, 20, "NAME"),  # "prawns"
            # Comma at 20 is "O"
            (22, 46, "PREP")  # "shells and veins removed" (Kept)
        ]
    }),

    # Example 11
    ("1 cup fresh ricotta", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 11, "PREP"),  # "fresh" (Kept)
            (12, 19, "NAME")  # "ricotta"
        ]
    }),

    # Example 12

    ("1 15- to 16-ounce box yellow cake mix (plus required ingredients)", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 17, "COMMENT"), (18, 21, "PREP"),
            (22, 28, "NAME"), (29, 33, "NAME"), (34, 37, "NAME"),
            (38, 65, "COMMENT")
        ]
    }),

    # Example 13
    ("1 cup yellow candy melts", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "NAME"),  # "yellow" (from original NAME "yellow candy melts" 6-24)
            (13, 18, "NAME"),  # "candy" (from original NAME 6-24)
            (19, 24, "NAME")  # "melts" (from original NAME 6-24)
        ]
    }),

    # Example 14
    ("1/4 cup finely chopped fresh parsley", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "finely" (from original PREP (8,28) "finely chopped fresh")
            (15, 22, "PREP"),  # "chopped" (from original PREP (8,28))
            (23, 28, "PREP"),  # "fresh" (from original PREP (8,28))
            (29, 36, "NAME")  # "parsley"
        ]
    }),

    # Example 15
    ("1 tablespoon finely chopped garlic", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 19, "PREP"),  # "finely" (from original PREP (13,27) "finely chopped")
            (20, 27, "PREP"),  # "chopped" (from original PREP (13,27))
            (28, 34, "NAME")  # "garlic"
        ]
    }),

    # Example 16
    ("3 cups 1 1/2-inch-cubed whole-wheat bread", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 23, "PREP"),  # "1 1/2-inch-cubed" (Kept)
            (24, 35, "NAME"),  # "whole-wheat" (from original NAME "whole-wheat bread" 24-41)
            (36, 41, "NAME")  # "bread" (from original NAME "whole-wheat bread" 24-41)
        ]
    }),

    # Example 17

    ("3 tablespoons warm water (about 100˚ F)", {  # If original (14,18,"COMMENT") and comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 13, "UNIT"), (14, 18, "PREP"), (19, 24, "NAME"),
            (25, 39, "COMMENT")
        ]
    }),

    # Example 18
    ("4 ¼-inch slices fresh ginger", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "COMMENT"),  # "¼-inch" (Kept)
            (9, 15, "PREP"),  # "slices" (from original PREP (9,21) "slices fresh")
            (16, 21, "PREP"),  # "fresh" (from original PREP (9,21))
            (22, 28, "NAME")  # "ginger"
        ]
    }),

    # Example 19
    ("2 to 3 medium-hot chiles, such as Fresnos or jalapeños, seeded and thinly sliced", {
        "entities": [
            (0, 1, "QTY"),  # "2" (from original QTY (0,6) "2 to 3")
            (2, 6, "ALT_QTY"),  # "to 3" (Following "X to Y" rule)
            (7, 17, "NAME"),  # "medium-hot" (Kept)
            (18, 24, "NAME"),  # "chiles"
            # Comma at 24 is "O"
            (26, 54, "COMMENT"),  # "such as Fresnos or jalapeños" (Kept)
            # Comma at 54 is "O"
            (56, 80, "PREP")  # "seeded and thinly sliced" (Kept)
        ]
    }),

    # Example 20
    ("1 cup Cooked Barley, recipe follows", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "NAME"),  # "Cooked" (from original NAME "Cooked Barley," 6-20)
            (13, 19, "NAME"),  # "Barley" (from original NAME 6-20)
            (21, 35, "COMMENT")  # "recipe follows" (Kept)
        ]
    }),

    # Example 21
    ("1/2 cup quick-cooking barley", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 21, "NAME"),  # "quick-cooking" (from original NAME "quick-cooking barley" 8-28)
            (22, 28, "NAME")  # "barley" (from original NAME "quick-cooking barley" 8-28)
        ]
    }),

    # Example 22
    ("4 (28-ounce) cans Italian plum San Marzano tomatoes", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 12, "COMMENT"),  # "(28-ounce)" (Kept)
            (13, 17, "UNIT"),  # "cans"
            (18, 25, "NAME"),  # "Italian" (from original NAME "Italian plum San Marzano tomatoes" 18-51)
            (26, 30, "NAME"),  # "plum" (from original NAME 18-51)
            (31, 34, "NAME"),  # "San" (from original NAME 18-51)
            (35, 42, "NAME"),  # "Marzano" (from original NAME 18-51)
            (43, 51, "NAME")  # "tomatoes" (from original NAME 18-51)
        ]
    }),

    # Example 23
    ("6 to 8 large Yukon gold potatoes cut into large chunks", {
        "entities": [
            (0, 1, "QTY"),  # "6" (from original QTY (0,6) "6 to 8")
            (2, 6, "ALT_QTY"),  # "to 8"
            (7, 12, "UNIT"),  # "large"
            (13, 18, "NAME"),  # "Yukon" (from original NAME "Yukon gold potatoes" 13-32)
            (19, 23, "NAME"),  # "gold" (from original NAME 13-32)
            (24, 32, "NAME"),  # "potatoes" (from original NAME 13-32)
            (33, 54, "PREP")  # "cut into large chunks" (Kept)
        ]
    }),

    # Example 24
    ("8 ounces sharp-tasting cheese", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 22, "NAME"),  # "sharp-tasting" (from original NAME "sharp-tasting cheese" 9-29)
            (23, 29, "NAME")  # "cheese" (from original NAME "sharp-tasting cheese" 9-29)
        ]
    }),

    # Example 25
    ("3/4 pound, 4 to 5 cups, baby spinach, packed", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 9, "UNIT"),  # "pound"
            # Comma at 9 is "O"
            (11, 23, "COMMENT"),  # "4 to 5 cups," (Kept, includes comma)
            (24, 28, "NAME"),  # "baby" (from original NAME "baby spinach" 24-36)
            (29, 36, "NAME"),  # "spinach" (from original NAME "baby spinach" 24-36)
            # Comma at 36 is "O"
            (38, 44, "PREP")  # "packed" (Kept)
        ]
    }),

    # Example 26
    ("1 1/4 pounds boiled, baked or smoked ham, order thick slices at deli counter", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/4" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 19, "NAME"),  # "boiled" (Kept from original (13,19))
            # Comma at 19 is "O"
            (21, 26, "ALT_NAME"),  # "baked" (Kept from original (21,26))
            (27, 36, "ALT_NAME"),  # "smoked" (Kept from original (27,36) "or smoked")
            (37, 40, "NAME"),  # "ham"
            # Comma at 40 is "O"
            (42, 76, "COMMENT")  # "order thick slices at deli counter" (Kept)
        ]
    }),

    # Example 27
    ("4 cleaned sole fillets (6 ounces each)", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 9, "PREP"), (10, 14, "NAME"), (15, 22, "NAME"),
            (23, 38, "COMMENT")
        ]
    }),

    # Example 28
    ("1/2 cup whole-grain mustard", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 19, "NAME"),  # "whole-grain" (from original NAME "whole-grain mustard" 8-27)
            (20, 27, "NAME")  # "mustard" (from original NAME "whole-grain mustard" 8-27)
        ]
    }),

    # Example 29
    ("1/4 cup sherry", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "NAME")  # "sherry"
        ]
    }),

    # Example 30
    ("1/2 pound smoked sausage or chorizo, cut lengthwise in half, then into 1/4-ince slices", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 16, "NAME"),  # "smoked" (from original NAME "smoked sausage" 10-24)
            (17, 24, "NAME"),  # "sausage" (from original NAME "smoked sausage" 10-24)
            (25, 35, "ALT_NAME"),  # "or chorizo" (Kept)
            # Comma at 35 is "O"
            (37, 79, "PREP")  # "cut lengthwise in half, then into 1/4-inch slices" (Kept, corrected "ince")
        ]
    }),

    # Example 31
    ("3/4 pound whole-wheat dried spaghettini", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 39, "NAME"),  # "whole-wheat"
        ]
    }),

    # Example 32
    ("8 manicotti shells", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 11, "NAME"),  # "manicotti"
            (12, 18, "NAME")  # "shells"
        ]
    }),

    # Example 33
    ("4 ounces good quality white chocolate, broken into pieces", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 13, "PREP"),  # "good" (from original PREP "good quality" 9-21)
            (14, 21, "PREP"),  # "quality" (from original PREP "good quality" 9-21)
            (22, 27, "NAME"),  # "white" (from original NAME "white chocolate" 22-37)
            (28, 37, "NAME"),  # "chocolate" (from original NAME "white chocolate" 22-37)
            # Comma at 37 is "O"
            (39, 57, "PREP")  # "broken into pieces" (Kept)
        ]
    }),

    # Example 34
    ("4 cups mixed baby lettuces, washed and dried", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 12, "NAME"),  # "mixed" (Kept)
            (13, 17, "NAME"),  # "baby" (from original NAME "baby lettuces" 13-26)
            (18, 26, "NAME"),  # "lettuces" (from original NAME "baby lettuces" 13-26)
            # Comma at 26 is "O"
            (28, 44, "PREP")  # "washed and dried" (Kept)
        ]
    }),

    # Example 35
    ("2 (6-ounce) center-cut Ahi tuna fillets, seasoned with freshly cracked coriander seeds, cracked black pepper, and kosher salt, to taste",
     {
         "entities": [
             (0, 1, "QTY"),  # "2" (Kept)
             (2, 11, "COMMENT"),  # "(6-ounce)" (Kept)
             (12, 22, "PREP"),  # "center-cut" (Kept)
             (23, 26, "NAME"),  # "Ahi" (from original NAME "Ahi tuna fillets" 23-39)
             (27, 31, "NAME"),  # "tuna" (from original NAME 23-39)
             (32, 39, "NAME"),  # "fillets" (from original NAME 23-39)
             # Comma at 39 is "O"
             (41, 126, "PREP")
             # "seasoned with freshly cracked coriander seeds, cracked black pepper, and kosher salt, to taste" (Kept)
         ]
     }),

    # Example 36
    ("1 cup Nigoise olives, pitted", {  # Assuming "Nigoise" is a typo for "Nicoise"
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 13, "NAME"),  # "Nicoise" (from original NAME "Nicoise olives" 6-20, corrected typo)
            (14, 20, "NAME"),  # "olives" (from original NAME "Nicoise olives" 6-20)
            # Comma at 20 is "O"
            (22, 28, "PREP")  # "pitted" (Kept)
        ]
    }),

    # Example 37
    ("1/4 cup Japanese pickled ginger, available in Japanese specialty shops (optional)", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 16, "NAME"),  # "Japanese" (from original NAME "Japanese pickled ginger" 8-31)
            (17, 24, "NAME"),  # "pickled" (from original NAME 8-31)
            (25, 31, "NAME"),  # "ginger" (from original NAME 8-31)
            # Comma at 31 is "O"
            (33, 81, "COMMENT")  # "available in Japanese specialty shops (optional)" (Kept)
        ]
    }),

    # Example 38
    ("1 tablespoon blackened seasoning", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 22, "NAME"),  # "blackened" (from original NAME "blackened seasoning" 13-32)
            (23, 32, "NAME")  # "seasoning" (from original NAME "blackened seasoning" 13-32)
        ]
    }),

    # Example 39
    ("2 medium or 1 large head kale, stem end removed", {
        "entities": [
            # Primary Item description
            (0, 1, "QTY"),         # "2"
            (2, 8, "UNIT"),        # "medium"
            (9,11,'ALT_NAME'),
            # Alternative description for the same item
            (12, 13, "ALT_QTY"),   # "1"
            (14, 19, "ALT_UNIT"),  # "large"
            # Common Unit/Form for both
            (20, 24, "UNIT"),      # "head"
            # Core Item Name
            (25, 29, "NAME"),      # "kale"
            # Comma at 29 is O
            # Preparation
            (31, 47, "PREP")       # "stem end removed"
        ]
    }),

    # Example 40
    ("4 ounces smoked yellow Cheddar, freshly shredded", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 15, "NAME"),  # "smoked" (Kept)
            (16, 22, "NAME"),  # "yellow" (from original NAME "yellow Cheddar" 16-30)
            (23, 30, "NAME"),  # "Cheddar" (from original NAME "yellow Cheddar" 16-30)
            # Comma at 30 is "O"
            (32, 48, "PREP"),  # "freshly" (from original PREP "freshly shredded" 32-48)
        ]
    }),

    # Example 41
    ("Rice bran oil, for frying", {
        "entities": [
            (0, 4, "NAME"),  # "Rice" (from original NAME "Rice bran oil" 0-13)
            (5, 9, "NAME"),  # "bran" (from original NAME 0-13)
            (10, 13, "NAME"),  # "oil" (from original NAME 0-13)
            # Comma at 13 is "O"
            (15, 25, "COMMENT")  # "for frying" (Kept)
        ]
    }),

    ("Several dashes hot pepper sauce", {  # If "Several dashes" was one COMMENT
        "entities": [
            (0, 14, "COMMENT"),
            (15, 18, "NAME"), (19, 25, "NAME"), (26, 31, "NAME")
        ]
    }),

    # Example 43 (Duplicate)
    ("1/4 cup diced red pepper", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "PREP"), (14, 17, "NAME"), (18, 24, "NAME")  # red, pepper
        ]
    }),

    # Example 44
    ("1 cup julienned heart of romaine", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 15, "PREP"),  # "julienned" (Kept)
            (16, 32, "NAME"),  # "heart
        ]
    }),

    # Example 45
    ("1 1/2 cups Italian-style breadcrumbs", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 24, "NAME"),  # "Italian-style" (from original NAME "Italian-style breadcrumbs" 11-36)
            (25, 36, "NAME")  # "breadcrumbs" (from original NAME "Italian-style breadcrumbs" 11-36)
        ]
    }),

    # Example 46
    ("2 teaspoons smoked sweet paprika", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 11, "UNIT"),  # "teaspoons"
            (12, 18, "NAME"),  # "smoked" (from original NAME "smoked sweet paprika" 12-32)
            (19, 24, "NAME"),  # "sweet" (from original NAME 12-32)
            (25, 32, "NAME")  # "paprika" (from original NAME 12-32)
        ]
    }),

    # Example 47
    ("1 (4 to 5-ounce) piece semisweet chocolate", {
        "entities": [
            (0, 1, "COMMENT"),  # "1" (Original label COMMENT)
            (3, 4, "QTY"),  # "4" (Original QTY (3,4))
            (5, 10, "ALT_QTY"),
            # "to 5-" (Original UNIT (10,15) "ounce" - your spans (3,4 QTY) (10,15 UNIT) are for "4" and "ounce". "to 5-" is in between)
            # This is messy. Assuming (3,16,"COMMENT") for "(4 to 5-ounce) piece"
            (10, 15, "UNIT"),  # "ounce)" - Original had UNIT for ounce.
            (17, 22, "COMMENT"),  # "piece" (Original COMMENT (17,22))
            (23, 32, "NAME"),  # "semisweet" (from original NAME "semisweet chocolate" 23-42)
            (33, 42, "NAME")  # "chocolate" (from original NAME "semisweet chocolate" 23-42)
        ]
    }),

    # Example 48
    ("2 cups cooked Arborio rice", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 13, "PREP"),  # "cooked" (Kept)
            (14, 21, "NAME"),  # "Arborio" (from original NAME "Arborio rice" 14-26)
            (22, 26, "NAME")  # "rice" (from original NAME "Arborio rice" 14-26)
        ]
    }),

    # Example 49
    ("2 tablespoons warm water, for blooming the saffron", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 18, "COMMENT"),  # "warm" (Original label COMMENT)
            (19, 24, "NAME"),  # "water"
            # Comma at 24 is "O"
            (26, 50, "COMMENT")  # "for blooming the saffron" (Kept)
        ]
    }),

    # Example 50
    ("16 ounces Greek or Bulgarian feta cheese, drained", {
        "entities": [
            (0, 2, "QTY"),  # "16" (Kept)
            (3, 9, "UNIT"),  # "ounces"
            (10, 15, "NAME"),  # "Greek"
            (16, 28, "ALT_NAME"),  # "or Bulgarian" (Kept)
            (29, 33, "NAME"),  # "feta" (from original NAME "feta cheese" 29-40)
            (34, 40, "NAME"),  # "cheese" (from original NAME "feta cheese" 29-40)
            # Comma at 40 is "O"
            (42, 49, "PREP")  # "drained" (Kept)
        ]
    }),

    # Example 51

    ("1/4 pound, 4 or 5 slices, pancetta*, chopped (See Cook's Note)", {  # If comment included parens
        "entities": [
            (0, 3, "QTY"), (4, 9, "UNIT"), (11, 24, "COMMENT"), (26, 35, "NAME"),
            (37, 44, "PREP"), (45, 62, "COMMENT")
        ]
    }),

    # Example 52
    ("2 tablespoons dried rose petals", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 19, "PREP"),  # "dried" (Kept)
            (20, 24, "NAME"),  # "rose" (from original NAME "rose petals" 20-31)
            (25, 31, "NAME")  # "petals" (from original NAME "rose petals" 20-31)
        ]
    }),

    # Example 53
    ("2 pounds fresh, young peas in their pods, about 2 cups shelled", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 21, "PREP"),  # "fresh" (Kept from original (9,21,"PREP") "fresh, young")
            (22, 26, "NAME"),  # "peas"
            (27, 62, "COMMENT")  # "in their pods, about 2 cups shelled" (Kept)
        ]
    }),

    # Example 54
    ("1/2 ounce ogo seaweed", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "ounce"
            (10, 13, "NAME"),  # "ogo" (from original NAME "ogo seaweed" 10-21)
            (14, 21, "NAME")  # "seaweed" (from original NAME "ogo seaweed" 10-21)
        ]
    }),

    # Example 55
    ("1 gallon apple", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "UNIT"),  # "gallon"
            (9, 14, "NAME")  # "apple"
        ]
    }),

    # Example 56
    ("2 pinches Hawaiian sea salt or pink Himalayan salt", {  # If "or pink Himalayan salt" was one ALT_NAME
        "entities": [
            (0, 1, "QTY"), (2, 9, "COMMENT"),
            (10, 18, "NAME"), (19, 22, "NAME"), (23, 27, "NAME"),
            (28, 50, "ALT_NAME")
        ]
    }),

    # Example 57
    ("One 7-ounce steak", {
        "entities": [
            (0, 3, "COMMENT"),  # "One" (Original label COMMENT)  (5,6,"QTY"),          # "7" - Assuming this was QTY
            (4, 5, "QTY"),  # "ounce" - Assuming this was UNIT
            (6, 11, "UNIT"),  # "ounce" - Assuming this was UNIT
            (12, 17, "NAME")  # "steak" (Original label for "steak" was NAME (12,17) which included closing paren)
        ]
    }),

    # Example 58
    ("5 pounds elk or venison, use fairly good quality meat", {
        "entities": [
            (0, 1, "QTY"),  # "5" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 12, "NAME"),  # "elk"
            (13, 23, "ALT_NAME"),  # "or venison" (Kept)
            # Comma at 23 is "O"
            (25, 53, "COMMENT")  # "use fairly good quality meat" (Kept)
        ]
    }),

    # Example 59
    ("1/2 cup finely ground or quick-cooking polenta", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 21, "PREP"),  # "finely" (from original PREP "finely ground or quick-cooking" 8-38)
            (22, 38, "PREP"),  # "or" (from original PREP 8-38) - *Unusual*
            (39, 46, "NAME")  # "polenta"
        ]
    }),

    # Example 61
    ("1 pound uncooked heirloom beans (Anasazi, butterscotch calypso, cranberry calypso and chestnut limas)",
     {  # If comment included parens
         "entities": [
             (0, 1, "QTY"), (2, 7, "UNIT"), (8, 16, "PREP"), (17, 25, "NAME"), (26, 31, "NAME"),
             (32, 100, "COMMENT")
         ]
     }),

    # Example 62
    ("1 tablespoon minced Roasted Garlic, recipe follows", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 19, "PREP"),  # "minced" (Kept)
            (20, 27, "NAME"),  # "Roasted" (from original NAME "Roasted Garlic" 20-34)
            (28, 34, "NAME"),  # "Garlic" (from original NAME "Roasted Garlic" 20-34)
            # Comma at 34 is "O"
            (36, 50, "COMMENT")  # "recipe follows" (Kept)
        ]
    }),

    # Example 63
    ("1/4 cup plus 2 tablespoons and a pinch of smoky maple seasoning, such as McCormick® Grill Mates® Smokehouse Maple Seasoning",
     {
         "entities": [
             (0, 3, "QTY"),  # "1/4" (Kept)
             (4, 7, "UNIT"),  # "cup"
             (8, 38, "COMMENT"),  # "plus 2 tablespoons and a pinch" (Kept)
             (39, 41, "PREP"),  # "of" (Kept)
             (42, 47, "NAME"),  # "smoky" (from original NAME "smoky maple seasoning" 42-63)
             (48, 53, "NAME"),  # "maple" (from original NAME 42-63)
             (54, 63, "NAME"),  # "seasoning" (from original NAME 42-63)
             # Comma at 63 is "O"
             (65, 123, "COMMENT")  # "such as McCormick® Grill Mates® Smokehouse Maple Seasoning" (Kept)
         ]
     }),

    # Example 64
    ("About 18 ounces 72% chocolate in bars", {
        "entities": [
            (0, 5, "COMMENT"),  # "About" (Kept)
            (6, 8, "QTY"),  # "18" (Kept)
            (9, 15, "UNIT"),  # "ounces"
            (16, 19, "PREP"),  # "72%" (Kept)
            (20, 29, "NAME"),  # "chocolate"
            (30, 37, "COMMENT")  # "in bars" (Kept)
        ]
    }),

    # Example 65
    ("About 1/11 ounce agar agar", {
        "entities": [
            (0, 5, "COMMENT"),  # "About" (Kept)
            (6, 10, "QTY"),  # "1/11" (Kept)
            (11, 16, "UNIT"),  # "ounce"
            (17, 21, "NAME"),  # "agar" (from original NAME "agar agar" 17-26)
            (22, 26, "NAME")  # "agar" (from original NAME "agar agar" 17-26)
        ]
    }),

    # Example 66
    ("1/2 teaspoon plus a pinch ground nutmeg", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 25, "COMMENT"),  # "plus a pinch" (Kept)
            (26, 32, "PREP"),  # "ground" (Kept)
            (33, 39, "NAME")  # "nutmeg"
        ]
    }),

    # Example 67 & 68 (Same text, assuming same annotation intent)
    ("1 14.5-ounce can fire-roasted diced tomatoes", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "COMMENT"),  # "14.5-ounce" (Kept)
            (13, 16, "UNIT"),  # "can"
            (17, 29, "NAME"),  # "fire-roasted" (from original NAME "fire-roasted diced tomatoes" 17-44)
            (30, 35, "NAME"),  # "diced" (from original NAME 17-44)
            (36, 44, "NAME")  # "tomatoes" (from original NAME 17-44)
        ]
    }),

    # Example 69
    ("2 teaspoons Quick Preserved Lemons, mashed, recipe follows", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 11, "UNIT"),  # "teaspoons"
            (12, 27, 'COMMENT'),  # "Quick" (Original label COMMENT)
            (28, 34, "NAME"),  # "Lemons" (from original NAME "Preserved Lemons" 18-34)
            # Comma at 34 is "O"
            (36, 42, "PREP"),  # "mashed" (Kept)
            # Comma at 42 is "O"
            (44, 58, "COMMENT")  # "recipe follows" (Kept)
        ]
    }),

    # Example 70
    ("2 pounds beefsteak tomatoes, halved and seeded", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 18, "NAME"),  # "beefsteak" (from original NAME "beefsteak tomatoes" 9-27)
            (19, 27, "NAME"),  # "tomatoes" (from original NAME "beefsteak tomatoes" 9-27)
            # Comma at 27 is "O"
            (29, 46, "PREP")  # "halved and seeded" (Kept)
        ]
    }),

    # Example 71
    ("4 cups packed roughly chopped broccoli rabe or mustard greens", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 13, "PREP"),  # "packed" (from original PREP "packed roughly chopped" 7-29)
            (14, 21, "PREP"),  # "roughly" (from original PREP 7-29)
            (22, 29, "PREP"),  # "chopped" (from original PREP 7-29)
            (30, 38, "NAME"),  # "broccoli" (from original NAME "broccoli rabe" 30-43)
            (39, 43, "NAME"),  # "rabe" (from original NAME "broccoli rabe" 30-43)
            (44, 61, "ALT_NAME")  # "or mustard greens" (Kept)
        ]
    }),

    # Example 72
    ("1 (1/4-inch thick) slice pancetta", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 18, "COMMENT"), (19, 24, "PREP"), (25, 33, "NAME")
        ]
    }),

    # Example 73
    ("2 small scoops vanilla ice cream, for serving", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 7, "UNIT"),  # "small"
            (8, 14, "COMMENT"),  # "scoops" (Original label COMMENT)
            (15, 22, "NAME"),  # "vanilla" (from original NAME "vanilla ice cream" 15-32)
            (23, 26, "NAME"),  # "ice" (from original NAME 15-32)
            (27, 32, "NAME"),  # "cream" (from original NAME 15-32)
            # Comma at 32 is "O"
            (34, 45, "COMMENT")  # "for serving" (Kept)
        ]
    }),

    # Example 74
    ("Heaping 1/4 teaspoon baking powder", {
        "entities": [
            (0, 7, "PREP"),  # "Heaping" (Kept)
            (8, 11, "QTY"),  # "1/4" (Kept)
            (12, 20, "UNIT"),  # "teaspoon"
            (21, 27, "NAME"),  # "baking" (from original NAME "baking powder" 21-34)
            (28, 34, "NAME")  # "powder" (from original NAME "baking powder" 21-34)
        ]
    }),

    # Example 75
    ("1/2 cup dark or light corn syrup", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "NAME"),  # "dark" (from original ALT_NAME "dark or light" 8-21)
            (13, 21, "ALT_NAME"),  # "or" (from ALT_NAME 8-21) - *Unusual*
            (22, 26, "NAME"),  # "corn" (from original NAME "corn syrup" 22-32)
            (27, 32, "NAME")  # "syrup" (from original NAME "corn syrup" 22-32)
        ]
    }),

    # Example 76
    ("1/3 cup (packed) chiffonade of fresh basil", {  # If comments/preps included parens and "fresh basil" is NAME
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 16, "COMMENT"), (17, 27, "PREP"),  # chiffonade
            (28, 30, "PREP"),  # of
            (31, 36, "PREP"),  # fresh
            (37, 42, "NAME")  # basil
        ]
    }),

    # Example 77
    ("2 legs of goat (4 to 5 pounds total)", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 6, "NAME"), (7, 9, "NAME"), (10, 14, "NAME"),
            (15, 36, "COMMENT")
        ]
    }),

    # Example 78
    ("2 bone-in racks of goat (2 to 3 pounds total) bones frenched",
     {  # Simpler if original COMMENT for weight was separate
         "entities": [
             (0, 1, "QTY"),  # Assuming 2 is QTY for racks
             (2, 9, "NAME"), (10, 15, "NAME"), (16, 18, "NAME"), (19, 23, "NAME"),  # bone-in racks of goat
             (24, 45, "COMMENT"),  # "(2 to 3 pounds total)"
             (46, 60, "PREP")  # "bones frenched"
         ]
     }),

    # Example 79
    ("16 butterball potatoes", {
        "entities": [
            (0, 2, "QTY"),  # "16" (Kept)
            (3, 13, "NAME"),  # "butterball" (from original NAME "butterball potatoes" 3-22)
            (14, 22, "NAME")  # "potatoes" (from original NAME "butterball potatoes" 3-22)
        ]
    }),

    # Example 80
    ("1 red, orange or yellow bell pepper, diced", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "NAME"),  # "red"
            # Comma at 5 is "O"
            (7, 13, "ALT_NAME"),  # "orange" (from original ALT_NAME "orange or yellow" 7-23)
            (14, 23, "ALT_NAME"),  # "or" (from ALT_NAME 7-23) - *Unusual*
            (24, 28, "NAME"),  # "bell" (from original NAME "bell pepper" 24-35)
            (29, 35, "NAME"),  # "pepper" (from original NAME "bell pepper" 24-35)
            # Comma at 35 is "O"
            (37, 42, "PREP")  # "diced" (Kept)
        ]
    }),

    # Example 81
    ("1 cup thinly sliced red radishes", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 19, "PREP"),  # "thinly" (from original PREP "thinly sliced" 6-19)
            (20, 23, "NAME"),  # "red" (from original NAME "red radishes" 20-32)
            (24, 32, "NAME")  # "radishes" (from original NAME "red radishes" 20-32)
        ]
    }),

    # Example 82
    ("1/4 cup cider vinegar", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "NAME"),  # "cider" (from original NAME "cider vinegar" 8-21)
            (14, 21, "NAME")  # "vinegar" (from original NAME "cider vinegar" 8-21)
        ]
    }),

    # Example 83
    ("One 10-ounce package falafel mix, such as Casbah", {
        "entities": [
            (0, 3, "QTY"),  # "One" (Kept)
            (4, 12, "COMMENT"),  # "10-ounce" (Kept)
            (13, 20, "UNIT"),  # "package"
            (21, 28, "NAME"),  # "falafel" (from original NAME "falafel mix" 21-32)
            (29, 32, "NAME"),  # "mix" (from original NAME "falafel mix" 21-32)
            # Comma at 32 is "O"
            (34, 48, "COMMENT")  # "such as Casbah" (Kept)
        ]
    }),

    # Example 84
    ("2 cups of your favorite granola", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 23, "PREP"),  # "of" (Kept)
            (24, 31, "NAME")  # "granola"
        ]
    }),

    # Example 85
    ("1/4 cup cider vinegar, or more to taste", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "NAME"),  # "cider" (from original NAME "cider vinegar" 8-21)
            (14, 21, "NAME"),  # "vinegar" (from original NAME "cider vinegar" 8-21)
            # Comma at 21 is "O"
            (23, 39, "COMMENT")  # "or more to taste" (Kept)
        ]
    }),

    # Example 86
    ("Jim's Really Easy and Really Good Barbecue Sauce, recipe follows", {  # If name was split
        "entities": [
            (0, 33, "COMMENT"), (34, 42, "NAME"), (43, 48, "NAME"),
            (50, 64, "COMMENT")
        ]
    }),
    # Example 87
    ("1 (5 to 6-pound) center-cut piece of brisket", {
        "entities": [
            (0, 1, "COMMENT"),  # "1" (Original label COMMENT)\
            (3, 4, "QTY"),  # "5" (Original QTY (3,4))
            (5, 10, "ALT_QTY"),  # "to 6-" (Assuming this is how "to 6-pound" was intended to be ALT_NAME for range)
            (10, 15, "UNIT"),  # "pound" (Original UNIT (10,15))
            (17, 27, "PREP"),  # "center-cut" (Kept from original PREP (17,36) "center-cut piece of")
            (28, 33, "PREP"),  # "piece" (from PREP 17-36)
            (34, 36, "PREP"),  # "of" (from PREP 17-36) - *Unusual*
            (37, 44, "NAME")  # "brisket"
        ]
    }),

    # Example 88
    ("2 cups your favorite barbecue sauce, (recommended: KC Masterpiece or Bull's Eye)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 20, "COMMENT"),  # "your favorite" (Kept)
            (21, 29, "NAME"),  # "barbecue" (from original NAME "barbecue sauce" 21-35)
            (30, 35, "NAME"),  # "sauce" (from original NAME "barbecue sauce" 21-35)
            # Comma at 35 is "O"
            (37, 80, "COMMENT"),  # "recommended: KC Masterpiece or Bull's Eye" (from original COMMENT (37,80))
        ]
    }),

    # Example 89
    ("1 to 2 cups your favorite mild or hot salsa", {
        "entities": [
            (0, 1, "QTY"),  # "1" (From original QTY (0,1))
            (2, 6, "ALT_QTY"),  # "to 2" (From original ALT_NAME (2,6))
            (7, 11, "UNIT"),  # "cups"
            (12, 25, "COMMENT"),  # "your favorite" (Kept)
            (26, 30, "NAME"),  # "mild" (Kept from original (26,30))
            (31, 37, "ALT_NAME"),  # "or hot" (Kept from original (31,37))
            (38, 43, "NAME")  # "salsa"
        ]
    }),

    # Example 90
    ("1 cup of safflower oil or vegetable oil", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 8, "PREP"),  # "of" (Kept)
            (9, 18, "NAME"),  # "safflower" (from original NAME "safflower oil" 9-22)
            (19, 22, "NAME"),  # "oil" (from original NAME "safflower oil" 9-22)
            (23, 39, "ALT_NAME")  # "or vegetable oil" (Kept)
        ]
    }),

    # Example 92
    ("6 leaves and 3 heads from fresh passion flowers", {
        "entities": [
            (0, 8, "COMMENT"),  # "6 leaves" (Kept)
            (9, 12, "PREP"),  # "and" (Original label PREP) - *Unusual*
            (13, 14, "QTY"),  # "3" (Kept)
            (15, 20, "UNIT"),  # "heads"
            (21, 25, "PREP"),  # "from" (Kept)
            (26, 31, "PREP"),  # "fresh" (from original NAME "fresh passion flowers" 26-47)
            (32, 39, "NAME"),  # "passion" (from original NAME 26-47)
            (40, 47, "NAME")  # "flowers" (from original NAME 26-47)
        ]
    }),

    # Example 93
    ("3 3/4 cups full-fat milk", {
        "entities": [
            (0, 5, "QTY"),  # "3 3/4" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 19, "NAME"),  # "full-fat" (from original NAME "full-fat milk" 11-24)
            (20, 24, "NAME")  # "milk" (from original NAME "full-fat milk" 11-24)
        ]
    }),

    # Example 94
    ("1 3/4 ounces dark chocolate (minimum 50-percent cocoa solids)", {
        "entities": [
            (0, 5, "QTY"),  # "1 3/4" (Kept)
            (6, 12, "UNIT"),  # "ounces"
            (13, 17, "NAME"),  # "dark" (from original NAME "dark chocolate" 13-27)
            (18, 27, "NAME"),  # "chocolate" (from original NAME "dark chocolate" 13-27)
            (28, 61, "COMMENT"),  # "minimum 50-percent cocoa solids" (from original COMMENT (28,61))
        ]
    }),

    # Example 95
    ("Dash vanilla extract", {
        "entities": [
            (0, 4, "COMMENT"),  # "Dash" (Original label COMMENT)
            (5, 12, "NAME"),  # "vanilla" (from original NAME "vanilla extract" 5-20)
            (13, 20, "NAME")  # "extract" (from original NAME "vanilla extract" 5-20)
        ]
    }),

    # Example 96
    ("1 cup thinly sliced white button mushroom", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "PREP"),  # "thinly" (from original PREP "thinly sliced" 6-19)
            (13, 19, "PREP"),  # "sliced" (from original PREP "thinly sliced" 6-19)
            (20, 25, "NAME"),  # "white" (from original NAME "white button mushroom" 20-41)
            (26, 32, "NAME"),  # "button" (from original NAME 20-41)
            (33, 41, "NAME")  # "mushroom" (from original NAME 20-41)
        ]
    }),

    # Example 97
    ("1 cup sliced strawberries", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "NAME"),  # "sliced" (Kept)
            (13, 25, "NAME")  # "strawberries"
        ]
    }),

    # Example 98
    ("1/2 teaspoon, plus pinch cayenne", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            # Comma at 12 is "O"
            (14, 24, "COMMENT"),  # "plus pinch" (Kept)
            (25, 32, "NAME")  # "cayenne"
        ]
    }),

    # Example 99
    ("1 1/2 pounds meatloaf mix", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 21, "NAME"),  # "meatloaf" (from original NAME "meatloaf mix" 13-25)
            (22, 25, "NAME")  # "mix" (from original NAME "meatloaf mix" 13-25)
        ]
    }),

    # Example 100
    ("1 3/4 to 2 pounds top round, sliced into 4 to 6 long slices about 1/4-inch thick", {
        "entities": [
            (0, 5, "QTY"),  # "1 3/4" (Kept from original (0,5,"QTY"))
            (6, 10, 'ALT_QTY'),  # "to 2" (Kept from original (6,10,"ALT_NAME"))
            (11, 17, "UNIT"),  # "pounds"
            (18, 21, "NAME"),  # "top" (from original NAME "top round" 18-27)
            (22, 27, "NAME"),  # "round" (from original NAME "top round" 18-27)
            # Comma at 27 is "O"
            (29, 74, "PREP")
            # "sliced into 4 to 6 long slices about 1/4-inch thick" (Kept, original end 74 for "thick")
        ]
    }),

    # Example 101
    ("3 tablespoons chopped parsley leaves", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, "PREP"),  # "chopped" (Kept)
            (22, 29, "NAME"),  # "parsley" (from original NAME "parsley leaves" 22-36)
            (30, 36, "NAME")  # "leaves" (from original NAME "parsley leaves" 22-36)
        ]
    }),

    # Example 102
    ("2 cups/500 ml flour, plus more for dusting and as needed", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 10, "UNIT"),  # "cups/500" (Kept as original UNIT span)
            (11, 13, "COMMENT"),  # "ml" (Kept as original COMMENT span)
            (14, 19, "NAME"),  # "flour"
            # Comma at 19 is "O"
            (21, 56, "COMMENT")  # "plus more for dusting and as needed" (Kept)
        ]
    }),

    # Example 103
    ("1 cup/250 ml dry porcini", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 9, "UNIT"),  # "cup/250" (Kept)
            (10, 12, "COMMENT"),  # "ml" (Kept)
            (13, 16, "NAME"),  # "dry" (from original NAME "dry porcini" 13-24)
            (17, 24, "NAME")  # "porcini" (from original NAME "dry porcini" 13-24)
        ]
    }),

    # Example 104
    ("1 cup/250 ml finely grated Parmigiano cheese", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 9, "UNIT"),  # "cup/250" (Kept)
            (10, 12, "COMMENT"),  # "ml" (Kept)
            (13, 19, "PREP"),  # "finely" (from original PREP "finely grated" 13-26)
            (20, 26, "NAME"),  # "grated" (from original PREP "finely grated" 13-26)
            (27, 37, "NAME"),  # "Parmigiano" (from original NAME "Parmigiano cheese" 27-44)
            (38, 44, "NAME")  # "cheese" (from original NAME "Parmigiano cheese" 27-44)
        ]
    }),

    # Example 106
    ("1 pound fresh broccoli rabe, separate", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 13, "PREP"),  # "fresh" (Kept)
            (14, 22, "NAME"),  # "broccoli" (from original NAME "broccoli rabe" 14-27)
            (23, 27, "NAME"),  # "rabe" (from original NAME "broccoli rabe" 14-27)
            # Comma at 27 is "O"
            (29, 37, "COMMENT")  # "separate" (Kept)
        ]
    }),

    # Example 107
    ("1 can of your favorite beer", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "can"
            (6, 8, "PREP"),  # "of" (Kept)
            (9, 22, "COMMENT"),  # "your favorite" (Kept)
            (23, 27, "NAME")  # "beer"
        ]
    }),

    # Example 108
    ("1 pound mixed chopped meat (veal, pork and beef)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 21, "PREP"),  # "mixed" (from original PREP "mixed chopped" 8-21)
            (22, 26, "NAME"),  # "meat"
            (27, 48, "COMMENT"),  # "veal, pork and beef" (from original COMMENT (27,48))
        ]
    }),

    # Example 109
    ("A few pinches grated Locatelli Romano", {
        "entities": [
            (0, 5, "QTY"),  # "A few" (Kept)
            (6, 13, "UNIT"),  # "pinches"
            (14, 20, "PREP"),  # "grated" (Kept)
            (21, 30, "NAME"),  # "Locatelli" (from original NAME "Locatelli Romano" 21-37)
            (31, 37, "NAME")  # "Romano" (from original NAME "Locatelli Romano" 21-37)
        ]
    }),

    # Example 110
    ("1/2 cup drained seaweed (soaked in water and squeezed dry)", {  # If comment included parens
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "PREP"), (16, 23, "NAME"),
            (24, 58, "COMMENT")
        ]
    }),

    # Example 111
    ("2 pounds thinly sliced veal scallopine", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 15, "PREP"),  # "thinly" (from original PREP "thinly sliced" 9-22)
            (16, 22, "PREP"),  # "sliced" (from original PREP "thinly sliced" 9-22)
            (23, 27, "NAME"),  # "veal" (from original NAME "veal scallopine" 23-38)
            (28, 38, "NAME")  # "scallopine" (from original NAME "veal scallopine" 23-38)
        ]
    }),

    # Example 112
    ("2 pounds (6 to 8) frog legs, split", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 17, "COMMENT"),
            (18, 22, "NAME"), (23, 27, "NAME"), (29, 34, "PREP")
        ]
    }),

    # Example 113
    ("1 1/2 cups 64% chocolate", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 14, "PREP"),  # "64%" (Kept)
            (15, 24, "NAME")  # "chocolate"
        ]
    }),

    # Example 114
    ("27 ounces (about 4 cups) sungold or cherry tomatoes, halved",
     {  # If comment included parens and ALT_NAME was "or cherry"
         "entities": [
             (0, 2, "QTY"), (3, 9, "UNIT"), (10, 24, "COMMENT"), (25, 32, "NAME"),
             (33, 42, "ALT_NAME"),  # "or cherry"
             (43, 51, "NAME"), (53, 59, "PREP")
         ]
     }),

    # Example 115
    ("1 pound ground meatloaf mix, such as beef, pork and veal", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 14, "PREP"),  # "ground" (Kept)
            (15, 23, "NAME"),  # "meatloaf" (from original NAME "meatloaf mix" 15-27)
            (24, 27, "NAME"),  # "mix" (from original NAME "meatloaf mix" 15-27)
            # Comma at 27 is "O"
            (29, 56, "COMMENT")  # "such as beef, pork and veal" (Kept)
        ]
    }),

    # Example 116
    ("7 lasagna noodles", {
        "entities": [
            (0, 1, "QTY"),  # "7" (Kept)
            (2, 9, "NAME"),  # "lasagna"
            (10, 17, "NAME")  # "noodles"
        ]
    }),

    # Example 117
    ("3 tablespoons grade A maple syrup", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 19, "NAME"),  # "grade" (from original NAME "grade A maple syrup" 14-32)
            (20, 21, "NAME"),  # "A" (from original NAME 14-32)
            (22, 27, "NAME"),  # "maple" (from original NAME 14-32)
            (28, 33, "NAME")  # "syrup" (from original NAME 14-32)
        ]
    }),

    # Example 118
    ("1/4 cup cider vinegar, eyeball it", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "NAME"),  # "cider"
            (14, 21, "NAME"),  # "vinegar"
            # Comma at 21 is "O"
            (23, 33, "COMMENT")  # "eyeball it" (Kept)
        ]
    }),

    # Example 119
    ("2 boxes corn muffin mix", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 7, "COMMENT"),  # "boxes" (Original label COMMENT)
            (8, 12, "NAME"),  # "corn" (from original NAME "corn muffin mix" 8-23)
            (13, 19, "NAME"),  # "muffin" (from original NAME 8-23)
            (20, 23, "NAME")  # "mix" (from original NAME 8-23)
        ]
    }),

    # Example 120
    ("1 small box biscuit mix (preferred brand Jiffy Mix)",
     {  # If (20,50,"COMMENT") was for "mix(preferred brand Jiffy Mix)"
         "entities": [
             (0, 1, "QTY"), (2, 7, "UNIT"), (8, 11, "COMMENT"), (12, 23, "NAME"),
             (24, 50, "COMMENT")
         ]
     }),

    # Example 121
    ("1 quart chicken broth or stock, canned or paper container", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "quart"
            (8, 15, "NAME"),  # "chicken" (from original NAME "chicken broth" 8-21)
            (16, 21, "NAME"),  # "broth" (from original NAME "chicken broth" 8-21)
            (22, 31, "ALT_NAME"),  # "or stock," (Kept, includes comma)
            (32, 57, "COMMENT")  # "canned or paper container" (Kept)
        ]
    }),

    # Example 122
    ("1/2 cup sliced, pitted green olives", {  # If (8,22,"PREP") "sliced, pitted"
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 22, "PREP"),
            (23, 28, "NAME"), (29, 35, "NAME")
        ]
    }),

    # Example 123
    ("1 (32-ounce) jar your favorite marinara sauce, divided", {
        "entities": [
            (0, 1, "COMMENT"),  # "1" (Kept as original COMMENT span)
            (3, 5, "QTY"),  # "32" (Kept as original QTY span)
            (6, 11, "UNIT"),  # "ounce" (Original label was UNIT)
            (13, 16, "COMMENT"),  # "jar" (Kept as original COMMENT span)
            (17, 30, "COMMENT"),  # "your favorite" (Kept as one COMMENT span)
            (31, 39, "NAME"),  # "marinara" (from original NAME "marinara sauce" 31-45)
            (40, 45, "NAME"),  # "sauce" (from original NAME "marinara sauce" 31-45)
            # Comma at 45 is "O"
            (47, 54, "COMMENT")  # "divided" (Kept as original COMMENT span)
        ]
    }),

    # Example 124
    ("4 cups Red Wine Marinade, recipe follows", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 10, "NAME"),  # "Red" (from original NAME "Red Wine Marinade" 7-24)
            (11, 15, "NAME"),  # "Wine" (from original NAME 7-24)
            (16, 24, "NAME"),  # "Marinade" (from original NAME 7-24)
            # Comma at 24 is "O"
            (26, 40, "COMMENT")  # "recipe follows" (Kept)
        ]
    }),

    # Example 125
    ("1 pound beef osso buco (shank)", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 12, "NAME"), (13, 17, "NAME"), (18, 22, "NAME"),
            (23, 30, "COMMENT")
        ]
    }),

    # Example 126
    ("1/4 cup chopped fresh ginger root", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "PREP"),  # "chopped" (Kept from original (8,21,"PREP") "chopped fresh")
            (16, 21, "PREP"),  # "fresh" (from original PREP 8-21)
            (22, 28, "NAME"),  # "ginger" (from original NAME "ginger root" 22-33)
            (29, 33, "NAME")  # "root" (from original NAME "ginger root" 22-33)
        ]
    }),
    # Re-annotated data based on the FINAL REFINED rules:
    # - NAME entities are broken into word-level NAME entities.
    # - COMMENT, PREP, ALT_NAME, QTY entities are kept as single, original spans.
    #   - QTY entities like "4 to 8": "4" is QTY, "to 8" is ALT_NAME (as per your specific instruction for ranges).
    #     If original QTY span was "4 to 8", it's kept as a single QTY.
    # - UNIT entities are single words.
    # - Parentheses and Commas (that are not part of a kept COMMENT/PREP/ALT_NAME/QTY span)
    #   are "O" (and thus not listed in the 'entities' list).
    # - "or" in ALT_NAME is kept if it was part of your original ALT_NAME span.
    # Tokenization based on spaCy's default English tokenizer.

    # ... (all previous examples from your earlier chunks would be here) ...

    # Example 1
    ("1/4 pound dry cured and smoked speck ham, thinly sliced", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 13, "PREP"),  # "dry" (from original PREP "dry cured and smoked" 10-30)
            (14, 19, "PREP"),  # "cured" (from PREP 10-30)
            (20, 23, "PREP"),  # "and" (from PREP 10-30) - *Unusual*
            (24, 30, "NAME"),  # "smoked" (from PREP 10-30)
            (31, 36, "NAME"),  # "speck" (from original NAME "speck ham" 31-40)
            (37, 40, "NAME"),  # "ham" (from original NAME "speck ham" 31-40)
            # Comma at 40 is "O"
            (42, 55, "PREP"),  # "thinly" (from original PREP "thinly sliced" 42-55)
        ]
    }),

    # Example 2
    ("1/2 cup leftover cooked chopped ham, chicken, turkey or sausage", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 16, "PREP"),  # "leftover" (from original PREP "leftover cooked chopped" 8-31)
            (17, 23, "PREP"),  # "cooked" (from original PREP 8-31)
            (24, 31, "NAME"),  # "chopped" (from original PREP 8-31)
            (32, 35, "NAME"),  # "ham"
            # Comma at 35 is "O"
            (37, 44, "ALT_NAME"),  # "chicken" (Kept)
            # Comma at 44 is "O"
            (46, 52, "ALT_NAME"),  # "turkey" (Kept)
            (53, 63, "ALT_NAME")  # "or sausage" (Kept)
        ]
    }),

    # Example 4
    ("1 pound cultivated, shiitake, or portobello mushrooms (choose one or several types)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 18, "NAME"),  # "cultivated," (Kept, includes comma)
            (20, 28, "ALT_NAME"),  # "shiitake," (Kept, includes comma)
            (30, 43, "ALT_NAME"),  # "or portobello" (Kept)
            (44, 53, "NAME"),  # "mushrooms"
            (54, 83, "COMMENT"),  # "choose one or several types" (from original COMMENT (54,83))
        ]
    }),

    # Example 5
    ("2 pounds bone-in skinless chicken pieces, such as legs, thighs and breasts, halved", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 16, "NAME"),  # "bone-in" (Kept)
            (17, 25, "NAME"),  # "skinless" (Kept)
            (26, 33, "NAME"),  # "chicken"
            (34, 40, "NAME"),  # "pieces"
            # Comma at 40 is "O"
            (42, 74, "COMMENT"),  # "such as legs, thighs and breasts" (Kept)
            # Comma at 74 is "O"
            (76, 82, "PREP")  # "halved" (Kept)
        ]
    }),

    # Example 6
    ("2 tablespoons chopped fresh herbs like parsley or tarragon", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, "PREP"),  # "chopped" (Kept)
            (22, 27, "PREP"),  # "fresh" (Kept)
            (28, 33, "NAME"),  # "herbs"
            (34, 58, "COMMENT")  # "like parsley or tarragon" (Kept)
        ]
    }),

    # Example 7

    ("2 pounds store-bought, trimmed fresh green beans or mix yellow wax and green beans, coarsely chopped on an angle",
     {  # If "green beans" is NAME, "or mix" is ALT_NAME
         "entities": [
             (0, 1, "QTY"), (2, 8, "UNIT"), (9, 21, "PREP"), (23, 30, "PREP"), (31, 36, "PREP"),
             (37, 42, "NAME"), (43, 48, "NAME"),  # green beans
             (49, 55, "ALT_NAME"),  # "or mix" (if this was a separate alt for "green beans")
             (56, 82, "ALT_NAME"),  # "yellow wax and green beans" (if this was another distinct alt)
             (84, 112, "PREP")
         ]  # This input is very hard to interpret without clearer original intent for "or mix".
     }),

    # Example 8
    ("1 1/2 tablespoons mild curry", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 17, "UNIT"),  # "tablespoons"
            (18, 22, "NAME"),  # "mild" (from original NAME "mild curry" 18-28)
            (23, 28, "NAME")  # "curry" (from original NAME "mild curry" 18-28)
        ]
    }),

    # Example 9 (Duplicate from previous, using corrected version)
    ("Two 2 pound whole lobsters, par cooked (12 minutes in boiling salted water), put in ice bath and split lengthwise",
     {
         "entities": [
             (0, 3, "QTY"), (4, 11, "COMMENT"), (12, 17, "PREP"), (18, 26, "NAME"),
             (28, 38, "PREP"), (39, 76, "COMMENT"), (77, 113, "PREP")
         ]
     }),

    # Example 10 (Duplicate)
    ("1 cup chopped basil", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 13, "PREP"), (14, 19, "NAME")]
    }),

    # Example 11 (Duplicate, using corrected version)
    ("1/2 cup freshly squeeze orange juice", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "PREP"), (16, 23, "PREP"),
            (24, 30, "NAME"), (31, 36, "NAME")  # orange, juice
        ]
    }),

    # Example 12 (Duplicate, using corrected version)
    ("1/2 cup freshly grated Locatelli (Pecorino Romano)", {  # If comment included parens
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "PREP"), (16, 22, "PREP"), (23, 32, "NAME"),
            (33, 50, "COMMENT")
        ]
    }),

    # Example 13 (Original had a nested tuple, assuming the inner one is the data)
    ("1 package (2 sheets) all-butter frozen puff pastry, defrosted but still cold", {  # If comments included parens
        "entities": [
            (0, 1, "QTY"), (2, 9, "UNIT"), (10, 20, "PREP"), (21, 31, "PREP"), (32, 38, "PREP"),
            (39, 43, "NAME"), (44, 50, "NAME"),
            (50, 76, "COMMENT")
        ]
    }),

    # Example 14 (Duplicate, using corrected)
    ("1 large egg plus 2 tablespoons water", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 11, "NAME"), (12, 36, "COMMENT")
        ]
    }),

    # Example 15 (Duplicate, using corrected)
    ("1/2 cup/125 ml freshly grated Pecorino cheese", {
        "entities": [
            (0, 3, "QTY"), (4, 11, "UNIT"), (12, 14, "COMMENT"), (15, 22, "PREP"), (23, 29, "NAME"),
            (30, 38, "NAME"), (39, 45, "NAME")  # Pecorino, cheese
        ]
    }),

    # Example 16 (Duplicate, using corrected)
    ("1/2 cup/125 ml freshly grated Parmigiano cheese", {
        "entities": [
            (0, 3, "QTY"), (4, 11, "UNIT"), (12, 14, "COMMENT"), (15, 22, "PREP"), (23, 29, "NAME"),
            (30, 40, "NAME"), (41, 47, "NAME")  # Parmigiano, cheese
        ]
    }),

    # Example 17
    ("1 cup 250 ml breadcrumbs", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "COMMENT"),  # "250 ml" (Kept)
            (13, 24, "NAME")  # "breadcrumbs"
        ]
    }),

    # Example 18
    ("1/4 pound fresh enoki mushrooms, brushed clean and thinly sliced", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 15, "PREP"),  # "fresh" (Kept)
            (16, 21, "NAME"),  # "enoki" (from original NAME "enoki mushrooms" 16-31)
            (22, 31, "NAME"),  # "mushrooms" (from original NAME "enoki mushrooms" 16-31)
            # Comma at 31 is "O"
            (33, 64, "PREP"),  # "brushed clean" (Kept from original (33,46,"PREP"))
        ]
    }),

    # Example 19
    ("1/2 pound fresh beech or hon shimeji mushrooms", {  # If "or hon shimeji" was one ALT_NAME
        "entities": [
            (0, 3, "QTY"), (4, 9, "UNIT"), (10, 15, "PREP"), (16, 21, "NAME"),
            (22, 36, "ALT_NAME"),  # "or hon shimeji"
            (37, 46, "NAME")
        ]
    }),

    # Example 20 (Duplicate, using corrected)
    ("2 teaspoons fresh thyme leaves or 1/2 teaspoon dried thyme", {
        "entities": [
            # Primary Item
            (0, 1, "QTY"),         # "2"
            (2, 11, "UNIT"),       # "teaspoons"
            (12, 17, "PREP"),      # "fresh"
            (18, 23, "NAME"),      # "thyme"
            (24, 30, "NAME"),      # "leaves"
            (31,33,'ALT_NAME'),
            # Alternative Item/Form
            (34, 37, "ALT_QTY"),   # "1/2" (quantity for the alternative thyme)
            (38, 46, "ALT_UNIT"),  # "teaspoon" (unit for the alternative thyme)
            (47, 58, "ALT_NAME")   # "thyme" (the alternative item name, which is the same base ingredient)
        ]
    }),

    # Example 21
    ("1 loaf country bread", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 6, "PREP"),  # "loaf"
            (7, 14, "NAME"),  # "country" (from original NAME "country bread" 7-20)
            (15, 20, "NAME")  # "bread" (from original NAME "country bread" 7-20)
        ]
    }),

    # Example 22
    ("8 ounces of your favorite bourbon", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 25, "PREP"),  # "of" (Kept)
            (26, 33, "NAME")  # "bourbon"
        ]
    }),

    # Example 23
    ("8 dashes bitters", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "COMMENT"),  # "dashes"
            (9, 16, "NAME")  # "bitters"
        ]
    }),

    # Example 24
    ("3/4 ounce to 1 ounce (20 grams to 25 grams) fresh non-GM yeast", {  # If QTY, UNIT was (0,3 QTY), (4,20 UNIT)
        "entities": [
            (0, 3, "QTY"), (4, 9, "UNIT"),  # 3/4, ounce
            (10, 14, "ALT_QTY"),  # to (if "to 1 ounce" is alt unit)
            (15, 20, "ALT_UNIT"),  # ounce
            (21, 43, "COMMENT"), (44, 49, "PREP"), (50, 56, "PREP"), (57, 62, "NAME")
        ]
    }),

    # Example 25 (Duplicate, using corrected)

    ("16 ounces/4 cups (450 grams) strong (stone-ground) wholemeal flour", {  # If comments included parens
        "entities": [
            (0, 2, "QTY"), (3, 16, "COMMENT"), (17, 28, "COMMENT"),
            (29, 35, "PREP"), (36, 50, "COMMENT"),
            (51, 60, "NAME"), (61, 66, "NAME")
        ]
    }),

    # Example 26

    ("15 fluid ounces/ scant 2 cups (425 milliliters) water at blood heat plus 10 fluid ounces/1 1/4 cups (275 milliliters)",
     {  # If (3,16,"UNIT") "fluid ounces/" and comment included parens
         "entities": [
             (0, 2, "QTY"), (3, 16, "UNIT"), (17, 29, "COMMENT"),
             (30, 47, "COMMENT"),  # (425 milliliters)
             (48, 53, "NAME"), (54, 67, "PREP"), (68, 117, "COMMENT")
         ]
     }),

    # Example 27
    ("1/2 (15-ounce) package refrigerated piecrusts", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 14, "COMMENT"),  # "15-ounce" (from original COMMENT (4,14))
            (15, 22, "UNIT"),  # "package"
            (23, 35, "PREP"),  # "refrigerated" (Kept)
            (36, 45, "NAME")  # "piecrusts"
        ]
    }),

    # Example 28

    ("1 1/2 teaspoons pimenton (Spanish paprika)", {  # If comment included parens
        "entities": [
            (0, 5, "QTY"), (6, 15, "UNIT"), (16, 24, "NAME"), (25, 42, "COMMENT")
        ]
    }),

    # Example 29
    ("1/2 an onion, finely chopped", {
        "entities": [
            (0, 3, "QTY"),  # "1/2 an" (Kept)
            (7, 12, "NAME"),  # "onion"
            # Comma at 12 is "O"
            (14, 28, "PREP"),  # "finely" (Kept)
        ]
    }),

    # Example 30
    ("12 glazed donut holes", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 9, "NAME"),  # "glazed" (from original NAME "glazed donut holes" 3-21)
            (10, 15, "NAME"),  # "donut" (from original NAME 3-21)
            (16, 21, "NAME")  # "holes" (from original NAME 3-21)
        ]
    }),

    # Example 31
    ("12 flower-shaped ginger cookies", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 16, "PREP"),  # "flower-shaped" (Kept)
            (17, 23, "NAME"),  # "ginger" (from original NAME "ginger cookies" 17-31)
            (24, 31, "NAME")  # "cookies" (from original NAME "ginger cookies" 17-31)
        ]
    }),

    # Example 32
    ("12 peanut-shaped peanut butter cookies", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 16, "PREP"),  # "peanut-shaped" (Kept)
            (17, 23, "NAME"),  # "peanut" (from original NAME "peanut butter cookies" 17-38)
            (24, 30, "NAME"),  # "butter" (from original NAME 17-38)
            (31, 38, "NAME")  # "cookies" (from original NAME 17-38)
        ]
    }),

    # Example 33
    ("1 1/2 cups dry rose wine", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 14, "NAME"),  # "dry" (from original NAME "dry rose wine" 11-24)
            (15, 19, "NAME"),  # "rose" (from original NAME 11-24)
            (20, 24, "NAME")  # "wine" (from original NAME 11-24)
        ]
    }),

    # Example 34
    ("1 angel food cake", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "NAME"),  # "angel" (from original NAME "angel food cake" 2-17)
            (8, 12, "NAME"),  # "food" (from original NAME 2-17)
            (13, 17, "NAME")  # "cake" (from original NAME 2-17)
        ]
    }),

    # Example 35
    ("2 ounces Licor 43", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 14, "NAME"),  # "Licor" (from original NAME "Licor 43" 9-17)
            (15, 17, "NAME")  # "43" (from original NAME "Licor 43" 9-17)
        ]
    }),

    # Example 36
    ("1 wide strip orange zest", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "PREP"),  # "wide" (Kept)
            (13, 19, "NAME"),  # "orange" (from original NAME "orange zest" 13-24)
            (20, 24, "NAME")  # "zest" (from original NAME "orange zest" 13-24)
        ]
    }),

    # Example 37
    ("6 ounces thinly sliced speck", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 22, "PREP"),  # "thinly" (Kept)
            (23, 28, "NAME")  # "speck"
        ]
    }),

    # Example 38
    ("Four 12-ounce balls Pizza Dough", {
        "entities": [
            (0, 4, "QTY"),  # "Four" (Kept)
            (5, 13, "COMMENT"),  # "12-ounce" (Kept)
            (14, 19, "PREP"),  # "balls"
            (20, 25, "NAME"),  # "Pizza" (from original NAME "Pizza Dough" 20-31)
            (26, 31, "NAME")  # "Dough" (from original NAME "Pizza Dough" 20-31)
        ]
    }),

    # Example 39

    ("1 medium size live eel (about 1 to 2 pounds, both sides or loins)", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 13, "PREP"), (14, 18, "PREP"), (19, 22, "NAME"),
            (23, 65, "COMMENT")
        ]
    }),

    # Example 40
    ("2 cups dry red wine, such as Pinot noir", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 10, "NAME"),  # "dry" (from original NAME "dry red wine" 7-19)
            (11, 14, "NAME"),  # "red" (from original NAME 7-19)
            (15, 19, "NAME"),  # "wine" (from original NAME 7-19)
            # Comma at 19 is "O"
            (21, 39, "COMMENT")  # "such as Pinot noir" (Kept)
        ]
    }),

    # Example 41
    ("3/4 cup warm water, plus more if needed", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "COMMENT"),  # "warm" (Kept)
            (13, 18, "NAME"),  # "water"
            # Comma at 18 is "O"
            (20, 39, "COMMENT")  # "plus more if needed" (Kept)
        ]
    }),

    # Example 42
    ("1 medium ripe kiwi, peeled and chopped", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "UNIT"),  # "medium"
            (9, 13, "PREP"),  # "ripe" (Kept)
            (14, 18, "NAME"),  # "kiwi"
            # Comma at 18 is "O"
            (20, 38, "PREP"),  # "peeled" (Kept)
        ]
    }),

    # Example 43 (Duplicate, using corrected)
    ("3/4 pound Chilean Sea Bass fillet", {
        "entities": [
            (0, 3, "QTY"), (4, 9, "UNIT"),
            (10, 17, "NAME"), (18, 21, "NAME"), (22, 26, "NAME"),  # Chilean, Sea, Bass
            (27, 33, "NAME")  # fillet
        ]
    }),

    # Example 44
    ("Sprigs of tarragon, dill and flat-leaf parsley", {
        "entities": [
            (0, 6, "UNIT"),  # "Sprigs"
            (7, 9, "PREP"),  # "of" (Kept)
            (10, 46, "NAME"),  # "tarragon"
        ]
    }),

    # Example 45
    ("3 tablespoons each of chopped tarragon, dill and flat-leaf parsley", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 18, "COMMENT"),  # "each" (Kept)
            (19, 29, "PREP"),  # "of" (Kept)
            (30, 66, "NAME"),  # "tarragon"
        ]
    }),

    # Example 46
    ("1/4 to 1/2 cup or more Sabra Guacamole (any flavor)", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (from original QTY "1/4 to 1/2" 0-10)
            (4, 10, "ALT_QTY"),  # "to 1/2" (Following "X to Y" rule)
            (11, 14, "UNIT"),  # "cup"
            (15, 22, "COMMENT"),  # "or more" (Kept)
            (23, 28, "NAME"),  # "Sabra" (from original NAME "Sabra Guacamole" 23-38)
            (29, 38, "NAME"),  # "Guacamole" (from original NAME "Sabra Guacamole" 23-38)
            (39, 51, "COMMENT"),  # "any flavor" (from original COMMENT (39,51))
        ]
    }),

    # Example 47

    ("1 (12-ounce) loaf favorite bread (Asiago cheese, olive, herb, etc.)", {  # If comment included parens
        "entities": [
            (0, 1, "COMMENT"),
            (3, 5, "QTY"),
            (6, 11, "UNIT"),
            (13, 17, "PREP"),
            (18, 26, "COMMENT"),
            (27, 32, "NAME"),
            (33, 65, "COMMENT")
        ]
    }),

    # Example 48
    ("6-ounces thinly sliced smoked turkey", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 22, "PREP"),  # "thinly" (Kept)
            (23, 36, "NAME")  # "turkey"
        ]
    }),

    # Example 49 (Alternative for 6-ounces)
    # Example 50
    ("2 cups shredded smoked scamorza or smoked provolone cheese", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 15, "PREP"),  # "shredded" (Kept)
            (16, 31, "NAME"),  # "smoked" (from original ALT_NAME "smoked scamorza" 16-31)
            (32, 51, "ALT_NAME"),  # "or smoked provolone cheese" (Kept)
            (52, 58, "NAME")  # "or smoked provolone cheese" (Kept)
        ]
    }),

    # Example 51
    ("5 bunches of scallions", {
        "entities": [
            (0, 1, "QTY"),  # "5" (Kept)
            (2, 9, "UNIT"),  # "bunches"
            (10, 12, "PREP"),  # "of" (Kept)
            (13, 22, "NAME")  # "scallions"
        ]
    }),

    # Example 52
    ("2 tablespoons freshly squeezed limejuice", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 30, "PREP"),  # "freshly" (Kept)
            (31, 40, "NAME")  # "limejuice"
        ]
    }),

    # Example 53
    ("1 small Maui sweet onion - sliced", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "small"
            (8, 12, "NAME"),  # "Maui" (from original NAME "Maui sweet onion" 8-24)
            (13, 18, "NAME"),  # "sweet" (from original NAME 8-24)
            (19, 24, "NAME"),  # "onion" (from original NAME 8-24)
            (27, 33, "PREP")  # "sliced" (Kept)
        ]
    }),

    # Example 54
    ("4 -6 sprigs fresh basil leaves", {
        "entities": [
            (0, 1, "QTY"),  # "4 -6" (Kept, includes space and hyphen)
            (2, 4, "ALT_QTY"),  # "4 -6" (Kept, includes space and hyphen)
            (5, 11, "PREP"),  # "sprigs"
            (12, 17, "PREP"),  # "fresh" (Kept)
            (18, 23, "NAME"),  # "basil" (from original NAME "basil leaves" 18-30)
            (24, 30, "NAME")  # "leaves" (from original NAME "basil leaves" 18-30)
        ]
    }),

    # Example 55
    ("1 gumball or other round hard candy", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 9, "NAME"),  # "gumball"
            (10, 35, "ALT_NAME")  # "or other round hard candy" (Kept)
        ]
    }),

    # Example 56
    ("3 cups sliced fresh string beans, in 1/2-inch pieces", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 13, "PREP"),  # "sliced" (Kept)
            (14, 19, "PREP"),  # "fresh" (Kept)
            (20, 26, "NAME"),  # "string" (from original NAME "string beans" 20-32)
            (27, 32, "NAME"),  # "beans" (from original NAME "string beans" 20-32)
            # Comma at 32 is "O"
            (34, 52, "PREP")  # "in 1/2-inch pieces" (Kept)
        ]
    }),

    # Example 57 (Duplicate, using corrected)
    ("1/2 cup/125 ml flour", {
        "entities": [
            (0, 3, "QTY"), (4, 11, "UNIT"), (12, 14, "COMMENT"), (15, 20, "NAME")
        ]
    }),

    # Example 58
    ("1 pound/500 g butternut squash", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 11, "UNIT"),  # "pound/500" (from original UNIT "pound/500 g" 2-13)
            (12, 13, "COMMENT"),  # "g" (from original UNIT "pound/500 g" 2-13)
            (14, 23, "NAME"),  # "butternut" (from original NAME "butternut squash" 14-30)
            (24, 30, "NAME")  # "squash" (from original NAME "butternut squash" 14-30)
        ]
    }),

    # Example 59
    ("1 (750-ml) bottle dry red wine", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (3, 9, "COMMENT"),  # "750-ml" (from original COMMENT (2,10))
            (11, 17, "COMMENT"),  # "bottle"
            (18, 21, "NAME"),  # "dry" (from original NAME "dry red wine" 18-30)
            (22, 25, "NAME"),  # "red" (from original NAME 18-30)
            (26, 30, "NAME")  # "wine" (from original NAME 18-30)
        ]
    }),

    # Example 60
    ("3 1/2 cups 00 flour, plus more for dusting", {
        "entities": [
            (0, 5, "QTY"),  # "3 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 13, "COMMENT"),  # "00" (from original NAME "00 flour" 11-19)
            (14, 19, "NAME"),  # "flour" (from original NAME "00 flour" 11-19)
            # Comma at 19 is "O"
            (21, 42, "COMMENT")  # "plus more for dusting" (Kept)
        ]
    }),

    # Example 61
    ("1 (28-ounce) can fire-roasted crushed tomatoes", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "COMMENT"),  # "(28-ounce)" (Kept)
            (13, 16, "UNIT"),  # "can"
            (17, 29, "NAME"),  # "fire-roasted" (from original NAME "fire-roasted crushed tomatoes" 17-46)
            (30, 37, "NAME"),  # "crushed" (from original NAME 17-46)
            (38, 46, "NAME")  # "tomatoes" (from original NAME 17-46)
        ]
    }),

    # Example 62
    ("2 tablespoons, plus 1/4 cup safflower oil", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            # Comma at 13 is "O"
            (15, 27, "COMMENT"),  # "plus 1/4 cup" (Kept)
            (28, 37, "NAME"),  # "safflower" (from original NAME "safflower oil" 28-41)
            (38, 41, "NAME")  # "oil" (from original NAME "safflower oil" 28-41)
        ]
    }),

    # Example 63
    ("6 ounces pilsner beer", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 16, "NAME"),  # "pilsner" (from original NAME "pilsner beer" 9-21)
            (17, 21, "NAME")  # "beer" (from original NAME "pilsner beer" 9-21)
        ]
    }),

    # Example 64
    ("1 pound small white button mushrooms, stemmed and thinly sliced", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 13, "PREP"),  # "small" (Kept)
            (14, 19, "NAME"),  # "white" (from original NAME "white button mushrooms" 14-36)
            (20, 26, "NAME"),  # "button" (from original NAME 14-36)
            (27, 36, "NAME"),  # "mushrooms" (from original NAME 14-36)
            # Comma at 36 is "O"
            (38, 63, "PREP"),  # "stemmed" (Kept from (38,45,"PREP"))
        ]
    }),

    # Example 65
    ("1/4 -ounce ice cream stabilizer", {  # Original: (0,3,"QTY"), (5,10,"UNIT"), (11,30,"NAME")
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 10, "UNIT"),  # "ounce"
            (11, 14, "NAME"),  # "ice" (from original NAME "ice cream stabilizer" 11-30)
            (15, 20, "NAME"),  # "cream" (from original NAME 11-30)
            (21, 31, "NAME")  # "stabilizer" (from original NAME 11-30, corrected end span)
        ]
    }),

    # Example 67
    ("15 curry leaves*", {
        "entities": [
            (0, 2, "QTY"),  # "15" (Kept)
            (3, 8, "NAME"),  # "curry" (from original NAME "curry leaves*" 3-15)
            (9, 15, "NAME")  # "leaves*" (from original NAME "curry leaves*" 3-15, includes *)
        ]
    }),

    # Example 68
    ("One 15-ounce can fire-roasted tomatoes", {
        "entities": [
            (0, 3, "QTY"),  # "One" (Kept)
            (4, 12, "COMMENT"),  # "15-ounce" (Kept)
            (13, 16, "UNIT"),  # "can"
            (17, 29, "NAME"), (30, 38, "NAME")
        ]
    }),

    # Example 69 (Duplicate, using corrected)
    ("One 28-ounce can fire-roasted diced tomatoes", {
        "entities": [
            (0, 3, "QTY"), (4, 12, "COMMENT"), (13, 16, "UNIT"),
            (17, 29, "NAME"), (30, 35, "NAME"), (36, 44, "NAME")  # fire-roasted, diced, tomatoes
        ]
    }),

    # Example 70
    ("1 chipotle in adobo, minced", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 19, "NAME"),  # "chipotle"=
            # Comma at 19 is "O"
            (21, 27, "PREP")  # "minced" (Kept)
        ]
    }),

    # Example 71 (Duplicate, using corrected)
    ("4 pounds top round with fat cap", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"),
            (9, 12, "NAME"), (13, 18, "NAME"),  # top, round
            (19, 31, "COMMENT")
        ]
    }),

    # Example 72 (Your original had "or a nub of" as ALT_NAME. Now COMMENT based on your notes)
    ("1 to 2 tablespoons or a nub of butter", {
        "entities": [
            (0, 1, "QTY"),  # "1 to 2 tablespoons" (Kept)
            (2, 6, "ALT_QTY"),  # "1 to 2 tablespoons" (Kept)
            (7, 18, "UNIT"),  # "1 to 2 tablespoons" (Kept)
            (19, 30, "COMMENT"),  # "or a nub of" (Kept as original COMMENT span)
            (31, 37, "NAME")  # "butter" (Original span (33,39) for "tter" was typo, assuming "butter" (31,37))
        ]
    }),

    # Example 73
    ("3 whole chicken legs and 3 wings", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 7, "PREP"),  # "whole" (Kept)
            (8, 15, "NAME"),  # "chicken"
            (16, 20, "NAME"),  # "legs"
            (21, 32, "ALT_NAME"),  # "and" (Original label was PREP) - *Unusual*
        ]
    }),

    # Example 74
    ("Dash ground cinnamon", {
        "entities": [
            (0, 4, "COMMENT"),  # "Dash" (Kept)
            (5, 11, "NAME"),  # "ground" (from original NAME "ground cinnamon" 5-20)
            (12, 20, "NAME")  # "cinnamon" (from original NAME "ground cinnamon" 5-20)
        ]
    }),

    # Example 75 (Duplicate, using corrected)
    ("1/4 cup or so half-and-half", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "COMMENT"), (14, 27, "NAME")
        ]
    }),

    # Example 76 (Duplicate, using corrected)
    ("5 pounds russet or Yukon gold potatoes", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 15, "NAME"),  # russet (original was ALT_NAME)
            (16, 29, "ALT_NAME"),  # "or Yukon gold"
            (30, 38, "NAME")  # potatoes
        ]
    }),

    # Example 77
    ("2 cups diced leftover rutabaga, carrots, potatoes and leek", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 12, "PREP"),  # "diced" (Kept)
            (13, 21, "PREP"),  # "leftover" (Kept)
            (22, 30, "NAME"),  # "rutabaga"
            # Comma at 30 is "O"
            (32, 39, "NAME"),  # "carrots"
            # Comma at 39 is "O"
            (41, 49, "NAME"),  # "potatoes"
            (50, 58, "O"),  # "and"
        ]
    }),

    # Example 78
    ("1/2 cup freshly squeezed citrus (blood oranges, oranges, key limes etc.)", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "PREP"),  # "freshly" (Kept)
            (16, 24, "PREP"),  # "squeezed" (Kept)
            (25, 31, "NAME"),  # "citrus"
            (32, 70, "COMMENT"),  # "blood oranges, oranges, key limes etc." (from original COMMENT (32,70))
        ]
    }),

    # Example 79 (Duplicate, using corrected)
    ("6 to 8 ounces frozen or fresh squid cleaned and sliced into tubes", {
        "entities": [
            (0, 1, "QTY"), (2, 6, "ALT_QTY"),  # "6", "to 8" (following X to Y rule)
            (7, 13, "UNIT"), (14, 20, "ALT_NAME"), (21, 29, "ALT_NAME"), (30, 35, "NAME"),
            (36, 43, "PREP"), (44, 47, "O"), (48, 65, "PREP")  # cleaned, and, sliced into tubes
        ]
    }),

    # Example 80
    ("2 bunches of watercress", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 9, "UNIT"),  # "bunches"
            (10, 12, "PREP"),  # "of" (Kept)
            (13, 23, "NAME")  # "watercress"
        ]
    }),

    # Example 81 (Duplicate, using corrected)
    ("1/2 pound very thinly sliced gravlax, Scottish smoked salmon or nova, separated and gently torn into 1- or 2-inch pieces",
     {
         "entities": [
             (0, 3, "QTY"), (4, 9, "UNIT"), (10, 21, "PREP"), (22, 28, "NAME"),
             (29, 36, "ALT_NAME"), (36, 37, "O"), (38, 60, "ALT_NAME"), (61, 68, "ALT_NAME"),
             (68, 69, "O"), (70, 120, "PREP")
         ]
     }),

    # Example 82
    ("1 quart water", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "quart"
            (8, 13, "NAME")  # "water"
        ]
    }),
    # Re-annotated data based on the FINAL REFINED rules:

    # ... (all previous examples from your earlier chunks would be here) ...

    # Example 1

    ("1/2 cup of the yogurt mixture, from above", {  # If "the yogurt mixture" was one NAME
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"),
            (15, 21, "NAME"), (22, 29, "NAME"),  # the, yogurt, mixture
            (31, 41, "COMMENT")
        ]
    }),

    # Example 2
    ("1/4 cup plus 2 teaspoons fish sauce", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 24, "COMMENT"),  # "plus 2 teaspoons" (Kept)
            (25, 29, "NAME"),  # "fish"
            (30, 35, "NAME")  # "sauce"
        ]
    }),

    # Example 3
    ("1 cup frozen mixed vegetables", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "PREP"),  # "frozen" (Kept)
            (13, 18, "NAME"),  # "mixed"
            (19, 29, "NAME")  # "vegetables"
        ]
    }),

    # Example 4
    ("3 tablespoons oil, divided", {  # If "divided" was PREP
        "entities": [
            (0, 1, "QTY"), (2, 13, "UNIT"), (14, 17, "NAME"),
            (19, 26, "PREP")
        ]
    }),

    # Example 5
    ("1/2 cup pitted mixed olives, finely chopped", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "pitted" (Kept)
            (15, 20, "NAME"),  # "mixed" (from original NAME "mixed olives" 15-27)
            (21, 27, "NAME"),  # "olives" (from original NAME "mixed olives" 15-27)
            # Comma at 27 is "O"
            (29, 43, "PREP")  # "finely chopped" (Kept)
        ]
    }),

    # Example 6
    ("1 1/2 teaspoons fine salt", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 15, "UNIT"),  # "teaspoons"
            (16, 20, "NAME"),  # "fine"
            (21, 25, "NAME")  # "salt"
        ]
    }),

    # Example 7
    ("1 pound pork belly", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 12, "NAME"),  # "pork"
            (13, 18, "NAME")  # "belly"
        ]
    }),

    # Example 8
    ("6 cups diced acorn or butternut squash, about 2 1/2 lb.", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 12, "PREP"),  # "diced" (Kept)
            (13, 18, "ALT_NAME"),  # "acorn"
            (19, 31, "ALT_NAME"),  # "or butternut squash" (Kept)
            (32, 38, "NAME"),  # "or butternut squash" (Kept)
            # Comma at 36 is "O"
            (40, 54, "COMMENT")  # "about 2 1/2 lb." (Kept)
        ]
    }),

    # Example 9
    ("1 cup mixed dried fruit, such as diced apricots, dates and pears, or blueberries, cranberries, currants and raisins",
     {
         "entities": [
             (0, 1, "QTY"),  # "1" (Kept)
             (2, 5, "UNIT"),  # "cup"
             (6, 11, "NAME"),  # "mixed" (Kept)
             (12, 17, "NAME"),  # "dried"
             (18, 23, "NAME"),  # "fruit"
             # Comma at 23 is "O"
             (25, 103, "COMMENT")
             # "such as diced apricots, dates and pears, or blueberries, cranberries, currants and raisins" (Kept)
         ]
     }),

    # Example 10
    ("1 cup cooked meat cut in 1/2-inch cubes, such as pork, ham, beef, or chicken", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 12, "PREP"),  # "cooked" (Kept)
            (13, 17, "NAME"),  # "meat"
            (18, 39, "PREP"),  # "cut in 1/2-inch cubes" (Kept)
            # Comma at 38 is "O"
            (41, 76, "COMMENT")  # "such as pork, ham, beef, or chicken" (Kept)
        ]
    }),

    # Example 11

    ("2 tablespoons kaong (palm nuts)", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 13, "UNIT"), (14, 19, "NAME"),
            (20, 31, "COMMENT")
        ]
    }),

    # Example 12
    ("2 cups fresh vegetables", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 12, "PREP"),  # "fresh"
            (13, 23, "NAME")  # "vegetables"
        ]
    }),

    # Example 13
    ("1/4 cup store-bought basil pesto", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 20, "PREP"),  # "store-bought" (Kept)
            (21, 26, "NAME"),  # "basil"
            (27, 32, "NAME")  # "pesto"
        ]
    }),

    # Example 14
    ("2 cups pitted cherries", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 13, "PREP"),  # "pitted" (Kept)
            (14, 22, "NAME")  # "cherries"
        ]
    }),

    # Example 15
    ("2 heads, plus 4 cloves garlic", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 7, "UNIT"),  # "heads"
            # Comma at 7 is "O"
            (9, 15, "COMMENT"),  # "plus 4 cloves" (Kept)
            (16, 29, "NAME")  # "garlic"
        ]
    }),

    # Example 16
    ("1/2 cup 1/2-inch sliced squash", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 16, "PREP"),  # "1/2-inch" (Kept)
            (17, 23, "PREP"),  # "sliced" (Kept)
            (24, 30, "NAME")  # "squash"
        ]
    }),

    # Example 17
    ("1 1/2 packed cups katsuobushi (dried bonito flakes; about 30 grams)", {  # If comment included parens
        "entities": [
            (0, 5, "QTY"), (6, 12, "PREP"), (13, 17, "UNIT"), (18, 29, "NAME"),
            (30, 60, "COMMENT")
        ]
    }),

    # Example 18
    ("2 medium acorn squash, halved, seeded and cut into 8 wedges each", {  # If the long prep was one span
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "NAME"), (15, 21, "NAME"),
            (23, 64, "PREP")  # "halved, seeded and cut into 8 wedges each"
        ]
    }),

    # Example 19
    ("1 1/2 pounds lean pork meat, such as loin, trimmed of any gristle or membranes and cut into small dice", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 12, "UNIT"),  # "pounds"
            (13, 17, "NAME"),  # "lean" (from original NAME "lean pork meat" 13-27)
            (18, 22, "NAME"),  # "pork" (from original NAME 13-27)
            (23, 27, "NAME"),  # "meat" (from original NAME 13-27)
            # Comma at 27 is "O"
            (29, 41, "COMMENT"),  # "such as loin," (Kept, includes comma)
            (43, 102, "PREP")  # "trimmed of any gristle or membranes and cut into small dice" (Kept)
        ]
    }),

    # Example 20
    ("1 small yucca, peeled and cut into 2-inch pieces", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "small"
            (8, 13, "NAME"),  # "yucca"
            # Comma at 13 is "O"
            (15, 48, "PREP")  # "peeled and cut into 2-inch pieces" (Kept)
        ]
    }),

    # Example 21
    ("1 cup plus 4 tablespoon for dredging and the gravy",
     {  # If (6,50) was COMMENT for "plus 4 tablespoon for dredging and the gravy"
         "entities": [
             (0, 1, "QTY"), (2, 5, "UNIT"),
             (6, 50, "COMMENT")
         ]
     }),

    # Example 22
    ("2 pounds stew meat, cut into cubes", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 13, "NAME"),  # "stew"
            (14, 18, "NAME"),  # "meat"
            # Comma at 18 is "O"
            (20, 34, "PREP")  # "cut into cubes" (Kept)
        ]
    }),

    # Example 23
    ("2 ounces chopped mixed herbs", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 16, "NAME"),  # "chopped" (from original NAME "chopped mixed herbs" 9-28)
            (17, 22, "NAME"),  # "mixed" (from original NAME 9-28)
            (23, 28, "NAME")  # "herbs" (from original NAME 9-28)
        ]
    }),

    # Example 24
    ("1/4 cup au jus powder mix", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 10, "NAME"),  # "au" (from original NAME "au jus powder mix" 8-23)
            (11, 14, "NAME"),  # "jus" (from original NAME 8-23)
            (15, 21, "NAME"),  # "powder" (from original NAME 8-23)
            (22, 25, "NAME")  # "mix" (from original NAME 8-23)
        ]
    }),

    # Example 25
    ("1 pound, lean ground turkey", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            # Comma at 7 is "O"
            (9, 13, "NAME"),  # "lean" (Kept)
            (14, 20, "NAME"),  # "ground"
            (21, 27, "NAME")  # "turkey"
        ]
    }),

    # Example 26
    ("1/4 cup reserved fat from the roasting liquid (from turkey, see recipe)", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 16, "PREP"),  # "reserved" (Kept)
            (17, 20, "NAME"),  # "fat"
            (21, 71, "COMMENT")  # "from the roasting liquid (from turkey, see recipe)" (Kept)
        ]
    }),

    # Example 27
    ("1 1/2 cups packaged couscous", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 19, "PREP"),  # "packaged" (Kept)
            (20, 28, "NAME")  # "couscous"
        ]
    }),

    # Example 28
    ("1 package, 2 ounces, chopped nut topping, available on baking aisle", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 9, "UNIT"),  # "package"
            # Comma at 9 is "O"
            (11, 19, "COMMENT"),
            # "2" (from original COMMENT "2 ounces, chopped nut topping, available on baking aisle" - this is very complex)

            # Comma at 19 is "O"
            (21, 28, "NAME"),  # "chopped" (from original COMMENT)
            (29, 32, "NAME"),  # "nut" (from original COMMENT)
            (33, 40, "NAME"),  # "topping" (from original COMMENT)
            # Comma at 40 is "O"
            (42, 67, "COMMENT")  # "available on baking aisle" (from original COMMENT)
        ]
    }),

    # Example 29
    ("4 ounces grated provolone", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 15, "PREP"),  # "grated" (Kept)
            (16, 25, "NAME")  # "provolone"
        ]
    }),

    # Example 30
    ("1 cup cracked freekeh", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 13, "NAME"),  # "cracked" (from original NAME "cracked freekeh" 6-21)
            (14, 21, "NAME")  # "freekeh" (from original NAME "cracked freekeh" 6-21)
        ]
    }),

    # Example 31
    ("1/3 to 1/2 pound manchego, thinly sliced with sharp knife or cheese plane", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (from original QTY "1/3 to 1/2" 0-10)
            (4, 10, "ALT_QTY"),  # "to 1/2"
            (11, 16, "UNIT"),  # "pound"
            (17, 25, "NAME"),  # "manchego"
            # Comma at 25 is "O"
            (27, 73, "PREP")  # "thinly sliced with sharp knife or cheese plane" (Kept)
        ]
    }),

    # Example 32
    ("14 ounces pork belly, skin removed, minced", {
        "entities": [
            (0, 2, "QTY"),  # "14" (Kept)
            (3, 9, "UNIT"),  # "ounces"
            (10, 14, "NAME"),  # "pork"
            (15, 20, "NAME"),  # "belly"
            # Comma at 20 is "O"
            (22, 42, "PREP"),  # "skin removed" (Kept from original PREP "skin removed, minced" 22-42)

        ]
    }),

    # Example 33
    ("1 tablespoon thinly sliced fresh basil leaves (chiffonade)", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"), (13, 19, "PREP"), (20, 26, "PREP"), (27, 32, "PREP"),
            (33, 38, "NAME"), (39, 45, "NAME"),
            (47, 57, "COMMENT")
        ]
    }),

    # Example 34

    ("1 pound 2-inch-wide stuffing mushrooms (about 14 to 16), cleaned",
     {  # If (40,54) was COMMENT and mushrooms (30,39) was NAME
         "entities": [
             (0, 1, "QTY"), (2, 7, "UNIT"), (8, 19, "PREP"), (20, 28, "PREP"),
             (29, 38, "NAME"),  # mushrooms
             (40, 54, "COMMENT"),  # (about 14 to 16)
             (55, 64, "PREP")
         ]
     }),

    # Example 35
    ("2 cups pretzel squares", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 14, "NAME"),  # "pretzel" (from original NAME "pretzel squares" 7-21)
            (15, 22, "NAME")  # "squares" (from original NAME "pretzel squares" 7-21, typo in your span end?)
        ]
    }),

    # Example 36

    ("4 ounces lean, smoky bacon, chopped", {  # If original NAME span for "bacon" was (21,26)
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"),
            (9, 13, "NAME"), (13, 14, "O"), (15, 20, "NAME"), (21, 26, "NAME"),
            (28, 35, "PREP")
        ]
    }),

    # Example 37
    ("3 cups \"00\" soft wheat pizza and pasta flour", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 11, "COMMENT"),
            # "\"00\"" (from original NAME ' "00" soft wheat pizza and pasta flour ' 7-41, includes quotes)
            (12, 16, "NAME"),  # "soft" (from original NAME 7-41)
            (17, 22, "NAME"),  # "wheat" (from original NAME 7-41)
            (23, 28, "NAME"),  # "pizza" (from original NAME 7-41)
            (29, 44, "ALT_NAME"),  # "and" (from original NAME 7-41) - *Unusual*=
        ]
    }),

    # Example 38
    ("4 tablespoons chopped basil leaves, divided", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, "PREP"),  # "chopped" (Kept)
            (22, 27, "NAME"),  # "basil"
            (28, 34, "NAME"),  # "leaves"
            # Comma at 34 is "O"
            (36, 43, "COMMENT")  # "divided" (Original label COMMENT)
        ]
    }),

    # Example 39
    ("1 pound thinly sliced bacon, each strip halved crosswise", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 14, "PREP"),  # "thinly" (from original PREP "thinly sliced" 8-21)
            (15, 21, "PREP"),  # "sliced" (from original PREP "thinly sliced" 8-21)
            (22, 27, "NAME"),  # "bacon"
            # Comma at 27 is "O"
            (29, 56, "COMMENT")  # "each strip halved crosswise" (Kept)
        ]
    }),

    # Example 40
    ("2 pounds pork neck bones", {  # If "bones" ends at 24
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 13, "NAME"), (14, 18, "NAME"), (19, 24, "NAME")
        ]
    }),

    # Example 41

    ("1/8 teaspoon powdered ascorbic acid (vitamin C)", {  # If "acid" ends at 35 and comment includes parens
        "entities": [
            (0, 3, "QTY"), (4, 12, "UNIT"), (13, 21, "NAME"), (22, 30, "NAME"), (31, 35, "NAME"),
            (36, 47, "COMMENT")
        ]
    }),

    # Example 42
    ("3/4 cup shaved jalapeño", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "shaved" (Kept)
            (15, 23, "NAME")  # "jalapeño"
        ]
    }),

    # Example 43
    ("6 tablespoons mixed peppercorns (black, white, green, pink)", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 13, "UNIT"), (14, 19, "NAME"), (20, 31, "NAME"),
            (32, 59, "COMMENT")
        ]
    }),

    # Example 44
    ("1/2 pound slab bacon, cut into 1/2-inch dice", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 14, "NAME"),  # "slab" (from original NAME "slab bacon" 10-20)
            (15, 20, "NAME"),  # "bacon" (from original NAME "slab bacon" 10-20)
            # Comma at 20 is "O"
            (22, 44, "PREP")  # "cut into 1/2-inch dice" (Kept)
        ]
    }),

    # Example 45
    ("1 pound shell, sirloin, or rib steak, well trimmed and boneless", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 13, "NAME"),  # "shell"
            # Comma at 13 is "O"
            (15, 22, "ALT_NAME"),  # "sirloin" (from original ALT_NAME "sirloin, or rib steak" 15-36)
            (24, 30, "ALT_NAME"),  # "or" (from ALT_NAME 15-36) - *Unusual*
            (31, 36, "NAME"),  # "steak" (from ALT_NAME 15-36)
            # Comma at 36 is "O"
            (38, 63, "PREP")  # "well trimmed and boneless" (Kept)
        ]
    }),

    # Example 46
    ("6 cups shaved curly kale", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 13, "PREP"),  # "shaved" (Kept)
            (14, 19, "NAME"),  # "curly" (from original NAME "curly kale" 14-24)
            (20, 24, "NAME")  # "kale" (from original NAME "curly kale" 14-24)
        ]
    }),

    # Example 47
    ("About 1 1/2 teaspoons or scant half palmful granulated garlic", {
        "entities": [
            (0, 5, "COMMENT"),  # "About" (Kept)
            (6, 11, "QTY"),  # "1 1/2" (Kept)
            (12, 21, "UNIT"),  # "teaspoons"
            (22, 43, "ALT_NAME"),  # "or scant half palmful" (Kept)
            (44, 61, "NAME")  # "garlic"
        ]
    }),

    # Example 48
    ("About 1 1/2 teaspoons or scant half palmful granulated onion", {
        "entities": [
            (0, 5, "COMMENT"),  # "About" (Kept)
            (6, 11, "QTY"),  # "1 1/2" (Kept)
            (12, 21, "UNIT"),  # "teaspoons"
            (22, 43, "ALT_NAME"),  # "or scant half palmful" (Kept)
            (44, 60, "NAME")  # "garlic"
        ]
    }),

    # Example 49
    ("About 1 1/2 teaspoons or scant half palmful chili powder", {
        "entities": [
            (0, 5, "COMMENT"),  # "About" (Kept)
            (6, 11, "QTY"),  # "1 1/2" (Kept)
            (12, 21, "UNIT"),  # "teaspoons"
            (22, 43, "ALT_NAME"),  # "or scant half palmful" (Kept)
            (44, 56, "NAME"),  # "chili" (from original NAME "chili powder" 44-56)
        ]
    }),

    # Example 50
    ("About 1 1/2 teaspoons or scant half palmful ground coriander", {
        "entities": [
            (0, 5, "COMMENT"),  # "About" (Kept)
            (6, 11, "QTY"),  # "1 1/2" (Kept)
            (12, 21, "UNIT"),  # "teaspoons"
            (22, 43, "ALT_NAME"),  # "or scant half palmful" (Kept)
            (44, 60, "NAME"),  # "ground" (from original NAME "ground coriander" 44-60)
        ]
    }),

    # Example 51
    ("About 1 1/2 teaspoons or scant half palmful ground cumin", {
        "entities": [
            (0, 5, "COMMENT"),  # "About" (Kept)
            (6, 11, "QTY"),  # "1 1/2" (Kept)
            (12, 21, "UNIT"),  # "teaspoons"
            (22, 43, "ALT_NAME"),  # "or scant half palmful" (Kept)
            (44, 56, "NAME"),  # "ground" (from original NAME "ground cumin" 44-56)
        ]
    }),

    # Example 52
    ("About 2 tablespoons olive oil or neutral oil", {
        "entities": [
            (0, 5, "COMMENT"),  # "About" (Kept)
            (6, 7, "QTY"),  # "2" (Kept)
            (8, 19, "UNIT"),  # "tablespoons"
            (20, 29, "NAME"),  # "olive" (from original NAME "olive oil" 20-29)
            (30, 44, "ALT_NAME")  # "or neutral oil" (Kept)
        ]
    }),

    # Example 53
    ("4 plum, Roma or vine tomatoes or yellow vine tomatoes", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "NAME"),  # "plum"
            # Comma at 6 is "O"
            (8, 12, "ALT_NAME"),  # "Roma" (from original ALT_NAME "Roma or vine tomatoes or yellow vine tomatoes" 8-49)
            (13, 29, "ALT_NAME"),  # "or" (from ALT_NAME 8-49) - *Unusual*
            (30, 44, "ALT_NAME"),  # "or" (from ALT_NAME 8-49) - *Unusual*
            (45, 53, "NAME")  # "tomatoes" (from ALT_NAME 8-49)
        ]
    }),

    # Example 54
    ("8 to 10 corn tortillas or 4 to 6 flour tortillas", {
        "entities": [
            (0, 1, "QTY"),  # "8" (from original QTY "8 to 10" 0-7)
            (2, 7, "ALT_QTY"),  # "to 10"
            (8, 22, "NAME"),  # "corn" (from original NAME "corn tortillas" 8-22)
            (23, 48, "ALT_NAME"),  # "or"
        ]
    }),

    # Example 55
    ("One 15-ounce jar Mexican crema or 1 cup sour cream", {
        "entities": [
            # Primary Item
            (0, 3, "COMMENT"),     # "One" (refers to the jar)
            (4, 6, "QTY"),         # "15" (from "15-ounce")
            (7, 12, "UNIT"),       # "ounce" (from "15-ounce")
            (13, 16, "COMMENT"),   # "jar" (container type, not a standard unit from your list)
            (17, 24, "NAME"),      # "Mexican"
            (25, 30, "NAME"),      # "crema"
            (31,33,'ALT_NAME'),            # Alternative Item
            (34, 35, "ALT_QTY"),   # "1" (quantity for the alternative item)
            (36, 39, "ALT_UNIT"),  # "cup" (unit for the alternative item)
            (40, 44, "ALT_NAME"),  # "sour" (alternative ingredient name part)
            (45, 50, "ALT_NAME")   # "cream" (alternative ingredient name part)
        ]
    }),

    # Re-annotated data based on the FINAL REFINED rules:
    # ... (all previous examples from your earlier chunks would be here) ...

    # Example 1
    ("1/2 pound hen of the woods", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 26, "NAME"),  # "hen" (from original NAME "hen of the woods" 10-26)
        ]
    }),

    # Example 2
    ("9 pounds assorted Mediterranean fish and shellfish, such as branzino, dorade, and red mullet, scaled and gutted; and langoustines and large sea scallops, shelled",
     {
         "entities": [
             (0, 1, "QTY"),  # "9"
             (2, 8, "UNIT"),  # "pounds"
             (9, 17, "PREP"),  # "assorted"
             (18, 31, "NAME"),  # "Mediterranean"
             (32, 36, "NAME"),  # "fish"
             (37, 50, "ALT_NAME"),
             # Comma at 50 is "O"
             (52, 111, "COMMENT"),  # "such as branzino, dorade, and red mullet, scaled and gutted" (Corrected)
             # Semicolon at 111 is "O"
             # "and" (113,116) is "O"
             (117, 152, "ALT_NAME"),  # "langoustines"
             # Comma at 152 is "O"
             (154, 161, "PREP")  # "shelled" (Token ends at 161)
         ]
     }),

    # Example 3
    ("2 cups canned or jarred tomato sauce", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 13, "NAME"),  # "canned" (from original ALT_NAME "canned or jarred" 7-23)
            (14, 16, "ALT_NAME"),  # "or" (from ALT_NAME 7-23) - *Unusual*
            (17, 23, "ALT_NAME"),  # "jarred" (from ALT_NAME 7-23)
            (24, 30, "NAME"),  # "tomato"
            (31, 36, "NAME")  # "sauce"
        ]
    }),

    # Example 4
    ("1/4 cup plus 2 tablespoons sour cream", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 26, "COMMENT"),  # "plus 2 tablespoons" (Kept)
            (27, 31, "NAME"),  # "sour"
            (32, 37, "NAME")  # "cream"
        ]
    }),

    # Example 5
    ("1 cup pieces of various meats from Sunday Gravy (sausage, meatballs, braciole)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 23, "COMMENT"),  # "pieces" (24,29,"NAME"),       # "meats" (from NAME 16-44)
            (24, 29, "NAME"),  # "pieces" (24,29,"NAME"),       # "meats" (from NAME 16-44)
            (30, 47, "PREP"),  # "from" (from NAME 16-44) - *Unusual*
            (49, 78, "COMMENT"),  # "sausage, meatballs, braciole" (from original COMMENT (48,79))
        ]
    }),

    # Example 6
    ("4 cups cooked, shredded chicken or pork", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 13, "PREP"),  # "cooked" (from original PREP "cooked, shredded" 7-24, includes comma)

            (15, 31, "NAME"),  # "chicken"
            (32, 39, "ALT_NAME"),  # "or"
        ]
    }),

    # Example 7
    ("2 ounces elephant ear stems, peeled and sliced*", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 17, "NAME"),  # "elephant" (from original NAME "elephant ear stems" 9-28)
            (18, 21, "NAME"),  # "ear" (from original NAME 9-28)
            (22, 27, "NAME"),  # "stems" (from original NAME 9-28, typo in your original span end?)
            # Comma at 28 is "O"
            (29, 47, "PREP"),  # "peeled" (from original PREP "peeled and sliced*" 30-46)
        ]
    }),

    # Example 8
    ("1/2 cup torn fresh mint", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "PREP"),  # "torn" (Kept)
            (13, 18, "PREP"),  # "fresh"
            (19, 23, "NAME")  # "mint"
        ]
    }),

    # Example 9
    ("1 pound ground meat of choice (beef, veal or pork)", {  # If comments included parens
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 19, "NAME"), (20, 29, "COMMENT"),
            (30, 50, "COMMENT")
        ]
    }),

    # Example 10
    ("1 cup/250ml grated Parmigiano-Reggiano", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 11, "UNIT"),  # "cup/250ml" (Kept as original UNIT span)
            (12, 38, "NAME"),  # "grated" (Kept)
        ]
    }),

    # Example 11
    ("1/2 teaspoon cracked black pepper, eyeball it in your palm", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 20, "NAME"),  # "cracked" (from original NAME "cracked black pepper" 13-31)
            (21, 26, "NAME"),  # "black" (from original NAME 13-31)
            (27, 33, "NAME"),  # "pepper" (from original NAME 13-31, typo on your end span?)
            # Comma at 33 is "O"
            (35, 58, "COMMENT")  # "eyeball it in your palm" (Kept)
        ]
    }),

    # Example 12
    ("1 1/2 to 2 pounds firm white fish (ono, swordfish, mahi mahi, dorado)", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (from original QTY "1 1/2 to 2" 0-10)
            (6, 10, "ALT_QTY"),  # "to 2"
            (11, 17, "UNIT"),  # "pounds"
            (18, 22, "PREP"),  # "firm" (Kept)
            (23, 28, "NAME"),  # "white"
            (29, 33, "NAME"),  # "fish"
            (35, 69, "COMMENT")
        ]
    }),

    # Example 13 (Duplicate)
    ("1 pound 80 percent lean ground beef", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 18, "NAME"), (19, 23, "NAME"), (24, 30, "NAME"), (31, 35, "NAME")
        ]
    }),

    # Example 14
    ("3 tablespoons fish and meat sauce", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 27, "NAME"),  # "fish" (from original NAME "fish and meat sauce" 14-33)
            (28, 33, "NAME")  # "sauce" (from original NAME 14-33)
        ]
    }),

    # Example 15
    ("1 cup shredded cheese of choice", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 21, "NAME"),  # "cheese"
            (22, 31, "COMMENT")  # "of choice" (Kept)
        ]
    }),

    # Example 16
    ("3 pounds combined beef shank and oxtail pieces", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 17, "PREP"),  # "combined" (Kept)
            (18, 22, "NAME"),  # "beef" (from original NAME "beef shank and oxtail pieces" 18-45)
            (23, 28, "NAME"),  # "shank" (from original NAME 18-45)
            (29, 46, "ALT_NAME"),  # "and" (from original NAME 18-45) - *Unusual*
        ]
    }),

    # Example 17
    ("2 cups stout", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 12, "NAME")  # "stout"
        ]
    }),

    # Example 18
    ("1/4 cup chevril, chopped", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 15, "NAME"),  # "chevril"
            # Comma at 15 is "O"
            (17, 24, "PREP")  # "chopped" (Kept)
        ]
    }),

    # Example 19
    ("2 oranges roughly chopped", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 9, "NAME"),  # "oranges"
            (10, 17, "PREP"),  # "roughly" (from original PREP "roughly chopped" 10-25)
            (18, 25, "PREP")  # "chopped" (from original PREP "roughly chopped" 10-25)
        ]
    }),

    # Example 20
    ("1/2 teaspoon each whole fennel, cumin and coriander seeds", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon" (from original UNIT "teaspoon each" 4-17)
            (13, 17, "UNIT"),  # "each" (from original UNIT "teaspoon each" 4-17)
            (18, 23, "PREP"),  # "whole" (Kept)
            (24, 30, "NAME"),  # "fennel"
            # Comma at 30 is "O"
            (32, 37, "ALT_NAME"),  # "cumin" (from original ALT_NAME "cumin and coriander seeds" 32-55)
            (38, 57, "ALT_NAME"),  # "and" (from ALT_NAME 32-55) - *Unusual*
        ]
    }),

    # Example 22
    ("1/2 cup stout or ale", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "NAME"),  # "stout"
            (14, 20, "O"),  # "or"
        ]
    }),

    # Example 23
    ("1/4 pound foie gras or chicken liver", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 14, "NAME"),  # "foie" (from original NAME "foie gras" 10-19)
            (15, 19, "NAME"),  # "gras" (from original NAME "foie gras" 10-19)
            (20, 36, "ALT_NAME"),  # "or"
        ]
    }),

    # Example 24
    ("4 stalks celery and leaves chopped", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "COMMENT"),  # "celery"
            (9, 15, "NAME"),  # "celery"
            (16, 26, "NAME"),  # "and"
            (27, 34, "PREP")  # "chopped" (Kept)
        ]
    }),

    # Example 25
    ("2 tablespoons cracked black pepper", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, "NAME"),  # "cracked" (from original NAME "cracked black pepper" 14-33)
            (22, 27, "NAME"),  # "black" (from original NAME 14-33)
            (28, 34, "NAME")  # "pepper" (from original NAME 14-33, typo in your span end?)
        ]
    }),

    # Example 26
    ("2 tablespoons (30 milliliters) brandy, white wine or red wine", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 13, "UNIT"), (14, 30, "COMMENT"), (31, 37, "NAME"),
            (39, 49, "ALT_NAME"), (50, 52, "O"), (53, 61, "ALT_NAME")
        ]
    }),

    # Example 27
    ("1 pound refrigerator pizza dough", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 20, "PREP"),  # "refrigerator" (from original NAME "refrigerator pizza dough" 8-32)
            (21, 26, "NAME"),  # "pizza" (from original NAME 8-32)
            (27, 32, "NAME")  # "dough" (from original NAME 8-32)
        ]
    }),

    # Example 28
    ("1 (16-ounce) box spaghetti", {
        "entities": [
            (0, 1, "COMMENT"),  # "1" (Kept)
            (3, 5, "QTY"),  # "(16-ounce)" (Kept)
            (6, 11, "UNIT"),  # "(16-ounce)" (Kept)
            (13, 16, "COMMENT"),  # "box"
            (17, 26, "NAME")  # "spaghetti"
        ]
    }),

    # Example 29
    ("1/2 medium onion diced", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 10, "UNIT"),  # "medium"
            (11, 16, "NAME"),  # "onion"
            (17, 22, "PREP")  # "diced" (Kept)
        ]
    }),

    # Example 30
    ("1/2 cup M&M'S® Brand MINIS®", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "NAME"),  # "M&M'S®" (from original NAME "M&M'S® Brand MINIS®" 8-27)
            (15, 20, "NAME"),  # "Brand" (from original NAME 8-27)
            (21, 27, "NAME")  # "MINIS®" (from original NAME 8-27)
        ]
    }),

    # Example 31
    ("1 box (18.25 oz.) chocolate cake mix", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 5, "COMMENT"), (6, 17, "COMMENT"),
            (18, 27, "NAME"), (28, 32, "NAME"), (33, 36, "NAME")
        ]
    }),

    # Example 32 (Equipment Line)
    ("Other supplies:", {
        "entities": [
            (0, 14, "COMMENT")  # Whole line as COMMENT as it's equipment/instruction
        ]
    }),

    # Example 33
    ("Printable template or your favorite flower cookie cutter", {
        "entities": [
            (0, 35, "COMMENT"),  # "favorite" (from original NAME 0-56)
            (36, 42, "NAME"),  # "flower" (from original NAME 0-56)
            (43, 49, "NAME"),  # "cookie" (from original NAME 0-56, typo in your span end?)
            (50, 56, "NAME")  # "cutter" (from original NAME 0-56, typo in your span end?)
        ]
    }),

    # Example 34
    ("2 cookie sheet pans", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "NAME"),  # "cookie" (from original NAME "cookie sheet pans" 2-19)
            (9, 14, "NAME"),  # "sheet" (from original NAME 2-19)
            (15, 19, "NAME")  # "pans" (from original NAME 2-19)
        ]
    }),

    # Example 35
    ("1 resealable plastic bags", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "NAME"),  # "resealable" (from original NAME "resealable plastic bags" 2-25)
            (13, 20, "NAME"),  # "plastic" (from original NAME 2-25)
            (21, 25, "NAME")  # "bags" (from original NAME 2-25)
        ]
    }),

    # Example 36
    ("24 paper cupcake liners", {
        "entities": [
            (0, 2, "QTY"),  # "24" (Kept)
            (3, 8, "NAME"),  # "paper" (from original NAME "paper cupcake liners" 3-24)
            (9, 16, "NAME"),  # "cupcake" (from original NAME 3-24)
            (17, 23, "NAME")  # "liners" (from original NAME 3-24)
        ]
    }),

    # Example 37
    ("2 (9.75-ounce) cans chicken in water, drained", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 14, "COMMENT"),  # "(9.75-ounce)" (Kept)
            (15, 19, "UNIT"),  # "cans"
            (20, 27, "NAME"),  # "chicken"
            (28, 36, "PREP"),  # "in water" (Kept)
            # Comma at 35 is "O"
            (38, 45, "PREP")  # "drained" (Kept)
        ]
    }),

    # Example 38
    ("1/2 cup blue cheese or ranch salad dressing", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "NAME"),  # "blue" (from original NAME "blue cheese" 8-19)
            (13, 19, "NAME"),  # "cheese" (from original NAME "blue cheese" 8-19)
            (20, 43, "ALT_NAME"),  # "or"
        ]
    }),

    # Example 40
    ("1/2 pound shirataki filaments, parboiled for 1 to 2 minutes", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 19, "NAME"),  # "shirataki" (from original NAME "shirataki filaments" 10-29)
            (20, 29, "NAME"),  # "filaments" (from original NAME "shirataki filaments" 10-29)
            # Comma at 29 is "O"
            (31, 59, "PREP")  # "parboiled for 1 to 2 minutes" (Kept)
        ]
    }),

    # Example 41
    ("1/2 teaspoon cracked black pepper", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 20, "NAME"),  # "cracked"
            (21, 26, "NAME"),  # "black"
            (27, 33, "NAME")  # "pepper"
        ]
    }),

    # Example 42
    ("3 tablespoons chopped green jalepenos from a jar or can", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, "PREP"),  # "chopped" (Kept)
            (22, 27, "NAME"),  # "green"
            (28, 37, "NAME"),  # "jalepenos"
            (38, 55, "COMMENT")  # "from a jar or can" (Kept)
        ]
    }),

    # Example 43
    ("2 cups crushed chocolate coated toffee bars (heath bars)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 14, "PREP"),  # "crushed" (from original NAME "crushed chocolate coated toffee bars" 7-39)
            (15, 24, "NAME"),  # "chocolate" (from original NAME 7-39)
            (25, 31, "NAME"),  # "coated" (from original NAME 7-39)
            (32, 38, "NAME"),  # "toffee" (from original NAME 7-39, typo in original span?)
            (39, 43, "PREP"),  # "bars" (from original NAME 7-39, assuming "bars" ends at 43)
            (44, 56, "COMMENT")  # (heath bars)
        ]
    }),

    # Example 44
    ("1 cup rau ram leaves (Vietnamese cilantro)", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 9, "NAME"),  # "rau" (from original NAME "rau ram leaves" 6-20)
            (10, 13, "NAME"),  # "ram" (from original NAME 6-20)
            (14, 20, "NAME"),  # "leaves" (from original NAME 6-20)
            (21, 42, "COMMENT")
        ]
    }),

    # Example 45
    ("3 ounces fresh ginger, peeled and thinly sliced (a 1 1/2 to 2-inch piece ginger root)",
     {  # If comment included parens
         "entities": [
             (0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "PREP"), (15, 21, "NAME"),
             (23, 47, "PREP"),
             (48, 85, "COMMENT")
         ]
     }),

    # Example 46
    ("1 1/3 cups matzo meal", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/3" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 16, "NAME"),  # "matzo"
            (17, 21, "NAME")  # "meal"
        ]
    }),

    # Example 47
    ("12 large flour tortillas", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 8, "UNIT"),  # "large"
            (9, 14, "NAME"),  # "flour"
            (15, 24, "NAME")  # "tortillas"
        ]
    }),

    # Example 48
    ("1/2 cup minced chives", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "PREP"),  # "minced" (Kept)
            (15, 21, "NAME")  # "chives"
        ]
    }),

    # Example 49
    ("4 anchovies, chopped", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 11, "NAME"),  # "anchovies"
            # Comma at 11 is "O"
            (13, 20, "PREP")  # "chopped" (Kept)
        ]
    }),

    # Example 50
    ("2 3/4 cups cake flour", {
        "entities": [
            (0, 5, "QTY"),  # "2 3/4" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 15, "NAME"),  # "cake"
            (16, 21, "NAME")  # "flour"
        ]
    }),

    # Example 51
    ("2 (15-ounce) cans sliced beets, drained", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 12, "COMMENT"),  # "(15-ounce)" (Kept)
            (13, 17, "UNIT"),  # "cans"
            (18, 24, "PREP"),  # "sliced" (Kept)
            (25, 30, "NAME"),  # "beets"
            # Comma at 30 is "O"
            (32, 39, "PREP")  # "drained" (Kept)
        ]
    }),

    # Example 52
    ("3 tablespoons hot curry powder", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 17, "NAME"),  # "hot" (Kept)
            (18, 23, "NAME"),  # "curry"
            (24, 30, "NAME")  # "powder"
        ]
    }),

    # Example 53
    ("3 tablespoons dried mint", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 19, "NAME"),  # "dried" (Kept)
            (20, 24, "NAME")  # "mint"
        ]
    }),

    # Example 54
    ("1 cup dried figs, chopped", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 11, "NAME"),  # "dried" (Kept)
            (12, 16, "NAME"),  # "figs"
            # Comma at 16 is "O"
            (18, 25, "PREP")  # "chopped" (Kept)
        ]
    }),

    # Example 55
    ("2 cups cake flour", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 11, "NAME"),  # "cake"
            (12, 17, "NAME")  # "flour"
        ]
    }),

    # Example 56
    ("3 mirlitons (chayote), cooked, peeled, and diced", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 11, "NAME"), (12, 21, "COMMENT"),
            (23, 29, "PREP"), (31, 48, "PREP")
        ]
    }),

    # Example 57
    ("1/4 teaspoon dried marjoram", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 18, "NAME"),  # "dried" (Kept)
            (19, 27, "NAME")  # "marjoram"
        ]
    }),

    # Example 58
    ("2 tablespoons dried mint, crumbled", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 19, "NAME"),  # "dried" (Kept)
            (20, 24, "NAME"),  # "mint"
            # Comma at 24 is "O"
            (26, 34, "PREP")  # "crumbled" (Kept)
        ]
    }),

    # Example 59
    ("2 (6oz) cans tuna packed in oil, drained", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 7, "COMMENT"), (8, 12, "UNIT"), (13, 17, "NAME"), (18, 31, "PREP"), (33, 40, "PREP")
        ]
    }),

    # Example 60
    ("2 tablespoons finely chopped shallot", {  # If PREP "finely chopped" was (14,27)
        "entities": [
            (0, 1, "QTY"), (2, 13, "UNIT"), (14, 28, "PREP"), (29, 36, "NAME")  # Corrected shallot span
        ]
    }),

    # Example 61
    ("2 teaspoons minced garlic", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 11, "UNIT"),  # "teaspoons"
            (12, 18, "NAME"),  # "minced" (Kept)
            (19, 25, "NAME")  # "garlic"
        ]
    }),

    # Example 62
    ("6 tablespoons freshly squeezed grapefruit juice", {
        "entities": [
            (0, 1, "QTY"),  # "6" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, "PREP"),  # "freshly" (Kept)
            (22, 30, "PREP"),  # "squeezed" (Kept)
            (31, 41, "NAME"),  # "grapefruit"
            (42, 47, "NAME")  # "juice"
        ]
    }),

    # Example 63
    ("1 teaspoon dried parsley", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 16, "PREP"),  # "dried" (Kept)
            (17, 24, "NAME")  # "parsley"
        ]
    }),

    # Example 64
    ("1/2 tablespoon liquid smoke", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 14, "UNIT"),  # "tablespoon"
            (15, 21, "NAME"),  # "liquid"
            (22, 27, "NAME")  # "smoke"
        ]
    }),

    # Example 65
    ("1/4 cup mint chiffonade", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "NAME"),  # "mint"
            (13, 23, "NAME")  # "chiffonade"
        ]
    }),

    # Example 66

    ("2 1/3 cups organic, unbleached white flour", {  # If "organic, unbleached" was one PREP
        "entities": [
            (0, 5, "QTY"), (6, 10, "UNIT"), (11, 30, "PREP"),  # "organic, unbleached"
            (31, 36, "NAME"), (37, 42, "NAME")
        ]
    }),

    # Example 67
    ("2 tablespoons akamiso (brown miso)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, "NAME"),  # "akamiso"
            (22, 34, "COMMENT")
        ]
    }),

    # Example 68
    ("1 small shallot finely chopped", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "small"
            (8, 15, "NAME"),  # "shallot"
            (16, 22, "PREP"),  # "finely" (from original PREP "finely chopped" 16-30)
            (23, 30, "PREP")  # "chopped" (from original PREP "finely chopped" 16-30)
        ]
    }),

    # Example 69
    ("1 cup dried figs, quartered", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 11, "NAME"),  # "dried" (Kept)
            (12, 16, "NAME"),  # "figs"
            # Comma at 16 is "O"
            (18, 27, "PREP")  # "quartered" (Kept)
        ]
    }),

    # Example 70
    ("1/2 teaspoon dried leaf thyme", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 12, "UNIT"),  # "teaspoon"
            (13, 18, "PREP"),  # "dried" (Kept)
            (19, 23, "NAME"),  # "leaf"
            (24, 29, "NAME")  # "thyme"
        ]
    }),

    # Example 71
    ("2 ounces kalamansi juice", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 18, "NAME"),  # "kalamansi"
            (19, 24, "NAME")  # "juice"
        ]
    }),

    # Example 72
    ("8 ounces finely chopped shallot", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 23, "PREP"),
            (24, 31, "NAME")  # "shallot"
        ]
    }),

    # Example 73
    ("1 cup dried figs, halved", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 11, "NAME"),  # "dried" (Kept)
            (12, 16, "NAME"),  # "figs"
            # Comma at 16 is "O"
            (18, 24, "PREP")  # "halved" (Kept)
        ]
    }),

    # Example 74
    ("1 pound white unbleached flour", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 13, "NAME"),  # "white"
            (14, 24, "NAME"),  # "unbleached"
            (25, 30, "NAME")  # "flour"
        ]
    }),

    # Example 75
    ("1/2 head radicchio", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 8, "UNIT"),  # "head"
            (9, 18, "NAME")  # "radicchio"
        ]
    }),

    # Example 76
    ("8 ounces yuca, peeled, fibrous core removed, cut into 1-inch chunks", {  # If PREP was one span
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 13, "NAME"),
            (15, 60, "PREP")  # "peeled, fibrous core removed, cut into 1-inch chunks"
        ]
    }),

    # Example 77
    ("1 head Little Gem lettuce, shredded", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 6, "UNIT"),  # "head"
            (7, 13, "NAME"),  # "Little" (from original NAME "Little Gem lettuce" 7-24)
            (14, 17, "NAME"),  # "Gem" (from original NAME 7-24)
            (18, 25, "NAME"),  # "lettuce" (from original NAME 7-24, typo in your original end span?)
            # Comma at 25 is "O"
            (27, 35, "PREP")  # "shredded" (Kept)
        ]
    }),

    # Example 78
    ("2 pounds tripe, cleaned, boiled* and cut into strips", {  # If PREP was one span
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "NAME"),
            (16, 52, "PREP")
        ]
    }),

    # Example 79
    ("4 tablespoons plus a few drops liquid smoke, divided", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 30, "COMMENT"),  # "plus a few drops" (Kept)
            (31, 37, "NAME"),  # "liquid"
            (38, 43, "NAME"),  # "smoke"
            # Comma at 42 is "O"
            (45, 52, "COMMENT")  # "divided" (Original label COMMENT)
        ]
    }),

    # Example 80
    ("3/4 cup seasoned flour", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 16, "NAME"),  # "seasoned" (Kept)
            (17, 22, "NAME")  # "flour"
        ]
    }),

    # Example 81
    ("1 tablespoon cardamom seeds", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 21, "NAME"),  # "cardamom"
            (22, 27, "NAME")  # "seeds"
        ]
    }),

    # Example 82
    ("1/2 small head radicchio, torn into bite-sized pieces", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "small"
            (10, 14, "UNIT"),  # "head"
            (15, 24, "NAME"),  # "radicchio"
            # Comma at 24 is "O"
            (26, 53, "PREP")  # "torn into bite-sized pieces" (Kept)
        ]
    }),

    # Example 83
    ("2 (15-ounce) cans great northern or kidney beans, drained and rinsed in a colander", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 12, "COMMENT"),  # "(15-ounce)" (Kept)
            (13, 17, "UNIT"),  # "cans"
            (18, 32, "NAME"),  # "great northern" (from original NAME "great northern or kidney beans" 18-45)
            (33, 42, "ALT_NAME"),  # "kidney" (from original NAME 18-45, making it ALT here based on "or")
            (43, 48, "NAME"),  # "beans" (Common part, can be NAME)
            # Comma at 48 is "O"
            (50, 82, "PREP")  # "drained and rinsed in a colander" (Kept)
        ]
    }),

    # Example 84
    ("1 pound fresh figs, quartered", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 13, "PREP"),  # "fresh" (Kept)
            (14, 18, "NAME"),  # "figs"
            # Comma at 18 is "O"
            (20, 29, "PREP")  # "quartered" (Kept)
        ]
    }),

    # Example 85
    ("1 1/2 cups dried figs, coarsely chopped", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/2" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 16, "NAME"),  # "dried" (Kept)
            (17, 21, "NAME"),  # "figs"
            # Comma at 21 is "O"
            (23, 31, "PREP"),  # "coarsely" (from original PREP "coarsely chopped" 23-38)
            (32, 39, "PREP")  # "chopped" (from original PREP "coarsely chopped" 23-38)
        ]
    }),

    # Example 86
    ("1 to 2 teaspoons liquid smoke, optional", {
        "entities": [
            (0, 1, "QTY"),  # "1" (from original QTY "1 to 2" 0-6)
            (2, 6, "ALT_NAME"),  # "to 2"
            (7, 16, "UNIT"),  # "teaspoons"
            (17, 23, "NAME"),  # "liquid"
            (24, 29, "NAME"),  # "smoke"
            # Comma at 29 is "O"
            (31, 39, "COMMENT")  # "optional" (Kept)
        ]
    }),

    # Example 87
    ("1/4 cup basil chiffonade", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 13, "NAME"),  # "basil"
            (14, 24, "NAME")  # "chiffonade"
        ]
    }),

    # Example 88

    ("1 1/4 pounds chopped fruit (see below for suggested flavors)", {  # If comment included parens
        "entities": [
            (0, 5, "QTY"), (6, 12, "UNIT"), (13, 20, "NAME"), (21, 26, "NAME"),
            (27, 59, "COMMENT")
        ]
    }),

    # Example 89
    ("4 pounds soft, dried figs, stems removed", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 13, "PREP"),  # "soft" (Kept from original (9,13,"PREP"))
            # Comma at 13 is "O"
            (15, 20, "NAME"),  # "dried" (Kept from original (15,20,"PREP"))
            (21, 25, "NAME"),  # "figs"
            # Comma at 25 is "O"
            (27, 40, "PREP")  # "stems removed" (Kept)
        ]
    }),

    # Example 90
    ("1 pound dried black-eyed peas, picked through and any pebbles removed", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 13, "PREP"),  # "dried" (Kept)
            (14, 24, "NAME"),  # "black-eyed" (from original NAME "black-eyed peas" 14-29)
            (25, 29, "NAME"),  # "peas" (from original NAME "black-eyed peas" 14-29)
            # Comma at 29 is "O"
            (31, 69, "PREP")  # "picked through and any pebbles removed" (Kept)
        ]
    }),

    # Example 91
    ("1 1/4 cups minced shallot", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/4" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 17, "PREP"),  # "minced" (Kept)
            (18, 25, "NAME")  # "shallot"
        ]
    }),

    # Example 92
    ("1 1/3 cups shredded romaine lettuce", {
        "entities": [
            (0, 5, "QTY"),  # "1 1/3" (Kept)
            (6, 10, "UNIT"),  # "cups"
            (11, 19, "NAME"),  # "shredded" (Kept)
            (20, 27, "NAME"),  # "romaine"
            (28, 35, "NAME")  # "lettuce"
        ]
    }),
    # Re-annotated data based on the FINAL REFINED rules:
    # - NAME entities are broken into word-level NAME entities.
    # - COMMENT, PREP, ALT_NAME, QTY entities are kept as single, original spans.
    #   - QTY entities like "4 to 8": If original QTY span was "X", and "to Y" was ALT_NAME/COMMENT, that's followed.
    #     If original QTY span was "X to Y", it's kept as a single QTY span.
    # - UNIT entities are single words, normalized.
    # - Parentheses and Commas (that are not part of a kept COMMENT/PREP/ALT_NAME/QTY span)
    #   are "O" (and thus not listed in the 'entities' list).
    # - "or" in ALT_NAME is kept if it was part of your original ALT_NAME span.
    # Tokenization based on spaCy's default English tokenizer.

    # ... (all previous examples from your earlier chunks would be here) ...

    # Example 1
    ("1/4 cup sake", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "NAME")  # "sake"
        ]
    }),

    # Example 2
    ("32 ounces 100 percent ground sirloin", {
        "entities": [
            (0, 2, "QTY"),  # "32" (Kept)
            (3, 9, "UNIT"),  # "ounces"
            (10, 21, "NAME"),  # "100" (from original PREP "100 percent" 10-20)
            (22, 28, "NAME"),  # "ground"
            (29, 36, "NAME")  # "sirloin"
        ]
    }),

    # Example 3
    ("One 9-ounce cone piloncillo, grated with a cheese grater", {
        "entities": [
            (0, 3, "COMMENT"),  # "One" (Kept)
            (4, 5, "QTY"),  # "9-ounce" (Kept)
            (6, 11, "UNIT"),  # "9-ounce" (Kept)
            (12, 16, "COMMENT"),  # "cone"
            (17, 27, "NAME"),  # "piloncillo"
            # Comma at 27 is "O"
            (29, 56, "PREP")  # "grated with a cheese grater" (Kept)
        ]
    }),

    # Example 4
    ("1 teaspoon kalonji (nigella seeds), optional, see Cook's Note**", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 10, "UNIT"),  # "teaspoon"
            (11, 18, "NAME"),  # "kalonji"
            (20, 33, "COMMENT"),  # "nigella seeds" (from original COMMENT (19,34))

            # Comma at 34 is "O"
            (36, 44, "COMMENT"),  # "optional" (Kept from original (36,44,"COMMENT"))
            # Comma at 44 is "O"
            (46, 63, "COMMENT")  # "see Cook's Note**" (Kept, includes asterisks)
        ]
    }),

    # Example 5
    ("4 cups cooked, shredded chicken or pork", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 13, "PREP"),  # "cooked" (Kept from original PREP (7,24) "cooked, shredded")

            (15, 32, "NAME"),  # "shredded" (from original PREP (7,24))
            (33, 40, "ALT_NAME")  # "pork" (Kept)
        ]
    }),

    # Example 6
    ("1 tablespoon sake", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 12, "UNIT"),  # "tablespoon"
            (13, 17, "NAME")  # "sake"
        ]
    }),

    # Example 7
    ("2 pounds peeled, deveined and quartered yuca", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 8, "UNIT"),  # "pounds"
            (9, 39, "PREP"),  # "peeled" (from original PREP (9,37) "peeled, deveined and quartered")

            (40, 44, "NAME")  # "yuca"
        ]
    }),

    # Example 8
    ("2 cups burnt ends, chopped", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 12, "NAME"),  # "burnt"
            (13, 17, "NAME"),  # "ends"
            # Comma at 17 is "O"
            (19, 26, "PREP")  # "chopped" (Kept)
        ]
    }),

    # Example 9

    ("12 cups 1/2 -inch stale white bread cubes (about 1 1/4 pounds)",
     {  # If "1/2-inch" is PREP, "stale" is PREP, and comment includes parens
         "entities": [
             (0, 2, "QTY"), (3, 7, "UNIT"),
             (8, 17, "PREP"),  # "1/2-inch"
             (18, 23, "PREP"),  # "stale"
             (24, 29, "NAME"), (30, 35, "NAME"), (36, 41, "NAME"),  # white bread cubes
             (42, 61, "COMMENT")  # (about 1 1/4 pounds)
         ]
     }),

    # Example 10
    ("3 medium turnips, peeled and thinly sliced", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 8, "UNIT"),  # "medium"
            (9, 16, "NAME"),  # "turnips"
            # Comma at 16 is "O"
            (18, 42, "PREP"),  # "peeled" (Kept)
        ]
    }),

    # Example 11

    ("1 tablespoon piloncillo (Mexican cane sugar)", {  # If comment included parens
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"), (13, 23, "NAME"),
            (24, 44, "COMMENT")
        ]
    }),

    # Example 12
    ("16 ounces your favorite wash (recommended: Hog Wild Hog Wash)", {
        "entities": [
            (0, 2, "QTY"),  # "16" (Kept)
            (3, 9, "UNIT"),  # "ounces"
            (10, 23, "COMMENT"),  # "your favorite" (Kept)
            (24, 28, "ALT_NAME"),  # "wash"
            (30, 42, "COMMENT"),  # "recommended: Hog Wild Hog Wash" (from original COMMENT (29,61))
            (43, 60, "NAME"),  # "recommended: Hog Wild Hog Wash" (from original COMMENT (29,61))

        ]
    }),

    # Example 13
    ("1/2 cup Sunday Gravy", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "NAME"),  # "Sunday" (from original NAME "Sunday Gravy" 8-20)
            (15, 20, "NAME")  # "Gravy" (from original NAME "Sunday Gravy" 8-20)
        ]
    }),

    # Example 14
    ("3/4 pound farfallini, cooked and drained", {
        "entities": [
            (0, 3, "QTY"),  # "3/4" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 20, "NAME"),  # "farfallini"
            # Comma at 20 is "O"
            (22, 40, "PREP")  # "cooked and drained" (Kept)
        ]
    }),

    # Example 15
    ("1/3 cup sake", {
        "entities": [
            (0, 3, "QTY"),  # "1/3" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 12, "NAME")  # "sake"
        ]
    }),

    # Example 16
    ("4 large slices stale white bread", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 7, "UNIT"),  # "large"
            (8, 14, "PREP"),  # "slices" (Original label PREP)
            (15, 20, "PREP"),  # "stale" (Kept)
            (21, 26, "NAME"),  # "white"
            (27, 32, "NAME")  # "bread"
        ]
    }),

    # Example 17
    ("1 cup stale bread, torn and soaked in water", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 11, "PREP"),  # "stale" (Kept)
            (12, 17, "NAME"),  # "bread"
            # Comma at 17 is "O"
            (19, 43, "PREP")  # "torn and soaked in water" (Kept)
        ]
    }),

    # Example 18
    ("1 large roasting pan", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "large"
            (8, 16, "NAME"),  # "roasting"
            (17, 20, "NAME")  # "pan"
        ]
    }),

    # Example 19
    ("2 cups prepared stuffing", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 15, "NAME"),  # "prepared" (Kept)
            (16, 24, "NAME")  # "stuffing"
        ]
    }),

    # Example 20
    ("2 cups leftover stuffing", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 15, "PREP"),  # "leftover" (Kept)
            (16, 24, "NAME")  # "stuffing"
        ]
    }),

    # Example 21
    ("2 cups crushed pretzel sticks (crush in a plastic bag with a rolling pin)", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 14, "PREP"),  # "crushed" (Kept)
            (15, 22, "NAME"),  # "pretzel"
            (23, 29, "NAME"),  # "sticks"
            (31, 73, "COMMENT"),  # "crush in a plastic bag with a rolling pin" (from original COMMENT (30,75))

        ]
    }),

    # Example 23
    ("2 tablespoons freshly squeezed limejuice", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, "PREP"),  # "freshly" (Kept)
            (22, 30, "PREP"),  # "squeezed" (Kept)
            (31, 40, "NAME")  # "limejuice"
        ]
    }),

    # Example 24
    ("4 small or baby turnips, trimmed and cut into 1/2-inch pieces and blanched for 2-3 minutes", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 7, "UNIT"),  # "small"
            (8, 15, "ALT_NAME"),  # "or baby" (Kept)
            (16, 23, "NAME"),  # "turnips"
            # Comma at 23 is "O"
            (25, 78, "PREP")  # "trimmed and cut into 1/2-inch pieces and blanched for 2-3 minutes" (Kept)
        ]
    }),

    # Example 25
    ("3 tablespoons 2 percent milk", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 23, "NAME"),  # "2 percent" (Kept)
            (24, 28, "NAME")  # "milk"
        ]
    }),

    # Example 26
    ("1 cup shredded and chopped rotisserie chicken", {  # Original had "rotisserie chicken meat"
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 5, "UNIT"),  # "cup"
            (6, 26, "PREP"),  # "shredded" (from original PREP (6,26) "shredded and chopped")
            (27, 37, "NAME"),  # "rotisserie"
            (38, 45, "NAME")  # "chicken"
        ]
    }),

    # Example 27
    ("2 cups shredded aged provolone", {
        "entities": [
            (0, 1, "QTY"),  # "2" (Kept)
            (2, 6, "UNIT"),  # "cups"
            (7, 15, "PREP"),  # "shredded" (Kept)
            (16, 20, "PREP"),  # "aged" (Kept)
            (21, 30, "NAME")  # "provolone"
        ]
    }),

    # Example 28
    ("1/2 pound turnips, diced", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 9, "UNIT"),  # "pound"
            (10, 17, "NAME"),  # "turnips"
            # Comma at 17 is "O"
            (19, 24, "PREP")  # "diced" (Kept)
        ]
    }),

    # Example 29
    ("4 large sheets parchment paper", {
        "entities": [
            (0, 1, "QTY"),  # "4" (Kept)
            (2, 7, "UNIT"),  # "large"
            (8, 14, "COMMENT"),  # "sheets"
            (15, 24, "NAME"),  # "parchment"
            (25, 30, "NAME")  # "paper"
        ]
    }),

    # Example 30
    ("8 ounces dried radiatore", {
        "entities": [
            (0, 1, "QTY"),  # "8" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 14, "PREP"),  # "dried" (Kept)
            (15, 24, "NAME")  # "radiatore"
        ]
    }),

    # Example 31
    ("3 tablespoons Miracle Whip", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 21, "NAME"),  # "Miracle"
            (22, 26, "NAME")  # "Whip"
        ]
    }),

    # Example 32
    ("1 tablespoons sake, or a splash mirin may be substituted", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 13, "UNIT"),  # "tablespoons"
            (14, 18, "NAME"),  # "sake"
            # Comma at 18 is "O"
            (20, 56, "ALT_NAME")  # "or a splash mirin may be substituted" (Kept)
        ]
    }),

    # Example 33
    ("1/4 cup 300 count baby shrimp", {
        "entities": [
            (0, 3, "QTY"),  # "1/4" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 17, "COMMENT"),  # "300 count" (Kept as a descriptive comment about the shrimp)
            (18, 22, "NAME"),  # "baby"
            (23, 29, "NAME")  # "shrimp"
        ]
    }),

    # Example 34
    ("1/2 cup plus a splash dry sherry", {
        "entities": [
            (0, 3, "QTY"),  # "1/2" (Kept)
            (4, 7, "UNIT"),  # "cup"
            (8, 21, "COMMENT"),  # "plus a splash" (Kept)
            (22, 25, "NAME"),  # "dry"
            (26, 32, "NAME")  # "sherry"
        ]
    }),

    # Example 35
    ("24 small turnips, scrubbed and halved", {
        "entities": [
            (0, 2, "QTY"),  # "24" (Kept)
            (3, 8, "UNIT"),  # "small"
            (9, 16, "NAME"),  # "turnips"
            # Comma at 16 is "O"
            (18, 37, "PREP"),  # "scrubbed" (Kept from (18,26,"PREP"))
        ]
    }),
    ("1 gallon re-sealable bag", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 8, "UNIT"),  # "gallon"
            (9, 20, "NAME"),  # "re-sealable" (Kept as original PREP span)
            (21, 24, "NAME")  # "bag"
        ]
    }),

    # Example 2
    ("3 ounces pancetta, thinly sliced", {
        "entities": [
            (0, 1, "QTY"),  # "3" (Kept)
            (2, 8, "UNIT"),  # "ounces"
            (9, 17, "NAME"),  # "pancetta"
            # Comma at 17 is "O"
            (19, 25, "PREP"),  # "thinly" (from original PREP "thinly sliced" 19-32)
            (26, 32, "PREP")  # "sliced" (from original PREP "thinly sliced" 19-32)
        ]
    }),

    # Example 3
    ("12 littleneck clams", {
        "entities": [
            (0, 2, "QTY"),  # "12" (Kept)
            (3, 13, "NAME"),  # "littleneck" (from original NAME "littleneck clams" 3-19)
            (14, 19, "NAME")  # "clams" (from original NAME "littleneck clams" 3-19)
        ]
    }),

    # Example 4
    ("1 pound hot links, sliced into half-moons", {
        "entities": [
            (0, 1, "QTY"),  # "1" (Kept)
            (2, 7, "UNIT"),  # "pound"
            (8, 17, "NAME"),  # "hot" (from original NAME "hot links" 8-17)
            # Comma at 17 is "O"
            (19, 41, "PREP")  # "sliced into half-moons" (Kept)
        ]
    }),
    ("1 tsp. black pepper", {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 12, "NAME"), (13, 19, "NAME")]}),
    ("Peel of 3 large oranges, cut into large strips",
     {"entities": [(0, 7, "COMMENT"), (8, 9, "QTY"), (10, 15, "UNIT"), (16, 23, "NAME"), (25, 46, "PREP")]}),
    ("1/2 cup crema", {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "NAME")]}),
    ("1/2 pound rib-eye, finely sliced",
     {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 17, "NAME"), (19, 32, "PREP")]}),
    ("1/2 stick unsalted butter", {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 18, "NAME"), (19, 25, "NAME")]}),
    ("1/2 pound clams, manila, count necks, and little necks, scrubbed",
     {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 15, "NAME"), (17, 54, "ALT_NAME"), (56, 64, "PREP")]}),
    ("Sliced Chinese sausage (optional)",
     {"entities": [(0, 6, "PREP"), (7, 14, "NAME"), (15, 22, "NAME"), (23, 33, "COMMENT")]}),
    ("1/2 pound Prince Edward Island mussels, scrubbed", {
        "entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 16, "NAME"), (17, 23, "NAME"), (24, 30, "NAME"),
                     (31, 38, "NAME"), (40, 48, "PREP")]}),
    ("1 teaspoon chopped fresh mint",
     {"entities": [(0, 1, "QTY"), (2, 10, "UNIT"), (11, 18, "PREP"), (19, 24, "NAME"), (25, 29, "NAME")]}),
    ("1/2 cup heavy whipping cream, whipped, as an accompaniment", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "NAME"), (14, 22, "NAME"), (23, 28, "NAME"),
                     (30, 37, "PREP"), (39, 58, "COMMENT")]}),
    ("2 liters water", {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "NAME")]}),
    ("2 cups yams, peeled and diced", {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 11, "NAME"), (13, 29, "PREP")]}),
    ("12 asparagus spears, tough ends snapped off",
     {"entities": [(0, 2, "QTY"), (3, 12, "NAME"), (13, 19, "NAME"), (21, 43, "PREP")]}),
    ("4 quail, boned", {"entities": [(0, 1, "QTY"), (2, 7, "NAME"), (9, 14, "PREP")]}),
    ("Pate de foie gras", {"entities": [(0, 4, "NAME"), (5, 7, "NAME"), (8, 12, "NAME"), (13, 17, "NAME")]}),
    ("4 pieces of bacon", {"entities": [(0, 1, "QTY"), (2, 8, "COMMENT"), (12, 17, "NAME")]}),
    ("2 tablespoons (20 grams) hemp seeds",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 24, "COMMENT"), (25, 29, "NAME"), (30, 35, "NAME")]}),
    ("1 package (8) uncooked pre-seasoned meatballs", {
        "entities": [(0, 1, "QTY"), (2, 9, "UNIT"), (10, 13, "COMMENT"), (14, 22, "PREP"), (23, 35, "PREP"),
                     (36, 45, "NAME")]}),
    ("1 (26-ounce) jar chunky tomato sauce with onion and garlic", {
        "entities": [
            (0, 1, "COMMENT"),  # "1" (referring to the jar)
            # Entities from within "(26-ounce)"
            (3, 5, "QTY"),  # "26"
            (6, 11, "UNIT"),  # "ounce"
            # "jar" is now a comment
            (13, 16, "COMMENT"),  # "jar"
            # The rest remains the same
            (17, 23, "NAME"),  # "chunky"
            (24, 30, "NAME"),  # "tomato"
            (31, 36, "NAME"),  # "sauce"
            (37, 58, "PREP")  # "with onion and garlic"
        ]
    }),
    ("3 tablespoons grated Parmesan",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 20, "NAME"), (21, 29, "NAME")]}),
    ("1 (8-ounce) package shredded mozzarella cheese", {
        "entities": [(0, 1, "QTY"), (2, 11, "COMMENT"), (12, 19, "UNIT"), (20, 28, "NAME"), (29, 39, "NAME"),
                     (40, 46, "NAME")]}),
    ("Special equipment: 1 (13 by 9-inch) baking dish or 1 (10-inch) round baking dish", {
        "entities": [
            (0, 18, "COMMENT"),  # "Special equipment: "
            (20, 21, "QTY"),  # "1"
            (22, 34, "COMMENT"),  # "(13 by 9-inch)"
            (36, 42, "NAME"),  # "baking"
            (43, 47, "NAME"),  # "dish"
            (51, 80, "COMMENT")  # " or 1 (10-inch) round baking dish"
        ]
    }),
    ("2 cups shredded Monterey Jack cheese", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 15, "NAME"), (16, 24, "NAME"), (25, 29, "NAME"),
                     (30, 36, "NAME")]}),
    ("2 stalks celery", {"entities": [(0, 1, "QTY"), (2, 8, "COMMENT"), (9, 15, "NAME")]}),
    ("2 tablespoons cooked and crispy wontons, for garnish", {
        "entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 31, "PREP"),
                     (32, 39, "NAME"), (41, 53, "COMMENT")]}),
    ("2 pound soup bones, well rinsed",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 12, "NAME"), (13, 18, "NAME"), (20, 31, "PREP")]}),
    ("3 cups 1-percent milk", {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 16, "NAME"), (17, 21, "NAME")]}),
    ("Accompaniment: Canadian bacon and mixed fresh fruit", {
        "entities": [
            (0, 14, "COMMENT"),  # "Accompaniment: "
            (15, 23, "NAME"),  # "Canadian"
            (24, 29, "NAME"),  # "bacon"
            (30, 51, "ALT_NAME")  # "and mixed fresh fruit"
        ]
    }),
    ("1/2 cup raisins, optional", {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "NAME"), (17, 25, "COMMENT")]}),
    ("1/2 cup packed, fresh basil leaves (about 2 ounces), soaked, rinsed thoroughly, and dried, plus about 8 basil sprigs, for garnish",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (16, 21, "PREP"), (22, 27, "NAME"), (28, 34, "NAME"),
                   (35, 51, "COMMENT"), (53, 59, "PREP"), (61, 78, "PREP"), (80, 89, "PREP"), (91, 129, "COMMENT")]}),
    ("1 tablespoon capers, roughly chopped",
     {"entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 19, "NAME"), (21, 36, "PREP")]}),
    ("Two 5-ounce cans boneless, skinless smoked salmon packed in olive oil", {
        "entities": [(0, 3, "QTY"), (4, 11, "PREP"), (12, 16, "UNIT"), (17, 25, "NAME"), (27, 35, "NAME"),
                     (36, 42, "NAME"), (43, 49, "NAME"), (50, 69, "PREP")]}),
    ("8 large or 12 mini cannoli shells, homemade or store-bought, recipe follows", {
        "entities": [
            # Primary Item description
            (0, 1, "QTY"),         # "8"
            (2, 7, "UNIT"),        # "large"
            (8,10,'ALT_NAME'),
            # Alternative description for the same item
            (11, 13, "ALT_QTY"),   # "12" (alternative quantity for cannoli shells)
            (14, 18, "ALT_UNIT"),  # "mini" (alternative size unit for cannoli shells)
            # Core Item Name
            (19, 26, "NAME"),      # "cannoli"
            (27, 33, "NAME"),      # "shells"
            # Comma at 33 is O
            # Preparation/Source
            (35, 43, "PREP"),      # "homemade"
            # "or" (44,46) is O (connecting PREP/source alternatives)
            (47, 59, "PREP"),      # "store-bought"
            # Comma at 59 is O
            # Comment
            (61, 75, "COMMENT")    # "recipe follows"
        ]
    }),
    ("1 tablespoon plus 1/2 teaspoon cardamom seeds",
     {"entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 30, "COMMENT"), (31, 39, "NAME"), (40, 45, "NAME")]}),
    ("2 oranges, zested and juiced", {"entities": [(0, 1, "QTY"), (2, 9, "NAME"), (11, 28, "PREP")]}),
    ("3 eggs beaten with 1/2 cup water", {"entities": [(0, 1, "QTY"), (2, 6, "NAME"), (7, 32, "PREP")]}),
    ("2 1/2 pounds skin-on chicken quarters (thighs and legs)", {
        "entities": [(0, 5, "QTY"), (6, 12, "UNIT"), (13, 20, "NAME"), (21, 28, "NAME"), (29, 37, "NAME"),
                     (38, 55, "COMMENT")]}),
    ("1 tablespoon plus 1/3 cup honey",
     {"entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 25, "COMMENT"), (26, 31, "NAME")]}),
    ("2 oranges, zested, for serving",
     {"entities": [(0, 1, "QTY"), (2, 9, "NAME"), (11, 17, "PREP"), (19, 30, "COMMENT")]}),
    ("2 cups arugula, stems removed, for serving",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 14, "NAME"), (16, 29, "PREP"), (31, 42, "COMMENT")]}),
    ("2 cups finely shredded romaine",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 13, "PREP"), (14, 22, "NAME"), (23, 30, "NAME")]}),
    ("2 cups small garlic- or Italian-flavored croutons, crushed slightly", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 12, "UNIT"), (13, 20, "NAME"), (21, 40, "ALT_NAME"),
                     (41, 49, "NAME"), (51, 67, "PREP")]}),
    ("1 teaspoon Inamona (roasted, crushed kukui nut), optional but very traditional, recipe follows", {
        "entities": [(0, 1, "QTY"), (2, 10, "UNIT"), (11, 18, "NAME"), (19, 47, "COMMENT"), (49, 78, "COMMENT"),
                     (80, 94, "COMMENT")]}),
    ("1 1/2 cups peeled and finely grated sweet potato", {
        "entities": [(0, 5, "QTY"), (6, 10, "UNIT"), (11, 17, "PREP"), (18, 21, "PREP"), (22, 35, "PREP"),
                     (36, 41, "NAME"), (42, 48, "NAME")]}),
    ("1/3 heaping cup anko (sweet red bean paste; see Cook’s Note)",
     {"entities": [(0, 3, "QTY"), (4, 11, "COMMENT"), (12, 15, "UNIT"), (16, 20, "NAME"), (22, 59, "COMMENT")]}),
    ("Vegetable or canola oil", {"entities": [(0, 9, "NAME"), (10, 19, "ALT_NAME"), (20, 23, "NAME")]}),
    ("2 tablespoons SimplyNature Chia Seeds",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 26, "NAME"), (27, 31, "NAME"), (32, 37, "NAME")]}),
    ("1/2 pound toasted II Row Pale malt", {
        "entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 17, "PREP"), (18, 24, "COMMENT"),
                     (25, 29, "NAME"), (30, 34, "NAME")]}),
    ("1/4 pound 120L crystal malt",
     {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 14, "PREP"), (15, 22, "NAME"), (23, 27, "NAME")]}),
    ("1 to 2 cups crushed amaretti cookies", {
        "entities": [(0, 1, "QTY"), (2, 6, "ALT_QTY"), (7, 11, "UNIT"), (12, 19, "PREP"), (20, 28, "NAME"),
                     (29, 36, "NAME")]}),
    ("5 cups lemonade (reconstituted, not concentrate) If you make your own fresh lemonade, by all means use it!",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 15, "NAME"), (17, 47, "COMMENT"), (49, 105, "COMMENT")]}),

    ("3 St. Louie style pork ribs, 2.5 pounds each", {
        "entities": [(0, 1, "QTY"), (2, 11, "PREP"), (12, 17, "PREP"), (18, 22, "NAME"),
                     (23, 27, "NAME"), (29, 44, "COMMENT")]}),
    ("2 cups TownLine BBQ Rub (see recipe)", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 15, "NAME"), (16, 19, "NAME"), (20, 23, "NAME"),
                     (25, 36, "COMMENT")]}),
    ("2 cups TownLine BBQ Texas Mop Base (see recipe)", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 15, "NAME"), (16, 19, "NAME"), (20, 25, "NAME"),
                     (26, 29, "NAME"), (30, 34, "NAME"), (36, 46, "COMMENT")]}),
    ("1 cup store bought or TownLine BBQ Sauce (see recipe)", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 18, "PREP"), (19, 30, "ALT_NAME"),
                     (31, 34, "NAME"), (35, 40, "NAME"), (42, 53, "COMMENT")]}),
    ("2 tablespoons chopped fresh tarragon stems and leaves", {
        "entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 21, "PREP"), (22, 27, "PREP"), (28, 36, "NAME"),
                     (37, 42, "NAME"), (43, 53, "ALT_NAME")]}),
    ("2 1/2 pounds oranges, segments and pulp only",
     {"entities": [(0, 5, "QTY"), (6, 12, "UNIT"), (13, 20, "NAME"), (22, 44, "PREP")]}),
    ("2 1/2 pounds organic Seville or blood oranges, skin scored, peeled, pith scraped from peel, julienned",
     {"entities":
          [(0, 5, "QTY"), (6, 12, "UNIT"), (13, 20, "PREP"), (21, 28, "NAME"), (29, 37, "ALT_NAME"), (38, 45, "NAME"),
           (47, 101, "PREP")]}),
    ("1 tablespoon hemp seeds", {"entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 17, "NAME"), (18, 23, "NAME")]}),
    ("1 1/2 cups shredded roasted pork",
     {"entities": [(0, 5, "QTY"), (6, 10, "UNIT"), (11, 19, "PREP"), (20, 27, "NAME"), (28, 32, "NAME")]}),
    ("4 pounds #1 yams", {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 11, "PREP"), (12, 16, "NAME")]}),
    ("3 cups packed leftover pulled pork (about 1 3/4 pounds)", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 13, "PREP"), (14, 22, "PREP"), (23, 29, "NAME"),
                     (30, 34, "NAME"), (36, 55, "COMMENT")]}),
    ("1 cup store-bought brownies, cut into 1/2-inch cubes (2 to 3 brownies)", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 18, "PREP"), (19, 27, "NAME"), (29, 52, "PREP"),
                     (54, 69, "COMMENT")]}),
    ("1/2 cup nuts (optional)", {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 12, "NAME"), (13, 23, "COMMENT")]}),
    ("12 ounces ono (wahoo), cut into strips",
     {"entities": [(0, 2, "QTY"), (3, 9, "UNIT"), (10, 13, "NAME"), (14, 21, "COMMENT"), (23, 38, "PREP")]}),
    ("1 ghost pepper or other hot pepper",
     {"entities": [(0, 1, "QTY"), (2, 7, "NAME"), (8, 14, "NAME"), (15, 34, "ALT_NAME")]}),
    ("1 teaspoon plus 1 tablespoon honey",
     {"entities": [(0, 1, "QTY"), (2, 10, "UNIT"), (11, 28, "COMMENT"), (29, 34, "NAME")]}),
    ("1/8 to 1/4 teaspoon turmeric",
     {"entities": [(0, 3, "QTY"), (4, 10, "ALT_QTY"), (11, 19, "UNIT"), (20, 28, "NAME")]}),
    ("2 cups coarsely chopped fresh ginger with peel, about 8 ounces", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 15, "PREP"), (16, 23, "PREP"), (24, 29, "NAME"),
                     (30, 36, "NAME"), (37, 46, "PREP"), (48, 62, "COMMENT")]}),
    ("1/2 cup all- purpose flour",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 20, "NAME"), (21, 26, "NAME")]}),
    ("1/2 pound hot Italian sausage, links", {
        "entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 13, "NAME"), (14, 21, "NAME"), (22, 29, "NAME"),
                     (31, 36, "COMMENT")]}),
    ("2 ounces Matacuy or Peruvian pisco",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 16, "NAME"), (17, 34, "ALT_NAME")]}),
    ("2 cups Sweet 100 tomatoes, sliced in half (sweet 100 tomatoes are very small, flavorful tomatoes)", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 12, "NAME"), (13, 16, "NAME"), (17, 25, "NAME"),
                     (27, 41, "PREP"), (43, 97, "COMMENT")]}),
    ("1/4 cup white distilled vinegar",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "NAME"), (14, 23, "NAME"), (24, 31, "NAME")]}),
    ("2 cups milk", {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 11, "NAME")]}),
    ("10 to 12 large fresh basil leaves, chopped", {
        "entities": [(0, 2, "QTY"), (3, 8, "ALT_QTY"), (9, 14, "UNIT"), (15, 20, "PREP"), (21, 26, "NAME"),
                     (27, 33, "NAME"), (35, 42, "PREP")]}),
    ("1- ounce Tiamaria", {"entities": [(0, 2, "QTY"), (3, 8, "UNIT"), (9, 17, "NAME")]}),
    ("6 ounces light wheat beer",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "NAME"), (15, 20, "NAME"), (21, 25, "NAME")]}),
    ("Pickled banana pepper strips, optional",
     {"entities": [(0, 7, "PREP"), (8, 14, "NAME"), (15, 21, "NAME"), (22, 28, "NAME"), (30, 38, "COMMENT")]}),
    ("1 pound meaty yet flaky white fish, like mahi mahi or cod, skinned and de-boned, cut into chunks", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "PREP"), (14, 17, "PREP"), (18, 23, "PREP"),
                     (24, 29, "NAME"), (30, 34, "NAME"), (36, 57, "ALT_NAME"), (59, 79, "PREP"), (81, 96, "PREP")]}),
    ("1/2 cup pure olive oil",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 12, "PREP"), (13, 18, "NAME"), (19, 22, "NAME")]}),
    ("A handful grated Parmigiano-Reggiano",
     {"entities": [(0, 1, "QTY"), (2, 9, "UNIT"), (10, 16, "NAME"), (17, 36, "NAME")]}),
    ("1 roll (18 oz) Pillsbury® refrigerated chocolate chip cookies", {
        "entities": [(0, 1, "QTY"), (2, 14, "COMMENT"), (15, 25, "NAME"), (26, 38, "PREP"),
                     (39, 48, "NAME"), (49, 53, "NAME"), (54, 61, "NAME")]}),
    ("12 round starlight mints", {"entities": [(0, 2, "QTY"), (3, 8, "COMMENT"), (9, 18, "NAME"), (19, 24, "NAME")]}),
    ("4 to 6 large fresh basil leaves", {
        "entities": [(0, 1, "QTY"), (2, 6, "ALT_QTY"), (7, 12, "UNIT"), (13, 18, "PREP"), (19, 24, "NAME"),
                     (25, 31, "NAME")]}),
    ("1/3 cup minced dried crystallized ginger (not in syrup)", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (15, 20, "PREP"), (21, 33, "NAME"),
                     (34, 40, "NAME"), (42, 55, "COMMENT")]}),
    ("Basic Pizza Dough, recipe follows",
     {"entities": [(0, 5, "NAME"), (6, 11, "NAME"), (12, 17, "NAME"), (19, 33, "COMMENT")]}),
    ("1/2 cup very hot water",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 12, "PREP"), (13, 16, "PREP"), (17, 22, "NAME")]}),
    ("1/2 pound hot Italian sausage, removed from casings and crumbled", {
        "entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 13, "NAME"), (14, 21, "NAME"), (22, 29, "NAME"),
                     (31, 64, "PREP")]}),
    ("1 tablespoon peeled and grated fresh ginger", {
        "entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 19, "PREP"), (20, 23, "PREP"), (24, 30, "PREP"),
                     (31, 36, "PREP"), (37, 43, "NAME")]}),
    ("2 rolls red fruit leather rounds, such as Joray", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 11, "NAME"), (12, 17, "NAME"), (18, 25, "NAME"),
                     (26, 32, "COMMENT"), (34, 47, "COMMENT")]}),
    ("3 spearmint candy leaves", {"entities": [(0, 1, "QTY"), (2, 11, "NAME"), (12, 17, "NAME"), (18, 24, "NAME")]}),
    ("1 teaspoon Madras curry powder",
     {"entities": [(0, 1, "QTY"), (2, 10, "UNIT"), (11, 17, "NAME"), (18, 23, "NAME"), (24, 30, "NAME")]}),
    ("1 tablespoon chopped thyme-- dry is good, fresh is better",
     {"entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 20, "PREP"), (21, 28, "NAME"), (29, 57, "COMMENT")]}),
    ("4 cups fresh basil leaves, washed and thoroughly dried", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 12, "PREP"), (13, 18, "NAME"), (19, 25, "NAME"),
                     (27, 54, "PREP")]}),
    ("12 figs, fresh or dried, washed and trimmed",
     {"entities": [(0, 2, "QTY"), (3, 7, "NAME"), (9, 24, "PREP"), (25, 43, "PREP")]}),
    ("1/4 pound ricotta salata, cut into small triangles 1-inch long",
     {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 17, "NAME"), (18, 24, "NAME"), (26, 62, "PREP")]}),
    ("2 (16-ounce) cans white frosting", {
        "entities": [(0, 1, "QTY"), (3, 11, "COMMENT"), (13, 17, "UNIT"), (18, 23, "NAME"),
                     (24, 32, "NAME")]}),
    ("3 (18.25-ounce) boxes white cake mix", {
        "entities": [(0, 1, "COMMENT"),  # SHOULD BE MULTIPLIER BUT LOGIC HASNT BEEN IMPLEMENTED
                     (3, 8, "QTY"), (9, 14, "UNIT"), (16, 21, "COMMENT"), (22, 27, "NAME"),
                     (28, 32, "NAME"), (33, 36, "NAME")]}),
    ("1 tablespoon peeled and minced ginger", {
        "entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 19, "PREP"), (20, 23, "PREP"), (24, 30, "PREP"),
                     (31, 37, "NAME")]}),
    ("1 (5-inch) stalk lemongrass, halved and smashed",
     {"entities": [(0, 1, "QTY"), (2, 10, "COMMENT"), (11, 16, "COMMENT"), (17, 27, "NAME"), (29, 47, "PREP")]}),
    ("Sliced green onion tops, optional for garnish",
     {"entities": [(0, 6, "PREP"), (7, 12, "NAME"), (13, 18, "NAME"), (19, 23, "NAME"), (25, 45, "COMMENT")]}),
    ("2 cups very hot water",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 11, "PREP"), (12, 15, "PREP"), (16, 21, "NAME")]}),
    ("1 1/2 cups self-rising flour",
     {"entities": [(0, 5, "QTY"), (6, 10, "UNIT"), (11, 15, "NAME"), (16, 22, "NAME"), (23, 28, "NAME")]}),
    ("1 1/2 teaspoons vanilla (recommended: Nielsen-Massey)",
     {"entities": [(0, 5, "QTY"), (6, 15, "UNIT"), (16, 23, "NAME"), (24, 52, "COMMENT")]}),
    ("11/4 pounds tarama", {"entities": [(0, 4, "QTY"), (5, 11, "UNIT"), (12, 18, "NAME")]}),
    # Assuming 11/4 is a typo for 1 1/4 or 1/4, parsed as single QTY
    ("1 tablespoon peeled and minced fresh ginger", {
        "entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 19, "PREP"), (20, 23, "PREP"), (24, 30, "PREP"),
                     (31, 36, "PREP"), (37, 43, "NAME")]}),
    ("8 pilchards or herrings", {"entities": [(0, 1, "QTY"), (2, 11, "NAME"), (12, 23, "ALT_NAME")]}),
    ("1/2 jalapeño, seeds and stem removed, finely chopped",
     {"entities": [(0, 3, "QTY"), (4, 12, "NAME"), (14, 36, "PREP"), (38, 52, "PREP")]}),
    ("8 large eggs", {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 12, "NAME")]}),
    ("1 pound pork, beef, or chicken, cooked and chopped into bite-size pieces", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 12, "NAME"), (14, 18, "ALT_NAME"), (20, 30, "ALT_NAME"),
                     (32, 72, "PREP")]}),
    ("3 tablespoons finely shredded fresh basil leaves", {
        "entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 20, "PREP"), (21, 29, "PREP"), (30, 35, "PREP"),
                     (36, 41, "NAME"), (42, 48, "NAME")]}),
    ("3 sprigs parsley or tarragon",
     {"entities": [(0, 1, "QTY"), (2, 8, "COMMENT"), (9, 16, "NAME"), (17, 28, "ALT_NAME")]}),
    ("6 medium peeled and cored tomatillos, cut into quarters",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 25, "PREP"), (26, 37, "NAME"), (38, 55, "PREP")]}),
    ("1 1/2 pounds McIntosh, Macoun, or Empire apples", {
        "entities": [(0, 5, "QTY"), (6, 12, "UNIT"), (13, 21, "NAME"), (23, 29, "ALT_NAME"), (31, 40, "ALT_NAME"),
                     (41, 47, "NAME")]}),
    ("1/4 cup granulated or superfine sugar",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 18, "NAME"), (19, 31, "ALT_NAME"), (32, 37, "NAME")]}),
    ("A small handful parsley, finely chopped",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 15, "COMMENT"), (16, 23, "NAME"), (25, 39, "PREP")]}),
    ("2 tablespoons lemon juice, about 1/2 lemon",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 19, "NAME"), (20, 25, "NAME"), (27, 42, "COMMENT")]}),
    ("1 teaspoon smoked sweet paprika",
     {"entities": [(0, 1, "QTY"), (2, 10, "UNIT"), (11, 17, "NAME"), (18, 23, "NAME"), (24, 31, "NAME")]}),
    # Duplicate entry
    ("1/2 cup chopped fresh flat leaf parsley", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "PREP"), (16, 21, "PREP"), (22, 26, "NAME"),
                     (27, 31, "NAME"), (32, 39, "NAME")]}),
    ("2 Pink Lady apples, unpeeled",
     {"entities": [(0, 1, "QTY"), (2, 6, "NAME"), (7, 11, "NAME"), (12, 18, "NAME"), (20, 28, "PREP")]}),
    ("8 ounces toro", {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 13, "NAME")]}),
    ("2 cups shredded romaine", {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 15, "NAME"), (16, 23, "NAME")]}),
    ("2 teaspoons Madras curry powder",
     {"entities": [(0, 1, "QTY"), (2, 11, "UNIT"), (12, 18, "NAME"), (19, 24, "NAME"), (25, 31, "NAME")]}),
    ("1 pound mixed mushrooms (cremini, oyster, shiitake) chopped", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "PREP"), (14, 23, "NAME"), (25, 50, "ALT_NAME"),
                     (52, 59, "PREP")]}),
    ("1/2 to 3/4 cup grated Parmesan",
     {"entities": [(0, 3, "QTY"), (4, 10, "ALT_QTY"), (11, 14, "UNIT"), (15, 21, "NAME"), (22, 30, "NAME")]}),
    ('1/3 cup "something crunchy" (celery, apple, radish, sweet pickle slices or a combo)',
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 27, "COMMENT"),  # ""something crunchy""
                   (29, 35, "NAME"),  # "celery"
                   (37, 42, "ALT_NAME"),  # "apple"
                   (44, 50, "ALT_NAME"),  # "radish"
                   (52, 71, "ALT_NAME"),  # "sweet pickle slices"
                   (72, 82, "ALT_NAME")  # "or a combo" - corrected span
                   ]}),
    # "something crunchy" as a single NAME as it's quoted
    ("1/4 cup mayonnaise or plain yogurt",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 18, "NAME"), (19, 34, "ALT_NAME")]}),
    ("1 tablespoon peeled and grated ginger", {
        "entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 19, "PREP"), (20, 23, "PREP"), (24, 30, "PREP"),
                     (31, 37, "NAME")]}),
    ("1 tablespoon minced fresh parsley plus parsley leaves, for garnish", {
        "entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 19, "PREP"), (20, 25, "PREP"), (26, 33, "NAME"),
                     (34, 66, "COMMENT")]}),
    ("3 baby carrots, plus shredded carrots, for garnish",
     {"entities": [(0, 1, "QTY"), (2, 6, "NAME"), (7, 14, "NAME"), (16, 37, "COMMENT"), (39, 50, "COMMENT")]}),
    ("1/2 teaspoon chopped fresh flat leaf parsley", {
        "entities": [(0, 3, "QTY"), (4, 12, "UNIT"), (13, 20, "PREP"), (21, 26, "PREP"), (27, 31, "NAME"),
                     (32, 36, "NAME"), (37, 44, "NAME")]}),
    ("1 small knob ginger, peeled and grated (about 2 tablespoons)", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 12, "COMMENT"), (13, 19, "NAME"), (21, 38, "PREP"),
                     (40, 60, "COMMENT")]}),

    ("1 (1-pound) package frozen puff pastry, thawed", {
        "entities": [(0, 1, "QTY"), (3, 10, "COMMENT"), (12, 19, "UNIT"), (20, 26, "PREP"), (27, 31, "NAME"),
                     (32, 38, "NAME"), (40, 46, "PREP")]}),
    ("1/2 cup liquid (I'm using cider)", {
        "entities": [
            (0, 3, "QTY"),  # "1/2"
            (4, 7, "UNIT"),  # "cup"
            (8, 14, "COMMENT"),  # "liquid" (The generic placeholder)
            (26, 31, "NAME")  # "cider" (The specific ingredient from the parenthesis)
            # The rest of the parenthetical "(I'm using " and ")" are effectively ignored for named entities,
            # or could be part of a broader COMMENT span if desired, but tagging "cider" as NAME is key.
        ]
    }),
    ("1 banana (1/2 cup), mashed", {"entities": [(0, 1, "QTY"), (2, 8, "NAME"), (9, 18, "COMMENT"), (20, 26, "PREP")]}),
    ("4 large day-old lavash or other large flatbreads", {
        "entities": [
            (0, 1, "QTY"),  # "4"
            (2, 7, "UNIT"),  # "large"
            (8, 15, "PREP"),  # "day-old"
            (16, 22, "NAME"),  # "lavash"
            (23, 37, "ALT_NAME"),  # "or other large" (The description of the alternative)
            (38, 48, "NAME")  # "flatbreads" (The actual alternative item name)
        ]
    }),
    ("4 cups medium or large marshmallows",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 13, "NAME"), (14, 22, "ALT_UNIT"), (23, 35, "NAME")]}),
    ("1 banana, sliced", {"entities": [(0, 1, "QTY"), (2, 8, "NAME"), (10, 16, "PREP")]}),
    ("2 cups ajicitos (sweet chile peppers), halved and seeded",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 15, "NAME"), (16, 37, "COMMENT"), (39, 56, "PREP")]}),
    ("1/2 cup pisco (Peruvian brandy)",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "NAME"), (14, 31, "COMMENT")]}),
    ("4 cups Easy Mac and Cheese, recipe follows", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 11, "NAME"), (12, 26, "NAME"), (28, 42, "COMMENT")]}),
    ("1/2 banana", {"entities": [(0, 3, "QTY"), (4, 10, "NAME")]}),
    ("3 to 3 1/2 ounces enokis",
     {"entities": [(0, 1, "QTY"), (2, 10, "ALT_QTY"), (11, 17, "UNIT"), (18, 24, "NAME")]}),
    ("1/2 cup Dutch process cocoa powder", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "NAME"), (14, 21, "NAME"), (22, 27, "NAME"),
                     (28, 34, "NAME")]}),
    ("1 sheet frozen puff pastry, thawed according to package directions", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 14, "PREP"), (15, 19, "NAME"), (20, 26, "NAME"),
                     (28, 66, "PREP")]}),
    ("1 pound smoked provolone, thinly sliced",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 14, "NAME"), (15, 24, "NAME"), (26, 39, "PREP")]}),
    ("3 sprigs fresh oregano", {"entities": [(0, 1, "QTY"), (2, 8, "COMMENT"), (9, 14, "PREP"), (15, 22, "NAME")]}),
    ("3 sprigs fresh thyme", {"entities": [(0, 1, "QTY"), (2, 8, "COMMENT"), (9, 14, "PREP"), (15, 20, "NAME")]}),
    ("1 sheet frozen puff pastry, thawed", {
        "entities": [(0, 1, "QTY"), (2, 7, "COMMENT"), (8, 14, "PREP"), (15, 19, "NAME"), (20, 26, "NAME"),
                     (28, 34, "PREP")]}),
    ("1 sheet frozen puff pastry, thawed (about 8 ounces)", {
        "entities": [(0, 1, "QTY"), (2, 7, "COMMENT"), (8, 14, "PREP"), (15, 19, "NAME"), (20, 26, "NAME"),
                     (28, 34, "PREP"), (35, 50, "COMMENT")]}),
    ("1 package rocket (arugula), washed",
     {"entities": [(0, 1, "QTY"), (2, 9, "UNIT"), (10, 16, "NAME"), (17, 27, "COMMENT"), (28, 34, "PREP")]}),
    ("1 small piece brightly colored fresh or dried fruit", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "COMMENT"), (14, 22, "PREP"), (23, 30, "PREP"),
                     (31, 45, "PREP"), (46, 51, "NAME")]}),
    ("1 banana, peeled and sliced", {"entities": [(0, 1, "QTY"), (2, 8, "NAME"), (10, 27, "PREP")]}),
    ("1/4 cup nut-size kernel cereal (recommended: Grape Nuts or Ezekiel)", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 16, "PREP"), (17, 23, "NAME"),
                     (24, 30, "NAME"), (32, 66, "COMMENT")]}),
    ("1/4 cup bite-size shredded wheat", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 17, "PREP"), (18, 26, "PREP"),
                     (27, 32, "NAME")]}),
    ("1 sheet frozen puff pastry, thawed (from a 17.5-ounce package)", {
        "entities": [(0, 1, "QTY"), (2, 7, "COMMENT"), (8, 14, "PREP"), (15, 19, "NAME"), (20, 26, "NAME"),
                     (28, 34, "PREP"), (36, 62, "COMMENT")]}),
    ("3/4 cup frozen corn, carrots, peas and green beans", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "NAME"), (15, 19, "NAME"), (21, 28, "ALT_NAME"),
                     (30, 34, "ALT_NAME"), (35, 50, "ALT_NAME")]}),
    ("1 large roll, without the crust cut into small pieces",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 12, "NAME"), (14, 53, "PREP")]}),
    ("1 large (6 inches long or more) or 2 small (4 inches long or less) fish heads from cod or haddock, split lengthwise, gills removed and rinsed clean of any blood.", {
        "entities": [
            # Primary Item description
            (0, 1, "QTY"),         # "1"
            (2, 7, "UNIT"),        # "large"
            (8, 31, "COMMENT"),    # "(6 inches long or more)"
            (32,34,'ALT_NAME'),
            # Alternative description for the same item ("fish heads")
            (35, 36, "ALT_QTY"),   # "2" (alternative quantity)
            (37, 42, "ALT_UNIT"),  # "small" (alternative size unit)
            (43, 66, "COMMENT"),   # "(4 inches long or less)" (comment on the alternative size)
            # Core Item Name (applies to both descriptions)
            (67, 71, "NAME"),      # "fish"
            (72, 77, "NAME"),      # "heads"
            # Preparation details
            (78, 97, "PREP"),      # "from cod or haddock"
            # Comma at 97 is O
            (99, 115, "PREP"),     # "split lengthwise"
            # Comma at 115 is O
            (117, 130, "PREP"),    # "gills removed"
            (131, 160, "PREP")     # "and rinsed clean of any blood"
            # Period at 160 is O
        ]
    }),
    ("5 cups Strong Fish Stock, recipe follows", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 13, "NAME"), (14, 18, "NAME"), (19, 24, "NAME"),
                     (26, 40, "COMMENT")]}),
    ("16 cups, plus 1 cup water", {"entities": [(0, 2, "QTY"), (3, 7, "UNIT"), (9, 22, "COMMENT"), (23, 28, "NAME")]}),
    ("1/4 cup instant tapioca (recommended: Minute tapioca)",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "NAME"), (16, 23, "NAME"), (25, 53, "COMMENT")]}),
    ("1 cup plus 2 tablespoons good quality Dutch process cocoa powder (such as Valhrona or Cocoa Barry)", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 24, "COMMENT"), (25, 29, "PREP"), (30, 37, "PREP"),
                     (38, 43, "NAME"), (44, 51, "NAME"), (52, 57, "NAME"), (58, 64, "NAME"), (66, 98, "COMMENT")]}),
    ("4 ounces thinly sliced finocchiona",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 15, "PREP"), (16, 22, "PREP"), (23, 34, "NAME")]}),
    ("12 ounces panettone, cubed", {"entities": [(0, 2, "QTY"), (3, 9, "UNIT"), (10, 19, "NAME"), (21, 26, "PREP")]}),
    ("1 tamarind pod, flesh removed and slightly smashed",
     {"entities": [(0, 1, "QTY"), (2, 10, "NAME"), (11, 14, "NAME"), (16, 50, "PREP")]}),
    ("1 vanilla pod, split in half", {"entities": [(0, 1, "QTY"), (2, 9, "NAME"), (10, 13, "NAME"), (15, 28, "PREP")]}),
    ("2 sprigs each, cilantro and parsley, leaves chopped", {
        "entities": [(0, 1, "QTY"), (2, 8, "COMMENT"), (9, 13, "UNIT"), (15, 23, "NAME"), (24, 35, "ALT_NAME"),
                     (37, 51, "PREP")]}),
    ("1 tablespoon WuWei", {"entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 18, "NAME")]}),
    ("Small pinch ground WuWei tea; Earl Grey may be substituted", {
        "entities": [(0, 5, "UNIT"), (6, 11, "COMMENT"), (12, 18, "PREP"), (19, 24, "NAME"), (25, 28, "NAME"),
                     (30, 58, "COMMENT")]}),

    ("1 banana, peeled and sliced into 1-inch pieces", {"entities": [(0, 1, "QTY"), (2, 8, "NAME"), (10, 46, "PREP")]}),
    ("4 pounds, 8 ounces/ 2 kg oxtail*",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (10, 24, "ALT_NAME"), (25, 32, "NAME")]}),
    # Asterisk as comment
    ("5 1/4 ounces/150 g unpeeled ginger",
     {"entities": [(0, 5, "QTY"), (6, 16, "UNIT"), (19, 27, "PREP"), (28, 34, "NAME")]}),
    ("1/2 cup (1 stick butter), room temperature", {
        "entities": [
            (0, 3, "QTY"),  # "1/2"
            (4, 7, "UNIT"),  # "cup"

            (8, 16, "COMMENT"),  # "(1 stick " (part of the comment describing the butter)
            (17, 23, "NAME"),  # "butter"
            # Character 23 is ')'. If it's part of the comment.
            (23, 24, "COMMENT"),  # ")" (closing part of the comment)
            (26, 42, "PREP")  # "room temperature"
        ]
    }),
    ("2 tablespoons southern style hot sauce (recommended: Tabasco)", {
        "entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 28, "NAME"), (29, 32, "NAME"),
                     (33, 38, "NAME"), (39, 61, "COMMENT")]}),
    ("4 cups (more or less) iced cold water", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 21, "COMMENT"), (22, 26, "PREP"), (27, 31, "PREP"),
                     (32, 37, "NAME")]}),
    ("1/2 banana, ripe or overipe, mashed",
     {"entities": [(0, 3, "QTY"), (4, 10, "NAME"), (12, 27, "PREP"), (29, 35, "PREP")]}),
    ("1 sheet frozen puff pastry, such as Pepperidge Farm, thawed", {
        "entities": [(0, 1, "QTY"), (2, 7, "COMMENT"), (8, 14, "PREP"), (15, 19, "NAME"), (20, 26, "NAME"),
                     (28, 51, "COMMENT"), (53, 59, "PREP")]}),
    ("3 large yolks, room temperature",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "NAME"), (15, 31, "PREP")]}),
    ("1/2 teaspoon cream of tartar",
     {"entities": [(0, 3, "QTY"), (4, 12, "UNIT"), (13, 28, "NAME"), ]}),
    ("12 large (size U-10) fresh scallops, muscle removed", {
        "entities": [(0, 2, "QTY"), (3, 8, "UNIT"), (9, 20, "COMMENT"), (21, 26, "PREP"), (27, 35, "NAME"),
                     (37, 51, "PREP")]}),
    ("Salt and finely ground black or white pepper", {
        "entities": [
            (0, 4, "NAME"),  # "Salt"
            # "and finely" (5-15) is O (no label)
            (16, 22, "NAME"),  # "ground"
            (23, 28, "NAME"),  # "black"

            (29, 37, "ALT_NAME"),  # "or white" (The alternative applied to pepper)
            (38, 44, "NAME"),  # "pepper" (The common noun for the second part of the primary)
        ]
    }),  # "Salt" as NAME, "and finely ground black or white pepper" as ALT_NAME
    ("1 sheet frozen puff pastry, thawed in the refrigerator", {
        "entities": [(0, 1, "QTY"), (2, 7, "COMMENT"), (8, 14, "PREP"), (15, 19, "NAME"), (20, 26, "NAME"),
                     (28, 54, "PREP")]}),
    ("1 ounces crumbled true cinnamon bark, plus 4-inch pieces for garnish (optional)", {
        "entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 17, "PREP"), (18, 22, "NAME"), (23, 31, "NAME"),
                     (32, 36, "NAME"), (38, 78, "COMMENT")]}),
    ("1 large panettone, about 2 pounds",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 17, "NAME"), (19, 33, "COMMENT")]}),
    ("2 16-ounce frozen pound cakes, thawed", {
        "entities": [(0, 1, "QTY"), (2, 10, "COMMENT"), (11, 17, "PREP"), (18, 23, "NAME"), (24, 29, "NAME"),
                     (31, 37, "PREP")]}),

    ("8 ounces (2 sticks butter), at room temperature", {
        "entities": [
            (0, 1, "QTY"),  # "8"
            (2, 8, "UNIT"),  # "ounces"
            (9, 18, "COMMENT"),  # "(2 sticks " (The descriptive part of the comment around the name)
            (19, 25, "NAME"),  # "butter"
            (25, 26, "COMMENT"),  # ")" (The closing of the comment)
            (28, 47, "PREP")  # "at room temperature" (Note: "at " starts at 28, "temperature" ends at 48)
        ]
    }),
    ("2 cups shredded Simple Roasted Pork Shoulder, recipe follows", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 15, "PREP"), (16, 22, "NAME"), (23, 30, "NAME"),
                     (31, 35, "NAME"), (36, 44, "NAME"), (46, 60, "COMMENT")]}),

    ("2 limes cut into palettes", {"entities": [(0, 1, "QTY"), (2, 7, "NAME"), (8, 25, "PREP")]}),
    ("8 ounces (225g) strong Cheddar, or red Leicester, grated", {
        "entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 15, "COMMENT"), (16, 22, "PREP"), (23, 30, "NAME"),
                     (32, 49, "ALT_NAME"), (50, 56, "PREP")]}),
    ("1/2 cup Hidden Valley® Original Ranch® Light Dressing", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "NAME"), (15, 22, "NAME"), (23, 31, "NAME"),
                     (32, 38, "NAME"), (39, 44, "NAME"), (45, 53, "NAME")]}),
    ("1 cup plus 3 tablespoon boiling water",
     {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 23, "COMMENT"), (24, 31, "PREP"), (32, 37, "NAME")]}),
    ("One 3-1/2 pound free-range chicken, cut into 8 pieces and patted dry",
     {"entities": [(0, 3, "QTY"), (4, 15, "UNIT"), (16, 26, "PREP"), (27, 35, "NAME"), (36, 68, "PREP")]}),
    ("2 pounds protein of your choice, such as pork chops, chicken, pork tenderloin, beef, lamb or tofu",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 16, "NAME"), (17, 32, "COMMENT"), (33, 97, "COMMENT")]}),
    # "such as..." part is a comment listing examples
    ("1 cup toasted croutons", {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 13, "PREP"), (14, 22, "NAME")]}),
    ("1 cup chopped up steak",
     {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 13, "PREP"), (14, 16, "PREP"), (17, 22, "NAME")]}),
    ("3 to 4 teaspoons cold cultured buttermilk", {
        "entities": [(0, 1, "QTY"), (2, 6, "ALT_QTY"), (7, 16, "UNIT"), (17, 21, "PREP"), (22, 30, "PREP"),
                     (31, 41, "NAME")]}),
    ("3/4 cup dried cherries, blueberries, cranberries, golden raisins, or chopped prunes", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "NAME"), (14, 22, "NAME"), (24, 35, "ALT_NAME"),
                     (37, 49, "ALT_NAME"), (50, 65, "ALT_NAME"), (66, 83, "ALT_NAME")]}),
    ("1 chicken (3 to 4 pounds), cut up into 10 pieces",
     {"entities": [(0, 1, "QTY"), (2, 9, "NAME"), (10, 26, "COMMENT"), (27, 48, "PREP")]}),
    ("1/2 cup plus 3 tablespoons grated Gruyere",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 26, "COMMENT"), (27, 33, "PREP"), (34, 41, "NAME")]}),
    ("1 1/3 pounds cipollinis, trimmed, peeled, and left whole*", {
        "entities": [(0, 5, "QTY"), (6, 12, "UNIT"), (13, 23, "NAME"), (25, 32, "PREP"), (34, 40, "PREP"),
                     (42, 56, "PREP"), (56, 57, "COMMENT")]}),
    ("1/2 cup M&M'S® Brand MINIS®",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "NAME"), (15, 20, "NAME"), (21, 27, "NAME")]}),
    ("1 cup plus 2 T. water", {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 15, "COMMENT"), (16, 21, "NAME")]}),
    ("1 cup croutons", {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 14, "NAME")]}),
    ("12 limes, halved", {"entities": [(0, 2, "QTY"), (3, 8, "NAME"), (10, 16, "PREP")]}),
    ("6 quail, dressed", {"entities": [(0, 1, "QTY"), (2, 7, "NAME"), (9, 16, "PREP")]}),
    ("1/4 cup peeled, chopped galangal",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (16, 23, "PREP"), (24, 32, "NAME")]}),
    ("1/4 cup plus 1 tablespoon half-and-half",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 25, "COMMENT"), (26, 39, "NAME")]}),
    ("1 cup chopped red and/or green bell peppers", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 13, "PREP"), (14, 17, "NAME"), (18, 30, "ALT_NAME"),
                     (31, 35, "NAME"), (36, 43, "NAME")]}),
    ("2 cans ackee", {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 12, "NAME")]}),
    ("1 to 2 cups (250 to 500 milliliters) diced cured or pickled vegetables, such as sundried tomatoes, artichokes, olives or pickles",
     {"entities": [(0, 1, "QTY"), (2, 6, "ALT_QTY"), (7, 11, "UNIT"), (12, 36, "COMMENT"), (37, 42, "PREP"),
                   (43, 48, "PREP"), (49, 59, "ALT_NAME"), (60, 70, "NAME"), (72, 128, "COMMENT")]}),
    ("4 cups hot (not boiling) water",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 10, "PREP"), (11, 24, "COMMENT"), (25, 30, "NAME")]}),
    ("1 cup coarsely ground Italian roast, French roast or espresso coffee", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 14, "PREP"), (15, 21, "PREP"), (22, 29, "NAME"),
                     (30, 35, "NAME"), (37, 49, "ALT_NAME"), (50, 61, "ALT_NAME"), (62, 68, "NAME")]}),
    ("2 tablespoons plus 2 teaspoons Hungarian paprika",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 30, "COMMENT"), (31, 40, "NAME"), (41, 48, "NAME")]}),
    ("Serving suggestions: labneh, chopped fresh parsley, Aleppo pepper, lemon wedges and toasted pita", {
        "entities": [
            (0, 19, "COMMENT"),  # "Serving suggestions: "
            (21, 28, "NAME"),  # "labneh"
            # Comma at 28 is O
            (29, 51, "ALT_NAME"),  # "chopped" (or PREP depending on rules for ALT_NAME components)
            # Comma at 51 is O
            (52, 66, "ALT_NAME"),  # "Aleppo"  (or NAME)
            # Comma at 66 is O
            (67, 79, "ALT_NAME"),  # "lemon"   (or NAME)
            (80, 96, "ALT_NAME"),  # "and toasted" (or "and" ALT_NAME, "toasted" PREP/ALT_NAME)
        ]
    }),
    ("6 cups stuffing cubes, such as Pepperidge Farms",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 15, "NAME"), (16, 21, "NAME"), (23, 47, "COMMENT")]}),
    ("1 stick softened butter", {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 16, "PREP"), (17, 23, "NAME")]}),
    ("1/2 cup (125 milliliters) mayo",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 25, "COMMENT"), (26, 30, "NAME")]}),
    ("2 tablespoons dill, mint, chives, cilantro and/or basil", {
        "entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 18, "NAME"), (20, 24, "ALT_NAME"), (26, 32, "ALT_NAME"),
                     (34, 55, "ALT_NAME")]}),
    ("8 to 10 ounces (3 to 4 cups) grated, toasted coconut, see note", {
        "entities": [(0, 1, "QTY"), (2, 7, "ALT_QTY"), (8, 14, "UNIT"), (15, 28, "COMMENT"), (29, 35, "PREP"),
                     (37, 44, "PREP"), (45, 52, "NAME"), (54, 62, "COMMENT")]}),
    ("A few spoonfuls melted, strained apricot preserves", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 15, "UNIT"), (16, 22, "PREP"), (24, 32, "PREP"),
                     (33, 40, "NAME"), (41, 50, "NAME")]}),
    ("1/2 cup cooked, diced chicken",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (16, 21, "PREP"), (22, 29, "NAME")]}),
    # Duplicate entry
    ("1/2 cup cooked, diced chicken",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (16, 21, "PREP"), (22, 29, "NAME")]}),
    # Duplicate entry
    ("3 pounds cod or haddock, cut into 3-ounce pieces",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 12, "NAME"), (13, 24, "ALT_NAME"), (25, 48, "PREP")]}),
    ("Lemon-Habanero Tartar Sauce, recipe follows",
     {"entities": [(0, 5, "NAME"), (6, 14, "NAME"), (15, 21, "NAME"), (22, 27, "NAME"), (29, 43, "COMMENT")]}),
    ("Canola or peanut oil, for frying",
     {"entities": [(0, 6, "NAME"), (7, 16, "ALT_NAME"), (17, 20, "NAME"), (22, 32, "COMMENT")]}),
    ("4 large day-old lavash or other large flatbreads", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 15, "PREP"), (16, 22, "NAME"), (23, 37, "ALT_NAME"),
                     (38, 48, "NAME")]}),  # Applying the refined logic from previous discussion
    ("1/3 cup finely chopped fresh herb leaves (parsley, oregano, basil, marjoram, etc.)", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (15, 22, "PREP"), (23, 28, "PREP"),
                     (29, 33, "NAME"), (34, 40, "NAME"), (41, 81, "COMMENT")]}),
    ("8 whole large, fresh sardines, cleaned but with head and tail intact", {
        "entities": [(0, 1, "QTY"), (2, 7, "PREP"), (8, 13, "UNIT"), (15, 20, "PREP"), (21, 29, "NAME"),
                     (31, 68, "PREP")]}),
    ("3 limes, juiced and strained", {"entities": [(0, 1, "QTY"), (2, 7, "NAME"), (9, 28, "PREP")]}),
    ("3 limes (including zest)", {"entities": [(0, 1, "QTY"), (2, 7, "NAME"), (8, 24, "COMMENT")]}),
    ("1 tablespoon dried Italian herb blend", {
        "entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 18, "PREP"), (19, 26, "NAME"), (27, 31, "NAME"),
                     (32, 37, "NAME")]}),
    ("One 14.5-ounce can whole, peeled tomatoes", {
        "entities": [(0, 3, "QTY"), (4, 14, "COMMENT"), (15, 18, "COMMENT"), (19, 24, "PREP"), (26, 32, "PREP"),
                     (33, 41, "NAME")]}),
    ("1 pound tubetti, or elbow macaroni",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 15, "NAME"), (17, 34, "ALT_NAME")]}),
    ("1 cup torn fresh basil",
     {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 10, "PREP"), (11, 16, "PREP"), (17, 22, "NAME")]}),
    ("1 leek, very thinly sliced", {"entities": [(0, 1, "QTY"), (2, 6, "NAME"), (8, 26, "PREP")]}),
    ("2 limes, juice of", {"entities": [(0, 1, "QTY"), (2, 7, "NAME"), (9, 17, "PREP")]}),
    # "juice of" as a preparation instruction
    ("1 tablespoon plus 1 teaspoon chile powder",
     {"entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 28, "COMMENT"), (29, 34, "NAME"), (35, 41, "NAME")]}),
    ("2 bell peppers (any color is fine), thinly sliced",
     {"entities": [(0, 1, "QTY"), (2, 6, "NAME"), (7, 14, "NAME"), (16, 33, "COMMENT"), (36, 49, "PREP")]}),
    ("1 to 2 tablespoons or a good nub butter",
     {"entities": [(0, 1, "QTY"), (2, 6, "ALT_QTY"), (7, 18, "UNIT"), (19, 32, "ALT_NAME"), (33, 39, "NAME")]}),
    ("1 large onion diced", {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "NAME"), (14, 19, "PREP")]}),
    ("3/4 pound, 1 package, chorizo, very thinly sliced on an angle, pull away any loose casings", {
        "entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (11, 20, "COMMENT"), (22, 30, "NAME"), (31, 61, "PREP"),
                     (63, 90, "PREP")]}),
    ("1 1/2 cups day-old bread cubes (1-inch), preferably sourdough", {
        "entities": [(0, 5, "QTY"), (6, 10, "UNIT"), (11, 18, "PREP"), (19, 24, "NAME"), (25, 30, "NAME"),
                     (31, 39, "COMMENT"), (41, 61, "PREP")]}),
    ("1 cup plus 1 tablespoon neutral oil, such as vegetable oil", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 23, "COMMENT"), (24, 31, "NAME"), (32, 35, "NAME"),
                     (37, 58, "COMMENT")]}),
    ("1/2 cup barberries", {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 18, "NAME")]}),
    ("1 large or 2 small focaccias (about 1 pound)", {
        "entities": [
            (0, 1, "QTY"),         # "1"
            (2, 7, "UNIT"),        # "large"
            (8,10,'ALT_NAME'),
            (11, 12, "ALT_QTY"),   # "2"
            (13, 18, "ALT_UNIT"),  # "small"
            (19, 28, "NAME"),      # "focaccias"
            (30, 43, "COMMENT")    # "(about 1 pound)"
        ]
    }),
    ("1/2 teaspoon finely chopped rinsed anchovies, optional", {
        "entities": [(0, 3, "QTY"), (4, 12, "UNIT"), (13, 19, "PREP"), (20, 27, "PREP"), (28, 34, "PREP"),
                     (35, 45, "NAME"), (46, 54, "COMMENT")]}),

    ("2 ounces jenever (or gin)", {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 16, "NAME"), (17, 25, "COMMENT")]}),
    # (or gin) as COMMENT, could also be ALT_NAME
    ("2 cups Cava (Spanish sparkling wine)",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 11, "NAME"), (12, 36, "COMMENT")]}),
    ("1 cup clam juice, shrimp stock or lobster stock", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 10, "NAME"), (11, 16, "NAME"), (18, 30, "ALT_NAME"),
                     (31, 47, "ALT_NAME")]}),
    ("24 small fresh mozzarella balls packed in water, drained", {
        "entities": [(0, 2, "QTY"), (3, 8, "UNIT"), (9, 14, "PREP"), (15, 25, "NAME"), (26, 31, "NAME"),
                     (32, 48, "PREP"), (49, 56, "PREP")]}),
    ("1 tablespoon tamari", {"entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 19, "NAME")]}),
    ("1/4 pound pancetta thinly sliced",
     {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 18, "NAME"), (19, 32, "PREP")]}),
    ("1/2 cup broken spaghettini", {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (15, 26, "NAME")]}),
    ("1 free-range chicken supreme (or skinless breast)",
     {"entities": [(0, 1, "QTY"), (2, 12, "PREP"), (13, 20, "NAME"), (21, 28, "NAME"), (29, 49, "COMMENT")]}),
    # (or skinless breast) as COMMENT
    ("Approximately 4 1/2-ounces trimmed kale (a generous 1/2 cup)",
     {"entities": [(0, 13, "QTY"), (14, 26, "UNIT"), (27, 34, "PREP"), (35, 39, "NAME"), (40, 60, "COMMENT")]}),
    ("1 cup fresh basil, roughly chopped",
     {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 11, "PREP"), (12, 17, "NAME"), (19, 34, "PREP")]}),
    ("3/4 pound, 3 links, hot or sweet Italian sausage, split and meat removed from casing", {"entities": [
        (0, 3, "QTY"),
        (4, 9, "UNIT"),
        (11, 18, "ALT_QTY"),
        (20, 32, "PREP"),     # Corrected: "hot or sweet"
        (33, 48, "NAME"),     # Corrected: "Italian sausage" (removed leading space)
        (50, 84, "PREP")
    ]}),
    ("3 tablespoons tamari", {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 20, "NAME")]}),
    ("1/4 cup tamari", {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "NAME")]}),
    ("1/4 cup shari", {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "NAME")]}),
    ("Use a scant 1/4 cup of shari for every cup of raw rice.", {"entities": [(0, 55, "COMMENT")]}),
    ("1/4 pound cooked and pulled turkey", {
        "entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 16, "PREP"), (17, 20, "PREP"), (21, 27, "PREP"),
                     (28, 34, "NAME")]}),
    ("1 pound fondant, store-bought", {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 15, "NAME"), (17, 29, "PREP")]}),
    ("10 to 12 ounces chopped or pulled Smokehouse Brisket, recipe follows", {
        "entities": [(0, 2, "QTY"), (3, 8, "ALT_QTY"), (9, 15, "UNIT"), (16, 23, "PREP"), (24, 33, "ALT_NAME"),
                     (34, 44, "NAME"), (45, 52, "NAME"), (54, 68, "COMMENT")]}),
    ("3 quarter-size pieces gingeroot, bruised",
     {"entities": [(0, 1, "QTY"), (2, 14, "COMMENT"), (15, 21, "COMMENT"), (22, 32, "NAME"), (33, 40, "PREP")]}),
    ("4 cups fresh coconut milk, or combination regular and coconut milk", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 12, "PREP"), (13, 20, "NAME"), (21, 25, "NAME"),
                     (27, 66, "ALT_NAME")]}),
    ("1/3 cup schmaltz (rendered chicken fat)",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 16, "NAME"), (17, 38, "COMMENT")]}),
    ("3 aluminum cans", {"entities": [(0, 1, "QTY"), (2, 10, "NAME"), (11, 15, "NAME")]}),
    # "aluminum cans" as equipment/NAME
    ("7.1 ounces (200 grams) verjus (vinegar from unripened white grapes)",
     {"entities": [(0, 3, "QTY"), (4, 10, "UNIT"), (11, 22, "COMMENT"), (23, 29, "NAME"), (30, 67, "COMMENT")]}),
    ("20 (Extra large, under 10 scallops per pound or U-10's) sea scallops",
     {"entities": [(0, 2, "QTY"), (3, 55, "COMMENT"), (56, 59, "NAME"), (60, 68, "NAME")]}),
    ("1 cup tamari", {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 12, "NAME")]}),
    ("2 pounds Kalbi (marinated short ribs), recipe follows",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "NAME"), (15, 37, "COMMENT"), (39, 53, "COMMENT")]}),
    ("1/4 teaspoon crushed pepperoncino",
     {"entities": [(0, 3, "QTY"), (4, 12, "UNIT"), (13, 20, "PREP"), (21, 33, "NAME")]}),
    ("6 large button mushrooms or small portabello, about 1 pound/450 g", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 14, "NAME"), (15, 24, "NAME"), (25, 45, "ALT_NAME"),
                     (46, 65, "COMMENT")]}),
    ("1 teaspoon fivespice powder", {"entities": [(0, 1, "QTY"), (2, 10, "UNIT"), (11, 20, "NAME"), (21, 27, "NAME")]}),
    ("1 quart hard cider", {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 12, "NAME"), (13, 18, "NAME")]}),
    ("1/4 to 1/2 cup of any wine or vermouth", {
        "entities": [(0, 3, "QTY"), (4, 10, "ALT_QTY"), (11, 14, "UNIT"), (18, 21, "NAME"), (22, 26, "NAME"),
                     (27, 38, "ALT_NAME")]}),
    ("1/3 to 1/2 cup of any wine or vermouth", {
        "entities": [(0, 3, "QTY"), (4, 10, "ALT_QTY"), (11, 14, "UNIT"), (18, 21, "NAME"), (22, 26, "NAME"),
                     (27, 38, "ALT_NAME")]}),
    ("1/4 to 1/3 cup of any wine or vermouth", {
        "entities": [(0, 3, "QTY"), (4, 10, "ALT_QTY"), (11, 14, "UNIT"), (18, 21, "NAME"), (22, 26, "NAME"),
                     (27, 38, "ALT_NAME")]}),
    ("2 pounds Portuguese chourico (linguica is the milder sausage for the faint of heart.)",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 19, "NAME"), (20, 28, "NAME"), (29, 85, "COMMENT")]}),
    ("1/2 cup chopped walnuts, optional",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "NAME"), (16, 23, "NAME"), (25, 33, "COMMENT")]}),
    ("1/4 pound giroles (very small) or morels, washed", {
        "entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 17, "NAME"), (18, 30, "COMMENT"), (31, 41, "ALT_NAME"),
                     (42, 48, "PREP")]}),
    ("About 1/4 cup mixed Hanukkah candies and sprinkles (dreidels, Hanukkah sprinkle mix, nonpareils, etc.)", {
        "entities": [(0, 9, "QTY"), (10, 13, "UNIT"), (14, 19, "PREP"), (20, 28, "NAME"), (29, 36, "NAME"),
                     (37, 50, "ALT_NAME"), (51, 102, "COMMENT")]}),
    ("1 1/2 cups fresh favas", {"entities": [(0, 5, "QTY"), (6, 10, "UNIT"), (11, 16, "PREP"), (17, 22, "NAME")]}),
    ("Fish head and bones", {"entities": [(0, 4, "NAME"), (5, 9, "NAME"), (10, 19, "ALT_NAME")]}),
    ("8 ounces peppercress", {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 20, "NAME")]}),
    ("3 cups sliced ramps, bulbs and leaves (or an equal amount of leeks and 1 garlic clove)", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 13, "PREP"), (14, 19, "NAME"), (21, 37, "PREP"),
                     (38, 86, "COMMENT")]}),
    ("1/3 cup dried cherries, roughly chopped",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "PREP"), (14, 22, "NAME"), (24, 39, "PREP")]}),
    ("2 cups tightly packed greens such as kale, arugula or mint", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 14, "PREP"), (15, 21, "PREP"), (22, 28, "NAME"),
                     (29, 58, "COMMENT")]}),
    ("1/4 cup tropical punch mix",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 16, "NAME"), (17, 22, "NAME"), (23, 26, "NAME")]}),
    ("1/2 to 2/3 cup freshly grated caciocavallo or Pecorino cheese", {
        "entities": [(0, 3, "QTY"), (4, 10, "ALT_QTY"), (11, 14, "UNIT"), (15, 22, "PREP"), (23, 29, "PREP"),
                     (30, 42, "NAME"), (43, 61, "ALT_NAME")]}),
    ("1 cup chicken stock/poaching liquid from Poached Chicken, recipe follows",
     {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 13, "NAME"), (14, 48, "ALT_NAME"), (49, 72, "COMMENT")]}),
    ("1 pound fondant in the color of your choice",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 15, "NAME"), (16, 43, "PREP")]}),
    ("Cornstarch or powdered sugar", {"entities": [(0, 10, "NAME"), (11, 28, "ALT_NAME")]}),
    ("1 1/2 teaspoons, 1/2 a palm full, cumin",
     {"entities": [(0, 5, "QTY"), (6, 15, "UNIT"), (17, 33, "ALT_NAME"), (34, 39, "NAME")]}),
    ("1 tablespoons grill seasoning (recommended: McCormick Montreal Seasoning)",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 19, "NAME"), (20, 29, "NAME"), (30, 73, "COMMENT")]}),
    ("3- ounce jar osetra caviar",
     {"entities": [(0, 2, "QTY"), (3, 8, "UNIT"), (9, 12, "COMMENT"), (13, 19, "NAME"), (20, 26, "NAME")]}),
    # "jar" as comment
    ("1 1/2 pounds steamers, scrubbed",
     {"entities": [(0, 5, "QTY"), (6, 12, "UNIT"), (13, 21, "NAME"), (23, 31, "PREP")]}),
    ("2 handful fresh basil, torn, plus more for serving", {
        "entities": [(0, 1, "QTY"), (2, 9, "COMMENT"), (10, 15, "PREP"), (16, 21, "NAME"), (23, 27, "PREP"),
                     (29, 50, "COMMENT")]}),
    ("6 to 8 tortillas or buns",
     {"entities": [(0, 1, "QTY"), (2, 6, "ALT_QTY"), (7, 16, "NAME"), (17, 24, "ALT_NAME")]}),

    ("Optional toppers: diced avocado, chopped tomatoes, fresh cilantro leaves, lime wedges, sliced radishes, shaved cabbage, sliced jalapenos",
     {"entities": [(0, 16, "COMMENT"),  # "Optional toppers: "
                   (18, 23, "PREP"),  # "diced"
                   (24, 31, "NAME"),  # "avocado"
                   (33, 136, "ALT_NAME"),
                   # "chopped tomatoes, fresh cilantro leaves, lime wedges, sliced radishes, shaved cabbage, sliced jalapenos"
                   ]}),
    ("3 tablespoons saikyo (sweet white miso)",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 20, "NAME"), (21, 39, "COMMENT")]}),
    ("2 tablespoons akamiso (brown miso)",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 21, "NAME"), (22, 34, "COMMENT")]}),
    ("1/2 pound your choice cooked and chopped meat", {
        "entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 21, "COMMENT"), (22, 28, "PREP"), (29, 32, "PREP"),
                     (33, 40, "PREP"), (41, 45, "NAME")]}),
    ("One 10- to 12-inch flour tortilla",
     {"entities": [(0, 3, "QTY"), (4, 18, "COMMENT"), (19, 24, "NAME"), (25, 33, "NAME")]}),
    ("1/2 pound dried great Northern beans (1 1/4 cups), picked through to remove any debris and rinsed", {
        "entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 15, "PREP"), (16, 21, "NAME"), (22, 30, "NAME"),
                     (31, 36, "NAME"), (37, 50, "COMMENT"), (51, 97, "PREP")]}),
    ("1/2 cup cashews, coarsely chopped",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "NAME"), (17, 33, "PREP")]}),
    ("1 cup mixed dried fruit, such as currants, diced pears, diced apricots, cranberries, raisins, blueberries, or chopped dates",
     {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 11, "PREP"), (12, 17, "PREP"), (18, 23, "NAME"),
                   (25, 123, "COMMENT")]}),
    ("1/4 cup vegetable oil, like soy, peanut, or corn",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 17, "NAME"), (18, 21, "NAME"), (23, 48, "COMMENT")]}),
    ("1 tablespoon preserved bean curd or fish sauce", {
        "entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 22, "PREP"), (23, 27, "NAME"), (28, 32, "NAME"),
                     (33, 46, "ALT_NAME")]}),
    ("1/2 pound snowpea, trimmed", {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 17, "NAME"), (19, 26, "PREP")]}),

    ("3 cups Quick Cake Mix, recipe follows", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 12, "NAME"), (13, 17, "NAME"), (18, 21, "NAME"),
                     (23, 37, "COMMENT")]}),
    ("1 head cauliflower, cut into florets",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 18, "NAME"), (20, 36, "PREP")]}),
    ("8 rolls", {"entities": [(0, 1, "QTY"), (2, 7, "NAME")]}),
    ("1 container (8 oz.) reduced fat frozen whipped, topping, thawed", {
        "entities": [(0, 1, "COMMENT"), (2, 11, "COMMENT"), (13, 14, "QTY"), (15, 18, "UNIT"), (20, 27, "PREP"),
                     (28, 31, "PREP"), (32, 38, "PREP"), (39, 46, "PREP"), (48, 55, "NAME"), (57, 63, "PREP")]}),
    ("2 teaspoons grated fresh wasabi (* Chef's Note)", {
        "entities": [(0, 1, "QTY"), (2, 11, "UNIT"), (12, 18, "PREP"), (19, 24, "PREP"), (25, 31, "NAME"),
                     (32, 47, "COMMENT")]}),
    ("2 pounds cut up pork, chicken, or beef", {
        "entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 12, "PREP"), (13, 15, "PREP"), (16, 20, "NAME"),
                     (22, 29, "ALT_NAME"), (31, 38, "ALT_NAME")]}),
    ("2 ounces kirschwasser", {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 21, "NAME")]}),
    ("2 pounds cauliflower, cut into large florets",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 20, "NAME"), (22, 44, "PREP")]}),
    ("150 grams pomelo, segmented", {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 16, "NAME"), (18, 27, "PREP")]}),
    ("2 tablespoons St. Germaine liqueur",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 17, "NAME"), (18, 26, "NAME"), (27, 34, "NAME")]}),
    ("1/2 cup thinly sliced scallion",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (15, 21, "PREP"), (22, 30, "NAME")]}),
    ("I cup plus 2 tablespoons superfine sugar",
     {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 24, "COMMENT"), (25, 34, "NAME"), (35, 40, "NAME")]}),
    # "I" assumed to be "1"
    ("2 grapefruits, segmented and cut into small dice",
     {"entities": [(0, 1, "QTY"), (2, 13, "NAME"), (15, 24, "PREP"), (25, 48, "PREP")]}),
    ("1 medium head cauliflower, cut into florets",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 13, "UNIT"), (14, 25, "NAME"), (27, 43, "PREP")]}),
    ("3 tablespoons grated cheese, Parmigiano or Romano", {
        "entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 20, "PREP"), (21, 27, "NAME"), (29, 39, "NAME"),
                     (40, 49, "ALT_NAME")]}),
    ("1 ounce St. Germain liqueur",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 11, "NAME"), (12, 19, "NAME"), (20, 27, "NAME")]}),
    ("1 1/4 pounds large lotus roots (See Cook’s Note)", {
        "entities": [(0, 5, "QTY"), (6, 12, "UNIT"), (13, 18, "UNIT"), (19, 24, "NAME"), (25, 30, "NAME"),
                     (31, 48, "COMMENT")]}),
    ("1 cup machj lettuce (or other seasonal 'soft' lettuce)",
     {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 11, "NAME"), (12, 19, "NAME"), (20, 54, "COMMENT")]}),
    ("1 head cauliflower, cut into florets (about 1 pound)",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 18, "NAME"), (20, 36, "PREP"), (37, 52, "COMMENT")]}),
    ("2 tablespoons jarred capers in brine, drained", {
        "entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 20, "PREP"), (21, 27, "NAME"), (28, 36, "PREP"),
                     (38, 45, "PREP")]}),
    ("2 medium sized jicamas, peeled and thinly sliced", {
        "entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "COMMENT"), (15, 22, "NAME"), (24, 30, "PREP"),
                     (31, 34, "PREP"), (35, 41, "PREP"), (42, 48, "PREP")]}),
    ("2 teaspoons chopped fresh basil or tarragon leaves", {
        "entities": [(0, 1, "QTY"), (2, 11, "UNIT"), (12, 19, "PREP"), (20, 25, "PREP"), (26, 31, "NAME"),
                     (32, 43, "ALT_NAME"), (44, 50, "NAME")]}),
    ("1/2 cup halved and thinly sliced sopressata", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (15, 18, "PREP"), (19, 25, "PREP"),
                     (26, 32, "PREP"), (33, 43, "NAME")]}),
    ("1/4 cup dried cherries or currants",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "NAME"), (14, 22, "NAME"), (23, 34, "ALT_NAME")]}),
    ("1 cup chopped, about 2 ounces, assorted lettuce (butter, red leaf, green leaf)", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 13, "PREP"), (15, 30, "COMMENT"), (31, 39, "PREP"),
                     (40, 47, "NAME"), (48, 78, "COMMENT")]}),
    ("3 tablespoons chopped fresh tarragon and/or parsley", {
        "entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 21, "PREP"), (22, 27, "PREP"), (28, 36, "NAME"),
                     (37, 51, "ALT_NAME")]}),
    ("6 ounces prepared mole, recipe follows",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 17, "PREP"), (18, 22, "NAME"), (24, 38, "COMMENT")]}),
    ("A few leaves fresh basil, torn", {
        "entities": [(0, 1, "QTY"), (2, 5, "COMMENT"), (6, 12, "PREP"), (13, 18, "PREP"), (19, 24, "NAME"),
                     (26, 30, "PREP")]}),
    ("2/3 cup chopped dried cherries (3 ounces)", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "PREP"), (16, 21, "NAME"), (22, 30, "NAME"),
                     (31, 41, "COMMENT")]}),
    ("1 to 2 tablespoons jam (any flavor)",
     {"entities": [(0, 1, "QTY"), (2, 6, "ALT_QTY"), (7, 18, "UNIT"), (19, 22, "NAME"), (23, 35, "COMMENT")]}),
    ("1/4 cup small-curd cottage cheese",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 18, "PREP"), (19, 26, "NAME"), (27, 33, "NAME")]}),
    ("8 cellophane bags and twist ties or ribbons for wrapping",
     {"entities": [(0, 1, "QTY"), (2, 12, "NAME"), (13, 17, "NAME"), (18, 56, "COMMENT")]}),
    ("1/2 cup grated cheese, Parmigiano or Romano", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "NAME"), (15, 21, "NAME"), (23, 33, "ALT_NAME"),
                     (34, 43, "ALT_NAME")]}),
    ("1 stick margarine, slightly melted",
     {"entities": [(0, 1, "QTY"), (2, 7, "COMMENT"), (8, 17, "NAME"), (19, 34, "PREP")]}),
    ("1 1/2 tablespoons each diced assorted peppers (red, yellow and green)", {
        "entities": [(0, 5, "QTY"), (6, 17, "UNIT"), (18, 22, "COMMENT"), (23, 28, "PREP"), (29, 37, "PREP"),
                     (38, 45, "NAME"), (46, 69, "COMMENT")]}),
    ("6 cups sliced mixed mushrooms (shiitake and cremini)", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 13, "PREP"), (14, 19, "PREP"), (20, 29, "NAME"),
                     (30, 52, "COMMENT")]}),
    ("2 tablespoons 1/4 inch thick strips basil", {
        "entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 22, "PREP"), (23, 28, "PREP"), (29, 35, "PREP"),
                     (36, 41, "NAME")]}),
    ("8-ounce piece veal butt tenderloin", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "COMMENT"), (14, 18, "NAME"), (19, 23, "NAME"),
                     (24, 34, "NAME")]}),
    ("1 tablespoon scallion, minced",
     {"entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 21, "NAME"), (23, 29, "PREP")]}),
    ("3 tablespoons finely chopped fresh",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 20, "PREP"), (21, 28, "PREP"), (29, 34, "NAME")]}),
    # Assuming "fresh" refers to an unnamed herb here
    ("3 tablespoons thinly sliced scallion",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 20, "PREP"), (21, 27, "PREP"), (28, 36, "NAME")]}),
    ("3/4 cup Aloha shoyu (it's the best, the only really)",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "NAME"), (14, 19, "NAME"), (20, 52, "COMMENT")]}),
    ("1 cup mochiko (rice flour)", {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 13, "NAME"), (14, 26, "COMMENT")]}),
    ("1/2 pound brick cheese, shredded",
     {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 15, "NAME"), (16, 22, "NAME"), (24, 32, "PREP")]}),
    ("1 pound, 1inch thick swordfish",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (9, 14, "COMMENT"), (15, 20, "PREP"), (21, 30, "NAME")]}),
    ("1 cup margarine, melted", {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 15, "NAME"), (17, 23, "PREP")]}),
    ("2 tablespoons (2 turns around the pan in a slow drizzle) vegetable or wok oil",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 56, "COMMENT"), (57, 66, "NAME"), (67, 77, "ALT_NAME")]}),
    ("1 cup salted and roasted mixed nuts", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 12, "PREP"), (13, 16, "PREP"), (17, 24, "PREP"),
                     (25, 30, "PREP"), (31, 35, "NAME")]}),
    ("1/4 cup medium-sweet sherry, optional",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 20, "PREP"), (21, 27, "NAME"), (29, 37, "COMMENT")]}),
    ("1/3 cup packed chopped fresh basil, plus small leaves for garnish", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (15, 22, "PREP"), (23, 28, "PREP"),
                     (29, 34, "NAME"), (36, 65, "COMMENT")]}),
    ("2 teaspoon dried basil, crumbled",
     {"entities": [(0, 1, "QTY"), (2, 10, "UNIT"), (11, 16, "PREP"), (17, 22, "NAME"), (24, 32, "PREP")]}),
    ("12 guajillos or 6 chilcostles", {"entities": [(0, 2, "QTY"), (3, 12, "NAME"), (13, 29, "ALT_NAME")]}),
    ("3 tablespoons plus 1/4 cup barley malt syrup", {
        "entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 26, "COMMENT"), (27, 33, "NAME"), (34, 38, "NAME"),
                     (39, 44, "NAME")]}),
    ("1180 grams (about 2.6 pounds) high-gluten flour", {
        "entities": [(0, 4, "QTY"), (5, 10, "UNIT"), (11, 29, "COMMENT"), (30, 34, "PREP"), (35, 41, "PREP"),
                     (42, 47, "NAME")]}),
    ("1 (32-ounce) jar mixed pickles, chopped", {
        "entities": [(0, 1, "COMMENT"), (3, 5, "QTY"), (6, 11, "UNIT"), (13, 16, "COMMENT"), (17, 22, "PREP"),
                     (23, 30, "NAME"), (32, 39, "PREP")]}),
    ("3 tablespoons prepared key lime curd", {
        "entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 22, "PREP"), (23, 26, "NAME"), (27, 31, "NAME"),
                     (32, 36, "NAME")]}),
    ("6 rolls, for serving", {"entities": [(0, 1, "QTY"), (2, 7, "NAME"), (9, 20, "COMMENT")]}),
    ("2 tablespoons liquid from marinated artichoke hearts",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 20, "NAME"), (21, 52, "PREP")]}),
    ("1/2 cup grated Parmiginao-Reggiano",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (15, 34, "NAME")]}),
    ("1/4 cup hot water", {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 11, "PREP"), (12, 17, "NAME")]}),
    ("5 ounces shredded meatballs", {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 17, "PREP"), (18, 27, "NAME")]}),
    ("4 tablespoons rendered goose fat or vegetable oil", {
        "entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 22, "PREP"), (23, 28, "NAME"), (29, 32, "NAME"),
                     (33, 49, "ALT_NAME")]}),
    ("12 ounces pitted, roughly chopped mixed olives, approximately 2 cups", {
        "entities": [(0, 2, "QTY"), (3, 9, "UNIT"), (10, 16, "PREP"), (18, 25, "PREP"), (26, 33, "PREP"),
                     (34, 39, "PREP"), (40, 46, "NAME"), (48, 68, "COMMENT")]}),
    ("1/4 cup plus 1 tablespoon freshly squeezed lemon juice (3 lemons)", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 25, "COMMENT"), (26, 33, "PREP"), (34, 42, "PREP"),
                     (43, 48, "NAME"), (49, 54, "NAME"), (55, 65, "COMMENT")]}),
    ("3/4 cup plus 2 tablespoons water",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 26, "COMMENT"), (27, 32, "NAME")]}),
    ("Scant 1/2 cup heavy cream", {"entities": [(0, 9, "QTY"), (10, 13, "UNIT"), (14, 19, "NAME"), (20, 25, "NAME")]}),
    ("1 quart (4 cups) stock or water",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 16, "COMMENT"), (17, 22, "NAME"), (23, 31, "ALT_NAME")]}),
    ("2 cups plus 3 tablespoons or 500 grams water",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 38, "COMMENT"), (39, 44, "NAME")]}),
    ("1 cup plus 2 tablespoons water (250 grams)",
     {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 24, "COMMENT"), (25, 30, "NAME"), (31, 42, "COMMENT")]}),
    ("3 teaspoons Earl Grey tea, ground in a blender or spice grinder until it is a powder", {
        "entities": [(0, 1, "QTY"), (2, 11, "UNIT"), (12, 16, "NAME"), (17, 21, "NAME"), (22, 25, "NAME"),
                     (27, 84, "PREP")]}),
    ("1 cup medium dice celery, no leaves", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 12, "PREP"), (13, 17, "PREP"), (18, 24, "NAME"),
                     (26, 35, "COMMENT")]}),
    ("2 quarts hot water", {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 12, "PREP"), (13, 18, "NAME")]}),
    ("1 gallon, plus 48 ounces water",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (10, 24, "COMMENT"), (25, 30, "NAME")]}),
    ("2 tablespoons chopped papalo or cilantro",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 21, "PREP"), (22, 28, "NAME"), (29, 40, "ALT_NAME")]}),
    ("1/4 cup plus 1 tablespoon cream",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 25, "COMMENT"), (26, 31, "NAME")]}),
    ("1 stalk celery", {"entities": [(0, 1, "QTY"), (2, 7, "COMMENT"), (8, 14, "NAME")]}),
    # "stalk" as COMMENT as it's not a standard unit for "celery" the ingredient itself but a form descriptor
    ("1 can (10 oz each) Ro*Tel® Mexican Diced Tomatoes with Lime Juice & Cilantro, drained", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 18, "COMMENT"), (19, 25, "NAME"), (25, 26, "NAME"),
                     (27, 34, "NAME"), (35, 76, "PREP"), (78, 85, "COMMENT")]}),
    ("1/4 cup plus 3 tablespoons ketchup",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 26, "COMMENT"), (27, 34, "NAME")]}),
    ("2 tablespoons Gwen's Cole Slaw, recipe follows", {
        "entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 20, "NAME"), (21, 25, "NAME"), (26, 30, "NAME"),
                     (32, 46, "COMMENT")]}), ("1/4 cup shredded celery (use a food processor)", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 16, "PREP"), (17, 23, "NAME"), (24, 46, "COMMENT")]}),
    ("2 carrots peeled and grated",
     {"entities": [(0, 1, "QTY"), (2, 9, "NAME"), (10, 16, "PREP"), (17, 20, "PREP"), (21, 27, "PREP")]}),
    ("3 ounces (about 1 cup) piquin chiles",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 22, "COMMENT"), (23, 29, "NAME"), (30, 36, "NAME")]}),
    ("6 pickles, processed in a food processor", {"entities": [(0, 1, "QTY"), (2, 9, "NAME"), (11, 40, "PREP")]}),
    ("36 mini paper cupcake liners",
     {"entities": [(0, 2, "QTY"), (3, 7, "COMMENT"), (8, 13, "NAME"), (14, 21, "NAME"), (22, 28, "NAME")]}),
    # Equipment
    ("2 laurel or bay leaves", {"entities": [(0, 1, "QTY"), (2, 8, "NAME"), (9, 22, "ALT_NAME")]}),
    ("1/2 cup plus 1 tablespoon grated Parmigiano-Reggiano (about 2 1/2 ounces)", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 25, "COMMENT"), (26, 32, "PREP"), (33, 52, "NAME"),
                     (53, 73, "COMMENT")]}),
    ("1/4 cup unsweeteend cocoa powder",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 19, "PREP"), (20, 25, "NAME"), (26, 32, "NAME")]}),
    ("2 tablespoons hot water", {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 17, "PREP"), (18, 23, "NAME")]}),
    ("2 tablespoons arrow root", {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 19, "NAME"), (20, 24, "NAME")]}),
    ("3 Tbsp. I Can't Believe It's Not Butter!® Spread, divided", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 9, "NAME"), (10, 15, "NAME"), (16, 23, "NAME"),
                     (24, 28, "NAME"), (29, 32, "NAME"), (33, 41, "NAME"), (42, 48, "NAME"), (48, 57, "COMMENT")]}),
    ("2 bags (12 oz. ea.) frozen cauliflower florets, cooked according to package directions", {
        "entities": [(0, 1, "COMMENT"), (2, 6, "COMMENT"), (8, 10, "QTY"), (11, 14, "UNIT"), (15, 18, "COMMENT"),
                     (20, 26, "PREP"), (27, 38, "NAME"), (39, 46, "NAME"), (48, 86, "PREP")]}),
    ("1/4 cup hot water", {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 11, "PREP"), (12, 17, "NAME")]}),
    # Duplicate
    ("About 2 cups shredded celery root, shredded using the grater attachment of a food processor or a mandoline", {
        "entities": [(0, 7, "QTY"), (8, 12, "UNIT"), (13, 21, "PREP"), (22, 28, "NAME"), (29, 33, "NAME"),
                     (35, 106, "PREP")]}),
    ("1/2 cup plus 1 tablespoon water",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 25, "COMMENT"), (26, 31, "NAME")]}),
    ("2 1/2 cups (about 11 ounces) allpurpose bleached flour", {
        "entities": [(0, 5, "QTY"), (6, 10, "UNIT"), (11, 28, "COMMENT"), (29, 39, "NAME"), (40, 48, "PREP"),
                     (49, 54, "NAME")]}),
    ("2 regular or English cucumbers", {"entities": [(0, 1, "QTY"), (2, 9, "NAME"), (10, 30, "ALT_NAME")]}),
    ("Two 15.5-ounce cans black-eyed peas, rinsed and drained", {
        "entities": [(0, 3, "QTY"), (15, 19, "UNIT"), (4, 14, "COMMENT"), (20, 25, "NAME"), (26, 30, "NAME"),
                     (31, 35, "NAME"), (37, 55, "PREP")]}),

    ("4 ounces loose sausage meat",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "PREP"), (15, 22, "NAME"), (23, 27, "NAME")]}),
    ("3 medium onions peeled, each cut into 6 wedges, root end intact",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 15, "NAME"), (16, 22, "PREP"), (24, 63, "PREP")]}),
    ("3 tablespoons, mustard seeds",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (15, 22, "NAME"), (23, 28, "NAME")]}),
    ("1/2 cup small dice celery",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "PREP"), (14, 18, "PREP"), (19, 25, "NAME")]}),

    ("24 ounces Fra Diavolo, recipe follows",
     {"entities": [(0, 2, "QTY"), (3, 9, "UNIT"), (10, 13, "NAME"), (14, 21, "NAME"), (23, 37, "COMMENT")]}),
    ("1 3/4 cup granola, organic preferred",
     {"entities": [(0, 5, "QTY"), (6, 9, "UNIT"), (10, 17, "NAME"), (19, 36, "COMMENT")]}),
    ("4 medium-large parsnips, halved lengthwise and cut on the bias into 2-inch lengths",
     {"entities": [(0, 1, "QTY"), (2, 14, "UNIT"), (15, 23, "NAME"), (25, 42, "PREP"), (43, 82, "PREP")]}),
    ("1 can (14.5 ounces) Del Monte® Cut Green Beans, drained", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 19, "COMMENT"), (20, 23, "NAME"), (24, 30, "NAME"),
                     (31, 34, "NAME"), (35, 40, "NAME"), (41, 46, "NAME"), (48, 55, "PREP")]}),
    ("½ cup diced red bell pepper or 1 jar (7 ounces) diced pimiento, drained", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 11, "PREP"), (12, 15, "NAME"), (16, 20, "NAME"),
                     (21, 27, "NAME"), (28, 71, "ALT_NAME")]}),
    ("1 pound parsnips, peeled and cut into 1-inch pieces",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 16, "NAME"), (18, 24, "PREP"), (25, 51, "PREP")]}),
    ("1/4 cup chive, chopped", {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "NAME"), (15, 22, "PREP")]}),
    ("About 3 1/2 ounces peanut putter crunch cereal (recommended: Captain Crunch)", {
        "entities": [(0, 5, "QTY"), (6, 11, "QTY"), (12, 18, "UNIT"), (19, 25, "NAME"), (26, 32, "NAME"),
                     (33, 39, "NAME"), (40, 46, "NAME"), (47, 76, "COMMENT")]}),
    ("1/2 pound Emmentaler or Swiss cheese, coarsely grated",
     {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 20, "NAME"), (21, 29, "ALT_NAME"), (30, 36, "NAME"),
                   (38, 53, "PREP")]}),
    ("Special equipment: 5-ounce paper cups",
     {"entities": [(0, 18, "COMMENT"), (19, 20, "QTY"), (21, 26, "UNIT"), (27, 32, "NAME"), (33, 37, "NAME")]}),
    # Equipment
    ("2 large Butterfinger bars, roughly chopped",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 20, "NAME"), (21, 25, "NAME"), (27, 42, "PREP")]}),
    ("2 pints vanilla ice cream",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 15, "NAME"), (16, 19, "NAME"), (20, 25, "NAME")]}),
    ("8 ounces dried bow ties",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "PREP"), (15, 18, "NAME"), (19, 23, "NAME")]}),
    ("1/4 cup canned or jarred artichoke hearts, chopped", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (15, 24, "ALT_NAME"), (25, 34, "NAME"),
                     (35, 41, "NAME"), (43, 50, "PREP")]}),
    ("1 pound firm bean curd, cut in 3/4-inch cubes, at room temperature", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 12, "PREP"), (13, 17, "NAME"), (18, 22, "NAME"),
                     (24, 45, "PREP"), (47, 66, "PREP")]}),
    ("1 tablespoon plus 1 1/2 teaspoons doubanjiang (spicy bean paste)",
     {"entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 33, "COMMENT"), (34, 45, "NAME"), (46, 64, "COMMENT")]}),
    ("2 heaping tablespoons rendered duck fat (can be purchased at most gourmet meat shops)", {
        "entities": [(0, 1, "QTY"), (2, 9, "PREP"), (10, 21, "UNIT"), (22, 30, "PREP"), (31, 35, "NAME"),
                     (36, 39, "NAME"), (40, 85, "COMMENT")]}),
    ("3/4 pound rhubarb, sliced (or use frozen, cut rhubarb, thawed)",
     {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 17, "NAME"), (19, 25, "PREP"), (26, 62, "COMMENT")]}),
    ("Half an 8-ounce package almond paste", {
        "entities": [(0, 4, "QTY"), (5, 7, "QTY"), (8, 15, "UNIT"), (16, 23, "UNIT"), (24, 30, "NAME"),
                     (31, 36, "NAME")]}),  # "Half an" QTY, "8-ounce" QTY, "package" UNIT
    ("14 ounces canned (or frozen, thawed) artichoke hearts, drained, diced (not marinated)", {
        "entities": [(0, 2, "QTY"), (3, 9, "UNIT"), (10, 16, "PREP"), (17, 36, "COMMENT"), (37, 46, "NAME"),
                     (47, 53, "NAME"), (55, 62, "PREP"), (64, 69, "PREP"), (70, 85, "COMMENT")]}),
    ("3/4 cup liquid of your choice, such as beef stock, chicken stock, water or wine (I'm using red wine)", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "COMMENT"), (15, 30, "COMMENT"), (31, 38, "COMMENT"),
                     (39, 43, "NAME"), (44, 49, "NAME"), (51, 64, "ALT_NAME"), (66, 71, "ALT_NAME"),
                     (72, 79, "ALT_NAME"), (80, 100, "COMMENT")]}),
    ("2 pounds ground meat of your choice, such as beef, pork, turkey, chicken, lamb (I'm using beef)", {
        "entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 15, "PREP"), (16, 20, "NAME"), (21, 36, "COMMENT"),
                     (37, 95, "COMMENT")]}),
    ("1 onion, diced (I'm using yellow onion)",
     {"entities": [(0, 1, "QTY"), (2, 7, "NAME"), (9, 14, "PREP"), (15, 39, "COMMENT")]}),
    ("3/4 pound cherries, pitted", {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 18, "NAME"), (20, 26, "PREP")]}),
    ("2 chocolate bars", {"entities": [(0, 1, "QTY"), (2, 11, "NAME"), (12, 16, "NAME")]}),
    ("2 (14 ounce) cans quartered artichoke hearts in water, drained", {
        "entities": [(0, 1, "QTY"), (13, 17, "UNIT"), (2, 12, "COMMENT"), (18, 27, "PREP"), (28, 37, "NAME"),
                     (38, 44, "NAME"), (45, 53, "PREP"), (55, 62, "PREP")]}),
    ("1 pound rhubarb, chopped into 1/2-inch pieces",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 15, "NAME"), (17, 45, "PREP")]}),
    ("1 ounce sugar, approximately 2 tablespoons, plus 1 cup sugar", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "NAME"), (15, 42, "COMMENT"), (44, 54, "COMMENT"),
                     (55, 60, "NAME")]}),

    ("8 ounces feta, cut into 1/2-inch cubes",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 13, "NAME"), (15, 38, "PREP")]}),
    ("12 large (U-8) dayboat scallops",
     {"entities": [(0, 2, "QTY"), (3, 8, "UNIT"), (9, 14, "COMMENT"), (15, 22, "NAME"), (23, 31, "NAME")]}),
    ("8 ounces floury or boiling potatoes, unpeeled and diced", {
        "entities": [
            (0, 1, "QTY"),  # "8"
            (2, 8, "UNIT"),  # "ounces"
            (9, 26, "PREP"),  # "floury" (describes potatoes)
            (27, 35, "NAME"),  # "potatoes" (The main ingredient)
            (37, 55, "PREP"),  # "unpeeled"
        ]
    }),
    ("1 cup dried cherries. optional",
     {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 11, "NAME"), (12, 20, "NAME"), (22, 30, "COMMENT")]}),
    ("4 tablespoons mirin, or white wine",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 19, "NAME"), (21, 34, "ALT_NAME")]}),
    ("2 pounds (2 pints) plain yogurt (regular or low-fat)", {
        "entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 18, "COMMENT"), (19, 24, "PREP"), (25, 31, "NAME"),
                     (32, 52, "COMMENT")]}),
    ("About 1/8 ounce curry powder",
     {"entities": [(0, 5, "QTY"), (6, 9, "QTY"), (10, 15, "UNIT"), (16, 21, "NAME"), (22, 28, "NAME")]}),
    ("1/2 pound littleneck or Manila clams",
     {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 20, "NAME"), (21, 36, "ALT_NAME")]}),
    ("1 pound Dungeness or lump crabmeat",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 17, "NAME"), (18, 34, "ALT_NAME")]}),
    ("1 small bok choy cut into 1/2-inch slices",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 11, "NAME"), (12, 16, "NAME"), (17, 41, "PREP")]}),
    ("1 (4 pound chicken) cut into 12 pieces", {
        "entities": [
            (0, 1, "COMMENT"),  # "1" (Refers to the item described in the parenthesis)
            # Entities from within "(4 pound chicken)"
            (3, 4, "QTY"),  # "4"
            (5, 10, "UNIT"),  # "pound"
            (11, 18, "NAME"),  # "chicken"
            # Rest of the instruction
            (20, 38, "PREP")  # "cut into 12 pieces" (Span "cut"(20,23) to "pieces"(32,38))
        ]
    }),
    ("2 cups thinly sliced white or cremini mushrooms", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 13, "PREP"), (14, 20, "PREP"), (21, 26, "NAME"),
                     (27, 47, "ALT_NAME")]}),
    ("1/2 cup homemade tomato sauce or good quality store bought sauce", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 16, "PREP"), (17, 23, "NAME"), (24, 29, "NAME"),
                     (30, 64, "ALT_NAME")]}),
    ("1 pound parsnips, peeled and chopped into even pieces",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 16, "NAME"), (18, 24, "PREP"), (25, 53, "PREP")]}),
    ("4 cups halved lengthwise and cut into strips nopales pieces", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 13, "PREP"), (14, 24, "PREP"), (25, 28, "PREP"),
                     (29, 32, "PREP"), (33, 44, "PREP"), (45, 52, "NAME"), (53, 59, "NAME")]}),
    ("30 cleaned king prawn", {"entities": [(0, 2, "QTY"), (3, 10, "PREP"), (11, 15, "NAME"), (16, 21, "NAME")]}),
    ("1 tablespoon gluten", {"entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 19, "NAME")]}),
    ("1/2 pound sea scallops, trimmed, or firm-fleshed fish, like halibut, cut into 1-inch cubes", {
        "entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 13, "NAME"), (14, 22, "NAME"), (24, 31, "PREP"),
                     (33, 54, "ALT_NAME"), (55, 68, "COMMENT"), (69, 90, "PREP")]}),
    ("2 (14-ounce) cans quartered artichoke hearts in water, drained", {
        "entities": [(0, 1, "QTY"), (13, 17, "UNIT"), (2, 12, "COMMENT"), (18, 27, "PREP"), (28, 37, "NAME"),
                     (38, 44, "NAME"), (45, 53, "PREP"), (55, 62, "PREP")]}),
    ("4 candy bars (recommended: Snickers, Milky Way,Zero, etc)",
     {"entities": [(0, 1, "QTY"), (2, 7, "NAME"), (8, 12, "NAME"), (13, 57, "COMMENT")]}),

    ("One 3.5-ounce package frozen açai (about 1/2 cup)", {
        "entities": [(0, 3, "QTY"), (14, 21, "UNIT"), (4, 13, "COMMENT"), (22, 28, "PREP"), (29, 33, "NAME"),
                     (34, 49, "COMMENT")]}),
    ("1 can (15.25 ounces) Del Monte® Whole Kernel Corn, drained", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 20, "COMMENT"), (21, 24, "NAME"), (25, 31, "NAME"),
                     (32, 37, "NAME"), (38, 44, "NAME"), (45, 49, "NAME"), (51, 58, "PREP")]}),
    ("1/4 cup mirin (see Cook's Note)",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "NAME"), (14, 31, "COMMENT")]}),
    ("Two 6-ounce cans tomato paste",
     {"entities": [(0, 3, "QTY"), (12, 16, "UNIT"), (4, 11, "COMMENT"), (17, 23, "NAME"), (24, 29, "NAME")]}),
    ("1 cup chopped toasted walnuts, for garnish", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 13, "PREP"), (14, 21, "PREP"), (22, 29, "NAME"),
                     (31, 42, "COMMENT")]}),
    ("1 pound bean sprouts", {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 12, "NAME"), (13, 20, "NAME")]}),
    ("1/2 pound good feta, cut into 1/2-inch cubes",
     {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 14, "PREP"), (15, 19, "NAME"), (21, 44, "PREP")]}),

    ("Assorted podis and chutneys, for serving",
     {"entities": [(0, 8, "PREP"), (9, 14, "NAME"), (15, 28, "ALT_NAME"), (29, 40, "COMMENT")]}),
    ("1 big pinch hing (asafoetida)",
     {"entities": [(0, 1, "QTY"), (2, 5, "COMMENT"), (6, 11, "COMMENT"), (12, 16, "NAME"), (17, 29, "COMMENT")]}),
    ("1 tablespoon sumakh, see note",
     {"entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 19, "NAME"), (21, 29, "COMMENT")]}),
    ("1 pound string beans, trimmed, or 1 pound asparagus, peeled and trimmed", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 14, "NAME"), (15, 20, "NAME"), (22, 29, "PREP"),
                     (31, 71, "ALT_NAME")]}),
    ("1-ounce good vinegar (sherry)",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 12, "PREP"), (13, 20, "NAME"), (21, 29, "COMMENT")]}),
    ("1 piloncillo cone (7 1/2 ounces), finely grated (see Cook's Note)", {
        "entities": [(0, 1, "QTY"), (2, 12, "NAME"), (13, 17, "NAME"), (19, 24, "QTY"),  # "7 1/2"
                     (25, 31, "UNIT"),  # "ounces"
                     (34, 47, "PREP"),  # "finely , (34, 47, "PREP"),
                     (48, 65, "COMMENT")]}),
    ("4 ounces pancetta, diced", {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 17, "NAME"), (19, 24, "PREP")]}),
    ("1/4 pound pancetta, thickly sliced (recommended: Golden Farms)",
     {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 18, "NAME"), (20, 34, "PREP"), (35, 62, "COMMENT")]}),
    ("1/4 pound mild semi-hard cheese (recommended: Old Kentucky Tomme)", {
        "entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 14, "PREP"), (15, 24, "PREP"), (25, 31, "NAME"),
                     (32, 65, "COMMENT")]}),
    ("3 quarts shrimp stock or water",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 15, "NAME"), (16, 21, "NAME"), (22, 30, "ALT_NAME")]}),
    ("4 tablespoons miso", {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 18, "NAME")]}),
    ("2 tablespoons shichimi", {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 22, "NAME")]}),
    ("3/4 cup veganaise (vegan mayonnaise)",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 17, "NAME"), (18, 36, "COMMENT")]}),
    ("12 slices sourdough bread, toasted",
     {"entities": [(0, 2, "QTY"), (3, 9, "COMMENT"), (10, 19, "NAME"), (20, 25, "NAME"), (27, 34, "PREP")]}),
    ("1 scoop collagen, optional",
     {"entities": [(0, 1, "QTY"), (2, 7, "COMMENT"), (8, 16, "NAME"), (18, 26, "COMMENT")]}),
    ("1/2 bacon, diced", {"entities": [(0, 3, "QTY"), (4, 9, "NAME"), (11, 16, "PREP")]}),
    ("1 pound pancetta, cut into 1-inch pieces",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 16, "NAME"), (18, 40, "PREP")]}),
    ("1 pound Cin Chili recipe follows,chilled", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 11, "NAME"), (12, 17, "NAME"), (18, 32, "COMMENT"),
                     (33, 40, "PREP")]}),  # comma before chilled makes it separate PREP
    ("1 (1 pound) package round dumpling wrappers (gyoza), 3 inches in diameter", {
        "entities": [(0, 1, "QTY"), (12, 19, "UNIT"), (2, 11, "COMMENT"), (20, 25, "PREP"), (26, 34, "NAME"),
                     (35, 43, "NAME"), (44, 51, "COMMENT"), (51, 73, "COMMENT")]}),
    ("1 pound weakfish, medium diced",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 16, "NAME"), (18, 24, "PREP"), (25, 30, "PREP")]}),
    ("1 gallon court bouillon", {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "NAME"), (15, 23, "NAME")]}),
    ("1 fruit roll tape", {"entities": [(0, 1, "QTY"), (2, 7, "NAME"), (8, 12, "NAME"), (13, 17, "NAME")]}),
    ("1 (8-ounce) packet amaretti morbidi (soft almond macaroons)", {
        "entities": [(0, 1, "QTY"), (12, 18, "UNIT"), (2, 11, "COMMENT"), (19, 27, "NAME"), (28, 35, "NAME"),
                     (36, 59, "COMMENT")]}),
    ("3/4 cup whole-wheat four", {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 19, "NAME"), (20, 24, "NAME")]}),
    ("3/4 Lb bulk chorizo", {"entities": [(0, 3, "QTY"), (4, 6, "UNIT"), (7, 11, "PREP"), (12, 19, "NAME")]}),
    ("1 T water", {"entities": [(0, 1, "QTY"), (2, 3, "COMMENT"), (4, 9, "NAME")]}),
    # "T" as COMMENT (not parsed as unit)
    ("1 melon, top removed and seeds scooped out (top reserved)",
     {"entities": [(0, 1, "QTY"), (2, 7, "NAME"), (9, 42, "PREP"), (43, 57, "COMMENT")]}),
    ("1 bottle of port wine", {"entities": [(0, 1, "QTY"), (2, 11, "COMMENT"), (12, 16, "NAME"), (17, 21, "NAME")]}),
    ("3/8 cup miso (soybean paste)",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 12, "NAME"), (13, 28, "COMMENT")]}),
    ("3/4 cup peppers (red, green and yellow), small dice", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "NAME"), (16, 39, "COMMENT"), (41, 46, "PREP"),
                     (47, 51, "PREP")]}),
    ("2 cups (about 4 1/2 ounces) ajicitos (sweet peppers), stemmed, halved and seeded", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 27, "COMMENT"), (28, 36, "NAME"), (37, 52, "COMMENT"),
                     (54, 61, "PREP"), (63, 69, "PREP"), (70, 73, "PREP"), (74, 80, "PREP")]}),
    ("1/4 cup achiote (annatto seeds)",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "NAME"), (16, 31, "COMMENT")]}),
    ("3 tablespoons mirin (Japanese rice wine)",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 19, "NAME"), (20, 40, "COMMENT")]}),  # Duplicate
    ("1 tablespoon hot bean paste or red chili paste", {
        "entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 16, "NAME"), (17, 21, "NAME"), (22, 27, "NAME"),
                     (28, 46, "ALT_NAME")]}),  # Duplicate
    ("Two 14-ounce packages round dumpling wrappers", {
        "entities": [(0, 3, "QTY"), (13, 21, "UNIT"), (4, 12, "COMMENT"), (22, 27, "PREP"), (28, 36, "NAME"),
                     (37, 45, "NAME")]}),
    ("40 dasima anchovies (large dried anchovies for soup or stock; about 3 ounces)",
     {"entities": [(0, 2, "QTY"), (3, 9, "NAME"), (10, 19, "NAME"), (20, 77, "COMMENT")]}),
    ("1/2 pound hamachi, cut into cubes",
     {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 17, "NAME"), (19, 33, "PREP")]}),
    ("1/2 small sourdough loaf, cut into six 1/2-inch-thick slices",
     {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 19, "NAME"), (20, 24, "NAME"), (26, 60, "PREP")]}),
    ("2 cups court bouillon, recipe follows",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 12, "NAME"), (13, 21, "NAME"), (23, 37, "COMMENT")]}),
    ("1/3 cup pepitos (pumpkin seeds)",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "NAME"), (16, 31, "COMMENT")]}),
    ("1/3 to 1/2 pound manchego, thinly sliced with sharp knife or cheese plane",
     {"entities": [(0, 3, "QTY"), (4, 10, "ALT_QTY"), (11, 16, "UNIT"), (17, 25, "NAME"), (27, 75, "PREP")]}),
    ("1 cup hot pickled vegetable salad of cauliflower, carrots, celery and hot peppers (giardiniera) drained,", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 9, "PREP"), (10, 17, "PREP"), (18, 27, "NAME"),
                     (28, 33, "NAME"), (34, 81, "PREP"), (82, 95, "COMMENT"), (96, 103, "PREP")]}),
    ("1 small loaf sourdough, torn into 1- to 2-inch chunks",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 12, "COMMENT"), (13, 22, "NAME"), (24, 53, "PREP")]}),
    ("1 to 2 canned chipotles, chopped, plus 2 tablespoons adobo sauce", {
        "entities": [(0, 1, "QTY"), (2, 6, "ALT_QTY"), (7, 13, "PREP"), (14, 23, "NAME"), (25, 32, "PREP"),
                     (34, 64, "COMMENT")]}),
    ("8 links knackwurst (white pork bratwurst) or weisswurst (white pork and veal sausage)",
     {"entities": [(0, 1, "QTY"), (2, 7, "COMMENT"), (8, 18, "NAME"), (19, 41, "COMMENT"), (42, 85, "ALT_NAME")]}),
    ("8 German-style brotchen rolls or hard-shell rolls (ciabatta is a great substitute!)", {
        "entities": [(0, 1, "QTY"), (2, 14, "PREP"), (15, 23, "NAME"), (24, 29, "NAME"), (30, 49, "ALT_NAME"),
                     (50, 83, "COMMENT")]}),
    ("1/4 cup four", {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 12, "NAME")]}),  # "four" assumed flour
    ("Two 540-gram cans 'ulu (or breadfruit), rinsed and large dice", {
        "entities": [(0, 3, "QTY"), (13, 17, "UNIT"), (4, 12, "COMMENT"), (18, 22, "NAME"), (23, 38, "COMMENT"),
                     (40, 61, "PREP")]}),
    ("1/2 pound pancetta, cut into 1/2-inch dice",
     {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 18, "NAME"), (20, 42, "PREP")]}),
    ("1 tablespoon (15 grams) mirin",
     {"entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 23, "COMMENT"), (24, 29, "NAME")]}),
    ("1/3 cup pignoli (pine nuts)",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "NAME"), (16, 27, "COMMENT")]}),
    ("One 14-ounce can jackfruit chunks, drained", {
        "entities": [(0, 3, "QTY"), (13, 16, "UNIT"), (4, 12, "COMMENT"), (17, 26, "NAME"), (27, 33, "NAME"),
                     (35, 42, "PREP")]}),
    ("1 cup (20 leaves) shredded or torn basil", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 17, "COMMENT"), (18, 34, "PREP"),
                     (35, 40, "NAME")]}),
    ("5 to 6 stems fresh sage, stripped", {
        "entities": [(0, 1, "QTY"), (2, 6, "ALT_QTY"), (7, 12, "COMMENT"), (13, 18, "PREP"), (19, 23, "NAME"),
                     (25, 33, "PREP")]}),
    ("1 1/2 teaspoons asafoetida", {"entities": [(0, 5, "QTY"), (6, 15, "UNIT"), (16, 26, "NAME")]}),
    ("1/2 teaspoon piment d’espelette (you can also try this with smoked or traditional paprika)",
     {"entities": [(0, 3, "QTY"), (4, 12, "UNIT"), (13, 19, "NAME"), (20, 31, "NAME"), (32, 90, "COMMENT")]}),
    ("1/2 stick (4 tablespoons) cold unsalted butter, plus 1 tablespoon, melted", {
        "entities": [
            (0, 9, "COMMENT"),  # "1/2 stick" (Descriptive quantity/form)
            # Parenthetical part:
            (11, 12, "QTY"),  # "4"
            (13, 24, "UNIT"),  # "tablespoons"
            # Rest of the ingredient
            (26, 30, "PREP"),  # "cold"
            (31, 39, "NAME"),  # "unsalted"
            (40, 46, "NAME"),  # "butter"
            (46, 66, "COMMENT"),  # ", plus 1 tablespoon," (Note: includes commas)
            (67, 73, "PREP")  # "melted" (Corrected end offset from 74 to 73 for "melted")
        ]
    }),
    ("1/4 cup sriracha mayonnaise or 1/4 cup mayonnaise mixed with 1/2 teaspoon sriracha sauce",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 16, "NAME"), (17, 27, "NAME"), (28, 88, "ALT_NAME")]}),

    ("1/4 cup katsuo (dried bonito flake)",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "NAME"), (15, 35, "COMMENT")]}),
    ("3/4 cup toasted walnuts, chopped",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "PREP"), (16, 23, "NAME"), (25, 32, "PREP")]}),
    ("2/3 cup cubed Brie, optional",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "PREP"), (14, 18, "NAME"), (20, 28, "COMMENT")]}),
    ("6 cups loosely packed mixed torn greens such as romaine, red or green leaf lettuce, or radicchio, washed and dried",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 14, "PREP"), (15, 21, "PREP"), (22, 27, "PREP"), (28, 32, "PREP"),
                   (33, 39, "NAME"), (40, 97, "COMMENT"), (98, 114, "PREP")]}),
    ("2 teaspoons finely chopped fresh Italian (flat-leaf parsley)", {
        "entities": [(0, 1, "QTY"), (2, 11, "UNIT"), (12, 18, "PREP"), (19, 26, "PREP"), (27, 32, "PREP"),
                     (33, 40, "NAME"), (41, 60, "COMMENT")]}),
    ("3/4 tablespoon whole dried ground ginger", {
        "entities": [(0, 3, "QTY"), (4, 14, "UNIT"), (15, 20, "PREP"), (21, 26, "PREP"), (27, 33, "NAME"),
                     (34, 40, "NAME")]}),
    ("1 cup Bob Evans Wildfire Barbecue Sauce", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 9, "NAME"), (10, 15, "NAME"), (16, 24, "NAME"),
                     (25, 33, "NAME"), (34, 39, "NAME")]}),
    ("1 lb. Bob Evans Zesty Hot Sausage Roll", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 9, "NAME"), (10, 15, "NAME"), (16, 21, "NAME"),
                     (22, 25, "NAME"), (26, 33, "NAME"), (34, 38, "NAME")]}),
    ("2 1/2 teaspoons powdered ginger",
     {"entities": [(0, 5, "QTY"), (6, 15, "UNIT"), (16, 24, "PREP"), (25, 31, "NAME")]}),
    ("1/4 bunch each, cilantro and parsley",
     {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 14, "UNIT"), (16, 24, "NAME"), (25, 36, "ALT_NAME")]}),
    ("4 cups thinly sliced clean leeks (white and green parts)", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 13, "PREP"), (14, 20, "PREP"), (21, 26, "PREP"),
                     (27, 32, "NAME"), (33, 56, "COMMENT")]}),
    ("12 ounces dried packed Pizzocheri (buckwheat short broad noodles)", {
        "entities": [(0, 2, "QTY"), (3, 9, "UNIT"), (10, 15, "PREP"), (16, 22, "PREP"), (23, 33, "NAME"),
                     (34, 65, "COMMENT")]}),
    ("2 cups aquafaba (chickpea water, from a 20-ounce can of chickpeas)",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 15, "NAME"), (16, 66, "COMMENT")]}),
    ("2 tablespoons chopped jarred jalapenos",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 21, "PREP"), (22, 28, "PREP"), (29, 38, "NAME")]}),
    ("5 1/2 pounds boned shoulder of lamb, trimmed of excess fat and cut into cubes about 1 1/2 by 2 1/2 inches", {
        "entities": [(0, 5, "QTY"), (6, 12, "UNIT"), (13, 18, "PREP"), (19, 27, "NAME"), (28, 30, "NAME"),
                     (31, 35, "NAME"), (37, 58, "PREP"), (59, 105, "PREP")]}),
    ("1 cup mixed soft fresh herbs such as parsley leaves, chives and dill", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 11, "PREP"), (12, 16, "PREP"), (17, 22, "PREP"),
                     (23, 28, "NAME"), (29, 68, "COMMENT")]}),
    ("Two 28-ounce cans whole peeled tomatoes, with juices (about 7 cups)", {
        "entities": [(0, 3, "QTY"), (13, 17, "UNIT"), (4, 12, "COMMENT"), (18, 23, "PREP"), (24, 30, "PREP"),
                     (31, 39, "NAME"), (41, 52, "PREP"), (53, 67, "COMMENT")]}),
    ("4 cups Tomato Sauce, recipe follows, or your favorite jarred", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 13, "NAME"), (14, 19, "NAME"), (21, 35, "COMMENT"),
                     (37, 60, "ALT_NAME")]}),
    ("1 pound mushrooms, domestic or wild, caps only thinly sliced", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 17, "NAME"), (19, 36, "COMMENT"), (37, 41, "PREP"),
                     (42, 46, "PREP"), (47, 53, "PREP"), (54, 60, "PREP")]}),
    ("1 pound ground turkey or chicken",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 14, "PREP"), (15, 21, "NAME"), (22, 32, "ALT_NAME")]}),
    ("Parmesan cheese-to serve on the side for grating",
     {"entities": [(0, 8, "NAME"), (9, 15, "NAME"), (15, 48, "COMMENT")]}),
    ("1 pound penne rigate, cooked al dente",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "NAME"), (14, 20, "NAME"), (22, 37, "PREP")]}),
    ("1/2 cup kasseri, grated", {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "NAME"), (17, 23, "PREP")]}),
    ("1 medium clove minced garlic",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "UNIT"), (15, 21, "PREP"), (22, 28, "NAME")]}),
    ("2 teaspoons adobo sauce (optional)",
     {"entities": [(0, 1, "QTY"), (2, 11, "UNIT"), (12, 17, "NAME"), (18, 23, "NAME"), (24, 34, "COMMENT")]}),
    ("4 pint-size mason jars, sterilized, procedure follows*", {
        "entities": [(0, 1, "QTY"), (2, 11, "PREP"), (12, 17, "NAME"), (18, 22, "NAME"), (24, 34, "PREP"),
                     (36, 54, "COMMENT")]}),
    ("1/4 cup chopped or torn fresh basil leaves", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 23, "PREP"), (24, 29, "PREP"),
                     (30, 35, "NAME"), (36, 42, "NAME")]}),

    ("1 bunch asparagus, cut into 1-inch pieces",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 17, "NAME"), (19, 41, "PREP")]}),
    ("1 tablespoon white pearl sugar",
     {"entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 18, "NAME"), (19, 24, "NAME"), (25, 30, "NAME")]}),
    ("2 cups fresh huckleberries or blueberries",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 12, "PREP"), (13, 26, "NAME"), (27, 41, "ALT_NAME")]}),
    ("3 ears corn, kernels removed", {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 11, "NAME"), (13, 28, "PREP")]}),
    ("1 cup pea pods, thinly sliced on an angle", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 9, "NAME"), (10, 14, "NAME"), (16, 22, "PREP"),
                     (23, 29, "PREP"), (30, 41, "PREP")]}),
    ("4 ears corn, in husk", {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 11, "NAME"), (13, 20, "PREP")]}),
    ("1/4 cup well-stirred tahini",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 20, "PREP"), (21, 27, "NAME")]}),
    ("2 tablespoons dried cloves, ground using a mortar and pestle",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 19, "PREP"), (20, 26, "NAME"), (28, 60, "PREP")]}),
    ("18 leaves each, red oak leaf lettuce, yellow chicory, and Belgian endive, washed", {
        "entities": [(0, 2, "QTY"), (3, 9, "COMMENT"), (10, 14, "UNIT"), (16, 19, "NAME"), (20, 23, "NAME"),
                     (24, 28, "NAME"), (29, 36, "NAME"), (38, 53, "ALT_NAME"), (54, 73, "ALT_NAME"),
                     (74, 80, "PREP")]}),
    ("1 pound linguisa Spanish sausage, blanched", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 16, "NAME"), (17, 24, "NAME"), (25, 32, "NAME"),
                     (34, 42, "PREP")]}),
    ("1/2 pound wild mushrooms (oyster, cremini, and shiitake) chopped", {
        "entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 14, "PREP"), (15, 24, "NAME"), (25, 56, "COMMENT"),
                     (57, 64, "PREP")]}),
    ("8 ears corn on the cob, silks removed, husks intact, soaked in water for 10 minutes", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 11, "NAME"), (12, 23, "PREP"), (24, 38, "PREP"),
                     (39, 52, "PREP"), (53, 83, "PREP")]}),
    ("1 bunch basil, bruised leaves removed",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "NAME"), (15, 37, "PREP")]}),
    ("1 pound asparagus, washed, tough ends removed",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 17, "NAME"), (19, 25, "PREP"), (27, 45, "PREP")]}),
    ("2 Tbsp. cilantro chopped", {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 16, "NAME"), (17, 24, "PREP")]}),
    ("3 Tbsp. Kikkoman Ponzu", {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 16, "NAME"), (17, 22, "NAME")]}),
    ("4 large eggs, separated", {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 12, "NAME"), (14, 23, "PREP")]}),
    ("1/2 pound each of 2 cheese selections such as: beer kaese, bruder basil, muenster", {
        "entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 14, "COMMENT"), (18, 37, "COMMENT"), (38, 46, "COMMENT"),
                     (47, 51, "NAME"), (52, 57, "NAME"), (59, 71, "ALT_NAME"), (73, 81, "ALT_NAME")]}),
    ("Sour pickles", {"entities": [(0, 4, "NAME"), (5, 12, "NAME")]}),
    ("1 bag Bavarian pretzels",
     {"entities": [(0, 1, "QTY"), (2, 5, "COMMENT"), (6, 14, "NAME"), (15, 23, "NAME")]}),
    # "bag" is COMMENT, "1" refers to bag
    ("2 cups asparagus, fresh or frozen, reserve some tips for garnish", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 16, "NAME"), (18, 34, "PREP"),
                     (35, 64, "COMMENT")]}),
    ("1 pint blackberries, halved lengthwise",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 19, "NAME"), (21, 38, "PREP")]}),
    ("1/4 pound pancetta, diced", {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 18, "NAME"), (20, 25, "PREP")]}),
    # Duplicate
    ("1/2 head of garlic", {"entities": [(0, 3, "QTY"), (4, 8, "UNIT"), (12, 18, "NAME")]}),
    ("2 carrots, peeled and cut into 1-centimeter (about 1/2-inch) rounds",
     {"entities": [(0, 1, "QTY"), (2, 9, "NAME"), (11, 17, "PREP"), (18, 21, "PREP"), (22, 67, "PREP")]}),
    ("1/4 red or yellow onion, diced",
     {"entities": [(0, 3, "QTY"), (4, 7, "NAME"), (8, 23, "ALT_NAME"), (25, 30, "PREP")]}),
    ("1 (16-ounce) bag frozen, fully cooked meatballs, defrosted and sliced 1/4-inch thick", {
        "entities": [(0, 1, "COMMENT"), (3, 5, "QTY"), (6, 11, "UNIT"), (13, 16, "COMMENT"), (17, 23, "PREP"),
                     (25, 30, "PREP"), (31, 37, "PREP"), (38, 47, "NAME"), (49, 58, "PREP"), (59, 62, "PREP"),
                     (63, 84, "PREP")]}),
    ("1/2 bag Townhouse Flip-Sides, pulverized", {
        "entities": [(0, 3, "QTY"), (4, 7, "COMMENT"), (8, 17, "NAME"), (18, 22, "NAME"), (23, 28, "NAME"),
                     (30, 40, "PREP")]}),  # "bag" as comment
    ("1 tablespoon Asian hot sauce, such as Sriracha", {
        "entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 18, "NAME"), (19, 22, "NAME"), (23, 28, "NAME"),
                     (30, 46, "COMMENT")]}),
    ("4 ears corn, kernels removed, cobs reserved",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 11, "NAME"), (13, 29, "PREP"), (30, 43, "PREP")]}),

    ("2 ounces grilled peach puree*", {
        "entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 16, "PREP"), (17, 22, "NAME"), (23, 28, "NAME"),
                     (28, 29, "COMMENT")]}),
    ("2 to 3 pounds chicken wing drumettes", {
        "entities": [(0, 1, "QTY"), (2, 6, "ALT_QTY"), (7, 13, "UNIT"), (14, 21, "NAME"), (22, 26, "NAME"),
                     (27, 36, "NAME")]}),
    ("2 ounces whipped cream, infused with brown sugar simple syrup",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 16, "PREP"), (17, 22, "NAME"), (24, 61, "PREP")]}),
    ("1 cup (160 g) red seedless grapes", {
        "entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 13, "COMMENT"), (14, 17, "PREP"), (18, 26, "PREP"),
                     (27, 33, "NAME")]}),
    ("1/2 pound asparagus, trimmed and cut into 1-2 inch pieces", {
        "entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 19, "NAME"), (21, 28, "PREP"), (29, 32, "PREP"),
                     (33, 57, "PREP")]}),
    ("11/2 pounds sirloin, sliced across the grain on the diagonal bias until very thin",
     {"entities": [(0, 4, "QTY"), (5, 11, "UNIT"), (12, 19, "NAME"), (21, 81, "PREP")]}),
    # Assuming 11/2 is a typo for 1 1/2
    ("1 bunch asparagus, blanched and refreshed",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 17, "NAME"), (19, 41, "PREP")]}),
    ("3 cups coarsely grated medium-sharp Cheddar", {
        "entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 15, "PREP"), (16, 22, "PREP"), (23, 29, "PREP"),
                     (30, 35, "PREP"), (36, 43, "NAME")]}),
    ("4 ounces sharp Cheddar, chopped into small pieces (or shredded)", {
        "entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "PREP"), (15, 22, "NAME"), (24, 49, "PREP"),
                     (50, 63, "COMMENT")]}),
    ("4 thick slices tomato, for serving",
     {"entities": [(0, 1, "QTY"), (2, 7, "PREP"), (8, 14, "PREP"), (15, 21, "NAME"), (23, 34, "COMMENT")]}),
    # Slices as UNIT,
    ("1 large or 2 small red onions, peeled and cut into 1/2-inch-thick rings", {
        "entities": [
            (0, 1, "QTY"),         # "1"
            (2, 7, "UNIT"),        # "large"
            (8,10,'ALT_NAME'),
            (11, 12, "ALT_QTY"),   # "2"
            (13, 18, "ALT_UNIT"),  # "small"
            (19, 22, "NAME"),      # "red"
            (23, 29, "NAME"),      # "onions"
            # Comma at 29 is O
            (31, 37, "PREP"),      # "peeled"
            # "and" (38,41) is O
            (42, 71, "PREP")       # "cut into 1/2-inch-thick rings"
        ]
    }),
    ("1/2 teaspoon ground star anise",
     {"entities": [(0, 3, "QTY"), (4, 12, "UNIT"), (13, 19, "PREP"), (20, 24, "NAME"), (25, 30, "NAME")]}),
    ("1 1/2 tablespoons CuraHao or other orange liqueur",
     {"entities": [(0, 5, "QTY"), (6, 17, "UNIT"), (18, 25, "NAME"), (26, 49, "ALT_NAME")]}),
    ("6 ounces calves liver, cubed",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 15, "NAME"), (16, 21, "NAME"), (23, 28, "PREP")]}),
    ("1/2 cup long grain rice",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 12, "PREP"), (13, 18, "PREP"), (19, 23, "NAME")]}),
    ("3/4 pound parsnips (about 2 medium)",
     {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 18, "NAME"), (19, 35, "COMMENT")]}),
    ("2 medium or 1 large onion, halved and thinly sliced", {
        "entities": [
            # Primary Item description
            (0, 1, "QTY"),         # "2"
            (2, 8, "UNIT"),        # "medium"
            (9,11,"ALT_NAME"),
            # Alternative description for the same item
            (12, 13, "ALT_QTY"),   # "1" (alternative quantity for onion)
            (14, 19, "ALT_UNIT"),  # "large" (alternative size unit for onion)
            # Core Item Name
            (20, 25, "NAME"),      # "onion"
            # Comma at 25 is O
            # Preparation
            (27, 33, "PREP"),      # "halved"
            # "and" (34,37) is O
            (38, 44, "PREP"),      # "thinly"
            (45, 51, "PREP")       # "sliced"
        ]
    }),
    ("1 cup plus 4 tablespoon for dredging and the gravy",
     {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 24, "COMMENT"), (25, 49, "COMMENT")]}),
    # "for dredging and the gravy" as comment
    ("1/2 bunch flatleaf parsley, leaves only, finely chopped", {
        "entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 18, "NAME"), (19, 26, "NAME"), (28, 39, "PREP"),
                     (41, 55, "PREP")]}),
    ("1 pint container of 1 1/2-inch casings",
     {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 16, "COMMENT"), (20, 30, "COMMENT"), (31, 38, "NAME")]}),
    # "container" as comment
    ("2 ounces organic sugar", {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 16, "PREP"), (17, 22, "NAME")]}),
    ("4 large parsnips, peeled (about 1 pound)",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 16, "NAME"), (18, 24, "PREP"), (25, 40, "COMMENT")]}),
    ("2 tablespoons sweetener of choice, such as honey, agave or maple syrup", {
        "entities": [
            (0, 1, "QTY"),           # "2"
            (2, 13, "UNIT"),         # "tablespoons"
            (14, 23, "COMMENT"),     # "sweetener" (The general category, now a comment)
            (24, 34, "COMMENT"),     # "of choice," (includes comma now as part of comment)
            (35, 42, "COMMENT"),     # "such as " (Introductory phrase)
            (43, 48, "NAME"),        # "honey" (First specific example)
            # Comma at 48 is O
            (50, 55, "ALT_NAME"),    # "agave"
            (56, 70, "ALT_NAME")     # "or maple syrup"
        ]
    }),
    ("3 tablespoons sweetener of choice, such as honey, agave or maple syrup", {
        "entities": [
            (0, 1, "QTY"),           # "2"
            (2, 13, "UNIT"),         # "tablespoons"
            (14, 23, "COMMENT"),     # "sweetener" (The general category, now a comment)
            (24, 34, "COMMENT"),     # "of choice," (includes comma now as part of comment)
            (35, 42, "COMMENT"),     # "such as " (Introductory phrase)
            (43, 48, "NAME"),        # "honey" (First specific example)
            # Comma at 48 is O
            (50, 55, "ALT_NAME"),    # "agave"
            (56, 70, "ALT_NAME")     # "or maple syrup"
        ]
    }),
    ("4 tablespoons sweetener of choice, such as honey, agave or maple syrup", {
        "entities": [
            (0, 1, "QTY"),           # "2"
            (2, 13, "UNIT"),         # "tablespoons"
            (14, 23, "COMMENT"),     # "sweetener" (The general category, now a comment)
            (24, 34, "COMMENT"),     # "of choice," (includes comma now as part of comment)
            (35, 42, "COMMENT"),     # "such as " (Introductory phrase)
            (43, 48, "NAME"),        # "honey" (First specific example)
            # Comma at 48 is O
            (50, 55, "ALT_NAME"),    # "agave"
            (56, 70, "ALT_NAME")     # "or maple syrup"
        ]
    }),
    ("1 tablespoons sweetener of choice, such as honey, agave or maple syrup", {
        "entities": [
            (0, 1, "QTY"),           # "2"
            (2, 13, "UNIT"),         # "tablespoons"
            (14, 23, "COMMENT"),     # "sweetener" (The general category, now a comment)
            (24, 34, "COMMENT"),     # "of choice," (includes comma now as part of comment)
            (35, 42, "COMMENT"),     # "such as " (Introductory phrase)
            (43, 48, "NAME"),        # "honey" (First specific example)
            # Comma at 48 is O
            (50, 55, "ALT_NAME"),    # "agave"
            (56, 70, "ALT_NAME")     # "or maple syrup"
        ]
    }),
    ("1 1/2 cups milk of choice, such as nut milk, low-fat cow’s milk or oat milk (see Cook’s Note)", {
        "entities": [
            (0, 5, "QTY"),           # "1 1/2"
            (6, 10, "UNIT"),         # "cups"
            (11, 15, "NAME"),     # "milk" (The general category)
            (16, 26, "COMMENT"),     # "of choice," (includes comma)
            (27, 34, "COMMENT"),     # "such as "
            (35, 43, "ALT_NAME"),        # "nut"
            # Comma at 43 is O
            (45, 63, "ALT_NAME"),    # "low-fat cow’s milk"
            (64, 75, "ALT_NAME"),    # "or oat milk"
            (76, 93, "COMMENT")      # "(see Cook’s Note)"
        ]
    }),
    ("1 pound of crab claw meat, picked over", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (11, 15, "NAME"), (16, 20, "NAME"), (21, 25, "NAME"),
                     (27, 38, "PREP")]}),
    ("2 pounds parsnips, peeled", {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 17, "NAME"), (19, 25, "PREP")]}),
    ("2 to 3 heads endive, chilled (about 24 leaves)", {
        "entities": [(0, 1, "QTY"), (2, 6, "ALT_QTY"), (7, 12, "UNIT"), (13, 19, "NAME"), (21, 28, "PREP"),
                     (29, 46, "COMMENT")]}),
    ("1 quart, plus 2 cups warm water",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (9, 20, "COMMENT"), (21, 25, "PREP"), (26, 31, "NAME")]}),
    ("1/8 cup patis (fish sauce)", {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "NAME"), (14, 26, "COMMENT")]}),
    ("1 large or 2 small yellow onions, sliced with the grain", {
        "entities": [
            (0, 1, "QTY"),         # "1"
            (2, 7, "UNIT"),        # "large"
            (8,10,'ALT_NAME'),
            (11, 12, "ALT_QTY"),   # "2"
            (13, 18, "ALT_UNIT"),  # "small"
            (19, 25, "NAME"),      # "yellow"
            (26, 32, "NAME"),      # "onions"
            # Comma at 32 is O
            (34, 40, "PREP"),      # "sliced"
            (41, 45, "PREP"),      # "with"
            (46, 49, "PREP"),      # "the"
            (50, 55, "PREP")       # "grain"
            # Or consolidate "sliced with the grain" to (34, 55, "PREP")
        ]
    }),
    ("2 tablespoons schmaltz or vegetable oil",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 22, "NAME"), (23, 39, "ALT_NAME")]}),
    ("1 1/2 pounds parsnips, peeled and quartered lengthwise", {
        "entities": [(0, 5, "QTY"), (6, 12, "UNIT"), (13, 21, "NAME"), (23, 29, "PREP"), (30, 33, "PREP"),
                     (34, 43, "PREP"), (44, 54, "PREP")]}),
    ("1 large or 2 small leeks, about 1 pound",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 18, "ALT_NAME"), (19, 24, "NAME"), (26, 39, "COMMENT")]}),
    ("1 1/2 lbs parsnips, peeled and trimmed", {
        "entities": [(0, 5, "QTY"), (6, 9, "UNIT"), (10, 18, "NAME"), (20, 26, "PREP"), (27, 30, "PREP"),
                     (31, 38, "PREP")]}),
    ("1/2 large head or 1 small head cauliflower, cut into florets", {
        "entities": [
            (0, 3, "QTY"),         # "1/2"
            (4, 9, "UNIT"),        # "large"
            (10, 14, "UNIT"),      # "head"
            # "or" (15,17) is O
            (15,17,'ALT_NAME'),
            (18, 19, "ALT_QTY"),   # "1"
            (20, 25, "ALT_UNIT"),  # "small"
            (26, 30, "ALT_UNIT"),  # "head" (This is an ALT_UNIT for the alternative specification)
            (31, 42, "NAME"),      # "cauliflower"
            # Comma at 42 is O
            (44, 47, "PREP"),      # "cut"
            (48, 52, "PREP"),      # "into"
            (53, 60, "PREP")       # "florets"
            # Or consolidate "cut into florets" to (44, 60, "PREP")
        ]
    }),
    ("1 cup pretzels, lightly crushed",
     {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 14, "NAME"), (16, 23, "PREP"), (24, 31, "PREP")]}),
    ("1 1/2 pounds parsnips, peeled",
     {"entities": [(0, 5, "QTY"), (6, 12, "UNIT"), (13, 21, "NAME"), (23, 29, "PREP")]}),  # Duplicate
    ("4 large radishes, washed and peeled", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 16, "NAME"), (18, 24, "PREP"), (25, 28, "PREP"),
                     (29, 35, "PREP")]}),
    ("1 packet Hidden Valley(R) Original Ranch(R) Seasoning Mix", {
        "entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 15, "NAME"), (16, 24, "NAME"), (26, 34, "NAME"),
                     (35, 42, "NAME"), (44, 53, "NAME"), (54, 57, "NAME")]}),  # packet as UNIT
    ("2 heads endive, sliced, for serving",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 14, "NAME"), (16, 22, "PREP"), (24, 35, "COMMENT")]}),
    ("1 pound parsnips, peeled and diced into 1-inch pieces", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 16, "NAME"), (18, 24, "PREP"), (25, 28, "PREP"),
                     (29, 34, "PREP"), (35, 53, "PREP")]}),
    ("2 cups oil for frying", {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 10, "NAME"), (11, 21, "COMMENT")]}),
    ("8 large stems and leaves of fresh epazote", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "COMMENT"), (14, 24, "PREP"), (25, 33, "PREP"),
                     (34, 41, "NAME")]}),
    ("A few leaves of basil, torn, plus a few to serve", {
        "entities": [(0, 1, "QTY"), (2, 5, "COMMENT"), (6, 12, "NAME"), (16, 21, "NAME"), (23, 27, "PREP"),
                     (29, 48, "COMMENT")]}),
    ("1/4 cup Pernod or white vermouth",
     {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "NAME"), (15, 23, "ALT_NAME"), (24, 32, "NAME")]}),
    ("2 tablespoons multicolored nonpareils",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 26, "PREP"), (27, 37, "NAME")]}),
    ("3/4 teaspoon anise seeds", {"entities": [(0, 3, "QTY"), (4, 12, "UNIT"), (13, 18, "NAME"), (19, 24, "NAME")]}),
    ("1 teaspoon Kentjoer (Indonesian ground spices)",
     {"entities": [(0, 1, "QTY"), (2, 10, "UNIT"), (11, 19, "NAME"), (20, 46, "COMMENT")]}),
    ("1/4 cup finely sliced white part only scallion", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (15, 21, "PREP"), (22, 27, "NAME"),
                     (28, 32, "NAME"), (33, 37, "PREP"), (38, 46, "NAME")]}),
    ("2 tablespoons schmaltz, at room temperature",
     {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 22, "NAME"), (24, 43, "PREP")]}),
    ("2 medium parsnips, unpeeled, poached for 15 minutes",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 17, "NAME"), (19, 27, "PREP"), (29, 51, "PREP")]}),
    ("6 ounces sparkling mineral water",
     {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 18, "PREP"), (19, 26, "NAME"), (27, 32, "NAME")]}),
    ("4 small parsnips, scrubbed and dried", {
        "entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 16, "NAME"), (18, 26, "PREP"), (27, 30, "PREP"),
                     (31, 36, "PREP")]}),
    ("2 heads endive, thinly sliced",
     {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 14, "NAME"), (16, 22, "PREP"), (23, 29, "PREP")]}),
    ("2 parsnips", {"entities": [(0, 1, "QTY"), (2, 10, "NAME")]}),
    ("4 standard po'boy rolls", {"entities": [(0, 1, "QTY"), (2, 10, "PREP"), (11, 17, "NAME"), (18, 23, "NAME")]}),
    ("Peanut or vegetable oil, for deep-frying",
     {"entities": [(0, 6, "NAME"), (7, 19, "ALT_NAME"), (20, 24, "NAME"), (25, 40, "COMMENT")]}),
    ("1 1/2 bottles beer, cold", {"entities": [(0, 5, "QTY"), (6, 13, "COMMENT"), (14, 18, "NAME"), (20, 24, "PREP")]}),
    ("1 (3-ounce) package commercial pectin",
     {"entities": [(0, 1, "QTY"), (12, 19, "UNIT"), (2, 11, "COMMENT"), (20, 30, "PREP"), (31, 37, "NAME")]}),
    # package as UNIT
    ("1 1/2 pounds parsnips, peeled and cubed into 1/2-inch pieces", {
        "entities": [(0, 5, "QTY"), (6, 12, "UNIT"), (13, 21, "NAME"), (23, 29, "PREP"), (34, 39, "PREP"),
                     (40, 60, "PREP")]}),
    ("2 medium or 1 large onion, finely chopped", {
        "entities": [(0, 1, "QTY"), (2, 8, "UNIT"),             (9,11,'ALT_NAME'),
                     # Alternative description for the same item
                     (12, 13, "ALT_QTY"),   # "1" (alternative quantity for onion)
                     (14, 19, "ALT_UNIT"),  # "large" (alternative size unit for onion),
                     (21, 26, "NAME"), (28, 34, "PREP"),
                     (35, 42, "PREP")]}),
    ("24 ounces dduk (about 4 cups)",
     {"entities": [(0, 2, "QTY"), (3, 9, "UNIT"), (10, 14, "NAME"), (15, 29, "COMMENT")]}),
    ("3 heads endive, trimmed", {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 14, "NAME"), (16, 23, "PREP")]}),
    ("1 potato, cut into chunks", {"entities": [(0, 1, "QTY"), (2, 8, "NAME"), (10, 25, "PREP")]}),
    ("One 8-ounce package or about 20 to 24 shishito peppers",
     {"entities": [(0, 3, "QTY"), (12, 19, "UNIT"), (4, 11, "COMMENT"), (20, 54, "ALT_NAME")]}),  # package as UNIT
    ("1 1/4 to 1 1/2 pounds flat iron steak, flank steak or thin-cut sirloin steak", {
        "entities": [(0, 5, "QTY"), (6, 14, "ALT_QTY"),(15, 21, "UNIT"), (22, 26, "NAME"), (27, 31, "NAME"), (32, 37, "NAME"),
                     (39, 50, "ALT_NAME"), (51, 76, "ALT_NAME")]}),
    ("1 tablespoon soy sauce or low-sodium soy sauce",
     {"entities": [(0, 1, "QTY"), (2, 12, "UNIT"), (13, 16, "NAME"), (17, 22, "NAME"), (23, 46, "ALT_NAME")]}),
    ("4 to 5 tablespoons peanut oil or other neutral oil", {
        "entities": [(0, 1, "QTY"), (2, 6, "ALT_QTY"), (7, 18, "UNIT"), (19, 25, "NAME"), (26, 29, "NAME"),
                     (30, 50, "ALT_NAME")]}),
    ("1 teaspoon, several drops, Worcestershire sauce",
     {"entities": [(0, 1, "QTY"), (2, 10, "UNIT"), (12, 26, "COMMENT"), (27, 41, "NAME"), (42, 47, "NAME")]}),
    ("1/2 cup grated Parmigiano-Reggiano, a couple of handfuls, plus some to pass at table", {
        "entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "NAME"), (15, 34, "NAME"), (36, 57, "COMMENT"),
                     (58, 84, "COMMENT")]}),

        ("6 rolls, for serving", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "NAME"),
            (9, 20, "COMMENT")
        ]}),
        ("2 rounded tablespoons finely cut or snipped parsley", {"entities": [
            (0, 1, "QTY"),
            (2, 9, "COMMENT"),
            (10, 21, "UNIT"),
            (22, 43, "PREP"),
            (44, 51, "NAME")
        ]}),
        ("1 pint natural organic yogurt", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),
            (7, 14, "PREP"),
            (15, 22, "PREP"),
            (23, 29, "NAME")
        ]}),
        ("3 tablespoons liquid smoke", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 26, "NAME")
        ]}),
        ("1 1/2 tablespoons liquid smoke", {"entities": [
            (0, 5, "QTY"),
            (6, 17, "UNIT"),
            (18, 30, "NAME")
        ]}),
        ("1 1/2 cups sour cream", {"entities": [
            (0, 5, "QTY"),
            (6, 10, "UNIT"),
            (11, 21, "NAME")
        ]}),
        ("2 onions chopped, about 1 1/2 cups", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "NAME"),
            (9, 16, "PREP"),
            (18, 34, "COMMENT")
        ]}),

        ("12 to 16 ounces sliced aged or sharp provolone", {"entities": [
            (0, 2, "QTY"),
            (3, 8, "ALT_QTY"),
            (9, 15, "UNIT"),
            (16, 22, "PREP"),
            (23, 27, "PREP"),
            (28, 30, "COMMENT"),
            (31, 36, "NAME"),
            (37, 46, "NAME")
        ]}),
        ("1/2 cup or the last bits of mayonnaise", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 27, "COMMENT"),
            (28, 38, "NAME")
        ]}),
        ("3 ounces dried bonito flakes", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 14, "PREP"),
            (15, 21, "NAME"),
            (22, 28, "NAME")
        ]}),
        ("4 cups shredded and green cabbage", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),
            (7, 15, "PREP"),
            (16, 19, "COMMENT"),
            (20, 25, "NAME"),
            (26, 33, "NAME")
        ]}),
        ("2 live lobsters 1 1/2 pounds each", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "PREP"),
            (7, 15, "NAME"),
            (16, 33, "COMMENT")
        ]}),
        ("1 pound cod", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),
            (8, 11, "NAME")
        ]}),
        ("1 cup (vegetable) stock, heated", {"entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 17, "COMMENT"),
            (18, 23, "NAME"),
            (25, 31, "PREP")
        ]}),
        ("3/4 pound percatelli", {"entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),
            (10, 20, "NAME")
        ]}),
        ("1 1/2 cups dried bonito flakes", {"entities": [
            (0, 5, "QTY"),
            (6, 10, "UNIT"),
            (11, 16, "PREP"),
            (17, 23, "NAME"),
            (24, 30, "NAME")
        ]}),
        ("1 pineapple- diced", {"entities": [
            (0, 1, "QTY"),
            (2, 12, "NAME"),
            (13, 18, "PREP")
        ]}),

        ("1 cup fresh or if unavailable, frozen cranberries, coarsely chopped (if using frozen, chop berries while still frozen)", {"entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 11, "PREP"),
            (12, 29, "COMMENT"),
            (31, 49, "NAME"),
            (51, 67, "PREP"),
            (69, 117, "COMMENT")
        ]}),
        ("32 littleneck clams on the half shell", {"entities": [
            (0, 2, "QTY"),
            (3, 13, "NAME"),
            (14, 19, "NAME"),
            (20, 37, "PREP")
        ]}),
        ("1 pound squid, cleaned and sliced", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),
            (8, 13, "NAME"),
            (15, 33, "PREP")
        ]}),

        ("1/4 cup currants", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 16, "NAME")
        ]}),
    ("3 cups all-purpose or bread flour, plus additional for rolling", {"entities": [ (0, 1, "QTY"), (2, 6, "UNIT"), (7, 18, "NAME"), (19, 27, "ALT_NAME"), (28, 33, "NAME"), (35, 62, "COMMENT") ]}),
    ("2 tablespoons plus 1 teaspoon Chef Paul Prudhomme's Meat Magic", {"entities": [ (0, 1, "QTY"), (2, 13, "UNIT"), (14, 29, "COMMENT"), (30, 62, "NAME") ]}),
        ("2/3 cup M&M's", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 13, "NAME")
        ]}),

    ("9 ounces (MSG free) fish balls", {"entities": [ (0, 1, "QTY"), (2, 8, "UNIT"), (10, 19, "COMMENT"), (20, 30, "NAME") ]}),
            ("1 cup plus 4 tablespoon for dredging and the gravy", {"entities": [
                (0, 1, "QTY"),
                (2, 5, "UNIT"),
                (6, 27, "COMMENT"),
                (28, 49, "COMMENT")
            ]}),
            ("3 tablespoons plus a drizzle Portuguese olive oil", {"entities": [
                (0, 1, "QTY"),
                (2, 13, "UNIT"),
                (14, 28, "COMMENT"),
                (29, 49, "NAME")
            ]}),
    ("1 (1 lb.) package frozen, mixed vegetables thawed", {"entities": [ (0, 1, "QTY"), (3, 8, "COMMENT"), (10, 17, "UNIT"), (18, 24, "PREP"), (26, 31, "PREP"), (32, 42, "NAME"), (43, 49, "PREP") ]}),

                ("12 pecan halves", {"entities": [
                    (0, 2, "QTY"),
                    (3, 8, "NAME"),
                    (9, 15, "COMMENT")
                ]}),            ("1 package store bought brownie mix, any brand, batter prepared to package directions", {"entities": [
                (0, 1, "QTY"),
                (2, 9, "UNIT"),
                (10, 22, "PREP"),
                (23, 34, "NAME"),
                (36, 45, "COMMENT"),
                (47, 84, "COMMENT")
            ]}),

            ("1 measure of Pimm's", {"entities": [
                (0, 1, "QTY"),
                (2, 9, "UNIT"),
                (13, 19, "NAME")
            ]}),
            ("1/2 cup pickled or roasted peppers, drained and chopped", {"entities": [
                (0, 3, "QTY"),
                (4, 7, "UNIT"),
                (8, 26, "PREP"),
                (27, 34, "NAME"),
                (36, 43, "PREP"),
                (44, 47, "COMMENT"),
                (48, 55, "PREP")
            ]}),
            ("3 tablespoons store-bought pesto", {"entities": [
                (0, 1, "QTY"),
                (2, 13, "UNIT"),
                (14, 26, "PREP"),
                (27, 32, "NAME")
            ]}),
            ("2 pounds crab meat", {"entities": [
                (0, 1, "QTY"),
                (2, 8, "UNIT"),
                (9, 13, "NAME"),
                (14, 18, "NAME")
            ]}),
            ("A handful of fresh herb leaves, such as basil, parsley and rosemary", {"entities": [
                (0, 9, "COMMENT"),
                (13, 18, "PREP"),
                (19, 23, "NAME"),
                (24, 30, "NAME"),
                (32, 39, "COMMENT"),
                (40, 45, "ALT_NAME"),
                (47, 54, "ALT_NAME"),
                (55, 67, "ALT_NAME")
            ]}),
    ("7 cups all-purpose or cake flour", {"entities": [ (0, 1, "QTY"), (2, 6, "UNIT"), (7, 18, "NAME"), (22, 26, "ALT_NAME"), (27, 32, "NAME") ]}),
    ("1/4 cup plus 2 tablespoons pure maple syrup", {"entities": [ (0, 3, "QTY"), (4, 7, "UNIT"), (8, 26, "COMMENT"), (27, 31, "NAME"), (32, 43, "NAME") ]}),
            ("2 parsnips cut into chunks", {"entities": [
                (0, 1, "QTY"),
                (2, 10, "NAME"),
                (11, 26, "PREP")
            ]}),

    ("3 tablespoons (45 grams) pure maple syrup", {"entities": [ (0, 1, "QTY"), (2, 13, "UNIT"), (14, 24, "COMMENT"), (25, 41, "NAME") ]}),
            ("3/4 cup all-purpose or chickpea flour", {"entities": [
                (0, 3, "QTY"),
                (4, 7, "UNIT"),
                (8, 19, "NAME"),
                (20, 31, "ALT_NAME"),
                (32, 37, "NAME")
            ]}),
    ("3 tablespoons cold pure maple syrup", {"entities": [ (0, 1, "QTY"), (2, 13, "UNIT"), (14, 18, "PREP"), (19, 35, "NAME") ]}),
            ("1/2 cup non-fat yogurt", {"entities": [
                (0, 3, "QTY"),
                (4, 7, "UNIT"),
                (8, 15, "PREP"),
                (16, 22, "NAME")
            ]}),
    ("4 cups leftover, turkey stuffing, dressing, moistened with leftover gravy or giblet broth - divided", {"entities": [ (0, 1, "QTY"), (2, 6, "UNIT"), (7, 15, "PREP"), (17, 32, "NAME"), (34, 42, "ALT_NAME"), (44, 89, "PREP"), (92, 99, "COMMENT") ]}),
    ("2 cups trimmed and sliced in coins broccoli stems", {"entities": [ (0, 1, "QTY"), (2, 6, "UNIT"), (7, 14, "PREP"), (15, 34, "PREP"), (35, 49, "NAME") ]}),
    ("1/3 ounce young or fresh ginger, peeled and diced", {"entities": [ (0, 3, "QTY"), (4, 9, "UNIT"), (10, 15, "PREP"), (19, 24, "PREP"), (25, 31, "NAME"), (33, 49, "PREP") ]}),
    ("Two 15-ounce cans sliced peaches in syrup", {"entities": [ (0, 3, "QTY"), (4, 12, "COMMENT"), (13, 17, "UNIT"), (18, 24, "PREP"), (25, 32, "NAME"), (33, 41, "PREP") ]}),
    ("2 quarts of your favorite turkey gravy", {"entities": [ (0, 1, "QTY"), (2, 8, "UNIT"), (9, 25, "COMMENT"), (26, 38, "NAME") ]}),

    ("1 tsp. balsamic reduction*", {"entities": [ (0, 1, "QTY"), (2, 6, "UNIT"), (7, 25, "NAME"), (25, 26, "COMMENT") ]}),
    ("5 ounces shredded 5-cheese blend (whole milk and skim milk mozzarella, Parmesan, Romano, provolone)", {"entities": [ (0, 1, "QTY"), (2, 8, "UNIT"), (9, 17, "PREP"), (18, 32, "NAME"), (34, 99, "COMMENT") ]}),
            ("1/4 cup shoyu (soy sauce), more or less", {"entities": [
                (0, 3, "QTY"),
                (4, 7, "UNIT"),
                (8, 13, "NAME"),
                (15, 39, "COMMENT")
            ]}),
            ("8 (#10) tin cans, lined with newspaper", {"entities": [
                (0, 1, "QTY"),
                (3, 7, "COMMENT"),
                (8, 11, "NAME"),
                (12, 16, "NAME"),
                (18, 38, "PREP")
            ]}),

    ("1 quart or more of liquid such as beer, or broth", {"entities": [ (0, 1, "QTY"), (2, 7, "UNIT"), (8, 25, "COMMENT"), (26, 33, "COMMENT"), (34, 38, "NAME"), (43, 48, "ALT_NAME") ]}),
            ("2 cups fresh or quick frozen cranberries", {"entities": [
                (0, 1, "QTY"),
                (2, 6, "UNIT"),
                (7, 12, "PREP"),
                (13, 28, "PREP"),
                (29, 40, "NAME")
            ]}),
            ("4 cups shoyu, yamasa", {"entities": [
                (0, 1, "QTY"),
                (2, 6, "UNIT"),
                (7, 12, "NAME"),
                (14, 20, "ALT_NAME")
            ]}),
            ("12 ounces pale ale", {"entities": [
                (0, 2, "QTY"),
                (3, 9, "UNIT"),
                (10, 18, "NAME")
            ]}),

            ("1/2 cup sour cream", {"entities": [
                (0, 3, "QTY"),
                (4, 7, "UNIT"),
                (8, 18, "NAME")
            ]}),
            ("8 ounces sour cream", {"entities": [
                (0, 1, "QTY"),
                (2, 8, "UNIT"),
                (9, 19, "NAME")
            ]}),
            ("3/4 cup sour cream", {"entities": [
                (0, 3, "QTY"),
                (4, 7, "UNIT"),
                (8, 18, "NAME")
            ]}),
            ("1 (16 ounce) container sour cream", {"entities": [
                (0, 1, "QTY"),
                (3, 11, "COMMENT"),
                (13, 22, "UNIT"),
                (23, 33, "NAME")
            ]}),
            ("One 16-ounce container sour cream", {"entities": [
                (0, 3, "QTY"),
                (4, 12, "COMMENT"),
                (13, 22, "UNIT"),
                (23, 33, "NAME")
            ]}),

    ("2 medium beets, trimmed and scrubbed", {"entities": [ (0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "NAME"), (16, 36, "PREP") ]}),
    ("1/2 cup plus 2 tablespoons cognac or brandy", {"entities": [ (0, 3, "QTY"), (4, 7, "UNIT"), (8, 26, "COMMENT"), (27, 33, "NAME"), (34, 43, "ALT_NAME") ]}),
    ("1/2 cup plus 2 tablespoons sriracha sauce, such as Huy Fong", {"entities": [ (0, 3, "QTY"), (4, 7, "UNIT"), (8, 26, "COMMENT"), (27, 35, "NAME"), (36, 41, "NAME"), (43, 59, "COMMENT") ]}),
    ("2 tablespoons fat reserved from the confit", {"entities": [ (0, 1, "QTY"), (2, 13, "UNIT"), (14, 17, "NAME"), (18, 42, "PREP") ]}),
    ("2 tablespoons of your favorite liqueur", {"entities": [ (0, 1, "QTY"), (2, 13, "UNIT"), (14, 30, "COMMENT"), (31, 38, "NAME") ]}),
            ("2 tablespoons cotija, finely grated, plus more at the end", {"entities": [
                (0, 1, "QTY"),
                (2, 13, "UNIT"),
                (14, 20, "NAME"),
                (22, 35, "PREP"),
                (37, 57, "COMMENT")
            ]}),
            ("4 large, not overripe bananas", {"entities": [
                (0, 1, "QTY"),
                (2, 7, "UNIT"),
                (9, 21, "PREP"),
                (22, 29, "NAME")
            ]}),

    ("1 small jar, 6 to 8 ounces, marinated mushrooms, drained", {"entities": [
        (0, 1, "QTY"),
        (2, 11, "UNIT"),
        (13, 26, "COMMENT"),
        (28, 47, "NAME"),
        (49, 56, "PREP")
    ]}),
        ("2 tablespoons low sodium soy sauce", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 24, "PREP"),
            (25, 34, "NAME")
        ]}),
    ("4 ounces frisee, washed and torn into pieces", {"entities": [
        (0, 1, "QTY"),
        (2, 8, "UNIT"),
        (9, 15, "NAME"),
        (17, 44, "PREP")
    ]}),
    ("1 pound very fresh, firm, white-fleshed fish", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 39, "PREP"),
        (40, 44, "NAME")
    ]}),
    ("1/2 cup dried currants", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (8, 13, "NAME"),
        (14, 22, "NAME")
    ]}),
        ("1/2 cup currants", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 16, "NAME")
        ]}),
    ("4 tablespoons Teriyaki with Wasabi and Ginger Sauce (recommended: Hoboken Eddie's Hukilau Hanna Sauce)", {"entities": [
        (0, 1, "QTY"),
        (2, 13, "UNIT"),
        (14, 51, "NAME"),
        (52, 101, "COMMENT")
    ]}),
    ("1 pound emmanthal, cubed", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 17, "NAME"),
        (19, 24, "PREP")
    ]}),
        ("5 large hamburger buns", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),
            (8, 22, "NAME")
        ]}),
    ("1/2 cup (125 milliliters) Any Herb Pesto, recipe follows", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (8, 25, "COMMENT"),
        (26, 40, "NAME"),
        (42, 56, "COMMENT")
    ]}),
        ("1 cup mayo", {"entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 10, "NAME")
        ]}),
        ("1/2 ounce B and B liqueur", {"entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),
            (10, 25, "NAME")
        ]}),
    ("1 cup cooked grain, like barley, brown rice or farro, or cooked root vegetable", {"entities": [
        (0, 1, "QTY"),
        (2, 5, "UNIT"),
        (6, 12, "PREP"),
        (13, 18, "NAME"),
        (20, 52, "ALT_NAME"),
        (54, 78, "ALT_NAME")
    ]}),
    ("2 tablespoons dried currants", {"entities": [
        (0, 1, "QTY"),
        (2, 13, "UNIT"),
        (14, 19, "NAME"),
        (20, 28, "NAME")
    ]}),

        ("1/2 cup fresh or frozen, thawed, corn", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 31, "PREP"),
            (33, 37, "NAME")
        ]}),
        ("6 ounces firm tofu, cut into 1/4-inch cubes", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 13, "PREP"),
            (14, 18, "NAME"),
            (20, 43, "PREP")
        ]}),
        ("3/4 pound, 3 links, hot or sweet Italian sausage, split and meat removed from casing", {"entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),
            (11, 18, "PREP"),
            (20, 32, "PREP"),
            (33, 48, "NAME"),
            (50, 83, "PREP")
        ]}),
        ("1/2 cup, dried scallops, soaked in hot water until soft", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (9, 14, "PREP"),
            (15, 23, "NAME"),
            (25, 55, "PREP")
        ]}),
        ("12 scallops", {"entities": [
            (0, 2, "QTY"),
            (3, 11, "NAME") # 'scallops' itself acts as the unit for countable items.
        ]}),
        ("10 1/2 ounces/300 g fried tofu, finely sliced", {"entities": [
            (0, 6, "QTY"),
            (7, 17, "UNIT"),
            (18, 19, "COMMENT"),
            (20, 25, "PREP"),
            (26, 30, "NAME"),
            (32, 45, "PREP")
        ]}),
        ("1/4 cup thinly sliced-on-the-bias celery", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 33, "PREP"),
            (34, 40, "NAME")
        ]}),

        ("2 tablespoons hot fudge sauce", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 29, "NAME")
        ]}),
    ("4 portions, 6 to 8 ounces each, mahi mahi fillets", {"entities": [
        (0, 1, "QTY"),
        (2, 10, "COMMENT"), # Reverted: 'portions' is a COMMENT, not a UNIT.
        (12, 30, "COMMENT"), # Corrected span for '6 to 8 ounces each'
        (32, 49, "NAME")     # Corrected span for 'mahi mahi fillets'
    ]}),
    ("2 tablespoons finely chopped, peeled fresh galanga or ginger", {"entities": [
        (0, 1, "QTY"),
        (2, 13, "UNIT"),
        (14, 28, "PREP"),   # Corrected: 'finely chopped'
        (30, 36, "PREP"),   # Corrected: 'peeled'
        (37, 42, "PREP"),   # Corrected: 'fresh'
        (43, 50, "NAME"),   # Corrected: 'galanga'
        (51, 60, "ALT_NAME") # Corrected: 'ginger' (with 'or' as 'O' between NAME and ALT_NAME)
    ]}),
    ("6 to 8 cups peeled and sliced fruit, like apples, pears, and strawberries", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "ALT_QTY"),
        (7, 11, "UNIT"),
        (12, 29, "PREP"),   # Corrected: 'peeled and sliced'
        (30, 35, "NAME"),   # Corrected: 'fruit'
        (37, 73, "COMMENT") # Corrected: 'like apples, pears, and strawberries'
    ]}),
    ("1/2 cup drained and sliced sundried tomatoes in oil", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (8, 26, "PREP"),    # Corrected: 'drained and sliced'
        (27, 44, "NAME"),    # Corrected: 'sundried tomatoes'
        (45, 51, "COMMENT")  # Corrected: 'in oil'
    ]}),
    ("1/8 teaspoon cloves, ground", {"entities": [
        (0, 3, "QTY"),
        (4, 12, "UNIT"),
        (13, 19, "NAME"),    # Corrected: 'cloves' (comma is separate)
        (21, 27, "PREP")
    ]}),
        ("1 snapper head", {"entities": [
            (0, 1, "QTY"),
            (2, 9, "NAME"),
            (10, 14, "UNIT") # 'head' is a countable unit for items like lettuce, fish heads.
        ]}),
        ("1 1/3 cups plus 1 tablespoon mayonnaise", {"entities": [
            (0, 5, "QTY"),
            (6, 10, "UNIT"),
            (11, 28, "COMMENT"), # "plus 1 tablespoon" is a comment on the quantity/unit
            (29, 39, "NAME")
        ]}),
    ("1 small disk washed-rind cheese, such as Camembert", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),   # Corrected: 'small' is a UNIT
        (8, 31, "NAME"),   # Corrected: 'disk washed-rind cheese' (combines disk, rind, cheese)
        (33, 50, "COMMENT") # Corrected: 'such as Camembert'
    ]}),
        ("8 medium or 12 small beets", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"), # "medium" describes the preparation/state of the item
            (12, 14, "ALT_QTY"),
            (15, 20, "ALT_UNIT"), # "small" describes the preparation/state of the item
            (21, 26, "NAME")
        ]}),
        ("1/3 pound minced clams, drained", {"entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),
            (10, 16, "PREP"),
            (17, 22, "NAME"),
            (24, 31, "PREP")
        ]}),

    ("1 cup liquid (water, broth, wine or a combo) for deglazing", {"entities": [
        (0, 1, "QTY"),
        (2, 5, "UNIT"),
        (6, 12, "NAME"),
        (14, 43, "COMMENT"), # Correct: '(water, broth, wine or a combo)' (span 13-42 is accurate)
        (45, 58, "COMMENT")  # Correct: 'for deglazing' (was 43-56 and started with ')', should be 45-56)
    ]}),
        ("1 celery stalk, finely diced", {"entities": [
            (0, 1, "QTY"),
            (2, 14, "NAME"), # 'stalk' is not in the allowed units list, so it's part of the NAME
            (16, 28, "PREP")
        ]}),

        ("4 sticks (1 pound butter) minus 1 heaping tablespoon, cut into chips and softened", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "COMMENT"), # 'sticks' is not in allowed units, so it's a descriptive comment
            (10, 11, "QTY"),     # Corrected: '1' for butter
            (12, 17, "UNIT"),    # Corrected: 'pound' as unit for butter
            (18, 24, "NAME"),    # Corrected: 'butter' as name
            (26, 31, "COMMENT"), # 'minus' as a directive/comment
            (32, 33, "QTY"),     # '1' for tablespoon
            (34, 41, "PREP"),    # 'heaping' as prep for tablespoon
            (42, 52, "UNIT"),    # 'tablespoon' as unit
            (54, 82, "PREP")     # 'cut into chips and softened'
        ]}),

    ("2 tablespoons sweetener of choice, such as honey, agave or maple syrup, plus more if desired", {"entities": [
        (0, 1, "QTY"),
        (2, 13, "UNIT"),
        (14, 42, "COMMENT"),   # "sweetener of choice"
        (43, 49, "NAME"),      # "honey"
        (50, 55, "ALT_NAME"),  # "agave"
        (56, 70, "ALT_NAME"),  # "maple syrup" (treating "or" as an 'O' token)
        (72, 92, "COMMENT")    # "plus more if desired"
    ]}),
        ("1 2-liter bottle ginger ale, well chilled", {"entities": [
            (0, 1, "QTY"),
            (2, 16, "COMMENT"), # '2-liter bottle' describes the form, 'bottle' is not an allowed unit
            (17, 27, "NAME"),
            (29, 41, "PREP")
        ]}),
    ("2 pounds oxtails, excess fat trimmed (substitute with chuck or short ribs)", {"entities": [
        (0, 1, "QTY"),
        (2, 8, "UNIT"),
        (9, 16, "NAME"),    # Corrected: 'oxtails' (removed comma)
        (18, 36, "PREP"),    # Corrected: 'excess fat trimmed' (removed opening parenthesis)
        (37, 74, "COMMENT")  # Corrected: '(substitute with chuck or short ribs)' (included both parentheses)
    ]}),
        ("1/2 to 3/4 cup sour cream", {"entities": [
            (0, 3, "QTY"),
            (4, 10, "ALT_QTY"),
            (11, 14, "UNIT"),
            (15, 25, "NAME")
        ]}),
    ("1/8 pound, 3 slices, pancetta, chopped", {"entities": [
        (0, 3, "QTY"),
        (4, 9, "UNIT"),
        (11, 19, "COMMENT"), # Corrected: '3 slices' (removed trailing comma)
        (21, 29, "NAME"),    # Corrected: 'pancetta' (removed trailing comma)
        (31, 38, "PREP")     # Corrected: 'chopped'
    ]}),
        ("1 celery stalk, sliced", {"entities": [
            (0, 1, "QTY"),
            (2, 14, "NAME"), # 'stalk' is not in the allowed units list, so it's part of the NAME
            (16, 22, "PREP")
        ]}),
    ("4 cups loosely packed arugula, washed and dried", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),
        (7, 21, "PREP"),
        (22, 29, "NAME"),
        (31, 47, "PREP")     # Corrected: 'washed and dried'
    ]}),

    ("1 shallot minced", {"entities": [
        (0, 1, "QTY"),
        (2, 9, "NAME"),      # Corrected: 'shallot'
        (10, 16, "PREP")     # Corrected: 'minced'
    ]}),
    ("2 cups cold allnatural fruit juice or juice blend", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),
        (7, 11, "PREP"),
        (12, 22, "PREP"),
        (23, 34, "NAME"),
        (35, 49, "ALT_NAME")  # Corrected: 'or juice blend'
    ]}),
    ("10 ounces bottled or filtered water", {"entities": [
        (0, 2, "QTY"),
        (3, 9, "UNIT"),
        (10, 17, "PREP"),
        (18, 29, "PREP"),     # Corrected: 'or filtered'
        (30, 35, "NAME")      # Corrected: 'water'
    ]}),
    ("1 package (21 ounces) fudge brownie mix", {"entities": [
        (0, 1, "QTY"),
        (2, 9, "UNIT"),
        (10, 21, "COMMENT"),  # Corrected: '(21 ounces)'
        (22, 39, "NAME")      # Corrected: 'fudge brownie mix'
    ]}),
        ("3 pounds flanken (short ribs)", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 16, "NAME"),
            (17, 29, "ALT_NAME") # '(short ribs)' as alt name
        ]}),
    ("6 cups lightly packed arugula, leafy hydroponic - if available", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),
        (7, 21, "PREP"),     # Corrected: 'lightly packed'
        (22, 29, "NAME"),     # Corrected: 'arugula'
        (31, 62, "COMMENT")   # Corrected: 'leafy hydroponic - if available'
    ]}),
    ("2 large bunches washed and stemmed arugula", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 15, "COMMENT"),  # 'bunches' as COMMENT, as per previous discussion
        (16, 34, "PREP"),     # Corrected: 'washed and stemmed'
        (35, 42, "NAME")      # Corrected: 'arugula'
    ]}),
    ("1/2 cup packed micro-parsley", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (8, 14, "PREP"),
        (15, 28, "NAME")      # Corrected: 'micro-parsley'
    ]}),
        ("1 tsp garlic, minced", {"entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 12, "NAME"),
            (14, 20, "PREP")
        ]}),
        ("1 pound fresh or frozen cavatelli", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),
            (8, 13, "PREP"),    # 'fresh'
            (14, 23, "PREP"),    # 'or frozen'
            (24, 33, "NAME")
        ]}),

        ("1/2 cup, packed, brown sugar", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (9, 15, "PREP"),     # 'packed'
            (17, 28, "NAME")      # 'brown sugar'
        ]}),
        ("2 bananas", {"entities": [
            (0, 1, "QTY"),
            (2, 9, "NAME")        # 'bananas' itself is the item, no unit from list.
        ]}),
        ("3 bananas", {"entities": [
            (0, 1, "QTY"),
            (2, 9, "NAME")
        ]}),
        ("2 pita pockets, halved", {"entities": [
            (0, 1, "QTY"),
            (2, 14, "NAME"),      # 'pita pockets' is the item name, not an allowed unit.
            (16, 22, "PREP")
        ]}),
        ("3/4 ounce pickle juice", {"entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),
            (10, 22, "NAME")
        ]}),
        ("1/4 cup toffee bits", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 19, "NAME")
        ]}),
        ("1/2- ounce pickle slices", {"entities": [
            (0, 4, "QTY"),         # '1/2-'
            (5, 10, "UNIT"),       # 'ounce'
            (11, 24, "NAME")       # 'pickle slices'
        ]}),
        ("8 large pita rounds, cut into strips", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # 'large' is an allowed UNIT.
            (8, 19, "NAME"),
            (21, 36, "PREP")
        ]}),
        ("3 pita pockets, each cut into 8 wedges", {"entities": [
            (0, 1, "QTY"),
            (2, 14, "NAME"),
            (16, 38, "PREP")      # 'each cut into 8 wedges' as a preparation instruction.
        ]}),

        ("1 teaspoon dried thyme", {"entities": [
            (0, 1, "QTY"),
            (2, 10, "UNIT"),
            (11, 16, "NAME"),
            (17, 22, "NAME")
        ]}),
        ("6 ounces (168 grams) fresh or frozen rhubarb, thick sliced (about 1 1/2 cups)", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (10, 19, "COMMENT"),
            (21, 36, "PREP"),
            (37, 44, "NAME"),
            (46, 58, "PREP"),
            (60, 76, "COMMENT")
        ]}),
        ("1 1/2 teaspoons dried thyme", {"entities": [
            (0, 5, "QTY"),
            (6, 15, "UNIT"),
            (16, 21, "NAME"),
            (22, 27, "NAME")
        ]}),
        ("12 ounces ripe, but not mushy peaches (about 2 peaches)", {"entities": [
            (0, 2, "QTY"),
            (3, 9, "UNIT"),
            (10, 29, "PREP"),
            (30, 37, "NAME"),
            (39, 54, "COMMENT")
        ]}),
        ("2 cups onions, diced", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),
            (7, 13, "NAME"),
            (15, 20, "PREP")
        ]}),
        ("1/2 teaspoon dried thyme", {"entities": [
            (0, 3, "QTY"),
            (4, 12, "UNIT"),
            (13, 18, "NAME"),
            (19, 24, "NAME")
        ]}),
        ("2 ounces mezcal, optional", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 15, "NAME"),
            (17, 25, "COMMENT")
        ]}),

        ("One 8-ounce package or about 20 to 24 shishito peppers", {"entities": [
            (0, 3, "QTY"),
            (4, 11, "COMMENT"),  # "8-ounce" describes the package size/weight
            (12, 19, "UNIT"),     # "package" is an allowed UNIT
            (20, 37, "COMMENT"),  # "or about 20 to 24" as a descriptive comment
            (38, 54, "NAME")
        ]}),
        ("6 ounces reshteh or linguine (see Cook\u2019s Note)", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 16, "NAME"),
            (17, 28, "ALT_NAME"),
            (30, 45, "COMMENT")
        ]}),
        ("1 can (14 to 14-1/2-ounce) reduced-sodium or regular beef broth", {"entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),       # "can" is an allowed UNIT
            (6, 26, "COMMENT"),    # "(14 to 14-1/2-ounce)" as descriptive comment
            (27, 52, "PREP"),
            (53, 63, "NAME")
        ]}),
        ("12 grissini (thin breadsticks)", {"entities": [
            (0, 2, "QTY"),
            (3, 11, "NAME"),      # "grissini" is the item name, not an allowed unit
            (13, 29, "COMMENT")
        ]}),
    ("Two 14-ounce cans of pinto or black beans, with liquid", {"entities": [
        (0, 3, "QTY"),
        (4, 12, "COMMENT"),   # "14-ounce" describes the cans
        (13, 17, "UNIT"),      # "cans" is an allowed UNIT
        (21, 26, "NAME"),      # Corrected: "pinto" as NAME
        (27, 35, "ALT_NAME"),  # Corrected: "black beans" as ALT_NAME ("or" is not included)
        (36, 41, "NAME"),  # Corrected: "black beans" as ALT_NAME ("or" is not included)
        (43, 54, "PREP")
    ]}),
        ("1 1/2 cups glaze of your choosing (recipes follow)", {"entities": [
            (0, 5, "QTY"),
            (6, 10, "UNIT"),
            (11, 16, "NAME"),
            (17, 33, "COMMENT"),
            (34, 50, "COMMENT")
        ]}),
        ("3 tablespoons finely chopped fresh", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 28, "PREP"),
            (29, 34, "PREP")      # "fresh" as a preparation status
        ]}),
        ("2 chiles such as red finger, Fresno or jalapeno, seeded and chopped", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "NAME"),      # "chiles" is the item name, not an allowed unit
            (9, 16, "COMMENT"),    # "such as"
            (17, 27, "ALT_NAME"),
            (29, 35, "ALT_NAME"),
            (36, 47, "ALT_NAME"),
            (49, 67, "PREP")
        ]}),
        ("3 parsley sprigs", {"entities": [
            (0, 1, "QTY"),
            (2, 9, "NAME"),
            (10, 16, "COMMENT")   # "sprigs" is not an allowed unit, treat as descriptive comment
        ]}),
        ("1 pound celeriac peeled and cut into 2-inch pieces", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),
            (8, 16, "NAME"),
            (17, 50, "PREP")
        ]}),

        ("2 bags Earl Grey tea", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "COMMENT"),   # "bags" is a descriptive comment, not an allowed unit
            (7, 20, "NAME")
        ]}),
        ("About 2 tablespoons Mixed Spices*", {"entities": [
            (0, 5, "COMMENT"),   # "About" is a descriptive comment
            (6, 7, "QTY"),
            (8, 19, "UNIT"),
            (20, 32, "NAME"),
        ]}),
        ("2 yolks", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "NAME")       # "yolks" is the item name, no unit from the allowed list
        ]}),
        ("2 ounces whiskey of choice", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 16, "NAME"),
            (17, 26, "COMMENT")  # "of choice" as a descriptive comment
        ]}),
        ("2 gallons fresh or sea water", {"entities": [
            (0, 1, "QTY"),
            (2, 9, "UNIT"),
            (10, 15, "PREP"),
            (16, 22, "PREP"),     # "or sea"
            (23, 28, "NAME")
        ]}),
        ("1/3 cup toasted, chopped, blanched hazelnuts", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 15, "PREP"),
            (17, 24, "PREP"),
            (26, 34, "PREP"),
            (35, 44, "NAME")
        ]}),
        ("8 ounces firm, solid low-moisture mozzarella, finely grated", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 33, "PREP"),
            (34, 44, "NAME"),
            (46, 59, "PREP")      # "finely grated"
        ]}),
    ("1 pound shishito peppers", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 24, "NAME")
    ]}),
    ("1 tablespoon (1 turn around the pan) vegetable, olive, or corn oil", {"entities": [
        (0, 1, "QTY"),
        (2, 12, "UNIT"),     # "tablespoon"
        (14, 35, "COMMENT"),  # "(1 turn around the pan)"
        (37, 46, "ALT_NAME"), # Corrected: "vegetable" (from 'v' to 'e')
        (48, 53, "NAME"),     # Corrected: "olive" (from 'o' to 'e')
        (58, 62, "ALT_NAME"), # Corrected: "corn" (from 'c' to 'n')
        (63, 66, "NAME")      # Corrected: "oil" (from 'o' to 'l')
    ]}),
    ("3 leeks, washed and sliced", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "NAME"),
        (9, 26, "PREP")      # Corrected: "washed and sliced" (from 'w' to 'd')
    ]}),
    ("2 tablespoons (2 turns around the pan) olive or vegetable oil", {"entities": [
        (0, 1, "QTY"),
        (2, 13, "UNIT"),     # Correct: "tablespoons"
        (14, 37, "COMMENT"),  # Corrected: "(2 turns around the pan)" (from '(' to ')')
        (39, 44, "NAME"),     # Corrected: "olive" (from 'o' to 'e')
        (48, 57, "ALT_NAME"), # Corrected: "vegetable" (from 'v' to 'e', "or" is implicitly outside)
        (58, 61, "NAME")      # Corrected: "oil" (from 'o' to 'l')
    ]}), ("3 leeks (white part only), thinly sliced", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "NAME"),
        (9, 24, "COMMENT"),  # Correct: "(white part only)"
        (27, 40, "PREP")     # Corrected: "thinly sliced" (from 't' to 'd')
    ]}),
    ("1/4 cup mojo", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (8, 12, "NAME")
    ]}),
    ("6 tablespoons browning", {"entities": [
        (0, 1, "QTY"),
        (2, 13, "UNIT"),
        (14, 22, "NAME")
    ]}),
    ("2 cans (14 to 14-1/2-ounce) reduced-sodium or regular beef broth", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),
        (7, 27, "COMMENT"),   # Corrected: "(14 to 14-1/2-ounce)" (includes both parentheses)
        (28, 53, "PREP"),     # Corrected: "reduced-sodium" (from 'r' to 'm')
        (54, 64, "NAME")      # Corrected: "beef broth" (from 'b' to 'h')
    ]}),
    ("1 pound sausage, cooked and cut into 1/2 inch pieces", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 15, "NAME"),
        (17, 52, "PREP")      # Corrected: "cooked and cut into 1/2 inch pieces" (from 'c' to 's')
    ]}),
    ("1 pound soy “meat”", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 18, "NAME")      # Corrected: "soy “meat”" (precisely covers from 's' to closing '”')
    ]}),

    ("1/2 head frisee, torn", {"entities": [
        (0, 3, "QTY"),
        (4, 8, "UNIT"),     # "head" is an allowed UNIT
        (9, 15, "NAME"),
        (17, 21, "PREP")
    ]}),
    ("1/2 teaspoon double-acting baking powder", {"entities": [
        (0, 3, "QTY"),
        (4, 12, "UNIT"),
        (13, 26, "PREP"),     # Corrected: "double-acting" (from 'd' at 13 to 'g' at 25 + 1 = 26)
        (27, 40, "NAME")      # Corrected: "baking powder" (from 'b' at 27 to 'r' at 39 + 1 = 40)
    ]}),
    ("2 cups low sodium soy sauce", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),
        (7, 17, "PREP"),     # "low sodium"
        (18, 27, "NAME")
    ]}),
    ("1/2 cup small dice of mixed yellow, green and red bell pepper, for garnish", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (8, 17, "PREP"),     # "small dice"
        (21, 57, "NAME"),     # "mixed yellow, green and red bell pepper"
        (59, 70, "COMMENT")   # "for garnish"
    ]}),
    ("2 1/2 pounds organic or grass-fed beef (80/20)", {"entities": [
        (0, 5, "QTY"),
        (6, 12, "UNIT"),
        (13, 20, "PREP"),
        (21, 33, "PREP"),     # Corrected: "or grass-fed" (from 'o' at 21 to 'd' at 32 + 1 = 33)
        (34, 38, "NAME"),     # Corrected: "beef" (from 'b' at 34 to 'f' at 37 + 1 = 38)
        (39, 45, "COMMENT")   # Corrected: "(80/20)" (from '(' at 39 to ')' at 44 + 1 = 45)
    ]}),
    ("3 cups (about 8 ounces) frisee, washed and dried", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),
        (7, 22, "COMMENT"), # (about 8 ounces) - This span is correct as per error output's tokenization.
        (24, 30, "NAME"),
        (32, 48, "PREP")     # Corrected: "washed and dried" (from 'w' at 32 to 'd' at 47 + 1 = 48)
    ]}),
    ("1 tablespoon non-hydrogenated vegan margarine, melted (recommended: Earth Balance)", {"entities": [
        (0, 1, "QTY"),
        (2, 12, "UNIT"),
        (13, 29, "PREP"),
        (30, 35, "PREP"),
        (36, 45, "NAME"),
        (47, 53, "PREP"),     # Corrected: "melted" (from 'm' at 47 to 'd' at 52 + 1 = 53)
        (54, 81, "COMMENT")   # Correct: "(recommended: Earth Balance)" (from '(' at 54 to ')' at 80 + 1 = 81)
    ]}),
    ("1 large Gala or other baking apple, peeled, cored, and finely chopped (about 1 cup)", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),      # "large"
        (8, 12, "NAME"),     # "Gala"
        (13, 28, "ALT_NAME"), # Corrected: "or other baking apple" (from 'o' at 13 to 'e' at 33 + 1 = 34)
        (29, 34, "ALT_NAME"), # Corrected: "or other baking apple" (from 'o' at 13 to 'e' at 33 + 1 = 34)
        (36, 69, "PREP"),     # Corrected: "peeled, cored, and finely chopped" (from 'p' at 36 to 'd' at 68 + 1 = 69)
        (70, 83, "COMMENT")  # Corrected: "(about 1 cup)" (from '(' at 70 to ')' at 82 + 1 = 83)
    ]}),
    ("1 large apricot, pitted, quartered and thinly sliced", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),      # "large" is an allowed UNIT
        (8, 15, "NAME"),
        (17, 52, "PREP")
    ]}),
    ("1 teaspoon MSG, optional", {"entities": [
        (0, 1, "QTY"),
        (2, 10, "UNIT"),
        (11, 14, "NAME"),
        (16, 24, "COMMENT")
    ]}),

    ("1 package pappadums, quartered (flavored with garlic, if possible)", {"entities": [
        (0, 1, "QTY"),
        (2, 9, "UNIT"),
        (10, 19, "NAME"),
        (21, 30, "PREP"),     # Corrected: "quartered" (from 'q' at 21 to 'd' at 29 + 1 = 30)
        (31, 66, "COMMENT")   # Corrected: "(flavored with garlic, if possible)" (from '(' at 31 to ')' at 65 + 1 = 66)
    ]}),
        ("3 mirlitons (chayote), cooked, peeled, and diced", {"entities": [
            (0, 1, "QTY"),
            (2, 11, "NAME"),
            (12, 21, "ALT_NAME"),
            (23, 43, "PREP")
        ]}),
    ("5 teaspoons gluten (available at health food stores and specialty grocery stores)", {"entities": [
        (0, 1, "QTY"),
        (2, 11, "UNIT"),
        (12, 18, "NAME"),
        (19, 81, "COMMENT")  # Corrected: "(available at health food stores and specialty grocery stores)" (from '(' at 19 to ')' at 80 + 1 = 81)
    ]}),

    ("1 package, 2 ounces, nut topping, available on baking aisle", {"entities": [
        (0, 1, "QTY"),
        (2, 9, "UNIT"),
        (11, 19, "COMMENT"),   # ", 2 ounces," (span 9-20 is accurate as shown in error output)
        (21, 32, "NAME"),     # Corrected: "nut topping" (from 'n' at 21 to 'g' at 31 + 1 = 32)
        (34, 59, "COMMENT")   # Corrected: "available on baking aisle" (from 'a' at 34 to 'e' at 59 + 1 = 60)
    ]}),
    ("4 pounds center cut cod, on the bone, but cut off 1-inch of the belly to make the saddle stand sturdily", {"entities": [
        (0, 1, "QTY"),
        (2, 8, "UNIT"),
        (9, 23, "NAME"),
        (25, 103, "COMMENT") # Corrected: "on the bone...sturdily" (from 'o' at 25 to 'y' at 102 + 1 = 103)
    ]}),
        ("1/2 cup small dice of mixed yellow, green and red bell pepper, for garnish", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 20, "PREP"),
            (21, 57, "NAME"),
            (59, 70, "COMMENT")
        ]}),
        ("2 tablespoons taj\u00edn, plus more for serving", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 19, "NAME"),
            (21, 42, "COMMENT")
        ]}),
    ("10 ounces mixed domestic and wild mushrooms, sliced or cut into bite-sized pieces (about 4 cups)", {"entities": [
        (0, 2, "QTY"),
        (3, 9, "UNIT"),
        (10, 43, "NAME"),     # Corrected: "mixed domestic and wild mushrooms" (from 'm' at 10 to 's' at 41 + 1 = 42)
        (45, 81, "PREP"),     # Corrected: ", sliced or cut into bite-sized pieces" (from ',' at 43 to 's' at 80 + 1 = 81)
        (82, 95, "COMMENT")   # Corrected: "(about 4 cups)" (from '(' at 82 to ')' at 95 + 1 = 96)
    ]}),
    ("1/3 cup koseret (dried woodsy flavored herb, dried oregano can be substituted)", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (8, 15, "NAME"),
        (16, 78, "COMMENT")  # Corrected: Span from '(' at 16 to ')' at 77 (so, 77+1=78)
    ]}),
        ("1/2 medium plantain, peeled and julienned", {"entities": [
            (0, 3, "QTY"),
            (4, 10, "UNIT"),
            (11, 19, "NAME"),
            (21, 41, "PREP")
        ]}),
        ("1 cup of your favorite ketchup", {"entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 22, "COMMENT"),
            (23, 30, "NAME")
        ]}),
        ("One 8-ounce package or about 20 to 24 shishito peppers", {"entities": [
            (0, 3, "QTY"),
            (4, 11, "COMMENT"),
            (12, 19, "UNIT"),
            (20, 37, "COMMENT"),
            (38, 54, "NAME")
        ]}),
    ("1/2 cup (1 stick butter), melted", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (9, 10, "QTY"),      # "1"
        (11, 16, "COMMENT"),  # "stick"
        (17, 23, "NAME"),     # "butter"
        (26, 32, "PREP")      # Corrected: "melted" (from 'm' at 26 to 'd' at 31 + 1 = 32)
    ]}),
        ("1 teaspoon cardamom pods", {"entities": [
            (0, 1, "QTY"),
            (2, 10, "UNIT"),
            (11, 24, "NAME")
        ]}),
    ("1 can (20 oz.) DOLE® Pineapple Slices", {"entities": [
        (0, 1, "QTY"),
        (2, 5, "UNIT"),
        (6, 14, "COMMENT"),   # Corrected: "(20 oz.)" (from '(' at 6 to ')' at 13 + 1 = 14)
        (15, 37, "NAME")      # Corrected: "DOLE® Pineapple Slices" (from 'D' at 15 to 's' at 37 + 1 = 38)
    ]}),
        ("12 ounces good ale (recommended: Bass)", {"entities": [
            (0, 2, "QTY"),
            (3, 9, "UNIT"),
            (10, 14, "PREP"),
            (15, 18, "NAME"),
            (19, 37, "COMMENT")
        ]}),
        ("1 1/2 cups no-sugar-added ketchup", {"entities": [
            (0, 5, "QTY"),
            (6, 10, "UNIT"),
            (11, 25, "PREP"),
            (26, 33, "NAME")
        ]}),
        ("1 package 3 or 4-inch wooden party picks", {"entities": [
            (0, 1, "QTY"),
            (2, 9, "UNIT"),
            (10, 21, "COMMENT"),
            (22, 28, "PREP"),
            (29, 40, "NAME")
        ]}),
    ("1/4 cup plus more, if necessary, lemon juice", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (8, 32, "COMMENT"),  # Fix: 'plus more, if necessary,'
        (33, 44, "NAME")      # Fix: 'lemon juice'
    ]}),
    ("1 1/2 cups peeled and finely grated sweet potato", {"entities": [
        (0, 5, "QTY"),
        (6, 10, "UNIT"),
        (11, 32, "PREP"),
        (33, 47, "NAME")
    ]}),
    ("4 sticks (1 pound butter) minus 1 heaping tablespoon, cut into chips and softened", {"entities": [
        (0, 1, "COMMENT"),
        (2, 8, "COMMENT"),
        (10, 11, "QTY"),
        (12, 17, "UNIT"),
        (18, 24, "NAME"),
        (26, 52, "COMMENT"),
        (54, 80, "PREP")
    ]}),
    ("One 8- to 9-ounce package of your favorite refrigerated tortellini", {"entities": [
        (0, 3, "QTY"),
        (4, 17, "COMMENT"),
        (18, 25, "UNIT"),
        (26, 42, "COMMENT"),
        (43, 55, "PREP"),
        (56, 66, "NAME")
    ]}),
    ("3 tablespoons chopped mixed green and red peppers", {"entities": [
        (0, 1, "QTY"),
        (2, 13, "UNIT"),
        (14, 21, "PREP"),
        (22, 49, "NAME")
    ]}),
    ("4 large crusty, seeded rolls, split", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 15, "PREP"),
        (16, 22, "PREP"),  # Fix: 'seeded'
        (23, 28, "NAME"),   # Fix: 'rolls'
        (30, 35, "PREP")    # Fix: 'split'
    ]}),
    ("4 ounces shishito peppers", {"entities": [
        (0, 1, "QTY"),
        (2, 8, "UNIT"),
        (9, 25, "NAME")
    ]}),
    ("1 panettone (about 2 pounds), cut into 1-inch-thick slices", {"entities": [
        (0, 1, "QTY"),
        (2, 11, "NAME"),
        (13, 28, "COMMENT"),
        (30, 58, "PREP")
    ]}),
    ("2 flatbreads", {"entities": [
        (0, 1, "QTY"),
        (2, 12, "NAME")
    ]}),
    ("1 cup oatmeal", {"entities": [
        (0, 1, "QTY"),
        (2, 5, "UNIT"),
        (6, 13, "NAME")
    ]}),
    ("4 cone cups", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "NAME"),
        (7, 11, "UNIT")
    ]}),
    ("4 large sprigs of chervil", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 14, "COMMENT"),
        (18, 25, "NAME")
    ]}),
    ("4 tablespoons, butter, divided", {"entities": [
        (0, 1, "QTY"),
        (2, 13, "UNIT"),
        (15, 21, "NAME"),
        (23, 30, "PREP")
    ]}),
    ("1 large raw lobster tail, shell removed and meat cut into 1-inch pieces, at room temperature", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 11, "PREP"),
        (12, 24, "NAME"),
        (26, 71, "PREP"),  # Fix: Span ends at 'pieces' (char 71), not including trailing comma or 'a'
        (73, 92, "COMMENT") # Fix: Span starts at 'at' (char 73) and ends at 'temperature' (char 94)
    ]}),
    ("1 pound emmanthal, cubed", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 17, "NAME"),
        (19, 24, "PREP")
    ]}),
    ("1 12-ounce package shishito peppers", {"entities": [
        (0, 1, "QTY"),
        (2, 10, "COMMENT"),
        (11, 18, "UNIT"),
        (19, 35, "NAME")
    ]}),
    ("1/2 cup oatmeal", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (8, 15, "NAME")
    ]}),
    ("1 quart (4 cups) liquid (I'm using chicken stock)", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 16, "COMMENT"),  # Fix: '(4 cups)'
        (17, 23, "NAME"),     # Fix: 'liquid'
        (25, 49, "COMMENT")
    ]}),
    ("2 cups (225 grams) chocolate chunks", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),
        (7, 18, "COMMENT"),  # Fix: '(225 grams)'
        (19, 35, "NAME")      # Fix: 'chocolate chunks'
    ]}),
    ("1 large or 2 regular Vidalia or sweet onions, halved and sliced", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 12, "ALT_QTY"),
        (13, 20, "ALT_UNIT"),
        (21, 28, "NAME"),
        (32, 37, "ALT_NAME"), # Fix: 'sweet'
        (38, 44, "ALT_NAME"), # Fix: 'onions'
        (46, 63, "PREP")      # Fix: 'halved and sliced'
    ]}),
    ("1/2 pound cooked special crabmeat", {"entities": [
        (0, 3, "QTY"),
        (4, 9, "UNIT"),
        (10, 16, "PREP"),
        (17, 24, "PREP"),
        (25, 33, "NAME")
    ]}),
    ("1 small wheel, 4 inches, camembert, liverot or Pont L'Eveque cheese, available in specialty cheese case", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 13, "UNIT"),      # Fix: 'wheel' as UNIT, corrected end
        (15, 24, "COMMENT"),   # Fix: '4 inches,'
        (25, 35, "NAME"),      # Fix: 'camembert,'
        (36, 43, "ALT_NAME"),  # Fix: 'liverot'
        (47, 68, "ALT_NAME"),  # Fix: 'Pont L'Eveque cheese,'
        (69, 103, "COMMENT")    # Fix: 'available in specialty cheese case'
    ]}),
    ("1/4 to 1/2 ounce dried morels or porcinis, or a combination of both", {"entities": [
        (0, 3, "QTY"),
        (4, 10, "ALT_QTY"),
        (11, 16, "UNIT"),
        (17, 22, "PREP"),    # Fix: 'dried'
        (23, 29, "NAME"),    # Fix: 'morels'
        (30, 42, "ALT_NAME"), # Fix: 'porcinis,'
        (43, 67, "COMMENT")  # Fix: 'or a combination of both'
    ]}),
    ("1/4 pound pickled tongue", {"entities": [
        (0, 3, "QTY"),
        (4, 9, "UNIT"),
        (10, 17, "PREP"),
        (18, 24, "NAME")
    ]}),
    ("1 tablespoon plus 1/2 teaspoon cardamom seeds", {"entities": [
        (0, 1, "QTY"),
        (2, 12, "UNIT"),
        (13, 29, "ALT_QTY"),
        (30, 44, "NAME")
    ]}),
    ("1 head frissee", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),
        (7, 14, "NAME")
    ]}),
    ("1 teaspoon, 1/3 palm full, fennel seeds", {"entities": [
        (0, 1, "QTY"),
        (2, 10, "UNIT"),      # Fixed: 'teaspoon' (char 2 to 10)
        (10, 26, "COMMENT"),  # Fixed: ', 1/3 palm full,' (char 10 to 26)
        (27, 39, "NAME")
    ]}),
    ("4 large sheets parchment paper", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "PREP"),
        (8, 14, "UNIT"),
        (15, 30, "NAME")
    ]}),
    ("12 tablespoons chopped, cooked vegetable of choice; such as asparagus, chopped spinach or artichoke hearts", {"entities": [
        (0, 2, "QTY"),
        (3, 14, "UNIT"),
        (15, 30, "PREP"),
        (31, 50, "NAME"),
        (52, 106, "COMMENT")  # Fixed: Start after semicolon (char 52)
    ]}),
    ("2 teaspoon MSG", {"entities": [
        (0, 1, "QTY"),
        (2, 9, "UNIT"),
        (10, 13, "NAME")
    ]}),
    ("1/2 cup kasseri, grated", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (8, 15, "NAME"),
        (15, 23, "PREP")
    ]}),
    ("2 bananas (not too ripe)", {"entities": [
        (0, 1, "QTY"),
        (2, 9, "NAME"),
        (10, 24, "COMMENT")
    ]}),
    ("2 quarts all-natural chunk charcoal", {"entities": [
        (0, 1, "QTY"),
        (2, 8, "UNIT"),
        (9, 26, "PREP"),
        (27, 35, "NAME")
    ]}),
    ("1 (8 to 10-pound turkey) neck and giblets removed", {"entities": [
        (0, 1, "QTY"),
        (2, 24, "COMMENT"),  # Fixed: '(8 to 10-pound turkey)' (char 1 to 24)
        (25, 49, "PREP")      # Fixed: 'neck and giblets removed' (char 25 to 49)
    ]}),
    ("4 mirlitons (chayote squash), halved (about 3 pounds)", {"entities": [
        (0, 1, "QTY"),
        (2, 11, "NAME"),
        (12, 29, "COMMENT"),
        (30, 36, "PREP"),     # Fixed: 'halved' (char 30 to 36)
        (37, 53, "COMMENT")   # Fixed: '(about 3 pounds)' (char 37 to 53)
    ]}),
    ("1 package (8 ounces) shredded 6-cheese Italian Blend (Mozzarella, smoked Provolone, Parmesan, Romano, Fontina, and Asiago cheeses)", {"entities": [
        (0, 1, "QTY"),
        (2, 9, "UNIT"),
        (10, 20, "COMMENT"),
        (21, 29, "NAME"),
        (30, 52, "NAME"),     # Fix: Corrected end char to 48 (for "6-cheese Italian Blend")
        (53, 129, "COMMENT")   # This entity's start char 53 is now correct (for "(Mozzarella...")
    ]}),
    ("2 cups 10x or 12x powdered sugar, sifted", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),
        (7, 17, "COMMENT"),  # Fixed: '10x or 12x' (char 7 to 17)
        (18, 33, "NAME"),     # Fixed: 'powdered sugar,' (char 18 to 33)
        (34, 40, "PREP")      # Fixed: 'sifted' (char 34 to 40)
    ]}),
    ("1 cup oil reserved from poaching tuna", {"entities": [
        (0, 1, "QTY"),
        (2, 5, "UNIT"),
        (6, 9, "NAME"),
        (10, 37, "COMMENT")
    ]}),
    ("1/4 teaspoon MSG (optional)", {"entities": [
        (0, 3, "QTY"),
        (4, 12, "UNIT"),      # Fixed: 'teaspoon' (char 4 to 12)
        (13, 16, "NAME"),      # Fixed: 'MSG' (char 13 to 16)
        (17, 26, "COMMENT")    # Fixed: '(optional)' (char 16 to 27)
    ]}),
    ("2 tablespoons fat reserved from the confit", {"entities": [
        (0, 1, "QTY"),
        (2, 13, "UNIT"),
        (14, 17, "NAME"),
        (18, 42, "COMMENT")
    ]}),
    ("1/4 cup equal parts chopped capers and cornichons", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (8, 19, "PREP"),
        (20, 27, "PREP"),
        (28, 49, "NAME")
    ]}),
    ("1/2 cup plus 2 teaspoons sour cream", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (8, 24, "COMMENT"),  # Fixed: 'plus 2 teaspoons' (char 8 to 24)
        (25, 35, "NAME")      # Fixed: 'sour cream' (char 25 to 35)
    ]}),
    ("14 ounces (400 grams) wild boar meat, minced", {"entities": [
        (0, 2, "QTY"),
        (3, 9, "UNIT"),
        (10, 21, "COMMENT"),
        (22, 36, "NAME"),
        (36, 44, "PREP")
    ]}),
    ("2 teaspoons non-fat or skim powdered milk", {"entities": [
        (0, 1, "QTY"),
        (2, 11, "UNIT"),      # Fixed: 'teaspoons' (char 2 to 11)
        (12, 19, "NAME"),      # Fixed: 'non-fat' (char 11 to 18)
        (20, 27, "ALT_NAME"),      # Fixed: 'or skim' (char 19 to 26)
        (28, 41, "NAME")       # Fixed: 'powdered milk' (char 27 to 41)
    ]}),
    ("1 ficelle (approximately 12 inches), or French bread of choice", {"entities": [
        (0, 1, "QTY"),
        (2, 9, "NAME"),
        (10, 35, "COMMENT"),  # Fixed: '(approximately 12 inches)' (char 10 to 35)
        (35, 62, "ALT_NAME")  # Fixed: ', or French bread of choice' (char 35 to 62)
    ]}),
    ("1/2 tablespoon reduced-sodium or lite soy sauce", {"entities": [
        (0, 3, "QTY"),
        (4, 14, "UNIT"),
        (15, 37, "PREP"),
        (38, 47, "NAME")
    ]}),
    ("1 ounce, or about 3 1/2 tablespoons, almond and sugar powder, recipe follows", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (7, 35, "COMMENT"),  # Correct span for ", or about 3 1/2 tablespoons"
        (35, 60, "NAME"),     # Correct span for ", almond and sugar powder"
        (60, 76, "COMMENT")   # Fix: Corrected string is "recipe follows" and end char is 76 (original was 75 and truncated)
    ]}),
    ("1 quart cold-smoked cod", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 19, "PREP"),
        (20, 23, "NAME")
    ]}),
    ("3 teaspoon MSG, optional", {"entities": [
        (0, 1, "QTY"),
        (2, 10, "UNIT"),      # Fixed: 'teaspoon' (char 2 to 10)
        (11, 14, "NAME"),      # Fixed: 'MSG' (char 11 to 14)
        (14, 24, "COMMENT")    # Fixed: ', optional' (char 14 to 24)
    ]}),

        ("1/4 ounce absinthe", {"entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),
            (10, 18, "NAME")
        ]}),
    ("2 cups chopped or sliced apricots, plums, peaches or pineapple", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),
        (7, 24, "PREP"),
        (25, 33, "NAME"),       # 'apricots' as NAME
        (35, 40, "ALT_NAME"),   # 'plums' as ALT_NAME
        (42, 49, "ALT_NAME"),   # 'peaches' as ALT_NAME
        (53, 62, "ALT_NAME")    # 'pineapple' as ALT_NAME (leaving 'or' as 'O' tag)
    ]}),
        ("2 partridges, washed and patted dry, broken into legs and breasts", {"entities": [
            (0, 1, "QTY"),
            (2, 12, "NAME"), # 'partridges' is a countable item. No specific unit like 'each' is requested for it, so it's part of the NAME.
            (12, 65, "PREP")
        ]}),
        ("1/2 cup chocolate chunks or chips", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 24, "NAME"),
            (25, 33, "ALT_NAME")
        ]}),
        ("3 to 4 quarts oil with a high smoke point, such as cottonseed, peanut or vegetable", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "ALT_QTY"),
            (7, 13, "UNIT"),
            (14, 17, "NAME"),
            (18, 82, "COMMENT")
        ]}),
        ("2 tablespoons freshly grated wasabi, flash frozen or powder made into a paste", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 28, "PREP"),
            (29, 35, "NAME"),
            (37, 77, "COMMENT")
        ]}),
        ("1 package pot sticker wraps (recommended: Dynasty, Gyoza/Potsticker wrappers)", {"entities": [
            (0, 1, "QTY"),
            (2, 9, "UNIT"),
            (10, 27, "NAME"),
            (28, 77, "COMMENT")
        ]}),
        ("1/4 cup thinly sliced young and tender celery stalk", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 21, "PREP"),
            (22, 38, "PREP"),
            (39, 51, "NAME")
        ]}),
        ("1 1/4 ounces (36 grams) trimoline", {"entities": [
            (0, 5, "QTY"),
            (6, 12, "UNIT"),
            (13, 23, "COMMENT"),
            (24, 33, "NAME")
        ]}),
        ("2 tablespoons, plus 1 cup pure olive oil", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (13, 25, "COMMENT"), # Covers ", plus 1 cup"
            (26, 30, "PREP"),
            (31, 40, "NAME")
        ]}),
        ("1 tablespoon plus 1/2 teaspoon cardamom seeds", {"entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),
            (13, 29, "COMMENT"), # Covers "plus 1/2 teaspoon"
            (30, 44, "NAME")
        ]}),
        ("1 cup chocolate chunks", {"entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 22, "NAME")
        ]}),
        ("2 pounds assorted wild and exotic mushrooms, such as morels, chanterelles, shiitake or oyster mushrooms", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 33, "PREP"),
            (34, 43, "NAME"),
            (43, 103, "COMMENT")
        ]}),
        ("4 ounces semi-sweet chocolate, chopped", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 19, "PREP"),
            (20, 29, "NAME"),
            (29, 38, "PREP")
        ]}),

    ("Generous handful or two of fresh coriander leaves, roughly chopped", {"entities": [
        (0, 23, "COMMENT"),  # Fix: 'Generous handful or two' (ends at 23, removing trailing space)
        (27, 32, "PREP"),   # Fix: 'fresh' (starts at 27)
        (33, 49, "NAME"),   # Fix: 'coriander leaves,' (starts at 33, ends at 49)
        (49, 66, "PREP")    # Fix: ', roughly chopped' (starts at 49, ends at 66)
    ]}),
    ("6 ounces (about 1/2 head) Hakusai (Chinese cabbage)", {"entities": [
        (0, 1, "QTY"),
        (2, 8, "UNIT"),
        (9, 25, "COMMENT"),  # Fix: '(about 1/2 head)' (ends at 25, removing trailing space)
        (26, 51, "NAME")    # Fix: 'Hakusai (Chinese cabbage)' (starts at 26, was 'akusai')
    ]}),
        ("15 steaks", {"entities": [
            (0, 2, "QTY"),
            (3, 9, "NAME")        # "steaks" (countable item)
        ]}),
    ("1 large or 2 medium onions, chopped", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 12, "ALT_QTY"),
        (13, 19, "ALT_UNIT"),
        (20, 26, "NAME"),
        (28, 35, "PREP")    # Fix: 'chopped' (starts at 28, not 27, and ends at 35)
    ]}),
        ("1/4 pound shiitakes, discard stems, julienned", {"entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),
            (10, 20, "NAME"),     # "shiitakes,"
            (21, 35, "PREP"),     # "discard stems,"
            (36, 45, "PREP")      # "julienned"
        ]}),
        ("One 8-ounce package mixed gourmet mushrooms (the package I buy contains trumpet, brown clamshell and velvet pioppini, but any mushroom you want to use is fine)", {"entities": [
            (0, 3, "QTY"),        # "One"
            (4, 11, "COMMENT"),  # "8-ounce" (size description for package)
            (12, 19, "UNIT"),     # "package"
            (20, 43, "NAME"),     # "mixed gourmet mushrooms"
            (44, 159, "COMMENT")   # "(the package I buy contains trumpet, brown clamshell and velvet pioppini, but any mushroom you want to use is fine)"
        ]}),
        ("One 8-ounce package mixed gourmet mushrooms (the package I buy contains trumpet, brown clamshell and velvet pioppini, but any mushroom you want to use is fine)", {"entities": [
            (0, 3, "QTY"),        # "One"
            (4, 11, "COMMENT"),  # "8-ounce"
            (12, 19, "UNIT"),     # "package"
            (20, 43, "NAME"),     # "mixed gourmet mushrooms"
            (44, 159, "COMMENT")   # "(the package I buy contains trumpet, brown clamshell and velvet pioppini, but any mushroom you want to use is fine)"
        ]}),
        ("1 cup bar-b-que sauce", {"entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 21, "NAME")
        ]}),
        ("1 large or 2 medium onions, finely chopped", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),      # "large"
            (8, 12, "ALT_QTY"),  # "or 2"
            (13, 19, "ALT_UNIT"), # "medium"
            (20, 27, "NAME"),     # "onions,"
            (28, 42, "PREP")      # "finely chopped"
        ]}),
    ("1 cup liquid of your choice, such as beer, wine, water or stock", {"entities": [
        (0, 1, "QTY"),
        (2, 5, "UNIT"),
        (6, 12, "NAME"),
        (13, 63, "COMMENT")  # Fix: 'of your choice, such as beer, wine, water or stock' (ends at 63 to include 'k' of 'stock')
    ]}),
    ("1 medium or 2 small onions, cut into 1/4-inch dice (about 1 1/2 cups)", {"entities": [
        (0, 1, "QTY"),
        (2, 8, "UNIT"),
        (9, 13, "ALT_QTY"),
        (14, 19, "ALT_UNIT"),
        (20, 27, "NAME"),
        (28, 50, "PREP"),    # Fix: 'cut into 1/4-inch dice' (ends at 50)
        (51, 69, "COMMENT")  # Fix: '(about 1 1/2 cups)' (starts at 51, not 48)
    ]}),
    ("2 cups fresh, or frozen and thawed, cranberries", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),
        (7, 13, "PREP"),
        (14, 34, "PREP"),  # Fix: 'or frozen and thawed,' (ends at 34 to include 'd,' of 'thawed,')
        (36, 47, "NAME")   # Fix: 'cranberries' (starts at 36, ends at 47)
    ]}),
    ("2 teaspoons togerashi*", {"entities": [
        (0, 1, "QTY"),
        (2, 11, "UNIT"),      # Fix: 'teaspoons' (ends at 11)
        (12, 21, "NAME"),     # Fix: 'togerashi' (starts at 12, ends at 21)
        (21, 22, "COMMENT")   # Fix: '*' (starts at 21, ends at 22)
    ]}),
    ("2 large, sweet, juicy carrots, julienned", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "PREP"),
        (9, 14, "PREP"),   # Fix: 'sweet' (starts at 9, not 8)
        (16, 21, "PREP"),   # Fix: 'juicy' (starts at 16, not 15)
        (22, 29, "NAME"),
        (31, 40, "PREP")    # Fix: 'julienned' (starts at 31, not 30)
    ]}),
        ("1 cup liquid (I'm using water)", {"entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 12, "NAME"),     # "liquid"
            (13, 30, "COMMENT")   # "(I'm using water)"
        ]}),
    ("1/4 cup packed very finely minced, pureed, or grated ginger", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (8, 14, "PREP"),
        (15, 34, "PREP"),
        (35, 42, "PREP"),
        (43, 52, "NAME"),  # Fix: 'or grated' (ends at 52, not 53)
        (53, 59, "NAME")   # Fix: 'ginger' (starts at 53, ends at 59)
    ]}),

    ("2 packages or 10 biscuits buttermilk biscuit dough", {"entities": [
        (0, 1, "QTY"),
        (2, 10, "UNIT"),
        (11, 25, "ALT_QTY"),
        (26, 50, "NAME")      # Fix: String representation is now "buttermilk biscuit dough" (ends at 49, fixing truncation)
    ]}),
    ("1 pound roasted, peeled, and cleaned chestnuts cut into quarters", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 36, "PREP"),      # Fix: String representation is now "roasted, peeled, and cleaned" (ends at 35, fixing truncation)
        (37, 46, "NAME"),
        (47, 64, "PREP")
    ]}),
        ("1/2 cup fudge sauce", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 19, "NAME")       # "fudge sauce"
        ]}),
    ("1 large rind trimmed from a hunk of Parmigiano-Reggiano cheese or a few small pieces rind perhaps saved-up", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 12, "PREP"),
        (13, 20, "PREP"),
        (21, 35, "COMMENT"),   # Fix: Span for "from a hunk of" (ends at 35)
        (36, 62, "NAME"),      # Fix: Span for "Parmigiano-Reggiano cheese" (starts at 36)
        (63, 106, "COMMENT"),   # Fix: Span for "or a few small pieces"
    ]}),
        ("About 1 1/2 teaspoons or scant half palmful chili powder", {"entities": [
            (0, 5, "COMMENT"),    # "About"
            (6, 11, "QTY"),        # "1 1/2"
            (12, 21, "UNIT"),     # "teaspoons"
            (22, 40, "COMMENT"),  # "or scant half palmful"
            (41, 53, "NAME")      # "chili powder"
        ]}),
    ("About 1 1/2 teaspoons or scant half palmful pimenton or smoked paprika", {"entities": [
        (0, 5, "COMMENT"),
        (6, 11, "QTY"),
        (12, 21, "UNIT"),
        (22, 43, "COMMENT"),  # Fix: Span for "or scant half palmful" (ends at 43)
        (44, 52, "NAME"),     # Fix: Span for "pimenton" (starts at 44)
        (53, 70, "ALT_NAME")  # Fix: Span for "or smoked paprika" (starts at 53)
    ]}),
        ("1 tablespoon single cream", {"entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),     # "tablespoon"
            (13, 19, "PREP"),     # "single"
            (20, 25, "NAME")      # "cream"
        ]}),
    ("1 large rind trimmed from a hunk of Parmigiano-Reggiano cheese, or a few small pieces of saved-up rind", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 12, "PREP"),
        (13, 20, "PREP"),
        (21, 35, "COMMENT"),   # Fix: Span for "from a hunk of" (ends at 35)
        (36, 62, "NAME"),      # Fix: Span for "Parmigiano-Reggiano cheese" (starts at 36)
        (64, 97, "COMMENT"),
    ]}),
        ("1 package (21 ounces) fudge brownie mix", {"entities": [
            (0, 1, "QTY"),
            (2, 9, "UNIT"),       # "package"
            (10, 21, "COMMENT"),  # "(21 ounces)"
            (22, 40, "NAME")      # "fudge brownie mix"
        ]}),
        ("2 cups (measured uncooked) medium shells cooked, chilled and patted dry", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),       # "cups"
            (7, 26, "COMMENT"),   # "(measured uncooked)"
            (27, 33, "PREP"),     # "medium"
            (34, 40, "NAME"),      # "shells"
            (41, 71, "PREP")       # "cooked, chilled and patted dry"
        ]}),
    ("1 cup and 2 tablespoons or 250 grams water", {"entities": [
        (0, 1, "QTY"),
        (2, 5, "UNIT"),
        (6, 36, "COMMENT"),  # Fix: Span for "and 2 tablespoons or 250 grams"
        (37, 42, "NAME")      # Fix: Span for "water"
    ]}),

    ("1/2 cup 1-inch parsnip chunks", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (8, 14, "PREP"),      # Fix: Span for "1-inch"
        (15, 29, "NAME")       # Fix: Span for "parsnip chunks"
    ]}),
        ("1 1/2 pounds loose sausage", {"entities": [
            (0, 5, "QTY"),
            (6, 12, "UNIT"),      # "pounds"
            (13, 18, "PREP"),      # "loose"
            (19, 26, "NAME")       # "sausage"
        ]}),
    ("A quarter of a pineapple, core removed and diced", {"entities": [
        (0, 14, "PREP"),      # Fix: Span for "A quarter of a"
        (15, 25, "NAME"),     # Fix: Span for "pineapple,"
        (26, 48, "PREP")      # Fix: Span for "core removed and diced"
    ]}),
        ("1 1/2 cups pitted, nicoise olives", {"entities": [
            (0, 5, "QTY"),
            (6, 10, "UNIT"),      # "cups"
            (11, 18, "PREP"),      # "pitted,"
            (19, 26, "PREP"),      # "nicoise"
            (27, 33, "NAME")       # "olives"
        ]}),
        ("4 Earl Grey tea bags", {"entities": [
            (0, 1, "QTY"),
            (2, 15, "NAME"),      # "Earl Grey tea"
            (16, 20, "COMMENT")      # "bags" (as countable unit)
        ]}),
    ("1 pound fresh, young, green beans, trimmed", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 14, "PREP"),
        (15, 21, "PREP"),
        (22, 27, "NAME"),     # Fix: Span for "green"
        (28, 34, "NAME"),     # Fix: Span for "beans,"
        (35, 42, "PREP")      # Fix: Span for "trimmed"
    ]}),
    ("1 1/2 cups low sodium, fat free chicken broth", {"entities": [
        (0, 5, "QTY"),
        (6, 10, "UNIT"),
        (11, 22, "PREP"),
        (23, 31, "PREP"),
        (32, 45, "NAME")       # Fix: Span for "chicken broth" (ends at 45)
    ]}),
    ("1 quart (approximately) vegetable or chicken stock to have on hand to adjust sauce", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 23, "COMMENT"),
        (24, 33, "NAME"),
        (34, 44, "ALT_NAME"),
        (45, 50, "NAME"),
        (51, 82, "COMMENT")    # Fix: Span for "to have on hand to adjust sauce" (ends at 83, removing trailing space if any)
    ]}),
    ("1 1/4 pounds skinned and bones uncooked chicken, cut into cubes to make 4 cups", {"entities": [
        (0, 5, "QTY"),
        (6, 12, "UNIT"),
        (13, 30, "PREP"),      # Fix: Span for "skinned and bones" (ends at 30)
        (31, 39, "PREP"),      # Fix: Span for "uncooked" (starts at 31)
        (40, 47, "NAME"),     # Fix: Span for "chicken" (starts at 40)
        (49, 78, "PREP")
    ]}),
        ("1 bundle thin asparagus trimmed and sliced on an angle", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),       # "bundle"
            (9, 13, "PREP"),       # "thin"
            (14, 23, "NAME"),      # "asparagus"
            (24, 54, "PREP")       # "trimmed and sliced on an angle"
        ]}),
        ("9 Earl Grey tea bags", {"entities": [
            (0, 1, "QTY"),
            (2, 15, "NAME"),      # "Earl Grey tea"
            (16, 20, "COMMENT")      # "bags" (as countable unit)
        ]}),
        ("1 1/2 pounds loose sweet Italian sausage", {"entities": [
            (0, 5, "QTY"),
            (6, 12, "UNIT"),      # "pounds"
            (13, 18, "PREP"),      # "loose"
            (19, 24, "NAME"),      # "sweet"
            (25, 32, "NAME"),      # "Italian"
            (33, 40, "NAME")       # "sausage"
        ]}),
    ("1 pound dried, salted codfish", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 13, "PREP"),      # Fix: Span for "dried" (ends at 13). The comma is left untagged.
        (15, 21, "PREP"),     # Fix: Span for "salted" (starts at 15)
        (22, 29, "NAME")      # Fix: Span for "codfish" (starts at 22)
    ]}),

        ("1 small disk washed-rind cheese, such as Camembert", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "small" (from countable items list)
            (8, 12, "UNIT"),      # "disk" (as a countable unit/form)
            (13, 24, "PREP"),      # "washed-rind"
            (25, 30, "NAME"),      # "cheese,"
            (31, 50, "COMMENT")    # "such as Camembert"
        ]}),
        ("1 ounce Herbsaint (or Absinth or Pernod)", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "ounce"
            (8, 17, "NAME"),      # "Herbsaint"
            (19, 39, "ALT_NAME")  # "(or Absinth or Pernod)"
        ]}),
        ("2 tablespoons of chipolte in adobo, pureed", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),      # "tablespoons"
            (14, 16, "COMMENT"),   # "of" (often untagged, or can be COMMENT if you want to include prepositions)
            (17, 34, "NAME"),      # "chipolte in adobo,"
            (36, 42, "PREP")       # "pureed"
        ]}),

        ("One 16-oz package kataifi (shredded phyllo dough)", {"entities": [
            (0, 3, "QTY"),        # "One"
            (4, 9, "COMMENT"),   # "16-oz" (size description for package)
            (10, 17, "UNIT"),     # "package"
            (18, 25, "NAME"),      # "kataifi"
            (27, 48, "COMMENT")    # "(shredded phyllo dough)"
        ]}),

        ("1 1/2 pound pre-marinated apple bourbon pork tenderloin, Hormel®", {"entities": [
            (0, 5, "QTY"),
            (6, 11, "COMMENT"),   # "1-1 1/2 pound" (a specific quantity/weight range description)
            (12, 25, "PREP"),      # "pre-marinated"
            (26, 55, "NAME"),      # "apple bourbon pork tenderloin,"
            (57, 64, "COMMENT")    # "Hormel®" (brand)
        ]}),
        ("5 ounces washed and dried lamb's lettuce, stemmed (aka corn salad or mache)", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),       # "ounces"
            (9, 25, "PREP"),      # "washed and dried"
            (26, 40, "NAME"),      # "lamb's lettuce,"
            (42, 49, "PREP"),      # "stemmed"
            (50, 74, "COMMENT")    # "(aka corn salad or mache)"
        ]}),
        ("1/2 cup processed or cream cheese", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 17, "PREP"),      # "processed"
            (18, 20, "O"),        # "or" (untagged, acts as a conjunction)
            (21, 33, "NAME")       # "cream cheese"
        ]}),
    ("1/3 cup processed or cream cheese", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 17, "PREP"),      # "processed"
            (18, 20, "O"),        # "or" (untagged, acts as a conjunction)
            (21, 33, "NAME")       # "cream cheese"
        ]}),
    ("1/4 cup processed or cream cheese", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 17, "PREP"),      # "processed"
            (18, 20, "O"),        # "or" (untagged, acts as a conjunction)
            (21, 33, "NAME")       # "cream cheese"
        ]}),
        ("1 pound (58 percent cocoa) chocolate, finely chopped", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "pound"
            (9, 25, "COMMENT"),   # "(58 percent cocoa)"
            (27, 36, "NAME"),      # "chocolate,"
            (38, 52, "PREP")       # "finely chopped"
        ]}),
        ("4 ounces very fine (fideo or capellini) noodles, broken into 1inch lengths", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),       # "ounces"
            (9, 18, "PREP"),      # "very fine"
            (19, 38, "COMMENT"),   # "(fideo or capellini)"
            (40, 48, "NAME"),      # "noodles,"
            (49, 74, "PREP")       # "broken into 1inch lengths"
        ]}),
    ("2 or 2 1/2 pounds head, bones, and skins from carp, pike, and whitefish", {"entities": [
        (0, 1, "QTY"),
        (2, 10, "ALT_QTY"),  # "or 2 1/2"
        (11, 17, "UNIT"),     # "pounds"
        (18, 23, "PREP"),      # "head,"
        (24, 30, "PREP"),      # "bones,"
        (31, 40, "PREP"),      # "and skins"
        (41, 45, "COMMENT"),   # "from" (as a preposition, best as COMMENT or O)
        (46, 50, "NAME"),      # 'carp' as NAME
        (52, 56, "ALT_NAME"),  # 'pike' as ALT_NAME (leaving ',' and 'and' untagged 'O')
        (58, 71, "ALT_NAME")   # 'whitefish' as ALT_NAME (leaving ',' and 'and' untagged 'O')
    ]}),
        ("1/2 cup popcorn kernels, freshly popped", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 23, "NAME"),      # "popcorn kernels,"
            (25, 39, "PREP")       # "freshly popped"
        ]}),
        ("1 tablespoon plus 1 1/2 teaspoons doubanjiang (spicy bean paste)", {"entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),     # "tablespoon"
            (13, 29, "COMMENT"),  # "plus 1 1/2 teaspoons"
            (30, 41, "NAME"),      # "doubanjiang"
            (42, 64, "COMMENT")    # "(spicy bean paste)"
        ]}),

        ("1 pound boned and skinned halibut, haddock, or cod", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "pound"
            (8, 25, "PREP"),      # "boned and skinned"
            (26, 33, "NAME"),      # "halibut,"
            (35, 42, "ALT_NAME"),  # "haddock,"
            (44, 50, "ALT_NAME")   # "or cod"
        ]}),
        ("4 tablespoons fat skimmed from the pan juices", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),      # "tablespoons"
            (14, 17, "NAME"),      # "fat"
            (18, 45, "PREP")       # "skimmed from the pan juices"
        ]}),
        ("3/4 cup liquid of your choice, such as beef stock, chicken stock, water or wine (I'm using red wine)", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 14, "NAME"),      # "liquid"
            (15, 61, "COMMENT"),   # "of your choice, such as beef stock, chicken stock, water or wine"
            (62, 89, "COMMENT")    # "(I'm using red wine)"
        ]}),
        ("10 pretzels", {"entities": [
            (0, 2, "QTY"),
            (3, 11, "NAME")       # "pretzels" (countable item)
        ]}),
        ("1 1/2 lbs ground, lean pork", {"entities": [
            (0, 5, "QTY"),
            (6, 9, "UNIT"),       # "lbs"
            (10, 16, "PREP"),      # "ground,"
            (18, 22, "PREP"),      # "lean"
            (23, 27, "NAME")       # "pork"
        ]}),
        ("1 cup torn or shredded mozzarella, such as Good & Gather™ Mozzarella Cheese", {"entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),       # "cup"
            (6, 22, "PREP"),      # "torn"
            (23, 33, "NAME"),      # "mozzarella,"
            (35, 75, "COMMENT")    # "such as Good & Gather™ Mozzarella Cheese"
        ]}),

        ("1 1/2 cups whipped cream, for garnish", {"entities": [
            (0, 5, "QTY"),
            (6, 10, "UNIT"),       # "cups"
            (11, 24, "NAME"),      # "whipped cream,"
            (26, 37, "COMMENT")    # "for garnish"
        ]}),
        ("1/3 cup plus 1 tablespoon EVOO", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 25, "COMMENT"),    # "plus 1 tablespoon"
            (26, 30, "NAME")       # "EVOO"
        ]}),
        ("8 tablespoons whipped cream or whipped topping", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),      # "tablespoons"
            (14, 27, "NAME"),      # "whipped cream"
            (28, 46, "ALT_NAME")   # "whipped topping"
        ]}),
        ("1/2 cup coarse, raw, or demerara sugar", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 32, "PREP"),      # "coarse,"
            (33, 38, "NAME")       # "sugar"
        ]}),
        ("2 tablespoons minced pimiento", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),      # "tablespoons"
            (14, 20, "PREP"),      # "minced"
            (21, 29, "NAME")       # "pimiento"
        ]}),
        ("3 tablespoons plus 1/3 cup walnuts, chopped", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),      # "tablespoons"
            (14, 26, "ALT_QTY"),  # "plus 1/3 cup"
            (27, 34, "NAME"),      # "walnuts,"
            (36, 43, "PREP")       # "chopped"
        ]}),

        ("1 cup grapes, sliced", {"entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),       # "cup"
            (6, 13, "NAME"),      # "grapes,"
            (14, 20, "PREP")       # "sliced"
        ]}),
        ("1 cup hot fudge sauce, warmed, plus more for serving", {"entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),       # "cup"
            (6, 21, "NAME"),      # "hot fudge sauce,"
            (23, 29, "PREP"),      # "warmed,"
            (31, 52, "COMMENT")    # "plus more for serving"
        ]}),
        ("1 (8- to 10-ounce) pack whole cremini mushrooms, halved", {"entities": [
            (0, 1, "QTY"),
            (2, 18, "COMMENT"),   # "(8- to 10-ounce)"
            (19, 23, "COMMENT"),     # "pack" (as a countable unit)
            (24, 29, "PREP"),      # "whole"
            (30, 47, "NAME"),      # "cremini mushrooms,"
            (49, 55, "PREP")       # "halved"
        ]}),
        ("12 tablespoons (1 1/2 sticks), butter chilled and cut into small pieces", {"entities": [
            (0, 2, "QTY"),
            (3, 14, "UNIT"),      # "tablespoons"
            (15, 30, "COMMENT"),   # "(1 1/2 sticks),"
            (31, 37, "NAME"),      # "butter"
            (38, 71, "PREP")       # "chilled and cut into small pieces"
        ]}),
        ("3 truffles with their juice", {"entities": [
            (0, 1, "QTY"),
            (2, 10, "NAME"),      # "truffles" (countable item)
            (11, 27, "COMMENT")    # "with their juice"
        ]}),

        ("1 (7.5-ounce) can refrigerator biscuits", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "COMMENT"),   # "(7.5-ounce)"
            (14, 17, "UNIT"),     # "can"
            (18, 30, "PREP"),      # "refrigerator"
            (31, 39, "NAME")       # "biscuits"
        ]}),
        ("1 pound hot or sweet Italian sausage links", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "pound"
            (8, 20, "PREP"),      # "hot"
            (21, 28, "NAME"),      # "Italian"
            (29, 42, "NAME")       # "sausage links"
        ]}),
        ("9 ounces (255ml) double cream", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),       # "ounces"
            (10, 15, "COMMENT"),   # "(255ml)"
            (17, 29, "NAME"),      # "double"
        ]}),
        ("8 cups homemade or low-sodium beef broth, recipe follows", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),       # "cups"
            (7, 29, "PREP"),      # "homemade"
            (30, 40, "NAME"),      # "beef broth,"
            (42, 56, "COMMENT")    # "recipe follows"
        ]}),
        ("1 waffle cone", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "NAME")       # "waffle cone" (countable item)
        ]}),
        ("1/4 cup hot fudge sauce, warmed", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 23, "NAME"),      # "hot fudge sauce,"
            (25, 31, "PREP")       # "warmed"
        ]}),

    ("2 tablespoons chopped pimiento", {"entities": [
        (0, 1, "QTY"),
        (2, 13, "UNIT"),
        (14, 21, "PREP"),     # Corrected: "chopped"
        (22, 30, "NAME")      # Corrected: "pimiento"
    ]}),
        ("1 1/2 cups fresh (seedless) grapes, stemmed, halved", {"entities": [
            (0, 5, "QTY"),
            (6, 10, "UNIT"),      # "cups"
            (11, 16, "PREP"),      # "fresh"
            (17, 27, "COMMENT"),   # "(seedless)"
            (28, 35, "NAME"),      # "grapes,"
            (36, 44, "PREP"),      # "stemmed,"
            (45, 51, "PREP")       # "halved"
        ]}),
    ("3 cups sparkling water, chilled", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),
        (7, 22, "NAME"),      # Corrected: "sparkling water"
        (24, 31, "PREP")       # Corrected: ", chilled"
    ]}),
    ("2 to 3 cups shredded provolone and mozzarella cheese blend", {"entities": [
        (0, 6, "QTY"),
        (7, 11, "UNIT"),
        (12, 20, "NAME"),
        (21, 30, "NAME"),
        (31, 58, "ALT_NAME")   # Corrected: "and mozzarella cheese blend"
    ]}),
        ("2 cups Quervo 1800", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),       # "cups"
            (7, 18, "NAME")       # "Quervo 1800"
        ]}),
    ("4 ounces of your favorite liquor", {"entities": [
        (0, 1, "QTY"),
        (2, 8, "UNIT"),
        (9, 25, "COMMENT"),   # Corrected: "of your favorite"
        (26, 32, "NAME")       # Corrected: "liquor" (adjusted start index)
    ]}),
        ("2 tablespoons drained, julienned Pickled Radishes, recipe follows", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),      # "tablespoons"
            (14, 22, "PREP"),      # "drained,"
            (23, 32, "PREP"),      # "julienned"
            (33, 50, "NAME"),      # "Pickled Radishes,"
            (51, 65, "COMMENT")    # "recipe follows"
        ]}),
        ("2 jars (16 ounces each) Pace® Picante Sauce", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "COMMENT"),       # "jars" (as a countable unit)
            (7, 23, "COMMENT"),   # "(16 ounces each)"
            (24, 43, "NAME")       # "Pace® Picante Sauce"
        ]}),
    ("2 cups plus 2 tablespoons bourbon", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),
        (7, 25, "COMMENT"),    # Corrected: "plus 2 tablespoons"
        (26, 33, "NAME")       # Corrected: "bourbon"
    ]}),
        ("1 pound char, skinless, 1/2-inch dice", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "pound"
            (8, 13, "NAME"),      # "char,"
            (14, 23, "PREP"),      # "skinless,"
            (24, 37, "PREP")       # "1/2-inch dice"
        ]}),
    ("4 tablespoons skimmed fat from turkey drippings", {"entities": [
        (0, 1, "QTY"),
        (2, 13, "UNIT"),
        (14, 21, "PREP"),     # Corrected: "skimmed" (removed trailing space)
        (22, 25, "NAME"),     # Corrected: "fat" (fixed starting index and content)
        (26, 47, "COMMENT")   # Corrected: "from turkey drippings" (fixed starting index and content)
    ]}),
    ("5 grams (1 teaspoon salt)", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 19, "COMMENT"),   # Corrected: "(1 teaspoon" (removed "salt)" from comment, keeping the full parentheses)
        (20, 24, "NAME")       # Corrected: "salt" as NAME (the ')' at index 24 is not part of the name)
    ]}),
    ("1 quince, peeled, cored, and cut into 1-inch dice", {"entities": [
        (0, 1, "QTY"),
        (2, 9, "NAME"),
        (10, 17, "PREP"),      # Corrected: "peeled,"
        (18, 24, "PREP"),      # Corrected: "cored,"
        (25, 49, "PREP")       # Corrected: "and cut into 1-inch dice"
    ]}),
        ("1 bottle tonic", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "COMMENT"),       # "bottle" (as a countable unit)
            (9, 14, "NAME")       # "tonic"
        ]}),
    ("1 1/2 cups sparkling water, such as San Pellegrino, chilled", {"entities": [
        (0, 5, "QTY"),
        (6, 10, "UNIT"),
        (11, 26, "NAME"),      # Corrected: "sparkling water"
        (28, 50, "COMMENT"),   # Corrected: ", such as San Pellegrino"
        (52, 59, "PREP")       # Corrected: ", chilled"
    ]}),
    ("1 pound center-cut halibut, skin removed, cut into 4 equal pieces", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),
        (8, 18, "PREP"),      # Corrected: "center-cut"
        (19, 27, "NAME"),      # Corrected: "halibut,"
        (28, 40, "PREP"),      # "skin removed" is correct as is
        (42, 65, "PREP")       # "cut into 4 equal pieces" is correct as is
    ]}),

        ("3 cups low-sodium turkey or chicken broth", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),       # "cups"
            (7, 17, "PREP"),      # "low-sodium"
            (18, 24, "NAME"),      # "turkey"
            (25, 35, "ALT_NAME"),  # "or chicken"
            (36, 41, "NAME")       # "broth"
        ]}),
        ("1 cup (250ml) sour cream", {"entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),       # "cup"
            (6, 13, "COMMENT"),   # "(250ml)"
            (14, 24, "NAME")      # "sour cream"
        ]}),
        ("1/2 cup kasseri, grated", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 15, "NAME"),      # "kasseri,"
            (16, 23, "PREP")       # "grated"
        ]}),
        ("1 tablespoon plus 1/2 teaspoon cardamom seeds", {"entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),     # "tablespoon"
            (13, 29, "COMMENT"),  # "plus 1/2 teaspoon"
            (30, 44, "NAME")      # "cardamom seeds"
        ]}),
        ("2 cups chopped (small cubes) fresh apricots (about 3 apricots)", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),       # "cups"
            (7, 14, "PREP"),      # "chopped"
            (15, 28, "COMMENT"),   # "(small cubes)"
            (29, 34, "PREP"),      # "fresh"
            (35, 43, "NAME"),      # "apricots"
            (45, 61, "COMMENT")    # "(about 3 apricots)"
        ]}),
        ("1 1/2 tablespoons Sofrito, recipe follows", {"entities": [
            (0, 5, "QTY"),
            (6, 17, "UNIT"),      # "tablespoons"
            (18, 26, "NAME"),      # "Sofrito,"
            (27, 41, "COMMENT")    # "recipe follows"
        ]}),
        ("1 small handful of thyme sprigs", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "small" (describes the size, as per 'large' etc. in countable items)
            (8, 15, "COMMENT"),   # "handful" (describes method of quantity, not a formal unit)
            (19, 31, "NAME")       # "thyme sprigs"
        ]}),
        ("1/8 teaspoon clove optional", {"entities": [
            (0, 3, "QTY"),
            (4, 12, "UNIT"),     # "teaspoon"
            (13, 18, "NAME"),      # "clove"
            (19, 27, "COMMENT")    # "optional"
        ]}),
        ("2 pounds hay", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),       # "pounds"
            (9, 12, "NAME")       # "hay"
        ]}),
        ("1 cup liquid of your choice, such as water, stock, beer, etc.", {"entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),       # "cup"
            (6, 12, "NAME"),      # "liquid"
            (13, 60, "COMMENT")    # "of your choice, such as water, stock, beer, etc."
        ]}),
        ("2 cups chopped (small cubes) fresh apricots (about 3 apricots)", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),       # "cups"
            (7, 14, "PREP"),      # "chopped"
            (15, 29, "COMMENT"),   # "(small cubes)"
            (30, 35, "PREP"),      # "fresh"
            (36, 45, "NAME"),      # "apricots"
            (46, 61, "COMMENT")    # "(about 3 apricots)"
        ]}),
        ("1 cup low-sodium turkey or chicken broth", {"entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),       # "cup"
            (6, 16, "PREP"),      # "low-sodium"
            (17, 23, "NAME"),      # "turkey"
            (24, 34, "ALT_NAME"),  # "or chicken"
            (35, 40, "NAME")       # "broth"
        ]}),
        ("6 (16-ounce) center-cut NY strips", {"entities": [
            (0, 1, "QTY"),
            (2, 12, "COMMENT"),   # "(16-ounce)"
            (13, 23, "PREP"),      # "center-cut"
            (24, 33, "NAME")       # "NY strips"
        ]}),
        ("1 1/2 pounds large yellow or red beets, washed and trimmed", {"entities": [
            (0, 5, "QTY"),
            (6, 12, "UNIT"),      # "pounds"
            (13, 18, "PREP"),      # "large" (describes quality/size of beets)
            (19, 25, "NAME"),      # "yellow"
            (26, 32, "ALT_NAME"),  # "or red"
            (33, 38, "NAME"),      # "beets,"
            (40, 58, "PREP")       # "washed and trimmed"
        ]}),

    ("1/2 pound clams, manila, count necks, and little necks, scrubbed", {"entities": [
        (0, 3, "QTY"),
        (4, 9, "UNIT"),       # "pound"
        (10, 15, "NAME"),      # "clams,"
        (16, 23, "ALT_NAME"),  # "manila,"
        (24, 35, "ALT_NAME"),  # "count necks,"
        (36, 49, "ALT_NAME"),  # "and little necks,"
        (50, 58, "PREP")       # "scrubbed"
    ]}),
    ("2 medium to large onions, sliced", {"entities": [
        (0, 1, "QTY"),
        (2, 8, "UNIT"),  # "medium to large"
        (9, 17, "ALT_UNIT"),  # "medium to large"
        (18, 24, "NAME"),      # "onions,"
        (26, 32, "PREP")       # "sliced"
    ]}),
    ("16 cups hot, freshly popped popcorn", {"entities": [
        (0, 2, "QTY"),
        (3, 7, "UNIT"),       # "cups"
        (8, 12, "PREP"),      # "hot,"
        (13, 27, "PREP"),      # "freshly popped"
        (28, 35, "NAME")      # "popcorn"
    ]}),
    ("1/2 pound domestic or wild mushrooms, sliced and sauteed", {"entities": [
        (0, 3, "QTY"),
        (4, 9, "UNIT"),       # "pound"
        (10, 26, "PREP"),      # "domestic"
        (27, 36, "NAME"),      # "mushrooms,"
        (38, 56, "PREP")       # "sliced and sauteed"
    ]}),
    ("16 large, perfect strawberries, preferably with stems", {"entities": [
        (0, 2, "QTY"),
        (3, 8, "PREP"),       # "large," (describes quality/size)
        (10, 17, "PREP"),      # "perfect"
        (18, 30, "NAME"),      # "strawberries,"
        (32, 53, "COMMENT")    # "preferably with stems"
    ]}),

    ("1/2 cup cucumber peeled and sliced into 1/2-inch pieces", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),       # "cup"
        (8, 16, "NAME"),      # "cucumber"
        (17, 55, "PREP")       # "peeled and sliced into 1/2-inch pieces"
    ]}),
    ("8 ounces any combination of cremini, shiitake, or oyster mushrooms (about 4 cups)", {"entities": [
        (0, 1, "QTY"),
        (2, 8, "UNIT"),       # "ounces"
        (9, 27, "COMMENT"),   # "any combination of"
        (28, 35, "NAME"),      # "cremini,"
        (37, 45, "ALT_NAME"),  # "shiitake,"
        (47, 56, "ALT_NAME"),  # "oyster mushrooms"
        (57, 66, "NAME"),  # "oyster mushrooms"
        (67, 81, "COMMENT")    # "(about 4 cups)"
    ]}),
    ("4 cups air-popped popcorn", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),       # "cups"
        (7, 17, "PREP"),      # "air-popped"
        (18, 25, "NAME")      # "popcorn"
    ]}),
    ("2 ounces chopped, crystallized or candied ginger", {"entities": [
        (0, 1, "QTY"),
        (2, 8, "UNIT"),       # "ounces"
        (9, 16, "PREP"),      # "chopped,"
        (18, 41, "PREP"),      # "crystallized"
        (42, 48, "NAME")       # "ginger"
    ]}),
    ("1 1/2 teaspoons, 1/2 a palm full, coriander", {"entities": [
        (0, 5, "QTY"),
        (6, 15, "UNIT"),      # "teaspoons"
        (15, 33, "COMMENT"),   # ", 1/2 a palm full,"
        (34, 43, "NAME")       # "coriander"
    ]}),
    ("1 large French loaf, split in half lengthwise", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),       # "large" (as per countable items)
        (8, 19, "NAME"),      # "French loaf,"
        (21, 45, "PREP")       # "split in half lengthwise"
    ]}),
    ("1 tablespoon whole grain or Dijon mustard", {"entities": [
        (0, 1, "QTY"),
        (2, 12, "UNIT"),      # "tablespoon"
        (13, 33, "PREP"),      # "whole grain"
        (34, 41, "NAME")       # "mustard"
    ]}),
    ("1 small jawbreaker", {"entities": [
        (0, 1, "QTY"),
        (2, 7, "UNIT"),       # "small" (as per countable items)
        (8, 18, "NAME")       # "jawbreaker"
    ]}),

        ("3 cups mixed blueberries and blackberries", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),       # "cups"
            (7, 12, "PREP"),      # "mixed"
            (13, 24, "NAME"),      # "blueberries"
            (25, 41, "ALT_NAME")   # "blackberries"
        ]}),
        ("1/3 cup instant grits", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 15, "PREP"),      # "instant"
            (16, 21, "NAME")       # "grits"
        ]}),
        ("1 1/2 cups single cream", {"entities": [
            (0, 5, "QTY"),
            (6, 10, "UNIT"),      # "cups"
            (11, 17, "PREP"),     # "single"
            (18, 23, "NAME")       # "cream"
        ]}),
        ("1/2 cup 35 percent cream", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 18, "PREP"),      # "35 percent"
            (19, 24, "NAME")       # "cream"
        ]}),
        ("1 1/2 cups asparagus tips", {"entities": [
            (0, 5, "QTY"),
            (6, 10, "UNIT"),      # "cups"
            (11, 25, "NAME")       # "asparagus tips"
        ]}),
        ("1 pound semi-sweet or bittersweet chocolate", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "pound"
            (8, 33, "PREP"),      # "semi-sweet"
            (34, 43, "NAME")       # "chocolate"
        ]}),
        ("1 1/2 cups quick grits", {"entities": [
            (0, 5, "QTY"),
            (6, 10, "UNIT"),      # "cups"
            (11, 16, "PREP"),     # "quick"
            (17, 22, "NAME")       # "grits"
        ]}),
        ("1 package store-bought biscuits", {"entities": [
            (0, 1, "QTY"),
            (2, 9, "UNIT"),       # "package"
            (10, 22, "PREP"),     # "store-bought"
            (23, 31, "NAME")       # "biscuits"
        ]}),
        ("1 1/2 pounds coarse-ground sirloin", {"entities": [
            (0, 5, "QTY"),
            (6, 12, "UNIT"),      # "pounds"
            (13, 26, "PREP"),     # "coarse-ground"
            (27, 34, "NAME")       # "sirloin"
        ]}),
        ("1 cup stone-ground grits", {"entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),       # "cup"
            (6, 18, "PREP"),     # "stone-ground"
            (19, 24, "NAME")       # "grits"
        ]}),
        ("3 pounds skinless, firm, white fish fillets, cut into large chunks", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),       # "pounds"
            (9, 17, "PREP"),      # "skinless,"
            (19, 23, "PREP"),      # "firm,"
            (25, 30, "PREP"),      # "white"
            (31, 43, "NAME"),      # "fish fillets,"
            (45, 66, "PREP")       # "cut into large chunks"
        ]}),
    # In your train_data.json or equivalent Python list:
    ("2 tablespoons roux, recipe follows", {"entities": [
        (0, 1, "QTY"),
        (2, 13, "UNIT"),      # "tablespoons"
        (14, 18, "NAME"),      # "roux"
        (18, 19, "O"),         # ","
        (20, 34, "COMMENT")    # "recipe follows"
    ]}),
    ("3 tablespoons peeled and chopped fresh ginger root, or galanga", {"entities": [
        (0, 1, "QTY"),
        (2, 13, "UNIT"),      # "tablespoons"
        (14, 32, "PREP"),      # "peeled"
        (33, 38, "PREP"),      # "fresh"
        (39, 50, "NAME"),      # "ginger root,"
        (52, 62, "ALT_NAME")   # "or galanga"
    ]}),
    ("1000 grams poolish", {"entities": [
        (0, 4, "QTY"),
        (5, 10, "UNIT"),      # "grams"
        (11, 18, "NAME")       # "poolish"
    ]}),
    # In your train_data.json or equivalent Python list:
    ("1/3 to 1/2 cup liquid such as dairy milk, almond, cashew or coconut milk", {"entities": [
        (0, 3, "QTY"),        # "1/3 to 1/2"
        (4, 10, "ALT_QTY"),        # "1/3 to 1/2"
        (11, 14, "UNIT"),     # "cup"
        (15, 21, "NAME"),      # "liquid"
        (22, 29, "COMMENT"),   # "such as"
        (30, 40, "ALT_NAME"),  # "dairy milk"
        (42, 48, "ALT_NAME"),  # "almond"
        (50, 56, "ALT_NAME"),  # "cashew"
        (57, 72, "ALT_NAME")   # "or coconut milk"
    ]}),
    # In your train_data.json or equivalent Python list:
    ("1 (12-ounce) can or pouch albacore tuna packed in water, drained and flaked", {"entities": [
        (0, 1, "QTY"),
        (2, 12, "COMMENT"),   # "(12-ounce)"
        (13, 16, "UNIT"),     # "can"
        (17, 25, "COMMENT"), # "or pouch"
        (26, 39, "NAME"),      # "albacore tuna"
        (40, 55, "PREP"),      # "packed in water"
        (55, 56, "O"),         # ","
        (57, 75, "PREP")       # "drained and flaked"
    ]}),
    # In your dev_data.json or equivalent Python list:
    ("2 pounds heads and bones from black bass, red snapper or halibut", {"entities": [
        (0, 1, "QTY"),
        (2, 8, "UNIT"),       # "pounds"
        (9, 14, "NAME"),      # "heads"
        (15, 18, "O"),         # "and"
        (19, 24, "NAME"),      # "bones"
        (25, 29, "COMMENT"),   # "from"
        (30, 40, "NAME"),      # "black bass"
        (40, 41, "O"),         # ","
        (42, 53, "ALT_NAME"),  # "red snapper"
        (54, 64, "ALT_NAME")   # "halibut"
    ]}),
    # In your dev_data.json or equivalent Python list:
    ("8 ounces (2 cups) shredded cheese recommended: Colby/Monterey blend or Mexican blend", {"entities": [
        (0, 1, "QTY"),
        (2, 8, "UNIT"),       # "ounces"
        (9, 17, "COMMENT"),   # "(2 cups)"
        (18, 26, "NAME"),      # "shredded"
        (27, 33, "NAME"),      # "cheese"
        (34, 84, "COMMENT")    # "recommended: Colby/Monterey blend or Mexican blend"
    ]}),
    ("1/3 ounce Jim Beam", {"entities": [
        (0, 3, "QTY"),
        (4, 9, "UNIT"),       # "ounce"
        (10, 18, "NAME")       # "Jim Beam"
    ]}),
    # In your dev_data.json or equivalent Python list:
    # In your dev_data.json or equivalent Python list:
    ("1/4 cup finely chopped fresh chervil if available", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),       # "cup"
        (8, 22, "PREP"),      # "finely chopped"
        (29, 36, "NAME"),      # "chervil"
        (37, 49, "COMMENT")    # "if available"
    ]}),
    ("2 teaspoons whole peppercorn", {"entities": [
        (0, 1, "QTY"),
        (2, 11, "UNIT"),      # "teaspoons"
        (12, 17, "PREP"),     # "whole"
        (18, 28, "NAME")       # "peppercorn"
    ]}),

        ("3 cups (700ml) stock or hot water", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),       # "cups"
            (7, 14, "COMMENT"),   # "(700ml)"
            (15, 20, "NAME"),      # "stock"
            (21, 33, "ALT_NAME")   # "hot water"
        ]}),
        ("1 pound All-Purpose Pasta Dough, cut into tagliatelle shape, recipe follows", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "pound"
            (8, 31, "NAME"),      # "All-Purpose Pasta Dough,"
            (33, 59, "PREP"),      # "cut into tagliatelle shape,"
            (61, 75, "COMMENT")    # "recipe follows"
        ]}),
        ("1/4 pound pork, trimmed of fat", {"entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),       # "pound"
            (10, 15, "NAME"),      # "pork,"
            (16, 30, "PREP")       # "trimmed of fat"
        ]}),
        ("1/3 cup store bought or homemade Tapenade, recipe follows", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 32, "PREP"),      # "homemade"
            (33, 42, "NAME"),      # "Tapenade,"
            (43, 57, "COMMENT")    # "recipe follows"
        ]}),
        ("1 pound firm, small zucchini, 1/2-inch dice", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "pound"
            (8, 12, "PREP"),      # "firm,"
            (14, 19, "PREP"),      # "small"
            (20, 28, "NAME"),      # "zucchini,"
            (30, 43, "PREP")       # "1/2-inch dice"
        ]}),
        ("8 T-bone steaks, each 10 to 12 ounces", {"entities": [
            (0, 1, "QTY"),
            (2, 15, "NAME"),      # "T-bone steaks," (countable item)
            (17, 37, "COMMENT")    # "each 10 to 12 ounces"
        ]}),

        ("1/4 cup granulated or powdered garlic", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 30, "PREP"),      # "granulated"
            (31, 37, "NAME")       # "garlic"
        ]}),
        ("1/2 pound penne, cooked and drained according to package directions", {"entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),       # "pound"
            (10, 15, "NAME"),      # "penne,"
            (17, 35, "PREP"),      # "cooked and drained"
            (36, 67, "COMMENT")    # "according to package directions"
        ]}),

        ("1/2 tablespoon ginger julienned super fine", {"entities": [
            (0, 3, "QTY"),
            (4, 14, "UNIT"),      # "tablespoon"
            (15, 21, "NAME"),      # "ginger"
            (22, 42, "PREP"),      # "julienned"
        ]}),
        ("1/2 cup of a mustard vinaigrette", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 11, "COMMENT"),   # "of a"
            (12, 32, "NAME")      # "mustard vinaigrette"
        ]}),
        ("1/2 cup buttermilk, room temperature", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 19, "NAME"),      # "buttermilk,"
            (20, 36, "PREP")       # "room temperature"
        ]}),
        ("4 cups pitted cherries", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),       # "cups"
            (7, 13, "PREP"),      # "pitted"
            (14, 22, "NAME")       # "cherries"
        ]}),

        ("1 pound purchased cheese tortellini", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "pound"
            (8, 17, "PREP"),      # "purchased"
            (18, 35, "NAME")       # "cheese tortellini"
        ]}),

        ("7 pounds bones with meat (pork ribs, neck bones and ox tails)", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),       # "pounds"
            (9, 14, "NAME"),      # "bones"
            (15, 24, "PREP"),      # "with meat"
            (25, 54, "COMMENT")    # "(pork ribs, neck bones and ox tails)"
        ]}),
        ("2 tablespoons capers, washed and drained", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),      # "tablespoons"
            (14, 21, "NAME"),      # "capers,"
            (22, 40, "PREP")       # "washed and drained"
        ]}),
    ("4 ounces thinly sliced hot or sweet capicola, torn", {"entities": [
        (0, 1, "QTY"),
        (2, 8, "UNIT"),
        (9, 22, "PREP"),      # "thinly sliced" (no trailing space)
        (23, 35, "PREP"),      # "hot or sweet" (correct start index and content)
        (36, 44, "NAME"),      # "capicola" (excluding comma)
        (44, 45, "O"),         # ","
        (46, 50, "PREP")       # "torn"
    ]}),
        ("3/4 pound stone crabmeat", {"entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),       # "pound"
            (10, 15, "PREP"),      # "stone"
            (16, 24, "NAME")       # "crabmeat"
        ]}),
    ("4 each rack of baby lamb, frenched and cleaned", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),
        (7, 24, "NAME"),      # "rack of baby lamb" (correct content)
        (24, 25, "O"),         # ","
        (26, 46, "PREP")       # "frenched and cleaned" (fixed start index)
    ]}),
        ("2 large onions, roughly chopped", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "large" (from countable items list)
            (8, 15, "NAME"),      # "onions,"
            (16, 31, "PREP")       # "roughly chopped"
        ]}),
        ("3 tablespoons sweetener (I'm using honey)", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),      # "tablespoons"
            (14, 23, "NAME"),      # "sweetener"
            (24, 41, "COMMENT")    # "(I'm using honey)"
        ]}),
        ("2 ounces hot fudge, heated to 150 degrees F", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),       # "ounces"
            (9, 12, "PREP"),      # "hot"
            (13, 19, "NAME"),      # "fudge,"
            (20, 43, "PREP")       # "heated to 150 degrees F"
        ]}),
    ("1/2 cup (packed) each - dried apricots and pitted prunes", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (8, 16, "PREP"),      # "(packed)"
        (17, 23, "COMMENT"),   # "each -"
        (24, 38, "NAME"),      # "dried apricots" (no trailing space)
        (39, 56, "ALT_NAME")   # "and pitted prunes" (fixed start index for 'and')
    ]}),
        ("1 large or 2 small clementines, sliced thin", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "large"
            (8, 12, "ALT_QTY"),  # "or 2"
            (13, 18, "ALT_UNIT"), # "small"
            (19, 31, "NAME"),      # "clementines,"
            (32, 43, "PREP")       # "sliced thin"
        ]}),
        ("2 cups chopped green and red cabbage", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),       # "cups"
            (7, 14, "PREP"),      # "chopped"
            (15, 28, "PREP"),      # "green"
            (29, 36, "NAME")       # "cabbage"
        ]}),
        ("1 1/4 teaspoons coarse or kosher salt", {"entities": [
            (0, 5, "QTY"),
            (6, 15, "UNIT"),      # "teaspoons"
            (16, 32, "PREP"),     # "coarse"
            (33, 37, "NAME")       # "salt"
        ]}),
        ("2 cubanelle peppers, roughly chopped", {"entities": [
            (0, 1, "QTY"),
            (2, 20, "NAME"),      # "cubanelle peppers," (countable item)
            (21, 36, "PREP")       # "roughly chopped"
        ]}),
    ("2 cups chopped or shredded roasted meat (I'm using yesterday's leftover chicken)", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),
        (7, 14, "PREP"),      # "chopped"
        (15, 26, "PREP"),      # "or shredded" (no trailing space)
        (27, 34, "PREP"),      # "roasted" (correct span)
        (35, 39, "NAME"),      # "meat" (correct span)
        (40, 41, "O"),         # "(" (separate token)
        (41, 79, "COMMENT"),   # "I'm using yesterday's leftover chicken" (excluding trailing ')')
        (79, 80, "O")          # ")" (separate token)
    ]}),
        ("3 ounces capers, drained", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),       # "ounces"
            (9, 16, "NAME"),      # "capers,"
            (17, 24, "PREP")       # "drained"
        ]}),
        ("8 ounces onions, roughly chopped", {"entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),       # "ounces"
            (9, 16, "NAME"),      # "onions,"
            (17, 32, "PREP")       # "roughly chopped"
        ]}),
    ("1/2 cup dry, pitted prunes", {"entities": [
        (0, 3, "QTY"),
        (4, 7, "UNIT"),
        (8, 11, "PREP"),      # "dry"
        (11, 12, "O"),         # ","
        (13, 19, "PREP"),      # "pitted" (no trailing space)
        (20, 26, "NAME")       # "prunes" (correct start and end index)
    ]}),("2 cups frozen grain-and-rice blend, thawed", {"entities": [
        (0, 1, "QTY"),
        (2, 6, "UNIT"),
        (7, 13, "PREP"),      # "frozen"
        (14, 34, "NAME"),      # "grain-and-rice blend"
        (34, 35, "O"),         # ","
        (36, 42, "PREP")       # "thawed" (correct start/end and content)
    ]}),
    ("2 tablespoons or more beurre manie, recipe follows", {"entities": [
        (0, 1, "QTY"),
        (2, 13, "UNIT"),      # "tablespoons"
        (14, 21, "COMMENT"),   # "or more" (no trailing space)
        (22, 34, "NAME"),      # "beurre manie" (correct start index and content)
        (34, 35, "O"),         # ","
        (36, 50, "COMMENT")    # "recipe follows" (correct start index and content)
    ]}),
        ("4 tablespoons coarse or kosher salt", {"entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),      # "tablespoons"
            (14, 20, "PREP"),     # "coarse"
            (21, 30, "PREP"),     # "or kosher"
            (31, 35, "NAME")       # "salt"
        ]}),
        ("1 pound onions, roughly chopped", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "pound"
            (8, 15, "NAME"),      # "onions,"
            (16, 31, "PREP")       # "roughly chopped"
        ]}),
        ("1 large glass container with a lid", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "large" (as per countable items list)
            (8, 13, "PREP"),      # "glass"
            (14, 23, "NAME"),      # "container"
            (24, 34, "COMMENT")    # "with a lid"
        ]}),

        ("Mint sprigs, for garnish", {"entities": [
            (0, 11, "NAME"),       # "Mint sprigs"
            (11, 12, "O"),          # ","
            (13, 24, "COMMENT")     # "for garnish"
        ]}),
        ("1/2 cup browning", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 16, "NAME")        # "browning"
        ]}),
        ("1/2 small sourdough loaf, cut into six 1/2-inch-thick slices", {"entities": [
            (0, 3, "QTY"),
            (4, 9, "PREP"),       # "small"
            (10, 24, "NAME"),      # "sourdough loaf"
            (24, 25, "O"),          # ","
            (26, 61, "PREP")        # "cut into six 1/2-inch-thick slices"
        ]}),
        ("1/4 cup pure Grade A maple syrup", {"entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),       # "cup"
            (8, 20, "PREP"),      # "pure Grade A" (could also be COMMENT, depending on your schema)
            (21, 32, "NAME")       # "maple syrup"
        ]}),
        ("1 chervil leaf for garnish", {"entities": [
            (0, 1, "QTY"),
            (2, 14, "NAME"),      # "chervil leaf"
            (15, 26, "COMMENT")    # "for garnish"
        ]}),
        ("1 tablespoon plus 1/2 teaspoon cardamom seeds", {"entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),      # "tablespoon"
            (13, 30, "COMMENT"),   # "plus 1/2 teaspoon"
            (31, 45, "NAME")       # "cardamom seeds"
        ]}),

        ("1 pound manila clams, scrubbed", {"entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "pound"
            (8, 20, "NAME"),      # "manila clams"
            (20, 21, "O"),          # ","
            (22, 30, "PREP")        # "scrubbed"
        ]}),
        ("3 cups peeled, seeded watermelon, diced", {"entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),       # "cups"
            (7, 13, "PREP"),      # "peeled"
            (13, 14, "O"),          # ","
            (15, 21, "PREP"),      # "seeded"
            (22, 32, "NAME"),      # "watermelon"
            (32, 33, "O"),          # ","
            (34, 39, "PREP")        # "diced"
        ]}),

        ("1/4 Falernum*", {"entities": [
            (0, 3, "QTY"),
            (4, 12, "NAME"),       # "Falernum" (excluding the asterisk)
        ]}),
        ("1/2 ounce seaweed, ognori, rinsed free of salt", {"entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),       # "ounce"
            (10, 17, "NAME"),      # "seaweed"
            (17, 18, "O"),          # ","
            (19, 25, "ALT_NAME"),   # "ognori" (assuming it's an alternative name or type of seaweed)
            (25, 26, "O"),          # ","
            (27, 46, "PREP")        # "rinsed free of salt"
        ]})














]
if __name__ == '__main__':
    out_file = open("./train_data.json", 'w')
    json.dump(TRAIN_DATA, out_file)