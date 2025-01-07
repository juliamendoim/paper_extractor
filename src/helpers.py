
import re

def matching_section(text: str) -> bool:
        pattern = r'\b(?:endpoint|endpoints|objective|objectives)\b'
        
        return re.search(pattern, text.lower()) is not None
