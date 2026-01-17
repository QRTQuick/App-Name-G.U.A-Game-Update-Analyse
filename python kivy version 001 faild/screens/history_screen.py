from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.appbar import MDTopAppBar
from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from utils.storage import storage


class HistoryScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        layout = MDBoxLayout(orientation='vertical')
        
        toolbar = MDTopAppBar()
        toolbar.headline_text = "Recently Viewed"
        toolbar.type = "small"
        back_btn = MDIconButton(icon="arrow-left", on_release=lambda x: self.go_back())
        toolbar.add_widget(back_btn)
        layout.add_widget(toolbar)
        
        history = storage.get_history()
        
        if not history:
            empty_box = MDBoxLayout(orientation='vertical', padding=dp(40), spacing=dp(20))
            empty_box.add_widget(MDBoxLayout())
            icon = MDIconButton(icon="history")
            icon_box = MDBoxLayout(size_hint_y=None, height=dp(80))
            icon_box.add_widget(MDBoxLayout())
            icon_box.add_widget(icon)
            icon_box.add_widget(MDBoxLayout())
            empty_box.add_widget(icon_box)
            empty_box.add_widget(MDLabel(text="No history yet", halign="center", font_size="18sp", bold=True, size_hint_y=None, height=dp(30)))
            empty_box.add_widget(MDLabel(text="Games you view will appear here", halign="center", font_size="14sp", size_hint_y=None, height=dp(40)))
            empty_box.add_widget(MDBoxLayout())
            layout.add_widget(empty_box)
        else:
            scroll = MDScrollView()
            grid = MDGridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=dp(10))
            grid.bind(minimum_height=grid.setter('height'))
            
            for game in reversed(history):
                card = self.create_game_card(game)
                grid.add_widget(card)
            
            scroll.add_widget(grid)
            layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def create_game_card(self, game):
        card = MDCard(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(120),
            padding=dp(8),
            spacing=dp(10),
            elevation=2,
            radius=[10, 10, 10, 10]
        )
        
        if game.get('image'):
            img = AsyncImage(source=game['image'], size_hint_x=0.3)
            card.add_widget(img)
        
        info_layout = MDBoxLayout(orientation='vertical', size_hint_x=0.7, spacing=dp(5))
        name = MDLabel(text=game.get('name', 'Unknown')[:30], font_size="15sp", bold=True, size_hint_y=None, height=dp(30))
        
        # Rating with icon
        rating_box = MDBoxLayout(orientation='horizontal', spacing=dp(3), size_hint_y=None, height=dp(20))
        star_icon = MDIconButton(icon="star", disabled=True, size_hint=(None, None), size=(dp(14), dp(14)))
        rating_label = MDLabel(text=f"{game.get('rating', 'N/A')}/5", font_size="12sp", size_hint_y=None, height=dp(20))
        rating_box.add_widget(star_icon)
        rating_box.add_widget(rating_label)
        
        btn = MDButton(style="text", size_hint_y=None, height=dp(40), on_release=lambda x: self.show_game_details(game['id']))
        btn.add_widget(MDButtonText(text="View Again"))
        
        info_layout.add_widget(name)
        info_layout.add_widget(rating_box)
        info_layout.add_widget(btn)
        card.add_widget(info_layout)
        
        return card
    
    def show_game_details(self, game_id):
        app = MDApp.get_running_app()
        app.show_game_details(game_id)
    
    def go_back(self):
        app = MDApp.get_running_app()
        app.switch_screen('profile')
