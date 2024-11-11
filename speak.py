
# back-end

import os
from gtts import gTTS, lang

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

def tts(language, text='no text'):
    filename = 'speak.mp3'
    thing = gTTS(text, lang=language)
    thing.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.music.stop()
    pygame.mixer.quit()

    os.remove(filename)

# TUI

from textual.app import App, ComposeResult
import textual.widgets as wdg
import textual.containers as cnt

class SpeakApp(App):
    CSS_PATH = "style.tcss"
 
    def compose(self) -> ComposeResult:
        
        self.OPTION_LIST = wdg.OptionList()

        self.TITLES = cnt.Horizontal(
            cnt.Container(
                wdg.Label('Language'),
                classes='label-container',
                id='language-label'
            ),
            cnt.Container(
                wdg.Label('Text to speak'),
                classes='label-container',
                id='tts-label'
            ),
            id='titles'
        )

        self.TEXT = wdg.TextArea()
        self.BUTTON = wdg.Button(label='Speak out loud')

        self.VERTICAL = cnt.Vertical(self.TEXT, self.BUTTON, id='vertical-main', classes='main')
        self.MAIN = cnt.Horizontal(self.OPTION_LIST, self.VERTICAL, classes='main')

        yield self.TITLES
        yield self.MAIN

    def on_button_pressed(self, event: wdg.Button.Pressed) -> None:
        selected_lang = list(lang.tts_langs().keys())[list(lang.tts_langs().values()).index(list(lang.tts_langs().values())[self.OPTION_LIST.highlighted])]
        if not selected_lang:
            selected_lang = 'en'
        tts(text=self.TEXT.text, language=selected_lang)

    def on_mount(self) -> None:
        for lg in lang.tts_langs().values():
            self.OPTION_LIST.add_option(wdg.option_list.Option(lg))

if __name__ == "__main__":
    app = SpeakApp()
    app.run()