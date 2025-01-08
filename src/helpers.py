
import re

def matching_section(text: str) -> bool:
        pattern = r'\b(?:endpoint|endpoints|objective|objectives)\b'

        return re.search(pattern, text.lower()) is not None

def matching_toc(text: str) -> list:
        matches_list = []
        pattern = r'^((\d+\.?)+)\s+([\w\s,()\'\-]+)\.?\s+(\d+)$'

        matches = re.findall(pattern, text, re.MULTILINE)

        for match in matches:
                result = [match[0], match[2], int(match[3])]
                matches_list.append(result)

        return matches_list