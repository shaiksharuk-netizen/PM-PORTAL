"""
Embedding Service
Provides text embeddings using Google's hosted API (Free & Low RAM) or fallback providers.
"""
import os
import gc
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for generating text embeddings"""
    
    def __init__(self):
        # Default to 'google' to stop RAM crashes on Render
        self.provider = os.getenv("EMBEDDING_PROVIDER", "google").lower()
        # Default Google model for free, high-quality embeddings
        self.model_name = os.getenv("EMBEDDING_MODEL_NAME", "models/text-embedding-004")
        self.api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        self._model = None
        self._embedding_dimension = None
        
    def _load_local_model(self):
        """Lazy load local sentence-transformers (WARNING: High RAM usage)"""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading local model: {self.model_name}")
                cache_dir = os.path.join(os.getcwd(), "model_cache")               
                os.makedirs(cache_dir, exist_ok=True)
                self._model = SentenceTransformer(self.model_name, cache_folder=cache_dir)
                self._embedding_dimension = self._model.get_sentence_embedding_dimension()
            except Exception as e:
                logger.error(f"Local model load failed: {str(e)}")
                raise

    def _embed_with_google(self, texts: List[str]) -> List[List[float]]:
        """Generates embeddings using Google's API (Uses 0MB Server RAM)"""
        try:
            import google.generativeai as genai
            if not self.api_key:
                raise ValueError("GOOGLE_API_KEY not set")
            
            genai.configure(api_key=self.api_key)
            
            # Optimized for retrieval tasks
            result = genai.embed_content(
                model=self.model_name,
                content=texts,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Google embedding failed: {str(e)}")
            raise

    def _embed_with_openai(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using OpenAI API (Paid)"""
        try:
            import openai
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.embeddings.create(
                model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"OpenAI embedding failed: {str(e)}")
            raise

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Main method to generate embeddings for a list of strings"""
        if not texts:
            return []
        
        try:
            if self.provider == "google":
                return self._embed_with_google(texts)
            elif self.provider == "local":
                self._load_local_model()
                embeddings = self._model.encode(texts, convert_to_numpy=True)
                return embeddings.tolist()
            elif self.provider == "openai":
                return self._embed_with_openai(texts)
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
        finally:
            # Manually trigger garbage collection to save RAM
            gc.collect()

    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a single query string"""
        if self.provider == "google":
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            result = genai.embed_content(
                model=self.model_name,
                content=query,
                task_type="retrieval_query" # Optimized for queries
            )
            return result['embedding']
        
        embeddings = self.embed([query])
        return embeddings[0] if embeddings else []
    
    def get_embedding_dimension(self) -> int:
        """Get the vector dimension based on the chosen provider"""
        if self.provider == "google":
            return 768  # Dimension for text-embedding-004
        elif self.provider == "openai":
            return 1536
        elif self.provider == "local":
            self._load_local_model()
            return self._embedding_dimension
        return 768

# Create service instance
embedding_service = EmbeddingService()
