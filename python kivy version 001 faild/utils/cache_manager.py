import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import hashlib


class CacheManager:
    """Manage API response caching with expiration"""
    
    def __init__(self, cache_days=2):
        self.cache_dir = Path.home() / '.gua_app' / 'cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_days = cache_days
        self.cache_duration = timedelta(days=cache_days)
    
    def _get_cache_key(self, url, params=None):
        """Generate unique cache key from URL and params"""
        cache_string = url
        if params:
            # Sort params for consistent keys
            sorted_params = sorted(params.items())
            cache_string += str(sorted_params)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def _get_cache_file(self, cache_key):
        """Get cache file path"""
        return self.cache_dir / f"{cache_key}.json"
    
    def get(self, url, params=None):
        """Get cached data if valid"""
        cache_key = self._get_cache_key(url, params)
        cache_file = self._get_cache_file(cache_key)
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
            
            # Check expiration
            cached_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.now() - cached_time > self.cache_duration:
                # Cache expired, delete it
                os.remove(cache_file)
                return None
            
            return cache_data['data']
        except Exception as e:
            print(f"Cache read error: {e}")
            return None
    
    def set(self, url, params, data):
        """Save data to cache"""
        cache_key = self._get_cache_key(url, params)
        cache_file = self._get_cache_file(cache_key)
        
        try:
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'url': url,
                'params': params,
                'data': data
            }
            
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
            
            return True
        except Exception as e:
            print(f"Cache write error: {e}")
            return False
    
    def clear_expired(self):
        """Clear all expired cache files"""
        if not self.cache_dir.exists():
            return 0
        
        cleared = 0
        for cache_file in self.cache_dir.glob('*.json'):
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                
                cached_time = datetime.fromisoformat(cache_data['timestamp'])
                if datetime.now() - cached_time > self.cache_duration:
                    os.remove(cache_file)
                    cleared += 1
            except Exception as e:
                print(f"Error clearing cache: {e}")
        
        return cleared
    
    def clear_all(self):
        """Clear all cache files"""
        if not self.cache_dir.exists():
            return 0
        
        cleared = 0
        for cache_file in self.cache_dir.glob('*.json'):
            try:
                os.remove(cache_file)
                cleared += 1
            except Exception as e:
                print(f"Error clearing cache: {e}")
        
        return cleared
    
    def get_cache_size(self):
        """Get total cache size in MB"""
        if not self.cache_dir.exists():
            return 0
        
        total_size = 0
        for cache_file in self.cache_dir.glob('*.json'):
            total_size += cache_file.stat().st_size
        
        return total_size / (1024 * 1024)  # Convert to MB
    
    def get_cache_info(self):
        """Get cache statistics"""
        if not self.cache_dir.exists():
            return {'count': 0, 'size_mb': 0, 'expired': 0}
        
        total = 0
        expired = 0
        
        for cache_file in self.cache_dir.glob('*.json'):
            total += 1
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                
                cached_time = datetime.fromisoformat(cache_data['timestamp'])
                if datetime.now() - cached_time > self.cache_duration:
                    expired += 1
            except:
                pass
        
        return {
            'count': total,
            'size_mb': round(self.get_cache_size(), 2),
            'expired': expired
        }


# Global cache instance
cache = CacheManager(cache_days=2)
