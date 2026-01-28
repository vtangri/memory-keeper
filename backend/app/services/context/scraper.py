import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HistoryScraper:
    """
    Fetches historical context to enrich stories.
    """
    
    def fetch_events_for_year(self, year: int) -> list:
        """
        Scrapes external sources (Wikipedia etc) for events in a given year.
        """
        logger.info(f"Fetching historical events for year {year}...")
        
        # Mock Response
        events = [
            f"Major event in {year} involving geopolitical shifts.",
            f"Popular cultural phenomenon of {year}.",
            f"Technological breakthrough in {year}."
        ]
        return events

    def enrich_story(self, text: str) -> str:
        """
        Analyzes text for entities (years, places) and appends "Did you know?" boxes.
        """
        # Logic to extract years via regex/NER and calls fetch_events_for_year
        return text + "\n\n[Context: In this era, television was just becoming popular...]"
