import json

TRAIN_DATA = [
    # Simple cases
    ("2 cups flour", {"entities": [(0, 1, "QTY"), (2, 6, "UNIT"), (7, 12, "NAME")]}),
    ("1 large egg", {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 11, "NAME")]}),
    ("salt", {"entities": [(0, 4, "NAME")]}),

    # Fraction and mixed number quantities
    ("1/2 cup sugar", {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "NAME")]}),
    ("1 1/2 tsp vanilla extract", {"entities": [(0, 5, "QTY"), (6, 9, "UNIT"), (10, 17, "NAME"), (18, 25, "NAME")]}), # "vanilla extract"

    # Word quantities
    ("One large onion, chopped", {"entities": [(0, 3, "QTY"), (4, 9, "UNIT"), (10, 15, "NAME"), (17, 24, "PREP")]}),

    # More complex names and descriptors
    ("1/2 cup whole milk", {"entities": [(0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "NAME"), (14, 18, "NAME")]}), # "whole milk"
    ("4 ounces cream cheese, at room temperature", {"entities": [(0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "NAME"), (15, 21, "NAME"), (23, 42, "COMMENT")]}),
    ("1 cup all-purpose flour", {"entities": [(0, 1, "QTY"), (2, 5, "UNIT"), (6, 17, "NAME"), (18, 23, "NAME")]}),
    ("2 tablespoons unsalted butter, melted", {"entities": [(0, 1, "QTY"), (2, 13, "UNIT"), (14, 22, "NAME"), (23, 29, "NAME"), (31, 37, "PREP")]}),

    ("1 1/2 cups finely chopped pecans", {"entities": [(0,5,"QTY"), (6,10,"UNIT"), (11,17,"PREP"), (18,25,"NAME"), (26,32,"NAME")]}),

    ("1 small bunch swiss chard stems removed leaves chopped", {"entities": [
        (0,1,"QTY"), (2,7,"UNIT"), (8,13,"UNIT"),
        (14,19,"NAME"), (20,25,"NAME"),
        (26,31,"PREP"),(32,39,"PREP"),(40,46,"PREP"),(47,54,"PREP")
    ]}),
    ("kosher salt", {"entities": [(0,6,"NAME"),(7,11,"NAME")]}),
    ("freshly ground pepper", {"entities": [(0,7,"PREP"),(8,14,"NAME"),(15,21,"NAME")]}),
    ("1 15-ounce can navy beans undrained", {"entities": [
        (0,1,"QTY"), (2,10,"COMMENT"), (11,14,"UNIT"),
        (15,19,"NAME"),(20,25,"NAME"), (26,35,"PREP")
    ]}),
    ("Juice of 2 lemons (about 1/4 cup)", {"entities": [
        (0,5,"NAME"),     # "Juice" <-- or PREP if it's an action
        (9,10,"QTY"),     # "2" (the initial quantity)
        (11,17,"NAME"),   # "lemons"
        (18,33,"COMMENT") # "(about 1/4 cup)" <-- Label the whole thing
        # Inside this COMMENT, your parser will find QTY/UNIT
    ]}),
    ("About 32 frozen turkey meatballs", {
        "entities": [
            (0, 5, "COMMENT"), # "About"
            (6, 8, "QTY"),     # "32"
            (9, 15, "PREP"),   # "frozen" (or could be part of NAME)
            (16, 22, "NAME"),  # "turkey"
            (23, 32, "NAME")   # "meatballs"
        ]
    }),
    ("1 tablespoon mayonnaise", {
        "entities": [
            (0, 1, "QTY"),        # "1"
            (2, 12, "UNIT"),      # "tablespoon"
            (13, 23, "NAME")      # "mayonnaise"
        ]
    }),
    ("2 chipotle peppers in adobo sauce", {
        "entities": [
            (0, 1, "QTY"),        # "2"
            (2, 10, "NAME"),      # "chipotle"
            (11, 18, "NAME"),     # "peppers"
            # "in" (19,21) will be O (Outside)
            (22, 27, "NAME"),     # "adobo"
            (28, 33, "NAME")      # "sauce"
        ]
    }),
    ("3 tablespoons chopped fresh cilantro", {
        "entities": [
            (0, 1, "QTY"),        # "3"
            (2, 13, "UNIT"),      # "tablespoons"
            (14, 21, "PREP"),     # "chopped"
            (22, 27, "PREP"),     # "fresh" (or NAME if "fresh cilantro" is common)
            (28, 36, "NAME")      # "cilantro"
        ]
    }),
    ("1/2 pint blueberries", {
        "entities": [
            (0, 3, "QTY"),    # "1/2"
            (4, 8, "UNIT"),   # "pint"
            (9, 20, "NAME")   # "blueberries"
        ]
    }),
    ("One 15-ounce loaf challah bread, broken into 2-inch chunks", {
        "entities": [
            (0, 3, "QTY"),        # "One"
            (4, 12, "COMMENT"),   # "15-ounce"
            (13, 17, "UNIT"),     # "loaf"
            (18, 25, "NAME"),     # "challah"
            (26, 31, "NAME"),     # "bread"
            (33, 39, "PREP"),     # "broken"
            (40, 44, "PREP"),     # "into"
            (45, 51, "COMMENT"),  # "2-inch" (describes chunks)
            (52, 58, "PREP")      # "chunks"
        ]
    }),
    ("1 pound bucatoni, cooked al dente", {
        "entities": [
            (0, 1, "QTY"),        # "1"
            (2, 7, "UNIT"),       # "pound"
            (8, 16, "NAME"),      # "bucatoni"
            (18, 24, "PREP"),     # "cooked"
            (25, 27, "PREP"),     # "al"
            (28, 33, "PREP")      # "dente"
        ]
    }),
    ("Alfredo Dipping Sauce", {
        "entities": [
            (0, 7, "NAME"),   # "Alfredo"
            (8, 15, "NAME"),  # "Dipping"
            (16, 21, "NAME")  # "Sauce"
        ]
    }),
    ("1 lemon",{'entities':[(0, 1, "QTY"),  (2,7,'NAME')]}),
    ("2 cups grated sharp Cheddar", {
        "entities": [
            (0, 1, "QTY"), (2, 6, "UNIT"), (7, 13, "PREP"),
            (14, 19, "PREP"), (20, 27, "NAME")
        ]
    }),
    ("1 unbaked Pam's Pie Crust, recipe follows", {
        "entities": [
            (0, 1, "QTY"), (2, 9, "PREP"), (10, 15, "NAME"),
            (16, 19, "NAME"), (20, 25, "NAME"), (27, 41, "COMMENT")
        ]
    }),
    ("20 large (size 16-20) shrimp, peeled and deveined with tail on", {
        "entities": [
            (0, 2, "QTY"),
            (3, 8, "UNIT"),
            (9, 21, "COMMENT"),
            (22, 28, "NAME"),
            (30, 36, "PREP"),
            (41, 49, "PREP"),
            (50, 54, "PREP"),
            (55, 59, "PREP"),
            (60, 62, "PREP")
        ]
    }),
    ("4 slices lemon, for garnish", {
        "entities": [
            (0, 1, "QTY"),     # "4"
            (2, 8, "UNIT"),    # "slices"
            (9, 14, "NAME"),   # "lemon"
            # Comma (char 14) is O
            (16, 27, "COMMENT")# "for garnish" <-- Corrected end offset
        ]
    }),
    ("1 teaspoon chili paste, or to taste and tolerance", {
        "entities": [
            (0, 1, "QTY"),
            (2, 10, "UNIT"),
            (11, 16, "NAME"),
            (17, 22, "NAME"),
            (24, 49, "COMMENT") # Corrected end offset
        ]
    }),
    ("8 garlic cloves, crushed and finely minced", {
        "entities": [
            (0, 1, "QTY"),     # "8"
            (2, 8, "NAME"),    # "garlic"
            (9, 15, "NAME"),   # "cloves"
            (17, 24, "PREP"),  # "crushed"
            # "and" is O
            (29, 35, "PREP"),  # "finely"
            (36, 42, "PREP")   # "minced"
        ]
    }),
    ("1/2 cup finely diced angelica, or citron", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 14, "PREP"),
            (15, 20, "PREP"),
            (21, 29, "NAME"),
            (31, 40, "COMMENT") # Corrected end offset
        ]
    }),
    ("2 to 3 packages popping rock candy, such as Pop Rocks", {
        "entities": [
            (0, 6, "QTY"),
            (7, 15, "UNIT"),
            (16, 23, "NAME"),
            (24, 28, "NAME"),
            (29, 34, "NAME"),
            (36, 53, "COMMENT") # Corrected end offset
        ]
    }),
    ("Olives, for garnish", {
        "entities": [
            (0, 6, "NAME"),     # "Olives"
            (8, 19, "COMMENT")  # "for garnish"
        ]
    }),
    ("Ice", {
        "entities": [
            (0, 3, "NAME")      # "Ice"
        ]
    }),
    (".5 ounces dry vermouth", { # Using Option 1 for "dry vermouth"
        "entities": [
            (0, 2, "QTY"), (3, 9, "UNIT"), (10, 13, "NAME"), (14, 22, "NAME")
        ]
    }),
    ("Olive or lemon twist for garnish", { # PREVIOUSLY EXAMPLE 36
        "entities": [
            (0, 5, "NAME"),
            (6, 20, "COMMENT"), # "or lemon twist"
            (21, 32, "COMMENT") # "for garnish"
        ]
    }),
    ("3 scallions, thinly sliced white and green, separated", {
        "entities": [
            (0, 1, "QTY"), (2, 11, "NAME"), (13, 19, "PREP"), (20, 26, "PREP"),
            (27, 32, "PREP"), (37, 42, "PREP"), (44, 53, "PREP") # Fixed
        ]
    }),
    ("1 pound peeled and cleaned medium shrimp", {
        "entities": [
            (0, 1, "QTY"),      # "1"
            (2, 7, "UNIT"),     # "pound"
            (8, 14, "PREP"),    # "peeled"
            # "and" (15,18) is O
            (19, 26, "PREP"),   # "cleaned"
            (27, 33, "COMMENT"),# "medium"
            (34, 40, "NAME")    # "shrimp"
        ]
    }),
    ("1 tablespoon Shao Hsing rice cooking wine, or pale dry sherry", {
        "entities": [
            (0, 1, "QTY"),      # "1"
            (2, 12, "UNIT"),    # "tablespoon"
            (13, 17, "NAME"),   # "Shao"
            (18, 23, "NAME"),   # "Hsing"
            (24, 28, "NAME"),   # "rice"
            (29, 36, "NAME"),   # "cooking"
            (37, 41, "NAME"),   # "wine"
            (43, 61, "COMMENT") # "or pale dry sherry"
        ]
    }),
    ("3/4 cup roasted salted cashews (4 ounces)", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "PREP"), (16, 22, "PREP"),
            (23, 30, "NAME"), (32, 41, "COMMENT")
        ]
    }),
    ("3.5 ounces vodka or gin", {
        "entities": [
            (0, 3, "QTY"), (4, 10, "UNIT"), (11, 16, "NAME"), (17, 23, "COMMENT")
        ]
    }),
    ("1/2 ounce dry vermouth", {
        "entities": [
            (0, 3, "QTY"),     # "1/2"
            (4, 9, "UNIT"),    # "ounce"
            (10, 13, "NAME"),  # "dry" (or PREP/COMMENT)
            (14, 22, "NAME")   # "vermouth"
        ]
    }),
    ("2 1/2 ounces gin", {
        "entities": [
            (0, 5, "QTY"),     # "2 1/2"
            (6, 12, "UNIT"),   # "ounces"
            (13, 16, "NAME")   # "gin"
        ]
    }),
    ("1 can (15 ounces) black beans, rinsed and drained", {"entities": [
        (0,1,"QTY"), (2,5,"UNIT"), (7,9,"QTY"), (10,16,"UNIT"),
        (18,23,"NAME"), (24,29,"NAME"), (31,37,"PREP"), (42,49,"PREP")
    ]}),
    ("1 large yellow squash about 8 ounces quartered lengthwise and sliced", {"entities": [
        (0,1,"QTY"), (2,7,"UNIT"),
        (8,14,"NAME"),(15,21,"NAME"), (22,27,"NAME"), (28,29,"NAME"), (30,36,"NAME"),
        (37,46,"PREP"), (47,57,"PREP"), (62,68,"PREP")
    ]}),
    ("Salt and pepper to taste", {"entities": [(0,4,"NAME"),(5,8,"NAME"),(9,15,"NAME"),(16,24,'COMMENT')]}),
    ("chopped parsley", {"entities": [(0,7,"NAME"),(8,15,"NAME")]}),
    ("2 tablespoons unsalted butter melted cooled plus more for brushing", {"entities": [
        (0,1,"QTY"),        # "2"
        (2,13,"UNIT"),      # "tablespoons" (len 11, 2+11=13)
        (14,22,"NAME"),     # "unsalted" (len 8, 14+8=22)
        (23,29,"NAME"),     # "butter" (len 6, 23+6=29)
        (30,36,"PREP"),     # "melted" (len 6, 30+6=36)
        (37,43,"PREP"),     # "cooled" (len 6, 37+6=43)
        (44,48,"COMMENT"),  # "plus" (len 4, 44+4=48)
        (49,53,"COMMENT"),  # "more" (len 4, 49+4=53)
        (54,57,"COMMENT"),  # "for" (len 3, 54+3=57)
        (58,66,"COMMENT")   # "brushing" (len 8, 58+8=66)
    ]}),
    ("20 clams, cleaned", {"entities": [(0,2,"QTY"),(3,8,"NAME"),(10,17,"PREP")]}),
    ("20 mussels, de-bearded and cleaned", {"entities": [
        (0,2,"QTY"), (3,10,"NAME"), (12,22,"PREP"), (27,34,"PREP") # Corrected
    ]}),
    ("40 small calamari rings, cleaned", {"entities": [
        (0,2,"QTY"),(3,8,"UNIT"), (9,17,"NAME"), (18,23,"NAME"), (25,32,"PREP")
    ]}),
    # TO BE ADDED or MODIFIED (ensure it's for the exact string)
    ("40 small rings of calamari, cleaned", {"entities": [
        (0,2,"QTY"),    # "40"
        (3,8,"UNIT"),   # "small"
        (9,14,"PREP"),  # "rings"
        (15,17,"PREP"), # "of"
        (18,26,"NAME"), # "calamari"
        (28,35,"PREP")  # "cleaned"
    ]}),
    ("4 cups (960 ml) vegetable or chicken broth", {"entities": [
        (0,1,"QTY"),        # "4"
        (2,6,"UNIT"),       # "cups"
        (8,15,"COMMENT"),   # "(960 ml)"
        (16,25,"COMMENT"),  # "vegetable" (Tag as COMMENT to exclude from primary name)
        # "or" (26,28) will be O (Outside)
        (29,36,"NAME"),     # "chicken"
        (37,42,"NAME")      # "broth"
    ]}),
    ("16 tiger shrimp, peeled and deveined", {"entities": [
        (0,2,"QTY"),(3,8,"NAME"),(9,15,"NAME"),(17,23,"PREP"),(28,36,"PREP")
    ]}),
    ("1/4 cup extra-virgin olive oil", {"entities": [(0,3,"QTY"),(4,7,"UNIT"),(8,20,"NAME"),(21,26,"NAME"),(27,30,"NAME")]}),
    ("2 teaspoons chopped garlic", {"entities": [(0,1,"QTY"),(2,11,"UNIT"),(12,19,"NAME"),(20,26,"NAME")]}),
    ("1/4 cup italian parsley leaves, divided", {"entities": [(0,3,"QTY"),(4,7,"UNIT"),(8,15,"NAME"),(16,23,"NAME"),(24,30,"COMMENT"),(32,39,"PREP")]}),
    ("1/8 teaspoon sea salt", {"entities": [(0,3,"QTY"),(4,12,"UNIT"),(13,16,"NAME"),(17,21,"NAME")]}),
    ("1/4 teaspoon crushed red pepper", {"entities": [(0,3,"QTY"),(4,12,"UNIT"),(13,20,"PREP"),(21,24,"NAME"),(25,31,"NAME")]}),
    ("1 cup Pinot Grigio wine", {"entities": [
        (0,1,"QTY"),(2,5,"UNIT"),(6,11,"NAME"),
        (12,18,"NAME"),(19,23,"NAME") # Corrected
    ]}),    ("2 cups tomato sauce", {"entities": [(0,1,"QTY"),(2,6,"UNIT"),(7,13,"NAME"),(14,19,"NAME")]}),
    ("1 (1-pound) box dried spaghetti", {"entities": [
        (0,1,"QTY"), (3,10,"COMMENT"), (12,15,"NAME"), (16,21,"NAME"), (22,31,"NAME")
    ]}),
    ("1 (200 g) large leek, cleaned, sliced ¼-inch-(.6 cm) thick", {"entities": [
        (0,1,"QTY"),        # "1"
        (3,9,"COMMENT"),    # "200 g)" -> text[3:9] (covers tokens '200', 'g', ')')
        (10,15,"UNIT"),     # "large" -> text[10:15]
        (16,20,"NAME"),     # "leek" -> text[16:20]
        (22,29,"PREP"),     # "cleaned" -> text[22:29]
        (31,37,"PREP"),     # "sliced" -> text[31:37]
        (38,52,"COMMENT"),  # "¼-inch-(.6 cm)" -> text[38:52] (covers '¼-inch-(.6', 'cm', ')')
        (53,58,"PREP")      # "thick" -> text[53:58]
    ]}),
    ("6 cups (335 g) fresh kale, chopped, stems removed", {"entities": [
        (0,1,"QTY"),        # "6"
        (2,6,"UNIT"),       # "cups"
        (8,14,"COMMENT"),   # "335 g)" -> text[8:14] (covers '335', 'g', ')')
        (15,20,"NAME"),     # "fresh" -> text[15:20]
        (21,25,"NAME"),     # "kale" -> text[21:25]
        (27,34,"PREP"),     # "chopped" -> text[27:34]
        (36,41,"PREP"),     # "stems" -> text[36:41]
        (42,49,"PREP")      # "removed" -> text[42:49]
    ]}),

    (
        "1 small bunch swiss chard or mustard greens stems removed leaves chopped",
        {
            "entities": [
                (0, 1, "QTY"),        # "1"
                (2, 7, "UNIT"),    # "small"
                (8, 13, "UNIT"),      # "bunch"
                (14, 19, "NAME"),     # "swiss"
                (20, 25, "NAME"),     # "chard"
                (26, 43, "ALT_NAME"), # "or mustard greens" - This is the key change
                (44, 49, "PREP"),     # "stems"
                (50, 57, "PREP"),     # "removed"
                (58, 64, "PREP"),     # "leaves"
                (65, 72, "PREP"),     # "chopped"
            ]
        },
    ),

    ("4 cups (960 ml) vegetable broth", {"entities": [
        (0,1,"QTY"),        # "4"
        (2,6,"UNIT"),       # "cups"
        (8,15,"COMMENT"),   # "960 ml)" -> text[8:15] (covers '960', 'ml', ')')
        (16,25,"NAME"),     # "vegetable" -> text[16:25]
        (26,31,"NAME")      # "broth" -> text[26:31]
    ]}),
    ("4 Japanese eggplants, cut in half lengthwise", {"entities": [
        (0,1,"QTY"), (2,10,"NAME"),(11,20,"NAME"),
        (22,25,"PREP"),(26,28,"PREP"),(29,33,"PREP"),(34,44,"PREP")
    ]}),
    ("4 Japanese eggplant, halved lengthwise", {"entities": [
        (0,1,"QTY"),(2,10,"NAME"),(11,19,"NAME"), (21,27,"PREP"),(28,38,"PREP")
    ]}),
    ("4 Japanese eggplant, sliced lengthwise", {"entities": [
        (0,1,"QTY"),(2,10,"NAME"),(11,19,"NAME"), (21,27,"PREP"),(28,38,"PREP")
    ]}),

    # Alternative for "1-ounce Rose's lime juice" if "1" is the core QTY:
    ("1-ounce Rose's lime juice", {
        "entities": [
            (0, 1, "QTY"),      # "1"
            (2, 7, "UNIT"),     # "ounce"
            (8, 14, "NAME"),    # "Rose's"
            (15, 19, "NAME"),   # "lime"
            (20, 25, "NAME")    # "juice"
        ]
    }), # Choose one annotation for this example based on your preference

    ("Lemon or lime twist for garnish", { # "or lime twist" could be ALT_NAME or part of COMMENT
        "entities": [
            (0, 5, "NAME"),       # "Lemon"
            (6, 19, "ALT_NAME"),  # "or lime twist" (treating as an alternative or a combined option)
            (20, 31, "COMMENT")   # "for garnish"
        ]
    }),


    ("2 ounces mandarin-orange-flavored vodka", {
        "entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 33, "NAME"),   # "mandarin-orange-flavored"
            (34, 39, "NAME")   # "vodka"
        ]
    }),

    ("5 tablespoons passion fruit liqueur (reccomended: Alize)", {
        "entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 21, "NAME"),
            (22, 27, "NAME"),
            (28, 35, "NAME"),     # "liqueur"
            (36, 56, "COMMENT")   # "(reccomended: Alize)"
        ]
    }),
    ("2 pounds milk chocolate, tempered", {
        "entities": [
            (0, 1, "QTY"),        # "2"
            (2, 8, "UNIT"),       # "pounds"
            (9, 13, "NAME"),      # "milk"
            (14, 23, "NAME"),     # "chocolate"
            (25, 33, "PREP")      # "tempered"
        ]
    }),
    # ("3.5 ounces/100 g butter", { # Handle dual units as separate comments or one combined comment
    #     "entities": [
    #         (0, 3, "QTY"),        # "3.5"
    #         (4, 10, "UNIT"),      # "ounces"
    #         (10, 17, "COMMENT"),  # "/100 g" (the alternative unit as a comment)
    #         (18, 24, "NAME")      # "butter"
    #     ]
    # }),
    # ("3.5 ounces/100 g sugar", {
    #     "entities": [
    #         (0, 3, "QTY"),
    #         (4, 10, "UNIT"),
    #         (10, 17, "COMMENT"),
    #         (18, 23, "NAME")
    #     ]
    # }),
    # ("7 ounces/200 g chopped semisweet dark chocolate", {
    #     "entities": [
    #         (0, 1, "QTY"),        # "7"
    #         (2, 8, "UNIT"),       # "ounces"
    #         (8, 15, "COMMENT"),  # "/200 g"
    #         (16, 23, "PREP"),     # "chopped"
    #         (24, 33, "NAME"),     # "semisweet" (or PREP)
    #         (34, 38, "NAME"),     # "dark" (or PREP)
    #         (39, 48, "NAME")      # "chocolate"
    #     ]
    # }),
    ("Icing (confectioners') sugar, for sprinkling", {
        "entities": [
            (0, 5, "NAME"),        # "Icing"
            (6, 22, "COMMENT"),    # "(confectioners')" - including the closing parenthesis
            (23, 28, "NAME"),      # "sugar"
            (30, 44, "COMMENT")    # "for sprinkling"
        ]
    }),
    ("1 head broccoli", {
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),
            (7, 15, "NAME")
        ]
    }),
    ("Fresh berries and whipped topping, for serving", {
        "entities": [
            (0, 5, "PREP"),
            (6, 13, "NAME"),
            (18, 25, "PREP"),
            (26, 33, "NAME"),
            (35, 46, "COMMENT")   # "for serving"
        ]
    }),
    ("3 cups lemonade", {
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),
            (7, 15, "NAME")
        ]
    }),
    ("4 egg yolks", {
        "entities": [
            (0, 1, "QTY"),
            (2, 5, "NAME"), # "egg"
            (6, 11, "NAME") # "yolks" (or treat "egg yolks" as one NAME)
        ]
    }),
    # Alternative for "4 egg yolks"
    # ("4 egg yolks", {"entities": [(0, 1, "QTY"), (2, 11, "NAME")]}),

    ("1 (15-ounce) box unroll and bake pie crusts (recommended: Pillsbury)", {
        "entities": [
            (0, 1, "QTY"),        # "1"
            (2, 12, "COMMENT"),   # "(15-ounce)"
            (13, 16, "UNIT"),     # "box"
            (17, 23, "PREP"),     # "unroll" (could be part of product NAME if it's "Unroll and Bake Pie Crusts")
            (28, 32, "PREP"),     # "bake"
            (33, 36, "NAME"),     # "pie"
            (37, 43, "NAME"),     # "crusts"
            (44, 68, "COMMENT")   # "(recommended: Pillsbury)"
        ]
    }),


    ("1 (4.3-ounce) box lemon pudding mix (recommended: Jell-O cook and serve)", {
        "entities": [
            (0, 1, "QTY"),
            (2, 13, "COMMENT"),   # "(4.3-ounce)" - This aligns based on tokens
            (14, 17, "UNIT"),
            (18, 23, "NAME"),
            (24, 31, "NAME"),
            (32, 35, "NAME"),
            (36, 72, "COMMENT")   # "(recommended: Jell-O cook and serve)"
        ]
    }),
    ("6 ounces bittersweet chocolate", {
        "entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 20, "NAME"),      # "bittersweet" (or PREP)
            (21, 30, "NAME")      # "chocolate"
        ]
    }),
    ("2 teaspoons finely shredded orange peel", {
        "entities": [
            (0, 1, "QTY"),
            (2, 11, "UNIT"),      # "teaspoons"
            (12, 18, "PREP"),     # "finely"
            (19, 27, "PREP"),     # "shredded"
            (28, 34, "NAME"),     # "orange"
            (35, 39, "NAME")      # "peel"
        ]
    }),
    ("Four 6-ounce swordfish steaks", { # "Four" is QTY, "6-ounce" is COMMENT describing steaks
        "entities": [
            (0, 4, "QTY"),        # "Four"
            (5, 12, "COMMENT"),   # "6-ounce"
            (13, 22, "NAME"),     # "swordfish"
            (23, 29, "UNIT")      # "steaks" (acting as a unit here)
        ]
    }),
    ("2 ripe mangoes, peeled and cut into large wedges", {
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "PREP"),
            (7, 14, "NAME"),      # "mangoes"
            (16, 22, "PREP"),     # "peeled"
            (27, 30, "PREP"),     # "cut"
            (31, 35, "PREP"),     # "into"
            (36, 41, "UNIT"),     # "large"
            (42, 48, "PREP")      # "wedges"
        ]
    }),
    ("2 bunches scallions, trimmed", {
        "entities": [
            (0, 1, "QTY"),
            (2, 9, "UNIT"),
            (10, 19, "NAME"),
            (21, 28, "PREP")
        ]
    }),
    ("2 Cornish game hens (1 1/2 to 1 3/4 pounds each)", {
        "entities": [
            (0, 1, "QTY"),        # "2"
            (2, 9, "NAME"),       # "Cornish"
            (10, 14, "NAME"),     # "game"
            (15, 19, "NAME"),     # "hens"
            (20, 47, "COMMENT")   # "(1 1/2 to 1 3/4 pounds each)"
        ]
    }),
    ("2 to 3 pounds boneless chicken cut into chunks (I prefer thigh meat)", {
        "entities": [
            (0, 6, "QTY"), (7, 13, "UNIT"), (14, 22, "PREP"), (23, 30, "NAME"),
            (31, 34, "PREP"), (35, 39, "PREP"), (40, 46, "PREP"),
            (47, 68, "COMMENT")   # "(I prefer thigh meat)"
        ]
    }),
    ("Sambal oelek, to taste (hot chili paste from Asian grocery section)", {
        "entities": [
            (0, 6, "NAME"),       # "Sambal"
            (7, 12, "NAME"),      # "oelek"
            (14, 22, "COMMENT"),  # "to taste"
            (23, 66, "COMMENT")   # "(hot chili paste from Asian grocery section)"
        ]
    }),
    ("1 large bunch collard or other greens, chopped fairly finely and after removing center ribs (frozen, drained greens can be used as a substitute)", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "UNIT"), (14, 21, "NAME"), # "collard"
            (22, 37, "ALT_NAME"), # "or other greens"
            # Comma at 37
            (39, 46, "PREP"),     # "chopped"
            (47, 53, "PREP"),     # "fairly"
            (54, 60, "PREP"),     # "finely"
            # "and" at 61
            (65, 86, "PREP"),     # "after removing center" (or break down further if needed)
            (87, 91, "PREP"),     # "ribs" (part of "removing center ribs")
            (92, 144, "COMMENT")  # "(frozen, drained greens can be used as a substitute)"
        ]
    }),
    ("2 tablespoons reserved spice mixture, from above", {
        "entities": [
            (0, 1, "QTY"), (2, 13, "UNIT"), (14, 22, "PREP"), (23, 28, "NAME"),
            (29, 36, "NAME"),
            (38, 48, "COMMENT")   # "from above"
        ]
    }),
    ("1/2 cup finely chopped green onions", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 14, "PREP"),     # "finely"
            (15, 22, "PREP"),     # "chopped"
            (23, 28, "NAME"),     # "green"
            (29, 35, "NAME")      # "onions"
        ]
    }),
    ("2 quarts broth (chicken, pork or veggie)", {
        "entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 14, "NAME"),      # "broth"
            (15, 39, "COMMENT")   # "(chicken, pork or veggie)"
        ]
    }),
    ("1 leek, washed and halved", {
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "NAME"),
            (8, 14, "PREP"),      # "washed"
            (19, 25, "PREP")      # "halved"
        ]
    }),
    ("2 cups chicken or beef stock", {
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),
            (7, 14, "NAME"),      # "chicken"
            (15, 22, "ALT_NAME"), # "or beef"
            (23, 28, "NAME")      # "stock"
        ]
    }),
    ("1 tablespoon chopped, fresh chives, plus 1 teaspoon for the sauce", { # Example 99
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"), (13, 20, "PREP"), (22, 27, "PREP"),
            (28, 34, "NAME"),
            (36, 65, "COMMENT")   # "plus 1 teaspoon for the sauce"
        ]
    }),
    ("1 tablespoon chopped, fresh thyme leaves, plus 1 teaspoon for the sauce", { # Example 100
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"), (13, 20, "PREP"), (22, 27, "PREP"),
            (28, 33, "NAME"), (34, 40, "NAME"),
            (42, 71, "COMMENT")   # "plus 1 teaspoon for the sauce" (char_idx of 'plus' is 42)
        ]
    }),
    ("1 tablespoon chopped, fresh Italian parsley, plus 1 teaspoon for the sauce", { # Example 101
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"), (13, 20, "PREP"), (22, 27, "PREP"),
            (28, 35, "NAME"), (36, 43, "NAME"),
            (45, 74, "COMMENT")   # "plus 1 teaspoon for the sauce" (char_idx of 'plus' is 45)
        ]
    }),
    ("1 tablespoon freshly ground black pepper", {
        "entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),
            (13, 20, "PREP"),     # "freshly"
            (21, 27, "PREP"),     # "ground"
            (28, 33, "NAME"),     # "black"
            (34, 40, "NAME")      # "pepper"
        ]
    }),
    ("1/2 pound ground pork (Don't get lean pork, the fat is good for juicy and flavorful dumplings)", {
        "entities": [
            (0, 3, "QTY"), (4, 9, "UNIT"), (10, 16, "PREP"), (17, 21, "NAME"),
            (22, 94, "COMMENT") # Corrected
        ]
    }),
    # Add these to your EXISTING_TRAIN_DATA list in ingredient_parser_trainer.py

    ("1 tablespoon (42 grams) honey", {
        "entities": [
            (0, 1, "QTY"),         # "1"
            (2, 12, "UNIT"),       # "tablespoon"
            (13, 23, "COMMENT"),   # "(42 grams)"
            (24, 29, "NAME")       # "honey"
        ]
    }),
    ("Sea salt and freshly ground black pepper", { # This was split by "and" in your original parser
        # For NER training, if they are distinct, list them separately.
        # Or if "Sea salt and freshly ground black pepper" is one common seasoning:
        "entities": [
            (0, 3, "NAME"),       # "Sea"
            (4, 8, "NAME"),       # "salt"
            # "and" is O
            (13, 20, "PREP"),     # "freshly"
            (21, 27, "PREP"),     # "ground"
            (28, 33, "NAME"),     # "black"
            (34, 40, "NAME")      # "pepper"
        ]
    }),
    # If you prefer to train on them as separate lines (as your old parser would have made them):
    # ("Sea salt", {"entities": [(0,3,"NAME"),(4,8,"NAME")]}),
    # ("freshly ground black pepper", {"entities": [(0,7,"PREP"),(8,14,"PREP"),(15,20,"NAME"),(21,27,"NAME")]}),

    ("2 cups leftover spaghetti with olives and tomato sauce, recipe follows", {
        "entities": [
            (0, 1, "QTY"),        # "2"
            (2, 6, "UNIT"),       # "cups"
            (7, 15, "PREP"),      # "leftover"
            (16, 25, "NAME"),     # "spaghetti"
            (26, 30, "PREP"),     # "with"
            (31, 37, "NAME"),     # "olives"
            (38, 41, "PREP"),     # "and" (or could be O, if "olives" and "tomato sauce" are separate components)
            (42, 48, "NAME"),     # "tomato"
            (49, 54, "NAME"),     # "sauce"
            (56, 70, "COMMENT")   # "recipe follows"
        ]
    }),
    ("1/2 tablespoon red pepper flakes, plus more if desired", {
        "entities": [
            (0, 3, "QTY"), (4, 14, "UNIT"), (15, 18, "NAME"), (19, 25, "NAME"),
            (26, 32, "NAME"),
            (34, 54, "COMMENT")   # "plus more if desired"
        ]
    }),
    ("1/2 small bulb of fennel, halved, cored and thinly sliced into half-moons (about 1 cup)", {
        "entities": [
            (0, 3, "QTY"), (4, 9, "UNIT"), (10, 14, "UNIT"), (15, 17, "PREP"),
            (18, 24, "NAME"), (26, 32, "PREP"), (34, 39, "PREP"), (44, 50, "PREP"),
            (51, 57, "PREP"), (58, 62, "PREP"), (63, 73, "PREP"), # "half-moons" (63-67 'half', 67-68 '-', 68-73 'moons')
            (74, 87, "COMMENT")   # "(about 1 cup)"
        ]
    }),
    # Note: The duplicate "1/2 small bulb of fennel..." is omitted assuming it was a copy-paste error.
    # If it's a distinct example, add it with its own annotation.

    ("3/4 cup sliced almonds, coarsely chopped", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 14, "PREP"),      # "sliced"
            (15, 22, "NAME"),     # "almonds"
            (24, 32, "PREP"),     # "coarsely"
            (33, 40, "PREP")      # "chopped"
        ]
    }),
    ("1/2 teaspoon ground caraway", {
        "entities": [
            (0, 3, "QTY"),
            (4, 12, "UNIT"),
            (13, 19, "PREP"),
            (20, 27, "NAME")
        ]
    }),
    ("6 slices center cut bacon", {
        "entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 15, "PREP"),      # "center"
            (16, 19, "PREP"),     # "cut"
            (20, 25, "NAME")      # "bacon"
        ]
    }),
    ("16 cups, plus 1 cup water", {
        "entities": [
            (0, 2, "QTY"),
            (3, 7, "UNIT"),
            (9, 25, "COMMENT")    # "plus 1 cup water"
        ]
    }),
    ("4 carrots", {"entities": [(0, 1, "QTY"), (2, 9, "NAME")]}),
    ("3 onions", {"entities": [(0, 1, "QTY"), (2, 8, "NAME")]}),
    ("2 large leeks", {"entities": [(0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "NAME")]}),
    ("4 celery stalks", {
        "entities": [
            (0, 1, "QTY"),
            (2, 8, "NAME"),      # "celery"
            (9, 15, "UNIT")       # "stalks" (acts as a unit)
        ]
    }),
    ("1 whole turkey breast, approximately 1 1/2 to 2 pounds", {
        "entities": [
            (0, 1, "QTY"),        # "1"
            (2, 7, "PREP"),       # "whole"
            (8, 14, "NAME"),      # "turkey"
            (15, 21, "NAME"),     # "breast"
            (23, 54, "COMMENT")   # "approximately 1 1/2 to 2 pounds"
        ]
    }),
    ("2/3 tablespoon marjoram", {
        "entities": [
            (0, 3, "QTY"),
            (4, 14, "UNIT"),
            (15, 23, "NAME")
        ]
    }),
    ("Generous pinch coarsely ground black pepper", { # "Generous pinch" is QTY/UNIT
        "entities": [
            (0, 8, "QTY"),        # "Generous" (word quantity)
            (9, 14, "UNIT"),      # "pinch"
            (15, 23, "PREP"),     # "coarsely"
            (24, 30, "PREP"),     # "ground"
            (31, 36, "NAME"),     # "black"
            (37, 43, "NAME")      # "pepper"
        ]
    }),
    ("1/4 cup sliced almonds, toasted, for garnish", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 14, "PREP"),
            (15, 22, "NAME"),
            (24, 31, "PREP"),     # "toasted"
            (33, 44, "COMMENT")   # "for garnish"
        ]
    }),
    ("7 ounces (1 3/4 sticks) butter, softened, plus 1 tablespoon for greasing the loaf pan", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 23, "COMMENT"), (24, 30, "NAME"),
            (32, 40, "PREP"),
            (42, 85, "COMMENT") # "plus 1 tablespoon for greasing the loaf pan"
        ]
    }),
    ("2/3 cup sliced almonds, toasted", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 14, "PREP"),
            (15, 22, "NAME"),
            (24, 31, "PREP")      # "toasted"
        ]
    }),
    ("1 cup shredded smoked gouda", {
        "entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 14, "PREP"),      # "shredded"
            (15, 21, "PREP"),     # "smoked" (descriptor, could be part of NAME)
            (22, 27, "NAME")      # "gouda"
        ]
    }),
    ("1 bunch watercress, stemmed", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),
            (8, 18, "NAME"),
            (20, 27, "PREP")      # "stemmed"
        ]
    }),
    ("1 head radicchio, chopped", {
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),
            (7, 16, "NAME"),
            (18, 25, "PREP")
        ]
    }),
    ("1 teaspoon chopped oregano leaves", {
        "entities": [
            (0, 1, "QTY"),
            (2, 10, "UNIT"),
            (11, 18, "PREP"),
            (19, 26, "NAME"),     # "oregano"
            (27, 33, "NAME")      # "leaves"
        ]
    }),
    ("1 large loaf of Cuban bread, cut into 4 equal pieces crosswise", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 12, "UNIT"), (13, 15, "PREP"),
            (16, 21, "NAME"), (22, 27, "NAME"),
            (29, 62, "PREP")      # "cut into 4 equal pieces crosswise"
        ]
    }),
    ("1 teaspoon freshly ground canela (cinnamon)", {
        "entities": [
            (0, 1, "QTY"), (2, 10, "UNIT"), (11, 18, "PREP"), (19, 25, "PREP"),
            (26, 32, "NAME"),
            (33, 43, "COMMENT")   # "(cinnamon)"
        ]
    }),
    ("2 tablespoons ground cumin", {
        "entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 20, "NAME"),
            (21, 26, "NAME")
        ]
    }),
    ("1 teaspoon oregano, dried", {
        "entities": [
            (0, 1, "QTY"),
            (2, 10, "UNIT"),
            (11, 18, "NAME"),
            (20, 25, "PREP")
        ]
    }),
    ("1 avocado, peeled and cubed", {
        "entities": [
            (0, 1, "QTY"),
            (2, 9, "NAME"),
            (11, 17, "PREP"),
            (22, 27, "PREP")
        ]
    }),
    ("1 ear corn, kernels removed and roasted until some of the kernels start to brown", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"), (6, 10, "NAME"),
            (12, 80, "PREP")      # "kernels removed and roasted until some of the kernels start to brown"
        ]
    }),
    ("12 cornichons", {"entities": [(0, 2, "QTY"), (3, 13, "NAME")]}),
    ("12 slider buns", {"entities": [(0, 2, "QTY"), (3, 9, "NAME"), (10, 14, "NAME")]}),
    ("About 1 pound (500g) farmed ground New Zealand venison (any cut will do but the most cost effective is from the leg)", {
        "entities": [
            (0, 5, "COMMENT"),    # "About"
            (6, 7, "QTY"),        # "1"
            (8, 13, "UNIT"),      # "pound"
            (14, 20, "COMMENT"),  # "(500g)"
            (21, 27, "PREP"),     # "farmed"
            (28, 34, "PREP"),     # "ground"
            (35, 38, "NAME"),     # "New"
            (39, 46, "NAME"),     # "Zealand"
            (47, 54, "NAME"),     # "venison"
            (55, 116, "COMMENT")  # "(any cut will do but the most cost effective is from the leg)"
        ]
    }),
    ("1 thumb fresh ginger, peeled and grated", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "thumb"
            (8, 13, "PREP"),      # "fresh"
            (14, 20, "NAME"),     # "ginger"
            (22, 28, "PREP"),
            (33, 39, "PREP")
        ]
    }),
    ("1 teaspoon ground cumin", {"entities": [(0,1,"QTY"),(2,10,"UNIT"),(11,17,"NAME"),(18,23,"NAME")]}), # Duplicate
    ("1 tablespoon cumin", {"entities": [(0,1,"QTY"),(2,12,"UNIT"),(13,18,"NAME")]}), # Duplicate (different QTY/UNIT)
    ("1 sprig thyme", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),
            (8, 13, "NAME")
        ]
    }),
    ("3 shallots, slice thin", {
        "entities": [
            (0, 1, "QTY"),
            (2, 10, "NAME"),
            (12, 17, "PREP"),     # "slice"
            (18, 22, "PREP")      # "thin"
        ]
    }),
    ("5 1/2 pounds bones and trimmings from white fish", {
        "entities": [
            (0, 5, "QTY"),        # "5 1/2"
            (6, 12, "UNIT"),      # "pounds"
            (13, 18, "NAME"),     # "bones"
            (19, 22, "PREP"),     # "and" (or O)
            (23, 32, "NAME"),     # "trimmings"
            (33, 37, "PREP"),     # "from"
            (38, 43, "NAME"),     # "white"
            (44, 48, "NAME")      # "fish"
        ]
    }),
    ("1 pound large shrimp, peeled and deveined, tails left on", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),
            (8, 13, "UNIT"),      # "large"
            (14, 20, "NAME"),
            (22, 28, "PREP"),
            (33, 41, "PREP"),
            (43, 48, "PREP"),     # "tails"
            (49, 53, "PREP"),     # "left"
            (54, 56, "PREP")      # "on"
        ]
    }),
    ("1 tablespoon toasted fennel seed", {
        "entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),
            (13, 20, "PREP"),
            (21, 27, "NAME"),
            (28, 32, "NAME")
        ]
    }),
    ("1 head fennel", {"entities": [(0,1,"QTY"),(2,6,"UNIT"),(7,13,"NAME")]}), # Duplicate
    ("1/2 pound clam base", {
        "entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),
            (10, 14, "NAME"),
            (15, 19, "NAME")
        ]
    }),
    ("3 (46-ounce) cans clam juice", {
        "entities": [
            (0, 1, "QTY"),
            (2, 12, "COMMENT"),   # "(46-ounce)"
            (13, 17, "UNIT"),     # "cans"
            (18, 22, "NAME"),
            (23, 28, "NAME")
        ]
    }),
    ("7 onions", {"entities": [(0,1,"QTY"),(2,8,"NAME")]}), # Duplicate
    ("4 small clams or 3 large clams", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "NAME"),
            (14, 30, "ALT_NAME")  # "or 3 large clams"
        ]
    }),
    ("2 ounces crabmeat or 3 crab legs", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 17, "NAME"),
            (18, 32, "ALT_NAME")  # "or 3 crab legs"
        ]
    }),
    ("2 tablespoons chopped oregano leaves", {"entities": [(0,1,"QTY"),(2,13,"UNIT"),(14,21,"PREP"),(22,29,"NAME"),(30,36,"NAME")]}), # Duplicate
    ("4 quenelle scoops of coconut ice cream (If coconut ice cream is not available, fold toasted coconut, 1 tablespoon Malabu Rum, with softened vanilla ice cream)", {
        "entities": [
            (0, 1, "QTY"), (2, 10, "PREP"), (11, 17, "UNIT"), (18, 20, "PREP"),
            (21, 28, "NAME"), (29, 32, "NAME"), (33, 38, "NAME"),
            (39, 158, "COMMENT")
        ]
    }),
    ("Juice of one lemon", { # "one" as QTY
        "entities": [
            (0, 5, "NAME"),       # "Juice" (or PREP if action "Juice the lemon")
            (6, 8, "PREP"),       # "of"
            (9, 12, "QTY"),       # "one"
            (13, 18, "NAME")      # "lemon"
        ]
    }),
    ("3 tablespoons small diced quava", {
        "entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 19, "PREP"),     # "small" (describing dice size)
            (20, 25, "PREP"),     # "diced"
            (26, 31, "NAME")      # "quava" -> guava?
        ]
    }),
    ("3 tablespoons small diced pineapple", {
        "entities": [
            (0, 1, "QTY"),(2,13,"UNIT"),(14,19,"PREP"),(20,25,"PREP"),(26,35,"NAME")
        ]
    }),
    ("3 tablespoons small diced mango", {
        "entities": [
            (0,1,"QTY"),(2,13,"UNIT"),(14,19,"PREP"),(20,25,"PREP"),(26,31,"NAME")
        ]
    }),
    ("3 tablespoons small diced papayas", {
        "entities": [
            (0,1,"QTY"),(2,13,"UNIT"),(14,19,"PREP"),(20,25,"PREP"),(26,33,"NAME")
        ]
    }),
    ("12 cold, freshly opened oysters", {
        "entities": [
            (0, 2, "QTY"),
            (3, 7, "PREP"),       # "cold"
            (9, 16, "PREP"),      # "freshly"
            (17, 23, "PREP"),     # "opened"
            (24, 31, "NAME")      # "oysters"
        ]
    }),
    ("About 4 ounces top-quality smoked salmon, sliced extremely thinly", {
        "entities": [
            (0, 5, "COMMENT"),    # "About"
            (6, 7, "QTY"),
            (8, 14, "UNIT"),
            (15, 26, "PREP"),     # "top-quality" (descriptor)
            (27, 33, "PREP"),     # "smoked"
            (34, 40, "NAME"),     # "salmon"
            (42, 48, "PREP"),     # "sliced"
            (49, 58, "PREP"),     # "extremely"
            (59, 65, "PREP")      # "thinly"
        ]
    }),
    ("12 cold, freshly opened oysters", {"entities": [(0,2,"QTY"),(3,7,"PREP"),(9,16,"PREP"),(17,23,"PREP"),(24,31,"NAME")]}), # Duplicate
    ("1 fresh jalapeno, diced, half seeded and deveined", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "PREP"),
            (8, 16, "NAME"),      # "jalapeno"
            (18, 23, "PREP"),     # "diced"
            (25, 29, "PREP"),     # "half"
            (30, 36, "PREP"),     # "seeded"
            (41, 49, "PREP")      # "deveined"
        ]
    }),
    ("1 tablespoon plus 1 teaspoon garlic powder", {
        "entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),
            (13, 28, "COMMENT"),  # "plus 1 teaspoon"
            (29, 35, "NAME"),     # "garlic"
            (36, 42, "NAME")      # "powder"
        ]
    }),
    # Add these to your EXISTING_TRAIN_DATA list in ingredient_parser_trainer.py

    ("1/4 cup kimchi, drained and coarsely chopped", {
        "entities": [
            (0, 3, "QTY"),        # "1/4"
            (4, 7, "UNIT"),       # "cup"
            (8, 14, "NAME"),      # "kimchi"
            (16, 23, "PREP"),     # "drained"
            # "and" is O
            (28, 36, "PREP"),     # "coarsely"
            (37, 44, "PREP")      # "chopped"
        ]
    }),
    ("1/4 cup apple cider", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 13, "NAME"),      # "apple"
            (14, 19, "NAME")      # "cider"
        ]
    }),
    ("2 Roma tomatoes", { # Countable, "2" is QTY, "Roma tomatoes" is NAME
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "NAME"),       # "Roma"
            (7, 15, "NAME")       # "tomatoes"
        ]
    }),
    ("1/4 cup fresh squeezed orange juice", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 13, "PREP"),      # "fresh"
            (14, 22, "PREP"),     # "squeezed"
            (23, 29, "NAME"),     # "orange"
            (30, 35, "NAME")      # "juice"
        ]
    }),
    ("1/4 cup beer", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 12, "NAME")
        ]
    }),
    ("One 8-inch sub roll or long roll, split", {
        "entities": [
            (0, 3, "QTY"),        # "One"
            (4, 10, "COMMENT"),   # "8-inch" (describes the roll)
            (11, 14, "NAME"),     # "sub"
            (15, 19, "NAME"),     # "roll"
            (20, 32, "ALT_NAME"), # "or long roll"
            (34, 39, "PREP")      # "split"
        ]
    }),
    ("6 feet all-natural hog casings", {
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),       # "feet"
            (7, 18, "PREP"),      # "all-natural" (descriptor)
            (19, 22, "NAME"),     # "hog"
            (23, 30, "NAME")      # "casings"
        ]
    }),
    ("2 cups shredded mozzarella", {
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),
            (7, 15, "PREP"),
            (16, 26, "NAME")
        ]
    }),
    ("One 24-ounce jar marinara sauce", {
        "entities": [
            (0, 3, "QTY"),        # "One"
            (4, 12, "COMMENT"),   # "24-ounce" (describes the jar)
            (13, 16, "UNIT"),     # "jar"
            (17, 25, "NAME"),     # "marinara"
            (26, 31, "NAME")      # "sauce"
        ]
    }),
    ("One 16-ounce box mezzi rigatoni or mezze penne", {
        "entities": [
            (0, 3, "QTY"), (4, 12, "COMMENT"), (13, 16, "UNIT"),
            (17, 22, "NAME"), (23, 31, "NAME"),
            (32, 46, "ALT_NAME")  # "or mezze penne"
        ]
    }),
    (".5 oz simple syrup", {
        "entities": [
            (0, 2, "QTY"),        # ".5"
            (3, 5, "UNIT"),       # "oz"
            (6, 12, "NAME"),      # "simple"
            (13, 18, "NAME")      # "syrup"
        ]
    }),
    ("1 large carrot, chopped", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "large"
            (8, 14, "NAME"),
            (16, 23, "PREP")
        ]
    }),
    ("1 cup half-and-half", {
        "entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 19, "NAME")      # "half-and-half"
        ]
    }),
    ("3/4 cup shredded part-skim mozzarella cheese", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 16, "PREP"),      # "shredded"
            (17, 26, "PREP"),     # "part-skim" (descriptor)
            (27, 37, "NAME"),     # "mozzarella"
            (38, 44, "NAME")      # "cheese"
        ]
    }),
    ("1 small shallot, peeled, trimmed and halved", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),
            (8, 15, "NAME"),
            (17, 23, "PREP"),
            (25, 32, "PREP"),
            (37, 43, "PREP")      # "halved"
        ]
    }),
    ("1 small garlic clove, peeled, trimmed and halved", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),
            (8, 14, "NAME"),      # "garlic"
            (15, 20, "NAME"),     # "clove"
            (22, 28, "PREP"),
            (30, 37, "PREP"),
            (42, 48, "PREP")
        ]
    }),
    ("1/2 teaspoon saffron threads", {
        "entities": [
            (0, 3, "QTY"),
            (4, 12, "UNIT"),
            (13, 20, "NAME"),
            (21, 28, "NAME")
        ]
    }),
    ("1 (5 to 6 pound) leg of lamb, trimmed of excess fat", {
        "entities": [
            (0, 1, "QTY"), (2, 16, "COMMENT"), (17, 20, "NAME"), (21, 23, "PREP"),
            (24, 28, "NAME"),
            (30, 51, "PREP")      # "trimmed of excess fat"
        ]
    }),
    ("1 tablespoon fresh oregano, chopped fine", {
        "entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),
            (13, 18, "PREP"),
            (19, 26, "NAME"),
            (28, 35, "PREP"),     # "chopped"
            (36, 40, "PREP")      # "fine"
        ]
    }),
    ("Pinch cayenne", { # "Pinch" is a QTY/UNIT
        "entities": [
            (0, 5, "UNIT"),       # "Pinch" (can be QTY if it's "A pinch")
            (6, 13, "NAME")       # "cayenne"
        ]
    }),
    # Alternative for "Pinch cayenne" if "Pinch" is considered a QTY:
    # ("Pinch cayenne", {"entities": [(0,5,"QTY"), (6,13,"NAME")]}),

    ("8 ounces tomatillo, papery husks removed, cut into 1/4-inch dice", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 18, "NAME"),
            (20, 40, "PREP"),     # "papery husks removed"
            (42, 64, "PREP")      # "cut into 1/4-inch dice"
        ]
    }),
    ("2 tablespoons pitted and finely chopped kalamata olives", {
        "entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 20, "PREP"),     # "pitted"
            (25, 31, "PREP"),     # "finely"
            (32, 39, "PREP"),     # "chopped"
            (40, 48, "NAME"),     # "kalamata"
            (49, 55, "NAME")      # "olives"
        ]
    }),
    ("1 tablespoon each vegetable and sesame oil", { # "each" implies two separate ingredients implicitly
        "entities": [
            (0, 1, "QTY"),        # "1"
            (2, 12, "UNIT"),      # "tablespoon"
            (13, 17, "COMMENT"),  # "each"
            (18, 27, "NAME"),     # "vegetable"
            # "and" is O
            (32, 38, "NAME"),     # "sesame"
            (39, 42, "NAME")      # "oil"
            # This annotation implies "1 tablespoon vegetable oil" AND "1 tablespoon sesame oil".
            # Your downstream parser would need to handle the "each".
            # Alternatively, break into two lines for training if that's how you want to parse it.
        ]
    }),
    ("1 tablespoon plus 2 teaspoons cornstarch", {
        "entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),
            (13, 29, "COMMENT"),  # "plus 2 teaspoons" (additional quantity aspect)
            (30, 40, "NAME")      # "cornstarch"
        ]
    }),
    ("1 tablespoon plus 1 teaspoon soy sauce", {
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"),
            (13, 28, "COMMENT"),  # "plus 1 teaspoon"
            (29, 32, "NAME"),     # "soy"
            (33, 38, "NAME")      # "sauce"
        ]
    }),
    ("Pinch crushed red pepper", {
        "entities": [
            (0, 5, "UNIT"),       # "Pinch"
            (6, 13, "PREP"),
            (14, 17, "NAME"),
            (18, 24, "NAME")
        ]
    }),
    ("Pinch sugar", {
        "entities": [
            (0, 5, "UNIT"),
            (6, 11, "NAME")
        ]
    }),
    ("1 tablespoon plus 1 teaspoon vegetable oil", {
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"),
            (13, 28, "COMMENT"),  # "plus 1 teaspoon"
            (29, 38, "NAME"),     # "vegetable"
            (39, 42, "NAME")      # "oil"
        ]
    }),
    ("1 medium carrot, thinly sliced", {
        "entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 15, "NAME"),
            (17, 23, "PREP"), # "thinly"
            (24, 30, "PREP")  # "sliced"
        ]
    }),
    ("1 bunch scallions, sliced, white and green parts kept separate", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 17, "NAME"), (19, 25, "PREP"),
            (27, 62, "COMMENT")   # "white and green parts kept separate"
        ]
    }),
    ("Pinch crushed red pepper", {"entities": [(0,5,"UNIT"),(6,13,"PREP"),(14,17,"NAME"),(18,24,"NAME")]}), # Duplicate
    ("2 teaspoons green peppercorns* (See Cook's Note", {
        "entities": [
            (0, 1, "QTY"), (2, 11, "UNIT"), (12, 17, "NAME"), (18, 30, "NAME"), # "peppercorns*"
            (31, 47, "COMMENT")   # "(See Cook's Note"
        ]
    }),
    ("1 cup seeded and chopped plum tomatoes", {
        "entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 12, "PREP"),      # "seeded"
            (17, 24, "PREP"),     # "chopped"
            (25, 29, "NAME"),     # "plum"
            (30, 38, "NAME")      # "tomatoes"
        ]
    }),
    ("2 quarts water", {
        "entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 14, "NAME")
        ]
    }),
    ("1/4 cup half-and-half", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 21, "NAME")
        ]
    }),
    ("1 teaspoon Szechwan peppercorns or 1/2 teaspoon cardamom seeds", {
        "entities": [
            (0, 1, "QTY"), (2, 10, "UNIT"), (11, 19, "NAME"), (20, 31, "NAME"),
            (32, 62, "ALT_NAME")  # "or 1/2 teaspoon cardamom seeds"
        ]
    }),
    ("2 ducks, about 5 pounds each, cavities cleaned, excess fat trimmed, rinsed and patted dry", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "NAME"),
            (9, 28, "COMMENT"),    # "about 5 pounds each"
            (30, 46, "PREP"),     # "cavities cleaned"
            (48, 66, "PREP"),     # "excess fat trimmed" (This looks okay from your original)
            (68, 74, "PREP"),     # "rinsed" (This looks okay)
            (79, 89, "PREP")      # "patted dry" (This looks okay)
        ]
    }),
    ("1/2 teaspoon sumac", {
        "entities": [
            (0, 3, "QTY"),
            (4, 12, "UNIT"),
            (13, 18, "NAME")
        ]
    }),
    ("1 medium red onion", {
        "entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 12, "NAME"), # "red"
            (13, 18, "NAME") # "onion"
        ]
    }),
    ("1 3-pound chicken, butterflied and lightly pounded for even thickness", {
        "entities": [
            (0, 1, "QTY"), (2, 9, "COMMENT"), (10, 17, "NAME"), (19, 30, "PREP"),
            (35, 69, "PREP")      # "lightly pounded for even thickness"
        ]
    }),
    ("1 head garlic, cloves separated and peeled", {
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),
            (7, 13, "NAME"),
            (15, 35, "PREP")      # "cloves separated and peeled"
        ]
    }),
    ("7 cups water", {"entities": [(0,1,"QTY"),(2,6,"UNIT"),(7,12,"NAME")]}), # Duplicate
    ("1 1/4 ounces cornstarch", {
        "entities": [
            (0, 5, "QTY"),        # "1 1/4"
            (6, 12, "UNIT"),
            (13, 23, "NAME")
        ]
    }),
    ("1 1/2 cups cornstarch", {
        "entities": [
            (0, 5, "QTY"),
            (6, 10, "UNIT"),
            (11, 21, "NAME")
        ]
    }),
    ("1 egg plus 2 egg yolks", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "NAME"),
            (6, 22, "COMMENT")    # "plus 2 egg yolks"
        ]
    }),
    ("1/3 cup cornstarch", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 18, "NAME")
        ]
    }),
    ("Pinch of salt", {
        "entities": [
            (0, 5, "UNIT"),       # "Pinch"
            (6, 8, "PREP"),       # "of"
            (9, 13, "NAME")       # "salt"
        ]
    }),
    ("1 8-ounce package cream cheese, at room temperature", {
        "entities": [
            (0, 1, "QTY"),
            (2, 9, "COMMENT"),   # "8-ounce"
            (10, 17, "UNIT"),    # "package"
            (18, 23, "NAME"),    # "cream"
            (24, 30, "NAME"),    # "cheese"
            (32, 51, "COMMENT")  # "at room temperature"
        ]
    }),
    ("1 8-ounce can crushed pineapple, drained", {
        "entities": [
            (0, 1, "QTY"),
            (2, 9, "COMMENT"),
            (10, 13, "UNIT"),
            (14, 21, "PREP"),
            (22, 31, "NAME"),
            (33, 40, "PREP")
        ]
    }),
    ("1 1/2 cups finely grated peeled carrots (use the small holes of a box grater)", {
        "entities": [
            (0, 5, "QTY"),
            (6, 10, "UNIT"),
            (11, 17, "PREP"),     # "finely"
            (18, 24, "PREP"),     # "grated"
            (25, 31, "PREP"),     # "peeled"
            (32, 39, "NAME"),     # "carrots"
            (40, 77, "COMMENT")   # "(use the small holes of a box grater)"
        ]
    }),
    ("1 tablespoon plus 1 teaspoon baking powder", {
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"),
            (13, 28, "COMMENT"),  # "plus 1 teaspoon"
            (29, 35, "NAME"),     # "baking"
            (36, 42, "NAME")      # "powder"
        ]
    }),
    ("2 cups pecan halves", {
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),
            (7, 12, "NAME"),
            (13, 19, "PREP")      # "halves" (or part of NAME: "pecan halves")
        ]
    }),
    # Alternative for "pecan halves" as one name:
    # ("2 cups pecan halves", {"entities": [(0,1,"QTY"),(2,6,"UNIT"),(7,19,"NAME")]}),
    ("1 tablespoon molasses", {
        "entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),
            (13, 21, "NAME")
        ]
    }),
    ("3 cups old-fashioned rolled oats", {
        "entities": [
            (0, 1, "QTY"), (2, 6, "UNIT"),
            (7, 20, "PREP"),      # "old-fashioned"
            (21, 27, "PREP"),     # "rolled"
            (28, 32, "NAME")      # "oats"
        ]
    }),
    ("4 ounces or 1/2 cup water", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"),
            (9, 19, "ALT_NAME"),  # "or 1/2 cup"
            (20, 25, "NAME")      # "water"
        ]
    }),
    ("2 green mangoes, peeled and julienned", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "NAME"),       # "green" (part of the name)
            (8, 15, "NAME"),      # "mangoes"
            (17, 23, "PREP"),
            (28, 37, "PREP")      # "julienned"
        ]
    }),
    ("1 long red chile, seeded and julienned", {
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),       # "long"
            (7, 10, "NAME"),      # "red"
            (11, 16, "NAME"),     # "chile"
            (18, 24, "PREP"),
            (29, 38, "PREP")
        ]
    }),
    ("1 cup Dashi, recipe follows (or 1 teaspoon instant dashi powder, such as Ajinomoto’s Hondashi, dissolved in 1 cup water)", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"), (6, 11, "NAME"), (13, 27, "COMMENT"),
            (28, 120, "COMMENT") # "(or 1 teaspoon ... water)"
        ]
    }),
    ("1/2 cup grated daikon radish, or to taste, lightly squeezed to remove excess liquid", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (15, 21, "NAME"), (22, 28, "NAME"),
            (30, 41, "COMMENT"),  # "or to taste"
            (43, 83, "PREP")      # "lightly squeezed to remove excess liquid"
        ]
    }),
    ("1 pound peeled and deveined large shrimp (see Cook’s Note), rinsed in cold water and thoroughly dried", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 14, "PREP"), (19, 27, "PREP"),
            (28, 33, "UNIT"), (34, 40, "NAME"), (41, 58, "COMMENT"),
            (60, 101, "PREP")     # "rinsed in cold water and thoroughly dried"
        ]
    }),
    ("1 3/4 cups seltzer", {
        "entities": [
            (0, 5, "QTY"),        # "1 3/4"
            (6, 10, "UNIT"),
            (11, 18, "NAME")
        ]
    }),
    # Add these to your EXISTING_TRAIN_DATA list in ingredient_parser_trainer.py

    ("1 tablespoon toasted sesame seeds, for garnish", {
        "entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),
            (13, 20, "PREP"),     # "toasted"
            (21, 27, "NAME"),     # "sesame"
            (28, 33, "NAME"),     # "seeds"
            (35, 46, "COMMENT")   # "for garnish"
        ]
    }),
    ("1 clove garlic, peeled and crushed, left whole", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "clove"
            (8, 14, "NAME"),      # "garlic"
            (16, 22, "PREP"),     # "peeled"
            (27, 34, "PREP"),     # "crushed"
            (36, 40, "PREP"),     # "left"
            (41, 46, "PREP")      # "whole"
        ]
    }),
    ("1 heaping tablespoon cornstarch", { # "heaping" describes the tablespoon
        "entities": [
            (0, 1, "QTY"),
            (2, 9, "PREP"),       # "heaping" (describes how the unit is measured)
            (10, 20, "UNIT"),
            (21, 31, "NAME")
        ]
    }),
    ("2 1/2 pounds boneless, skinless chicken thighs, cut into 1-inch cubes", {
        "entities": [
            (0, 5, "QTY"), (6, 12, "UNIT"), (13, 21, "PREP"), (23, 31, "PREP"),
            (32, 39, "NAME"), (40, 46, "NAME"),
            (48, 69, "PREP")  # "cut into 1-inch cubes"
        ]
    }),
    ("Pinch freshly ground white pepper", {
        "entities": [
            (0, 5, "UNIT"),       # "Pinch"
            (6, 13, "PREP"),
            (14, 20, "PREP"),
            (21, 26, "NAME"),     # "white"
            (27, 33, "NAME")      # "pepper"
        ]
    }),
    ("1/2 pound thick flank steak, weighed after trimming, cut into strips 2 1/2 inches by 1/4 inch", {
        "entities": [
            (0, 3, "QTY"), (4, 9, "UNIT"), (10, 15, "PREP"), (16, 21, "NAME"), (22, 27, "NAME"),
            (29, 51, "COMMENT"),  # "weighed after trimming"
            (53, 93, "PREP")      # "cut into strips 2 1/2 inches by 1/4 inch"
        ]
    }),
    ("1 (3-pound) chicken", { # NER labels "1" QTY, "(3-pound)" COMMENT, "chicken" NAME.
        # Downstream logic can use COMMENT to adjust QTY/UNIT for "chicken".
        "entities": [
            (0, 1, "QTY"),
            (2, 11, "COMMENT"),   # "(3-pound)"
            (12, 19, "NAME")
        ]
    }),
    ("4 cups broccoli florets, pre-cooked", {
        "entities": [
            (0, 1, "QTY"), (2, 6, "UNIT"), (7, 15, "NAME"),
            (16, 23, "NAME"),     # "florets"
            (25, 35, "PREP")      # "pre-cooked"
        ]
    }),
    ("1 pound boneless, skinless chicken thighs, cut into 1/2-inch pieces", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 16, "PREP"), (18, 26, "PREP"),
            (27, 34, "NAME"), (35, 41, "NAME"),
            (43, 67, "PREP")      # "cut into 1/2-inch pieces"
        ]
    }),
    ("1 tablespoon peanut oil, plus more as needed", {
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"), (13, 19, "NAME"), (20, 23, "NAME"),
            (25, 44, "COMMENT")   # "plus more as needed"
        ]
    }),
    ("10 ounces assorted wild mushrooms, such as oyster, shitake, chanterelles, wood ear, or porcini", {
        "entities": [
            (0, 2, "QTY"), (3, 9, "UNIT"), (10, 18, "PREP"), (19, 23, "NAME"), (24, 33, "NAME"),
            (35, 94, "COMMENT") # "such as oyster, shitake, chanterelles, wood ear, or porcini"
        ]
    }),
    ("3 (2 1/2 to 3 pound) farm-raised pheasants*, innards removed, wing tips and necks trimmed (See Cook's Note)", {
        "entities": [
            (0, 1, "QTY"), (2, 20, "COMMENT"), (21, 32, "PREP"), (33, 43, "NAME"),
            (45, 60, "PREP"),
            (62, 89, "PREP"),     # "wing tips and necks trimmed"
            (90, 107, "COMMENT")  # "(See Cook's Note)"
        ]
    }),
    ("1/4 pound cured and smoked country ham, finely chopped (or chopped in a food processor)", {
        "entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),
            (10, 15, "PREP"),     # "cured"
            (20, 26, "PREP"),     # "smoked"
            (27, 34, "NAME"),     # "country"
            (35, 38, "NAME"),     # "ham"
            (40, 54, "PREP"),     # "finely chopped"
            (55, 87, "COMMENT")   # "(or chopped in a food processor)"
        ]
    }),
    ("1 1/4 pounds ground chuck", {
        "entities": [
            (0, 5, "QTY"),
            (6, 12, "UNIT"),
            (13, 19, "PREP"),
            (20, 25, "NAME")
        ]
    }),
    ("1 teaspoon seafood seasoning, such as Old Bay", {
        "entities": [
            (0, 1, "QTY"),
            (2, 10, "UNIT"),
            (11, 18, "NAME"),     # "seafood"
            (19, 28, "NAME"),     # "seasoning"
            (30, 45, "COMMENT")   # "such as Old Bay"
        ]
    }),
    ("2 to 3 ounces rice wine vinegar", {
        "entities": [
            (0, 6, "QTY"),        # "2 to 3"
            (7, 13, "UNIT"),
            (14, 18, "NAME"),     # "rice"
            (19, 23, "NAME"),     # "wine"
            (24, 31, "NAME")      # "vinegar"
        ]
    }),
    ("10 ounces medium or wide egg noodles", {
        "entities": [
            (0, 2, "QTY"), (3, 9, "UNIT"), (10, 16, "PREP"),
            (17, 24, "ALT_NAME"), # "or wide"
            (25, 28, "NAME"),     # "egg"
            (29, 36, "NAME")      # "noodles"
        ]
    }),
    ("1 tablespoon (15 g) white sugar", {
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"),
            (13, 19, "COMMENT"),  # "(15 g)"
            (20, 25, "NAME"),     # "white"
            (26, 31, "NAME")      # "sugar"
        ]
    }),
    ("1 pod star anise", {
        "entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),       # "pod"
            (6, 10, "NAME"),      # "star"
            (11, 16, "NAME")      # "anise"
        ]
    }),
    ("1/4 cup sliced and drained pickled jalapenos, chopped", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 14, "PREP"),      # "sliced"
            (19, 26, "PREP"),     # "drained"
            (27, 34, "PREP"),     # "pickled"
            (35, 44, "NAME"),     # "jalapenos"
            (46, 53, "PREP")      # "chopped"
        ]
    }),
    ("1/2 teaspoon ground cumin", { # As per your note, "ground cumin" is NAME
        "entities": [
            (0, 3, "QTY"),
            (4, 12, "UNIT"),
            (13, 25, "NAME")      # "ground cumin"
        ]
    }),
    ("1 bunch arugula", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),
            (8, 15, "NAME")
        ]
    }),
    ("1 (8-ounce) chicken breast, grilled or poached and cut into small cubes or shredded", {
        "entities": [
            (0, 1, "QTY"),
            (2, 11, "UNIT"),      # "(8-ounce)" - including parentheses as part of the unit descriptor
            (12, 19, "NAME"),     # "chicken"
            (20, 26, "NAME"),     # "breast"
            (28, 83, "PREP")      # "grilled or poached and cut into small cubes or shredded"
        ]
    }),
    ("1 pound (453 grams) peeled and deveined large shrimp, tail on", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 19, "COMMENT"), (20, 26, "PREP"),
            (31, 39, "PREP"), (40, 45, "UNIT"), (46, 52, "NAME"),
            (54, 61, "PREP")      # "tail on"
        ]
    }),
    ("1 cup (175 grams) halved grape or cherry tomatoes", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"), (6, 17, "COMMENT"), (18, 24, "PREP"),
            (25, 30, "NAME"),
            (31, 49, "ALT_NAME")  # "or cherry tomatoes"
        ]
    }),
    ("1 cup Clamato", {
        "entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 13, "NAME")
        ]
    }),
    ("1/4 seedless watermelon, rind removed, peeled and cut into 1-inch pieces, flesh reserved", {
        "entities": [
            (0, 3, "QTY"),        # "1/4" (of a watermelon)
            (4, 12, "PREP"),      # "seedless"
            (13, 23, "NAME"),     # "watermelon"
            (25, 37, "PREP"),     # "rind removed"
            (39, 45, "PREP"),     # "peeled"
            (50, 72, "PREP"),     # "cut into 1-inch pieces"
            (74, 88, "COMMENT")   # "flesh reserved"
        ]
    }),
    ("One 15-ounce can chickpeas", {
        "entities": [
            (0, 3, "QTY"), (4, 12, "COMMENT"), (13, 16, "UNIT"),
            (17, 26, "NAME")      # "chickpeas"
        ]
    }),
    ("1/3 cup plus 1 tablespoon tahini", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (8, 25, "COMMENT"),   # "plus 1 tablespoon"
            (26, 32, "NAME")      # "tahini"
        ]
    }),
    ("4 heads garlic, roasted; paper skin removed and cored", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 14, "NAME"), (16, 23, "PREP"),
            (25, 53, "PREP")      # "paper skin removed and cored"
        ]
    }),
    ("1 red onion, peeled and sliced into 3 parts width wise", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "NAME"), (6, 11, "NAME"), (13, 19, "PREP"),
            (24, 54, "PREP")      # "sliced into 3 parts width wise"
        ]
    }),
    ("1 tablespoon basil, minced", {
        "entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),
            (13, 18, "NAME"),
            (20, 26, "PREP")
        ]
    }),
    ("8 oz duck or rabbit confit, medium to large pieces removed from bones", {
        "entities": [
            (0, 1, "QTY"), (2, 4, "UNIT"), (5, 9, "NAME"),
            (10, 26, "ALT_NAME"), # "or rabbit confit"
            (28, 69, "PREP")      # "medium to large pieces removed from bones" (removed comma from start)
        ]
    }),
    ("15 steaks", { # "steaks" acts as a unit here for a count
        "entities": [
            (0, 2, "QTY"),
            (3, 9, "UNIT")
        ]
    }),
    ("Flaky sea salt", {
        "entities": [
            (0, 5, "PREP"),       # "Flaky"
            (6, 9, "NAME"),
            (10, 14, "NAME")
        ]
    }),
    ("2 boneless rib-eye steaks", {
        "entities": [
            (0, 1, "QTY"),
            (2, 10, "PREP"),
            (11, 18, "NAME"),     # "rib-eye"
            (19, 25, "UNIT")      # "steaks"
        ]
    }),
    ("1 tablespoon annatto seeds", {
        "entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),
            (13, 20, "NAME"),
            (21, 26, "NAME")
        ]
    }),
    ("4 cups peeled and grated sweet potatoes", {
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),
            (7, 13, "PREP"),
            (18, 24, "PREP"),
            (25, 30, "NAME"),     # "sweet"
            (31, 39, "NAME")      # "potatoes"
        ]
    }),
    ("2 ounces sliced pastrami, finely chopped", {
        "entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 15, "PREP"),
            (16, 24, "NAME"),
            (26, 32, "PREP"),
            (33, 40, "PREP")
        ]
    }),
    ("2 teaspoons toasted and ground coriander seed", {
        "entities": [
            (0, 1, "QTY"), (2, 11, "UNIT"), (12, 19, "PREP"),
            (24, 45, "NAME")      # "ground coriander seed"
        ]
    }),
    ("3 ancho chiles, stemmed, seeded and sliced", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "NAME"),
            (8, 14, "NAME"),
            (16, 23, "PREP"),
            (25, 31, "PREP"),
            (36, 42, "PREP")
        ]
    }),
    ("3 cascabel chiles, stemmed, seeded and sliced", {
        "entities": [
            (0,1,"QTY"),(2,10,"NAME"),(11,17,"NAME"),(19,26,"PREP"),(28,34,"PREP"),(39,45,"PREP")
        ]
    }),
    ("3 dried arbol chiles, stemmed, seeded and sliced", {
        "entities": [
            (0,1,"QTY"),(2,7,"PREP"),(8,13,"NAME"),(14,20,"NAME"),(22,29,"PREP"),(31,37,"PREP"),(42,48,"PREP")
        ]
    }),
    ("2 tablespoons whole cumin seeds", {
        "entities": [
            (0,1,"QTY"),(2,13,"UNIT"),(14,19,"PREP"),(20,25,"NAME"),(26,31,"NAME")
        ]
    }),
    ("One 9-ounce package fresh fettuccine", {
        "entities": [
            (0,3,"QTY"),(4,11,"COMMENT"),(12,19,"UNIT"),(20,25,"PREP"),(26,36,"NAME")
        ]
    }),
    ("4 pounds spinach, stems removed, washed and dried", {
        "entities": [
            (0,1,"QTY"),(2,8,"UNIT"),(9,16,"NAME"),(18,23,"PREP"),(24,31,"PREP"),(33,39,"PREP"),(44,49,"PREP")
        ]
    }),
    ("1/2 pound dried cannellini beans, black-eyed peas, soaked overnight in cold water and drained", {
        "entities": [
            (0, 3, "QTY"), (4, 9, "UNIT"), (10, 15, "PREP"), (16, 26, "NAME"),
            (27, 32, "NAME"), (34, 49, "ALT_NAME"),
            (51, 93, "PREP")      # "soaked overnight in cold water and drained"
        ]
    }),
    ("1/2 teaspoon Four-Spice Power (recipe follows)", {
        "entities": [
            (0, 3, "QTY"), (4, 12, "UNIT"),
            (13, 29, "NAME"),     # "Four-Spice Power"
            (30, 46, "COMMENT")   # "(recipe follows)"
        ]
    }),
    ("1 pound and 10 ounces sour cherries, pre-pitted weight; or 6 cups frozen or jarred", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"),
            (8, 21, "COMMENT"),    # "and 10 ounces"
            (22, 26, "NAME"),     # "sour"
            (27, 35, "NAME"),     # "cherries"
            (37, 54, "COMMENT"),  # "pre-pitted weight"
            (56, 82, "ALT_NAME")  # "or 6 cups frozen or jarred"
        ]
    }),
    ("Beaten egg, for glaze", {
        "entities": [
            (0, 6, "PREP"), (7, 10, "NAME"),
            (12, 21, "COMMENT")   # "for glaze"
        ]
    }),
    ("7 ounces (200 grams) spicy or mild genoa salami, thinly sliced or shaved", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 20, "COMMENT"),
            (21, 26, "PREP"),     # "spicy"
            (27, 34, "ALT_NAME"), # "or mild" (alternative to spicy)
            (35, 40, "NAME"),     # "genoa"
            (41, 47, "NAME"),     # "salami"
            (49, 62, "PREP"),     # "thinly sliced"
            (63, 72, "ALT_PREP")  # "or shaved"
        ]
    }),
    ("2 cups of white grits", {
        "entities": [
            (0,1,"QTY"),(2,6,"UNIT"),(7,9,"PREP"),(10,15,"NAME"),(16,21,"NAME")
        ]
    }),
    ("4 slices cooked and crumbled bacon", {
        "entities": [
            (0,1,"QTY"),(2,8,"UNIT"),(9,15,"PREP"),(20,28,"PREP"),(29,34,"NAME")
        ]
    }),
    ("1 tablespoon minced seeded red jalapenos", {
        "entities": [
            (0,1,"QTY"),(2,12,"UNIT"),(13,19,"PREP"),(20,26,"PREP"),(27,30,"NAME"),(31,40,"NAME")
        ]
    }),
    ("1 tablespoon basil leaves, torn", {
        "entities": [
            (0,1,"QTY"),(2,12,"UNIT"),(13,18,"NAME"),(19,25,"NAME"),(27,31,"PREP")
        ]
    }),
    ("1/2 large watermelon", {
        "entities": [
            (0,3,"QTY"),(4,9,"UNIT"),(10,20,"NAME")
        ]
    }),
    ("1 pound fresh or frozen cranberries", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "PREP"),
            (14, 23, "ALT_PREP"), # "or frozen"
            (24, 35, "NAME")      # "cranberries"
        ]
    }),
    ("10 large basil leaves", {
        "entities": [
            (0,2,"QTY"),(3,8,"UNIT"),(9,14,"NAME"),(15,21,"NAME")
        ]
    }),
    ("3 tablespoons best quality cocoa powder", {
        "entities": [
            (0,1,"QTY"),(2,13,"UNIT"),(14,26,"PREP"),(27,32,"NAME"),(33,39,"NAME") # best quality
        ]
    }),
    ("1 cup very cold heavy cream", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"),
            (6, 10, "PREP"),      # "very"
            (11, 15, "PREP"),     # "cold"
            (16, 21, "NAME"),     # "heavy"
            (22, 27, "NAME")      # "cream"
        ]
    }),
    # Alternative: ("heavy cream", NAME) -> (16, 27, "NAME")
    ("3 cups lightly packed basil leaves", {
        "entities": [
            (0,1,"QTY"),(2,6,"UNIT"),(7,14,"PREP"),(15,21,"PREP"),(22,27,"NAME"),(28,34,"NAME") # lightly packed
        ]
    }),
    ("1 pound linguine", {
        "entities": [
            (0,1,"QTY"),(2,7,"UNIT"),(8,16,"NAME")
        ]
    }),
    ("1 ounce tequila", {
        "entities": [
            (0,1,"QTY"),(2,7,"UNIT"),(8,15,"NAME")
        ]
    }),
    ("1 tablespoon tomatoes, peeled, seeded and small dice", {
        "entities": [
            (0,1,"QTY"),(2,12,"UNIT"),(13,21,"NAME"),(23,29,"PREP"),(31,37,"PREP"),(42,47,"PREP"),(48,52,"PREP") # small, dice
        ]
    }),
    ("12 ounces lump crab meat", {
        "entities": [
            (0,2,"QTY"),(3,9,"UNIT"),(10,14,"NAME"),(15,19,"NAME"),(20,24,"NAME")
        ]
    }),
    ("3 cups bread crumbs", {
        "entities": [
            (0,1,"QTY"),(2,6,"UNIT"),(7,12,"NAME"),(13,19,"NAME")
        ]
    }),
    ("6 (5 to 6-ounce) tuna paillards, 1/2-inch thick", {
        "entities": [
            (0, 1, "QTY"), (2, 16, "COMMENT"), (17, 21, "NAME"),
            (22, 31, "NAME"),     # "paillards"
            (33, 47, "COMMENT")   # "1/2-inch thick"
        ]
    }),
    ("1 pound spinach, picked and washed (loosely packed)", {
        "entities": [
            (0,1,"QTY"),(2,7,"UNIT"),(8,15,"NAME"),(17,23,"PREP"),(28,34,"PREP"),(35,51,"COMMENT")
        ]
    }),
    ("1/2 cup pitted and chopped kalamata olives", {
        "entities": [
            (0,3,"QTY"),(4,7,"UNIT"),(8,14,"PREP"),(19,26,"PREP"),(27,35,"NAME"),(36,42,"NAME")
        ]
    }),
    ("2 (1 pound) halibut steaks, 1 1/4-inch thick, from tail end of fish", {
        "entities": [
            (0, 1, "QTY"), (2, 11, "COMMENT"), (12, 19, "NAME"), (20, 26, "UNIT"),
            (28, 44, "COMMENT"),  # "1 1/4-inch thick"
            (46, 67, "COMMENT")   # "from tail end of fish"
        ]
    }),
    ("2 1/3 cups warm water, 100 to 110 degrees F", {
        "entities": [
            (0,5,"QTY"),(6,10,"UNIT"),(11,15,"PREP"),(16,21,"NAME"),(23,43,"COMMENT")
        ]
    }),
    ("2 tablespoons (three .75-ounce packets) active dry yeast, such as Fleischmann's", {
        "entities": [
            (0, 1, "QTY"), (2, 13, "UNIT"),
            (14, 39, "COMMENT"),  # "(three .75-ounce packets)"
            (40, 46, "PREP"),     # "active"
            (47, 50, "PREP"),     # "dry"
            (51, 56, "NAME"),     # "yeast"
            (56, 79, "COMMENT")   # ", such as Fleischmann's"
        ]
    }),
    ("3 tablespoons zaatar, optional", {
        "entities": [
            (0,1,"QTY"),(2,13,"UNIT"),(14,20,"NAME"),(22,30,"COMMENT")
        ]
    }),
    ("1 cup unsalted butter, room temperature and cut into small pieces", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"), (6, 14, "NAME"), (15, 21, "NAME"),
            (23, 39, "COMMENT"),  # "room temperature"
            # "and" is O (40-43)
            (44, 65, "PREP")      # "cut into small pieces"
        ]
    }),
    ("1 large egg yolk beaten with 1 tablespoon water, for egg wash", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 11, "NAME"), (12, 16, "NAME"),
            (17, 47, "PREP"),     # "beaten with 1 tablespoon water"
            (49, 61, "COMMENT")   # "for egg wash"
        ]
    }),
    ("1 tablespoon active dry yeast", {
        "entities": [
            (0,1,"QTY"),(2,12,"UNIT"),(13,19,"PREP"),(20,23,"PREP"),(24,29,"NAME")
        ]
    }),
    ("1 3/4 cups warm (110 degrees F) water", {
        "entities": [
            (0, 5, "QTY"), (6, 10, "UNIT"), (11, 15, "PREP"),
            (16, 31, "COMMENT"),  # "(110 degrees F)"
            (32, 37, "NAME")      # "water"
        ]
    }),
    ("3/4 cup warm water (100 degrees F to 110 degrees F)", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 12, "PREP"), (13, 18, "NAME"),
            (19, 51, "COMMENT")   # "(100 degrees F to 110 degrees F)"
        ]
    }),
    ("1 cup shredded and chopped rotisserie chicken meat", {
        "entities": [
            (0,1,"QTY"),(2,5,"UNIT"),(6,14,"PREP"),(19,26,"PREP"),(27,37,"NAME"),(38,45,"NAME"),(46,50,"NAME")
        ]
    }),
    ("2 grams ground coriander", { # "ground coriander" as NAME
        "entities": [
            (0,1,"QTY"),(2,7,"UNIT"),(8,24,"NAME")
        ]
    }),
    ("3 grams garlic powder", {
        "entities": [
            (0,1,"QTY"),(2,7,"UNIT"),(8,14,"NAME"),(15,21,"NAME")
        ]
    }),
    ("10 pounds beef top round", {
        "entities": [
            (0,2,"QTY"),(3,9,"UNIT"),(10,14,"NAME"),(15,18,"NAME"),(19,24,"NAME")
        ]
    }),
    ("85 grams nonfat milk powder", {
        "entities": [
            (0,2,"QTY"),(3,8,"UNIT"),(9,15,"PREP"),(16,20,"NAME"),(21,27,"NAME")
        ]
    }),
    ("66 grams kosher salt", {
        "entities": [
            (0,2,"QTY"),(3,8,"UNIT"),(9,15,"NAME"),(16,20,"NAME")
        ]
    }),
    ("1 tablespoon (15 milliliters) milk or water, for an egg wash", {
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"),
            (13, 29, "COMMENT"),  # "(15 milliliters)"
            (30, 34, "NAME"),     # "milk"
            (35, 43, "ALT_NAME"), # "or water"
            (45, 60, "COMMENT")   # "for an egg wash"
        ]
    }),
    ("1 whole ripe pineapple, cut in 1/2 lengthwise and flesh removed (making 2 'boats'), core removed and fruit diced", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "PREP"), (8, 12, "PREP"),
            (13, 22, "NAME"),     # "pineapple"
            (24, 63, "PREP"),     # "cut in 1/2 lengthwise and flesh removed"
            (64, 82, "COMMENT"),  # "(making 2 'boats')"
            (84, 96, "PREP"),     # "core removed" (Corrected from your entity)
            # "and" (97-100) is O
            (101, 112, "PREP")    # "fruit diced"
        ]
    }),
    ("Large flake sea salt", {
        "entities": [
            (0,5,"PREP"),(6,11,"PREP"),(12,15,"NAME"),(16,20,"NAME") # Large, flake
        ]
    }),
    ("4 tablespoons peeled and grated fresh ginger", {
        "entities": [
            (0,1,"QTY"),(2,13,"UNIT"),(14,20,"PREP"),(25,31,"PREP"),(32,37,"PREP"),(38,44,"NAME")
        ]
    }),

    # Add these to your EXISTING_TRAIN_DATA list in ingredient_parser_trainer.py

    ("1 tablespoon dry rubbed sage", {
        "entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),
            (13, 16, "PREP"),     # "dry"
            (17, 23, "PREP"),     # "rubbed"
            (24, 28, "NAME")      # "sage"
        ]
    }),
    ("16 thin slices prosciutto", {
        "entities": [
            (0, 2, "QTY"),
            (3, 7, "PREP"),       # "thin"
            (8, 14, "UNIT"),      # "slices"
            (15, 25, "NAME")      # "prosciutto"
        ]
    }),
    ("12 paper thin slices prosciutto", {
        "entities": [
            (0, 2, "QTY"),
            (3, 8, "PREP"),       # "paper" (describing thinness)
            (9, 13, "PREP"),      # "thin"
            (14, 20, "UNIT"),
            (21, 31, "NAME")
        ]
    }),
    ("6 sage leaves", {
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "NAME"),
            (7, 13, "UNIT")       # "leaves"
        ]
    }),
    ("12 slices thinly sliced prosciutto (about 6 ounces)", {
        "entities": [
            (0, 2, "QTY"),
            (3, 9, "UNIT"),
            (10, 16, "PREP"),     # "thinly"
            (17, 23, "PREP"),     # "sliced"
            (24, 34, "NAME"),
            (35, 51, "COMMENT")   # "(about 6 ounces)"
        ]
    }),
    ("1 Japanese eggplant sliced on an angle in half-inch thick slices", {
        "entities": [
            (0, 1, "QTY"), (2, 10, "NAME"), (11, 19, "NAME"),
            (20, 64, "PREP")  # "sliced on an angle in half-inch thick slices"
        ]
    }),
    ("1 small zucchini sliced on an angle in half-inch thick slices", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "small"
            (8, 16, "NAME"),      # "zucchini"
            (17, 61, "PREP")      # "sliced on an angle in half-inch thick slices"
        ]
    }),
    ("3 3/4 to 4 cups confectioners' sugar (use more for stiffer icing, less for thinner)", {
        "entities": [
            (0, 10, "QTY"), (11, 15, "UNIT"),
            (16, 30, "NAME"),     # "confectioners'" (token 'confectioners' 16-29, then ''' 29-30)
            (31, 36, "NAME"),     # "sugar"
            (37, 83, "COMMENT")   # "(use more for stiffer icing, less for thinner)"
        ]
    }),
    ("Your favorite sprinkles or other edible candy, for decorating", {
        "entities": [
            (0, 13, "NAME"), (14, 23, "NAME"),
            (24, 45, "ALT_NAME"), # "or other edible candy"
            (47, 61, "COMMENT")   # "for decorating"
        ]
    }),
    ("1 vanilla bean pod, split and seeds scraped", {
        "entities": [
            (0, 1, "QTY"),
            (2, 9, "NAME"),       # "vanilla"
            (10, 14, "NAME"),     # "bean"
            (15, 18, "UNIT"),     # "pod"
            (20, 25, "PREP"),     # "split"
            (30, 35, "PREP"),     # "seeds" (as in "seeds removed/scraped")
            (36, 43, "PREP")      # "scraped"
        ]
    }),
    ("Edible gold foil, optional", {
        "entities": [
            (0, 6, "PREP"),       # "Edible"
            (7, 11, "NAME"),      # "gold"
            (12, 16, "NAME"),     # "foil"
            (18, 26, "COMMENT")   # "optional"
        ]
    }),
    ("2 pieces naan, warmed and torn into pieces", {
        "entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 13, "NAME"),      # "naan"
            (15, 21, "PREP"),     # "warmed"
            (26, 42, "PREP")      # "torn into pieces"
        ]
    }),
    ("1/2 cup chopped fresh cilantro, plus more for topping", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "PREP"), (16, 21, "PREP"),
            (22, 30, "NAME"),
            (32, 53, "COMMENT")   # "plus more for topping"
        ]
    }),
    ("1 cup frozen sliced okra, thawed", {
        "entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 12, "PREP"),      # "frozen"
            (13, 19, "PREP"),     # "sliced"
            (20, 24, "NAME"),     # "okra"
            (26, 32, "PREP")      # "thawed"
        ]
    }),
    ("2 tablespoons gochujang (Korean chile paste)", {
        "entities": [
            (0, 1, "QTY"), (2, 13, "UNIT"), (14, 23, "NAME"),
            (24, 44, "COMMENT")   # "(Korean chile paste)"
        ]
    }),
    ("3 tablespoons chopped roasted salted peanuts", { # "chopped roasted salted" are all PREP
        "entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 21, "PREP"),
            (22, 29, "PREP"),
            (30, 36, "PREP"),
            (37, 44, "NAME")
        ]
    }),
    ("1/4 cup creme fraiche", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 13, "NAME"),      # "creme"
            (14, 21, "NAME")      # "fraiche"
        ]
    }),
    (
        "1 jar (at least 6 ounces) jalapeno jelly",
        {
            "entities": [
                (0, 1, "QTY"),         # "1"
                (2, 5, "UNIT"),        # "jar"
                (6, 25, "COMMENT"),    # "(at least 6 ounces)"  -- Token `(` is 6, `)` is 24. Span is (6, 25)
                (26, 34, "NAME"),      # "jalapeno" -- Token `jalapeno` is 26
                (35, 40, "NAME")       # "jelly" -- Token `jelly` is 35
            ]
        }
    ),
    ("Dill-and-Caper Creme Fraiche Sauce, for serving, recipe follows", {
        "entities": [
            (0, 34, "NAME"),      # "Dill-and-Caper Creme Fraiche Sauce"
            (36, 47, "COMMENT"),  # "for serving" (comma at 34 is O, comma at 47 is O)
            (49, 63, "COMMENT")   # "recipe follows"
        ]
    }),
    ("1 tablespoons creme fraiche", { # Note: 1 tablespoonS - likely a typo, but annotating as is.
        "entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 19, "NAME"),
            (20, 27, "NAME")
        ]
    }),
    ("2 jalapenos, seeded and diced fine, plus whole or sliced, for serving", {
        "entities": [
            (0, 1, "QTY"), (2, 11, "NAME"), (13, 19, "PREP"), (24, 29, "PREP"),
            (30, 34, "PREP"),
            (36, 69, "COMMENT")   # "plus whole or sliced, for serving"
        ]
    }),
    ("1/4 cup store-bought salsa verde", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 20, "PREP"),      # "store-bought"
            (21, 26, "NAME"),     # "salsa"
            (27, 32, "NAME")      # "verde"
        ]
    }),
    ("2 green onions, green and pale green part, thinly sliced", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "NAME"), (8, 14, "NAME"),
            (16, 41, "COMMENT"),  # "green and pale green part"
            (43, 49, "PREP"),     # "thinly"
            (50, 56, "PREP")      # "sliced"
        ]
    }),
    ("1/2 teaspoon fleur de sel", {
        "entities": [
            (0, 3, "QTY"),
            (4, 12, "UNIT"),
            (13, 18, "NAME"),     # "fleur"
            (19, 21, "NAME"),     # "de"
            (22, 25, "NAME")      # "sel"
        ]
    }),
    ("3 tablespoons high-quality caramel sauce, plus more for topping", {
        "entities": [
            (0, 1, "QTY"), (2, 13, "UNIT"), (14, 26, "PREP"), (27, 34, "NAME"),
            (35, 40, "NAME"),
            (42, 63, "COMMENT")   # "plus more for topping"
        ]
    }),
    ("1/3 cup frisee", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 14, "NAME")
        ]
    }),
    ("1 teaspoon minced fresh dill", {
        "entities": [
            (0, 1, "QTY"),
            (2, 10, "UNIT"),
            (11, 17, "PREP"),
            (18, 23, "PREP"),
            (24, 28, "NAME")
        ]
    }),
    ("1/2 cup minced scallions, white and green parts (4 scallions)", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 14, "PREP"),
            (15, 24, "NAME"),     # "scallions"
            (26, 47, "COMMENT"),  # "white and green parts"
            (48, 61, "COMMENT")   # "(4 scallions)"
        ]
    }),
    ("1/2 cup minced fresh dill", {"entities": [(0,3,"QTY"),(4,7,"UNIT"),(8,14,"PREP"),(15,20,"PREP"),(21,25,"NAME")]}), # Duplicate of an earlier one

    ("2 pounds fingerling or baby potatoes, scrubbed and halved lengthwise", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 19, "NAME"),
            (20, 36, "ALT_NAME"), # "or baby potatoes"
            # Comma at 36 is O
            (38, 46, "PREP"),     # "scrubbed"
            # "and" at 47 is O
            (51, 57, "PREP"),     # "halved"
            (58, 68, "PREP")      # "lengthwise"
        ]
    }),
    ("1 cup whole-milk ricotta (about 10 ounces)", {
        "entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 16, "NAME"),      # "whole-milk" (or PREP for whole, NAME for milk)
            (17, 24, "NAME"),     # "ricotta"
            (25, 41, "COMMENT")   # "(about 10 ounces)"
        ]
    }),
    ("4 large zucchinis (about 3 pounds)", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),
            (8, 17, "NAME"),
            (18, 34, "COMMENT")
        ]
    }),
    ("1/2 cup crumbled Gorgonzola", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 16, "PREP"),
            (17, 27, "NAME")
        ]
    }),
    ("1/2 cup roughly chopped raw walnuts", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "PREP"),
            (16, 23, "PREP"),     # "chopped"
            (24, 27, "PREP"),     # "raw"
            (28, 35, "NAME")      # "walnuts"
        ]
    }),
    # Based on your note "chopped walnuts is a name":
    ("1/2 cup roughly chopped walnuts", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 15, "PREP"),      # "roughly"
            (16, 31, "NAME")      # "chopped walnuts"
        ]
    }),

    ("1/4 pound gorgonzola dolce", {
        "entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),
            (10, 20, "NAME"),     # "gorgonzola"
            (21, 26, "NAME")      # "dolce"
        ]
    }),
    ("1/4 teaspoon red pepper flakes, optional", {
        "entities": [
            (0, 3, "QTY"),
            (4, 12, "UNIT"),
            (13, 16, "NAME"),
            (17, 23, "NAME"),
            (24, 30, "NAME"),
            (32, 40, "COMMENT")
        ]
    }),
    ("Frozen (not in syrup) raspberries", {
        "entities": [
            (0, 6, "PREP"),
            (7, 21, "COMMENT"),   # "(not in syrup)"
            (22, 33, "NAME")      # "raspberries"
        ]
    }),
    ("1/2 ounce Framboise", {
        "entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),
            (10, 19, "NAME")
        ]
    }),
    ("1/2 ounce Grand Marnier", {
        "entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),
            (10, 15, "NAME"),     # "Grand"
            (16, 23, "NAME")      # "Marnier"
        ]
    }),
    ("3/4 cup toasted and chopped pecans", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 15, "PREP"),      # "toasted"
            (20, 27, "PREP"),     # "chopped"
            (28, 34, "NAME")      # "pecans"
        ]
    }),
    ("1/3 cup plus 3 tablespoons Parmesan", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 26, "COMMENT"),  # "plus 3 tablespoons"
            (27, 35, "NAME")      # "Parmesan"
        ]
    }),
    ("2 pounds zucchini (each about 8 inches long and 1 1/2 inches in diameter work best)", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 17, "NAME"),
            (18, 83, "COMMENT")
        ]
    }),
    ("6 thin slices prosciutto, halved", {
        "entities": [
            (0,1,"QTY"),(2,6,"PREP"),(7,13,"UNIT"),(14,24,"NAME"),(26,32,"PREP")
        ]
    }),
    ("24 very thin slices prosciutto", {
        "entities": [
            (0,2,"QTY"),(3,7,"PREP"),(8,12,"PREP"),(13,19,"UNIT"),(20,30,"NAME")
        ]
    }),
    ("1/2 honeydew melon", {
        "entities": [
            (0, 3, "QTY"),
            (4, 12, "NAME"),      # "honeydew"
            (13, 18, "NAME")      # "melon"
        ]
    }),
    ("1 eggplant cut into 8 (1/4-inch) slices", {
        "entities": [
            (0, 1, "QTY"), (2, 10, "NAME"),
            (11, 39, "PREP")      # "cut into 8 (1/4-inch) slices"
        ]
    }),
    ("1 yellow squash cut into 8 (1/2-inch) slices", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "NAME"), (9, 15, "NAME"),
            (16, 44, "PREP")      # "cut into 8 (1/2-inch) slices"
        ]
    }),
    ("1/4 cup finely chopped dried dates", {
        "entities": [
            (0,3,"QTY"),(4,7,"UNIT"),(8,14,"PREP"),(15,22,"PREP"),(23,28,"PREP"),(29,34,"NAME")
        ]
    }),
    ("Couscous with Dried Dates, recipe follows", {
        "entities": [
            (0,8,"NAME"),(9,13,"PREP"),(14,19,"NAME"),(20,25,"NAME"),(27,41,"COMMENT")
        ]
    }),
    ("1/2 cup pitted and chopped briny olives", {
        "entities": [
            (0,3,"QTY"),(4,7,"UNIT"),(8,14,"PREP"),(19,26,"PREP"),(27,32,"PREP"),(33,39,"NAME") # briny
        ]
    }),
    ("1/4 cup dry sherry", {
        "entities": [
            (0,3,"QTY"),(4,7,"UNIT"),(8,11,"PREP"),(12,18,"NAME")
        ]
    }),
    ("4 ounces cremini mushrooms, stemmed and sliced 1/4 inch thick", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 16, "NAME"), (17, 26, "NAME"),
            (28, 35, "PREP"), # stemmed
            # "and" at 36 is O
            (40, 46, "PREP"), # sliced
            (47, 61, "COMMENT")   # "1/4 inch thick"
        ]
    }),
    ("4 ounces shiitake mushrooms, stemmed and sliced 1/4 inch thick", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 17, "NAME"), (18, 27, "NAME"),
            (29, 36, "PREP"), (41, 47, "PREP"),
            (48, 62, "COMMENT")   # "1/4 inch thick"
        ]
    }),
    ("Two 15-ounce cans cannellini beans, drained and rinsed", {
        "entities": [
            (0,3,"QTY"),(4,12,"COMMENT"),(13,17,"UNIT"),(18,28,"NAME"),(29,34,"NAME"),(36,43,"PREP"),(48,54,"PREP")
        ]
    }),
    ("1 cup fresh flat-leaf parsley leaves, finely chopped, plus more for garnish, optional", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"), (6, 11, "PREP"), (12, 21, "NAME"),
            (22, 29, "NAME"), (30, 36, "NAME"), (38, 52, "PREP"),
            (54, 85, "COMMENT") # "plus more for garnish, optional"
        ]
    }),
    ("2 red onions, 1 cut into 1/4-inch dice and 1 sliced for garnish", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "NAME"), (6, 12, "NAME"),
            (14, 63, "COMMENT") # "1 cut into 1/4-inch dice and 1 sliced for garnish"
        ]
    }),
    ("1/2 bunch fresh dill, finely chopped", {
        "entities": [
            (0,3,"QTY"),(4,9,"UNIT"),(10,15,"PREP"),(16,20,"NAME"),(22,28,"PREP"),(29,36,"PREP")
        ]
    }),
    ("Pinch crushed red pepper", {"entities": [(0,5,"UNIT"),(6,13,"PREP"),(14,17,"NAME"),(18,24,"NAME")]}), # Already added
    ("Zest of 1/2 lemon", {
        "entities": [
            (0,4,"NAME"),(5,7,"PREP"),(8,11,"QTY"),(12,17,"NAME")
        ]
    }),
    ("4 Whole-Wheat Pitas, recipe follows, or 4 seeded hamburger buns", {
        "entities": [
            (0, 1, "QTY"), (2, 13, "NAME"), (14, 19, "NAME"), (21, 35, "COMMENT"),
            (37, 63, "ALT_NAME")  # "or 4 seeded hamburger buns"
        ]
    }),
    ("2 mint tea bags", {
        "entities": [
            (0,1,"QTY"),(2,6,"NAME"),(7,10,"NAME"),(11,15,"UNIT")
        ]
    }),
    ("4 ounces cremini mushrooms, stemmed and sliced 1/4 inch thick", {"entities": [(0,1,"QTY"),(2,8,"UNIT"),(9,16,"NAME"),(17,26,"NAME"),(28,35,"PREP"),(40,46,"PREP"),(47,58,"COMMENT")]}), # Duplicate
    ("1/2 bunch fresh mint, finely chopped", {
        "entities": [
            (0,3,"QTY"),(4,9,"UNIT"),(10,15,"PREP"),(16,20,"NAME"),(22,28,"PREP"),(29,36,"PREP")
        ]
    }),
    ("1 tablespoon chopped mint leaves", {
        "entities": [
            (0,1,"QTY"),(2,12,"UNIT"),(13,20,"PREP"),(21,25,"NAME"),(26,32,"NAME")
        ]
    }),
    ("4 (6-ounce) bluefish fillets, skin on", {
        "entities": [
            (0, 1, "QTY"),
            (2, 11, "COMMENT"),  # "(6-ounce)"
            (12, 20, "NAME"),    # "bluefish"
            (21, 28, "UNIT"),    # "fillets"
            (30, 37, "COMMENT")  # "skin on"
        ]
    }),
    ("1 teaspoon toasted and crushed coriander seeds", {
        "entities": [
            (0,1,"QTY"),(2,10,"UNIT"),(11,18,"PREP"),(23,30,"PREP"),(31,40,"NAME"),(41,46,"NAME")
        ]
    }),
    ("1 cup chicken stock, plus more as needed", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"), (6, 13, "NAME"), (14, 19, "NAME"),
            (21, 40, "COMMENT")   # "plus more as needed"
        ]
    }),
    ("Two 15.5-ounce cans pinto beans, drained and rinsed", {
        "entities": [
            (0,3,"QTY"),(4,14,"COMMENT"),(15,19,"UNIT"),(20,25,"NAME"),(26,31,"NAME"),(33,40,"PREP"),(45,51,"PREP")
        ]
    }),
    ("1/2 teaspoon coriander", {
        "entities": [
            (0, 3, "QTY"), (4, 12, "UNIT"),
            (13, 22, "NAME")      # "coriander"
        ]
    }),
    ("Three 15-ounce cans black-eyed peas, rinsed", {
        "entities": [
            (0,5,"QTY"),(6,14,"COMMENT"),(15,19,"UNIT"),(20,30,"NAME"),(31,35,"NAME"),(37,43,"PREP") # black-eyed peas
        ]
    }),
    ("2 T-bone steaks, each about 1 1/2 pounds and 1 1/2 to 2 inches thick", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "NAME"), (9, 15, "UNIT"),
            (17, 68, "COMMENT")
        ]
    }),
    ("Finely grated zest and juice from 1 lime", {
        "entities": [
            (0,6,"PREP"),(7,13,"PREP"),(14,18,"NAME"),(19,22,"PREP"),(23,28,"NAME"),(29,33,"PREP"),(34,35,"QTY"),(36,40,"NAME") # Finely grated
        ]
    }),
    ("1 cup (240 ml) ice cubes", {
        "entities": [
            (0,1,"QTY"),(2,5,"UNIT"),(6,14,"COMMENT"),(15,18,"NAME"),(19,24,"NAME")
        ]
    }),
    ("*Note: Regular limes work fine. #NotBougie", {
        "entities": [
            (0, 42, "COMMENT")
        ]
    }),
    ("1 1/2 teaspoons confectioners? sugar", { # Question mark likely a typo for apostrophe
        "entities": [
            (0,5,"QTY"),(6,15,"UNIT"),(16,30,"NAME") # confectioners? sugar
        ]
    }),
    ("1/2 cup freshly squeezed Key lime juice*", {
        "entities": [
            (0,3,"QTY"),(4,7,"UNIT"),(8,15,"PREP"),(16,24,"PREP"),(25,28,"NAME"),(29,33,"NAME"),(34,40,"NAME") # Key lime juice*
        ]
    }),
    ("1 teaspoon grated Key lime zest*, plus more for topping", {
        "entities": [
            (0, 1, "QTY"), (2, 10, "UNIT"), (11, 17, "PREP"), (18, 21, "NAME"),
            (22, 26, "NAME"), (27, 32, "NAME"), # "zest*"
            (34, 55, "COMMENT")   # "plus more for topping"
        ]
    }),
    ("1 1/2 teaspoons grated Key lime zest*", {"entities": [(0,5,"QTY"),(6,15,"UNIT"),(16,22,"PREP"),(23,26,"NAME"),(27,31,"NAME"),(32,37,"NAME")]}), # Duplicate

    ("Jazz apricot can be substituted for the apricots, honey, and jalapenos", {
        "entities": [
            (0, 70, "COMMENT")
        ]
    }),
    ("1 (15 1/4-ounce) can apricots, drained and finely chopped", {
        "entities": [
            (0,1,"QTY"),(2,16,"COMMENT"),(17,20,"UNIT"),(21,29,"NAME"),(31,38,"PREP"),(43,49,"PREP"),(50,57,"PREP") # drained and finely chopped
        ]
    }),
    ("1/4 cup seeded and finely chopped jalapenos", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 14, "PREP"), (19, 25, "PREP"), # seeded, finely (and is O)
            (26, 33, "PREP"),     # "chopped"
            (34, 43, "NAME")      # "jalapenos"
        ]
    }),
    ("1/2 cup whipped topping, plus more for topping", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "PREP"), (16, 23, "NAME"),
            (25, 46, "COMMENT")   # "plus more for topping"
        ]
    }),
    ("2 shots espresso, or 1/2 cup very strong coffee", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 16, "NAME"),
            (18, 47, "ALT_NAME")  # "or 1/2 cup very strong coffee"
        ]
    }),
    ("1 cup ice cubes", {"entities": [(0,1,"QTY"),(2,5,"UNIT"),(6,9,"NAME"),(10,15,"NAME")]}), # Duplicate
    # Add these to your EXISTING_TRAIN_DATA list

    ("6 large tortillas", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "large"
            (8, 17, "NAME")       # "tortillas"
        ]
    }),
    ("1 tablespoon dark rum", {
        "entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),
            (13, 21, "NAME")      # "rum"
        ]
    }),
    ("2 tablespoons pine nuts, toasted, to garnish", {
        "entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 18, "NAME"),     # "pine"
            (19, 23, "NAME"),     # "nuts"
            (25, 32, "PREP"),     # "toasted"
            (34, 44, "COMMENT")   # "to garnish"
        ]
    }),
    # Corrected entry
    ("3 small eggplants (1 to 1 1/2 pounds) to make about 1 1/4 cups when roasted, pulped and sieved", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 17, "NAME"),
            (18, 37, "COMMENT"),  # "(1 to 1 1/2 pounds)"
            (38, 94, "COMMENT")   # "to make about 1 1/4 cups when roasted, pulped and sieved"
        ]
    }),
    ("1 cup Greek yogurt", {
        "entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 11, "NAME"),      # "Greek"
            (12, 18, "NAME")      # "yogurt"
        ]
    }),
    # Corrected entry
    ("1/4 teaspoon saffron threads, soaked in 2 tablespoons warm water", {
        "entities": [
            (0, 3, "QTY"), (4, 12, "UNIT"), (13, 20, "NAME"), (21, 28, "NAME"),
            (30, 64, "PREP")      # "soaked in 2 tablespoons warm water"
        ]
    }),
    ("3 cups peeled and shredded carrots", {
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),
            (7, 13, "PREP"),
            (18, 26, "PREP"),
            (27, 34, "NAME")
        ]
    }),
    ("4 cups reduced-fat milk", {
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),
            (7, 18, "PREP"),      # "reduced-fat"
            (19, 23, "NAME")
        ]
    }),
    ("1 ounce whisky", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),
            (8, 14, "NAME")
        ]
    }),
    ("2 pellets achiote", {
        "entities": [
            (0, 1, "QTY"),
            (2, 9, "UNIT"),       # "pellets"
            (10, 17, "NAME")      # "achiote"
        ]
    }),
    ("1/2 cup crushed biscotti", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 15, "PREP"),
            (16, 24, "NAME")
        ]
    }),
    ("1/2 teaspoon orange zest", {
        "entities": [
            (0, 3, "QTY"),
            (4, 12, "UNIT"),
            (13, 19, "NAME"),
            (20, 24, "NAME")
        ]
    }),
    ("3 tablespoons salted butter, at room temperature", {
        "entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 20, "PREP"),     # "salted"
            (21, 27, "NAME"),
            (29, 48, "COMMENT")   # "at room temperature"
        ]
    }),
    ("1/2 cup chicken fat", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 15, "NAME"),
            (16, 19, "NAME")
        ]
    }),
    ("2 tablespoons plus 2 teaspoons schmaltz (rendered chicken fat)", {
        "entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 30, "COMMENT"),  # "plus 2 teaspoons"
            (31, 39, "NAME"),     # "schmaltz"
            (40, 62, "COMMENT")   # "(rendered chicken fat)"
        ]
    }),
    ("1 pound frozen peeled and deveined jumbo shrimp (16/20)", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),
            (8, 14, "PREP"),
            (15, 21, "PREP"),
            (26, 34, "PREP"),
            (35, 40, "PREP"),     # "jumbo" (size descriptor)
            (41, 47, "NAME"),
            (48, 55, "COMMENT")   # "(16/20)"
        ]
    }),
    ("4 (4-ounce) sole fillets, hake, flounder or other white fish", {
        "entities": [
            (0, 1, "QTY"),
            (2, 11, "COMMENT"),   # "(4-ounce)"
            (12, 16, "NAME"),     # "sole"
            (17, 24, "UNIT"),     # "fillets"
            (26, 30, "ALT_NAME"), # "hake"
            (32, 60, "ALT_NAME")  # "flounder or other white fish"
        ]
    }),
    ("1 1/2 cups rainbow nonpareils, large and small mixed", {
        "entities": [
            (0, 5, "QTY"), (6, 10, "UNIT"), (11, 18, "NAME"), (19, 29, "NAME"),
            (31, 52, "COMMENT")   # "large and small mixed"
        ]
    }),
    ("1 cup diced firm tofu", {
        "entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 11, "PREP"),
            (12, 16, "PREP"),     # "firm" (descriptor of tofu)
            (17, 21, "NAME")
        ]
    }),
    ("4 ounces rum, such as Mount Gay", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 12, "NAME"),
            (14, 31, "COMMENT")   # "such as Mount Gay"
        ]
    }),
    ("1/2 cup small dice of mixed yellow, green and red bell pepper, for garnish", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "PREP"), (14, 18, "PREP"), (19, 21, "PREP"),
            (22, 61, "NAME"),      # "mixed yellow, green and red bell pepper"
            (63, 74, "COMMENT")    # "for garnish"
        ]
    }),
    ("1 pound orzo", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),
            (8, 12, "NAME")
        ]
    }),
    ("1 cup pearled farro", {
        "entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 13, "PREP"),      # "pearled"
            (14, 19, "NAME")
        ]
    }),
    ("1 small bulb fennel, trimmed, halved and thinly sliced", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),
            (8, 12, "UNIT"),
            (13, 19, "NAME"),
            (21, 28, "PREP"),     # "trimmed"
            (30, 36, "PREP"),     # "halved"
            (41, 47, "PREP"),     # "thinly"
            (48, 54, "PREP")      # "sliced"
        ]
    }),
    ("1 cup Greek yogurt", {"entities": [(0,1,"QTY"),(2,5,"UNIT"),(6,11,"NAME"),(12,18,"NAME")]}), # Duplicate
    ("1/4 cup toasted pine nuts* see Cook's Note", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 15, "PREP"),
            (16, 20, "NAME"),
            (21, 26, "NAME"),     # "nuts*"
            (27, 42, "COMMENT")   # "see Cook's Note"
        ]
    }),
    ("1 pear", {"entities": [(0,1,"QTY"),(2,6,"NAME")]}),
    ("4 pounds wings, separated into wingettes and drumettes, tips discarded", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "NAME"),
            (16, 54, "PREP"),     # "separated into wingettes and drumettes"
            (56, 70, "COMMENT")   # "tips discarded"
        ]
    }),
    ("5 tablespoons whole Greek yogurt", {
        "entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 19, "PREP"),     # "whole"
            (20, 25, "NAME"),
            (26, 32, "NAME")
        ]
    }),
    ("1 teaspoon black mustard seeds", {
        "entities": [
            (0, 1, "QTY"),
            (2, 10, "UNIT"),
            (11, 16, "NAME"),     # "black"
            (17, 24, "NAME"),     # "mustard"
            (25, 30, "NAME")      # "seeds"
        ]
    }),
    ("Small handful fresh cilantro, leaves and soft stems rustically ripped into bite-size pieces", {
        "entities": [
            (0, 5, "UNIT"), (6, 13, "UNIT"), (14, 19, "PREP"), (20, 28, "NAME"),
            (30, 91, "PREP")
        ]
    }),
    ("Big pinch ground cardamom", {
        "entities": [
            (0, 3, "QTY"),        # "Big"
            (4, 9, "UNIT"),
            (10, 16, "NAME"),     # "ground cardamom" (as per your rule for ground spices)
            (17, 25, "NAME")      # (oops, already included in above) -> (10,25,"NAME")
        ]
    }),
    ("Big pinch ground cardamom", { # Corrected version
        "entities": [
            (0, 3, "QTY"),        # "Big"
            (4, 9, "UNIT"),       # "pinch"
            (10, 25, "NAME")      # "ground cardamom"
        ]
    }),
    ("Big pinch chaat masala", {
        "entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),
            (10, 15, "NAME"),     # "chaat"
            (16, 22, "NAME")      # "masala"
        ]
    }),
    ("3 large ears corn, husks and silk removed", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 12, "UNIT"), (13, 17, "NAME"),
            (19, 41, "PREP")
        ]
    }),
    # Assuming "Olive oil" is a new ingredient line
    ("Olive oil", {"entities": [(0,5,"NAME"),(6,9,"NAME")]}),

    ("1 pound peeled and deveined large shrimp", {
        "entities": [
            (0,1,"QTY"),(2,7,"UNIT"),(8,14,"PREP"),(19,27,"PREP"),(28,33,"UNIT"),(34,40,"NAME")
        ]
    }),
    ("4 ounces dark rum", {
        "entities": [
            (0,1,"QTY"),(2,8,"UNIT"),(9,17,"NAME")
        ]
    }),
    ("1 package (10 oz.) frozen chopped spinach, thawed and squeezed dry", {
        "entities": [
            (0, 1, "QTY"), (2, 9, "UNIT"), (10, 18, "COMMENT"), (19, 25, "PREP"),
            (26, 33, "PREP"), (34, 41, "NAME"), (43, 49, "PREP"),
            (54, 66, "PREP")      # "squeezed dry"
        ]
    }),
    ("1/2 pound turnips, diced", {
        "entities": [
            (0,3,"QTY"),(4,9,"UNIT"),(10,17,"NAME"),(19,24,"PREP")
        ]
    }),
    ("2 pounds goat head, organs and feet (2 pounds lamb meat may be substituted)", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 13, "NAME"), (14, 18, "NAME"),
            (20, 26, "COMMENT"), (31, 35, "COMMENT"),
            (36, 75, "COMMENT")
        ]
    }),
    ("1 1/4 teaspoons black mustard seeds", {
        "entities": [
            (0,5,"QTY"),(6,15,"UNIT"),(16,21,"NAME"),(22,29,"NAME"),(30,35,"NAME")
        ]
    }),
    ("2 cups loosely packed fresh morels", {
        "entities": [
            (0,1,"QTY"),(2,6,"UNIT"),(7,14,"PREP"),(15,21,"PREP"),(22,27,"PREP"),(28,34,"NAME")
        ]
    }),
    ("1 cup peeled and diced kiwi (about 2 or 3 whole kiwi)", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"), (6, 12, "PREP"), (17, 22, "PREP"),
            (23, 27, "NAME"),
            (28, 53, "COMMENT")
        ]
    }),
    ("1 cup diced pineapple (fresh or canned in juice)", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"), (6, 11, "PREP"), (12, 21, "NAME"),
            (22, 48, "COMMENT")
        ]
    }),
    ("1/2 cup 151-proof rum", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (8, 17, "PREP"),      # "151-proof"
            (18, 21, "NAME")      # "rum"
        ]
    }),
    ("1 cup macadamia nuts, toasted and coarsely ground", {
        "entities": [
            (0,1,"QTY"),(2,5,"UNIT"),(6,15,"NAME"),(16,20,"NAME"),
            (22,29,"PREP"),(34,42,"PREP"),(43,49,"PREP") # toasted and coarsely ground
        ]
    }),
    ("2 1/2 cups lightly crushed potato chips with ridges", {
        "entities": [
            (0, 5, "QTY"), (6, 10, "UNIT"), (11, 18, "PREP"), (19, 26, "PREP"),
            (27, 33, "NAME"),
            (34, 39, "NAME"),     # "chips"
            (40, 51, "COMMENT")   # "with ridges"
        ]
    }),
    ("Nonstick cooking spray, for the parchment", {
        "entities": [
            (0, 8, "PREP"), (9, 16, "NAME"), (17, 22, "NAME"),
            (24, 41, "COMMENT")
        ]
    }),
    ("4 ounces kombu", {
        "entities": [
            (0,1,"QTY"),(2,8,"UNIT"),(9,14,"NAME")
        ]
    }),
    ("2 cups cooked and cooled Carolina Gold rice (from 3/4 cup uncooked rice)", {
        "entities": [
            (0,1,"QTY"),(2,6,"UNIT"),(7,13,"PREP"),(18,24,"PREP"),(25,33,"NAME"),(34,38,"NAME"),(39,43,"NAME"), # Carolina Gold rice
            (44,71,"COMMENT") # (from 3/4 cup uncooked rice)
        ]
    }),
    ("Canola or vegetable oil, for frying", {
        "entities": [
            (0, 6, "NAME"),
            (7, 23, "ALT_NAME"),  # "or vegetable oil"
            (25, 35, "COMMENT")   # "for frying"
        ]
    }),
    ("1/4 cup spiced rum", {
        "entities": [
            (0,3,"QTY"),(4,7,"UNIT"),(8,18,"NAME")
        ]
    }),
    ("About 1/3 cup EVOO", {
        "entities": [
            (0,5,"COMMENT"),(6,9,"QTY"),(10,13,"UNIT"),(14,18,"NAME")
        ]
    }),
    ("Generous handful of fresh cilantro leaves, chopped", {
        "entities": [
            (0,8,"QTY"),(9,16,"UNIT"),(17,19,"PREP"),(20,25,"PREP"),(26,34,"NAME"),(35,41,"NAME"),(43,50,"PREP")
        ]
    }),
    ("1 pound haricot verts, blanched and shocked", {
        "entities": [
            (0,1,"QTY"),(2,7,"UNIT"),(8,15,"NAME"),(16,21,"NAME"),(23,31,"PREP"),(36,43,"PREP")
        ]
    }),
    ("12 scallops", { "entities": [(0,2,"QTY"),(3,11,"NAME")]}),


    # Add these to your EXISTING_TRAIN_DATA list

    ("1/2 cup walnut pieces", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 14, "NAME"),      # "walnut"
            (15, 21, "PREP")      # "pieces" (form/preparation)
        ]
    }),
    ("1/3 cup minced scallion, including green", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 14, "PREP"),
            (15, 23, "NAME"),     # "scallion"
            (25, 40, "COMMENT")   # "including green"
        ]
    }),
    ("1/2 pound cooked shrimp or other shellfish", {
        "entities": [
            (0, 3, "QTY"), (4, 9, "UNIT"), (10, 16, "PREP"), (17, 23, "NAME"),
            (24, 42, "ALT_NAME")  # "or other shellfish"
        ]
    }),
    ("1/2 pound mixed baby greens", {
        "entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),
            (10, 15, "PREP"),     # "mixed"
            (16, 20, "NAME"),     # "baby"
            (21, 27, "NAME")      # "greens"
        ]
    }),
    ("1 pound package instant polenta", {
        "entities": [
            (0, 1, "QTY"),
            (2, 7, "UNIT"),       # "pound" (primary unit)
            (8, 15, "UNIT"),      # "package" (container type, or COMMENT if pound is always preferred)
            (16, 23, "PREP"),     # "instant"
            (24, 31, "NAME")      # "polenta"
        ]
    }),
    ("Vegetable oil, for greasing pan", {
        "entities": [
            (0, 9, "NAME"), (10, 13, "NAME"),
            (15, 31, "COMMENT")   # "for greasing pan"
        ]
    }),
    ("1 pound cavatelli or any short pasta (penne, paccheri, ziti…)", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 17, "NAME"),
            (18, 61, "ALT_NAME")  # "or any short pasta (penne, paccheri, ziti…)"
        ]
    }),
    ("1 teaspoon prepared horseradish", {
        "entities": [
            (0, 1, "QTY"),
            (2, 10, "UNIT"),
            (11, 19, "PREP"),
            (20, 31, "NAME")
        ]
    }),
    ("6 frozen parathas (see Cook's Note)", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "PREP"), (9, 17, "NAME"),
            (18, 35, "COMMENT")   # "(see Cook's Note)"
        ]
    }),
    ("6 ears fresh corn on the cob, shucked", {
        "entities": [
            (0, 1, "QTY"),
            (2, 6, "UNIT"),       # "ears"
            (7, 12, "PREP"),      # "fresh"
            (13, 17, "NAME"),     # "corn"
            (18, 28, "COMMENT"),  # "on the cob"
            (30, 37, "PREP")      # "shucked"
        ]
    }),
    ("15 ounces drained canned chestnuts packed in water", {
        "entities": [
            (0, 2, "QTY"),
            (3, 9, "UNIT"),
            (10, 17, "PREP"),     # "drained"
            (18, 24, "PREP"),     # "canned"
            (25, 34, "NAME"),     # "chestnuts"
            (35, 50, "PREP")      # "packed in water"
        ]
    }),
    ("1/2 cup stemmed and halved porcini mushrooms", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "PREP"), (20, 26, "PREP"),
            (27, 34, "NAME"),
            (35, 44, "NAME")      # "mushrooms"
        ]
    }),
    ("1 tablespoon Essence, recipe follows", {
        "entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),
            (13, 20, "NAME"),     # "Essence"
            (22, 36, "COMMENT")   # "recipe follows"
        ]
    }),
    ("1 cup diced roasted, seeded and peeled Anaheim chilies", {
        "entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 11, "PREP"),      # "diced"
            (12, 19, "PREP"),     # "roasted"
            (21, 27, "PREP"),     # "seeded"
            (32, 38, "PREP"),     # "peeled"
            (39, 46, "NAME"),     # "Anaheim"
            (47, 54, "NAME")      # "chilies"
        ]
    }),
    ("1/4 cup plus 2 tablespoons jarred grated horseradish (with liquid)", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 26, "COMMENT"),  # "plus 2 tablespoons"
            (27, 33, "PREP"),     # "jarred"
            (34, 40, "PREP"),     # "grated"
            (41, 52, "NAME"),     # "horseradish"
            (53, 66, "COMMENT")   # "(with liquid)"
        ]
    }),
    ("One 3-pound corned beef brisket (uncooked), in brine", {
        "entities": [
            (0, 3, "QTY"), (4, 11, "COMMENT"), (12, 18, "NAME"), (19, 23, "NAME"),
            (24, 31, "NAME"),
            (32, 43, "COMMENT"),  # "(uncooked)," - This aligns with the tokens.
            (44, 52, "PREP")      # "in brine"
        ]
    }),
    ("1/4 cup plus 2 tablespoons jarred grated horseradish (with liquid)", {"entities": [(0,3,"QTY"),(4,7,"UNIT"),(8,26,"COMMENT"),(27,33,"PREP"),(34,40,"PREP"),(41,52,"NAME"),(53,66,"COMMENT")]}), # Duplicate
    ("1/2 medium yellow medium onion, grated", { # "medium" appears twice, likely one is for size, one for type/descriptor
        "entities": [
            (0, 3, "QTY"),
            (4, 10, "UNIT"),      # "medium" (size)
            (11, 17, "PREP"),     # "yellow" (color/type)
            (18, 24, "COMMENT"),  # "medium" (perhaps descriptor, less clear)
            (25, 30, "NAME"),
            (32, 38, "PREP")
        ]
    }),
    ("1 can (26 ounces) Campbell's® Condensed Cream of Mushroom Soup (Regular or 98% Fat Free)", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"), (6, 17, "COMMENT"),
            (18, 57, "NAME"),     # "Campbell's® Condensed Cream of Mushroom"
            (58, 88, "COMMENT")   # "Soup (Regular or 98% Fat Free)"
        ]
    }),
    ("2 bags (16 ounces each) frozen vegetable combination (broccoli, cauliflower, carrots), cooked and drained", {
        "entities": [
            (0, 1, "QTY"), (2, 6, "UNIT"),
            (7, 23, "COMMENT"),   # "(16 ounces each)"
            (24, 30, "PREP"),     # "frozen"
            (31, 40, "NAME"),     # "vegetable"
            (41, 52, "NAME"),     # "combination"
            (53, 85, "COMMENT"),  # "(broccoli, cauliflower, carrots)"
            (87, 105, "PREP")     # "cooked and drained"
        ]
    }),
    ("2 to 3 packages pre-prepared won ton wrappers", {
        "entities": [
            (0, 6, "QTY"), (7, 15, "UNIT"),
            (16, 28, "PREP"),     # "pre-prepared"
            (29, 32, "NAME"),     # "won"
            (33, 36, "NAME"),     # "ton"
            (37, 45, "NAME")      # "wrappers"
        ]
    }),
    ("Few drops of truffle oil", { # "Few" is QTY
        "entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),       # "drops"
            (10, 12, "PREP"),     # "of"
            (13, 20, "NAME"),     # "truffle"
            (21, 24, "NAME")      # "oil"
        ]
    }),
    ("6 cups mixed baby greens", {"entities": [(0,1,"QTY"),(2,6,"UNIT"),(7,12,"PREP"),(13,17,"NAME"),(18,24,"NAME")]}), # Duplicate
    ("16 oz. ginger ale", {
        "entities": [
            (0, 2, "QTY"),        # "16"
            (3, 6, "UNIT"),       # "oz." (including period)
            (7, 13, "NAME"),
            (14, 17, "NAME")
        ]
    }),
    ("1 tablespoons peeled and finely chopped ginger", { # tablespoons is plural, 1 is singular
        "entities": [
            (0, 1, "QTY"),
            (2, 13, "UNIT"),
            (14, 20, "PREP"),
            (25, 31, "PREP"),
            (32, 39, "PREP"),
            (40, 46, "NAME")
        ]
    }),
    ("16 ounces leftover Oil Poached Flounder, recipe follows, flaked", {
        "entities": [
            (0, 2, "QTY"),
            (3, 9, "UNIT"),
            (10, 18, "PREP"),     # "leftover"
            (19, 22, "NAME"),     # "Oil"
            (23, 30, "PREP"),     # "Poached"
            (31, 39, "NAME"),     # "Flounder"
            (41, 55, "COMMENT"),
            (57, 63, "PREP")      # "flaked"
        ]
    }),
    ("1/2 wet cured, smoked ham, about 5 to 7 1/2 pounds", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "PREP"), (8, 13, "PREP"), (15, 21, "PREP"),
            (22, 25, "NAME"),
            (27, 50, "COMMENT")   # "about 5 to 7 1/2 pounds"
        ]
    }),
    ("Prepared horseradish", {"entities": [(0,8,"PREP"),(9,20,"NAME")]}),
    ("Prepared mustard", {"entities": [(0,8,"PREP"),(9,16,"NAME")]}),
    ("1 cup coarsely ground or chopped pistachios, for serving", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"), (6, 14, "PREP"), (15, 21, "NAME"), # Assuming "ground" is NAME here, or PREP
            (22, 32, "ALT_PREP"), # "or chopped"
            (33, 43, "NAME"),     # "pistachios"
            (45, 56, "COMMENT")   # "for serving"
        ]
    }),
    ("1 1/2 cups polenta", {
        "entities": [
            (0,5,"QTY"),(6,10,"UNIT"),(11,18,"NAME")
        ]
    }),
    ("1 box cous cous (approximately 16 ounces)", {
        "entities": [
            (0,1,"QTY"),(2,5,"UNIT"),(6,10,"NAME"),(11,15,"NAME"),
            (16,40,"COMMENT")
        ]
    }),
    ("Ramekin for molding", {
        "entities": [
            (0, 7, "NAME"),
            (8, 19, "COMMENT")   # "for molding"
        ]
    }),
    ("1 1/4 pounds haricots verts or green beans, trimmed", {
        "entities": [
            (0, 5, "QTY"), (6, 12, "UNIT"), (13, 21, "NAME"), (22, 27, "NAME"),
            (28, 43, "ALT_NAME"), # "or green beans,"
            (44, 51, "PREP")      # "trimmed"
        ]
    }),
    ("8 cups seeded and diced heirloom tomatoes", {
        "entities": [
            (0,1,"QTY"),(2,6,"UNIT"),(7,13,"PREP"),(18,23,"PREP"),(24,32,"NAME"),(33,41,"NAME")
        ]
    }),
    ("1 salmon filet (about 3 pounds), pin bones removed and halved horizontally", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "NAME"), (9, 14, "UNIT"), (15, 31, "COMMENT"),
            (33, 61, "PREP"),     # "pin bones removed and halved"
            (62, 74, "PREP")      # "horizontally"
        ]
    }),
    ("1 1/2 teaspoons liquid smoke", {
        "entities": [
            (0,5,"QTY"),(6,15,"UNIT"),(16,22,"NAME"),(23,28,"NAME")
        ]
    }),
    ("1 tablespoon (9.3 grams) instant yeast", {
        "entities": [
            (0,1,"QTY"),(2,12,"UNIT"),(13,24,"COMMENT"),(25,32,"PREP"),(33,38,"NAME")
        ]
    }),
    ("3 pounds skin-on, bone-in chicken parts (breasts halved crosswise)", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 16, "PREP"), (18, 25, "PREP"),
            (26, 33, "NAME"), (34, 39, "NAME"),
            (40, 66, "COMMENT")
        ]
    }),
    ("1 1/2 cups polenta (not quick-cooking)", {
        "entities": [
            (0,5,"QTY"),(6,10,"UNIT"),(11,18,"NAME"),(19,38,"COMMENT")
        ]
    }),
    ("3 oranges, juiced", {
        "entities": [
            (0,1,"QTY"),(2,9,"NAME"),(11,17,"PREP")
        ]
    }),
    ("3 tablespoons freshly grated Parmesan, plus 1/4 cup freshly grated", {
        "entities": [
            (0, 1, "QTY"), (2, 13, "UNIT"), (14, 21, "PREP"), (22, 28, "PREP"),
            (29, 37, "NAME"),
            (39, 66, "COMMENT")
        ]
    }),
    ("Minced fresh flat-leaf parsley leaves", { # No QTY/UNIT, implies "to taste" or for garnish
        "entities": [
            (0,6,"PREP"),(7,12,"PREP"),(13,22,"NAME"),(23,30,"NAME"),(31,37,"NAME")
        ]
    }),
    ("2 marshmallows, for garnish", {
        "entities": [
            (0,1,"QTY"),(2,14,"NAME"),(16,27,"COMMENT")
        ]
    }),
    ("1/3 cup soybean or safflower oil", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "NAME"),
            (16, 32, "ALT_NAME")  # "or safflower oil"
        ]
    }),
    ("3 large russet potatoes scrubbed", {
        "entities": [
            (0,1,"QTY"),(2,7,"UNIT"),(8,14,"NAME"),(15,23,"NAME"),(24,32,"PREP")
        ]
    }),
    ("2 tablespoons, 5 or 6 sprigs, fresh thyme, leaves stripped and chopped", {
        "entities": [
            (0, 1, "QTY"), (2, 13, "UNIT"), (15, 28, "ALT_UNIT_QTY"),
            (30, 35, "PREP"), (36, 41, "NAME"),
            (43, 70, "PREP")      # "leaves stripped and chopped"
        ]
    }),
    ("1 teaspoon ground toasted cardamom", {
        "entities": [
            (0, 1, "QTY"), (2, 10, "UNIT"),
            (11, 34, "NAME")      # "ground toasted cardamom"
        ]
    }),
    ("1/2 cup finely chopped fresh flat-leaf parsley, or a combination of parsley and fresh mint", {
        "entities": [
            (0,3,"QTY"),(4,7,"UNIT"),(8,14,"PREP"),(15,22,"PREP"),(23,28,"PREP"),(29,38,"NAME"),(39,46,"NAME"), # fresh flat-leaf parsley
            (48,90,"ALT_NAME") # or a combination of parsley and fresh mint
        ]
    }),
    ("1/2 cup panko or homemade breadcrumbs", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "NAME"),
            (14, 37, "ALT_NAME")  # "or homemade breadcrumbs"
        ]
    }),
    ("1 pound thinly sliced serrano ham (about 24 slices)", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 14, "PREP"), (15, 21, "PREP"),
            (22, 29, "NAME"), (30, 33, "NAME"),
            (34, 51, "COMMENT")   # "(about 24 slices)"
        ]
    }),
    ("3 bunches (about 1 pound) baby turnips (ping pong ball size), greens and soft stems reserved", {
        "entities": [
            (0, 1, "QTY"), (2, 9, "UNIT"),
            (10, 25, "COMMENT"),  # "(about 1 pound)"
            (26, 30, "NAME"),     # "baby"
            (31, 38, "NAME"),     # "turnips"
            (39, 60, "COMMENT"),  # "(ping pong ball size)"
            (62, 92, "COMMENT")   # "greens and soft stems reserved"
        ]
    }),
    ("3/4 cup toasted pecans finely chopped", {
        "entities": [
            (0,3,"QTY"),(4,7,"UNIT"),(8,15,"PREP"),(16,22,"NAME"),(23,29,"PREP"),(30,37,"PREP")
        ]
    }),
    ("3 tablespoons ginger wine (recommended: Stone's Ginger Wine)", {
        "entities": [
            (0,1,"QTY"),(2,13,"UNIT"),(14,20,"NAME"),(21,25,"NAME"),
            (26,60,"COMMENT")
        ]
    }),
    ("1/4 cup finely chopped glace baby ginger", {
        "entities": [
            (0,3,"QTY"),(4,7,"UNIT"),(8,14,"PREP"),(15,22,"PREP"),(23,28,"NAME"),(29,33,"NAME"),(34,40,"NAME") # glace baby ginger
        ]
    }),
    ("3/4 pound total (1/4 pound each) thinly sliced Italian meats: sliced sopressata, capicola and Genoa salami", {
        "entities": [
            (0, 3, "QTY"), (4, 9, "UNIT"), (10, 15, "COMMENT"),
            (16, 32, "COMMENT"),  # "(1/4 pound each)"
            (33, 39, "PREP"),     # "thinly"
            (40, 46, "PREP"),     # "sliced"
            (47, 54, "NAME"),     # "Italian"
            (55, 60, "NAME"),     # "meats"
            (60, 106, "COMMENT") # ": sliced sopressata, capicola and Genoa salami"
        ]
    }),
    ("1 jar, 16 ounces, roasted red peppers, drained and sliced", { # "1 jar" QTY/UNIT, "16 ounces" COMMENT
        "entities": [
            (0,1,"QTY"),(2,5,"UNIT"),(7,16,"COMMENT"),(18,25,"PREP"),(26,29,"NAME"),(30,37,"NAME"),
            (39,46,"PREP"),(51,57,"PREP")
        ]
    }),
    ("2/3 pound total Italian table cheeses, 1/3 pound each of 2 varieties: sharp provolone, Pepato, Fontina, Parmigian-Reggiano", {
        "entities": [
            (0, 3, "QTY"), (4, 9, "UNIT"), (10, 15, "COMMENT"), (16, 23, "NAME"),
            (24, 29, "NAME"), (30, 37, "NAME"),
            (39, 68, "COMMENT"),  # "1/3 pound each of 2 varieties"
            (68, 122, "COMMENT") # ": sharp provolone, Pepato, Fontina, Parmigian-Reggiano"
        ]
    }),
    ("1 Granny Smith apple", {
        "entities": [
            (0,1,"QTY"),(2,8,"NAME"),(9,14,"NAME"),(15,20,"NAME")
        ]
    }),
    ("1 1/4-ounce packet unflavored powdered gelatin", {
        "entities": [
            (0, 1, "QTY"),
            (2, 18, "UNIT"),      # "1/4-ounce packet"
            (19, 29, "PREP"),     # "unflavored"
            (30, 38, "PREP"),     # "powdered"
            (39, 46, "NAME")      # "gelatin"
        ]
    }),
    ("2 oranges", {"entities": [(0,1,"QTY"),(2,9,"NAME")]}),
    ("1 tablespoon finely chopped fines herbes (chervil, parsley, tarragon, and chives)", {
        "entities": [
            (0,1,"QTY"),(2,12,"UNIT"),(13,19,"PREP"),(20,27,"PREP"),(28,33,"NAME"),(34,40,"NAME"), # fines herbes
            (41,80,"COMMENT")
        ]
    }),
    ("1 1/2 pounds peeled and deveined large shrimp", {"entities": [(0,5,"QTY"),(6,12,"UNIT"),(13,19,"PREP"),(24,32,"PREP"),(33,38,"UNIT"),(39,45,"NAME")]}), # Duplicate
    ("1 1/2 pounds medium peeled and deveined shrimp, tails removed", {
        "entities": [
            (0, 5, "QTY"), (6, 12, "UNIT"), (13, 19, "UNIT"), (20, 26, "PREP"),
            (31, 39, "PREP"), (40, 46, "NAME"),
            (48, 61, "PREP")      # "tails removed"
        ]
    }),
    ("6 cups zucchini noodles, from 2 medium zucchinis (about 1 pound)", {
        "entities": [
            (0,1,"QTY"),(2,6,"UNIT"),(7,15,"NAME"),(16,23,"NAME"),
            (25,64,"COMMENT") # from 2 medium zucchinis (about 1 pound)
        ]
    }),
    ("2 (12-ounce) boneless rib eye steaks", {
        "entities": [
            (0,1,"QTY"),(2,12,"COMMENT"),(13,21,"PREP"),(22,25,"NAME"),(26,29,"NAME"),(30,36,"UNIT")
        ]
    }),
    ("2 cups small-diced, peeled russet potatoes (1 large russet)", {
        "entities": [
            (0,1,"QTY"),(2,6,"UNIT"),(7,18,"PREP"),(20,26,"PREP"),(27,33,"NAME"),(34,42,"NAME"), # small-diced, peeled
            (43,59,"COMMENT")
        ]
    }),
    ("4 cups small-diced zucchini (green/yellow) (5 small zucchini)", {
        "entities": [
            (0,1,"QTY"),(2,6,"UNIT"),(7,18,"PREP"),(19,27,"NAME"),
            (28,42,"COMMENT"),(43,60,"COMMENT") # (green/yellow), (5 small zucchini)
        ]
    }),
    ("1 tablespoon finely chopped rosemary or thyme leaves", {
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"), (13, 19, "PREP"), (20, 27, "PREP"),
            (28, 36, "NAME"),
            (37, 52, "ALT_NAME")  # "or thyme leaves"
        ]
    }),
    ("12 ounces macaroni (or your choice of pasta)", {
        "entities": [
            (0,2,"QTY"),(3,9,"UNIT"),(10,18,"NAME"),
            (19,44,"COMMENT")
        ]
    }),
    ("2 tablespoons ghee", {
        "entities": [
            (0,1,"QTY"),(2,13,"UNIT"),(14,18,"NAME")
        ]
    }),
    ("1 (8-ounce) package frozen artichoke hearts, thawed", {
        "entities": [
            (0, 1, "QTY"),
            (2, 11, "COMMENT"),  # "(8-ounce)"
            (12, 19, "UNIT"),    # "package"
            (20, 26, "PREP"),    # "frozen"
            (27, 36, "NAME"),    # "artichoke"
            (37, 43, "NAME"),    # "hearts"
            (45, 51, "PREP")     # "thawed"
        ]
    }),
    ("1/3 cup olive oil, plus extra for drizzling", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 13, "NAME"), (14, 17, "NAME"),
            (19, 43, "COMMENT")   # "plus extra for drizzling"
        ]
    }),
    ("5 cups (5 ounces) baby arugula", {
        "entities": [
            (0,1,"QTY"),(2,6,"UNIT"),(7,17,"COMMENT"),(18,22,"NAME"),(23,30,"NAME")
        ]
    }),
    ("1 pound cherry or grape tomatoes, halved through the stem", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 14, "NAME"),
            (15, 32, "ALT_NAME"), # "or grape tomatoes"
            (34, 57, "PREP")      # "halved through the stem"
        ]
    }),
    ("4 fillets walleye or other white flaky fish such as black bass or tilapia (about 1 pound 1 ounce)", {
        "entities": [
            (0, 1, "QTY"), (2, 9, "UNIT"), (10, 17, "NAME"),
            (18, 73, "ALT_NAME"), # "or other white flaky fish such as black bass or tilapia"
            (74, 97, "COMMENT")   # "(about 1 pound 1 ounce)"
        ]
    }),
    # Add these to your training data file

    ("2 lemons juiced and zested", {
        "entities": [
            (0, 1, "QTY"),
            (2, 8, "NAME"),       # "lemons"
            (9, 15, "PREP"),      # "juiced"
            (20, 26, "PREP")      # "zested"
        ]
    }),
    ("1 cup (250 milliliters) dry white wine", {
        "entities": [
            (0, 1, "QTY"),
            (2, 5, "UNIT"),
            (6, 23, "COMMENT"),   # "(250 milliliters)"
            (24, 27, "PREP"),     # "dry"
            (28, 33, "NAME"),     # "white"
            (34, 38, "NAME")      # "wine"
        ]
    }),
    ("2 cups broccoli florets", {
        "entities": [
            (0, 1, "QTY"), (2, 6, "UNIT"), (7, 15, "NAME"),
            (16, 23, "NAME")      # "florets"
        ]
    }),
    ("1 tablespoon herbs de Provence", {
        "entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),
            (13, 18, "NAME"),     # "herbs"
            (19, 21, "NAME"),     # "de"
            (22, 30, "NAME")      # "Provence"
        ]
    }),
    ("3 slices bacon, thinly sliced crosswise", {
        "entities": [
            (0, 1, "QTY"),
            (2, 8, "UNIT"),
            (9, 14, "NAME"),
            (16, 22, "PREP"),     # "thinly"
            (23, 29, "PREP"),     # "sliced"
            (30, 39, "PREP")      # "crosswise"
        ]
    }),
    ("2 (14-ounce) pork tenderloins, each halved crosswise", {
        "entities": [
            (0, 1, "QTY"), (2, 12, "COMMENT"), (13, 17, "NAME"), (18, 29, "NAME"),
            (31, 52, "PREP")      # "each halved crosswise"
        ]
    }),
    ("Store-bought dinner rolls or biscuits, for serving", {
        "entities": [
            (0, 12, "PREP"), (13, 19, "NAME"), (20, 25, "NAME"),
            (26, 38, "ALT_NAME"), # "or biscuits,"
            (39, 50, "COMMENT")   # "for serving"
        ]
    }),
    ("1/4 cup chopped roasted cashews for garnish", {
        "entities": [
            (0, 3, "QTY"),
            (4, 7, "UNIT"),
            (8, 15, "PREP"),
            (16, 23, "PREP"),
            (24, 31, "NAME"),     # "cashews"
            (32, 43, "COMMENT")   # "for garnish"
        ]
    }),
    ("1 jar (15 ounces) Patak's® Korma Curry Cooking Sauce", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"), (6, 17, "COMMENT"),
            (18, 52, "NAME")      # "Patak's® Korma Curry Cooking Sauce"
        ]
    }),
    ("1 1/2 pounds coarsely ground turkey (dark meat)", {
        "entities": [
            (0, 5, "QTY"), (6, 12, "UNIT"), (13, 21, "PREP"), (22, 28, "PREP"),
            (29, 35, "NAME"),
            (36, 47, "COMMENT")   # "(dark meat)"
        ]
    }),
    ("3 large, ripe tomatoes, seeded and cut into 1/2-inch cubes", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (9, 13, "PREP"), (14, 22, "NAME"),
            (24, 30, "PREP"), # seeded
            # "and" is O (31-34)
            (35, 58, "PREP")      # "cut into 1/2-inch cubes"
        ]
    }),
    ("3/4 pound tomatillos, husked, washed, cored and diced", {
        "entities": [
            (0, 3, "QTY"),
            (4, 9, "UNIT"),
            (10, 20, "NAME"),
            (22, 28, "PREP"),     # "husked"
            (30, 36, "PREP"),     # "washed"
            (38, 43, "PREP"),     # "cored"
            (48, 53, "PREP")      # "diced"
        ]
    }),
    ("1 cup (77 g) pineapple chunks", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"),
            (6, 12, "COMMENT"),   # "(77 g)"
            (13, 22, "NAME"),     # "pineapple"
            (23, 29, "PREP")      # "chunks"
        ]
    }),
    ("12 cups cubed crustless, stale sourdough or peasant bread", {
        "entities": [
            (0, 2, "QTY"),
            (3, 7, "UNIT"),
            (8, 13, "PREP"),      # "cubed"
            (14, 23, "PREP"),     # "crustless"
            (25, 30, "PREP"),     # "stale"
            (31, 40, "NAME"),     # "sourdough"
            (41, 57, "ALT_NAME"), # "or peasant bread"
        ]
    }),
    ("1 tablespoon coriander seeds, toasted and crushed", {
        "entities": [
            (0, 1, "QTY"),
            (2, 12, "UNIT"),
            (13, 22, "NAME"),
            (23, 28, "NAME"),
            (30, 37, "PREP"),
            (42, 49, "PREP")
        ]
    }),
    ("One 13-rib pork loin, membrane between the rib bones slit to allow the pork to curl around and stand up", {
        "entities": [
            (0, 3, "QTY"), (4, 10, "COMMENT"), (11, 15, "NAME"), (16, 20, "NAME"),
            (22, 103, "COMMENT")
        ]
    }),
    ("1 cup, plus 1 teaspoon, granulated sugar", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"),
            (7, 23, "COMMENT"),   # "plus 1 teaspoon,"
            (24, 34, "PREP"),     # "granulated"
            (35, 40, "NAME")      # "sugar"
        ]
    }),
    ("1/2 cup plus 1 teaspoon vegetable shortening", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (8, 23, "COMMENT"),   # "plus 1 teaspoon"
            (24, 33, "NAME"),     # "vegetable"
            (34, 44, "NAME")      # "shortening"
        ]
    }),
    ("1 tablespoon brandy", {
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"), (13, 19, "NAME")
        ]
    }),
    ("1 large head escarole, washed and hand torn", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 12, "UNIT"), (13, 21, "NAME"),
            (23, 29, "PREP"), (34, 38, "PREP"), (39, 43, "PREP") # washed and hand torn
        ]
    }),
    ("6 salami slices", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "NAME"), (9, 15, "UNIT")
        ]
    }),
    ("6 pieces soppressata, cut into batons", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 20, "NAME"),
            (22, 37, "PREP")      # "cut into batons"
        ]
    }),
    ("6 trout fillets", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "NAME"), (8, 15, "UNIT")
        ]
    }),
    ("1 medium white or yellow onion", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "NAME"), # white
            (15, 24, "ALT_NAME"), # "or yellow"
            (25, 30, "NAME")      # "onion"
        ]
    }),
    ("1 1/2 cups plus 3 tablespoons buttermilk", {
        "entities": [
            (0, 5, "QTY"), (6, 10, "UNIT"),
            (11, 29, "COMMENT"),  # "plus 3 tablespoons"
            (30, 40, "NAME")      # "buttermilk"
        ]
    }),
    ("2 skinless walleye fillets (about 4 ounces/113 grams each), halved crosswise", {
        "entities": [
            (0, 1, "QTY"), (2, 10, "PREP"), (11, 18, "NAME"), (19, 26, "UNIT"),
            (27, 58, "COMMENT"),  # "(about 4 ounces/113 grams each)"
            (60, 76, "PREP")      # "halved crosswise"
        ]
    }),
    ("1 tablespoon triple sec", {
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"), (13, 19, "NAME"), (20, 23, "NAME")
        ]
    }),
    ("2 to 3 teaspoons seeded, ribbed and minced jalapeno pepper", {
        "entities": [
            (0, 6, "QTY"), (7, 16, "UNIT"), (17, 23, "PREP"),
            (25, 31, "PREP"), (36, 42, "PREP"), (43, 51, "NAME"), (52, 58, "NAME")
        ]
    }),
    ("1/2 cup roasted and chopped Hatch green chile, homemade from fresh or store-bought, such as 505 Southwestern Green Chile, plus more for garnish", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"), (8, 15, "PREP"), (20, 27, "PREP"),
            (28, 33, "NAME"), (34, 39, "NAME"), (40, 45, "NAME"),
            (47, 91, "COMMENT"),  # "homemade from fresh or store-bought, such as"
            (92, 120, "NAME"),    # "505 Southwestern Green Chile" (treating as product)
            (122, 143, "COMMENT") # "plus more for garnish" (comma at 120 is O)
        ]
    }),
    ("1 1/2 cups yellow cornmeal", {
        "entities": [
            (0, 5, "QTY"), (6, 10, "UNIT"), (11, 17, "NAME"), (18, 26, "NAME")
        ]
    }),
    ("4 cups thawed and drained frozen cherries", {
        "entities": [
            (0, 1, "QTY"), (2, 6, "UNIT"), (7, 13, "PREP"), (18, 25, "PREP"),
            (26, 32, "PREP"), (33, 41, "NAME")
        ]
    }),
    ("2 cups pineapple chunks", {
        "entities": [
            (0, 1, "QTY"), (2, 6, "UNIT"), (7, 16, "NAME"), (17, 23, "PREP")
        ]
    }),
    ("1/4 pound Proscuitto di Parma, julienned", {
        "entities": [
            (0, 3, "QTY"), (4, 9, "UNIT"), (10, 20, "NAME"), (21, 23, "NAME"), (24, 29, "NAME"), # Proscuitto di Parma
            (31, 40, "PREP")
        ]
    }),
    ("8 large black mission figs or 12 green figs", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "NAME"), (14, 21, "NAME"),
            (22, 26, "NAME"),
            (27, 43, "ALT_NAME")  # "or 12 green figs"
        ]
    }),
    ("2 cups peeled, seeded, and chopped vine-ripened tomatoes", {
        "entities": [
            (0, 1, "QTY"), (2, 6, "UNIT"), (7, 13, "PREP"),
            (15, 21, "PREP"),     # "seeded"
            (27, 34, "PREP"),     # "chopped"
            (35, 47, "PREP"),     # "vine-ripened"
            (48, 56, "NAME")      # "tomatoes"
        ]
    }),
    ("2 cups roasted, peeled, and seeded red and yellow bell peppers", {
        "entities": [
            (0, 1, "QTY"), (2, 6, "UNIT"), (7, 14, "PREP"),
            (16, 22, "PREP"),     # "peeled"
            (28, 34, "PREP"),     # "seeded"
            (35, 38, "NAME"),     # "red"
            (43, 49, "NAME"),     # "yellow"
            (50, 54, "NAME"),     # "bell"
            (55, 62, "NAME")      # "peppers"
        ]
    }),
    ("1 papaya, chopped", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "NAME"), (10, 17, "PREP")
        ]
    }),
    ("1 red onion, sliced", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "NAME"), (6, 11, "NAME"), (13, 19, "PREP")
        ]
    }),
    ("1 1/4 cups wheat starch, plus more for dusting", {
        "entities": [
            (0, 5, "QTY"), (6, 10, "UNIT"), (11, 16, "NAME"), (17, 23, "NAME"),
            (25, 46, "COMMENT")
        ]
    }),
    ("1 pound peeled and deveined small shrimp (51/60), tails removed", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 14, "PREP"), (19, 27, "PREP"),
            (28, 33, "UNIT"), (34, 40, "NAME"), (41, 48, "COMMENT"),
            (50, 63, "PREP")      # "tails removed"
        ]
    }),
    ("1 tablespoon peeled and grated fresh ginger", {"entities": [(0,1,"QTY"),(2,12,"UNIT"),(13,19,"PREP"),(24,30,"PREP"),(31,36,"PREP"),(37,43,"NAME")]}), # Duplicate
    ("3 1/2 cups rye flour", {
        "entities": [
            (0, 5, "QTY"), (6, 10, "UNIT"), (11, 14, "NAME"), (15, 20, "NAME")
        ]
    }),
    ("1 pound dried cherries", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"), (8, 13, "PREP"), (14, 22, "NAME")
        ]
    }),
    ("3/4 cup, plus 2 tablespoons honey", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (9, 27, "COMMENT"), # plus 2 tablespoons
            (28, 33, "NAME")
        ]
    }),
    ("1/2 cup 1/4-inch strips red bell pepper", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (8, 16, "PREP"),      # "1/4-inch"
            (17, 23, "PREP"),     # "strips"
            (24, 27, "NAME"),     # "red"
            (28, 32, "NAME"),     # "bell"
            (33, 39, "NAME")      # "pepper"
        ]
    }),
    ("3/4 cup 1/2-inch strips snow peas", {
        "entities": [
            (0, 3, "QTY"), (4, 7, "UNIT"),
            (8, 16, "PREP"),      # "1/2-inch"
            (17, 23, "PREP"),     # "strips"
            (24, 28, "NAME"),     # "snow"
            (29, 33, "NAME")      # "peas"
        ]
    }),
    ("5 cups peeled and chopped firm, ripe mangoes", {
        "entities": [
            (0, 1, "QTY"), (2, 6, "UNIT"), (7, 13, "PREP"), (18, 25, "PREP"),
            (26, 30, "PREP"), (32, 36, "PREP"), (37, 44, "NAME")
        ]
    }),
    ("1 large or 2 small ripe mangoes, peeled, fruit sliced from the pit, and diced", {
        "entities": [
            (0, 1, "QTY"), (2, 7, "UNIT"),
            (8, 18, "ALT_QTY_UNIT"), # "or 2 small"
            (19, 23, "PREP"),     # "ripe"
            (24, 31, "NAME"),     # "mangoes"
            (33, 77, "PREP")      # "peeled, fruit sliced from the pit, and diced"
        ]
    }),
    ("1 package (14 ounces) Pepperidge Farm® Herb Seasoned Stuffing", {
        "entities": [
            (0, 1, "QTY"), (2, 9, "UNIT"), (10, 21, "COMMENT"),
            (22, 61, "NAME")
        ]
    }),
    ("1 tablespoon plus 1 teaspoon McCormick® Grill Mates® Molasses Bacon Seasoning, divided", {
        "entities": [
            (0, 1, "QTY"), (2, 12, "UNIT"),
            (13, 28, "COMMENT"),  # "plus 1 teaspoon"
            (29, 77, "NAME"),     # "McCormick® Grill Mates® Molasses Bacon Seasoning"
            (79, 86, "COMMENT")   # "divided"
        ]
    }),
    ("3 pounds canned hominy, drained", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 15, "PREP"), (16, 22, "NAME"),
            (24, 31, "PREP")
        ]
    }),
    ("Chopped green onion, for garnish", { # No QTY/UNIT implies to taste/as needed
        "entities": [
            (0, 7, "PREP"), (8, 13, "NAME"), (14, 19, "NAME"),
            (21, 32, "COMMENT")
        ]
    }),
    ("1 pound peeled and deveined shrimp", {
        "entities": [
            (0,1,"QTY"),(2,7,"UNIT"),(8,14,"PREP"),(19,27,"PREP"),(28,34,"NAME")
        ]
    }),
    ("2 grapefruits", { "entities": [(0,1,"QTY"),(2,13,"NAME")]}),
    ("2 jars Spanish olives", {
        "entities": [
            (0,1,"QTY"),(2,6,"UNIT"),(7,14,"NAME"),(15,21,"NAME")
        ]
    }),
    ("2 bags frozen green peas", {
        "entities": [
            (0,1,"QTY"),(2,6,"UNIT"),(7,13,"PREP"),(14,19,"NAME"),(20,24,"NAME")
        ]
    }),
    ("1 1/2 pounds (about 4 1/2 cups) frozen peas", {
        "entities": [
            (0, 5, "QTY"), (6, 12, "UNIT"),
            (13, 31, "COMMENT"),  # "(about 4 1/2 cups)"
            (32, 38, "PREP"),     # "frozen"
            (39, 43, "NAME")      # "peas"
        ]
    }),
    ("3 pomegranates, peeled and seeded", {
        "entities": [
            (0,1,"QTY"),(2,14,"NAME"),(16,22,"PREP"),(27,33,"PREP")
        ]
    }),
    ("3 cups plain croutons", {
        "entities": [
            (0,1,"QTY"),(2,6,"UNIT"),(7,12,"PREP"),(13,21,"NAME")
        ]
    }),
    ("1 knob of ginger, peeled and chopped", {
        "entities": [
            (0,1,"QTY"),(2,6,"UNIT"),(7,9,"PREP"),(10,16,"NAME"),(18,24,"PREP"),(29,36,"PREP")
        ]
    }),
    ("1 tablespoon Old Bay seasoning", {
        "entities": [
            (0,1,"QTY"),(2,12,"UNIT"),(13,16,"NAME"),(17,20,"NAME"),(21,30,"NAME")
        ]
    }),
    ("1/2 cup shredded and chopped iceberg lettuce", {
        "entities": [
            (0,3,"QTY"),(4,7,"UNIT"),(8,16,"PREP"),(21,28,"PREP"),(29,36,"NAME"),(37,44,"NAME")
        ]
    }),
    ("10 tomatillos, husked", {
        "entities": [
            (0,2,"QTY"),(3,13,"NAME"),(15,21,"PREP")
        ]
    }),
    ("1 clove", { "entities": [(0,1,"QTY"),(2,7,"UNIT")]}), # NAME is missing, might be implied "garlic clove" from context
    ("2 medium bowls", { # This is equipment, not an ingredient. How do you want to handle? For now, NAME.
        "entities": [
            (0,1,"QTY"),(2,8,"UNIT"),(9,14,"NAME")
        ]
    }),
    ("4 ounces Monterey Jack cheese, shredded", {
        "entities": [
            (0,1,"QTY"),(2,8,"UNIT"),(9,17,"NAME"),(18,22,"NAME"),(23,29,"NAME"),(31,39,"PREP")
        ]
    }),
    ("16 ounces Chihuahua or Oaxaca cheese, shredded", {
        "entities": [
            (0, 2, "QTY"), (3, 9, "UNIT"), (10, 19, "NAME"),
            (20, 36, "ALT_NAME"), # "or Oaxaca cheese"
            (38, 46, "PREP")      # "shredded"
        ]
    }),
    ("2 cups seeded and cubed watermelon", {
        "entities": [
            (0,1,"QTY"),(2,6,"UNIT"),(7,13,"PREP"),(18,23,"PREP"),(24,34,"NAME")
        ]
    }),
    ("6 ounces club soda", {
        "entities": [
            (0,1,"QTY"),(2,8,"UNIT"),(9,13,"NAME"),(14,18,"NAME")
        ]
    }),
    ("1 bottle white wine, such as Sancerre or Sauvignon Blanc", {
        "entities": [
            (0, 1, "QTY"), (2, 8, "UNIT"), (9, 14, "NAME"), (15, 19, "NAME"),
            (21, 56, "COMMENT")
        ]
    }),
    ("2 oz. of club soda", {
        "entities": [
            (0,1,"QTY"),(2,5,"UNIT"),(6,8,"PREP"),(9,13,"NAME"),(14,18,"NAME")
        ]
    }),
    ("1 cup cut fruit from in store service deli", {
        "entities": [
            (0, 1, "QTY"), (2, 5, "UNIT"), (6, 9, "PREP"), (10, 15, "NAME"),
            (16, 42, "COMMENT")
        ]
    }),
    ("1 single-serve cup fruit flavored custard style low fat yogurt", {
        "entities": [
            (0,1,"QTY"),(2,14,"UNIT"),(15,18,"UNIT"),(19,24,"NAME"),(25,33,"PREP"),(34,41,"NAME"),(42,47,"PREP"),(48,51,"PREP"),(52,55,"PREP"),(56,62,"NAME") # fruit flavored custard style low fat yogurt
        ]
    })

]
if __name__=='__main__':
    out_file = open("./train_data.json",'w')
    json.dump(TRAIN_DATA,out_file)