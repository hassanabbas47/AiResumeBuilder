import spacy
from typing import List, Set

def get_keyword_suggestions(text: str, nlp) -> List[str]:
    """
    Analyze text and suggest relevant keywords based on industry standards.
    """
    # Common professional keywords
    PROFESSIONAL_KEYWORDS = {
        'leadership', 'management', 'development', 'analysis', 'strategy',
        'communication', 'collaboration', 'implementation', 'optimization',
        'innovation', 'problem-solving', 'coordination', 'planning'
    }
    
    # Technical keywords
    TECH_KEYWORDS = {
        'python', 'java', 'javascript', 'react', 'node.js', 'sql',
        'aws', 'docker', 'kubernetes', 'machine learning', 'ai',
        'data analysis', 'cloud computing', 'devops', 'agile'
    }
    
    doc = nlp(text.lower())
    
    # Extract existing keywords
    existing_keywords = set()
    for token in doc:
        if not token.is_stop and not token.is_punct and len(token.text) > 2:
            existing_keywords.add(token.text)
    
    # Suggest missing relevant keywords
    suggestions = []
    
    # Check professional keywords
    for keyword in PROFESSIONAL_KEYWORDS:
        if keyword not in existing_keywords and keyword not in text.lower():
            suggestions.append(keyword)
            
    # Check technical keywords
    for keyword in TECH_KEYWORDS:
        if keyword not in existing_keywords and keyword not in text.lower():
            suggestions.append(keyword)
    
    return suggestions[:5]  # Return top 5 suggestions

def improve_text(text: str, nlp) -> str:
    """
    Improve the given text by making it more professional and concise.
    """
    doc = nlp(text)
    
    # Simple improvements
    improvements = {
        "i ": "I ",
        "worked on": "developed",
        "helped with": "contributed to",
        "was responsible for": "managed",
        "did": "executed",
        "made": "created",
        "got": "achieved",
    }
    
    improved_text = text
    for original, improved in improvements.items():
        improved_text = improved_text.replace(original, improved)
    
    # Ensure first letter is capitalized
    improved_text = improved_text[0].upper() + improved_text[1:]
    
    # Ensure it ends with a period
    if not improved_text.endswith(('.', '!', '?')):
        improved_text += '.'
    
    return improved_text
