from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField
from kivymd.uix.appbar import MDTopAppBar
from kivy.metrics import dp
from kivy.animation import Animation
import re
from utils.storage import storage


class EditProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        toolbar = MDTopAppBar()
        toolbar.headline_text = "Edit Profile"
        toolbar.type = "small"
        back_btn = MDIconButton(icon="arrow-left", on_release=lambda x: self.go_back())
        toolbar.add_widget(back_btn)
        layout.add_widget(toolbar)
        
        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20), size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        user = storage.get_user()
        
        # Avatar
        avatar_box = MDBoxLayout(size_hint_y=None, height=dp(100), spacing=dp(10))
        avatar = MDIconButton(icon="account-circle")
        avatar_box.add_widget(MDBoxLayout())
        avatar_box.add_widget(avatar)
        avatar_box.add_widget(MDBoxLayout())
        content.add_widget(avatar_box)
        
        # Form card
        card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(380),
            padding=dp(20),
            spacing=dp(12),
            elevation=2,
            radius=[10, 10, 10, 10]
        )
        
        card_title = MDLabel(text="Update Your Information", font_size="18sp", bold=True, size_hint_y=None, height=dp(30))
        card.add_widget(card_title)
        
        # Username section
        username_label = MDLabel(text="Username", font_size="14sp", bold=True, size_hint_y=None, height=dp(25))
        card.add_widget(username_label)
        
        self.username_field = MDTextField(mode="outlined", size_hint_y=None, height=dp(56))
        self.username_field.hint_text = "Enter your username"
        self.username_field.text = user.get('username', '') if user else ''
        self.username_field.bind(text=self.on_username_change)
        card.add_widget(self.username_field)
        
        self.username_error = MDLabel(text="", font_size="12sp", theme_text_color="Error", size_hint_y=None, height=dp(20))
        card.add_widget(self.username_error)
        
        # Email section
        email_label = MDLabel(text="Email Address", font_size="14sp", bold=True, size_hint_y=None, height=dp(25))
        card.add_widget(email_label)
        
        self.email_field = MDTextField(mode="outlined", size_hint_y=None, height=dp(56))
        self.email_field.hint_text = "Enter your email"
        self.email_field.text = user.get('email', '') if user else ''
        self.email_field.bind(text=self.on_email_change)
        card.add_widget(self.email_field)
        
        self.email_error = MDLabel(text="", font_size="12sp", theme_text_color="Error", size_hint_y=None, height=dp(20))
        card.add_widget(self.email_error)
        
        # Success/Error message
        self.message_label = MDLabel(text="", halign="center", font_size="13sp", bold=True, size_hint_y=None, height=dp(25))
        card.add_widget(self.message_label)
        
        # Save button
        save_btn = MDButton(style="filled", size_hint_y=None, height=dp(50), on_release=self.save_profile)
        save_btn.add_widget(MDButtonText(text="Save Changes"))
        card.add_widget(save_btn)
        
        content.add_widget(card)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)
    
    def on_username_change(self, instance, value):
        """Real-time username validation"""
        self.username_error.text = ""
        self.message_label.text = ""
        
        if len(value) > 0 and len(value) < 3:
            self.username_error.text = "Username must be at least 3 characters"
        elif len(value) > 20:
            self.username_error.text = "Username must be less than 20 characters"
        elif value and not re.match("^[a-zA-Z0-9_]+$", value):
            self.username_error.text = "Only letters, numbers and underscore allowed"
    
    def on_email_change(self, instance, value):
        """Real-time email validation"""
        self.email_error.text = ""
        self.message_label.text = ""
        
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
    
    def save_profile(self, instance):
        username = self.username_field.text.strip()
        email = self.email_field.text.strip()
        
        # Clear previous errors
        self.message_label.text = ""
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
        
        # Save changes
        user = storage.get_user()
        if user:
            user['username'] = username
            user['email'] = email
            storage.save_user(user)
        
        # Show success message
        self.message_label.text = "✓ Profile updated successfully!"
        self.message_label.theme_text_color = "Primary"
        
        # Refresh profile screen
        app = MDApp.get_running_app()
        profile_screen = app.sm.get_screen('profile')
        profile_screen.refresh_ui()
        
        # Navigate back after short delay
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.go_back(), 1.0)
    
    def go_back(self):
        app = MDApp.get_running_app()
        app.switch_screen('profile')
