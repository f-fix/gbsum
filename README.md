# Overview
gbsum.py is a GB cartridge checksum checker and corrector

## Caveats
TODO: Currently this is still in an archaic Python 2 dialect. It needs to be modernised.

## Usage
`usage: python2 gbsum.py { -c -OR- -v } FILE.GB  -OR-  python gbsum.py FILE.GB OUTFILE.GB`

It can display the "logo" section of the header a few different ways, dependent on CHARSET/DEFAULT_CHARSET environment variables or the current locale setting.
Example from a V.Fame cartridge:
Unicode Braille patterns
```
⣿⢆⢸⡇⣛⢀⡀⣀⠠⣶⠄⣀⣀⠀⣀⢀⡀⠀⣀⣸⡇⢀⣀⡀
⣿⠈⢾⡇⣿⠸⣇⡿⠀⣿⠸⣇⣸⠇⢿⣸⠇⢿⣀⣸⠇⢿⣒⡛
```
ASCII art
```
::.  :: ::        ..                   ::
::'. :: .. .. .. '::' ....  .. ..   ...::  ....
:: '.:: :: :: ::  :: ::  :: :: :: ::   :: ::..::
::  ':: :: ':.:'  :: ':..:' ':.:' ':...:' ':...
```
Block graphics (e.g. for CP437)
```
██▄  ██ ██        ▄▄                   ██
██▀▄ ██ ▄▄ ▄▄ ▄▄ ▀██▀ ▄▄▄▄  ▄▄ ▄▄   ▄▄▄██  ▄▄▄▄
██ ▀▄██ ██ ██ ██  ██ ██  ██ ██ ██ ██   ██ ██▄▄██
██  ▀██ ██ ▀█▄█▀  ██ ▀█▄▄█▀ ▀█▄█▀ ▀█▄▄▄█▀ ▀█▄▄▄
```
