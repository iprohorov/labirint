import pygame_gui
import pygame

class MenuWindow(pygame_gui.elements.UIWindow):
    def __init__(self,
                 rect: pygame.Rect,
                 ui_manager: pygame_gui.core.interfaces.IUIManagerInterface):
        super().__init__(rect, ui_manager, window_display_title="menu", resizable=True)

    def update(self, time_delta: float):
        super().update(time_delta)