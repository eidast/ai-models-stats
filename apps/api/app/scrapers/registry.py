"""Provider → scraper mapping."""
from app.scrapers.base import BaseScraper
from app.scrapers.anthropic import AnthropicScraper
from app.scrapers.deepseek import DeepSeekScraper
from app.scrapers.google import GoogleScraper
from app.scrapers.mistral import MistralScraper
from app.scrapers.openai import OpenAIScraper

SCRAPERS: list[type[BaseScraper]] = [
    OpenAIScraper,
    AnthropicScraper,
    GoogleScraper,
    MistralScraper,
    DeepSeekScraper,
]
