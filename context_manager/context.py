import os
import json
from typing import List, Dict
from shared.types import ContextLoadResult

# Load FAQ data from file
def load_faq_data():
    """Load FAQ questions and answers from file"""
    try:
        with open("questions_and_answers.txt", "r", encoding='utf-8') as file:
            faq_content = file.read()
        return faq_content
    except FileNotFoundError:
        print("Warning: questions_and_answers.txt not found. Using default FAQ data.")
        return """Q: What is Amazon EC2 Auto Scaling?
Amazon EC2 Auto Scaling is a fully managed service designed to launch or terminate Amazon EC2 instances automatically to help ensure you have the correct number of Amazon EC2 instances available to handle the load for your application."""

# Mock vector database enhanced with FAQ data
class MockVectorDB:
    def __init__(self):
        # Load FAQ data
        self.faq_data = load_faq_data()
        
        # Parse FAQ into structured format
        self.faq_entries = self._parse_faq_data()
        
        # Additional contexts beyond FAQ
        self.additional_contexts = [
            {
                "id": "weather_001",
                "content": "Weather information: Current temperature in Hanoi is 38°C, humidity 65%. It's sunny with light wind.",
                "keywords": ["weather", "temperature", "hanoi", "climate"]
            },
            {
                "id": "traffic_001", 
                "content": "Traffic information: Current traffic in Ho Chi Minh City is heavy during rush hours. Alternative routes recommended.",
                "keywords": ["traffic", "ho chi minh", "routes", "transportation"]
            },
            {
                "id": "restaurant_001",
                "content": "Restaurant recommendations: Top-rated Vietnamese restaurants in Da Nang include specialty pho and seafood dishes.",
                "keywords": ["restaurant", "food", "da nang", "vietnamese", "pho", "seafood"]
            }
        ]
    
    def _parse_faq_data(self):
        """Parse FAQ data into structured entries"""
        entries = []
        lines = self.faq_data.split('\n')
        current_question = ""
        current_answer = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('Q:') or line.startswith('Q.'):
                # Save previous entry if exists
                if current_question and current_answer:
                    entries.append({
                        "question": current_question,
                        "answer": current_answer.strip(),
                        "keywords": self._extract_keywords(current_question + " " + current_answer)
                    })
                
                # Start new entry
                current_question = line
                current_answer = ""
            elif line and current_question:
                current_answer += line + " "
        
        # Add last entry
        if current_question and current_answer:
            entries.append({
                "question": current_question,
                "answer": current_answer.strip(),
                "keywords": self._extract_keywords(current_question + " " + current_answer)
            })
        
        return entries
    
    def _extract_keywords(self, text):
        """Extract keywords from text with multilingual support"""
        # Simple keyword extraction - convert to lowercase and split
        words = text.lower().split()
        # Filter out common words and keep meaningful terms
        stop_words = {
            # English stop words
            'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by', 'what', 'how', 'when', 'where', 'why',
            # Vietnamese stop words
            'là', 'gì', 'như', 'thế', 'nào', 'tại', 'sao', 'có', 'được', 'này', 'đó', 'các', 'một', 'những', 'với', 'trong', 'của', 'cho', 'về', 'từ', 'dịch', 'vụ'
        }
        keywords = [word.strip('.,?!:;') for word in words if len(word) > 2 and word.lower() not in stop_words]
        return list(set(keywords))  # Remove duplicates
    
    def _create_multilingual_mappings(self):
        """Create mappings between Vietnamese and English terms"""
        return {
            # AWS Services
            'auto scaling': ['auto scaling', 'tự động mở rộng', 'tự động scale', 'autoscaling'],
            'ec2': ['ec2', 'elastic compute cloud'],
            'amazon': ['amazon', 'aws'],
            'scaling': ['scaling', 'mở rộng', 'co giãn', 'scale'],
            'instances': ['instances', 'instance', 'máy ảo', 'phiên bản'],
            'group': ['group', 'nhóm', 'asg'],
            'fleet': ['fleet', 'đội tàu', 'nhóm máy'],
            'target tracking': ['target tracking', 'theo dõi mục tiêu'],
            'launch configuration': ['launch configuration', 'cấu hình khởi chạy'],
            'benefits': ['benefits', 'lợi ích', 'ưu điểm'],
            'predictive': ['predictive', 'dự đoán', 'tiên đoán'],
            
            # Question words
            'what is': ['what is', 'là gì', 'gì là'],
            'when': ['when', 'khi nào', 'lúc nào'],
            'how': ['how', 'như thế nào', 'làm sao', 'cách nào'],
            'why': ['why', 'tại sao', 'vì sao'],
            'where': ['where', 'ở đâu', 'tại đâu'],
            
            # Common terms
            'service': ['service', 'dịch vụ'],
            'different': ['different', 'khác nhau', 'khác biệt'],
            'vs': ['vs', 'versus', 'so với', 'và'],
            'use': ['use', 'sử dụng', 'dùng'],
            'should': ['should', 'nên', 'cần']
        }
    
    def _normalize_query(self, query: str) -> str:
        """Normalize Vietnamese query to match English FAQ entries"""
        query_lower = query.lower()
        mappings = self._create_multilingual_mappings()
        
        # Replace Vietnamese terms with English equivalents
        normalized = query_lower
        for english_term, variations in mappings.items():
            for variation in variations:
                if variation in normalized and variation != english_term:
                    normalized = normalized.replace(variation, english_term)
        
        return normalized

    def search_similar(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Enhanced vector similarity search with multilingual FAQ integration
        """
        query_lower = query.lower()
        # Normalize Vietnamese query to English for better matching
        normalized_query = self._normalize_query(query)
        
        results = []
        
        # Search in FAQ entries first with both original and normalized queries
        for faq in self.faq_entries:
            score = 0
            
            # Check with original query
            if any(keyword in query_lower for keyword in faq["keywords"]):
                score += 2  # Higher weight for FAQ matches
            
            # Check with normalized query
            if any(keyword in normalized_query for keyword in faq["keywords"]):
                score += 3  # Even higher weight for normalized matches
            
            # Check for direct text matches in both queries
            query_words = query_lower.split() + normalized_query.split()
            if any(word in faq["answer"].lower() for word in query_words if len(word) > 2):
                score += 1
            
            # Special handling for Vietnamese "gì" questions (what is questions)
            if any(term in query_lower for term in ['là gì', 'gì là']) and 'what is' in faq["question"].lower():
                score += 4  # Very high score for "what is" questions
            
            # Special handling for common AWS terms
            aws_terms = ['ec2', 'auto scaling', 'autoscaling', 'amazon', 'aws']
            if any(term in query_lower for term in aws_terms) and any(term in faq["question"].lower() for term in aws_terms):
                score += 2
            
            if score > 0:
                results.append({
                    "content": f"{faq['question']}\n{faq['answer']}",
                    "score": score,
                    "type": "faq"
                })
        
        # Search in additional contexts
        for context in self.additional_contexts:
            score = 0
            # Check with both original and normalized query
            for keyword in context["keywords"]:
                if keyword in query_lower or keyword in normalized_query:
                    score += 1
            
            if score > 0:
                results.append({
                    "content": context["content"],
                    "score": score,
                    "type": "general"
                })
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

# Global vector DB instance
vector_db = MockVectorDB()

def init_context():
    """
    Initialize context system with FAQ data
    """
    print("Context system initialized with FAQ database")
    print(f"Loaded {len(vector_db.faq_entries)} FAQ entries")
    # In real implementation, this would also:
    # - Call OpenAI API to get embeddings for FAQ entries
    # - Store embeddings in vector database
    pass

def load_context(question: str) -> ContextLoadResult:
    """
    Load relevant context based on user question with FAQ integration
    
    Args:
        question: User's question string
        
    Returns:
        ContextLoadResult with status and context including FAQ data
    """
    try:
        # Search for similar contexts including FAQ
        similar_contexts = vector_db.search_similar(question, top_k=3)
        
        if similar_contexts:
            # Combine contexts with FAQ data as primary source
            context_text = f"FAQ Database:\n{vector_db.faq_data}\n\nRelevant Context:\n"
            
            for i, ctx in enumerate(similar_contexts, 1):
                context_text += f"Context {i} ({ctx['type']}): {ctx['content']}\n\n"
            
            return ContextLoadResult(status="FOUND", context=context_text.strip())
        else:
            # Even if no specific context found, include FAQ data
            return ContextLoadResult(status="FOUND", context=f"FAQ Database:\n{vector_db.faq_data}")
            
    except Exception as e:
        print(f"Error loading context: {e}")
        return ContextLoadResult(status="NOT_FOUND", context="")
