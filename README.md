# TTW

Tesseract Translator Window.

# Table of Contents

- [Getting](#getting)
- [Configuration](#configuration)
- [Running](#running)

# Getting

- Using venv

1. Clone this repository

2. Run start.bat

- Or (if you don't like use venv)

1. Clone this repository

2. Install dependencies running `pip3 install -r requirements.txt`.

# Configuration

You need a configuration file called config.ini in the root directory.
config file is as follows:

```

[Settings]

; example eng, jpn, jpn_vert. osd, spa
language = eng
;ar: arabic, zh-cn: chinese (simplified), zh-tw: chinese (traditional), da: danish, nl: dutch, en: english, fr: french ,de: german ,el: greek ,gu: gujarati ,hi: hindi ,ja: japanese ,ko: korean,pt: portuguese ,ru: russian ,es: spanish

;language to translate
target_language = es

;key for translate
key_t = x

;controller keys
;LEFT_THUMB, RIGHT_THUMB, LEFT_SHOULDER, RIGHT_SHOULDER, BACK, START, DPAD_LEFT, DPAD_RIGHT, DPAD_UP, DPAD_DOWN, A, B, X ,Y
Ckey_t = DPAD_LEFT

;key for hide
key_h = v

;controller keys
;LEFT_THUMB, RIGHT_THUMB, LEFT_SHOULDER, RIGHT_SHOULDER, BACK, START, DPAD_LEFT, DPAD_RIGHT, DPAD_UP, DPAD_DOWN, A, B, X ,Y
Ckey_h = DPAD_RIGHT

;tesseract path
tesseract = Tesseract\tesseract.exe

;tesseract config
t_config = --oem 3 --psm 6

[Post_processing]

;gray scale
gray = False

;gray scale and threshold
gray_thresh = False

;gray scale, threshold and sharpen
gray_sharpen_thresh = True

```

# Running

1. Run start.bat

- Or (if you don't use venv)

1. Open translate_screen.pyw
