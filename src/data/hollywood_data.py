# src/data/hollywood_data.py
# ─────────────────────────────────────────────────────────────────────────────
# Complete dataset for the hollywood Knowledge Graph.
#
# This module defines all entities and relationships that will be loaded into
# Neo4j. The data covers English cinema from 1995–2024, including iconic films,
# major actors, celebrated directors, legendary music composers, production
# houses, and a selection of Filmfare and National Awards.
#
# Ontology:
#   Nodes:  Person, Movie, ProductionHouse, Award, MusicAlbum
#   Edges:  ACTED_IN, DIRECTED, COMPOSED_MUSIC_FOR, PRODUCED, WON,
#           WORKED_WITH, RELEASED_BY
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# PEOPLE
# ─────────────────────────────────────────────────────────────────────────────

PEOPLE = [
    # Actors
    {"name": "Leonardo DiCaprio",      "born": 1974, "profession": "Actor",            "hometown": "Los Angeles"},
    {"name": "Tom Hardy",              "born": 1977, "profession": "Actor",            "hometown": "London"},
    {"name": "Cillian Murphy",         "born": 1976, "profession": "Actor",            "hometown": "Cork"},
    {"name": "Joseph Gordon-Levitt",   "born": 1981, "profession": "Actor",            "hometown": "Los Angeles"},
    {"name": "Brad Pitt",              "born": 1963, "profession": "Actor",            "hometown": "Shawnee"},
    {"name": "George Clooney",         "born": 1961, "profession": "Actor",            "hometown": "Lexington"},
    {"name": "Matt Damon",             "born": 1970, "profession": "Actor",            "hometown": "Cambridge"},
    {"name": "Christian Bale",         "born": 1974, "profession": "Actor",            "hometown": "Haverfordwest"},
    {"name": "Michael Caine",          "born": 1933, "profession": "Actor",            "hometown": "London"},
    {"name": "Robert Downey Jr.",      "born": 1965, "profession": "Actor",            "hometown": "New York City"},
    {"name": "Scarlett Johansson",     "born": 1984, "profession": "Actor",            "hometown": "New York City"},
    {"name": "Chris Evans",            "born": 1981, "profession": "Actor",            "hometown": "Boston"},
    {"name": "Chris Hemsworth",        "born": 1983, "profession": "Actor",            "hometown": "Melbourne"},
    {"name": "Will Smith",             "born": 1968, "profession": "Actor",            "hometown": "Philadelphia"},
    {"name": "Martin Lawrence",        "born": 1965, "profession": "Actor",            "hometown": "Frankfurt"},
    {"name": "Anne Hathaway",          "born": 1982, "profession": "Actor",            "hometown": "Brooklyn"},
    {"name": "Meryl Streep",           "born": 1949, "profession": "Actor",            "hometown": "Summit"},
    {"name": "Emily Blunt",            "born": 1983, "profession": "Actor",            "hometown": "London"},
    {"name": "Sandra Bullock",         "born": 1964, "profession": "Actor",            "hometown": "Arlington"},
    {"name": "Margot Robbie",          "born": 1990, "profession": "Actor",            "hometown": "Dalby"},
    {"name": "Ryan Gosling",           "born": 1980, "profession": "Actor",            "hometown": "London, Ontario"},
    {"name": "Russell Crowe",          "born": 1964, "profession": "Actor",            "hometown": "Wellington"},
    {"name": "Amanda Seyfried",        "born": 1985, "profession": "Actor",            "hometown": "Allentown"},
    {"name": "Christine Baranski",     "born": 1952, "profession": "Actor",            "hometown": "Buffalo"},

    # Directors
    {"name": "Christopher Nolan",      "born": 1970, "profession": "Director",         "hometown": "London"},
    {"name": "Martin Scorsese",        "born": 1942, "profession": "Director",         "hometown": "New York City"},
    {"name": "Greta Gerwig",           "born": 1983, "profession": "Director",         "hometown": "Sacramento"},
    {"name": "Shane Black",            "born": 1961, "profession": "Director",         "hometown": "Pittsburgh"},
    {"name": "Tom Hooper",             "born": 1972, "profession": "Director",         "hometown": "London"},
    {"name": "Michael Bay",            "born": 1965, "profession": "Director",         "hometown": "Los Angeles"},
    {"name": "Steven Soderbergh",      "born": 1963, "profession": "Director",         "hometown": "Atlanta"},
    {"name": "David Frankel",          "born": 1959, "profession": "Director",         "hometown": "New York City"},
    {"name": "Phyllida Lloyd",         "born": 1957, "profession": "Director",         "hometown": "Bristol"},
    {"name": "Ol Parker",              "born": 1969, "profession": "Director",         "hometown": "London"},
    {"name": "Jan de Bont",            "born": 1943, "profession": "Director",         "hometown": "Eindhoven"},
    {"name": "Alfonso Cuarón",         "born": 1961, "profession": "Director",         "hometown": "Mexico City"},
    {"name": "Jon Favreau",            "born": 1966, "profession": "Director",         "hometown": "Queens"},
    {"name": "Joss Whedon",            "born": 1964, "profession": "Director",         "hometown": "New York City"},
    {"name": "Anthony Russo",          "born": 1970, "profession": "Director",         "hometown": "Cleveland"},
    {"name": "Joe Russo",              "born": 1971, "profession": "Director",         "hometown": "Cleveland"},
    {"name": "The Russo Brothers",     "born": 1970, "profession": "Director",         "hometown": "Cleveland"},
    {"name": "James Mangold",          "born": 1963, "profession": "Director",         "hometown": "New York City"},
    {"name": "Quentin Tarantino",      "born": 1963, "profession": "Director",         "hometown": "Knoxville"},
    {"name": "Gary Ross",              "born": 1956, "profession": "Director",         "hometown": "Los Angeles"},
    {"name": "The Coen Brothers",      "born": 1954, "profession": "Director",         "hometown": "United States"},
    {"name": "Alejandro G. Iñárritu",  "born": 1963, "profession": "Director",         "hometown": "Mexico City"},
    {"name": "James Cameron",          "born": 1954, "profession": "Director",         "hometown": "Kapuskasing"},

    # Music composers
    {"name": "Hans Zimmer",                "born": 1957, "profession": "Music Composer", "hometown": "Frankfurt"},
    {"name": "Ludwig Göransson",           "born": 1984, "profession": "Music Composer", "hometown": "Linköping"},
    {"name": "Howard Shore",               "born": 1946, "profession": "Music Composer", "hometown": "Toronto"},
    {"name": "Mark Mancina",               "born": 1957, "profession": "Music Composer", "hometown": "Santa Monica"},
    {"name": "Alan Silvestri",             "born": 1950, "profession": "Music Composer", "hometown": "New York City"},
    {"name": "David Holmes",               "born": 1969, "profession": "Music Composer", "hometown": "Belfast"},
    {"name": "Theodore Shapiro",           "born": 1971, "profession": "Music Composer", "hometown": "New York City"},
    {"name": "Benny Andersson",            "born": 1946, "profession": "Music Composer", "hometown": "Stockholm"},
    {"name": "Steven Price",               "born": 1977, "profession": "Music Composer", "hometown": "Nottingham"},
    {"name": "John Debney",                "born": 1956, "profession": "Music Composer", "hometown": "Glendale"},
    {"name": "Claude-Michel Schönberg",    "born": 1944, "profession": "Music Composer", "hometown": "Vannes"},
    {"name": "Marco Beltrami",             "born": 1966, "profession": "Music Composer", "hometown": "New York City"},
    {"name": "Carter Burwell",             "born": 1954, "profession": "Music Composer", "hometown": "New York City"},
    {"name": "Daniel Pemberton",           "born": 1977, "profession": "Music Composer", "hometown": "London"},
    {"name": "John Ottman",                "born": 1964, "profession": "Music Composer", "hometown": "San Diego"},
    {"name": "Mark Ronson and Andrew Wyatt","born": 1975, "profession": "Music Composer", "hometown": "London"},
    {"name": "Ryuichi Sakamoto",           "born": 1952, "profession": "Music Composer", "hometown": "Tokyo"},
    {"name": "James Newton Howard",        "born": 1951, "profession": "Music Composer", "hometown": "Los Angeles"},
]

# ─────────────────────────────────────────────────────────────────────────────
# PRODUCTION HOUSES
# ─────────────────────────────────────────────────────────────────────────────

PRODUCTION_HOUSES = [
    {"name": "Warner Bros. Pictures",      "founded": 1923, "founder": "Warner brothers",      "hq": "Burbank"},
    {"name": "Legendary Pictures",         "founded": 2000, "founder": "Thomas Tull",           "hq": "Burbank"},
    {"name": "Syncopy",                    "founded": 2001, "founder": "Christopher Nolan",     "hq": "London"},
    {"name": "Red Granite Pictures",       "founded": 2010, "founder": "Riza Aziz",             "hq": "Los Angeles"},
    {"name": "Columbia Pictures",          "founded": 1918, "founder": "Harry Cohn",            "hq": "Culver City"},
    {"name": "Village Roadshow Pictures",  "founded": 1986, "founder": "Greg Coote",            "hq": "Melbourne"},
    {"name": "Marvel Studios",             "founded": 1993, "founder": "Avi Arad",              "hq": "Burbank"},
    {"name": "20th Century Fox",           "founded": 1935, "founder": "Joseph Schenck",        "hq": "Los Angeles"},
    {"name": "Universal Pictures",         "founded": 1912, "founder": "Carl Laemmle",          "hq": "Universal City"},
    {"name": "Working Title Films",        "founded": 1983, "founder": "Tim Bevan",             "hq": "London"},
    {"name": "Paramount Pictures",         "founded": 1912, "founder": "Adolph Zukor",          "hq": "Hollywood"},
    {"name": "Regency Enterprises",        "founded": 1982, "founder": "Arnon Milchan",         "hq": "Beverly Hills"},
    {"name": "Focus Features",             "founded": 2001, "founder": "Universal Pictures",    "hq": "Universal City"},
    {"name": "Silver Pictures",            "founded": 1980, "founder": "Joel Silver",           "hq": "Los Angeles"},
    {"name": "Mattel Films",               "founded": 2018, "founder": "Mattel",                "hq": "El Segundo"},
]

# ─────────────────────────────────────────────────────────────────────────────
# MOVIES
# ─────────────────────────────────────────────────────────────────────────────

MOVIES = [
    {
        "title": "Inception",
        "year": 2010, "genre": "Science Fiction Thriller", "language": "English",
        "box_office_million": 829.9,
        "description": "A skilled thief enters dreams to steal secrets and is offered a chance to erase his past by planting an idea."
    },
    {
        "title": "The Revenant",
        "year": 2015, "genre": "Adventure Drama", "language": "English",
        "box_office_million": 533.0,
        "description": "A frontiersman fights for survival after being left for dead in the unforgiving American wilderness."
    },
    {
        "title": "The Wolf of Wall Street",
        "year": 2013, "genre": "Biographical Comedy Drama", "language": "English",
        "box_office_million": 392.0,
        "description": "A stockbroker's rapid rise and scandalous fall on Wall Street is told with black comedy and excess."
    },
    {
        "title": "Barbie",
        "year": 2023, "genre": "Fantasy Comedy", "language": "English",
        "box_office_million": 1450.0,
        "description": "Barbie leaves her perfect world and discovers what it means to live in the real one."
    },
    {
        "title": "The Nice Guys",
        "year": 2016, "genre": "Crime Comedy", "language": "English",
        "box_office_million": 62.8,
        "description": "A private eye and a hired enforcer stumble into a conspiracy in 1970s Los Angeles."
    },
    {
        "title": "Les Misérables",
        "year": 2012, "genre": "Musical Drama", "language": "English",
        "box_office_million": 441.8,
        "description": "A former prisoner is relentlessly pursued by a police inspector while trying to build a new life."
    },
    {
        "title": "Batman Begins",
        "year": 2005, "genre": "Superhero Action", "language": "English",
        "box_office_million": 373.7,
        "description": "Bruce Wayne learns to fight fear and becomes Batman to save Gotham City."
    },
    {
        "title": "The Dark Knight",
        "year": 2008, "genre": "Superhero Crime", "language": "English",
        "box_office_million": 1006.0,
        "description": "Batman faces the chaos-driven Joker while Gotham is pushed to the brink."
    },
    {
        "title": "The Dark Knight Rises",
        "year": 2012, "genre": "Superhero Action", "language": "English",
        "box_office_million": 1084.9,
        "description": "Batman returns to defend Gotham from Bane after years in hiding."
    },
    {
        "title": "Interstellar",
        "year": 2014, "genre": "Science Fiction Drama", "language": "English",
        "box_office_million": 758.6,
        "description": "A team travels through a wormhole in search of a new home for humanity."
    },
    {
        "title": "The Devil Wears Prada",
        "year": 2006, "genre": "Comedy Drama", "language": "English",
        "box_office_million": 326.7,
        "description": "A young assistant navigates the high-pressure world of a powerful fashion magazine editor."
    },
    {
        "title": "Mamma Mia!",
        "year": 2008, "genre": "Musical Romance", "language": "English",
        "box_office_million": 694.0,
        "description": "A bride on a Greek island invites three men from her mother's past to discover who is her father."
    },
    {
        "title": "Mamma Mia! Here We Go Again",
        "year": 2018, "genre": "Musical Romance", "language": "English",
        "box_office_million": 395.0,
        "description": "A new generation revisits the story of Donna and the island where it all began."
    },
    {
        "title": "Bad Boys",
        "year": 1995, "genre": "Action Comedy", "language": "English",
        "box_office_million": 141.4,
        "description": "Two Miami detectives race to recover stolen evidence and protect a witness."
    },
    {
        "title": "Bad Boys II",
        "year": 2003, "genre": "Action Comedy", "language": "English",
        "box_office_million": 273.0,
        "description": "The detectives tackle a drug trafficking case that spirals into chaos across Miami."
    },
    {
        "title": "Bad Boys for Life",
        "year": 2020, "genre": "Action Comedy", "language": "English",
        "box_office_million": 426.5,
        "description": "The old-school detectives reunite to take down a ruthless cartel boss."
    },
    {
        "title": "Ocean's Eleven",
        "year": 2001, "genre": "Heist Thriller", "language": "English",
        "box_office_million": 451.5,
        "description": "A suave criminal assembles a crew to rob three Las Vegas casinos in one night."
    },
    {
        "title": "Ocean's Twelve",
        "year": 2004, "genre": "Heist Comedy", "language": "English",
        "box_office_million": 362.0,
        "description": "The crew reunites for another globe-trotting heist after a new challenge in Europe."
    },
    {
        "title": "Ocean's Thirteen",
        "year": 2007, "genre": "Heist Comedy", "language": "English",
        "box_office_million": 311.7,
        "description": "The team plots revenge against a ruthless casino owner who betrayed one of their own."
    },
    {
        "title": "Ocean's 8",
        "year": 2018, "genre": "Heist Comedy", "language": "English",
        "box_office_million": 297.0,
        "description": "Debbie Ocean assembles a team to pull off an elaborate heist at the Met Gala."
    },
    {
        "title": "Gravity",
        "year": 2013, "genre": "Science Fiction Thriller", "language": "English",
        "box_office_million": 723.2,
        "description": "Two astronauts fight for survival after debris destroys their shuttle in orbit."
    },
    {
        "title": "Iron Man 2",
        "year": 2010, "genre": "Superhero Action", "language": "English",
        "box_office_million": 621.0,
        "description": "Tony Stark faces new threats while dealing with a failing arc reactor and rising enemies."
    },
    {
        "title": "The Avengers",
        "year": 2012, "genre": "Superhero Action", "language": "English",
        "box_office_million": 1518.8,
        "description": "Earth's greatest heroes unite to stop Loki and his alien invasion."
    },
    {
        "title": "Avengers: Endgame",
        "year": 2019, "genre": "Superhero Action", "language": "English",
        "box_office_million": 2797.8,
        "description": "The remaining Avengers attempt to undo Thanos' catastrophic snap."
    },
    {
        "title": "Oppenheimer",
        "year": 2023, "genre": "Biographical Drama", "language": "English",
        "box_office_million": 976.0,
        "description": "The story of J. Robert Oppenheimer and the creation of the atomic bomb."
    },
    {
        "title": "Ford v Ferrari",
        "year": 2019, "genre": "Sports Drama", "language": "English",
        "box_office_million": 225.5,
        "description": "Car designer Carroll Shelby and driver Ken Miles battle Ferrari at Le Mans for Ford."
    },
    {
        "title": "Burn After Reading",
        "year": 2008, "genre": "Black Comedy", "language": "English",
        "box_office_million": 163.7,
        "description": "Two gym employees stumble into a tangled web of secrets, espionage and bad decisions."
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# AWARDS
# ─────────────────────────────────────────────────────────────────────────────

AWARDS = [
    {"name": "Academy Award Best Actor 2016",                 "category": "Academy",         "year": 2016},
    {"name": "Academy Award Best Supporting Actor 2020",      "category": "Academy",         "year": 2020},
    {"name": "Academy Award Best Supporting Actor 2006",      "category": "Academy",         "year": 2006},
    {"name": "Academy Award Best Original Screenplay 1998",   "category": "Academy",         "year": 1998},
    {"name": "Academy Award Best Actress 2010",               "category": "Academy",         "year": 2010},
    {"name": "Academy Award Best Supporting Actress 2013",    "category": "Academy",         "year": 2013},
    {"name": "Academy Award Best Actress 2012",               "category": "Academy",         "year": 2012},
    {"name": "Academy Award Best Supporting Actor 2005",      "category": "Academy",         "year": 2005},
    {"name": "Academy Award Best Supporting Actor 2011",      "category": "Academy",         "year": 2011},
    {"name": "Academy Award Best Actor 2022",                 "category": "Academy",         "year": 2022},
    {"name": "Academy Award Best Supporting Actor 2024",      "category": "Academy",         "year": 2024},
    {"name": "Academy Award Best Actor 2024",                 "category": "Academy",         "year": 2024},
    {"name": "Academy Award Best Director 2024",              "category": "Academy",         "year": 2024},
    {"name": "Academy Award Best Director 2007",              "category": "Academy",         "year": 2007},
    {"name": "Academy Award Best Director 2001",              "category": "Academy",         "year": 2001},
    {"name": "Academy Award Best Original Score 2022",        "category": "Academy",         "year": 2022},
    {"name": "Academy Award Best Original Score 2019",        "category": "Academy",         "year": 2019},
    {"name": "Academy Award Best Visual Effects 2000",        "category": "Academy",         "year": 2000},
    {"name": "Academy Award Best Visual Effects 2011",        "category": "Academy",         "year": 2011},
    {"name": "Academy Award Best Visual Effects 2014",        "category": "Academy",         "year": 2014},
    {"name": "Saturn Award Best Science Fiction Film 2004",   "category": "Saturn",          "year": 2004},
    {"name": "Saturn Award Best Comic-to-Film Motion Picture 2013", "category": "Saturn",   "year": 2013},
    {"name": "People's Choice Award Favorite Movie 2013",     "category": "People's Choice", "year": 2013},
    {"name": "People's Choice Award Favorite Movie 2020",     "category": "People's Choice", "year": 2020},
    {"name": "MTV Movie Award Best On-Screen Duo 1996",       "category": "MTV",             "year": 1996},
    {"name": "Golden Globe Best Supporting Actress 2006",     "category": "Golden Globe",    "year": 2006},
    {"name": "Golden Globe Best Motion Picture Musical 2009", "category": "Golden Globe",    "year": 2009},
    {"name": "Golden Globe Best Actor 2014",                  "category": "Golden Globe",    "year": 2014},
    {"name": "BAFTA Best Film 2016",                          "category": "BAFTA",           "year": 2016},
    {"name": "BAFTA Best Cinematography 2014",                "category": "BAFTA",           "year": 2014},
    {"name": "BAFTA Best Editing 2002",                       "category": "BAFTA",           "year": 2002},
    {"name": "Grammy Best Compilation Soundtrack 2017",       "category": "Grammy",          "year": 2017},
]


# ─────────────────────────────────────────────────────────────────────────────
# RELATIONSHIPS
# ─────────────────────────────────────────────────────────────────────────────

# (actor, movie, character_name, lead_role: bool)
ACTED_IN = [
    ("Leonardo DiCaprio",    "Inception",                  "Cobb",                      True),
    ("Tom Hardy",            "Inception",                  "Eames",                     True),
    ("Cillian Murphy",       "Inception",                  "Robert Fischer",            False),
    ("Joseph Gordon-Levitt", "Inception",                  "Arthur",                    True),

    ("Leonardo DiCaprio",    "The Revenant",               "Hugh Glass",                True),
    ("Tom Hardy",            "The Revenant",               "John Fitzgerald",           False),

    ("Leonardo DiCaprio",    "The Wolf of Wall Street",    "Jordan Belfort",            True),
    ("Margot Robbie",        "The Wolf of Wall Street",    "Naomi Lapaglia",            True),
    ("Matthew McConaughey",  "The Wolf of Wall Street",    "Mark Hanna",                False),

    ("Margot Robbie",        "Barbie",                     "Barbie",                    True),
    ("Ryan Gosling",         "Barbie",                     "Ken",                       True),

    ("Ryan Gosling",         "The Nice Guys",              "Holland March",             True),
    ("Russell Crowe",        "The Nice Guys",              "Jackson Healy",             True),

    ("Anne Hathaway",        "Les Misérables",             "Fantine",                   True),
    ("Russell Crowe",        "Les Misérables",             "Javert",                    True),
    ("Amanda Seyfried",      "Les Misérables",             "Cosette",                   True),

    ("Meryl Streep",         "Mamma Mia!",                 "Donna",                     True),
    ("Amanda Seyfried",      "Mamma Mia!",                 "Sophie",                    True),
    ("Christine Baranski",   "Mamma Mia!",                 "Tanya",                     True),

    ("Meryl Streep",         "Mamma Mia! Here We Go Again","Donna",                     True),
    ("Amanda Seyfried",      "Mamma Mia! Here We Go Again","Sophie",                    True),
    ("Christine Baranski",   "Mamma Mia! Here We Go Again","Tanya",                     True),

    ("Christian Bale",       "Batman Begins",              "Bruce Wayne",               True),
    ("Michael Caine",        "Batman Begins",              "Alfred Pennyworth",         False),
    ("Cillian Murphy",       "Batman Begins",              "Dr. Jonathan Crane",        False),

    ("Christian Bale",       "The Dark Knight",            "Bruce Wayne",               True),
    ("Michael Caine",        "The Dark Knight",            "Alfred Pennyworth",         False),
    ("Cillian Murphy",       "The Dark Knight",            "Dr. Jonathan Crane",        False),

    ("Christian Bale",       "The Dark Knight Rises",      "Bruce Wayne",               True),
    ("Michael Caine",        "The Dark Knight Rises",      "Alfred Pennyworth",         False),
    ("Tom Hardy",            "The Dark Knight Rises",      "Bane",                      True),
    ("Joseph Gordon-Levitt", "The Dark Knight Rises",      "John Blake",                True),

    ("Matthew McConaughey",  "Interstellar",               "Cooper",                    True),
    ("Anne Hathaway",        "Interstellar",               "Brand",                     True),
    ("Michael Caine",        "Interstellar",               "Professor Brand",           False),

    ("Anne Hathaway",        "The Devil Wears Prada",      "Andy Sachs",                True),
    ("Meryl Streep",         "The Devil Wears Prada",      "Miranda Priestly",          True),
    ("Emily Blunt",          "The Devil Wears Prada",      "Emily Charlton",            True),

    ("Will Smith",           "Bad Boys",                   "Mike Lowrey",               True),
    ("Martin Lawrence",      "Bad Boys",                   "Marcus Burnett",            True),

    ("Will Smith",           "Bad Boys II",                "Mike Lowrey",               True),
    ("Martin Lawrence",      "Bad Boys II",                "Marcus Burnett",            True),

    ("Will Smith",           "Bad Boys for Life",          "Mike Lowrey",               True),
    ("Martin Lawrence",      "Bad Boys for Life",          "Marcus Burnett",            True),

    ("Brad Pitt",            "Ocean's Eleven",             "Rusty Ryan",                True),
    ("George Clooney",       "Ocean's Eleven",             "Danny Ocean",               True),
    ("Matt Damon",           "Ocean's Eleven",             "Linus Caldwell",            True),

    ("Brad Pitt",            "Ocean's Twelve",             "Rusty Ryan",                True),
    ("George Clooney",       "Ocean's Twelve",             "Danny Ocean",               True),
    ("Matt Damon",           "Ocean's Twelve",             "Linus Caldwell",            True),

    ("Brad Pitt",            "Ocean's Thirteen",           "Rusty Ryan",                True),
    ("George Clooney",       "Ocean's Thirteen",           "Danny Ocean",               True),
    ("Matt Damon",           "Ocean's Thirteen",           "Linus Caldwell",            True),

    ("Sandra Bullock",       "Ocean's 8",                  "Debbie Ocean",              True),
    ("Anne Hathaway",        "Ocean's 8",                  "Daphne Kluger",             True),

    ("Sandra Bullock",       "Gravity",                    "Dr. Ryan Stone",            True),
    ("George Clooney",       "Gravity",                    "Matt Kowalski",             True),

    ("Robert Downey Jr.",    "Iron Man 2",                 "Tony Stark",                True),
    ("Scarlett Johansson",   "Iron Man 2",                 "Natalie Rushman",           True),

    ("Robert Downey Jr.",    "The Avengers",               "Tony Stark",                True),
    ("Scarlett Johansson",   "The Avengers",               "Natasha Romanoff",          True),
    ("Chris Evans",          "The Avengers",               "Steve Rogers",              True),
    ("Chris Hemsworth",      "The Avengers",               "Thor",                      True),

    ("Robert Downey Jr.",    "Avengers: Endgame",          "Tony Stark",                True),
    ("Scarlett Johansson",   "Avengers: Endgame",          "Natasha Romanoff",          True),
    ("Chris Evans",          "Avengers: Endgame",          "Steve Rogers",              True),
    ("Chris Hemsworth",      "Avengers: Endgame",          "Thor",                      True),

    ("Cillian Murphy",       "Oppenheimer",                "J. Robert Oppenheimer",     True),
    ("Robert Downey Jr.",    "Oppenheimer",                "Lewis Strauss",             True),
    ("Emily Blunt",          "Oppenheimer",                "Kitty Oppenheimer",         True),
    ("Matt Damon",           "Oppenheimer",                "Leslie Groves",             True),

    ("Matt Damon",           "Ford v Ferrari",             "Carroll Shelby",            True),
    ("Christian Bale",       "Ford v Ferrari",             "Ken Miles",                 True),

    ("Brad Pitt",            "Burn After Reading",         "Chad Feldheimer",           True),
    ("George Clooney",       "Burn After Reading",         "Harry Pfarrer",             True),
]

# (director, movie)
DIRECTED = [
    ("Christopher Nolan",       "Inception"),
    ("Alejandro G. Iñárritu",   "The Revenant"),
    ("Martin Scorsese",         "The Wolf of Wall Street"),
    ("Greta Gerwig",            "Barbie"),
    ("Shane Black",             "The Nice Guys"),
    ("Tom Hooper",              "Les Misérables"),
    ("Christopher Nolan",       "Batman Begins"),
    ("Christopher Nolan",       "The Dark Knight"),
    ("Christopher Nolan",       "The Dark Knight Rises"),
    ("Christopher Nolan",       "Interstellar"),
    ("David Frankel",           "The Devil Wears Prada"),
    ("Phyllida Lloyd",          "Mamma Mia!"),
    ("Ol Parker",               "Mamma Mia! Here We Go Again"),
    ("Michael Bay",             "Bad Boys"),
    ("Michael Bay",             "Bad Boys II"),
    ("Adil El Arbi",            "Bad Boys for Life"),
    ("Bilall Fallah",           "Bad Boys for Life"),
    ("Steven Soderbergh",       "Ocean's Eleven"),
    ("Steven Soderbergh",       "Ocean's Twelve"),
    ("Steven Soderbergh",       "Ocean's Thirteen"),
    ("Gary Ross",               "Ocean's 8"),
    ("Alfonso Cuarón",          "Gravity"),
    ("Jon Favreau",             "Iron Man 2"),
    ("Joss Whedon",             "The Avengers"),
    ("Anthony Russo",           "Avengers: Endgame"),
    ("Joe Russo",               "Avengers: Endgame"),
    ("Christopher Nolan",       "Oppenheimer"),
    ("James Mangold",           "Ford v Ferrari"),
    ("The Coen Brothers",       "Burn After Reading"),
]

# (composer, movie)
COMPOSED_MUSIC_FOR = [
    ("Hans Zimmer",                  "Inception"),
    ("Hans Zimmer",                  "Batman Begins"),
    ("Hans Zimmer",                  "The Dark Knight"),
    ("Hans Zimmer",                  "The Dark Knight Rises"),
    ("Hans Zimmer",                  "Interstellar"),
    ("Ryuichi Sakamoto",             "The Revenant"),
    ("Howard Shore",                 "The Wolf of Wall Street"),
    ("Mark Ronson and Andrew Wyatt", "Barbie"),
    ("John Ottman",                  "The Nice Guys"),
    ("Claude-Michel Schönberg",      "Les Misérables"),
    ("Benny Andersson",              "Mamma Mia!"),
    ("Benny Andersson",              "Mamma Mia! Here We Go Again"),
    ("Mark Mancina",                 "Bad Boys"),
    ("Mark Mancina",                 "Bad Boys II"),
    ("Lorne Balfe",                  "Bad Boys for Life"),
    ("David Holmes",                 "Ocean's Eleven"),
    ("David Holmes",                 "Ocean's Twelve"),
    ("David Holmes",                 "Ocean's Thirteen"),
    ("Daniel Pemberton",             "Ocean's 8"),
    ("Steven Price",                 "Gravity"),
    ("John Debney",                  "Iron Man 2"),
    ("Alan Silvestri",               "The Avengers"),
    ("Alan Silvestri",               "Avengers: Endgame"),
    ("Ludwig Göransson",             "Oppenheimer"),
    ("Marco Beltrami",               "Ford v Ferrari"),
    ("Carter Burwell",               "Burn After Reading"),
    ("Theodore Shapiro",             "The Devil Wears Prada"),
]

# (production_house, movie)
PRODUCED_BY = [
    ("Warner Bros. Pictures",      "Inception"),
    ("Legendary Pictures",         "Inception"),
    ("Syncopy",                    "Inception"),

    ("Regency Enterprises",        "The Revenant"),

    ("Red Granite Pictures",       "The Wolf of Wall Street"),

    ("Mattel Films",               "Barbie"),
    ("Warner Bros. Pictures",      "Barbie"),

    ("Silver Pictures",            "The Nice Guys"),

    ("Working Title Films",        "Les Misérables"),

    ("Universal Pictures",         "Mamma Mia!"),
    ("Universal Pictures",         "Mamma Mia! Here We Go Again"),

    ("Columbia Pictures",          "Bad Boys"),
    ("Columbia Pictures",          "Bad Boys II"),
    ("Columbia Pictures",          "Bad Boys for Life"),

    ("Warner Bros. Pictures",      "Batman Begins"),
    ("Warner Bros. Pictures",      "The Dark Knight"),
    ("Warner Bros. Pictures",      "The Dark Knight Rises"),
    ("Legendary Pictures",         "The Dark Knight"),
    ("Legendary Pictures",         "The Dark Knight Rises"),

    ("Warner Bros. Pictures",      "Interstellar"),
    ("Legendary Pictures",         "Interstellar"),
    ("Syncopy",                    "Interstellar"),

    ("20th Century Fox",           "The Devil Wears Prada"),

    ("Warner Bros. Pictures",      "Ocean's Eleven"),
    ("Village Roadshow Pictures",  "Ocean's Twelve"),
    ("Village Roadshow Pictures",  "Ocean's Thirteen"),
    ("Warner Bros. Pictures",      "Ocean's 8"),

    ("Warner Bros. Pictures",      "Gravity"),

    ("Marvel Studios",             "Iron Man 2"),
    ("Paramount Pictures",         "Iron Man 2"),

    ("Marvel Studios",             "The Avengers"),
    ("Paramount Pictures",         "The Avengers"),

    ("Marvel Studios",             "Avengers: Endgame"),

    ("Syncopy",                    "Oppenheimer"),
    ("Universal Pictures",         "Oppenheimer"),

    ("20th Century Fox",           "Ford v Ferrari"),

    ("Focus Features",             "Burn After Reading"),
]

# (entity_name, entity_type, award_name)
# entity_type is "person" or "movie"
WON_AWARDS = [
    # Movie awards
    ("Inception",                  "movie",  "Academy Award Best Visual Effects 2011"),
    ("The Revenant",               "movie",  "BAFTA Best Film 2016"),
    ("The Wolf of Wall Street",    "movie",  "Golden Globe Best Actor 2014"),
    ("Barbie",                     "movie",  "Grammy Best Compilation Soundtrack 2017"),
    ("Batman Begins",              "movie",  "Saturn Award Best Science Fiction Film 2004"),
    ("The Dark Knight Rises",      "movie",  "Saturn Award Best Comic-to-Film Motion Picture 2013"),
    ("Gravity",                    "movie",  "Academy Award Best Visual Effects 2014"),
    ("The Avengers",               "movie",  "People's Choice Award Favorite Movie 2013"),
    ("Avengers: Endgame",          "movie",  "People's Choice Award Favorite Movie 2020"),
    ("Mamma Mia!",                 "movie",  "Golden Globe Best Motion Picture Musical 2009"),
    ("Ocean's Eleven",             "movie",  "BAFTA Best Editing 2002"),

    # Personal awards
    ("Leonardo DiCaprio",          "person", "Academy Award Best Actor 2016"),
    ("Brad Pitt",                  "person", "Academy Award Best Supporting Actor 2020"),
    ("George Clooney",             "person", "Academy Award Best Supporting Actor 2006"),
    ("Matt Damon",                 "person", "Academy Award Best Original Screenplay 1998"),
    ("Sandra Bullock",             "person", "Academy Award Best Actress 2010"),
    ("Anne Hathaway",              "person", "Academy Award Best Supporting Actress 2013"),
    ("Meryl Streep",               "person", "Academy Award Best Actress 2012"),
    ("Michael Caine",              "person", "Academy Award Best Supporting Actor 2005"),
    ("Christian Bale",             "person", "Academy Award Best Supporting Actor 2011"),
    ("Will Smith",                 "person", "Academy Award Best Actor 2022"),
    ("Robert Downey Jr.",          "person", "Academy Award Best Supporting Actor 2024"),
    ("Cillian Murphy",             "person", "Academy Award Best Actor 2024"),
    ("Christopher Nolan",          "person", "Academy Award Best Director 2024"),
    ("Martin Scorsese",            "person", "Academy Award Best Director 2007"),
    ("Steven Soderbergh",          "person", "Academy Award Best Director 2001"),
    ("Hans Zimmer",                "person", "Academy Award Best Original Score 2022"),
    ("Ludwig Göransson",           "person", "Academy Award Best Original Score 2019"),
    ("Meryl Streep",               "person", "Golden Globe Best Supporting Actress 2006"),
]