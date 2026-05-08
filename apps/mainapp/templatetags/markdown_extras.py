from django import template
import markdown

register = template.Library()

@register.filter
def markdown_to_html(value):
    """
    Converts Markdown text to HTML using the markdown library with extra extensions.
    """
    if not value:
        return ''
    return markdown.markdown(value, extensions=['extra', 'codehilite', 'toc'])

@register.filter
def deduplicate_heading(content, title):
    """
    Removes redundant title from the beginning of the content.
    Matches Markdown headings (# Title) or plain text titles followed by a newline.
    """
    if not content or not title:
        return content
    
    title_str = str(title).strip().lower()
    content_str = content.strip()
    content_lower = content_str.lower()
    
    # Check for Markdown heading: # Title
    if content_lower.startswith(f'# {title_str}\n'):
        return content_str[len(title_str) + 3:].strip()
    
    # Check for Markdown heading: ## Title (common if users copy-paste)
    if content_lower.startswith(f'## {title_str}\n'):
        return content_str[len(title_str) + 4:].strip()

    # Check for Markdown heading: ### Title
    if content_lower.startswith(f'### {title_str}\n'):
        return content_str[len(title_str) + 5:].strip()
        
    # Check for plain text title followed by newline
    if content_lower.startswith(f'{title_str}\n'):
        return content_str[len(title_str):].strip()
        
    return content

@register.filter
def has_any_keyword(materials, keywords):
    """
    Checks if any material in the list has a title containing any of the comma-separated keywords.
    Usage: {{ study_materials|has_any_keyword:"Folklore,Myth,Sacred,Legend,Story" }}
    """
    if not materials or not keywords:
        return False
    keyword_list = [k.strip().lower() for k in keywords.split(',')]
    for material in materials:
        title = str(getattr(material, 'title', '')).lower()
        if any(kw in title for kw in keyword_list):
            return True
    return False

register.filter('markdown', markdown_to_html)
