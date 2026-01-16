from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.metrics import dp


class RatingWidget(MDBoxLayout):
    """Widget to display game rating with star icon"""
    
    def __init__(self, rating, show_max=True, font_size="13sp", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(3)
        self.size_hint_y = None
        self.height = dp(25)
        
        # Star icon
        star_icon = MDIconButton(
            icon="star",
            icon_size=font_size,
            disabled=True,
            size_hint=(None, None),
            size=(dp(20), dp(20))
        )
        self.add_widget(star_icon)
        
        # Rating text
        rating_text = f"{rating}" + ("/5" if show_max else "")
        rating_label = MDLabel(
            text=rating_text,
            font_size=font_size,
            size_hint_y=None,
            height=dp(20)
        )
        self.add_widget(rating_label)


class InfoRow(MDBoxLayout):
    """Widget to display info with icon"""
    
    def __init__(self, icon, text, font_size="14sp", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = dp(8)
        self.size_hint_y = None
        self.height = dp(30)
        
        # Icon
        icon_btn = MDIconButton(
            icon=icon,
            icon_size=font_size,
            disabled=True,
            size_hint=(None, None),
            size=(dp(24), dp(24))
        )
        self.add_widget(icon_btn)
        
        # Text
        text_label = MDLabel(
            text=text,
            font_size=font_size,
            size_hint_y=None,
            height=dp(25)
        )
        self.add_widget(text_label)
