from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.appbar import MDTopAppBar
from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from utils.api_helper import api


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
        
        # Search input row
        search_row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(56), spacing=dp(10))
        
        self.search_field = MDTextField(mode="outlined", size_hint_x=0.75)
        self.search_field.hint_text = "Search for games..."
        search_row.add_widget(self.search_field)
        
        # Search button
        search_btn = MDButton(style="filled", size_hint=(None, None), size=(dp(80), dp(50)), on_release=self.on_search_click)
        search_btn.add_widget(MDButtonText(text="Search"))
        search_row.add_widget(search_btn)
        
        content.add_widget(search_row)
        
        # Results area
        scroll = MDScrollView()
        self.results_grid = MDGridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=dp(5))
        self.results_grid.bind(minimum_height=self.results_grid.setter('height'))
        
        # Initial message
        self.initial_message = MDLabel(
            text="Enter a game name and click Search",
            halign="center",
            font_size="14sp",
            size_hint_y=None,
            height=dp(100)
        )
        self.results_grid.add_widget(self.initial_message)
        
        scroll.add_widget(self.results_grid)
        content.add_widget(scroll)
        
        layout.add_widget(content)
        self.add_widget(layout)
    
    def on_search_click(self, instance):
        """Search when button is clicked"""
        query = self.search_field.text.strip()
        if len(query) >= 2:
            self.search_games(query)
        else:
            self.results_grid.clear_widgets()
            error_msg = MDLabel(
                text="Please enter at least 2 characters",
                halign="center",
                theme_text_color="Error",
                size_hint_y=None,
                height=dp(50)
            )
            self.results_grid.add_widget(error_msg)
    
    def search_games(self, query):
        self.results_grid.clear_widgets()
        
        # Show loading
        loading = MDLabel(text="Searching...", halign="center", size_hint_y=None, height=dp(50))
        self.results_grid.add_widget(loading)
        
        try:
            data = api.search_games(query, page_size=15)
            if data:
                self.results_grid.clear_widgets()
                games = data.get('results', [])
                if games:
                    for game in games:
                        self.add_game_card(game)
                else:
                    self.results_grid.add_widget(MDLabel(text="No games found", halign="center", size_hint_y=None, height=dp(50)))
            else:
                self.results_grid.clear_widgets()
                self.results_grid.add_widget(MDLabel(text="Error loading results", halign="center", theme_text_color="Error", size_hint_y=None, height=dp(50)))
        except Exception as e:
            self.results_grid.clear_widgets()
            error = MDLabel(text=f"Error: {e}", halign="center", theme_text_color="Error", size_hint_y=None, height=dp(50))
            self.results_grid.add_widget(error)
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
        
        # Rating with icon
        rating_box = MDBoxLayout(orientation='horizontal', spacing=dp(3), size_hint_y=None, height=dp(20))
        star_icon = MDIconButton(icon="star", disabled=True, size_hint=(None, None), size=(dp(14), dp(14)))
        rating_label = MDLabel(text=f"{game.get('rating', 'N/A')}/5", font_size="12sp", size_hint_y=None, height=dp(20))
        rating_box.add_widget(star_icon)
        rating_box.add_widget(rating_label)
        
        btn = MDButton(style="text", size_hint_y=None, height=dp(40), on_release=lambda x: self.show_game_details(game['id']))
        btn.add_widget(MDButtonText(text="Details"))
        
        info_layout.add_widget(name)
        info_layout.add_widget(rating_box)
        info_layout.add_widget(btn)
        card.add_widget(info_layout)
        
        self.results_grid.add_widget(card)
    
    def show_game_details(self, game_id):
        app = MDApp.get_running_app()
        app.show_game_details(game_id)
