from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.appbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogButtonContainer
from kivy.metrics import dp
from utils.cache_manager import cache
from utils.storage import storage


class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        toolbar = MDTopAppBar()
        toolbar.headline_text = "Settings"
        toolbar.type = "small"
        layout.add_widget(toolbar)
        
        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, padding=dp(15))
        content.bind(minimum_height=content.setter('height'))
        
        sections = [
            ("General", [
                ("theme", "Dark Mode", self.toggle_theme),
                ("translate", "Language", self.change_language),
                ("bell-outline", "Notifications", self.notification_settings)
            ]),
            ("Storage", [
                ("database", "Cache Management", self.show_cache_info),
                ("delete", "Clear Cache", self.clear_cache),
                ("broom", "Clear History", self.clear_history)
            ]),
            ("Account", [
                ("lock", "Privacy", self.privacy_settings),
                ("shield-check", "Security", self.security_settings),
                ("logout", "Sign Out", self.sign_out)
            ]),
            ("About", [
                ("information", "About G.U.A", self.show_about),
                ("file-document", "Terms of Service", self.show_terms),
                ("help-circle", "Help & Support", self.show_help)
            ])
        ]
        
        for section_title, items in sections:
            section_label = MDLabel(text=section_title, font_size="14sp", bold=True, size_hint_y=None, height=dp(30))
            content.add_widget(section_label)
            
            for icon, text, callback in items:
                item = MDCard(size_hint_y=None, height=dp(55), padding=dp(10), elevation=1, radius=[8, 8, 8, 8])
                item_layout = MDBoxLayout(spacing=dp(15))
                item_layout.add_widget(MDIconButton(icon=icon, on_release=callback))
                item_layout.add_widget(MDLabel(text=text, font_size="14sp"))
                item_layout.add_widget(MDIconButton(icon="chevron-right", on_release=callback))
                item.add_widget(item_layout)
                content.add_widget(item)
            
            content.add_widget(MDBoxLayout(size_hint_y=None, height=dp(10)))
        
        version = MDLabel(text="G.U.A v1.0.0", halign="center", font_size="12sp", size_hint_y=None, height=dp(40))
        content.add_widget(version)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)

    
    def toggle_theme(self, instance):
        """Toggle between dark and light theme"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        
        if app.theme_cls.theme_style == "Dark":
            app.theme_cls.theme_style = "Light"
            message = "Switched to Light Mode"
        else:
            app.theme_cls.theme_style = "Dark"
            message = "Switched to Dark Mode"
        
        dialog = MDDialog(
            MDDialogHeadlineText(text="Theme Changed"),
            MDDialogContentContainer(
                MDLabel(text=message, size_hint_y=None, height=dp(50))
            ),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="OK"), style="text", on_release=lambda x: dialog.dismiss())
            )
        )
        dialog.open()
    
    def change_language(self, instance):
        """Show language selection dialog"""
        languages = ["English", "Spanish", "French", "German", "Portuguese", "Chinese", "Japanese"]
        
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, padding=dp(10))
        content.bind(minimum_height=content.setter('height'))
        
        for lang in languages:
            btn = MDButton(
                MDButtonText(text=lang),
                style="outlined",
                size_hint_y=None,
                height=dp(45),
                on_release=lambda x, l=lang: self.set_language(l)
            )
            content.add_widget(btn)
        
        self.lang_dialog = MDDialog(
            MDDialogHeadlineText(text="Select Language"),
            MDDialogContentContainer(content),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="Cancel"), style="text", on_release=lambda x: self.lang_dialog.dismiss())
            )
        )
        self.lang_dialog.open()
    
    def set_language(self, language):
        """Set app language"""
        self.lang_dialog.dismiss()
        
        dialog = MDDialog(
            MDDialogHeadlineText(text="Language Set"),
            MDDialogContentContainer(
                MDLabel(text=f"Language changed to {language}\n(Feature coming soon)", halign="center", size_hint_y=None, height=dp(60))
            ),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="OK"), style="text", on_release=lambda x: dialog.dismiss())
            )
        )
        dialog.open()
    
    def notification_settings(self, instance):
        """Show notification settings"""
        content = MDBoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, padding=dp(10))
        content.bind(minimum_height=content.setter('height'))
        
        settings = [
            ("New Games", "Get notified about new game releases"),
            ("Updates", "Game updates and patches"),
            ("Sales", "Price drops on favorite games"),
            ("Trending", "Trending games notifications")
        ]
        
        for title, desc in settings:
            item = MDCard(size_hint_y=None, height=dp(70), padding=dp(10), elevation=1, radius=[8, 8, 8, 8])
            item_layout = MDBoxLayout(orientation='vertical', spacing=dp(5))
            item_layout.add_widget(MDLabel(text=title, font_size="15sp", bold=True, size_hint_y=None, height=dp(25)))
            item_layout.add_widget(MDLabel(text=desc, font_size="12sp", size_hint_y=None, height=dp(30)))
            item.add_widget(item_layout)
            content.add_widget(item)
        
        self.notif_dialog = MDDialog(
            MDDialogHeadlineText(text="Notification Settings"),
            MDDialogContentContainer(content),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="Close"), style="text", on_release=lambda x: self.notif_dialog.dismiss())
            )
        )
        self.notif_dialog.open()
    
    def show_cache_info(self, instance):
        """Show cache information dialog"""
        cache_info = cache.get_cache_info()
        
        dialog_content = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(150))
        dialog_content.add_widget(MDLabel(text=f"Cached Items: {cache_info['count']}", size_hint_y=None, height=dp(30)))
        dialog_content.add_widget(MDLabel(text=f"Cache Size: {cache_info['size_mb']} MB", size_hint_y=None, height=dp(30)))
        dialog_content.add_widget(MDLabel(text=f"Expired Items: {cache_info['expired']}", size_hint_y=None, height=dp(30)))
        dialog_content.add_widget(MDLabel(text="Cache expires after 2 days", font_size="12sp", size_hint_y=None, height=dp(30)))
        
        self.cache_dialog = MDDialog(
            MDDialogHeadlineText(text="Cache Information"),
            MDDialogContentContainer(dialog_content),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="Clear Expired"), style="text", on_release=self.clear_expired_cache),
                MDButton(MDButtonText(text="Close"), style="text", on_release=lambda x: self.cache_dialog.dismiss())
            )
        )
        self.cache_dialog.open()
    
    def clear_expired_cache(self, instance):
        """Clear expired cache items"""
        cleared = cache.clear_expired()
        self.cache_dialog.dismiss()
        
        # Show confirmation
        confirm_dialog = MDDialog(
            MDDialogHeadlineText(text="Cache Cleared"),
            MDDialogContentContainer(
                MDLabel(text=f"Cleared {cleared} expired items", size_hint_y=None, height=dp(50))
            ),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="OK"), style="text", on_release=lambda x: confirm_dialog.dismiss())
            )
        )
        confirm_dialog.open()
    
    def clear_cache(self, instance):
        """Clear all cache"""
        cleared = cache.clear_all()
        
        dialog = MDDialog(
            MDDialogHeadlineText(text="Cache Cleared"),
            MDDialogContentContainer(
                MDLabel(text=f"Cleared {cleared} cache items\nTotal space freed", size_hint_y=None, height=dp(60))
            ),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="OK"), style="text", on_release=lambda x: dialog.dismiss())
            )
        )
        dialog.open()
    
    def clear_history(self, instance):
        """Clear viewing history"""
        storage.clear_history()
        
        dialog = MDDialog(
            MDDialogHeadlineText(text="History Cleared"),
            MDDialogContentContainer(
                MDLabel(text="Your viewing history has been cleared", size_hint_y=None, height=dp(50))
            ),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="OK"), style="text", on_release=lambda x: dialog.dismiss())
            )
        )
        dialog.open()
    
    def privacy_settings(self, instance):
        """Show privacy settings"""
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, padding=dp(10))
        content.bind(minimum_height=content.setter('height'))
        
        privacy_text = """Privacy Policy

• All data is stored locally on your device
• No data is sent to external servers
• No tracking or analytics
• No personal information collected
• You control all your data

Data Stored:
- Login credentials (local only)
- Favorite games
- Viewing history
- App cache (2 days)

You can delete all data anytime from Settings."""
        
        privacy_label = MDLabel(text=privacy_text, size_hint_y=None)
        privacy_label.bind(texture_size=privacy_label.setter('size'))
        content.add_widget(privacy_label)
        
        self.privacy_dialog = MDDialog(
            MDDialogHeadlineText(text="Privacy Settings"),
            MDDialogContentContainer(content),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="Close"), style="text", on_release=lambda x: self.privacy_dialog.dismiss())
            )
        )
        self.privacy_dialog.open()
    
    def security_settings(self, instance):
        """Show security settings"""
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, padding=dp(10))
        content.bind(minimum_height=content.setter('height'))
        
        security_text = """Security Information

• Local storage only
• No cloud sync
• No password storage
• Secure API communication
• Regular cache cleanup

Recommendations:
- Clear cache regularly
- Review app permissions
- Keep app updated
- Use device lock screen

Your data is safe and private."""
        
        security_label = MDLabel(text=security_text, size_hint_y=None)
        security_label.bind(texture_size=security_label.setter('size'))
        content.add_widget(security_label)
        
        self.security_dialog = MDDialog(
            MDDialogHeadlineText(text="Security Settings"),
            MDDialogContentContainer(content),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="Close"), style="text", on_release=lambda x: self.security_dialog.dismiss())
            )
        )
        self.security_dialog.open()
    
    def sign_out(self, instance):
        """Sign out user"""
        from kivymd.app import MDApp
        storage.logout_user()
        app = MDApp.get_running_app()
        app.switch_screen('login')
    
    def show_about(self, instance):
        """Show about dialog with disclaimer"""
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, padding=dp(10))
        content.bind(minimum_height=content.setter('height'))
        
        about_text = """G.U.A (Game Update Analyse)
Version 1.0.0

A lightweight mobile app for game updates and analysis, designed to run smoothly on low-end devices.

━━━━━━━━━━━━━━━━━━━━━━

⚠️ DISCLAIMER

This software is powered by RAWG API and is NOT meant to replace official game platforms or stores.

Purpose:
• View game information
• Track game updates
• Browse game catalogs
• Optimized for low-end devices

This app does NOT:
• Allow game downloads
• Provide game files
• Replace official platforms
• Store copyrighted content

━━━━━━━━━━━━━━━━━━━━━━

Data Source: RAWG API
Website: rawg.io

All game data, images, and information are provided by RAWG and belong to their respective owners.

━━━━━━━━━━━━━━━━━━━━━━

Developed for educational and informational purposes only."""
        
        about_label = MDLabel(text=about_text, size_hint_y=None, halign="left")
        about_label.bind(texture_size=about_label.setter('size'))
        content.add_widget(about_label)
        
        self.about_dialog = MDDialog(
            MDDialogHeadlineText(text="About G.U.A"),
            MDDialogContentContainer(content),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="Visit RAWG"), style="text", on_release=lambda x: self.open_rawg()),
                MDButton(MDButtonText(text="Close"), style="text", on_release=lambda x: self.about_dialog.dismiss())
            )
        )
        self.about_dialog.open()
    
    def open_rawg(self):
        """Open RAWG website"""
        import webbrowser
        webbrowser.open("https://rawg.io")
        self.about_dialog.dismiss()
    
    def show_terms(self, instance):
        """Show terms of service"""
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, padding=dp(10))
        content.bind(minimum_height=content.setter('height'))
        
        terms_text = """Terms of Service

1. ACCEPTANCE OF TERMS
By using G.U.A, you agree to these terms.

2. SERVICE DESCRIPTION
G.U.A is an informational app that displays game data from RAWG API. It is designed for low-end devices.

3. DATA USAGE
• All data from RAWG API
• Cached locally for 2 days
• No user data collection
• No tracking or analytics

4. LIMITATIONS
This app does NOT:
• Provide game downloads
• Host game files
• Replace official platforms
• Violate copyright laws

5. DISCLAIMER
• Information provided "as is"
• No warranties or guarantees
• Not affiliated with game publishers
• Not a replacement for official sources

6. USER RESPONSIBILITIES
• Use app legally
• Respect copyright
• No unauthorized distribution
• Follow device guidelines

7. MODIFICATIONS
Terms may be updated without notice.

8. CONTACT
For issues or questions, refer to app settings.

Last Updated: January 2026"""
        
        terms_label = MDLabel(text=terms_text, size_hint_y=None)
        terms_label.bind(texture_size=terms_label.setter('size'))
        content.add_widget(terms_label)
        
        self.terms_dialog = MDDialog(
            MDDialogHeadlineText(text="Terms of Service"),
            MDDialogContentContainer(content),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="Close"), style="text", on_release=lambda x: self.terms_dialog.dismiss())
            )
        )
        self.terms_dialog.open()
    
    def show_help(self, instance):
        """Show help and support"""
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, padding=dp(10))
        content.bind(minimum_height=content.setter('height'))
        
        help_text = """Help & Support

━━━━━━━━━━━━━━━━━━━━━━

GETTING STARTED

1. Login or Continue as Guest
2. Browse games on Home screen
3. Search for specific games
4. View trending games
5. Add games to favorites
6. Check your profile stats

━━━━━━━━━━━━━━━━━━━━━━

FEATURES

🏠 Home: Latest game releases
🔍 Search: Find specific games
🔥 Trending: Top-rated games
👤 Profile: Your stats & favorites
⚙️ Settings: App configuration

━━━━━━━━━━━━━━━━━━━━━━

TROUBLESHOOTING

App running slow?
• Clear cache in Settings
• Clear expired items
• Restart the app

Can't find a game?
• Check spelling
• Try different keywords
• Game might not be in database

Data not loading?
• Check internet connection
• Clear cache and retry
• Restart the app

━━━━━━━━━━━━━━━━━━━━━━

TIPS

• Cache expires after 2 days
• Clear cache to free space
• Use search for quick access
• Add favorites for easy access
• Check notifications regularly

━━━━━━━━━━━━━━━━━━━━━━

OPTIMIZED FOR LOW-END DEVICES

This app is designed to run smoothly on devices with limited resources."""
        
        help_label = MDLabel(text=help_text, size_hint_y=None)
        help_label.bind(texture_size=help_label.setter('size'))
        content.add_widget(help_label)
        
        self.help_dialog = MDDialog(
            MDDialogHeadlineText(text="Help & Support"),
            MDDialogContentContainer(content),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="Close"), style="text", on_release=lambda x: self.help_dialog.dismiss())
            )
        )
        self.help_dialog.open()
