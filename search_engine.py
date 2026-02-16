# SEARCH ENGINE - Custom semantic search for FAQs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict

class SemanticSearch:
    """Semantic search engine using TF-IDF and cosine similarity"""
    
    def __init__(self, questions: List[str]):
        """Initialize search engine with questions"""
        self.questions = questions
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', ngram_range=(1, 2))
        self.question_vectors = self.vectorizer.fit_transform(questions)
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for similar questions and return results"""
        if len(self.questions) == 0:
            return []
        
        # Transform query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarity scores
        similarities = cosine_similarity(query_vector, self.question_vectors)[0]
        
        # Get top K matches
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                'index': idx,
                'question': self.questions[idx],
                'similarity': float(similarities[idx]),
                'confidence_percent': float(similarities[idx] * 100)
            })
        
        return results
    
    def retrain(self, questions: List[str]) -> None:
        """Retrain search engine with new questions"""
        self.questions = questions
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english', ngram_range=(1, 2))
        self.question_vectors = self.vectorizer.fit_transform(questions)
    
    def get_confidence_color(self, confidence: float) -> tuple:
        """Get color and emoji based on confidence level"""
        if confidence >= 0.7:
            return "#28a745", "✅"  # Green - high confidence
        elif confidence >= 0.5:
            return "#ffc107", "⚠️"  # Yellow - medium confidence
        else:
            return "#dc3545", "❌"  # Red - low confidence
    
    def get_confidence_label(self, confidence: float) -> str:
        """Get label based on confidence level"""
        if confidence >= 0.7:
            return "High Confidence Match"
        elif confidence >= 0.5:
            return "Moderate Confidence Match"
        else:
            return "Low Confidence Match"
