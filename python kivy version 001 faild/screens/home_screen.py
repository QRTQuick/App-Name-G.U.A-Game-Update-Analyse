from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.appbar import MDTopAppBar
from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from utils.api_helper import api


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
            data = api.get_games(params={"page_size": 10, "ordering": "-added"})
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
        
        # Rating with icon
        rating_box = MDBoxLayout(orientation='horizontal', spacing=dp(3), size_hint_y=None, height=dp(20))
        star_icon = MDIconButton(icon="star", disabled=True, size_hint=(None, None), size=(dp(16), dp(16)))
        rating_label = MDLabel(text=f"{game.get('rating', 'N/A')}/5", font_size="13sp", size_hint_y=None, height=dp(20))
        rating_box.add_widget(star_icon)
        rating_box.add_widget(rating_label)
        
        info_layout.add_widget(name)
        info_layout.add_widget(rating_box)
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
