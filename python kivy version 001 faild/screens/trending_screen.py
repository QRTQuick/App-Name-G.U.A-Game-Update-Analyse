from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.appbar import MDTopAppBar
from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from utils.api_helper import api


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
            data = api.get_games(params={"page_size": 20, "ordering": "-rating"})
            if data:
                games = data.get('results', [])
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
        
        # Rating with icon
        rating_box = MDBoxLayout(orientation='horizontal', spacing=dp(2), size_hint_y=None, height=dp(20))
        star_icon = MDIconButton(icon="star", disabled=True, size_hint=(None, None), size=(dp(12), dp(12)))
        rating_label = MDLabel(text=f"{game.get('rating', 'N/A')}", font_size="11sp", size_hint_y=None, height=dp(20))
        rating_box.add_widget(star_icon)
        rating_box.add_widget(rating_label)
        
        info.add_widget(name)
        info.add_widget(rating_box)
        card.add_widget(info)
        
        self.games_grid.add_widget(card)
    
    def show_game_details(self, game_id):
        app = MDApp.get_running_app()
        app.show_game_details(game_id)
