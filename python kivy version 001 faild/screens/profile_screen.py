from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.appbar import MDTopAppBar
from kivymd.uix.divider import MDDivider
from kivy.metrics import dp
from utils.storage import storage


class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        user = storage.get_user()
        
        # If not logged in, show login prompt
        if not user:
            self.show_login_prompt()
            return
        
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
        
        name = MDLabel(text=user.get('username', 'User'), halign="center", font_size="20sp", bold=True, size_hint_y=None, height=dp(30))
        email = MDLabel(text=user.get('email', ''), halign="center", font_size="14sp", size_hint_y=None, height=dp(25))
        
        header.add_widget(avatar_box)
        header.add_widget(name)
        header.add_widget(email)
        content.add_widget(header)
        content.add_widget(MDDivider())
        
        # Stats card
        stats = storage.get_stats()
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
        
        for label, value in [("Viewed", str(stats['viewed'])), ("Favorites", str(stats['favorites'])), ("Reviews", str(stats['reviews']))]:
            stat_box = MDBoxLayout(orientation='vertical')
            stat_box.add_widget(MDLabel(text=value, halign="center", font_size="18sp", bold=True))
            stat_box.add_widget(MDLabel(text=label, halign="center", font_size="12sp"))
            stats_grid.add_widget(stat_box)
        
        stats_card.add_widget(stats_title)
        stats_card.add_widget(stats_grid)
        content.add_widget(stats_card)
        
        # Menu items
        menu_items = [
            ("account-edit", "Edit Profile", self.edit_profile),
            ("heart", "Favorites", self.show_favorites),
            ("history", "Recently Viewed", self.show_history),
            ("bell", "Notifications", self.show_notifications),
            ("cog", "Settings", self.show_settings),
        ]
        
        for icon, text, callback in menu_items:
            item = MDCard(size_hint_y=None, height=dp(60), padding=dp(10), elevation=1, radius=[8, 8, 8, 8])
            item_layout = MDBoxLayout(spacing=dp(15))
            item_layout.add_widget(MDIconButton(icon=icon, on_release=callback))
            item_layout.add_widget(MDLabel(text=text, font_size="15sp"))
            item_layout.add_widget(MDIconButton(icon="chevron-right", on_release=callback))
            item.add_widget(item_layout)
            content.add_widget(item)
        
        # Logout button
        if user.get('logged_in', False):
            logout_btn = MDButton(style="outlined", size_hint_y=None, height=dp(50), on_release=self.logout)
            logout_btn.add_widget(MDButtonText(text="Logout"))
            content.add_widget(logout_btn)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)
    
    def show_login_prompt(self):
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        layout.add_widget(MDBoxLayout(size_hint_y=0.3))
        
        icon_box = MDBoxLayout(size_hint_y=None, height=dp(80))
        icon = MDIconButton(icon="account-circle")
        icon_box.add_widget(MDBoxLayout())
        icon_box.add_widget(icon)
        icon_box.add_widget(MDBoxLayout())
        layout.add_widget(icon_box)
        
        title = MDLabel(text="Login Required", halign="center", font_size="24sp", bold=True, size_hint_y=None, height=dp(40))
        subtitle = MDLabel(text="Login to access your profile and save favorites", halign="center", font_size="14sp", size_hint_y=None, height=dp(60))
        
        layout.add_widget(title)
        layout.add_widget(subtitle)
        
        btn_box = MDBoxLayout(orientation='vertical', size_hint_y=None, height=dp(120), spacing=dp(10), padding=[dp(40), 0])
        
        login_btn = MDButton(style="filled", size_hint_y=None, height=dp(50), on_release=self.go_to_login)
        login_btn.add_widget(MDButtonText(text="Login"))
        
        guest_btn = MDButton(style="text", size_hint_y=None, height=dp(40), on_release=self.continue_as_guest)
        guest_btn.add_widget(MDButtonText(text="Continue as Guest"))
        
        btn_box.add_widget(login_btn)
        btn_box.add_widget(guest_btn)
        layout.add_widget(btn_box)
        
        layout.add_widget(MDBoxLayout(size_hint_y=0.3))
        
        self.add_widget(layout)
    
    def go_to_login(self, instance):
        app = MDApp.get_running_app()
        app.switch_screen('login')
    
    def continue_as_guest(self, instance):
        user_data = {
            'username': 'Guest',
            'email': 'guest@gua.app',
            'logged_in': False
        }
        storage.save_user(user_data)
        self.refresh_ui()
    
    def refresh_ui(self):
        self.build_ui()
    
    def edit_profile(self, instance):
        app = MDApp.get_running_app()
        app.switch_screen('edit_profile')
    
    def show_favorites(self, instance):
        app = MDApp.get_running_app()
        app.switch_screen('favorites')
    
    def show_history(self, instance):
        app = MDApp.get_running_app()
        app.switch_screen('history')
    
    def show_notifications(self, instance):
        app = MDApp.get_running_app()
        app.switch_screen('notifications')
    
    def show_settings(self, instance):
        app = MDApp.get_running_app()
        app.switch_screen('settings')
    
    def logout(self, instance):
        storage.logout_user()
        self.refresh_ui()
