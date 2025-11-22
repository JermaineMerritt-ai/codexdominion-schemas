#!/usr/bin/env python3
"""
Codex Multi-Language Intelligence System

Advanced multi-language processing capabilities for the Codex Dominion including:
- Natural language understanding and generation
- Programming language interpretation and generation
- Real-time translation and localization
- Cross-language communication protocols
- Universal code generation
"""

import re
import json
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from pathlib import Path
import streamlit as st

class CodexMultiLanguageIntelligence:
    """Advanced multi-language processing system"""
    
    def __init__(self):
        self.supported_natural_languages = {
            "en": {"name": "English", "native": "English", "direction": "ltr", "status": "native"},
            "es": {"name": "Spanish", "native": "Español", "direction": "ltr", "status": "active"},
            "fr": {"name": "French", "native": "Français", "direction": "ltr", "status": "active"},
            "de": {"name": "German", "native": "Deutsch", "direction": "ltr", "status": "active"},
            "ja": {"name": "Japanese", "native": "日本語", "direction": "ltr", "status": "active"},
            "zh": {"name": "Chinese", "native": "中文", "direction": "ltr", "status": "active"},
            "ar": {"name": "Arabic", "native": "العربية", "direction": "rtl", "status": "active"},
            "ru": {"name": "Russian", "native": "Русский", "direction": "ltr", "status": "active"},
            "pt": {"name": "Portuguese", "native": "Português", "direction": "ltr", "status": "active"},
            "ko": {"name": "Korean", "native": "한국어", "direction": "ltr", "status": "active"},
            "hi": {"name": "Hindi", "native": "हिंदी", "direction": "ltr", "status": "learning"},
            "it": {"name": "Italian", "native": "Italiano", "direction": "ltr", "status": "active"}
        }
        
        self.supported_programming_languages = {
            "python": {
                "name": "Python",
                "extensions": [".py", ".pyw"],
                "interpreter": "python",
                "paradigms": ["object-oriented", "functional", "procedural"],
                "complexity": "beginner",
                "ai_capability": "expert"
            },
            "javascript": {
                "name": "JavaScript", 
                "extensions": [".js", ".mjs"],
                "interpreter": "node",
                "paradigms": ["functional", "object-oriented", "event-driven"],
                "complexity": "intermediate",
                "ai_capability": "expert"
            },
            "typescript": {
                "name": "TypeScript",
                "extensions": [".ts", ".tsx"],
                "interpreter": "ts-node",
                "paradigms": ["functional", "object-oriented", "static-typed"],
                "complexity": "intermediate",
                "ai_capability": "expert"
            },
            "java": {
                "name": "Java",
                "extensions": [".java"],
                "interpreter": "java",
                "paradigms": ["object-oriented", "concurrent"],
                "complexity": "intermediate",
                "ai_capability": "advanced"
            },
            "cpp": {
                "name": "C++",
                "extensions": [".cpp", ".cc", ".cxx"],
                "interpreter": "g++",
                "paradigms": ["object-oriented", "procedural", "generic"],
                "complexity": "advanced",
                "ai_capability": "advanced"
            },
            "rust": {
                "name": "Rust",
                "extensions": [".rs"],
                "interpreter": "rustc",
                "paradigms": ["systems", "functional", "concurrent"],
                "complexity": "advanced",
                "ai_capability": "intermediate"
            },
            "go": {
                "name": "Go",
                "extensions": [".go"],
                "interpreter": "go",
                "paradigms": ["concurrent", "procedural"],
                "complexity": "intermediate",
                "ai_capability": "advanced"
            },
            "php": {
                "name": "PHP",
                "extensions": [".php"],
                "interpreter": "php",
                "paradigms": ["web", "object-oriented"],
                "complexity": "beginner",
                "ai_capability": "advanced"
            },
            "swift": {
                "name": "Swift",
                "extensions": [".swift"],
                "interpreter": "swift",
                "paradigms": ["object-oriented", "functional"],
                "complexity": "intermediate",
                "ai_capability": "intermediate"
            },
            "kotlin": {
                "name": "Kotlin",
                "extensions": [".kt", ".kts"],
                "interpreter": "kotlinc",
                "paradigms": ["object-oriented", "functional"],
                "complexity": "intermediate",
                "ai_capability": "intermediate"
            },
            "sql": {
                "name": "SQL",
                "extensions": [".sql"],
                "interpreter": "various",
                "paradigms": ["declarative", "relational"],
                "complexity": "beginner",
                "ai_capability": "expert"
            },
            "html": {
                "name": "HTML",
                "extensions": [".html", ".htm"],
                "interpreter": "browser",
                "paradigms": ["markup", "declarative"],
                "complexity": "beginner",
                "ai_capability": "expert"
            },
            "css": {
                "name": "CSS",
                "extensions": [".css"],
                "interpreter": "browser",
                "paradigms": ["declarative", "styling"],
                "complexity": "beginner",
                "ai_capability": "expert"
            }
        }
        
        self.translation_templates = {
            "greeting": {
                "en": "Hello! Welcome to the Codex Dominion.",
                "es": "¡Hola! Bienvenido al Dominio Codex.",
                "fr": "Bonjour! Bienvenue dans le Domaine Codex.",
                "de": "Hallo! Willkommen in der Codex-Herrschaft.",
                "ja": "こんにちは！Codex Dominionへようこそ。",
                "zh": "您好！欢迎来到法典统治。",
                "ar": "مرحبا! أهلا بك في مملكة المخطوطات.",
                "ru": "Привет! Добро пожаловать в Кодекс Доминион."
            },
            "flame_blessing": {
                "en": "By flame and by silence, the eternal wisdom guides us.",
                "es": "Por llama y por silencio, la sabiduría eterna nos guía.",
                "fr": "Par la flamme et par le silence, la sagesse éternelle nous guide.",
                "de": "Durch Flamme und durch Stille leitet uns die ewige Weisheit.",
                "ja": "炎と静寂によって、永遠の知恵が私たちを導く。",
                "zh": "通过火焰和寂静，永恒的智慧指引着我们。",
                "ar": "بالنار والصمت، تهدينا الحكمة الأبدية.",
                "ru": "Пламенем и молчанием вечная мудрость ведет нас."
            },
            "council_proclamation": {
                "en": "The Council proclaims digital sovereignty for all.",
                "es": "El Consejo proclama la soberanía digital para todos.",
                "fr": "Le Conseil proclame la souveraineté numérique pour tous.",
                "de": "Der Rat verkündet digitale Souveränität für alle.",
                "ja": "評議会はすべての人のためのデジタル主権を宣言する。",
                "zh": "议会宣布为所有人实现数字主权。",
                "ar": "يعلن المجلس السيادة الرقمية للجميع.",
                "ru": "Совет провозглашает цифровой суверенитет для всех."
            }
        }
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect the language of input text"""
        
        # Simple language detection based on character patterns
        detection_result = {
            "detected_language": "en",
            "confidence": 0.0,
            "possible_languages": [],
            "is_code": False,
            "programming_language": None
        }
        
        # Check if it's code first
        if self._is_programming_code(text):
            detection_result["is_code"] = True
            detection_result["programming_language"] = self._detect_programming_language(text)
            return detection_result
        
        # Natural language detection
        text_lower = text.lower()
        
        # Language patterns and keywords
        language_patterns = {
            "en": ["the", "and", "is", "in", "to", "of", "a", "for", "with"],
            "es": ["el", "la", "de", "que", "y", "en", "un", "es", "se", "no"],
            "fr": ["le", "de", "et", "à", "un", "il", "être", "et", "en", "avoir"],
            "de": ["der", "die", "und", "in", "den", "von", "zu", "das", "mit", "sich"],
            "ja": ["の", "に", "は", "を", "が", "と", "で", "て", "だ", "です"],
            "zh": ["的", "一", "是", "在", "不", "了", "有", "和", "人", "这"],
            "ar": ["في", "من", "إلى", "على", "أن", "هذا", "كان", "قد", "لا", "ما"],
            "ru": ["и", "в", "не", "на", "я", "быть", "тот", "этот", "они", "мы"]
        }
        
        # Score each language
        scores = {}
        for lang_code, keywords in language_patterns.items():
            score = 0
            for keyword in keywords:
                score += text_lower.count(keyword)
            scores[lang_code] = score
        
        # Find best match
        if scores:
            best_match = max(scores, key=scores.get)
            max_score = scores[best_match]
            total_words = len(text.split())
            
            if max_score > 0 and total_words > 0:
                detection_result["detected_language"] = best_match
                detection_result["confidence"] = min(max_score / total_words, 1.0)
                
                # Add possible alternatives
                sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                detection_result["possible_languages"] = [
                    {"language": lang, "score": score} 
                    for lang, score in sorted_scores[:3] if score > 0
                ]
        
        return detection_result
    
    def translate_text(self, text: str, source_lang: str = "auto", target_lang: str = "en") -> Dict[str, Any]:
        """Translate text between languages"""
        
        # Auto-detect source language if needed
        if source_lang == "auto":
            detection = self.detect_language(text)
            source_lang = detection["detected_language"]
        
        translation_result = {
            "source_text": text,
            "source_language": source_lang,
            "target_language": target_lang,
            "translated_text": text,  # Default to original
            "confidence": 0.0,
            "method": "template_based"
        }
        
        # Check template translations first
        for template_key, translations in self.translation_templates.items():
            if text.lower() in translations.get(source_lang, "").lower():
                if target_lang in translations:
                    translation_result["translated_text"] = translations[target_lang]
                    translation_result["confidence"] = 0.95
                    translation_result["method"] = "template_exact_match"
                    return translation_result
        
        # Simple rule-based translations for common patterns
        if source_lang != target_lang:
            translation_result["translated_text"] = self._rule_based_translate(text, source_lang, target_lang)
            translation_result["confidence"] = 0.6
            translation_result["method"] = "rule_based"
        
        return translation_result
    
    def generate_code(self, description: str, target_language: str, style: str = "professional") -> Dict[str, Any]:
        """Generate code in specified programming language"""
        
        generation_result = {
            "description": description,
            "target_language": target_language,
            "style": style,
            "generated_code": "",
            "explanation": "",
            "confidence": 0.0,
            "suggestions": []
        }
        
        if target_language not in self.supported_programming_languages:
            generation_result["generated_code"] = f"# Language '{target_language}' not supported yet"
            return generation_result
        
        # Code generation templates based on common patterns
        description_lower = description.lower()
        
        if "hello world" in description_lower:
            generation_result = self._generate_hello_world(target_language, style)
        elif "api" in description_lower or "endpoint" in description_lower:
            generation_result = self._generate_api_code(target_language, style, description)
        elif "function" in description_lower:
            generation_result = self._generate_function_code(target_language, style, description)
        elif "class" in description_lower:
            generation_result = self._generate_class_code(target_language, style, description)
        elif "database" in description_lower or "sql" in description_lower:
            generation_result = self._generate_database_code(target_language, style, description)
        else:
            generation_result = self._generate_generic_code(target_language, style, description)
        
        return generation_result
    
    def interpret_code(self, code: str, context: Dict = None) -> Dict[str, Any]:
        """Interpret and analyze code"""
        
        interpretation_result = {
            "code": code,
            "detected_language": None,
            "analysis": {},
            "suggestions": [],
            "errors": [],
            "complexity": "unknown",
            "purpose": "unknown"
        }
        
        # Detect programming language
        detected_lang = self._detect_programming_language(code)
        interpretation_result["detected_language"] = detected_lang
        
        if detected_lang:
            # Analyze code structure
            interpretation_result["analysis"] = self._analyze_code_structure(code, detected_lang)
            interpretation_result["suggestions"] = self._generate_code_suggestions(code, detected_lang)
            interpretation_result["complexity"] = self._assess_code_complexity(code, detected_lang)
            interpretation_result["purpose"] = self._determine_code_purpose(code, detected_lang)
        
        return interpretation_result
    
    def create_multilingual_interface(self, content: Dict, target_languages: List[str]) -> Dict[str, Any]:
        """Create multilingual interface content"""
        
        interface_result = {
            "source_content": content,
            "target_languages": target_languages,
            "translations": {},
            "rtl_languages": [],
            "missing_translations": []
        }
        
        for lang_code in target_languages:
            if lang_code in self.supported_natural_languages:
                lang_info = self.supported_natural_languages[lang_code]
                
                # Track RTL languages
                if lang_info["direction"] == "rtl":
                    interface_result["rtl_languages"].append(lang_code)
                
                # Translate content
                translations = {}
                for key, text in content.items():
                    if isinstance(text, str):
                        translation = self.translate_text(text, "en", lang_code)
                        translations[key] = translation["translated_text"]
                    else:
                        translations[key] = text  # Keep non-string content as is
                
                interface_result["translations"][lang_code] = {
                    "language_info": lang_info,
                    "content": translations
                }
            else:
                interface_result["missing_translations"].append(lang_code)
        
        return interface_result
    
    def _is_programming_code(self, text: str) -> bool:
        """Check if text appears to be programming code"""
        
        code_indicators = [
            r'def\s+\w+\s*\(',  # Python functions
            r'function\s+\w+\s*\(',  # JavaScript functions
            r'class\s+\w+',  # Class definitions
            r'import\s+\w+',  # Import statements
            r'#include\s*<',  # C/C++ includes
            r'\w+\s*=\s*\w+\(',  # Variable assignments with function calls
            r'if\s*\(',  # If statements
            r'for\s*\(',  # For loops
            r'while\s*\(',  # While loops
            r'\{[\s\S]*\}',  # Code blocks with braces
            r'console\.log\(',  # Console logging
            r'print\s*\(',  # Print statements
        ]
        
        for pattern in code_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        # Check for high density of programming symbols
        programming_chars = ['(', ')', '{', '}', '[', ']', ';', '=', '+', '-', '*', '/', '%']
        char_count = sum(text.count(char) for char in programming_chars)
        
        return char_count > len(text) * 0.1  # More than 10% programming symbols
    
    def _detect_programming_language(self, code: str) -> Optional[str]:
        """Detect programming language from code"""
        
        language_patterns = {
            "python": [
                r'def\s+\w+\s*\(',
                r'import\s+\w+',
                r'from\s+\w+\s+import',
                r'print\s*\(',
                r'if\s+__name__\s*==\s*["\']__main__["\']',
                r'class\s+\w+\s*\([^)]*\)\s*:'
            ],
            "javascript": [
                r'function\s+\w+\s*\(',
                r'const\s+\w+\s*=',
                r'let\s+\w+\s*=',
                r'var\s+\w+\s*=',
                r'console\.log\s*\(',
                r'=>',
                r'document\.',
                r'window\.'
            ],
            "typescript": [
                r'interface\s+\w+',
                r'type\s+\w+\s*=',
                r':\s*string\b',
                r':\s*number\b',
                r':\s*boolean\b',
                r'<.*>',
                r'export\s+(interface|type|class)'
            ],
            "java": [
                r'public\s+class\s+\w+',
                r'public\s+static\s+void\s+main',
                r'System\.out\.println',
                r'import\s+java\.',
                r'@\w+',
                r'new\s+\w+\s*\('
            ],
            "cpp": [
                r'#include\s*<\w+>',
                r'std::\w+',
                r'cout\s*<<',
                r'cin\s*>>',
                r'int\s+main\s*\(',
                r'using\s+namespace\s+std'
            ],
            "sql": [
                r'\bSELECT\b.*\bFROM\b',
                r'\bINSERT\s+INTO\b',
                r'\bUPDATE\b.*\bSET\b',
                r'\bDELETE\s+FROM\b',
                r'\bCREATE\s+TABLE\b',
                r'\bJOIN\b',
                r'\bWHERE\b'
            ],
            "html": [
                r'<html>',
                r'<head>',
                r'<body>',
                r'<div>',
                r'<p>',
                r'</\w+>',
                r'<!DOCTYPE'
            ],
            "css": [
                r'\w+\s*\{[^}]*\}',
                r'@media',
                r'@import',
                r'color\s*:',
                r'font-size\s*:',
                r'background\s*:'
            ]
        }
        
        scores = {}
        for lang, patterns in language_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, code, re.IGNORECASE | re.MULTILINE))
                score += matches
            scores[lang] = score
        
        if scores:
            best_match = max(scores, key=scores.get)
            if scores[best_match] > 0:
                return best_match
        
        return None
    
    def _rule_based_translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Simple rule-based translation for basic patterns"""
        
        # Very basic translation patterns - in real implementation, this would be much more sophisticated
        basic_translations = {
            ("en", "es"): {
                "hello": "hola",
                "world": "mundo",
                "the": "el/la",
                "and": "y",
                "system": "sistema",
                "code": "código",
                "function": "función"
            },
            ("en", "fr"): {
                "hello": "bonjour",
                "world": "monde",
                "the": "le/la",
                "and": "et",
                "system": "système",
                "code": "code",
                "function": "fonction"
            }
        }
        
        translation_dict = basic_translations.get((source_lang, target_lang), {})
        
        translated_text = text
        for source_word, target_word in translation_dict.items():
            translated_text = re.sub(rf'\b{source_word}\b', target_word, translated_text, flags=re.IGNORECASE)
        
        return translated_text
    
    def _generate_hello_world(self, language: str, style: str) -> Dict[str, Any]:
        """Generate Hello World code in specified language"""
        
        hello_world_templates = {
            "python": 'print("Hello, World!")',
            "javascript": 'console.log("Hello, World!");',
            "typescript": 'console.log("Hello, World!");',
            "java": '''public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}''',
            "cpp": '''#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World!" << endl;
    return 0;
}''',
            "rust": '''fn main() {
    println!("Hello, World!");
}''',
            "go": '''package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}''',
            "php": '<?php\necho "Hello, World!";',
            "html": '''<!DOCTYPE html>
<html>
<head>
    <title>Hello World</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>'''
        }
        
        code = hello_world_templates.get(language, f'// Hello World in {language}')
        
        return {
            "generated_code": code,
            "explanation": f"Basic Hello World program in {language}",
            "confidence": 0.95,
            "suggestions": ["Add error handling", "Make it interactive"]
        }
    
    def _generate_api_code(self, language: str, style: str, description: str) -> Dict[str, Any]:
        """Generate API code template"""
        
        api_templates = {
            "python": '''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/items/")
def create_item(item: Item):
    return {"item": item}''',
            
            "javascript": '''const express = require('express');
const app = express();

app.use(express.json());

app.get('/', (req, res) => {
    res.json({ message: 'Hello World' });
});

app.post('/items', (req, res) => {
    const item = req.body;
    res.json({ item });
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});''',
            
            "typescript": '''import express, { Request, Response } from 'express';

const app = express();
app.use(express.json());

interface Item {
    name: string;
    description?: string;
}

app.get('/', (req: Request, res: Response) => {
    res.json({ message: 'Hello World' });
});

app.post('/items', (req: Request, res: Response) => {
    const item: Item = req.body;
    res.json({ item });
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});'''
        }
        
        code = api_templates.get(language, f'// API template for {language} not available yet')
        
        return {
            "generated_code": code,
            "explanation": f"Basic REST API template in {language}",
            "confidence": 0.85,
            "suggestions": ["Add authentication", "Add error handling", "Add data validation"]
        }
    
    def _generate_function_code(self, language: str, style: str, description: str) -> Dict[str, Any]:
        """Generate function code based on description"""
        
        # Extract function name from description
        function_name = "myFunction"
        if "calculate" in description.lower():
            function_name = "calculate"
        elif "process" in description.lower():
            function_name = "processData"
        elif "validate" in description.lower():
            function_name = "validate"
        
        function_templates = {
            "python": f'''def {function_name}(data):
    """
    {description}
    """
    # Implementation here
    return data''',
            
            "javascript": f'''function {function_name}(data) {{
    // {description}
    // Implementation here
    return data;
}}''',
            
            "typescript": f'''function {function_name}(data: any): any {{
    // {description}  
    // Implementation here
    return data;
}}''',
            
            "java": f'''public static Object {function_name}(Object data) {{
    // {description}
    // Implementation here
    return data;
}}'''
        }
        
        code = function_templates.get(language, f'// Function template for {language}')
        
        return {
            "generated_code": code,
            "explanation": f"Function template in {language} based on: {description}",
            "confidence": 0.75,
            "suggestions": ["Add input validation", "Add error handling", "Add unit tests"]
        }
    
    def _generate_class_code(self, language: str, style: str, description: str) -> Dict[str, Any]:
        """Generate class code template"""
        
        class_templates = {
            "python": '''class MyClass:
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name''',
            
            "javascript": '''class MyClass {
    constructor(name) {
        this.name = name;
    }
    
    getName() {
        return this.name;
    }
    
    setName(name) {
        this.name = name;
    }
}''',
            
            "typescript": '''class MyClass {
    private name: string;
    
    constructor(name: string) {
        this.name = name;
    }
    
    getName(): string {
        return this.name;
    }
    
    setName(name: string): void {
        this.name = name;
    }
}''',
            
            "java": '''public class MyClass {
    private String name;
    
    public MyClass(String name) {
        this.name = name;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
}'''
        }
        
        code = class_templates.get(language, f'// Class template for {language}')
        
        return {
            "generated_code": code,
            "explanation": f"Basic class template in {language}",
            "confidence": 0.80,
            "suggestions": ["Add more methods", "Add validation", "Implement interfaces"]
        }
    
    def _generate_database_code(self, language: str, style: str, description: str) -> Dict[str, Any]:
        """Generate database code"""
        
        if language == "sql":
            code = '''CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- Insert sample data
INSERT INTO users (name, email) VALUES 
('John Doe', 'john@example.com'),
('Jane Smith', 'jane@example.com');

-- Query users
SELECT * FROM users WHERE email = 'john@example.com';'''
            
        elif language == "python":
            code = '''import sqlite3

def create_connection(db_file):
    """Create database connection"""
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    """Create users table"""
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn.execute(sql)
    conn.commit()

def insert_user(conn, name, email):
    """Insert a new user"""
    sql = "INSERT INTO users (name, email) VALUES (?, ?)"
    conn.execute(sql, (name, email))
    conn.commit()'''
        
        else:
            code = f'// Database code for {language} not implemented yet'
        
        return {
            "generated_code": code,
            "explanation": f"Database operations in {language}",
            "confidence": 0.80,
            "suggestions": ["Add error handling", "Add connection pooling", "Add migrations"]
        }
    
    def _generate_generic_code(self, language: str, style: str, description: str) -> Dict[str, Any]:
        """Generate generic code template"""
        
        code = f'''// {description}
// Generated code template for {language}

// TODO: Implement functionality based on description
// This is a placeholder implementation'''
        
        return {
            "generated_code": code,
            "explanation": f"Generic code template for {description}",
            "confidence": 0.50,
            "suggestions": ["Specify requirements more clearly", "Provide examples", "Break down into smaller tasks"]
        }
    
    def _analyze_code_structure(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code structure and patterns"""
        
        analysis = {
            "lines_of_code": len(code.splitlines()),
            "functions": 0,
            "classes": 0,
            "imports": 0,
            "comments": 0,
            "complexity_indicators": []
        }
        
        # Count different code elements
        function_patterns = {
            "python": [r'def\s+\w+', r'async\s+def\s+\w+'],
            "javascript": [r'function\s+\w+', r'\w+\s*=\s*\([^)]*\)\s*=>', r'\w+\s*:\s*function'],
            "java": [r'public\s+\w+\s+\w+\s*\(', r'private\s+\w+\s+\w+\s*\(']
        }
        
        class_patterns = {
            "python": [r'class\s+\w+'],
            "javascript": [r'class\s+\w+'],
            "java": [r'class\s+\w+', r'interface\s+\w+']
        }
        
        if language in function_patterns:
            for pattern in function_patterns[language]:
                analysis["functions"] += len(re.findall(pattern, code))
        
        if language in class_patterns:
            for pattern in class_patterns[language]:
                analysis["classes"] += len(re.findall(pattern, code))
        
        # Count imports
        import_patterns = [r'import\s+', r'from\s+\w+\s+import', r'#include', r'require\(']
        for pattern in import_patterns:
            analysis["imports"] += len(re.findall(pattern, code))
        
        # Count comments
        comment_patterns = [r'//.*$', r'#.*$', r'/\*.*?\*/', r'""".*?"""', r"'''.*?'''"]
        for pattern in comment_patterns:
            analysis["comments"] += len(re.findall(pattern, code, re.MULTILINE | re.DOTALL))
        
        return analysis
    
    def _generate_code_suggestions(self, code: str, language: str) -> List[str]:
        """Generate improvement suggestions for code"""
        
        suggestions = []
        
        # Check for common issues
        if not re.search(r'#.*|//.*', code):
            suggestions.append("Add comments to explain the code")
        
        if language == "python":
            if not re.search(r'""".*?"""', code, re.DOTALL):
                suggestions.append("Add docstrings to functions and classes")
            if re.search(r'except:', code):
                suggestions.append("Use specific exception types instead of bare except")
        
        elif language in ["javascript", "typescript"]:
            if not re.search(r'const\s+|let\s+', code):
                suggestions.append("Use const/let instead of var for variable declarations")
            if not re.search(r'===|!==', code) and re.search(r'==|!=', code):
                suggestions.append("Use strict equality (===) instead of loose equality (==)")
        
        # General suggestions
        if len(code.splitlines()) > 50:
            suggestions.append("Consider breaking this into smaller functions")
        
        if not suggestions:
            suggestions.append("Code looks good! Consider adding unit tests")
        
        return suggestions
    
    def _assess_code_complexity(self, code: str, language: str) -> str:
        """Assess code complexity level"""
        
        lines = len(code.splitlines())
        functions = len(re.findall(r'def\s+|function\s+|=>\s*{', code))
        classes = len(re.findall(r'class\s+', code))
        loops = len(re.findall(r'for\s*\(|while\s*\(|for\s+\w+\s+in', code))
        conditions = len(re.findall(r'if\s*\(|elif\s+|else\s*:|switch\s*\(', code))
        
        complexity_score = lines * 0.1 + functions * 2 + classes * 3 + loops * 1.5 + conditions * 1
        
        if complexity_score < 10:
            return "simple"
        elif complexity_score < 25:
            return "moderate"
        elif complexity_score < 50:
            return "complex"
        else:
            return "very_complex"
    
    def _determine_code_purpose(self, code: str, language: str) -> str:
        """Determine the purpose of code"""
        
        code_lower = code.lower()
        
        if any(word in code_lower for word in ["api", "endpoint", "route", "server"]):
            return "web_api"
        elif any(word in code_lower for word in ["database", "sql", "query", "model"]):
            return "data_processing"
        elif any(word in code_lower for word in ["test", "assert", "mock"]):
            return "testing"
        elif any(word in code_lower for word in ["class", "object", "interface"]):
            return "object_oriented"
        elif any(word in code_lower for word in ["calculate", "math", "algorithm"]):
            return "computation"
        elif any(word in code_lower for word in ["ui", "component", "render", "html"]):
            return "user_interface"
        else:
            return "general_purpose"

def main():
    """Demo the multi-language system"""
    
    st.set_page_config(
        page_title="Codex Multi-Language Intelligence",
        page_icon="🌍",
        layout="wide"
    )
    
    st.title("🌍 Codex Multi-Language Intelligence System")
    st.markdown("*Advanced multi-language processing capabilities for the Codex Dominion*")
    
    mli = CodexMultiLanguageIntelligence()
    
    # Sidebar for feature selection
    st.sidebar.title("🔧 Features")
    feature = st.sidebar.selectbox(
        "Choose a feature:",
        [
            "🔍 Language Detection",
            "🌐 Text Translation", 
            "💻 Code Generation",
            "🔬 Code Analysis",
            "🌍 Multilingual Interface",
            "📊 System Overview"
        ]
    )
    
    if feature == "🔍 Language Detection":
        st.header("🔍 Language Detection")
        
        test_text = st.text_area(
            "Enter text to detect language:",
            value="Hello! Welcome to the Codex Dominion. We support multiple languages and programming capabilities.",
            height=150
        )
        
        if st.button("🔍 Detect Language"):
            result = mli.detect_language(test_text)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Detection Result")
                if result["is_code"]:
                    st.success(f"**Detected:** Programming Code ({result['programming_language']})")
                else:
                    lang_info = mli.supported_natural_languages.get(result["detected_language"], {})
                    st.success(f"**Detected:** {lang_info.get('name', 'Unknown')} ({result['detected_language']})")
                    st.info(f"**Confidence:** {result['confidence']:.1%}")
            
            with col2:
                st.subheader("Possible Languages")
                if result["possible_languages"]:
                    for lang_data in result["possible_languages"]:
                        lang_code = lang_data["language"]
                        lang_info = mli.supported_natural_languages.get(lang_code, {})
                        st.write(f"- {lang_info.get('name', lang_code)}: {lang_data['score']} matches")
    
    elif feature == "🌐 Text Translation":
        st.header("🌐 Text Translation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            source_lang = st.selectbox(
                "Source Language:",
                ["auto"] + list(mli.supported_natural_languages.keys()),
                format_func=lambda x: "Auto-detect" if x == "auto" else f"{mli.supported_natural_languages[x]['name']} ({mli.supported_natural_languages[x]['native']})"
            )
            
            source_text = st.text_area(
                "Text to translate:",
                value="By flame and by silence, the eternal wisdom guides us.",
                height=150
            )
        
        with col2:
            target_lang = st.selectbox(
                "Target Language:",
                list(mli.supported_natural_languages.keys()),
                index=1,
                format_func=lambda x: f"{mli.supported_natural_languages[x]['name']} ({mli.supported_natural_languages[x]['native']})"
            )
        
        if st.button("🌐 Translate"):
            result = mli.translate_text(source_text, source_lang, target_lang)
            
            st.subheader("Translation Result")
            st.success(f"**Translated Text:** {result['translated_text']}")
            st.info(f"**Method:** {result['method']}")
            st.info(f"**Confidence:** {result['confidence']:.1%}")
    
    elif feature == "💻 Code Generation":
        st.header("💻 Code Generation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            description = st.text_area(
                "Describe what you want to code:",
                value="Create a hello world program",
                height=100
            )
            
            target_language = st.selectbox(
                "Programming Language:",
                list(mli.supported_programming_languages.keys()),
                format_func=lambda x: mli.supported_programming_languages[x]["name"]
            )
            
            style = st.selectbox("Style:", ["professional", "beginner", "advanced"])
        
        with col2:
            if st.button("💻 Generate Code"):
                result = mli.generate_code(description, target_language, style)
                
                st.subheader("Generated Code")
                st.code(result["generated_code"], language=target_language)
                
                st.subheader("Explanation")
                st.write(result["explanation"])
                
                if result["suggestions"]:
                    st.subheader("Suggestions")
                    for suggestion in result["suggestions"]:
                        st.write(f"- {suggestion}")
    
    elif feature == "🔬 Code Analysis":
        st.header("🔬 Code Analysis")
        
        code_input = st.text_area(
            "Paste your code here:",
            value='''def calculate_fibonacci(n):
    """Calculate fibonacci number recursively"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# Test the function
print(calculate_fibonacci(10))''',
            height=200
        )
        
        if st.button("🔬 Analyze Code"):
            result = mli.interpret_code(code_input)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Analysis Results")
                if result["detected_language"]:
                    lang_info = mli.supported_programming_languages[result["detected_language"]]
                    st.success(f"**Language:** {lang_info['name']}")
                
                st.write(f"**Purpose:** {result['purpose'].replace('_', ' ').title()}")
                st.write(f"**Complexity:** {result['complexity'].title()}")
                
                if result["analysis"]:
                    st.write("**Code Metrics:**")
                    for key, value in result["analysis"].items():
                        if isinstance(value, (int, float)):
                            st.write(f"- {key.replace('_', ' ').title()}: {value}")
            
            with col2:
                st.subheader("Suggestions")
                if result["suggestions"]:
                    for suggestion in result["suggestions"]:
                        st.write(f"💡 {suggestion}")
                else:
                    st.write("No suggestions - code looks good!")
    
    elif feature == "🌍 Multilingual Interface":
        st.header("🌍 Multilingual Interface Generator")
        
        interface_content = {
            "welcome_message": "Welcome to Codex Dominion",
            "navigation_home": "Home",
            "navigation_about": "About",
            "navigation_contact": "Contact",
            "button_submit": "Submit",
            "button_cancel": "Cancel",
            "flame_blessing": "By flame and by silence, wisdom eternal"
        }
        
        selected_languages = st.multiselect(
            "Select target languages:",
            list(mli.supported_natural_languages.keys()),
            default=["es", "fr", "de", "ja"],
            format_func=lambda x: f"{mli.supported_natural_languages[x]['name']} ({mli.supported_natural_languages[x]['native']})"
        )
        
        if st.button("🌍 Generate Multilingual Interface") and selected_languages:
            result = mli.create_multilingual_interface(interface_content, selected_languages)
            
            st.subheader("Generated Translations")
            
            for lang_code, translation_data in result["translations"].items():
                lang_info = translation_data["language_info"]
                
                st.markdown(f"### {lang_info['name']} ({lang_info['native']})")
                
                if lang_info["direction"] == "rtl":
                    st.info("⚠️ This is a right-to-left language - UI layout should be mirrored")
                
                for key, translated_text in translation_data["content"].items():
                    st.write(f"**{key}:** {translated_text}")
                
                st.markdown("---")
    
    elif feature == "📊 System Overview":
        st.header("📊 Multi-Language System Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌐 Natural Languages")
            st.metric("Supported Languages", len(mli.supported_natural_languages))
            
            active_languages = [lang for lang, info in mli.supported_natural_languages.items() if info["status"] == "active"]
            st.metric("Active Languages", len(active_languages))
            
            rtl_languages = [lang for lang, info in mli.supported_natural_languages.items() if info["direction"] == "rtl"]
            st.metric("RTL Languages", len(rtl_languages))
            
            st.write("**Language Status:**")
            for lang_code, lang_info in mli.supported_natural_languages.items():
                status_emoji = {"active": "✅", "native": "🏠", "learning": "📚"}.get(lang_info["status"], "❓")
                st.write(f"{status_emoji} {lang_info['name']} ({lang_info['native']})")
        
        with col2:
            st.subheader("💻 Programming Languages")
            st.metric("Supported Languages", len(mli.supported_programming_languages))
            
            expert_languages = [lang for lang, info in mli.supported_programming_languages.items() if info["ai_capability"] == "expert"]
            st.metric("Expert Level", len(expert_languages))
            
            st.write("**Programming Language Capabilities:**")
            for lang_code, lang_info in mli.supported_programming_languages.items():
                capability_emoji = {"expert": "🏆", "advanced": "⭐", "intermediate": "👍"}.get(lang_info["ai_capability"], "📝")
                st.write(f"{capability_emoji} {lang_info['name']} ({lang_info['complexity']})")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🏛️ Codex Dominion**")
    st.sidebar.markdown("*Multi-Language Intelligence*")

if __name__ == "__main__":
    main()