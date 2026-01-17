from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.appbar import MDTopAppBar
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemLeadingIcon
from kivy.metrics import dp
from datetime import datetime, timedelta


class NotificationsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        toolbar = MDTopAppBar()
        toolbar.headline_text = "Notifications"
        toolbar.type = "small"
        back_btn = MDIconButton(icon="arrow-left", on_release=lambda x: self.go_back())
        toolbar.add_widget(back_btn)
        layout.add_widget(toolbar)
        
        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, padding=dp(10))
        content.bind(minimum_height=content.setter('height'))
        
        # Sample notifications
        notifications = [
            {
                'icon': 'star',
                'title': 'New Trending Game',
                'message': 'Cyberpunk 2077 is now trending!',
                'time': 'Just now',
                'unread': True
            },
            {
                'icon': 'update',
                'title': 'Game Update',
                'message': 'The Witcher 3 has a new update available',
                'time': '2 hours ago',
                'unread': True
            },
            {
                'icon': 'heart',
                'title': 'Favorite Game Sale',
                'message': 'Red Dead Redemption 2 is on sale!',
                'time': '1 day ago',
                'unread': False
            },
            {
                'icon': 'information',
                'title': 'Welcome to G.U.A',
                'message': 'Thanks for joining! Explore trending games and add favorites.',
                'time': '3 days ago',
                'unread': False
            }
        ]
        
        for notif in notifications:
            card = self.create_notification_card(notif)
            content.add_widget(card)
        
        # Mark all as read button
        mark_read_btn = MDButton(
            style="outlined",
            size_hint_y=None,
            height=dp(50),
            on_release=self.mark_all_read
        )
        mark_read_btn.add_widget(MDButtonText(text="Mark All as Read"))
        content.add_widget(mark_read_btn)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)
    
    def create_notification_card(self, notif):
        card = MDCard(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(90),
            padding=dp(10),
            spacing=dp(10),
            elevation=2 if notif['unread'] else 1,
            radius=[10, 10, 10, 10]
        )
        
        # Icon
        icon_box = MDBoxLayout(size_hint_x=None, width=dp(40))
        icon = MDIconButton(icon=notif['icon'], disabled=True)
        icon_box.add_widget(icon)
        card.add_widget(icon_box)
        
        # Content
        content_box = MDBoxLayout(orientation='vertical', spacing=dp(3))
        
        title = MDLabel(
            text=notif['title'],
            font_size="15sp",
            bold=notif['unread'],
            size_hint_y=None,
            height=dp(25)
        )
        message = MDLabel(
            text=notif['message'],
            font_size="13sp",
            size_hint_y=None,
            height=dp(35)
        )
        time = MDLabel(
            text=notif['time'],
            font_size="11sp",
            size_hint_y=None,
            height=dp(20)
        )
        
        content_box.add_widget(title)
        content_box.add_widget(message)
        content_box.add_widget(time)
        
        card.add_widget(content_box)
        
        # Unread indicator
        if notif['unread']:
            indicator = MDIconButton(
                icon="circle",
                icon_color=(0, 0.5, 1, 1),
                size_hint=(None, None),
                size=(dp(20), dp(20))
            )
            card.add_widget(indicator)
        
        return card
    
    def mark_all_read(self, instance):
        # Refresh UI to show all as read
        self.clear_widgets()
        self.build_ui()
    
    def go_back(self):
        app = MDApp.get_running_app()
        app.switch_screen('profile')
