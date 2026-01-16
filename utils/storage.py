import json
import os
from pathlib import Path


class UserStorage:
    """Handle user data storage locally"""
    
    def __init__(self):
        # Use app data directory
        self.data_dir = Path.home() / '.gua_app'
        self.data_dir.mkdir(exist_ok=True)
        self.user_file = self.data_dir / 'user_data.json'
        self.favorites_file = self.data_dir / 'favorites.json'
        self.history_file = self.data_dir / 'history.json'
    
    def save_user(self, user_data):
        """Save user login data"""
        with open(self.user_file, 'w') as f:
            json.dump(user_data, f)
    
    def get_user(self):
        """Get logged in user data"""
        if self.user_file.exists():
            with open(self.user_file, 'r') as f:
                return json.load(f)
        return None
    
    def logout_user(self):
        """Remove user data (logout)"""
        if self.user_file.exists():
            os.remove(self.user_file)
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return self.user_file.exists()
    
    def add_favorite(self, game_id, game_data):
        """Add game to favorites"""
        favorites = self.get_favorites()
        favorites[str(game_id)] = game_data
        with open(self.favorites_file, 'w') as f:
            json.dump(favorites, f)
    
    def remove_favorite(self, game_id):
        """Remove game from favorites"""
        favorites = self.get_favorites()
        if str(game_id) in favorites:
            del favorites[str(game_id)]
            with open(self.favorites_file, 'w') as f:
                json.dump(favorites, f)
    
    def get_favorites(self):
        """Get all favorite games"""
        if self.favorites_file.exists():
            with open(self.favorites_file, 'r') as f:
                return json.load(f)
        return {}
    
    def is_favorite(self, game_id):
        """Check if game is in favorites"""
        favorites = self.get_favorites()
        return str(game_id) in favorites
    
    def add_to_history(self, game_id, game_data):
        """Add game to recently viewed"""
        history = self.get_history()
        # Keep only last 50 items
        if len(history) >= 50:
            history.pop(0)
        # Remove if already exists and add to end
        history = [h for h in history if h['id'] != game_id]
        history.append({'id': game_id, **game_data})
        with open(self.history_file, 'w') as f:
            json.dump(history, f)
    
    def get_history(self):
        """Get recently viewed games"""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []
    
    def clear_history(self):
        """Clear viewing history"""
        if self.history_file.exists():
            os.remove(self.history_file)
    
    def get_stats(self):
        """Get user statistics"""
        favorites = self.get_favorites()
        history = self.get_history()
        return {
            'favorites': len(favorites),
            'viewed': len(history),
            'reviews': 0  # Placeholder for future feature
        }


# Global storage instance
storage = UserStorage()
