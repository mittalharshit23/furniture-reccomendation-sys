"""
Embedding generation service for text and image features.

This module provides services for generating semantic embeddings from text
using transformer models and image features using pre-trained CNNs.
"""

import logging
from typing import List, Optional

import numpy as np
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from sentence_transformers import SentenceTransformer

from config.settings import TEXT_EMBEDDING_MODEL

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for generating semantic embeddings from text and images.
    
    Uses SentenceTransformers for text encoding and ResNet50 for image
    feature extraction. Provides methods for single and batch encoding.
    """

    # Embedding dimension for the text model
    TEXT_EMBEDDING_DIM = 384  # MiniLM-L6-v2 dimension

    def __init__(self):
        """Initialize text and image embedding models."""
        logger.info(" Initializing embedding models...")

        # Initialize text embedding model
        self.text_encoder = SentenceTransformer(TEXT_EMBEDDING_MODEL)
        logger.info(f"    Text model loaded: {TEXT_EMBEDDING_MODEL}")

        # Initialize image feature extractor (ResNet50)
        self.image_model = models.resnet50(pretrained=True)
        self.image_model.eval()  # Set to evaluation mode
        
        # Define image preprocessing pipeline
        self.image_transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
        ])
        logger.info("    Image model loaded: ResNet50")

        logger.info(" Embedding models ready")

    def encode_text(self, text: str) -> np.ndarray:
        """
        Generate semantic embedding for a text string.
        
        Args:
            text: Input text to encode
        
        Returns:
            NumPy array of embedding values
        """
        if not text or not text.strip():
            # Return zero vector for empty text
            return np.zeros(self.TEXT_EMBEDDING_DIM)
        
        return self.text_encoder.encode(text)

    def encode_text_batch(self, texts: List[str]) -> np.ndarray:
        """
        Generate semantic embeddings for multiple texts efficiently.
        
        Args:
            texts: List of text strings to encode
        
        Returns:
            NumPy array of shape (n_texts, embedding_dim)
        """
        return self.text_encoder.encode(texts, show_progress_bar=True)

    def encode_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Generate feature embedding for an image using ResNet50.
        
        Args:
            image_path: Path to the image file
        
        Returns:
            NumPy array of image features, or None if processing fails
        """
        try:
            # Load and preprocess image
            img = Image.open(image_path).convert("RGB")
            img_tensor = self.image_transform(img).unsqueeze(0)
            
            # Extract features without gradient computation
            with torch.no_grad():
                features = self.image_model(img_tensor)
            
            return features.squeeze().numpy()
        
        except Exception as e:
            logger.warning(f"  Error processing image {image_path}: {e}")
            return None

    def combine_embeddings(
        self,
        text_embedding: np.ndarray,
        image_embedding: Optional[np.ndarray] = None,
        text_weight: float = 0.7,
    ) -> np.ndarray:
        """
        Combine text and image embeddings using weighted average.
        
        Args:
            text_embedding: Text embedding vector
            image_embedding: Optional image embedding vector
            text_weight: Weight for text embedding (0-1)
        
        Returns:
            Combined embedding vector
        """
        if image_embedding is None:
            return text_embedding

        # Ensure embeddings have same dimension
        min_dim = min(len(text_embedding), len(image_embedding))
        text_resized = text_embedding[:min_dim]
        image_resized = image_embedding[:min_dim]

        # Compute weighted combination
        image_weight = 1.0 - text_weight
        combined = text_weight * text_resized + image_weight * image_resized

        return combined

