import requests
from config import RAWG_API_KEY, API_BASE_URL
from utils.cache_manager import cache


class APIHelper:
    """Helper for API calls with caching"""
    
    @staticmethod
    def get_games(params=None, use_cache=True):
        """Get games list with caching"""
        url = f"{API_BASE_URL}/games"
        
        # Add API key to params
        if params is None:
            params = {}
        params['key'] = RAWG_API_KEY
        
        # Try cache first
        if use_cache:
            cached_data = cache.get(url, params)
            if cached_data:
                print(f"Using cached data for games")
                return cached_data
        
        # Fetch from API
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                # Cache the response
                cache.set(url, params, data)
                return data
            return None
        except Exception as e:
            print(f"API Error: {e}")
            return None
    
    @staticmethod
    def get_game_details(game_id, use_cache=True):
        """Get game details with caching"""
        url = f"{API_BASE_URL}/games/{game_id}"
        params = {'key': RAWG_API_KEY}
        
        # Try cache first
        if use_cache:
            cached_data = cache.get(url, params)
            if cached_data:
                print(f"Using cached data for game {game_id}")
                return cached_data
        
        # Fetch from API
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                # Cache the response
                cache.set(url, params, data)
                return data
            return None
        except Exception as e:
            print(f"API Error: {e}")
            return None
    
    @staticmethod
    def search_games(query, page_size=15, use_cache=True):
        """Search games with caching"""
        url = f"{API_BASE_URL}/games"
        params = {
            'key': RAWG_API_KEY,
            'search': query,
            'page_size': page_size
        }
        
        # Try cache first
        if use_cache:
            cached_data = cache.get(url, params)
            if cached_data:
                print(f"Using cached search results for '{query}'")
                return cached_data
        
        # Fetch from API
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                # Cache the response
                cache.set(url, params, data)
                return data
            return None
        except Exception as e:
            print(f"API Error: {e}")
            return None


# Global API helper instance
api = APIHelper()
