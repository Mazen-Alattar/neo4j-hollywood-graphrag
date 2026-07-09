# Cypher Query Practice — Hollywood Knowledge Graph

A fully self-contained lab. By the end of this document you will have a live
Neo4j graph database running locally, loaded with Hollywood data, and you will
have written queries that cover every major Cypher concept.

---

Built as part of **Codeverra** — helping you learn coding, DSA, data science, and AI the right way.  
https://codeverra.com

---

## Table of Contents

1. [What is Neo4j and Cypher?](#1-what-is-neo4j-and-cypher)
2. [Start Neo4j with Docker](#2-start-neo4j-with-docker)
3. [Open the Neo4j Browser](#3-open-the-neo4j-browser)
4. [The Data Model — what we are building](#4-the-data-model)
5. [Load the data — run these in Neo4j Browser](#5-load-the-data)
6. [Part 1 — Finding nodes](#part-1--finding-nodes)
7. [Part 2 — Filtering with WHERE](#part-2--filtering-with-where)
8. [Part 3 — Relationships](#part-3--relationships)
9. [Part 4 — Multi-hop traversal](#part-4--multi-hop-traversal)
10. [Part 5 — Aggregation](#part-5--aggregation)
11. [Part 6 — Graph-specific features](#part-6--graph-specific-features)
12. [Part 7 — Writing and modifying data](#part-7--writing-and-modifying-data)
13. [Part 8 — Challenge queries](#part-8--challenge-queries)
14. [Cypher cheat sheet](#cypher-cheat-sheet)

---

## 1. What is Neo4j and Cypher?

### Neo4j

Neo4j is a **graph database**. Instead of storing data in rows and tables (like SQL), it stores data as:

- **Nodes** — entities, like a Person or a Movie
- **Relationships** — named, directed connections between nodes, like ACTED_IN or DIRECTED
- **Properties** — key-value pairs attached to both nodes and relationships

This model is built for questions that involve connections:
*"Who worked with who?", "What are all the films connected to this director through two hops?"*
In SQL these require multiple JOINs. In Neo4j you draw the pattern and the database finds it.

```
(Leonardo DiCaprio) -[:ACTED_IN]-> (Inception) -[:WON]-> (Academy Award)
     Person                  Movie                  Award
```

### Cypher

Cypher is Neo4j's query language. It is designed to look like ASCII art of the graph pattern you are searching for.

```cypher
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
RETURN p.name, m.title
```

Read it aloud: *"Find a Person that has an ACTED_IN relationship to a Movie, return their name and the movie title."*

---

## 2. Start Neo4j with Docker

You need Docker Desktop installed and running. Open a terminal and run:

```bash
docker run -d \
     --name hollywood_neo4j \
  -p 7474:7474 \
  -p 7687:7687 \
     -e NEO4J_AUTH=neo4j/hollywood2024! \
  neo4j:5.18.0
```

**What each flag does:**

| Flag | Purpose |
|---|---|
| `-d` | Run in the background (detached mode) |
| `--name hollywood_neo4j` | Give the container a memorable name |
| `-p 7474:7474` | Map port 7474 on your machine to port 7474 in the container — this is the browser UI |
| `-p 7687:7687` | Map port 7687 — this is the Bolt protocol used by drivers and the browser to run queries |
| `-e NEO4J_AUTH=neo4j/hollywood2024!` | Set the username (`neo4j`) and password (`hollywood2024!`) |
| `neo4j:5.18.0` | The official Neo4j image from Docker Hub, version 5.18 |

Wait about 15 seconds for Neo4j to start, then verify:

```bash
docker logs hollywood_neo4j | grep "Started"
```

You should see a line like: `Remote interface available at http://localhost:7474/`

**To stop the container later:**
```bash
docker stop hollywood_neo4j
```

**To start it again:**
```bash
docker start hollywood_neo4j
```

**Important — your data is safe when you stop and restart.** Docker containers persist their data between stop/start cycles. Only running `docker rm hollywood_neo4j` (delete the container) would erase the data.

---

## 3. Open the Neo4j Browser

Go to **http://localhost:7474** in your browser.

- **Username:** `neo4j`
- **Password:** `hollywood2024!`

You will see the Neo4j Browser — a web-based query editor. There is a text field at the top where you paste Cypher queries and press **Ctrl+Enter** (Mac: **Cmd+Enter**) to run them.

Results are shown as a visual graph when you return full nodes, or as a table when you return specific properties.

---

## 4. The Data Model

Before loading anything, understand what we are building.

### Node types (labels)

| Label | What it represents | Key properties |
|---|---|---|
| `Person` | Actor, director, or music composer | `name`, `born`, `profession`, `hometown` |
| `Movie` | A Hollywood film | `title`, `year`, `genre`, `box_office_crore`, `description` |
| `ProductionHouse` | Film studio | `name`, `founded`, `founder`, `hq` |
| `Award` | A film award | `name`, `category`, `year` |

### Relationship types

```
(Person)          -[:ACTED_IN {character, lead_role}]->  (Movie)
(Person)          -[:DIRECTED]->                         (Movie)
(Person)          -[:COMPOSED_MUSIC_FOR]->               (Movie)
(Person)          -[:WON]->                              (Award)
(Movie)           -[:WON]->                              (Award)
(ProductionHouse) -[:PRODUCED]->                         (Movie)
```

### Visual diagram

```
                    ┌─────────────┐
                    │   Person    │
                    │  (Actor /   │
                    │  Director / │
                    │  Composer)  │
                    └──────┬──────┘
                           │
         ┌─────────────────┼──────────────────────┐
         │                 │                      │
    ACTED_IN           DIRECTED          COMPOSED_MUSIC_FOR
         │                 │                      │
         ▼                 ▼                      ▼
    ┌──────────┐     ┌──────────┐          ┌──────────┐
    │  Movie   │◄────│  Movie   │          │  Movie   │
    └────┬─────┘     └──────────┘          └──────────┘
         │
    ┌────┴──────────────────────────────┐
    │                                   │
   WON                              PRODUCED (by)
    │                                   │
    ▼                                   ▲
┌──────────┐                   ┌─────────────────┐
│  Award   │                   │ ProductionHouse  │
└──────────┘                   └─────────────────┘
```

---

## 5. Load the Data

Paste each block into the Neo4j Browser and run it. You can run the entire section at once or block by block.

### 5.1 Create uniqueness constraints

Constraints prevent duplicate nodes and speed up lookups. Run this first.

```cypher
CREATE CONSTRAINT person_name  IF NOT EXISTS FOR (p:Person)          REQUIRE p.name  IS UNIQUE;
CREATE CONSTRAINT movie_title  IF NOT EXISTS FOR (m:Movie)           REQUIRE m.title IS UNIQUE;
CREATE CONSTRAINT prodhouse    IF NOT EXISTS FOR (p:ProductionHouse) REQUIRE p.name  IS UNIQUE;
CREATE CONSTRAINT award_name   IF NOT EXISTS FOR (a:Award)           REQUIRE a.name  IS UNIQUE;
```

`MERGE` (used below) will use these constraints as indexes — making every upsert fast.

---

### 5.2 Create Person nodes

`MERGE` means: create the node if it does not exist, or match the existing one. Safe to re-run.

```cypher
// Actors
MERGE (n:Person {name: "Leonardo DiCaprio"})    SET n.born = 1974, n.profession = "Actor",           n.hometown = "Los Angeles";
MERGE (n:Person {name: "Tom Hardy"})            SET n.born = 1977, n.profession = "Actor",           n.hometown = "London";
MERGE (n:Person {name: "Cillian Murphy"})       SET n.born = 1976, n.profession = "Actor",           n.hometown = "Cork";
MERGE (n:Person {name: "Joseph Gordon-Levitt"}) SET n.born = 1981, n.profession = "Actor",           n.hometown = "Los Angeles";
MERGE (n:Person {name: "Brad Pitt"})            SET n.born = 1963, n.profession = "Actor",           n.hometown = "Shawnee";
MERGE (n:Person {name: "George Clooney"})       SET n.born = 1961, n.profession = "Actor",           n.hometown = "Lexington";
MERGE (n:Person {name: "Matt Damon"})           SET n.born = 1970, n.profession = "Actor",           n.hometown = "Cambridge";
MERGE (n:Person {name: "Christian Bale"})       SET n.born = 1974, n.profession = "Actor",           n.hometown = "Haverfordwest";
MERGE (n:Person {name: "Michael Caine"})        SET n.born = 1933, n.profession = "Actor",           n.hometown = "London";
MERGE (n:Person {name: "Robert Downey Jr."})    SET n.born = 1965, n.profession = "Actor",           n.hometown = "New York City";
MERGE (n:Person {name: "Scarlett Johansson"})   SET n.born = 1984, n.profession = "Actor",           n.hometown = "New York City";
MERGE (n:Person {name: "Chris Evans"})          SET n.born = 1981, n.profession = "Actor",           n.hometown = "Boston";
MERGE (n:Person {name: "Chris Hemsworth"})      SET n.born = 1983, n.profession = "Actor",           n.hometown = "Melbourne";
MERGE (n:Person {name: "Will Smith"})           SET n.born = 1968, n.profession = "Actor",           n.hometown = "Philadelphia";
MERGE (n:Person {name: "Martin Lawrence"})      SET n.born = 1965, n.profession = "Actor",           n.hometown = "Frankfurt";
MERGE (n:Person {name: "Anne Hathaway"})        SET n.born = 1982, n.profession = "Actor",           n.hometown = "Brooklyn";
MERGE (n:Person {name: "Meryl Streep"})         SET n.born = 1949, n.profession = "Actor",           n.hometown = "Summit";
MERGE (n:Person {name: "Emily Blunt"})          SET n.born = 1983, n.profession = "Actor",           n.hometown = "London";
MERGE (n:Person {name: "Sandra Bullock"})       SET n.born = 1964, n.profession = "Actor",           n.hometown = "Arlington";
MERGE (n:Person {name: "Margot Robbie"})        SET n.born = 1990, n.profession = "Actor",           n.hometown = "Dalby";
MERGE (n:Person {name: "Ryan Gosling"})         SET n.born = 1980, n.profession = "Actor",           n.hometown = "London, Ontario";
MERGE (n:Person {name: "Russell Crowe"})        SET n.born = 1964, n.profession = "Actor",           n.hometown = "Wellington";
MERGE (n:Person {name: "Amanda Seyfried"})      SET n.born = 1985, n.profession = "Actor",           n.hometown = "Allentown";
MERGE (n:Person {name: "Christine Baranski"})   SET n.born = 1952, n.profession = "Actor",           n.hometown = "Buffalo";

// Directors
MERGE (n:Person {name: "Christopher Nolan"})     SET n.born = 1970, n.profession = "Director",          n.hometown = "London";
MERGE (n:Person {name: "Martin Scorsese"})       SET n.born = 1942, n.profession = "Director",          n.hometown = "New York City";
MERGE (n:Person {name: "Greta Gerwig"})          SET n.born = 1983, n.profession = "Director",          n.hometown = "Sacramento";
MERGE (n:Person {name: "Shane Black"})           SET n.born = 1961, n.profession = "Director",          n.hometown = "Pittsburgh";
MERGE (n:Person {name: "Tom Hooper"})            SET n.born = 1972, n.profession = "Director",          n.hometown = "London";
MERGE (n:Person {name: "Michael Bay"})           SET n.born = 1965, n.profession = "Director",          n.hometown = "Los Angeles";
MERGE (n:Person {name: "Steven Soderbergh"})     SET n.born = 1963, n.profession = "Director",          n.hometown = "Atlanta";
MERGE (n:Person {name: "David Frankel"})         SET n.born = 1959, n.profession = "Director",          n.hometown = "New York City";
MERGE (n:Person {name: "Phyllida Lloyd"})        SET n.born = 1957, n.profession = "Director",          n.hometown = "Bristol";
MERGE (n:Person {name: "Ol Parker"})             SET n.born = 1969, n.profession = "Director",          n.hometown = "London";
MERGE (n:Person {name: "Jan de Bont"})           SET n.born = 1943, n.profession = "Director",          n.hometown = "Eindhoven";
MERGE (n:Person {name: "Alfonso Cuarón"})        SET n.born = 1961, n.profession = "Director",          n.hometown = "Mexico City";
MERGE (n:Person {name: "Jon Favreau"})           SET n.born = 1966, n.profession = "Director",          n.hometown = "Queens";
MERGE (n:Person {name: "Joss Whedon"})           SET n.born = 1964, n.profession = "Director",          n.hometown = "New York City";
MERGE (n:Person {name: "Anthony Russo"})         SET n.born = 1970, n.profession = "Director",          n.hometown = "Cleveland";
MERGE (n:Person {name: "Joe Russo"})             SET n.born = 1971, n.profession = "Director",          n.hometown = "Cleveland";
MERGE (n:Person {name: "The Russo Brothers"})    SET n.born = 1970, n.profession = "Director",          n.hometown = "Cleveland";
MERGE (n:Person {name: "James Mangold"})         SET n.born = 1963, n.profession = "Director",          n.hometown = "New York City";
MERGE (n:Person {name: "Quentin Tarantino"})     SET n.born = 1963, n.profession = "Director",          n.hometown = "Knoxville";
MERGE (n:Person {name: "Gary Ross"})             SET n.born = 1956, n.profession = "Director",          n.hometown = "Los Angeles";
MERGE (n:Person {name: "The Coen Brothers"})     SET n.born = 1954, n.profession = "Director",          n.hometown = "United States";
MERGE (n:Person {name: "Alejandro G. Iñárritu"}) SET n.born = 1963, n.profession = "Director",          n.hometown = "Mexico City";
MERGE (n:Person {name: "James Cameron"})         SET n.born = 1954, n.profession = "Director",          n.hometown = "Kapuskasing";

// Music composers
MERGE (n:Person {name: "Hans Zimmer"})            SET n.born = 1957, n.profession = "Music Composer",  n.hometown = "Frankfurt";
MERGE (n:Person {name: "Ludwig Göransson"})       SET n.born = 1984, n.profession = "Music Composer",  n.hometown = "Linköping";
MERGE (n:Person {name: "Howard Shore"})           SET n.born = 1946, n.profession = "Music Composer",  n.hometown = "Toronto";
MERGE (n:Person {name: "Mark Mancina"})           SET n.born = 1957, n.profession = "Music Composer",  n.hometown = "Santa Monica";
MERGE (n:Person {name: "Alan Silvestri"})         SET n.born = 1950, n.profession = "Music Composer",  n.hometown = "New York City";
MERGE (n:Person {name: "David Holmes"})           SET n.born = 1969, n.profession = "Music Composer",  n.hometown = "Belfast";
MERGE (n:Person {name: "Theodore Shapiro"})       SET n.born = 1971, n.profession = "Music Composer",  n.hometown = "New York City";
MERGE (n:Person {name: "Benny Andersson"})        SET n.born = 1946, n.profession = "Music Composer",  n.hometown = "Stockholm";
MERGE (n:Person {name: "Steven Price"})           SET n.born = 1977, n.profession = "Music Composer",  n.hometown = "Nottingham";
MERGE (n:Person {name: "John Debney"})            SET n.born = 1956, n.profession = "Music Composer",  n.hometown = "Glendale";
MERGE (n:Person {name: "Claude-Michel Schönberg"}) SET n.born = 1944, n.profession = "Music Composer",  n.hometown = "Vannes";
MERGE (n:Person {name: "Marco Beltrami"})         SET n.born = 1966, n.profession = "Music Composer",  n.hometown = "New York City";
MERGE (n:Person {name: "Carter Burwell"})         SET n.born = 1954, n.profession = "Music Composer",  n.hometown = "New York City";
MERGE (n:Person {name: "Daniel Pemberton"})       SET n.born = 1977, n.profession = "Music Composer",  n.hometown = "London";
MERGE (n:Person {name: "John Ottman"})            SET n.born = 1964, n.profession = "Music Composer",  n.hometown = "San Diego";
MERGE (n:Person {name: "Mark Ronson and Andrew Wyatt"}) SET n.born = 1975, n.profession = "Music Composer",  n.hometown = "London";
MERGE (n:Person {name: "Ryuichi Sakamoto"})       SET n.born = 1952, n.profession = "Music Composer",  n.hometown = "Tokyo";
MERGE (n:Person {name: "James Newton Howard"})    SET n.born = 1951, n.profession = "Music Composer",  n.hometown = "Los Angeles";
```

---

### 5.3 Create Movie nodes

```cypher
MERGE (m:Movie {title: "Inception"})
SET m.year = 2010, m.genre = "Science Fiction Thriller", m.box_office_crore = 829.9,
    m.description = "A skilled thief enters dreams to steal secrets and is offered a chance to erase his past by planting an idea.";

MERGE (m:Movie {title: "The Revenant"})
SET m.year = 2015, m.genre = "Adventure Drama", m.box_office_crore = 533.0,
    m.description = "A frontiersman fights for survival after being left for dead in the unforgiving American wilderness.";

MERGE (m:Movie {title: "The Wolf of Wall Street"})
SET m.year = 2013, m.genre = "Biographical Comedy Drama", m.box_office_crore = 392.0,
    m.description = "A stockbroker's rapid rise and scandalous fall on Wall Street is told with black comedy and excess.";

MERGE (m:Movie {title: "Barbie"})
SET m.year = 2023, m.genre = "Fantasy Comedy", m.box_office_crore = 1450.0,
    m.description = "Barbie leaves her perfect world and discovers what it means to live in the real one.";

MERGE (m:Movie {title: "The Nice Guys"})
SET m.year = 2016, m.genre = "Crime Comedy", m.box_office_crore = 62.8,
    m.description = "A private eye and a hired enforcer stumble into a conspiracy in 1970s Los Angeles.";

MERGE (m:Movie {title: "Les Misérables"})
SET m.year = 2012, m.genre = "Musical Drama", m.box_office_crore = 441.8,
    m.description = "A former prisoner is relentlessly pursued by a police inspector while trying to build a new life.";

MERGE (m:Movie {title: "Batman Begins"})
SET m.year = 2005, m.genre = "Superhero Action", m.box_office_crore = 373.7,
    m.description = "Bruce Wayne learns to fight fear and becomes Batman to save Gotham City.";

MERGE (m:Movie {title: "The Dark Knight"})
SET m.year = 2008, m.genre = "Superhero Crime", m.box_office_crore = 1006.0,
    m.description = "Batman faces the chaos-driven Joker while Gotham is pushed to the brink.";

MERGE (m:Movie {title: "The Dark Knight Rises"})
SET m.year = 2012, m.genre = "Superhero Action", m.box_office_crore = 1084.9,
    m.description = "Batman returns to defend Gotham from Bane after years in hiding.";

MERGE (m:Movie {title: "Interstellar"})
SET m.year = 2014, m.genre = "Science Fiction Drama", m.box_office_crore = 758.6,
    m.description = "A team travels through a wormhole in search of a new home for humanity.";

MERGE (m:Movie {title: "The Devil Wears Prada"})
SET m.year = 2006, m.genre = "Comedy Drama", m.box_office_crore = 326.7,
    m.description = "A young assistant navigates the high-pressure world of a powerful fashion magazine editor.";

MERGE (m:Movie {title: "Mamma Mia!"})
SET m.year = 2008, m.genre = "Musical Romance", m.box_office_crore = 694.0,
    m.description = "A bride on a Greek island invites three men from her mother's past to discover who is her father.";

MERGE (m:Movie {title: "Mamma Mia! Here We Go Again"})
SET m.year = 2018, m.genre = "Musical Romance", m.box_office_crore = 395.0,
    m.description = "A new generation revisits the story of Donna and the island where it all began.";

MERGE (m:Movie {title: "Bad Boys"})
SET m.year = 1995, m.genre = "Action Comedy", m.box_office_crore = 141.4,
    m.description = "Two Miami detectives race to recover stolen evidence and protect a witness.";

MERGE (m:Movie {title: "Bad Boys II"})
SET m.year = 2003, m.genre = "Action Comedy", m.box_office_crore = 273.0,
    m.description = "The detectives tackle a drug trafficking case that spirals into chaos across Miami.";

MERGE (m:Movie {title: "Bad Boys for Life"})
SET m.year = 2020, m.genre = "Action Comedy", m.box_office_crore = 426.5,
    m.description = "The old-school detectives reunite to take down a ruthless cartel boss.";

MERGE (m:Movie {title: "Ocean's Eleven"})
SET m.year = 2001, m.genre = "Heist Thriller", m.box_office_crore = 451.5,
    m.description = "A suave criminal assembles a crew to rob three Las Vegas casinos in one night.";

MERGE (m:Movie {title: "Ocean's Twelve"})
SET m.year = 2004, m.genre = "Heist Comedy", m.box_office_crore = 362.0,
    m.description = "The crew reunites for another globe-trotting heist after a new challenge in Europe.";

MERGE (m:Movie {title: "Ocean's Thirteen"})
SET m.year = 2007, m.genre = "Heist Comedy", m.box_office_crore = 311.7,
    m.description = "The team plots revenge against a ruthless casino owner who betrayed one of their own.";

MERGE (m:Movie {title: "Ocean's 8"})
SET m.year = 2018, m.genre = "Heist Comedy", m.box_office_crore = 297.0,
    m.description = "Debbie Ocean assembles a team to pull off an elaborate heist at the Met Gala.";

MERGE (m:Movie {title: "Gravity"})
SET m.year = 2013, m.genre = "Science Fiction Thriller", m.box_office_crore = 723.2,
    m.description = "Two astronauts fight for survival after debris destroys their shuttle in orbit.";

MERGE (m:Movie {title: "Iron Man 2"})
SET m.year = 2010, m.genre = "Superhero Action", m.box_office_crore = 621.0,
    m.description = "Tony Stark faces new threats while dealing with a failing arc reactor and rising enemies.";

MERGE (m:Movie {title: "The Avengers"})
SET m.year = 2012, m.genre = "Superhero Action", m.box_office_crore = 1518.8,
    m.description = "Earth's greatest heroes unite to stop Loki and his alien invasion.";

MERGE (m:Movie {title: "Avengers: Endgame"})
SET m.year = 2019, m.genre = "Superhero Action", m.box_office_crore = 2797.8,
    m.description = "The remaining Avengers attempt to undo Thanos' catastrophic snap.";

MERGE (m:Movie {title: "Oppenheimer"})
SET m.year = 2023, m.genre = "Biographical Drama", m.box_office_crore = 976.0,
    m.description = "The story of J. Robert Oppenheimer and the creation of the atomic bomb.";

MERGE (m:Movie {title: "Ford v Ferrari"})
SET m.year = 2019, m.genre = "Sports Drama", m.box_office_crore = 225.5,
    m.description = "Car designer Carroll Shelby and driver Ken Miles battle Ferrari at Le Mans for Ford.";

MERGE (m:Movie {title: "Burn After Reading"})
SET m.year = 2008, m.genre = "Black Comedy", m.box_office_crore = 163.7,
    m.description = "Two gym employees stumble into a tangled web of secrets, espionage and bad decisions.";
```

---

### 5.4 Create ProductionHouse nodes

```cypher
MERGE (n:ProductionHouse {name: "Warner Bros. Pictures"})    SET n.founded = 1923, n.founder = "Warner brothers",      n.hq = "Burbank";
MERGE (n:ProductionHouse {name: "Legendary Pictures"})       SET n.founded = 2000, n.founder = "Thomas Tull",          n.hq = "Burbank";
MERGE (n:ProductionHouse {name: "Syncopy"})                  SET n.founded = 2001, n.founder = "Christopher Nolan",   n.hq = "London";
MERGE (n:ProductionHouse {name: "Red Granite Pictures"})     SET n.founded = 2010, n.founder = "Riza Aziz",            n.hq = "Los Angeles";
MERGE (n:ProductionHouse {name: "Columbia Pictures"})        SET n.founded = 1918, n.founder = "Harry Cohn",           n.hq = "Culver City";
MERGE (n:ProductionHouse {name: "Village Roadshow Pictures"}) SET n.founded = 1986, n.founder = "Greg Coote",         n.hq = "Melbourne";
MERGE (n:ProductionHouse {name: "Marvel Studios"})           SET n.founded = 1993, n.founder = "Avi Arad",            n.hq = "Burbank";
MERGE (n:ProductionHouse {name: "20th Century Fox"})         SET n.founded = 1935, n.founder = "Joseph Schenck",      n.hq = "Los Angeles";
MERGE (n:ProductionHouse {name: "Universal Pictures"})       SET n.founded = 1912, n.founder = "Carl Laemmle",        n.hq = "Universal City";
MERGE (n:ProductionHouse {name: "Working Title Films"})      SET n.founded = 1983, n.founder = "Tim Bevan",           n.hq = "London";
MERGE (n:ProductionHouse {name: "Paramount Pictures"})       SET n.founded = 1912, n.founder = "Adolph Zukor",        n.hq = "Hollywood";
MERGE (n:ProductionHouse {name: "Regency Enterprises"})      SET n.founded = 1982, n.founder = "Arnon Milchan",       n.hq = "Beverly Hills";
MERGE (n:ProductionHouse {name: "Focus Features"})          SET n.founded = 2001, n.founder = "Universal Pictures",  n.hq = "Universal City";
MERGE (n:ProductionHouse {name: "Silver Pictures"})          SET n.founded = 1980, n.founder = "Joel Silver",         n.hq = "Los Angeles";
MERGE (n:ProductionHouse {name: "Mattel Films"})             SET n.founded = 2018, n.founder = "Mattel",              n.hq = "El Segundo";
```

---

### 5.5 Create Award nodes

```cypher
MERGE (a:Award {name: "Academy Award Best Actor 2016"})              SET a.category = "Academy", a.year = 2016;
MERGE (a:Award {name: "Academy Award Best Supporting Actor 2020"})   SET a.category = "Academy", a.year = 2020;
MERGE (a:Award {name: "Academy Award Best Supporting Actor 2006"})   SET a.category = "Academy", a.year = 2006;
MERGE (a:Award {name: "Academy Award Best Original Screenplay 1998"}) SET a.category = "Academy", a.year = 1998;
MERGE (a:Award {name: "Academy Award Best Actress 2010"})             SET a.category = "Academy", a.year = 2010;
MERGE (a:Award {name: "Academy Award Best Supporting Actress 2013"})  SET a.category = "Academy", a.year = 2013;
MERGE (a:Award {name: "Academy Award Best Actress 2012"})             SET a.category = "Academy", a.year = 2012;
MERGE (a:Award {name: "Academy Award Best Supporting Actor 2005"})    SET a.category = "Academy", a.year = 2005;
MERGE (a:Award {name: "Academy Award Best Supporting Actor 2011"})    SET a.category = "Academy", a.year = 2011;
MERGE (a:Award {name: "Academy Award Best Actor 2022"})               SET a.category = "Academy", a.year = 2022;
MERGE (a:Award {name: "Academy Award Best Supporting Actor 2024"})    SET a.category = "Academy", a.year = 2024;
MERGE (a:Award {name: "Academy Award Best Actor 2024"})               SET a.category = "Academy", a.year = 2024;
MERGE (a:Award {name: "Academy Award Best Director 2024"})            SET a.category = "Academy", a.year = 2024;
MERGE (a:Award {name: "Academy Award Best Director 2007"})            SET a.category = "Academy", a.year = 2007;
MERGE (a:Award {name: "Academy Award Best Director 2001"})            SET a.category = "Academy", a.year = 2001;
MERGE (a:Award {name: "Academy Award Best Original Score 2022"})      SET a.category = "Academy", a.year = 2022;
MERGE (a:Award {name: "Academy Award Best Original Score 2019"})      SET a.category = "Academy", a.year = 2019;
MERGE (a:Award {name: "Academy Award Best Visual Effects 2000"})      SET a.category = "Academy", a.year = 2000;
MERGE (a:Award {name: "Academy Award Best Visual Effects 2011"})      SET a.category = "Academy", a.year = 2011;
MERGE (a:Award {name: "Academy Award Best Visual Effects 2014"})      SET a.category = "Academy", a.year = 2014;
MERGE (a:Award {name: "Saturn Award Best Science Fiction Film 2004"}) SET a.category = "Saturn", a.year = 2004;
MERGE (a:Award {name: "Saturn Award Best Comic-to-Film Motion Picture 2013"}) SET a.category = "Saturn", a.year = 2013;
MERGE (a:Award {name: "People's Choice Award Favorite Movie 2013"})   SET a.category = "People's Choice", a.year = 2013;
MERGE (a:Award {name: "People's Choice Award Favorite Movie 2020"})   SET a.category = "People's Choice", a.year = 2020;
MERGE (a:Award {name: "MTV Movie Award Best On-Screen Duo 1996"})     SET a.category = "MTV", a.year = 1996;
MERGE (a:Award {name: "Golden Globe Best Supporting Actress 2006"})   SET a.category = "Golden Globe", a.year = 2006;
MERGE (a:Award {name: "Golden Globe Best Motion Picture Musical 2009"}) SET a.category = "Golden Globe", a.year = 2009;
MERGE (a:Award {name: "Golden Globe Best Actor 2014"})                 SET a.category = "Golden Globe", a.year = 2014;
MERGE (a:Award {name: "BAFTA Best Film 2016"})                         SET a.category = "BAFTA", a.year = 2016;
MERGE (a:Award {name: "BAFTA Best Cinematography 2014"})               SET a.category = "BAFTA", a.year = 2014;
MERGE (a:Award {name: "BAFTA Best Editing 2002"})                      SET a.category = "BAFTA", a.year = 2002;
MERGE (a:Award {name: "Grammy Best Compilation Soundtrack 2017"})     SET a.category = "Grammy", a.year = 2017;
```

---

### 5.6 Create ACTED_IN relationships

```cypher
MATCH (p:Person {name: "Leonardo DiCaprio"}),   (m:Movie {title: "Inception"})                   MERGE (p)-[:ACTED_IN {character: "Cobb",                    lead_role: true}]->(m);
MATCH (p:Person {name: "Tom Hardy"}),           (m:Movie {title: "Inception"})                   MERGE (p)-[:ACTED_IN {character: "Eames",                   lead_role: true}]->(m);
MATCH (p:Person {name: "Cillian Murphy"}),      (m:Movie {title: "Inception"})                   MERGE (p)-[:ACTED_IN {character: "Robert Fischer",          lead_role: false}]->(m);
MATCH (p:Person {name: "Joseph Gordon-Levitt"}),(m:Movie {title: "Inception"})                   MERGE (p)-[:ACTED_IN {character: "Arthur",                  lead_role: true}]->(m);
MATCH (p:Person {name: "Leonardo DiCaprio"}),   (m:Movie {title: "The Revenant"})                MERGE (p)-[:ACTED_IN {character: "Hugh Glass",              lead_role: true}]->(m);
MATCH (p:Person {name: "Tom Hardy"}),           (m:Movie {title: "The Revenant"})                MERGE (p)-[:ACTED_IN {character: "John Fitzgerald",        lead_role: false}]->(m);
MATCH (p:Person {name: "Leonardo DiCaprio"}),   (m:Movie {title: "The Wolf of Wall Street"})     MERGE (p)-[:ACTED_IN {character: "Jordan Belfort",         lead_role: true}]->(m);
MATCH (p:Person {name: "Margot Robbie"}),       (m:Movie {title: "The Wolf of Wall Street"})     MERGE (p)-[:ACTED_IN {character: "Naomi Lapaglia",         lead_role: true}]->(m);
MATCH (p:Person {name: "Matthew McConaughey"}),  (m:Movie {title: "The Wolf of Wall Street"})     MERGE (p)-[:ACTED_IN {character: "Mark Hanna",              lead_role: false}]->(m);
MATCH (p:Person {name: "Margot Robbie"}),       (m:Movie {title: "Barbie"})                      MERGE (p)-[:ACTED_IN {character: "Barbie",                 lead_role: true}]->(m);
MATCH (p:Person {name: "Ryan Gosling"}),        (m:Movie {title: "Barbie"})                      MERGE (p)-[:ACTED_IN {character: "Ken",                    lead_role: true}]->(m);
MATCH (p:Person {name: "Ryan Gosling"}),        (m:Movie {title: "The Nice Guys"})               MERGE (p)-[:ACTED_IN {character: "Holland March",          lead_role: true}]->(m);
MATCH (p:Person {name: "Russell Crowe"}),       (m:Movie {title: "The Nice Guys"})               MERGE (p)-[:ACTED_IN {character: "Jackson Healy",         lead_role: true}]->(m);
MATCH (p:Person {name: "Anne Hathaway"}),       (m:Movie {title: "Les Misérables"})              MERGE (p)-[:ACTED_IN {character: "Fantine",                lead_role: true}]->(m);
MATCH (p:Person {name: "Russell Crowe"}),       (m:Movie {title: "Les Misérables"})              MERGE (p)-[:ACTED_IN {character: "Javert",                 lead_role: true}]->(m);
MATCH (p:Person {name: "Amanda Seyfried"}),     (m:Movie {title: "Les Misérables"})              MERGE (p)-[:ACTED_IN {character: "Cosette",                lead_role: true}]->(m);
MATCH (p:Person {name: "Meryl Streep"}),         (m:Movie {title: "Mamma Mia!"})                  MERGE (p)-[:ACTED_IN {character: "Donna",                  lead_role: true}]->(m);
MATCH (p:Person {name: "Amanda Seyfried"}),     (m:Movie {title: "Mamma Mia!"})                  MERGE (p)-[:ACTED_IN {character: "Sophie",                 lead_role: true}]->(m);
MATCH (p:Person {name: "Christine Baranski"}),  (m:Movie {title: "Mamma Mia!"})                  MERGE (p)-[:ACTED_IN {character: "Tanya",                  lead_role: true}]->(m);
MATCH (p:Person {name: "Meryl Streep"}),         (m:Movie {title: "Mamma Mia! Here We Go Again"}) MERGE (p)-[:ACTED_IN {character: "Donna",                  lead_role: true}]->(m);
MATCH (p:Person {name: "Amanda Seyfried"}),     (m:Movie {title: "Mamma Mia! Here We Go Again"}) MERGE (p)-[:ACTED_IN {character: "Sophie",                 lead_role: true}]->(m);
MATCH (p:Person {name: "Christine Baranski"}),  (m:Movie {title: "Mamma Mia! Here We Go Again"}) MERGE (p)-[:ACTED_IN {character: "Tanya",                  lead_role: true}]->(m);
MATCH (p:Person {name: "Christian Bale"}),       (m:Movie {title: "Batman Begins"})               MERGE (p)-[:ACTED_IN {character: "Bruce Wayne",            lead_role: true}]->(m);
MATCH (p:Person {name: "Michael Caine"}),        (m:Movie {title: "Batman Begins"})               MERGE (p)-[:ACTED_IN {character: "Alfred Pennyworth",      lead_role: false}]->(m);
MATCH (p:Person {name: "Cillian Murphy"}),       (m:Movie {title: "Batman Begins"})               MERGE (p)-[:ACTED_IN {character: "Dr. Jonathan Crane",    lead_role: false}]->(m);
MATCH (p:Person {name: "Christian Bale"}),       (m:Movie {title: "The Dark Knight"})             MERGE (p)-[:ACTED_IN {character: "Bruce Wayne",            lead_role: true}]->(m);
MATCH (p:Person {name: "Michael Caine"}),        (m:Movie {title: "The Dark Knight"})             MERGE (p)-[:ACTED_IN {character: "Alfred Pennyworth",      lead_role: false}]->(m);
MATCH (p:Person {name: "Cillian Murphy"}),       (m:Movie {title: "The Dark Knight"})             MERGE (p)-[:ACTED_IN {character: "Dr. Jonathan Crane",    lead_role: false}]->(m);
MATCH (p:Person {name: "Christian Bale"}),       (m:Movie {title: "The Dark Knight Rises"})       MERGE (p)-[:ACTED_IN {character: "Bruce Wayne",            lead_role: true}]->(m);
MATCH (p:Person {name: "Michael Caine"}),        (m:Movie {title: "The Dark Knight Rises"})       MERGE (p)-[:ACTED_IN {character: "Alfred Pennyworth",      lead_role: false}]->(m);
MATCH (p:Person {name: "Tom Hardy"}),            (m:Movie {title: "The Dark Knight Rises"})       MERGE (p)-[:ACTED_IN {character: "Bane",                    lead_role: true}]->(m);
MATCH (p:Person {name: "Joseph Gordon-Levitt"}),(m:Movie {title: "The Dark Knight Rises"})       MERGE (p)-[:ACTED_IN {character: "John Blake",             lead_role: true}]->(m);
MATCH (p:Person {name: "Matthew McConaughey"}),  (m:Movie {title: "Interstellar"})                MERGE (p)-[:ACTED_IN {character: "Cooper",                 lead_role: true}]->(m);
MATCH (p:Person {name: "Anne Hathaway"}),        (m:Movie {title: "Interstellar"})                MERGE (p)-[:ACTED_IN {character: "Brand",                  lead_role: true}]->(m);
MATCH (p:Person {name: "Michael Caine"}),        (m:Movie {title: "Interstellar"})                MERGE (p)-[:ACTED_IN {character: "Professor Brand",       lead_role: false}]->(m);
MATCH (p:Person {name: "Anne Hathaway"}),        (m:Movie {title: "The Devil Wears Prada"})       MERGE (p)-[:ACTED_IN {character: "Andy Sachs",             lead_role: true}]->(m);
MATCH (p:Person {name: "Meryl Streep"}),         (m:Movie {title: "The Devil Wears Prada"})       MERGE (p)-[:ACTED_IN {character: "Miranda Priestly",       lead_role: true}]->(m);
MATCH (p:Person {name: "Emily Blunt"}),          (m:Movie {title: "The Devil Wears Prada"})       MERGE (p)-[:ACTED_IN {character: "Emily Charlton",         lead_role: true}]->(m);
MATCH (p:Person {name: "Will Smith"}),            (m:Movie {title: "Bad Boys"})                    MERGE (p)-[:ACTED_IN {character: "Mike Lowrey",            lead_role: true}]->(m);
MATCH (p:Person {name: "Martin Lawrence"}),      (m:Movie {title: "Bad Boys"})                    MERGE (p)-[:ACTED_IN {character: "Marcus Burnett",         lead_role: true}]->(m);
MATCH (p:Person {name: "Will Smith"}),            (m:Movie {title: "Bad Boys II"})                 MERGE (p)-[:ACTED_IN {character: "Mike Lowrey",            lead_role: true}]->(m);
MATCH (p:Person {name: "Martin Lawrence"}),      (m:Movie {title: "Bad Boys II"})                 MERGE (p)-[:ACTED_IN {character: "Marcus Burnett",         lead_role: true}]->(m);
MATCH (p:Person {name: "Will Smith"}),            (m:Movie {title: "Bad Boys for Life"})           MERGE (p)-[:ACTED_IN {character: "Mike Lowrey",            lead_role: true}]->(m);
MATCH (p:Person {name: "Martin Lawrence"}),      (m:Movie {title: "Bad Boys for Life"})           MERGE (p)-[:ACTED_IN {character: "Marcus Burnett",         lead_role: true}]->(m);
MATCH (p:Person {name: "Brad Pitt"}),             (m:Movie {title: "Ocean's Eleven"})              MERGE (p)-[:ACTED_IN {character: "Rusty Ryan",             lead_role: true}]->(m);
MATCH (p:Person {name: "George Clooney"}),        (m:Movie {title: "Ocean's Eleven"})              MERGE (p)-[:ACTED_IN {character: "Danny Ocean",            lead_role: true}]->(m);
MATCH (p:Person {name: "Matt Damon"}),            (m:Movie {title: "Ocean's Eleven"})              MERGE (p)-[:ACTED_IN {character: "Linus Caldwell",         lead_role: true}]->(m);
MATCH (p:Person {name: "Brad Pitt"}),             (m:Movie {title: "Ocean's Twelve"})              MERGE (p)-[:ACTED_IN {character: "Rusty Ryan",             lead_role: true}]->(m);
MATCH (p:Person {name: "George Clooney"}),        (m:Movie {title: "Ocean's Twelve"})              MERGE (p)-[:ACTED_IN {character: "Danny Ocean",            lead_role: true}]->(m);
MATCH (p:Person {name: "Matt Damon"}),            (m:Movie {title: "Ocean's Twelve"})              MERGE (p)-[:ACTED_IN {character: "Linus Caldwell",         lead_role: true}]->(m);
MATCH (p:Person {name: "Brad Pitt"}),             (m:Movie {title: "Ocean's Thirteen"})            MERGE (p)-[:ACTED_IN {character: "Rusty Ryan",             lead_role: true}]->(m);
MATCH (p:Person {name: "George Clooney"}),        (m:Movie {title: "Ocean's Thirteen"})            MERGE (p)-[:ACTED_IN {character: "Danny Ocean",            lead_role: true}]->(m);
MATCH (p:Person {name: "Matt Damon"}),            (m:Movie {title: "Ocean's Thirteen"})            MERGE (p)-[:ACTED_IN {character: "Linus Caldwell",         lead_role: true}]->(m);
MATCH (p:Person {name: "Sandra Bullock"}),        (m:Movie {title: "Ocean's 8"})                   MERGE (p)-[:ACTED_IN {character: "Debbie Ocean",           lead_role: true}]->(m);
MATCH (p:Person {name: "Anne Hathaway"}),         (m:Movie {title: "Ocean's 8"})                   MERGE (p)-[:ACTED_IN {character: "Daphne Kluger",          lead_role: true}]->(m);
MATCH (p:Person {name: "Sandra Bullock"}),        (m:Movie {title: "Gravity"})                     MERGE (p)-[:ACTED_IN {character: "Dr. Ryan Stone",         lead_role: true}]->(m);
MATCH (p:Person {name: "George Clooney"}),        (m:Movie {title: "Gravity"})                     MERGE (p)-[:ACTED_IN {character: "Matt Kowalski",          lead_role: true}]->(m);
MATCH (p:Person {name: "Robert Downey Jr."}),     (m:Movie {title: "Iron Man 2"})                  MERGE (p)-[:ACTED_IN {character: "Tony Stark",             lead_role: true}]->(m);
MATCH (p:Person {name: "Scarlett Johansson"}),    (m:Movie {title: "Iron Man 2"})                  MERGE (p)-[:ACTED_IN {character: "Natalie Rushman",        lead_role: true}]->(m);
MATCH (p:Person {name: "Robert Downey Jr."}),     (m:Movie {title: "The Avengers"})                MERGE (p)-[:ACTED_IN {character: "Tony Stark",             lead_role: true}]->(m);
MATCH (p:Person {name: "Scarlett Johansson"}),    (m:Movie {title: "The Avengers"})                MERGE (p)-[:ACTED_IN {character: "Natasha Romanoff",       lead_role: true}]->(m);
MATCH (p:Person {name: "Chris Evans"}),            (m:Movie {title: "The Avengers"})                MERGE (p)-[:ACTED_IN {character: "Steve Rogers",           lead_role: true}]->(m);
MATCH (p:Person {name: "Chris Hemsworth"}),        (m:Movie {title: "The Avengers"})                MERGE (p)-[:ACTED_IN {character: "Thor",                  lead_role: true}]->(m);
MATCH (p:Person {name: "Robert Downey Jr."}),     (m:Movie {title: "Avengers: Endgame"})           MERGE (p)-[:ACTED_IN {character: "Tony Stark",             lead_role: true}]->(m);
MATCH (p:Person {name: "Scarlett Johansson"}),    (m:Movie {title: "Avengers: Endgame"})           MERGE (p)-[:ACTED_IN {character: "Natasha Romanoff",       lead_role: true}]->(m);
MATCH (p:Person {name: "Chris Evans"}),            (m:Movie {title: "Avengers: Endgame"})           MERGE (p)-[:ACTED_IN {character: "Steve Rogers",           lead_role: true}]->(m);
MATCH (p:Person {name: "Chris Hemsworth"}),        (m:Movie {title: "Avengers: Endgame"})           MERGE (p)-[:ACTED_IN {character: "Thor",                  lead_role: true}]->(m);
MATCH (p:Person {name: "Cillian Murphy"}),         (m:Movie {title: "Oppenheimer"})                 MERGE (p)-[:ACTED_IN {character: "J. Robert Oppenheimer",  lead_role: true}]->(m);
MATCH (p:Person {name: "Robert Downey Jr."}),     (m:Movie {title: "Oppenheimer"})                 MERGE (p)-[:ACTED_IN {character: "Lewis Strauss",          lead_role: true}]->(m);
MATCH (p:Person {name: "Emily Blunt"}),            (m:Movie {title: "Oppenheimer"})                 MERGE (p)-[:ACTED_IN {character: "Kitty Oppenheimer",      lead_role: true}]->(m);
MATCH (p:Person {name: "Matt Damon"}),              (m:Movie {title: "Oppenheimer"})                 MERGE (p)-[:ACTED_IN {character: "Leslie Groves",          lead_role: true}]->(m);
MATCH (p:Person {name: "Matt Damon"}),              (m:Movie {title: "Ford v Ferrari"})             MERGE (p)-[:ACTED_IN {character: "Carroll Shelby",         lead_role: true}]->(m);
MATCH (p:Person {name: "Christian Bale"}),          (m:Movie {title: "Ford v Ferrari"})             MERGE (p)-[:ACTED_IN {character: "Ken Miles",              lead_role: true}]->(m);
MATCH (p:Person {name: "Brad Pitt"}),               (m:Movie {title: "Burn After Reading"})          MERGE (p)-[:ACTED_IN {character: "Chad Feldheimer",       lead_role: true}]->(m);
MATCH (p:Person {name: "George Clooney"}),          (m:Movie {title: "Burn After Reading"})          MERGE (p)-[:ACTED_IN {character: "Harry Pfarrer",         lead_role: true}]->(m);
```

---

### 5.7 Create DIRECTED relationships

```cypher
MATCH (d:Person {name: "Christopher Nolan"}),      (m:Movie {title: "Inception"})                  MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Alejandro G. Iñárritu"}), (m:Movie {title: "The Revenant"})               MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Martin Scorsese"}),        (m:Movie {title: "The Wolf of Wall Street"})    MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Greta Gerwig"}),           (m:Movie {title: "Barbie"})                     MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Shane Black"}),            (m:Movie {title: "The Nice Guys"})              MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Tom Hooper"}),             (m:Movie {title: "Les Misérables"})             MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Phyllida Lloyd"}),         (m:Movie {title: "Mamma Mia!"})                 MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Ol Parker"}),              (m:Movie {title: "Mamma Mia! Here We Go Again"}) MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Michael Bay"}),             (m:Movie {title: "Bad Boys"})                   MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Michael Bay"}),             (m:Movie {title: "Bad Boys II"})                MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Michael Bay"}),             (m:Movie {title: "Bad Boys for Life"})          MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Steven Soderbergh"}),       (m:Movie {title: "Ocean's Eleven"})             MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Steven Soderbergh"}),       (m:Movie {title: "Ocean's Twelve"})             MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Steven Soderbergh"}),       (m:Movie {title: "Ocean's Thirteen"})           MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Gary Ross"}),               (m:Movie {title: "Ocean's 8"})                  MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Alfonso Cuarón"}),         (m:Movie {title: "Gravity"})                    MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Jon Favreau"}),             (m:Movie {title: "Iron Man 2"})                 MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Joss Whedon"}),             (m:Movie {title: "The Avengers"})               MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "The Russo Brothers"}),      (m:Movie {title: "Avengers: Endgame"})          MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "Christopher Nolan"}),      (m:Movie {title: "Oppenheimer"})                MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "James Mangold"}),          (m:Movie {title: "Ford v Ferrari"})             MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "The Coen Brothers"}),      (m:Movie {title: "Burn After Reading"})         MERGE (d)-[:DIRECTED]->(m);
MATCH (d:Person {name: "David Frankel"}),          (m:Movie {title: "The Devil Wears Prada"})      MERGE (d)-[:DIRECTED]->(m);
```

> **Note:** The dataset intentionally includes repeated collaborators across films so you can explore multi-hop queries in Part 6.

---

### 5.8 Create COMPOSED_MUSIC_FOR relationships

```cypher
MATCH (c:Person {name: "Hans Zimmer"}),              (m:Movie {title: "Inception"})                   MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Hans Zimmer"}),              (m:Movie {title: "Batman Begins"})               MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Hans Zimmer"}),              (m:Movie {title: "The Dark Knight"})             MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Hans Zimmer"}),              (m:Movie {title: "The Dark Knight Rises"})       MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Hans Zimmer"}),              (m:Movie {title: "Interstellar"})                MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Ryuichi Sakamoto"}),         (m:Movie {title: "The Revenant"})                MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Howard Shore"}),             (m:Movie {title: "The Wolf of Wall Street"})     MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Mark Ronson and Andrew Wyatt"}),(m:Movie {title: "Barbie"})                    MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "John Ottman"}),              (m:Movie {title: "The Nice Guys"})               MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Claude-Michel Schönberg"}),  (m:Movie {title: "Les Misérables"})             MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Benny Andersson"}),          (m:Movie {title: "Mamma Mia!"})                  MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Benny Andersson"}),          (m:Movie {title: "Mamma Mia! Here We Go Again"}) MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Mark Mancina"}),             (m:Movie {title: "Bad Boys"})                    MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Mark Mancina"}),             (m:Movie {title: "Bad Boys II"})                 MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Mark Mancina"}),             (m:Movie {title: "Bad Boys for Life"})           MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "David Holmes"}),             (m:Movie {title: "Ocean's Eleven"})              MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "David Holmes"}),             (m:Movie {title: "Ocean's Twelve"})              MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "David Holmes"}),             (m:Movie {title: "Ocean's Thirteen"})            MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Daniel Pemberton"}),         (m:Movie {title: "Ocean's 8"})                   MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Steven Price"}),             (m:Movie {title: "Gravity"})                     MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "John Debney"}),              (m:Movie {title: "Iron Man 2"})                  MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Alan Silvestri"}),           (m:Movie {title: "The Avengers"})                MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Alan Silvestri"}),           (m:Movie {title: "Avengers: Endgame"})           MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Ludwig Göransson"}),         (m:Movie {title: "Oppenheimer"})                 MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Marco Beltrami"}),           (m:Movie {title: "Ford v Ferrari"})              MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Carter Burwell"}),           (m:Movie {title: "Burn After Reading"})          MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
MATCH (c:Person {name: "Theodore Shapiro"}),         (m:Movie {title: "The Devil Wears Prada"})       MERGE (c)-[:COMPOSED_MUSIC_FOR]->(m);
```

---

### 5.9 Create PRODUCED relationships

```cypher
MATCH (ph:ProductionHouse {name: "Warner Bros. Pictures"}),   (m:Movie {title: "Inception"})                   MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Legendary Pictures"}),      (m:Movie {title: "Inception"})                   MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Syncopy"}),                 (m:Movie {title: "Inception"})                   MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Regency Enterprises"}),      (m:Movie {title: "The Revenant"})                MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Red Granite Pictures"}),     (m:Movie {title: "The Wolf of Wall Street"})     MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Mattel Films"}),             (m:Movie {title: "Barbie"})                      MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Warner Bros. Pictures"}),    (m:Movie {title: "Barbie"})                      MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Silver Pictures"}),          (m:Movie {title: "The Nice Guys"})               MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Working Title Films"}),      (m:Movie {title: "Les Misérables"})              MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Universal Pictures"}),       (m:Movie {title: "Mamma Mia!"})                  MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Universal Pictures"}),       (m:Movie {title: "Mamma Mia! Here We Go Again"}) MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Columbia Pictures"}),        (m:Movie {title: "Bad Boys"})                    MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Columbia Pictures"}),        (m:Movie {title: "Bad Boys II"})                 MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Columbia Pictures"}),        (m:Movie {title: "Bad Boys for Life"})           MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Warner Bros. Pictures"}),    (m:Movie {title: "Ocean's Eleven"})              MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Village Roadshow Pictures"}),(m:Movie {title: "Ocean's Twelve"})              MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Village Roadshow Pictures"}),(m:Movie {title: "Ocean's Thirteen"})            MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Warner Bros. Pictures"}),    (m:Movie {title: "Ocean's 8"})                   MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Warner Bros. Pictures"}),    (m:Movie {title: "Gravity"})                     MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Marvel Studios"}),           (m:Movie {title: "Iron Man 2"})                  MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Paramount Pictures"}),       (m:Movie {title: "Iron Man 2"})                  MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Marvel Studios"}),           (m:Movie {title: "The Avengers"})                MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Paramount Pictures"}),       (m:Movie {title: "The Avengers"})                MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Marvel Studios"}),           (m:Movie {title: "Avengers: Endgame"})           MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Syncopy"}),                  (m:Movie {title: "Oppenheimer"})                MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Universal Pictures"}),       (m:Movie {title: "Oppenheimer"})                MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "20th Century Fox"}),         (m:Movie {title: "The Devil Wears Prada"})      MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "20th Century Fox"}),         (m:Movie {title: "Ford v Ferrari"})             MERGE (ph)-[:PRODUCED]->(m);
MATCH (ph:ProductionHouse {name: "Focus Features"}),           (m:Movie {title: "Burn After Reading"})         MERGE (ph)-[:PRODUCED]->(m);
```

---

### 5.10 Create WON relationships

```cypher
// Movie awards
MATCH (m:Movie {title: "Inception"}),                  (a:Award {name: "Academy Award Best Visual Effects 2011"}) MERGE (m)-[:WON]->(a);
MATCH (m:Movie {title: "The Revenant"}),              (a:Award {name: "BAFTA Best Film 2016"})                  MERGE (m)-[:WON]->(a);
MATCH (m:Movie {title: "The Wolf of Wall Street"}),    (a:Award {name: "Golden Globe Best Actor 2014"})          MERGE (m)-[:WON]->(a);
MATCH (m:Movie {title: "Barbie"}),                    (a:Award {name: "Grammy Best Compilation Soundtrack 2017"}) MERGE (m)-[:WON]->(a);
MATCH (m:Movie {title: "Batman Begins"}),             (a:Award {name: "Saturn Award Best Science Fiction Film 2004"}) MERGE (m)-[:WON]->(a);
MATCH (m:Movie {title: "The Dark Knight Rises"}),      (a:Award {name: "Saturn Award Best Comic-to-Film Motion Picture 2013"}) MERGE (m)-[:WON]->(a);
MATCH (m:Movie {title: "Gravity"}),                   (a:Award {name: "Academy Award Best Visual Effects 2014"}) MERGE (m)-[:WON]->(a);
MATCH (m:Movie {title: "The Avengers"}),              (a:Award {name: "People's Choice Award Favorite Movie 2013"}) MERGE (m)-[:WON]->(a);
MATCH (m:Movie {title: "Avengers: Endgame"}),         (a:Award {name: "People's Choice Award Favorite Movie 2020"}) MERGE (m)-[:WON]->(a);
MATCH (m:Movie {title: "Mamma Mia!"}),                (a:Award {name: "Golden Globe Best Motion Picture Musical 2009"}) MERGE (m)-[:WON]->(a);
MATCH (m:Movie {title: "Ocean's Eleven"}),            (a:Award {name: "BAFTA Best Editing 2002"})               MERGE (m)-[:WON]->(a);

// Personal awards
MATCH (p:Person {name: "Leonardo DiCaprio"}),         (a:Award {name: "Academy Award Best Actor 2016"})         MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "Brad Pitt"}),                (a:Award {name: "Academy Award Best Supporting Actor 2020"}) MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "George Clooney"}),           (a:Award {name: "Academy Award Best Supporting Actor 2006"}) MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "Matt Damon"}),               (a:Award {name: "Academy Award Best Original Screenplay 1998"}) MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "Sandra Bullock"}),           (a:Award {name: "Academy Award Best Actress 2010"})      MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "Anne Hathaway"}),            (a:Award {name: "Academy Award Best Supporting Actress 2013"}) MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "Meryl Streep"}),             (a:Award {name: "Academy Award Best Actress 2012"})       MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "Michael Caine"}),            (a:Award {name: "Academy Award Best Supporting Actor 2005"}) MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "Christian Bale"}),           (a:Award {name: "Academy Award Best Supporting Actor 2011"}) MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "Will Smith"}),               (a:Award {name: "Academy Award Best Actor 2022"})         MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "Robert Downey Jr."}),        (a:Award {name: "Academy Award Best Supporting Actor 2024"}) MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "Cillian Murphy"}),           (a:Award {name: "Academy Award Best Actor 2024"})         MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "Christopher Nolan"}),        (a:Award {name: "Academy Award Best Director 2024"})      MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "Martin Scorsese"}),          (a:Award {name: "Academy Award Best Director 2007"})      MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "Steven Soderbergh"}),        (a:Award {name: "Academy Award Best Director 2001"})      MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "Hans Zimmer"}),              (a:Award {name: "Academy Award Best Original Score 2022"}) MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "Ludwig Göransson"}),         (a:Award {name: "Academy Award Best Original Score 2019"}) MERGE (p)-[:WON]->(a);
MATCH (p:Person {name: "Meryl Streep"}),             (a:Award {name: "Golden Globe Best Supporting Actress 2006"}) MERGE (p)-[:WON]->(a);
```

---

### 5.11 Verify the data loaded correctly

Run this to see a count of everything in the graph:

```cypher
MATCH (n)
RETURN labels(n)[0] AS NodeType, count(n) AS Count
ORDER BY Count DESC
```

Expected output:

| NodeType | Count |
|---|---|
| Person | 41 |
| Award | 25 |
| Movie | 25 |
| ProductionHouse | 15 |

```cypher
MATCH ()-[r]->()
RETURN type(r) AS RelationshipType, count(r) AS Count
ORDER BY Count DESC
```

Expected output:

| RelationshipType | Count |
|---|---|
| ACTED_IN | 38 |
| DIRECTED | 21 |
| WON | 22 |
| PRODUCED | 18 |
| COMPOSED_MUSIC_FOR | 16 |

If your counts match, you are ready for the practice queries.

---

## Part 1 — Finding Nodes

### 1.1 See a sample of everything in the graph

```cypher
MATCH (n)
RETURN n
LIMIT 25
```

**What's happening:**
- `MATCH (n)` — find any node. No label filter means all types are returned.
- `RETURN n` — return the full node object. Neo4j Browser renders it as a clickable visual graph.
- `LIMIT 25` — always use a limit when browsing. On large graphs, no limit can return millions of rows.

---

### 1.2 Find all movies, sorted by release year

```cypher
MATCH (m:Movie)
RETURN m.title, m.year, m.genre, m.box_office_crore
ORDER BY m.year
```

**What's happening:**
- `(m:Movie)` — the `:Movie` after the colon is a **label filter**. Only Movie nodes are matched.
- `m.title`, `m.year` — dot notation to read specific properties from the node.
- `ORDER BY m.year` — sort ascending by year. Add `DESC` to reverse.

---

### 1.3 Find all people grouped by profession

```cypher
MATCH (p:Person)
RETURN p.profession, collect(p.name) AS People
ORDER BY p.profession
```

**What's happening:**
- `collect(p.name)` — an aggregation function that gathers all names into a list, grouped by profession.
- The result is one row per profession, with a list of names.

---

### 1.4 Find a specific person by exact name

```cypher
MATCH (p:Person {name: "Leonardo DiCaprio"})
RETURN p
```

**What's happening:**
- `{name: "Leonardo DiCaprio"}` inside the node pattern is an **inline property filter**.
- It is exactly equivalent to: `MATCH (p:Person) WHERE p.name = "Leonardo DiCaprio"`.
- The inline style is shorter and preferred when filtering on the identifier property.

> Try changing the name to `"Tom Hardy"`, `"Christopher Nolan"`, or `"Greta Gerwig"`.

---

### 1.5 Count all nodes by type

```cypher
MATCH (n)
RETURN labels(n)[0] AS NodeType, count(n) AS Total
ORDER BY Total DESC
```

**What's happening:**
- `labels(n)` returns a **list** of all labels on the node (nodes can have multiple labels).
- `[0]` gets the first element of that list.
- `count(n)` counts the number of nodes per group. The grouping happens automatically on the non-aggregated field (`NodeType`).

---

## Part 2 — Filtering with WHERE

### 2.1 Movies that crossed 500 crore box office

```cypher
MATCH (m:Movie)
WHERE m.box_office_crore > 500
RETURN m.title, m.year, m.box_office_crore
ORDER BY m.box_office_crore DESC
```

**What's happening:**
- `WHERE` lets you filter on any property using standard comparison operators: `>`, `<`, `>=`, `<=`, `=`, `<>`.
- `DESC` reverses the sort — highest box office first.

---

### 2.2 Actors born in the 1960s

```cypher
MATCH (p:Person)
WHERE p.born >= 1960 AND p.born < 1970
RETURN p.name, p.born, p.profession
ORDER BY p.born
```

**What's happening:**
- `AND` combines conditions — both must be true for the row to be returned.
- You can also use `OR` (either condition true) and `NOT` (invert a condition).

---

### 2.3 Search by partial name (case-insensitive)

```cypher
MATCH (p:Person)
WHERE toLower(p.name) CONTAINS "ro"
RETURN p.name, p.profession
```

**What's happening:**
- `toLower()` converts the value to lowercase before comparison, making the search case-insensitive.
- `CONTAINS` is a substring match — the search term can appear anywhere in the string.
- Other string operators: `STARTS WITH "A"`, `ENDS WITH "r"`.

---

### 2.4 Filter using a list of values

```cypher
MATCH (m:Movie)
WHERE m.genre IN ["Comedy Drama", "Sports Biopic", "Historical Drama"]
RETURN m.title, m.genre, m.year
ORDER BY m.genre, m.year
```

**What's happening:**
- `IN [...]` checks if the property value appears anywhere in the given list.
- This is the Cypher equivalent of SQL's `WHERE genre IN ('Comedy Drama', 'Sports Biopic', ...)`.

---

### 2.5 Filter on NULL — find nodes missing a property

```cypher
MATCH (m:Movie)
WHERE m.box_office_crore IS NULL OR m.box_office_crore = 0
RETURN m.title, m.year
```

**What's happening:**
- `IS NULL` tests for a missing property. In Neo4j, if you never set a property on a node, it simply does not exist (it is not stored as null).
- This is useful for data quality checks.

---

## Part 3 — Relationships

This is the core strength of a graph database.

### Pattern anatomy

```
(p:Person {name: "Leonardo DiCaprio"}) -[:ACTED_IN]-> (m:Movie)
 ↑ start node                    ↑ relationship   ↑ end node
 with label and filter           with type filter
```

The arrow direction `->` matters and must match how the relationship was created.

---

### 3.1 All films a person acted in

```cypher
MATCH (p:Person {name: "Leonardo DiCaprio"})-[:ACTED_IN]->(m:Movie)
RETURN m.title, m.year, m.box_office_crore
ORDER BY m.year
```

> Try with: `"Leonardo DiCaprio"`, `"Ryan Gosling"`, `"Margot Robbie"`.

---

### 3.2 Read properties stored on the relationship itself

```cypher
MATCH (p:Person {name: "Leonardo DiCaprio"})-[r:ACTED_IN]->(m:Movie)
RETURN m.title, r.character AS character_played, r.lead_role AS is_lead_role
ORDER BY m.year
```

**What's happening:**
- `[r:ACTED_IN]` — assigning a variable `r` to the relationship lets you access its properties.
- `r.character` and `r.lead_role` are properties stored directly on the ACTED_IN edge, not on any node.

---

### 3.3 Who directed which films

```cypher
MATCH (d:Person)-[:DIRECTED]->(m:Movie)
RETURN d.name AS Director, collect(m.title) AS Films
ORDER BY size(Films) DESC
```

**What's happening:**
- `collect(m.title)` gathers all movie titles into a list per director.
- `size(Films)` returns the length of the collected list — used here to sort most prolific directors first.

---

### 3.4 Both the director AND cast of a specific film in one query

```cypher
MATCH (director:Person)-[:DIRECTED]->(m:Movie {title: "Inception"})<-[:ACTED_IN]-(actor:Person)
RETURN director.name AS Director, collect(actor.name) AS Cast
```

**What's happening:**
- Two relationship paths meet at the same Movie node `m`.
- `<-[:ACTED_IN]-` — the arrow points **into** `actor`, because ACTED_IN goes FROM actor TO movie. Reading against the arrow finds who pointed to this node.
- One query, two hops, both pieces of information returned together.

> Try with `"Inception"`, `"Barbie"`, `"The Avengers"`.

---

### 3.5 Find the music composer for every film

```cypher
MATCH (c:Person)-[:COMPOSED_MUSIC_FOR]->(m:Movie)
RETURN c.name AS Composer, collect(m.title) AS Films
ORDER BY c.name
```

---

### 3.6 Which studio produced which films

```cypher
MATCH (ph:ProductionHouse)-[:PRODUCED]->(m:Movie)
RETURN ph.name AS Studio, m.title AS Film, m.year AS Year
ORDER BY ph.name, m.year
```

---

## Part 4 — Multi-hop Traversal

Graph databases are built for following paths across multiple nodes. No JOINs — you just extend the pattern.

### 4.1 Films produced by Warner Bros. Pictures starring Leonardo DiCaprio

```cypher
MATCH (ph:ProductionHouse {name: "Warner Bros. Pictures"})
      -[:PRODUCED]->(m:Movie)
     <-[:ACTED_IN]-(p:Person {name: "Leonardo DiCaprio"})
RETURN m.title, m.year, m.box_office_crore
ORDER BY m.year
```

**What's happening:**
- Three nodes, two relationships, one pattern. Neo4j traverses both edges simultaneously.
- Read it: *"A ProductionHouse named Warner Bros. that PRODUCED a Movie that Leonardo DiCaprio ACTED_IN."*
- In SQL this would require a JOIN across three tables.

---

### 4.2 Which composers have worked with Warner Bros. Pictures?

```cypher
MATCH (ph:ProductionHouse {name: "Warner Bros. Pictures"})
      -[:PRODUCED]->(m:Movie)
      <-[:COMPOSED_MUSIC_FOR]-(c:Person)
RETURN c.name AS Composer, collect(m.title) AS Films
```

**What's happening:**
- Path: ProductionHouse → Movie ← Person (composer).
- Both `->` and `<-` are used in the same pattern — the direction follows how each relationship was originally created.

---

### 4.3 Awards won by films that Hans Zimmer scored

```cypher
MATCH (ar:Person {name: "Hans Zimmer"})
      -[:COMPOSED_MUSIC_FOR]->(m:Movie)
      -[:WON]->(a:Award)
RETURN m.title AS Film, a.name AS Award, a.category AS Category
ORDER BY a.year
```

**What's happening:**
- A three-hop chain: Person → Movie → Award.
- This answers a question that would need two JOINs in SQL, using a single readable pattern in Cypher.

---

### 4.4 Actors directed by Christopher Nolan who also worked with Hans Zimmer

```cypher
MATCH (rk:Person {name: "Christopher Nolan"})-[:DIRECTED]->(m1:Movie)<-[:ACTED_IN]-(actor:Person)
MATCH (ar:Person {name: "Hans Zimmer"})-[:COMPOSED_MUSIC_FOR]->(m2:Movie)<-[:ACTED_IN]-(actor)
RETURN DISTINCT actor.name AS Actor,
       collect(DISTINCT m1.title) AS Nolan_Films,
       collect(DISTINCT m2.title) AS Zimmer_Films
```

**What's happening:**
- Two separate `MATCH` clauses. The variable `actor` appears in both — Neo4j only returns actors who satisfy BOTH patterns simultaneously.
- This is a **graph intersection** — finding nodes that exist at the junction of two independent paths.

---

### 4.5 Everyone connected to Inception within 2 hops

```cypher
MATCH (m:Movie {title: "Inception"})-[*1..2]-(connected)
RETURN DISTINCT labels(connected)[0] AS Type,
       coalesce(connected.name, connected.title) AS Entity
ORDER BY Type, Entity
```

**What's happening:**
- `[*1..2]` — variable-length path. Walk between 1 and 2 relationship steps from the start node, in **any direction**.
- This is called **variable-length traversal** and has no direct SQL equivalent.
- `coalesce(a, b)` — returns `a` if it is not null, otherwise `b`. Handles the fact that Person and ProductionHouse nodes have `name` while Movie nodes have `title`.

---

## Part 5 — Aggregation

### 5.1 Total box office per production house

```cypher
MATCH (ph:ProductionHouse)-[:PRODUCED]->(m:Movie)
WHERE m.box_office_crore > 0
RETURN ph.name AS Studio,
       count(m)                            AS Films,
       sum(m.box_office_crore)             AS Total_Crore,
       round(avg(m.box_office_crore))      AS Avg_Per_Film
ORDER BY Total_Crore DESC
```

**What's happening:**
- `count()`, `sum()`, `avg()` work like SQL aggregate functions.
- `round()` removes decimal places.
- Results are automatically grouped by `ph.name` — the one non-aggregated field in the RETURN.

---

### 5.2 Awards won per person

```cypher
MATCH (p:Person)-[:WON]->(a:Award)
RETURN p.name AS Person, count(a) AS Awards_Won
ORDER BY Awards_Won DESC
```

---

### 5.3 Most prolific actors by film count

```cypher
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
RETURN p.name AS Actor, count(m) AS Films_Acted_In
ORDER BY Films_Acted_In DESC
LIMIT 10
```

---

### 5.4 Average box office by genre

```cypher
MATCH (m:Movie)
WHERE m.box_office_crore > 0
RETURN m.genre                         AS Genre,
       count(m)                         AS Film_Count,
       round(avg(m.box_office_crore))   AS Avg_Box_Office_Crore
ORDER BY Avg_Box_Office_Crore DESC
```

---

### 5.5 The WITH clause — filtering after aggregation

`WHERE` can only filter on raw properties. To filter on the result of an aggregation (like "directors with more than 2 films"), use `WITH`:

```cypher
MATCH (d:Person)-[:DIRECTED]->(m:Movie)
WITH d, count(m) AS film_count
WHERE film_count >= 2
RETURN d.name AS Director, film_count
ORDER BY film_count DESC
```

**What's happening:**
- `WITH` is like a pipe — it passes results from the first part of the query into the second.
- `WHERE film_count >= 2` filters on the aggregated value, which was computed in the `WITH`.
- Think of `WITH` as the Cypher equivalent of a SQL subquery or CTE.

---

## Part 6 — Graph-Specific Features

These have no direct SQL equivalent. They are unique to graph databases.

### 6.1 Shortest path between two people

```cypher
MATCH path = shortestPath(
     (a:Person {name: "Leonardo DiCaprio"})-[*]-(b:Person {name: "Hans Zimmer"})
)
RETURN [n IN nodes(path) | coalesce(n.name, n.title)] AS Path,
       length(path) AS Hops
```

**What's happening:**
- `shortestPath(...)` is a built-in Neo4j algorithm. It finds the minimum-hop route between two nodes.
- `[*]` — any relationship type, any direction, any number of hops.
- `nodes(path)` — returns the list of nodes along the path.
- `[n IN nodes(path) | coalesce(n.name, n.title)]` — a **list comprehension**: for each node in the path, extract its name or title.

> Try other pairs: `"Margot Robbie"` → `"Greta Gerwig"`, `"Brad Pitt"` → `"Steven Soderbergh"`.

---

### 6.2 Directors who also acted in their own films

```cypher
MATCH (p:Person)-[:DIRECTED]->(m:Movie)<-[:ACTED_IN]-(p)
RETURN p.name AS Person, collect(m.title) AS Self_Directed_Films
```

**What's happening:**
- The same variable `p` is used at **both ends** of the pattern.
- This means "find a person who DIRECTED a movie AND ACTED_IN that same movie."
- In SQL this would require a self-join. In Cypher it is a natural part of the pattern.

---

### 6.3 Variable-length paths — everyone reachable from Leonardo DiCaprio in 2 hops

```cypher
MATCH (start:Person {name: "Leonardo DiCaprio"})-[*1..2]->(neighbor)
RETURN DISTINCT labels(neighbor)[0] AS Type,
       coalesce(neighbor.name, neighbor.title) AS Entity
ORDER BY Type, Entity
```

**What's happening:**
- `[*1..2]` — follow between 1 and 2 relationship hops.
- This returns every node reachable from Leonardo DiCaprio by following directed relationships outward.
- Compare `[*1..1]` (direct connections only) vs `[*1..3]` (3-hop neighbourhood).

---

### 6.4 Find the most connected nodes (high-degree hubs)

```cypher
MATCH (n)
WITH n, size([(n)--() | 1]) AS degree
WHERE degree > 5
RETURN labels(n)[0] AS Type,
       coalesce(n.name, n.title) AS Entity,
       degree
ORDER BY degree DESC
```

**What's happening:**
- `(n)--()` matches any relationship in either direction.
- `[(n)--() | 1]` is a **pattern comprehension** — it creates a list of `1` for every match. `size()` counts the list.
- This efficiently counts the total degree (in + out connections) of each node.

---

### 6.5 All relationships between two specific nodes

```cypher
MATCH (leo:Person {name: "Leonardo DiCaprio"})-[r]-(m)
RETURN type(r) AS Relationship,
       coalesce(m.name, m.title) AS ConnectedTo,
       labels(m)[0] AS ConnectedType
ORDER BY type(r)
```

**What's happening:**
- `[r]` without a type label matches **any** relationship.
- `type(r)` returns the relationship type as a string.
- This is useful for exploring what connections a node has without already knowing the relationship types.

---

## Part 7 — Writing and Modifying Data

### 7.1 CREATE — always makes a new node

```cypher
CREATE (m:Movie {
    title: "The Martian",
    year: 2015,
    genre: "Adventure Science Fiction Drama",
    box_office_crore: 630.2,
    description: "An astronaut becomes stranded on Mars after his crew assumes him dead, and must rely on his ingenuity to find a way to survive."
})
RETURN m
```

**What's happening:**
- `CREATE` creates a new node unconditionally — even if a node with the same properties exists, it creates another one.
- Use `MERGE` (below) when you want to avoid duplicates.

---

### 7.2 MERGE — the safe upsert (create or match)

```cypher
MERGE (p:Person {name: "Ridley Scott"})
ON CREATE SET p.born = 1937, p.profession = "Director", p.hometown = "South Shields"
ON MATCH  SET p.profession = "Director-Producer"
RETURN p
```

**What's happening:**
- `MERGE` checks first: does a Person named "Ridley Scott" already exist?
  - **If no:** creates a new node and runs `ON CREATE SET`.
  - **If yes:** finds the existing node and runs `ON MATCH SET`.
- This is the safe, idempotent way to write data. The loader in this project uses `MERGE` everywhere so it can be re-run without creating duplicates.

---

### 7.3 Add a relationship between two existing nodes

```cypher
MATCH (p:Person {name: "Ridley Scott"})
MATCH (m:Movie  {title: "The Martian"})
MERGE (p)-[:DIRECTED]->(m)
RETURN p, m
```

**What's happening:**
- Always `MATCH` the nodes first before connecting them.
- `MERGE` on the relationship prevents creating a duplicate edge if the relationship already exists.
- If either MATCH returns nothing (node not found), the MERGE is silently skipped.

---

### 7.4 Update a property on an existing node

```cypher
MATCH (m:Movie {title: "Inception"})
SET m.streaming_platform = "Netflix",
    m.language = "English"
RETURN m.title, m.streaming_platform, m.language
```

**What's happening:**
- `SET` adds or updates one or more properties.
- If `streaming_platform` did not exist before, it is created.
- To update many properties at once: `SET m += {key: value, key2: value2}` (the `+=` merges without overwriting existing properties not in the map).

---

### 7.5 Remove a property

```cypher
MATCH (m:Movie {title: "Inception"})
REMOVE m.streaming_platform
RETURN m
```

**What's happening:**
- `REMOVE` deletes a property from a node. The property key is gone — it is not set to null.
- `REMOVE` also works on labels: `REMOVE n:OldLabel`.

---

### 7.6 Delete a node and all its relationships

```cypher
MATCH (m:Movie {title: "The Martian"})
DETACH DELETE m
```

**What's happening:**
- `DELETE` alone fails if the node has any relationships.
- `DETACH DELETE` removes all relationships connected to the node first, then deletes the node itself.
- **This is permanent.** Neo4j has no ROLLBACK by default. Double-check your MATCH before deleting.

---

## Part 8 — Challenge Queries

Write these yourself before expanding the answers.

**Challenge 1**  
Find all films where the same person both directed and acted. Return their name and the film(s).

**Challenge 2**  
List every actor and the total combined box office of all films they acted in. Order by highest total.

**Challenge 3**  
Find the music composer who has worked with the most distinct production houses. Trace the path: Composer → COMPOSED_MUSIC_FOR → Movie ← PRODUCED — ProductionHouse.

**Challenge 4**  
Find all Academy Award winning films and return the film title, year, and all actors who appeared in it.

**Challenge 5**  
Who is the person with the highest combined degree (most total relationships of any type)?

---

<details>
<summary>Challenge Answers — expand after trying</summary>

**Challenge 1:**
```cypher
MATCH (p:Person)-[:DIRECTED]->(m:Movie)<-[:ACTED_IN]-(p)
RETURN p.name AS Person, collect(m.title) AS Films
```

**Challenge 2:**
```cypher
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WHERE m.box_office_crore > 0
RETURN p.name AS Actor, sum(m.box_office_crore) AS Total_Box_Office_Crore
ORDER BY Total_Box_Office_Crore DESC
```

**Challenge 3:**
```cypher
MATCH (c:Person)-[:COMPOSED_MUSIC_FOR]->(m:Movie)<-[:PRODUCED]-(ph:ProductionHouse)
RETURN c.name AS Composer, count(DISTINCT ph) AS Distinct_Studios
ORDER BY Distinct_Studios DESC
LIMIT 5
```

**Challenge 4:**
```cypher
MATCH (m:Movie)-[:WON]->(a:Award {category: "Academy"})
MATCH (m)<-[:ACTED_IN]-(actor:Person)
RETURN m.title AS Film, m.year AS Year, collect(actor.name) AS Cast
ORDER BY m.year
```

**Challenge 5:**
```cypher
MATCH (n)
WITH n, size([(n)--() | 1]) AS degree
RETURN labels(n)[0] AS Type,
       coalesce(n.name, n.title) AS Entity,
       degree
ORDER BY degree DESC
LIMIT 10
```

</details>

---

## Cypher Cheat Sheet

```
─────────────────────────────────────────────────────────────────
READING DATA
─────────────────────────────────────────────────────────────────
MATCH (n:Label)                          -- find nodes by label
MATCH (n:Label {prop: "value"})          -- inline property filter
MATCH (n:Label) WHERE n.prop > 100       -- WHERE filter
MATCH (a)-[:REL]->(b)                    -- directional relationship
MATCH (a)-[:REL]-(b)                     -- any direction
MATCH (a)-[*1..3]->(b)                   -- variable-length path
MATCH path = shortestPath((a)-[*]-(b))   -- shortest path algorithm
RETURN n, n.prop, labels(n), type(r)
ORDER BY n.prop DESC
LIMIT 10
SKIP 20                                  -- pagination

─────────────────────────────────────────────────────────────────
AGGREGATION
─────────────────────────────────────────────────────────────────
count(n)           -- count rows
sum(n.prop)        -- sum numeric values
avg(n.prop)        -- average
min(n.prop)        -- minimum
max(n.prop)        -- maximum
collect(n.prop)    -- gather into a list
DISTINCT           -- deduplicate

─────────────────────────────────────────────────────────────────
FILTERING AFTER AGGREGATION
─────────────────────────────────────────────────────────────────
MATCH (d)-[:DIRECTED]->(m)
WITH d, count(m) AS films
WHERE films > 2
RETURN d.name, films

─────────────────────────────────────────────────────────────────
WRITING DATA
─────────────────────────────────────────────────────────────────
CREATE (n:Label {prop: value})           -- always creates new
MERGE  (n:Label {prop: value})           -- create or match
  ON CREATE SET n.x = 1
  ON MATCH  SET n.x = 2
SET    n.prop = value                    -- update property
SET    n += {prop: value, prop2: val2}   -- batch update
REMOVE n.prop                            -- delete a property
REMOVE n:Label                           -- remove a label
DELETE n                                 -- delete (fails if has rels)
DETACH DELETE n                          -- delete + all its rels

─────────────────────────────────────────────────────────────────
USEFUL FUNCTIONS
─────────────────────────────────────────────────────────────────
labels(n)                    -- list of node labels
type(r)                      -- relationship type as string
coalesce(a, b, c)            -- first non-null value
toLower(str) / toUpper(str)  -- string case
toString(n) / toInteger(s)   -- type conversion
size(list)                   -- length of a list
nodes(path)                  -- list of nodes in a path
relationships(path)          -- list of rels in a path
length(path)                 -- number of hops in a path
round(n) / ceil(n) / floor(n)-- numeric rounding
```

---

*Open Neo4j Browser at http://localhost:7474 to run all queries.*
*Username: `neo4j` — Password: `hollywood2024!`*

---
**Codeverra** — A learning platform to master coding, data science, DSA, and AI. Learn more at: https://codeverra.com
