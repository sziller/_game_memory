"""All Widgets and Layouts defined for the main Python file"""

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout


class LabelTitle(Label):
    """custom Label"""
    pass


class LabelInfo(Label):
    """custom Label"""
    pass


class LabelSubTitle(Label):
    """custom Label"""
    pass


class LabelSubSubTitle(Label):
    """custom Label"""
    pass


class LabelListitem(Label):
    """custom Label"""
    pass


class LabelLead(LabelListitem):
    """custom Label"""
    pass


class LabelEnd(LabelListitem):
    """custom Label"""
    pass


class LabelWelcomeListLeft(Label):
    """custom Label"""
    pass


class LabelWelcomeList(Label):
    """custom Label"""
    pass


class LabelWelcomeListNarrow(Label):
    """custom Label"""
    pass


class ScreenTitleLabel(Label):
    """custom Label"""
    pass


class ButtonSallet(Button):
    """custom Button"""
    pass


class ButtonListitem(ButtonSallet):
    """custom Button"""
    pass


class ButtonInfo(ButtonSallet):
    """custom Button"""
    pass


class ToggleButtonSallet(ToggleButton):
    """custom ToggleButton"""
    pass


class TextInputSallet(TextInput):
    """custom TextInput"""
    pass


class UtxoDisplayArea(StackLayout):
    def __init__(self, **kwargs):
        super(UtxoDisplayArea, self).__init__(**kwargs)


class InputDisplayArea(StackLayout):
    def __init__(self, **kwargs):
        super(InputDisplayArea, self).__init__(**kwargs)


class OutputDisplayArea(StackLayout):
    def __init__(self, **kwargs):
        super(OutputDisplayArea, self).__init__(**kwargs)


class NodeDisplayArea(StackLayout):
    def __init__(self, **kwargs):
        super(NodeDisplayArea, self).__init__(**kwargs)


class OperationAreaBox(BoxLayout):
    """custom BoxLayout"""
    pass
