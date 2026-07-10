# 🎬 Hollywood GraphRAG

A complete GraphRAG (Graph Retrieval-Augmented Generation) system built on a **Hollywood knowledge graph**. Ask questions about English cinema in plain English — the system finds the answer by traversing a Neo4j graph of movies, actors, directors, composers, and awards, then generating a natural language response via Groq (Llama 3.3).

---

# 🚀 Live Demo

### Streamlit Frontend

https://hollywood-neo4j-graphrag.streamlit.app/

### FastAPI Backend

https://neo4j-hollywood-graphrag.onrender.com

### API Documentation (Swagger UI)

https://neo4j-hollywood-graphrag.onrender.com/docs

> [!IMPORTANT]
> **Deployment Notice:** This project uses free hosting services (Render + Streamlit Community Cloud). The backend may take **1–2 minutes** to start after being idle. Please be patient during the first request.

---

## Deployment Architecture

```
                    User
                      │
                      ▼
      Streamlit Community Cloud
https://hollywood-neo4j-graphrag.streamlit.app
                      │
               HTTP Requests
                      │
                      ▼
           FastAPI Backend (Render)
https://neo4j-hollywood-graphrag.onrender.com
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
    Neo4j Aura      Groq LLM   Google Gemini
     Graph DB       (Llama 3.3)  Embeddings
```

---

## Try It Online

Open the Streamlit application and ask questions such as:

- Which films did Leonardo DiCaprio and Hans Zimmer work on together?
- Which directors have won an Academy Award for Best Director?
- What are all the films produced by Marvel Studios starring Robert Downey Jr.?
- Which actors have worked under both Christopher Nolan and Martin Scorsese?

No local installation is required.

---

## What This Project Demonstrates

| Concept                          | How it appears in this project                                               |
| -------------------------------- | ---------------------------------------------------------------------------- |
| Graph database fundamentals      | Neo4j with a Hollywood ontology                                              |
| Cypher query language            | Loader, traversal, and stat queries                                          |
| Vector embeddings on graph nodes | Each node carries a Google Gemini (`gemini-embedding-001`) embedding         |
| GraphRAG pipeline                | Vector search (Python cosine similarity) → graph traversal → Groq LLM answer |
| FastAPI backend                  | REST endpoints for all pipeline operations                                   |
| Streamlit frontend               | 4-page chat + explorer interface                                             |
| Docker Compose                   | Multi-container setup for services                                           |

---

## Knowledge Graph Ontology

```
NODES
──────────────────────────────────────────────────────────
Person          {name, born, profession, hometown}
Movie           {title, year, genre, language, box_office_million, description}
ProductionHouse {name, founded, founder, hq}
Award           {name, category, year}

RELATIONSHIPS
──────────────────────────────────────────────────────────
(Person)          -[:ACTED_IN {character, lead_role}]-> (Movie)
(Person)          -[:DIRECTED]->                       (Movie)
(Person)          -[:COMPOSED_MUSIC_FOR]->             (Movie)
(Person)          -[:WON]->                            (Award)
(Movie)           -[:WON]->                            (Award)
(ProductionHouse) -[:PRODUCED]->                       (Movie)
```

---

## Setup

### Prerequisites

| Tool           | Version           | Notes                                            |
| -------------- | ----------------- | ------------------------------------------------ |
| Neo4j          | 5.x+ / Aura Cloud | Running instance (local or remote)               |
| Python         | 3.10+             | For running scripts and servers                  |
| Gemini API key | —                 | Required for `gemini-embedding-001` embeddings   |
| Groq API key   | —                 | Required for `llama-3.3-70b-versatile` reasoning |

### 1. Clone and configure

```bash
git clone <repo-url>
cd hollywood-graphrag

# Edit or create .env file at the root
```

Your `.env` file:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=AIzaSy...
API_URL=http://localhost:8000
```

### 2. Install Python dependencies

```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Load the knowledge graph

Execute the loader script to set up constraints and import the Hollywood dataset:

```bash
python src/loader.py
```

Expected output:

```
[1/2] Loading nodes...
  Setting up ontology constraints...
  ✓ Constraints active
  ✓ 92 Person nodes
  ✓ 28 Movie nodes
  ...
[2/2] Loading relationships...
  ✓ 89 ACTED_IN relationships
  ✓ 29 DIRECTED relationships
  ...
```

### 4. Add vector embeddings

This calls the Google Gemini embeddings API for each node and stores the vectors as JSON properties in Neo4j.

```bash
python src/embeddings.py
```

### Running Locally (Optional)

The project is already deployed online.

If you want to run it locally:

#### 5. Start the FastAPI backend

```bash
python src/api.py
```

Open:

http://localhost:8000/docs

#### 6. Start Streamlit

```bash
streamlit run src/app.py
```

Open:

http://localhost:8501

## Usage

### Streamlit Chat Interface

The **💬 Chat** page lets you ask natural language questions. Try:

- _"Which films did Leonardo DiCaprio and Hans Zimmer work on together?"_
- _"Which directors have won an Academy Award for Best Director?"_
- _"What are all the films produced by Marvel Studios starring Robert Downey Jr.?"_
- _"Which actors have worked under both Christopher Nolan and Martin Scorsese?"_

The **🔍 Explore** page lets you look up any entity by name and see its full graph neighbourhood.

### FastAPI Endpoints

```bash
# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Which movies did Christopher Nolan direct?", "top_k": 3, "hops": 2}'

# Vector search
curl "http://localhost:8000/search?q=superhero&label=Movie"

# Get an entity's neighbourhood
curl "http://localhost:8000/graph/Inception?label=Movie&hops=2"

# Filmography of a person
curl "http://localhost:8000/person/Christopher%20Nolan/filmography"

# Graph statistics
curl "http://localhost:8000/stats"
```

---

## Project Structure

```
hollywood-graphrag/
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── src/
    ├── db.py                   ← Thread-safe Neo4j driver connection manager
    ├── loader.py               ← Load ontology constraints + data into Neo4j
    ├── embeddings.py           ← Compute + store node embeddings (Gemini API)
    ├── graphrag.py             ← Context synthesis and Groq LLM pipelines
    ├── api.py                  ← FastAPI backend
    ├── app.py                  ← Streamlit frontend
    └── data/
        └── hollywood_data.py   ← All graph data (nodes + relationships)
```

---

## How the GraphRAG Pipeline Works

```
User question (text)
       │
       ▼
┌──────────────────────────────┐
│  1. Vector Search            │  Embed question → find top-k similar nodes
│     (embeddings.py)          │  e.g. "Who directed Inception?" → [Christopher Nolan, Inception]
└──────────────────┬───────────┘
                   │  top-k node identifiers
                   ▼
┌──────────────────────────────┐
│  2. Graph Traversal          │  Walk N hops from each identified node
│     (graphrag.py)            │  Collect all connected facts as triples
└──────────────────┬───────────┘
                   │  subgraph as structured text
                   ▼
┌──────────────────────────────┐
│  3. LLM Answer Generation    │  Groq Llama 3.3 reasons over graph context
│     (Groq Llama 3.3)         │  Returns grounded, verifiable answer
└──────────────────────────────┘
```

---

## Extending the Project

### Adding more movies

Add entries to `MOVIES`, `ACTED_IN`, `DIRECTED` etc. in `src/data/hollywood_data.py`, then re-run `loader.py` and `embeddings.py`.

### Adding a new relationship type

1. Add rows to the relevant list in `hollywood_data.py`
2. Add a loading function in `loader.py`
3. Call it from `load_all()`

### Switching to a different LLM

Replace the `groq` or `google-genai` calls in `graphrag.py` and `embeddings.py` with another API SDK.

---

## Interesting Graph Queries to Try in Neo4j Browser

```cypher
-- All Leonardo DiCaprio films with box office > 500 million
MATCH (p:Person {name: 'Leonardo DiCaprio'})-[:ACTED_IN]->(m:Movie)
WHERE m.box_office_million > 500
RETURN m.title, m.year, m.box_office_million ORDER BY m.box_office_million DESC

-- Directors who also acted in their own films
MATCH (p:Person)-[:DIRECTED]->(m:Movie)<-[:ACTED_IN]-(p)
RETURN p.name, m.title

-- Movies where Hans Zimmer composed and the film won an Academy Award
MATCH (hz:Person {name:'Hans Zimmer'})-[:COMPOSED_MUSIC_FOR]->(m:Movie)-[:WON]->(a:Award)
WHERE a.category = 'Academy'
RETURN m.title, a.name

-- Shortest path between Cillian Murphy and Brad Pitt
MATCH path = shortestPath(
    (a:Person {name: 'Cillian Murphy'})-[*]-(b:Person {name: 'Brad Pitt'})
)
RETURN [n IN nodes(path) | coalesce(n.name, n.title)] AS path, length(path) AS hops

-- All films produced by Universal Pictures
MATCH (ph:ProductionHouse {name: 'Universal Pictures'})-[:PRODUCED]->(m:Movie)
RETURN m.title, m.year, m.box_office_million ORDER BY m.box_office_million DESC
```
