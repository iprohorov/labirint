import pygame_gui
import pygame

class MenuWindow(pygame_gui.elements.UIWindow):
    def __init__(self,
                 rect: pygame.Rect,
                 ui_manager: pygame_gui.core.interfaces.IUIManagerInterface):
        super().__init__(rect, ui_manager, window_display_title="menu", resizable=True)
        htm_text_block_2 = pygame_gui.elements.UITextBox('<font face=fira_code size=2 color=#000000><b>Hey, What the heck!</b>'
                             '<br><br>'
                             'This is some <a href="test">text</a> in a different box,'
                             ' hooray for variety - '
                             'if you want then you should put a ring upon it. '
                             '<body bgcolor=#990000>What if we do a really long word?</body> '
                             '<b><i>derp FALALALALALALALXALALALXALALALALAAPaaaaarp gosh'
                             '</b></i></font>',
                             pygame.Rect((0, 0), (250, 200)),
                             manager=self.ui_manager,
                             container=self,
                             object_id="#text_box_2")
        self.resizable = False 

    def update(self, time_delta: float):
        super().update(time_delta)