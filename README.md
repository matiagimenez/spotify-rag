# 🎵 Spotify Semantic Vibe Searcher (RAG)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Ollama](https://img.shields.io/badge/AI-Ollama-orange)
![LangChain](https://img.shields.io/badge/RAG-LangChain-green)
![Spotify API](https://img.shields.io/badge/Data-Spotify-1DB954)
![Genius](https://img.shields.io/badge/Lyrics-Genius-FFFF00)

> **Stop searching by Genre. Start searching by _Vibe_ and _Meaning_.** > **Now 100% Local & Private.**

This project is a **Retrieval-Augmented Generation (RAG)** application that allows you to search your personal Spotify "Liked Songs" library using natural language abstract descriptions.

It goes beyond simple audio features by performing a **Multi-Modal Analysis**: it bridges raw **Audio Metrics** (Spotify) and **Lyrical Content** (Genius) to understand not just how a song _sounds_, but what it _says_.

## 🧠 How it Works

Standard Spotify search relies on metadata. This project uses a **Local RAG pipeline** to create a "Semantic Fingerprint" for every song:

1.  **Dual Extraction (ETL):**
    - **Audio:** Fetches specific _Audio Features_ (Valence, Energy, Danceability, BPM) via Spotify API.
    - **Lyrics:** Scrapes/Fetches song lyrics via the Genius API.
2.  **Semantic Synthesis (Local LLM):**
    - A local model (Ollama) acts as a music critic. It analyzes the **contrast** or **alignment** between the music and the words.
    - _Input:_ `Valence: 0.8 (Happy)` + `Lyrics: "I'm so lonely"`
    - _Output:_ _"An upbeat, high-energy track that disguises deep lyrical sorrow and isolation, creating an ironic, bittersweet atmosphere."_
3.  **Embedding:** Vectorizes these complex synthesized descriptions into **ChromaDB**.
4.  **Retrieval & Generation:**
    - **User Query:** _"Songs that sound happy but are actually depressing."_
    - **Vector Search:** Finds songs where the "Semantic Fingerprint" matches this specific contrast.
    - **The DJ (Ollama):** Explains the choice: _"I picked 'Hey Ya!' because despite its high danceability, the lyrics explicitly discuss the inability to maintain a relationship."_

## 🛠️ Tech Stack

- **Language:** Python 3.12+
- **Data Sources:**
  - [Spotify Web API](https://developer.spotify.com/) (Audio Features)
  - [Genius API](https://docs.genius.com/) (Lyrics)
- **Inference Engine:** [Ollama](https://ollama.com/) (Llama 3 / Mistral)
- **Vector Database:** [ChromaDB](https://www.trychroma.com/) (Local persistence)
- **Orchestration:** LangChain
- **Data Validation:** Pydantic

## 🚀 Prerequisites

1.  **Spotify App:** Get your `CLIENT_ID` and `CLIENT_SECRET` from the [Spotify Dashboard](https://developer.spotify.com/dashboard).
2.  **Genius API:** Get a Client Access Token from the [Genius API Clients Page](https://genius.com/api-clients).
3.  **Ollama:**
    - Download and install [Ollama](https://ollama.com/download).
    - Pull your model: `ollama pull llama3`

## ⚙️ Configuration

Create a `.env` file in the root directory:

```ini
# Spotify Credentials
SPOTIPY_CLIENT_ID='your_spotify_id'
SPOTIPY_CLIENT_SECRET='your_spotify_secret'
SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'

# Genius Credentials (Lyrics)
GENIUS_ACCESS_TOKEN='your_genius_token'

# Ollama Settings
OLLAMA_BASE_URL='http://localhost:11434'
OLLAMA_MODEL='llama3'
```

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
