import requests
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

class RobotsProcessor:
    def __init__(self):
        self.robots = {}

    def can_fetch(self, url):
        """Check if we are allowed to crawl the given URL."""
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

        if base_url not in self.robots:
            robots_txt = self.fetch_robots_txt(base_url)
            self.robots[base_url] = robots_txt

        return self.robots[base_url].can_fetch("*", url)

    def fetch_robots_txt(self, url):
        """Fetch and parse the robots.txt file."""
        robots = RobotFileParser()
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                robots.parse(response.text.splitlines())
        except requests.RequestException:
            pass

        return robots

