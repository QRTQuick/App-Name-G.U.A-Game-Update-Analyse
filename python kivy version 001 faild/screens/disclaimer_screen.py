from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivy.metrics import dp
from utils.storage import storage


class DisclaimerScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Logo/Icon
        icon_box = MDBoxLayout(size_hint_y=None, height=dp(80))
        icon = MDIconButton(icon="alert-circle-outline")
        icon_box.add_widget(MDBoxLayout())
        icon_box.add_widget(icon)
        icon_box.add_widget(MDBoxLayout())
        layout.add_widget(icon_box)
        
        # Title
        title = MDLabel(
            text="Important Disclaimer",
            halign="center",
            font_size="24sp",
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(title)
        
        # Disclaimer content
        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, padding=dp(10))
        content.bind(minimum_height=content.setter('height'))
        
        disclaimer_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(15),
            spacing=dp(10),
            elevation=3,
            radius=[15, 15, 15, 15]
        )
        disclaimer_card.bind(minimum_height=disclaimer_card.setter('height'))
        
        disclaimer_text = """⚠️ PLEASE READ CAREFULLY

━━━━━━━━━━━━━━━━━━━━━━

POWERED BY RAWG API

This application uses RAWG API (rawg.io) to provide game information, images, and data.

━━━━━━━━━━━━━━━━━━━━━━

NOT A REPLACEMENT

G.U.A is NOT meant to replace:
• Official game platforms
• Game stores (Steam, Epic, etc.)
• Publisher websites
• Console marketplaces

━━━━━━━━━━━━━━━━━━━━━━

PURPOSE

This app is designed to:
✓ View game information
✓ Track game updates
✓ Browse game catalogs
✓ Run on low-end devices
✓ Provide quick game lookups

━━━━━━━━━━━━━━━━━━━━━━

WHAT THIS APP DOES NOT DO

✗ Download games
✗ Provide game files
✗ Host copyrighted content
✗ Replace official platforms
✗ Violate copyright laws

━━━━━━━━━━━━━━━━━━━━━━

OPTIMIZED FOR LOW-END DEVICES

G.U.A is specifically designed to run smoothly on devices with limited resources, providing a lightweight alternative for game information.

━━━━━━━━━━━━━━━━━━━━━━

DATA & PRIVACY

• All data from RAWG API
• Cached locally for 2 days
• No personal data collection
• No tracking or analytics
• You control your data

━━━━━━━━━━━━━━━━━━━━━━

LEGAL

All game data, images, names, and trademarks belong to their respective owners. This app is for informational and educational purposes only.

━━━━━━━━━━━━━━━━━━━━━━

By continuing, you acknowledge that you have read and understood this disclaimer."""
        
        disclaimer_label = MDLabel(text=disclaimer_text, size_hint_y=None)
        disclaimer_label.bind(texture_size=disclaimer_label.setter('size'))
        disclaimer_card.add_widget(disclaimer_label)
        
        content.add_widget(disclaimer_card)
        scroll.add_widget(content)
        layout.add_widget(scroll)
        
        # Buttons
        btn_layout = MDBoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
        
        decline_btn = MDButton(
            style="outlined",
            size_hint_x=0.4,
            on_release=self.decline
        )
        decline_btn.add_widget(MDButtonText(text="Decline"))
        
        accept_btn = MDButton(
            style="filled",
            size_hint_x=0.6,
            on_release=self.accept
        )
        accept_btn.add_widget(MDButtonText(text="Accept & Continue"))
        
        btn_layout.add_widget(decline_btn)
        btn_layout.add_widget(accept_btn)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def accept(self, instance):
        """User accepted disclaimer"""
        # Mark disclaimer as accepted
        user = storage.get_user()
        if not user:
            user = {}
        user['disclaimer_accepted'] = True
        storage.save_user(user)
        
        # Navigate to login or home
        app = MDApp.get_running_app()
        if storage.is_logged_in():
            app.switch_screen('home')
        else:
            app.switch_screen('login')
    
    def decline(self, instance):
        """User declined disclaimer"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.stop()
