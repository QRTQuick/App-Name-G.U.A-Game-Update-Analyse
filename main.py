from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.appbar import MDTopAppBar
from kivymd.uix.divider import MDDivider
from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window
import requests
from config import RAWG_API_KEY, API_BASE_URL

# Mobile window size
Window.size = (360, 640)


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        toolbar = MDTopAppBar()
        toolbar.headline_text = "G.U.A"
        toolbar.type = "small"
        layout.add_widget(toolbar)
        
        scroll = MDScrollView()
        self.games_grid = MDGridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=dp(10))
        self.games_grid.bind(minimum_height=self.games_grid.setter('height'))
        scroll.add_widget(self.games_grid)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
        self.load_trending_games()
    
    def load_trending_games(self):
        try:
            response = requests.get(
                f"{API_BASE_URL}/games",
                params={"key": RAWG_API_KEY, "page_size": 10, "ordering": "-added"}
            )
            if response.status_code == 200:
                games = response.json().get('results', [])
                for game in games:
                    self.add_game_card(game)
        except Exception as e:
            print(f"Error: {e}")
    
    def add_game_card(self, game):
        card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(320),
            padding=dp(8),
            spacing=dp(8),
            elevation=3,
            radius=[15, 15, 15, 15]
        )
        
        if game.get('background_image'):
            img = AsyncImage(source=game['background_image'], size_hint_y=0.65)
            card.add_widget(img)
        
        info_layout = MDBoxLayout(orientation='vertical', size_hint_y=0.25, spacing=dp(3), padding=[dp(5), 0])
        name = MDLabel(text=game.get('name', 'Unknown')[:40], font_size="16sp", bold=True, size_hint_y=None, height=dp(25))
        rating = MDLabel(text=f"⭐ {game.get('rating', 'N/A')}/5", font_size="13sp", size_hint_y=None, height=dp(20))
        info_layout.add_widget(name)
        info_layout.add_widget(rating)
        card.add_widget(info_layout)
        
        btn_layout = MDBoxLayout(size_hint_y=0.1, padding=[dp(5), 0])
        btn = MDButton(style="text", on_release=lambda x: self.show_game_details(game['id']))
        btn.add_widget(MDButtonText(text="View Details"))
        btn_layout.add_widget(btn)
        card.add_widget(btn_layout)
        
        self.games_grid.add_widget(card)
    
    def show_game_details(self, game_id):
        app = MDApp.get_running_app()
        app.show_game_details(game_id)


class SearchScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        toolbar = MDTopAppBar()
        toolbar.headline_text = "Search Games"
        toolbar.type = "small"
        layout.add_widget(toolbar)
        
        content = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        self.search_field = MDTextField(mode="outlined", size_hint_y=None, height=dp(56))
        self.search_field.hint_text = "Search for games..."
        self.search_field.bind(text=self.on_search_text)
        content.add_widget(self.search_field)
        
        scroll = MDScrollView()
        self.results_grid = MDGridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=dp(5))
        self.results_grid.bind(minimum_height=self.results_grid.setter('height'))
        scroll.add_widget(self.results_grid)
        content.add_widget(scroll)
        
        layout.add_widget(content)
        self.add_widget(layout)
    
    def on_search_text(self, instance, value):
        if len(value) >= 3:
            Clock.unschedule(self.search_games)
            Clock.schedule_once(lambda dt: self.search_games(value), 0.5)
    
    def search_games(self, query):
        self.results_grid.clear_widgets()
        try:
            response = requests.get(
                f"{API_BASE_URL}/games",
                params={"key": RAWG_API_KEY, "search": query, "page_size": 15}
            )
            if response.status_code == 200:
                games = response.json().get('results', [])
                if games:
                    for game in games:
                        self.add_game_card(game)
                else:
                    self.results_grid.add_widget(MDLabel(text="No games found", halign="center", size_hint_y=None, height=dp(50)))
        except Exception as e:
            print(f"Error: {e}")
    
    def add_game_card(self, game):
        card = MDCard(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(120),
            padding=dp(8),
            spacing=dp(10),
            elevation=2,
            radius=[10, 10, 10, 10]
        )
        
        if game.get('background_image'):
            img = AsyncImage(source=game['background_image'], size_hint_x=0.3)
            card.add_widget(img)
        
        info_layout = MDBoxLayout(orientation='vertical', size_hint_x=0.7, spacing=dp(5))
        name = MDLabel(text=game.get('name', 'Unknown')[:35], font_size="15sp", bold=True, size_hint_y=None, height=dp(30))
        rating = MDLabel(text=f"⭐ {game.get('rating', 'N/A')}/5", font_size="12sp", size_hint_y=None, height=dp(20))
        
        btn = MDButton(style="text", size_hint_y=None, height=dp(40), on_release=lambda x: self.show_game_details(game['id']))
        btn.add_widget(MDButtonText(text="Details"))
        
        info_layout.add_widget(name)
        info_layout.add_widget(rating)
        info_layout.add_widget(btn)
        card.add_widget(info_layout)
        
        self.results_grid.add_widget(card)
    
    def show_game_details(self, game_id):
        app = MDApp.get_running_app()
        app.show_game_details(game_id)


class TrendingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        toolbar = MDTopAppBar()
        toolbar.headline_text = "Trending"
        toolbar.type = "small"
        layout.add_widget(toolbar)
        
        scroll = MDScrollView()
        self.games_grid = MDGridLayout(cols=2, spacing=dp(10), size_hint_y=None, padding=dp(10))
        self.games_grid.bind(minimum_height=self.games_grid.setter('height'))
        scroll.add_widget(self.games_grid)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
        self.load_trending_games()
    
    def load_trending_games(self):
        try:
            response = requests.get(
                f"{API_BASE_URL}/games",
                params={"key": RAWG_API_KEY, "page_size": 20, "ordering": "-rating"}
            )
            if response.status_code == 200:
                games = response.json().get('results', [])
                for game in games:
                    self.add_game_card(game)
        except Exception as e:
            print(f"Error: {e}")
    
    def add_game_card(self, game):
        card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(220),
            padding=dp(5),
            spacing=dp(5),
            elevation=2,
            radius=[10, 10, 10, 10],
            on_release=lambda x: self.show_game_details(game['id'])
        )
        
        if game.get('background_image'):
            img = AsyncImage(source=game['background_image'], size_hint_y=0.7)
            card.add_widget(img)
        
        info = MDBoxLayout(orientation='vertical', size_hint_y=0.3, padding=[dp(3), 0])
        name = MDLabel(text=game.get('name', 'Unknown')[:20], font_size="13sp", bold=True, size_hint_y=None, height=dp(35))
        rating = MDLabel(text=f"⭐ {game.get('rating', 'N/A')}", font_size="11sp", size_hint_y=None, height=dp(20))
        info.add_widget(name)
        info.add_widget(rating)
        card.add_widget(info)
        
        self.games_grid.add_widget(card)
    
    def show_game_details(self, game_id):
        app = MDApp.get_running_app()
        app.show_game_details(game_id)


class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        toolbar = MDTopAppBar()
        toolbar.headline_text = "Profile"
        toolbar.type = "small"
        layout.add_widget(toolbar)
        
        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', spacing=dp(20), size_hint_y=None, padding=dp(20))
        content.bind(minimum_height=content.setter('height'))
        
        # Profile header
        header = MDBoxLayout(orientation='vertical', size_hint_y=None, height=dp(150), spacing=dp(10))
        avatar_box = MDBoxLayout(size_hint_y=None, height=dp(80))
        avatar = MDIconButton(icon="account-circle")
        avatar_box.add_widget(MDBoxLayout())
        avatar_box.add_widget(avatar)
        avatar_box.add_widget(MDBoxLayout())
        
        name = MDLabel(text="Gamer", halign="center", font_size="20sp", bold=True, size_hint_y=None, height=dp(30))
        email = MDLabel(text="gamer@gua.app", halign="center", font_size="14sp", size_hint_y=None, height=dp(25))
        
        header.add_widget(avatar_box)
        header.add_widget(name)
        header.add_widget(email)
        content.add_widget(header)
        content.add_widget(MDDivider())
        
        # Stats card
        stats_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            padding=dp(15),
            elevation=2,
            radius=[10, 10, 10, 10]
        )
        
        stats_title = MDLabel(text="Your Stats", font_size="16sp", bold=True, size_hint_y=None, height=dp(30))
        stats_grid = MDGridLayout(cols=3, size_hint_y=None, height=dp(50), spacing=dp(10))
        
        for label, value in [("Games", "127"), ("Reviews", "45"), ("Favorites", "23")]:
            stat_box = MDBoxLayout(orientation='vertical')
            stat_box.add_widget(MDLabel(text=value, halign="center", font_size="18sp", bold=True))
            stat_box.add_widget(MDLabel(text=label, halign="center", font_size="12sp"))
            stats_grid.add_widget(stat_box)
        
        stats_card.add_widget(stats_title)
        stats_card.add_widget(stats_grid)
        content.add_widget(stats_card)
        
        # Menu items
        for icon, text in [("account-edit", "Edit Profile"), ("heart", "Favorites"), ("history", "Recently Viewed"), ("bell", "Notifications")]:
            item = MDCard(size_hint_y=None, height=dp(60), padding=dp(10), elevation=1, radius=[8, 8, 8, 8])
            item_layout = MDBoxLayout(spacing=dp(15))
            item_layout.add_widget(MDIconButton(icon=icon))
            item_layout.add_widget(MDLabel(text=text, font_size="15sp"))
            item.add_widget(item_layout)
            content.add_widget(item)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)


class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        toolbar = MDTopAppBar()
        toolbar.headline_text = "Settings"
        toolbar.type = "small"
        layout.add_widget(toolbar)
        
        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, padding=dp(15))
        content.bind(minimum_height=content.setter('height'))
        
        sections = [
            ("General", [("theme", "Dark Mode"), ("translate", "Language"), ("bell-outline", "Notifications")]),
            ("Content", [("filter", "Content Filter"), ("download", "Auto-Download Images"), ("quality-high", "Image Quality")]),
            ("Account", [("lock", "Privacy"), ("shield-check", "Security"), ("logout", "Sign Out")]),
            ("About", [("information", "About G.U.A"), ("file-document", "Terms of Service"), ("help-circle", "Help & Support")])
        ]
        
        for section_title, items in sections:
            section_label = MDLabel(text=section_title, font_size="14sp", bold=True, size_hint_y=None, height=dp(30))
            content.add_widget(section_label)
            
            for icon, text in items:
                item = MDCard(size_hint_y=None, height=dp(55), padding=dp(10), elevation=1, radius=[8, 8, 8, 8])
                item_layout = MDBoxLayout(spacing=dp(15))
                item_layout.add_widget(MDIconButton(icon=icon))
                item_layout.add_widget(MDLabel(text=text, font_size="14sp"))
                item_layout.add_widget(MDIconButton(icon="chevron-right"))
                item.add_widget(item_layout)
                content.add_widget(item)
            
            content.add_widget(MDBoxLayout(size_hint_y=None, height=dp(10)))
        
        version = MDLabel(text="G.U.A v1.0.0", halign="center", font_size="12sp", size_hint_y=None, height=dp(40))
        content.add_widget(version)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)


class GameDetailsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_id = None
        
    def load_game_details(self, game_id):
        self.game_id = game_id
        self.clear_widgets()
        
        layout = MDBoxLayout(orientation='vertical')
        
        toolbar = MDTopAppBar()
        toolbar.headline_text = "Game Details"
        toolbar.type = "small"
        back_btn = MDIconButton(icon="arrow-left", on_release=lambda x: self.go_back())
        toolbar.add_widget(back_btn)
        layout.add_widget(toolbar)
        
        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, padding=dp(10))
        content.bind(minimum_height=content.setter('height'))
        
        loading = MDLabel(text="Loading...", halign="center", size_hint_y=None, height=dp(50))
        content.add_widget(loading)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)
        
        Clock.schedule_once(lambda dt: self.fetch_details(content), 0.1)
    
    def fetch_details(self, content):
        try:
            response = requests.get(f"{API_BASE_URL}/games/{self.game_id}", params={"key": RAWG_API_KEY})
            if response.status_code == 200:
                game = response.json()
                content.clear_widgets()
                
                if game.get('background_image'):
                    img = AsyncImage(source=game['background_image'], size_hint_y=None, height=dp(220))
                    content.add_widget(img)
                
                info_card = MDCard(orientation='vertical', size_hint_y=None, padding=dp(15), spacing=dp(8), elevation=2, radius=[10, 10, 10, 10])
                info_card.bind(minimum_height=info_card.setter('height'))
                
                name = MDLabel(text=game.get('name', 'Unknown'), font_size="22sp", bold=True, size_hint_y=None, height=dp(35))
                rating = MDLabel(text=f"⭐ {game.get('rating', 'N/A')}/5 ({game.get('ratings_count', 0)} ratings)", font_size="15sp", size_hint_y=None, height=dp(25))
                released = MDLabel(text=f"📅 {game.get('released', 'TBA')}", font_size="14sp", size_hint_y=None, height=dp(25))
                
                info_card.add_widget(name)
                info_card.add_widget(rating)
                info_card.add_widget(released)
                
                platforms = [p['platform']['name'] for p in game.get('platforms', [])]
                if platforms:
                    plat = MDLabel(text=f"🎮 {', '.join(platforms[:4])}", font_size="13sp", size_hint_y=None)
                    plat.bind(texture_size=plat.setter('size'))
                    info_card.add_widget(plat)
                
                genres = [g['name'] for g in game.get('genres', [])]
                if genres:
                    genre = MDLabel(text=f"🎯 {', '.join(genres)}", font_size="13sp", size_hint_y=None, height=dp(25))
                    info_card.add_widget(genre)
                
                content.add_widget(info_card)
                
                desc = game.get('description_raw', 'No description')
                if desc:
                    desc_card = MDCard(orientation='vertical', size_hint_y=None, padding=dp(15), elevation=2, radius=[10, 10, 10, 10])
                    desc_card.bind(minimum_height=desc_card.setter('height'))
                    
                    desc_title = MDLabel(text="Description", font_size="16sp", bold=True, size_hint_y=None, height=dp(30))
                    desc_text = MDLabel(text=desc[:400] + "...", font_size="13sp", size_hint_y=None)
                    desc_text.bind(texture_size=desc_text.setter('size'))
                    
                    desc_card.add_widget(desc_title)
                    desc_card.add_widget(desc_text)
                    content.add_widget(desc_card)
                
        except Exception as e:
            content.clear_widgets()
            error = MDLabel(text=f"Error: {e}", halign="center", size_hint_y=None, height=dp(50))
            content.add_widget(error)
    
    def go_back(self):
        app = MDApp.get_running_app()
        app.sm.current = 'home'


class GUAApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        self.sm = MDScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(SearchScreen(name='search'))
        self.sm.add_widget(TrendingScreen(name='trending'))
        self.sm.add_widget(ProfileScreen(name='profile'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(GameDetailsScreen(name='details'))
        
        main_layout.add_widget(self.sm)
        
        # Bottom navigation
        nav_bar = MDBoxLayout(size_hint_y=None, height=dp(65), padding=[dp(10), dp(5)])
        
        buttons = [
            ("home", "Home", 'home'),
            ("magnify", "Search", 'search'),
            ("fire", "Trending", 'trending'),
            ("account", "Profile", 'profile'),
            ("cog", "Settings", 'settings'),
        ]
        
        for icon, label, screen in buttons:
            btn_layout = MDBoxLayout(orientation='vertical', spacing=dp(2))
            btn = MDIconButton(icon=icon, on_release=lambda x, s=screen: self.switch_screen(s))
            lbl = MDLabel(text=label, halign="center", font_size="10sp", size_hint_y=None, height=dp(15))
            btn_layout.add_widget(btn)
            btn_layout.add_widget(lbl)
            nav_bar.add_widget(btn_layout)
        
        main_layout.add_widget(nav_bar)
        return main_layout
    
    def switch_screen(self, screen_name):
        self.sm.current = screen_name
    
    def show_game_details(self, game_id):
        details_screen = self.sm.get_screen('details')
        details_screen.load_game_details(game_id)
        self.sm.current = 'details'


if __name__ == '__main__':
    GUAApp().run()
