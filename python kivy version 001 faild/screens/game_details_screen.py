from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.appbar import MDTopAppBar
from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from kivy.clock import Clock
from utils.api_helper import api
from utils.storage import storage


class GameDetailsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_id = None
        self.game_data = None
        self.favorite_btn = None
        
    def load_game_details(self, game_id):
        self.game_id = game_id
        self.clear_widgets()
        
        layout = MDBoxLayout(orientation='vertical')
        
        toolbar = MDTopAppBar()
        toolbar.headline_text = "Game Details"
        toolbar.type = "small"
        back_btn = MDIconButton(icon="arrow-left", on_release=lambda x: self.go_back())
        toolbar.add_widget(back_btn)
        
        # Favorite button
        is_fav = storage.is_favorite(game_id)
        self.favorite_btn = MDIconButton(
            icon="heart" if is_fav else "heart-outline",
            on_release=lambda x: self.toggle_favorite()
        )
        toolbar.add_widget(self.favorite_btn)
        
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
            game = api.get_game_details(self.game_id)
            if game:
                self.game_data = game
                
                # Save to history
                storage.add_to_history(self.game_id, {
                    'name': game.get('name', 'Unknown'),
                    'image': game.get('background_image'),
                    'rating': game.get('rating', 'N/A')
                })
                
                content.clear_widgets()
                
                if game.get('background_image'):
                    img = AsyncImage(source=game['background_image'], size_hint_y=None, height=dp(220))
                    content.add_widget(img)
                
                info_card = MDCard(orientation='vertical', size_hint_y=None, padding=dp(15), spacing=dp(8), elevation=2, radius=[10, 10, 10, 10])
                info_card.bind(minimum_height=info_card.setter('height'))
                
                name = MDLabel(text=game.get('name', 'Unknown'), font_size="22sp", bold=True, size_hint_y=None, height=dp(35))
                
                # Rating with icon
                rating_box = MDBoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(25))
                star_icon = MDIconButton(icon="star", disabled=True, size_hint=(None, None), size=(dp(20), dp(20)))
                rating_label = MDLabel(text=f"{game.get('rating', 'N/A')}/5 ({game.get('ratings_count', 0)} ratings)", font_size="15sp", size_hint_y=None, height=dp(25))
                rating_box.add_widget(star_icon)
                rating_box.add_widget(rating_label)
                
                # Released date with icon
                released_box = MDBoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(25))
                calendar_icon = MDIconButton(icon="calendar", disabled=True, size_hint=(None, None), size=(dp(20), dp(20)))
                released_label = MDLabel(text=game.get('released', 'TBA'), font_size="14sp", size_hint_y=None, height=dp(25))
                released_box.add_widget(calendar_icon)
                released_box.add_widget(released_label)
                
                info_card.add_widget(name)
                info_card.add_widget(rating_box)
                info_card.add_widget(released_box)
                
                platforms = [p['platform']['name'] for p in game.get('platforms', [])]
                if platforms:
                    plat_box = MDBoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None)
                    plat_box.bind(minimum_height=plat_box.setter('height'))
                    gamepad_icon = MDIconButton(icon="gamepad-variant", disabled=True, size_hint=(None, None), size=(dp(20), dp(20)))
                    plat_label = MDLabel(text=', '.join(platforms[:4]), font_size="13sp", size_hint_y=None)
                    plat_label.bind(texture_size=plat_label.setter('size'))
                    plat_box.add_widget(gamepad_icon)
                    plat_box.add_widget(plat_label)
                    info_card.add_widget(plat_box)
                
                genres = [g['name'] for g in game.get('genres', [])]
                if genres:
                    genre_box = MDBoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(25))
                    tag_icon = MDIconButton(icon="tag-multiple", disabled=True, size_hint=(None, None), size=(dp(20), dp(20)))
                    genre_label = MDLabel(text=', '.join(genres), font_size="13sp", size_hint_y=None, height=dp(25))
                    genre_box.add_widget(tag_icon)
                    genre_box.add_widget(genre_label)
                    info_card.add_widget(genre_box)
                
                content.add_widget(info_card)
                
                desc = game.get('description_raw', 'No description')
                if desc:
                    desc_card = MDCard(orientation='vertical', size_hint_y=None, padding=dp(15), elevation=2, radius=[10, 10, 10, 10])
                    desc_card.bind(minimum_height=desc_card.setter('height'))
                    
                    # Title with icon
                    desc_title_box = MDBoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(30))
                    info_icon = MDIconButton(icon="information", disabled=True, size_hint=(None, None), size=(dp(20), dp(20)))
                    desc_title_label = MDLabel(text="Description", font_size="16sp", bold=True, size_hint_y=None, height=dp(30))
                    desc_title_box.add_widget(info_icon)
                    desc_title_box.add_widget(desc_title_label)
                    
                    desc_text = MDLabel(text=desc[:400] + "...", font_size="13sp", size_hint_y=None)
                    desc_text.bind(texture_size=desc_text.setter('size'))
                    
                    desc_card.add_widget(desc_title_box)
                    desc_card.add_widget(desc_text)
                    content.add_widget(desc_card)
                
        except Exception as e:
            content.clear_widgets()
            error = MDLabel(text=f"Error: {e}", halign="center", size_hint_y=None, height=dp(50))
            content.add_widget(error)
    
    def go_back(self):
        app = MDApp.get_running_app()
        app.sm.current = 'home'

    
    def toggle_favorite(self):
        if not self.game_data:
            return
        
        if storage.is_favorite(self.game_id):
            storage.remove_favorite(self.game_id)
            self.favorite_btn.icon = "heart-outline"
        else:
            storage.add_favorite(self.game_id, {
                'name': self.game_data.get('name', 'Unknown'),
                'image': self.game_data.get('background_image'),
                'rating': self.game_data.get('rating', 'N/A')
            })
            self.favorite_btn.icon = "heart"
