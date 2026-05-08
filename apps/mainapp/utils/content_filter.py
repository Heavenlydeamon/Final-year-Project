"""
Content Filter Module
====================
Processes study material text to extract key facts for AI quiz generation.

Features:
- Strip non-factual metadata (Learning Outcomes, Summary)
- Extract key terminology from tables
- Highlight numerical facts for precise question generation
- Prepare context for FLAN-T5 model
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional


@dataclass
class ProcessedContent:
    """Processed content with extracted facts and terminology"""
    clean_text: str
    numerical_facts: List[Dict[str, str]]
    terminology: List[Dict[str, str]]
    landmarks: List[str]
    entities: List[str]
    context_summary: str


class ContentFilter:
    """
    Filter and process educational content for AI quiz generation.
    
    This class handles:
    1. Removing non-factual sections (Learning Outcomes, Summary)
    2. Extracting terminology from tables
    3. Identifying numerical facts
    4. Extracting landmarks and entities
    """
    
    # Sections to remove (non-factual metadata)
    SECTIONS_TO_REMOVE = [
        'learning outcomes',
        'summary',
        'conclusion',
        'key takeaways',
        'assessment',
        'objectives',
    ]
    
    # Numerical patterns to extract
    NUMERICAL_PATTERNS = [
        # Years/Age (e.g., 150 million years, 150M years)
        (r'(\d+(?:\.\d+)?\s*(?:million|billion|M|B)?\s*years?\s*(?:old|ago)?)', 'age'),
        # Length/Distance (e.g., 1,600 km, 1600km)
        (r'(\d+(?:,\d{3})*(?:\.\d+)?\s*(?:km|kilometer|m|mile)s?)', 'distance'),
        # Height/Elevation (e.g., 2,695 m, 2695m)
        (r'(\d+(?:,\d{3})*(?:\.\d+)?\s*(?:m|meter|feet|ft)\s*(?:high|above|peak)?)', 'height'),
        # Area (e.g., 160,000 km²)
        (r'(\d+(?:,\d{3})*(?:\.\d+)?\s*(?:km²|sq\s*km|hectare|acre)s?)', 'area'),
        # Percentage
        (r'(\d+(?:\.\d+)?\s*%)', 'percentage'),
        # Population
        (r'(\d+(?:,\d{3})*(?:\.\d+)?\s*(?:million|billion|thousand)?\s*(?:people|persons|people))', 'population'),
        # Temperature
        (r'(\d+(?:\.\d+)?\s*°?[CF])', 'temperature'),
        # Count/Numbers
        (r'(over\s+)?(\d+(?:,\d{3})*(?:\.\d+)?\s*(?:species|plants|animals|species))', 'count'),
    ]
    
    # Landmark patterns (national parks, reserves, etc.)
    LANDMARK_PATTERNS = [
        r'(?:National\s+Park| wildlife\s+sanctuary|Reserve|Forest)',
    ]
    
    # Western Ghats specific entities
    WESTERN_GHATS_ENTITIES = [
        'Eravikulam National Park',
        'Silent Valley',
        ' Periyar',
        'Wayanad',
        'Kodagu',
        'Munnar',
        'Anamudi',
        'Meesapulimala',
        'Nilgiri Tahr',
        'Lion-tailed Macaque',
        'Malabar Giant Squirrel',
        'Neelakurinji',
        'Gondwana',
        'Shola',
        'Rain Shadow',
        'Gadgil Report',
        'Kasturirangan Report',
        'Project Tiger',
    ]
    
    # States for distractor generation
    INDIAN_STATES = [
        'Gujarat', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'Kerala',
        'Goa', 'Andhra Pradesh', 'Telangana', 'Madhya Pradesh', 'Odisha'
    ]
    
    def __init__(self, content: str):
        """
        Initialize with study material content.
        
        Args:
            content: Raw study material text
        """
        self.raw_content = content
        self.processed: Optional[ProcessedContent] = None
    
    def process(self) -> ProcessedContent:
        """
        Process the content and extract all relevant information.
        
        Returns:
            ProcessedContent object with extracted facts
        """
        # Step 1: Remove non-factual sections
        clean_text = self._strip_non_factual_sections(self.raw_content)
        
        # Step 2: Extract numerical facts
        numerical_facts = self._extract_numerical_facts(clean_text)
        
        # Step 3: Extract terminology from tables
        terminology = self._extract_terminology(self.raw_content)
        
        # Step 4: Extract landmarks
        landmarks = self._extract_landmarks(clean_text)
        
        # Step 5: Extract entities
        entities = self._extract_entities(clean_text)
        
        # Step 6: Generate context summary
        context_summary = self._generate_context_summary(
            clean_text, numerical_facts, terminology
        )
        
        self.processed = ProcessedContent(
            clean_text=clean_text,
            numerical_facts=numerical_facts,
            terminology=terminology,
            landmarks=landmarks,
            entities=entities,
            context_summary=context_summary
        )
        
        return self.processed
    
    def _strip_non_factual_sections(self, text: str) -> str:
        """
        Remove non-factual metadata sections.
        
        Removes:
        - Learning Outcomes
        - Summary
        - Conclusion
        - Assessment sections
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Split by major sections
        sections = re.split(r'\n#{1,3}\s+', text)
        filtered_sections = []
        
        for section in sections:
            section_lower = section.lower().strip()
            
            # Check if section should be removed
            should_remove = False
            for remove_term in self.SECTIONS_TO_REMOVE:
                if section_lower.startswith(remove_term):
                    should_remove = True
                    break
            
            if not should_remove:
                filtered_sections.append(section)
        
        # Rejoin sections
        clean_text = '\n\n'.join(filtered_sections)
        
        # Also remove bullet points that are learning outcomes
        lines = clean_text.split('\n')
        filtered_lines = []
        skip_section = False
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Skip if this looks like a learning outcome bullet
            if any(term in line_lower for term in ['upon completing', 'will be able to', 'learners will']):
                skip_section = True
                continue
            
            # Stop skipping after a blank line (end of learning outcomes)
            if skip_section and not line.strip():
                skip_section = False
            
            if not skip_section:
                filtered_lines.append(line)
        
        return '\n'.join(filtered_lines).strip()
    
    def _extract_numerical_facts(self, text: str) -> List[Dict[str, str]]:
        """
        Extract numerical facts from text.
        
        Finds patterns like:
        - 150 million years (age)
        - 1,600 km (distance)
        - 2,695 m (height)
        - 500 million people (population)
        
        Args:
            text: Text to search
            
        Returns:
            List of dicts with 'value', 'type', 'context'
        """
        facts = []
        
        for pattern, fact_type in self.NUMERICAL_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                value = match.group(0)
                
                # Get surrounding context (50 chars before and after)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                
                facts.append({
                    'value': value,
                    'type': fact_type,
                    'context': context
                })
        
        return facts
    
    def _extract_terminology(self, text: str) -> List[Dict[str, str]]:
        """
        Extract key terminology from tables and definitions.
        
        Looks for:
        - Markdown tables (| Term | Definition |)
        - Bold terms with definitions
        - Key concept lists
        
        Args:
            text: Text to search
            
        Returns:
            List of dicts with 'term' and 'definition'
        """
        terminology = []
        
        # Extract from markdown tables
        table_pattern = r'\|\s*\*\*?([^\|]+?)\*?\*\*?\s*\|\s*([^\|]+?)\s*\|'
        matches = re.finditer(table_pattern, text)
        
        for match in matches:
            term = match.group(1).strip()
            definition = match.group(2).strip()
            
            if term and definition and len(term) > 2:
                terminology.append({
                    'term': term,
                    'definition': definition,
                    'source': 'table'
                })
        
        # Also look for bold terms with following text
        bold_pattern = r'\*\*([^*]+)\*\*[:\s]+([^.\n]+)'
        matches = re.finditer(bold_pattern, text)
        
        for match in matches:
            term = match.group(1).strip()
            definition = match.group(2).strip()[:150]  # Limit length
            
            # Avoid duplicates
            if term and definition and not any(t['term'] == term for t in terminology):
                terminology.append({
                    'term': term,
                    'definition': definition,
                    'source': 'bold'
                })
        
        return terminology
    
    def _extract_landmarks(self, text: str) -> List[str]:
        """
        Extract landmarks (national parks, reserves, etc.)
        
        Args:
            text: Text to search
            
        Returns:
            List of landmark names
        """
        landmarks = []
        
        for pattern in self.LANDMARK_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in range(len(list(re.finditer(pattern, text)))):
                # Get more context to get full name
                start = match.start() if hasattr(match, 'start') else 0
                end = match.end() if hasattr(match, 'end') else 0
        
        # Use simpler approach - find capitalized phrases with landmark keywords
        landmark_keywords = [
            'National Park', 'Wildlife Sanctuary', 'Reserve Forest',
            'Tiger Reserve', 'Biosphere Reserve'
        ]
        
        for keyword in landmark_keywords:
            # Find phrases containing keyword
            pattern = rf'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+{keyword})'
            matches = re.finditer(pattern, text)
            
            for match in matches:
                landmark = match.group(1).strip()
                if landmark and landmark not in landmarks:
                    landmarks.append(landmark)
        
        return landmarks
    
    def _extract_entities(self, text: str) -> List[str]:
        """
        Extract relevant entities for question generation.
        
        Includes:
        - Western Ghats specific entities
        - State names
        - Important locations
        
        Args:
            text: Text to search
            
        Returns:
            List of entity names
        """
        entities = []
        
        # Add Western Ghats specific entities if mentioned
        for entity in self.WESTERN_GHATS_ENTITIES:
            if entity.lower() in text.lower():
                entities.append(entity)
        
        # Add Indian states if mentioned
        for state in self.INDIAN_STATES:
            if state.lower() in text.lower():
                entities.append(state)
        
        return list(set(entities))  # Remove duplicates
    
    def _generate_context_summary(
        self,
        text: str,
        numerical_facts: List[Dict],
        terminology: List[Dict]
    ) -> str:
        """
        Generate a concise context summary for the AI prompt.
        
        Args:
            text: Cleaned text
            numerical_facts: Extracted numerical facts
            terminology: Extracted terminology
            
        Returns:
            Context summary string
        """
        summary_parts = []
        
        # Add key numerical facts (limit to top 5)
        if numerical_facts:
            summary_parts.append("KEY FACTS:")
            for fact in numerical_facts[:5]:
                summary_parts.append(f"- {fact['value']}")
        
        # Add key terminology (limit to top 10)
        if terminology:
            if summary_parts:
                summary_parts.append("")
            summary_parts.append("KEY TERMINOLOGY:")
            for term in terminology[:10]:
                summary_parts.append(f"- {term['term']}: {term['definition'][:80]}")
        
        return "\n".join(summary_parts)
    
    def get_vocabulary_bank(self) -> List[str]:
        """
        Get vocabulary bank for distractor generation.
        
        Returns:
            List of terms that can be used as distractors
        """
        if not self.processed:
            self.process()
        
        vocabulary = []
        
        # Add terminology terms
        for term in self.processed.terminology:
            vocabulary.append(term['term'])
        
        # Add entities (excluding correct answers)
        vocabulary.extend(self.processed.entities)
        
        # Add states as potential distractors
        vocabulary.extend(self.INDIAN_STATES)
        
        return list(set(vocabulary))
    
    def get_numerical_focus_areas(self) -> List[str]:
        """
        Get numerical facts formatted for question generation.
        
        Returns:
            List of numerical facts suitable for AI prompting
        """
        if not self.processed:
            self.process()
        
        focus_areas = []
        
        for fact in self.processed.numerical_facts:
            focus_areas.append(f"{fact['value']} ({fact['type']})")
        
        return focus_areas


def filter_content_for_quiz(content: str) -> ProcessedContent:
    """
    Convenience function to filter content.
    
    Args:
        content: Raw study material content
        
    Returns:
        ProcessedContent object
    """
    filter_obj = ContentFilter(content)
    return filter_obj.process()


def extract_western_ghats_facts(text: str) -> Dict:
    """
    Specialized extraction for Western Ghats content.
    
    Args:
        text: Study material about Western Ghats
        
    Returns:
        Dictionary with specialized facts
    """
    filter_obj = ContentFilter(text)
    processed = filter_obj.process()
    
    # Find specific Western Ghats facts
    ghats_facts = {
        'age': None,
        'length': None,
        'height': None,
        'biodiversity': None,
        'rivers': [],
        'protected_areas': [],
        'endemic_species': [],
    }
    
    # Extract age (e.g., "150 million years")
    age_match = re.search(r'(\d+(?:\.\d+)?\s*(?:million|billion)\s*years?)', text, re.IGNORECASE)
    if age_match:
        ghats_facts['age'] = age_match.group(1)
    
    # Extract length (e.g., "1,600 km")
    length_match = re.search(r'(\d+(?:,\d{3})*\s*km)', text, re.IGNORECASE)
    if length_match:
        ghats_facts['length'] = length_match.group(1)
    
    # Extract height (e.g., "2,695 m")
    height_match = re.search(r'(\d+(?:,\d{3})*\s*m(?:\s*above)?)', text, re.IGNORECASE)
    if height_match:
        ghats_facts['height'] = height_match.group(1)
    
    # Extract biodiversity numbers
    bio_match = re.search(r'(over\s+)?(\d+(?:,\d{3})*\s+(?:species|flowering\s+plants))', text, re.IGNORECASE)
    if bio_match:
        ghats_facts['biodiversity'] = bio_match.group(0)
    
    # Extract river names
    rivers = ['Periyar', 'Bharatapuzha', 'Pamba', 'Chalakudy', 'Bharatapuzha', 'Godavari', 'Krishna']
    for river in rivers:
        if river.lower() in text.lower():
            ghats_facts['rivers'].append(river)
    
    # Extract protected areas
    protected = ['Eravikulam', 'Silent Valley', 'Wayanad', 'Bandipur', 'Nagarhole', ' Periyar']
    for area in protected:
        if area.lower() in text.lower():
            ghats_facts['protected_areas'].append(area)
    
    # Extract endemic species
    species = ['Nilgiri Tahr', 'Lion-tailed Macaque', 'Malabar Giant Squirrel', 'Neelakurinji']
    for sp in species:
        if sp.lower() in text.lower():
            ghats_facts['endemic_species'].append(sp)
    
    return ghats_facts

