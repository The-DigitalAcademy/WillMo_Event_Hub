from datetime import datetime

# Sample list of upcoming events (replace with real data from a database or API later)
upcoming_events = [
    {"title": "Tech Conference 2025", "date": "2025-03-20", "location": "San Francisco, CA", "description": "A conference about the latest in tech."},
    {"title": "Music Festival", "date": "2025-04-10", "location": "Los Angeles, CA", "description": "An unforgettable weekend of music."},
    {"title": "Business Networking Gala", "date": "2025-05-15", "location": "New York, NY", "description": "Meet professionals and expand your network."},
]

# Function to get upcoming events
def get_upcoming_events():
    """Returns a list of upcoming events with dates on or after today."""
    today = datetime.today().date()
    return [event for event in upcoming_events if datetime.strptime(event["date"], "%Y-%m-%d").date() >= today]


