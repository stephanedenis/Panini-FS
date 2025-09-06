#!/usr/bin/env python3
"""
📚 PANINI PUBLICATION ENGINE
Génération automatisée contenu pour Medium et Leanpub

GitHub: https://github.com/stephanedenis/PaniniFS-PublicationEngine
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import markdown
import re

class PublicationGenerator:
    """
    Générateur automatisé de contenu pour plateformes de publication
    """
    
    def __init__(self):
        self.templates = {
            'medium_short': self._load_medium_template(),
            'leanpub_book': self._load_leanpub_template(),
            'blog_post': self._load_blog_template()
        }
        
    def generate_medium_article(self, content_data: Dict) -> str:
        """
        Génération article Medium optimisé viral
        
        Args:
            content_data: {
                'title': str,
                'hook': str,
                'key_points': List[str],
                'story': str,
                'code_examples': List[str],
                'call_to_action': str
            }
        """
        
        template = self.templates['medium_short']
        
        # Hook accrocheur
        hook_section = self._format_hook(content_data['hook'])
        
        # Points clés avec emojis
        points_section = self._format_key_points(content_data['key_points'])
        
        # Story narrative
        story_section = self._format_story(content_data['story'])
        
        # Exemples code
        code_section = self._format_code_examples(content_data['code_examples'])
        
        # CTA
        cta_section = self._format_cta(content_data['call_to_action'])
        
        article = template.format(
            title=content_data['title'],
            hook=hook_section,
            key_points=points_section,
            story=story_section,
            code_examples=code_section,
            cta=cta_section,
            date=datetime.now().strftime("%B %d, %Y")
        )
        
        return article
    
    def generate_leanpub_book(self, chapters_data: List[Dict]) -> Dict[str, str]:
        """
        Génération livre Leanpub complet multi-chapitres
        
        Args:
            chapters_data: List[{
                'title': str,
                'content': str,
                'code_examples': List[str],
                'exercises': List[str]
            }]
        """
        
        book_files = {}
        
        # Génération Book.txt (table des matières)
        toc = self._generate_table_of_contents(chapters_data)
        book_files['Book.txt'] = toc
        
        # Génération chapitres individuels
        for i, chapter in enumerate(chapters_data):
            chapter_filename = f"chapter_{i+1:02d}.md"
            chapter_content = self._format_leanpub_chapter(chapter)
            book_files[chapter_filename] = chapter_content
        
        # Génération métadonnées
        book_files['metadata.txt'] = self._generate_leanpub_metadata()
        
        return book_files
    
    def _load_medium_template(self) -> str:
        return """# {title}

{hook}

---

## 🎯 The Key Insights

{key_points}

---

## 🚀 The Story

{story}

---

## �� Code in Action

{code_examples}

---

## 🌟 What's Next?

{cta}

---

*Published on {date} | Follow for more AI-human collaboration insights*
"""
    
    def _load_leanpub_template(self) -> str:
        return """# {title}

{content}

## 💻 Code Examples

{code_examples}

## 🧪 Exercises

{exercises}

---
"""
    
    def _load_blog_template(self) -> str:
        return """---
title: {title}
date: {date}
tags: {tags}
---

{content}
"""
    
    def _format_hook(self, hook: str) -> str:
        """Format hook avec impact visuel"""
        return f"## 🔥 {hook}\n\n*This changed everything...*"
    
    def _format_key_points(self, points: List[str]) -> str:
        """Format points clés avec emojis"""
        formatted_points = []
        emojis = ["⚡", "🧠", "🎯", "🚀", "💡", "🔥", "✨", "🌟"]
        
        for i, point in enumerate(points):
            emoji = emojis[i % len(emojis)]
            formatted_points.append(f"{emoji} **{point}**")
        
        return "\n\n".join(formatted_points)
    
    def _format_story(self, story: str) -> str:
        """Format story avec structure narrative"""
        # Ajout de breaks visuels
        story = story.replace('\n\n', '\n\n---\n\n')
        return story
    
    def _format_code_examples(self, examples: List[str]) -> str:
        """Format exemples code avec syntax highlighting"""
        formatted_examples = []
        
        for example in examples:
            formatted_examples.append(f"```python\n{example}\n```")
        
        return "\n\n".join(formatted_examples)
    
    def _format_cta(self, cta: str) -> str:
        """Format call-to-action engageant"""
        return f"""**{cta}**

👏 **Clap if this resonated with you**
🔔 **Follow for more AI insights**  
💬 **Comment your thoughts below**
🔗 **Share with your network**"""
    
    def _generate_table_of_contents(self, chapters: List[Dict]) -> str:
        """Génération table des matières Leanpub"""
        toc = "frontmatter.md\n"
        
        for i, chapter in enumerate(chapters):
            toc += f"chapter_{i+1:02d}.md\n"
        
        toc += "backmatter.md"
        return toc
    
    def _format_leanpub_chapter(self, chapter: Dict) -> str:
        """Format chapitre Leanpub"""
        template = self._load_leanpub_template()
        
        code_section = "\n\n".join([f"```python\n{code}\n```" for code in chapter.get('code_examples', [])])
        exercises_section = "\n\n".join([f"**Exercise {i+1}**: {ex}" for i, ex in enumerate(chapter.get('exercises', []))])
        
        return template.format(
            title=chapter['title'],
            content=chapter['content'],
            code_examples=code_section,
            exercises=exercises_section
        )
    
    def _generate_leanpub_metadata(self) -> str:
        """Génération métadonnées Leanpub"""
        return """title: PaniniFS - AI-Human Collaboration Revolution
subtitle: Ultra-Reactive Systems & Autonomous Intelligence
author: Stéphane Denis
language: en
version: 1.0
"""

# 🧪 DEMO SYSTÈME
def demo_publication_engine():
    print("📚 DEMO PUBLICATION ENGINE")
    print("=" * 50)
    
    generator = PublicationGenerator()
    
    # Test génération Medium
    medium_data = {
        'title': "The 2-Second Rule That Changed AI Forever",
        'hook': "What I learned building ultra-reactive AI systems",
        'key_points': [
            "Humans get frustrated after 2 seconds",
            "Multi-path execution saves everything",
            "Feedback loops are more important than speed"
        ],
        'story': "It started with a simple Colab timeout...",
        'code_examples': ["controller = UltraReactiveController()", "await controller.execute()"],
        'call_to_action': "Try this in your next AI project"
    }
    
    print("📝 Génération article Medium...")
    medium_article = generator.generate_medium_article(medium_data)
    print(f"✅ Article généré: {len(medium_article)} caractères")
    
    # Test génération Leanpub
    chapters_data = [
        {
            'title': "Introduction to Ultra-Reactive Systems",
            'content': "The journey begins...",
            'code_examples': ["print('Hello Ultra-Reactive')"],
            'exercises': ["Implement your first reactive controller"]
        }
    ]
    
    print("\n📖 Génération livre Leanpub...")
    book_files = generator.generate_leanpub_book(chapters_data)
    print(f"✅ Livre généré: {len(book_files)} fichiers")
    
    print("\n🏁 Demo completed!")

if __name__ == "__main__":
    demo_publication_engine()
