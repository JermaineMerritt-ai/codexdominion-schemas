"""
AI Prompt Manager
Loads and manages AI prompt templates
"""
import os
from pathlib import Path

# Prompt file mapping
PROMPT_FILES = {
    'stock_analyst': 'ai_stock_analyst_prompt.txt',
    'portfolio_analyst': 'ai_portfolio_analyst_prompt.txt',
    'day_trade_ideas': 'ai_day_trade_ideas_prompt.txt',
    'daily_email': 'ai_daily_email_prompt.txt',
    'weekly_email': 'ai_weekly_portfolio_email_prompt.txt',
    'monthly_email': 'ai_monthly_deep_dive_prompt.txt',
    'risk_translator': 'ai_risk_profile_translator_prompt.txt',
    'concept_explainer': 'ai_concept_explainer_prompt.txt'
}

class AIPromptManager:
    """Manages AI prompt templates"""

    def __init__(self, prompts_dir=None):
        if prompts_dir is None:
            # Default to parent directory where prompts are stored
            prompts_dir = Path(__file__).parent.parent
        self.prompts_dir = Path(prompts_dir)
        self._cache = {}

    def load_prompt(self, prompt_name):
        """Load a specific prompt template"""
        if prompt_name in self._cache:
            return self._cache[prompt_name]

        if prompt_name not in PROMPT_FILES:
            raise ValueError(f"Unknown prompt: {prompt_name}")

        file_path = self.prompts_dir / PROMPT_FILES[prompt_name]

        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self._cache[prompt_name] = content
        return content

    def get_all_prompts(self):
        """Load all prompt templates"""
        return {name: self.load_prompt(name) for name in PROMPT_FILES.keys()}

    def format_prompt(self, prompt_name, **kwargs):
        """Load and format a prompt with data"""
        template = self.load_prompt(prompt_name)
        return template.format(**kwargs)

# Global instance
_manager = None

def get_manager(prompts_dir=None):
    """Get or create prompt manager instance"""
    global _manager
    if _manager is None:
        _manager = AIPromptManager(prompts_dir)
    return _manager

def load_prompt(prompt_name):
    """Convenience function to load a prompt"""
    return get_manager().load_prompt(prompt_name)

def get_all_prompts():
    """Convenience function to get all prompts"""
    return get_manager().get_all_prompts()

def format_prompt(prompt_name, **kwargs):
    """Convenience function to format a prompt"""
    return get_manager().format_prompt(prompt_name, **kwargs)
