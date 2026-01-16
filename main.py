from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screenmanager import MDScreenManager
from kivy.metrics import dp
from kivy.core.window import Window

from screens import (
    HomeScreen,
    SearchScreen,
    TrendingScreen,
    ProfileScreen,
    SettingsScreen,
    GameDetailsScreen,
    LoginScreen,
    EditProfileScreen,
    FavoritesScreen,
    HistoryScreen,
    NotificationsScreen,
    DisclaimerScreen
)
from utils.storage import storage
import sys
import traceback
from datetime import datetime

# Mobile window size
Window.size = (360, 640)


class GUAApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Screen manager
        self.sm = MDScreenManager()
        self.sm.add_widget(DisclaimerScreen(name='disclaimer'))
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(SearchScreen(name='search'))
        self.sm.add_widget(TrendingScreen(name='trending'))
        self.sm.add_widget(ProfileScreen(name='profile'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(GameDetailsScreen(name='details'))
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(EditProfileScreen(name='edit_profile'))
        self.sm.add_widget(FavoritesScreen(name='favorites'))
        self.sm.add_widget(HistoryScreen(name='history'))
        self.sm.add_widget(NotificationsScreen(name='notifications'))
        
        # Check if disclaimer was accepted
        user = storage.get_user()
        if not user or not user.get('disclaimer_accepted', False):
            self.sm.current = 'disclaimer'
        elif not storage.is_logged_in():
            self.sm.current = 'login'
        else:
            self.sm.current = 'home'
        
        main_layout.add_widget(self.sm)
        
        # Bottom navigation
        nav_bar = self.create_navigation_bar()
        main_layout.add_widget(nav_bar)
        
        return main_layout
    
    def create_navigation_bar(self):
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
        
        return nav_bar
    
    def switch_screen(self, screen_name):
        self.sm.current = screen_name
    
    def show_game_details(self, game_id):
        details_screen = self.sm.get_screen('details')
        details_screen.load_game_details(game_id)
        self.sm.current = 'details'


def _write_crash_log(exc_type, exc_value, tb):
    try:
        log_dir = storage.data_dir
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / 'crash.log'
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"--- Crash at {datetime.utcnow().isoformat()} UTC ---\n")
            traceback.print_exception(exc_type, exc_value, tb, file=f)
            f.write('\n')
    except Exception:
        # Best-effort; avoid masking the original exception
        pass


if __name__ == '__main__':
    # Install global exception hook to capture unhandled exceptions
    def _ex_hook(exc_type, exc_value, exc_tb):
        _write_crash_log(exc_type, exc_value, exc_tb)
        # Also print to stderr so CI/device logs include the traceback
        traceback.print_exception(exc_type, exc_value, exc_tb)

    sys.excepthook = _ex_hook

    try:
        GUAApp().run()
    except Exception:
        # Catch anything that escapes Kivy's internals and log it
        exc_type, exc_value, exc_tb = sys.exc_info()
        _write_crash_log(exc_type, exc_value, exc_tb)
        raise
