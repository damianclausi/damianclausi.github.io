#!/usr/bin/env python3
"""
RSS Feed Generator for Static Markdown Blog
Scans /logs folder for .md files and generates a valid RSS 2.0 feed.

Usage:
    python scripts/generate_rss.py

The script will create feed.xml in the project root.
"""

import os
import re
from datetime import datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Configuration
SITE_URL = "https://damianclausi.github.io"
SITE_TITLE = "Damian Clausi - Developer Logs"
SITE_DESCRIPTION = "Technical notes, tutorials, and insights from a Software Developer focused on Fullstack and Cloud."
AUTHOR_EMAIL = "damian.clausi@gmail.com"
LOGS_DIR = "logs"
OUTPUT_FILE = "feed.xml"


def extract_frontmatter(content: str) -> dict:
    """
    Extract YAML frontmatter from markdown content.
    Supports format:
    ---
    title: My Title
    date: 2026-01-26
    description: Some description
    ---
    """
    frontmatter = {}
    
    # Check for YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            yaml_content = parts[1].strip()
            for line in yaml_content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip().lower()] = value.strip().strip('"\'')
    
    return frontmatter


def extract_title_from_content(content: str) -> str:
    """Extract title from first H1 heading in markdown."""
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    return None


def extract_date_from_filename(filename: str) -> str:
    """
    Try to extract date from filename patterns:
    - YYYY-MM-DD-slug.md
    - Returns None if no date pattern found
    """
    # Pattern: YYYY-MM-DD at start of filename
    match = re.match(r'^(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return match.group(1)
    return None


def extract_date_from_content(content: str) -> str:
    """
    Try to extract date from content.
    Looks for patterns like:
    - *Posted: 2026-01-26*
    - *Last Updated: 2026-01-26*
    - date: 2026-01-26 (in frontmatter)
    """
    # Look for Posted/Updated pattern
    match = re.search(r'\*(?:Posted|Last Updated|Date):\s*(\d{4}-\d{2}-\d{2})\*', content)
    if match:
        return match.group(1)
    
    # Look for ISO date anywhere
    match = re.search(r'(\d{4}-\d{2}-\d{2})', content)
    if match:
        return match.group(1)
    
    return None


def get_post_metadata(filepath: Path) -> dict:
    """Extract all metadata from a markdown file."""
    content = filepath.read_text(encoding='utf-8')
    filename = filepath.stem  # filename without extension
    
    # Try frontmatter first
    frontmatter = extract_frontmatter(content)
    
    # Get title
    title = frontmatter.get('title') or extract_title_from_content(content) or filename.replace('-', ' ').title()
    
    # Get date
    date_str = (
        frontmatter.get('date') or
        extract_date_from_filename(filename) or
        extract_date_from_content(content)
    )
    
    # Parse date or use file modification time
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            date = datetime.fromtimestamp(filepath.stat().st_mtime)
    else:
        date = datetime.fromtimestamp(filepath.stat().st_mtime)
    
    # Get description
    description = frontmatter.get('description')
    if not description:
        # Use first paragraph after title as description
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('---') and not line.startswith('>'):
                # Clean markdown formatting
                description = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
                description = re.sub(r'\*([^*]+)\*', r'\1', description)
                description = re.sub(r'`([^`]+)`', r'\1', description)
                break
    
    if not description:
        description = f"Read more about {title}"
    
    return {
        'title': title,
        'date': date,
        'description': description[:200] + '...' if len(description) > 200 else description,
        'filename': filename,
        'link': f"{SITE_URL}/logs/viewer.html?post={filename}"
    }


def generate_rss(posts: list) -> str:
    """Generate RSS 2.0 XML from list of post metadata."""
    
    # Create root element
    rss = Element('rss')
    rss.set('version', '2.0')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
    
    # Create channel
    channel = SubElement(rss, 'channel')
    
    # Channel metadata
    SubElement(channel, 'title').text = SITE_TITLE
    SubElement(channel, 'link').text = SITE_URL
    SubElement(channel, 'description').text = SITE_DESCRIPTION
    SubElement(channel, 'language').text = 'en-us'
    SubElement(channel, 'lastBuildDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    SubElement(channel, 'generator').text = 'Custom Python RSS Generator'
    
    # Atom self-link (required for valid feed)
    atom_link = SubElement(channel, 'atom:link')
    atom_link.set('href', f'{SITE_URL}/feed.xml')
    atom_link.set('rel', 'self')
    atom_link.set('type', 'application/rss+xml')
    
    # Add items (sorted by date, newest first)
    for post in sorted(posts, key=lambda x: x['date'], reverse=True):
        item = SubElement(channel, 'item')
        SubElement(item, 'title').text = post['title']
        SubElement(item, 'link').text = post['link']
        SubElement(item, 'description').text = post['description']
        SubElement(item, 'pubDate').text = post['date'].strftime('%a, %d %b %Y 00:00:00 +0000')
        SubElement(item, 'guid').text = post['link']
        SubElement(item, 'author').text = AUTHOR_EMAIL
    
    # Pretty print XML
    rough_string = tostring(rss, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    
    # Add XML declaration
    return reparsed.toprettyxml(indent="  ", encoding=None)


def main():
    """Main entry point."""
    # Get script directory and project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    logs_dir = project_root / LOGS_DIR
    output_path = project_root / OUTPUT_FILE
    
    print(f"📂 Scanning {logs_dir} for markdown files...")
    
    # Find all markdown files
    md_files = list(logs_dir.glob('*.md'))
    
    if not md_files:
        print("⚠️  No markdown files found in logs directory.")
        return
    
    print(f"📄 Found {len(md_files)} posts:")
    
    # Extract metadata from each file
    posts = []
    for filepath in md_files:
        try:
            metadata = get_post_metadata(filepath)
            posts.append(metadata)
            print(f"   ✓ {metadata['title']} ({metadata['date'].strftime('%Y-%m-%d')})")
        except Exception as e:
            print(f"   ✗ Error processing {filepath.name}: {e}")
    
    # Generate RSS
    print(f"\n🔧 Generating RSS feed...")
    rss_content = generate_rss(posts)
    
    # Write to file
    output_path.write_text(rss_content, encoding='utf-8')
    print(f"✅ Feed generated: {output_path}")
    print(f"   URL: {SITE_URL}/feed.xml")


if __name__ == '__main__':
    main()
