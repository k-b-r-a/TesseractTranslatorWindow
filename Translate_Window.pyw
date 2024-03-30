import cv2
import io
import configparser
import pytesseract
import win32con
import win32gui
import wx
import numpy as np
from pynput import keyboard
from PIL import ImageGrab
from deep_translator import GoogleTranslator
from XInput import *

config = configparser.ConfigParser()
config.read('config.ini')
language = config.get('Settings', 'language')
target_language = config.get('Settings', 'target_language')
key_t = config.get('Settings', 'key_t')
Ckey_t = config.get('Settings', 'Ckey_t')
key_h = config.get('Settings', 'key_h')
Ckey_h = config.get('Settings', 'Ckey_h')
pytesseract.pytesseract.tesseract_cmd = config.get('Settings', 'tesseract')
custom_config = config.get('Settings', 't_config')


def set_window_always_on_top(hwnd):
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,
                          0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)


def translucent(self):
    self.SetTransparent(0)


def Notranslucent(self):
    self.SetTransparent(200)


def transform_w(self):
    current_style = self.GetWindowStyle()
    if current_style == wx.FRAME_EX_METAL:
        self.SetWindowStyle(wx.FRAME_NO_TASKBAR)
    else:
        self.SetWindowStyle(wx.FRAME_EX_METAL)

########################################################################


class MainFrame(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Translator", size=(
            1200, 400), pos=(80, 200), style=wx.FRAME_EX_METAL)
        self.text = wx.StaticText(
            self, label=f'\nPress {key_t} for translate\nPress {key_h} for hide taskbar', pos=(10, 0))

        font = wx.Font(20, wx.FONTFAMILY_SWISS,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.text.SetFont(font)
        self.text.SetForegroundColour(wx.Colour(255, 255, 255))
        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.Show()

        hwnd = self.GetHandle()
        set_window_always_on_top(hwnd)

        def on_key(key):
            if hasattr(key, 'char'):
                if key.char == key_t:
                    try:
                        # Get
                        w_position = frame.GetPosition()
                        # Get
                        w_size = frame.GetSize()
                        translucent(frame)
                        screenshot = ImageGrab.grab(bbox=(
                            w_position[0], w_position[1], w_position[0] + w_size[0], w_position[1] + w_size[1]))
                        screenshot_buffer = io.BytesIO()
                        screenshot.save(screenshot_buffer, format='PNG')
                        screenshot_data = np.frombuffer(
                            screenshot_buffer.getvalue(), dtype=np.uint8)
                        Notranslucent(frame)
                        img = cv2.imdecode(screenshot_data, cv2.IMREAD_COLOR)
                        if config.get('Post_processing', 'gray_thresh_sharpen') == 'True':
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                            sharpen_kernel = np.array(
                                [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
                            sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
                            thresh = cv2.threshold(
                                sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                            post_Img = thresh
                        if config.get('Post_processing', 'gray_thresh') == 'True':
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                            thresh = cv2.threshold(
                                gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                            post_Img = thresh
                        if config.get('Post_processing', 'gray') == 'True':
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                            post_Img = gray
                        text_o = pytesseract.image_to_string(
                            post_Img, config=custom_config, lang=language)
                        translated_text = GoogleTranslator(
                            source='auto', target=target_language).translate(text_o)
                        self.text.SetLabel(translated_text)
                    except Exception as ex:
                        self.text.SetLabel("Error")
                        pass
                if key.char == key_h:
                    transform_w(frame)

        class MyHandler(EventHandler):
            def __init__(self, *controllers):
                super().__init__(*controllers, filter=BUTTON_DPAD_UP+BUTTON_DPAD_DOWN+BUTTON_DPAD_LEFT+BUTTON_DPAD_RIGHT+BUTTON_START+BUTTON_BACK +
                                 BUTTON_LEFT_THUMB+BUTTON_RIGHT_THUMB+BUTTON_LEFT_SHOULDER+BUTTON_RIGHT_SHOULDER+BUTTON_A+BUTTON_B+BUTTON_X+BUTTON_Y+FILTER_PRESSED_ONLY)

            def process_button_event(self, event):

                if event.button == Ckey_t:
                    class key:
                        char = key_t
                    on_key(key)

                elif event.button == Ckey_h:
                    class key:
                        char = key_h
                    on_key(key)

            def process_stick_event(self, event):
                if event.stick == LEFT:
                    pass

            def process_trigger_event(self, event):
                if event.trigger == LEFT:
                    pass

            def process_connection_event(self, event):
                if event.type == EVENT_CONNECTED:
                    pass
                elif event.type == EVENT_DISCONNECTED:
                    pass

        # initialize handler object
        handler = MyHandler(0)
        # initialize controller thread
        GamepadThread(handler)

        listener = keyboard.Listener(on_release=on_key)
        listener.start()
    # ----------------------------------------------------------------------


app = wx.App(False)
frame = MainFrame()
app.MainLoop()
