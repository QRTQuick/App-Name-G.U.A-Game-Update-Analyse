from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivy.animation import Animation
import re
from utils.storage import storage


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        scroll = MDScrollView()
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        # Spacer
        layout.add_widget(MDBoxLayout(size_hint_y=None, height=dp(40)))
        
        # Logo/Title
        title_box = MDBoxLayout(orientation='vertical', size_hint_y=None, height=dp(120), spacing=dp(10))
        
        icon_container = MDBoxLayout(size_hint_y=None, height=dp(60))
        icon = MDIconButton(icon="gamepad-variant")
        icon_container.add_widget(MDBoxLayout())
        icon_container.add_widget(icon)
        icon_container.add_widget(MDBoxLayout())
        
        title = MDLabel(text="G.U.A", halign="center", font_size="36sp", bold=True, size_hint_y=None, height=dp(40))
        subtitle = MDLabel(text="Game Update Analyse", halign="center", font_size="14sp", size_hint_y=None, height=dp(20))
        
        title_box.add_widget(icon_container)
        title_box.add_widget(title)
        title_box.add_widget(subtitle)
        layout.add_widget(title_box)
        
        # Login card
        card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(450),
            padding=dp(20),
            spacing=dp(12),
            elevation=4,
            radius=[15, 15, 15, 15]
        )
        
        card_title = MDLabel(text="Welcome Back!", font_size="22sp", bold=True, size_hint_y=None, height=dp(35))
        card_subtitle = MDLabel(text="Login to access your profile", font_size="13sp", size_hint_y=None, height=dp(25))
        card.add_widget(card_title)
        card.add_widget(card_subtitle)
        
        # Username section
        username_label = MDLabel(text="Username", font_size="14sp", bold=True, size_hint_y=None, height=dp(25))
        card.add_widget(username_label)
        
        self.username_field = MDTextField(mode="outlined", size_hint_y=None, height=dp(56))
        self.username_field.hint_text = "Enter your username"
        self.username_field.bind(text=self.on_username_change)
        card.add_widget(self.username_field)
        
        self.username_error = MDLabel(text="", font_size="12sp", theme_text_color="Error", size_hint_y=None, height=dp(20))
        card.add_widget(self.username_error)
        
        # Email section
        email_label = MDLabel(text="Email Address", font_size="14sp", bold=True, size_hint_y=None, height=dp(25))
        card.add_widget(email_label)
        
        self.email_field = MDTextField(mode="outlined", size_hint_y=None, height=dp(56))
        self.email_field.hint_text = "Enter your email"
        self.email_field.bind(text=self.on_email_change)
        card.add_widget(self.email_field)
        
        self.email_error = MDLabel(text="", font_size="12sp", theme_text_color="Error", size_hint_y=None, height=dp(20))
        card.add_widget(self.email_error)
        
        # General error message
        self.error_label = MDLabel(text="", halign="center", theme_text_color="Error", font_size="13sp", bold=True, size_hint_y=None, height=dp(25))
        card.add_widget(self.error_label)
        
        # Login button
        self.login_btn = MDButton(style="filled", size_hint_y=None, height=dp(50), on_release=self.do_login)
        self.login_btn.add_widget(MDButtonText(text="Login"))
        card.add_widget(self.login_btn)
        
        # Guest button
        guest_btn = MDButton(style="text", size_hint_y=None, height=dp(40), on_release=self.login_as_guest)
        guest_btn.add_widget(MDButtonText(text="Continue as Guest"))
        card.add_widget(guest_btn)
        
        layout.add_widget(card)
        
        # Info text
        info_text = MDLabel(
            text="Your data is stored locally on your device",
            halign="center",
            font_size="11sp",
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(info_text)
        
        # Spacer
        layout.add_widget(MDBoxLayout(size_hint_y=None, height=dp(40)))
        
        scroll.add_widget(layout)
        self.add_widget(scroll)
    
    def on_username_change(self, instance, value):
        """Real-time username validation"""
        self.username_error.text = ""
        
        if len(value) > 0 and len(value) < 3:
            self.username_error.text = "Username must be at least 3 characters"
        elif len(value) > 20:
            self.username_error.text = "Username must be less than 20 characters"
        elif value and not re.match("^[a-zA-Z0-9_]+$", value):
            self.username_error.text = "Only letters, numbers and underscore allowed"
    
    def on_email_change(self, instance, value):
        """Real-time email validation"""
        self.email_error.text = ""
        
        if value and not self.is_valid_email(value):
            self.email_error.text = "Please enter a valid email address"
    
    def is_valid_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_username(self, username):
        """Validate username"""
        if not username:
            return False, "Username is required"
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(username) > 20:
            return False, "Username must be less than 20 characters"
        if not re.match("^[a-zA-Z0-9_]+$", username):
            return False, "Username can only contain letters, numbers and underscore"
        return True, ""
    
    def validate_email(self, email):
        """Validate email"""
        if not email:
            return False, "Email is required"
        if not self.is_valid_email(email):
            return False, "Please enter a valid email address"
        return True, ""
    
    def shake_animation(self, widget):
        """Shake animation for errors"""
        anim = Animation(x=widget.x + 10, duration=0.05)
        anim += Animation(x=widget.x - 10, duration=0.05)
        anim += Animation(x=widget.x + 10, duration=0.05)
        anim += Animation(x=widget.x, duration=0.05)
        anim.start(widget)
    
    def do_login(self, instance):
        username = self.username_field.text.strip()
        email = self.email_field.text.strip()
        
        # Clear previous errors
        self.error_label.text = ""
        self.username_error.text = ""
        self.email_error.text = ""
        
        # Validate username
        username_valid, username_msg = self.validate_username(username)
        if not username_valid:
            self.username_error.text = username_msg
            self.shake_animation(self.username_field)
            return
        
        # Validate email
        email_valid, email_msg = self.validate_email(email)
        if not email_valid:
            self.email_error.text = email_msg
            self.shake_animation(self.email_field)
            return
        
        # Save user data
        user_data = {
            'username': username,
            'email': email,
            'logged_in': True
        }
        storage.save_user(user_data)
        
        # Show success message
        self.error_label.text = "✓ Login successful!"
        self.error_label.theme_text_color = "Primary"
        
        # Navigate to home after short delay
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.navigate_to_home(), 0.5)
    
    def navigate_to_home(self):
        app = MDApp.get_running_app()
        app.switch_screen('home')
        
        # Refresh profile screen
        profile_screen = app.sm.get_screen('profile')
        profile_screen.refresh_ui()
    
    def login_as_guest(self, instance):
        # Save guest data
        user_data = {
            'username': 'Guest',
            'email': 'guest@gua.app',
            'logged_in': False
        }
        storage.save_user(user_data)
        
        # Navigate to home
        app = MDApp.get_running_app()
        app.switch_screen('home')
        
        # Refresh profile screen
        profile_screen = app.sm.get_screen('profile')
        profile_screen.refresh_ui()
