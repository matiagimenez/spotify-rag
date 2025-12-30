from unittest.mock import MagicMock

import pytest

from spotify_rag.infrastructure.llm import LLMClient


@pytest.fixture
def llm_client() -> LLMClient:
    """Fixture for LLM client instance."""
    return LLMClient()


@pytest.fixture
def llm_client_with_api_error() -> LLMClient:
    """Fixture for LLM client with mocked API error."""
    llm_client = LLMClient()

    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API Error")
    llm_client._client = mock_client

    return llm_client


@pytest.fixture
def simple_prompt() -> str:
    """Fixture for a simple test prompt."""
    return "What is the capital of France? Answer in one word."


@pytest.fixture
def analysis_prompt() -> str:
    """Fixture for a music analysis prompt."""
    return """Analyze this song in one sentence:
    - Title: Bohemian Rhapsody
    - Artist: Queen
    - Genre: Rock
    - Theme: Complex narrative about a young man's existential crisis

    Provide a brief vibe description."""
