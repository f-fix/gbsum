# Overview
gbsum.py is a GB cartridge checksum checker and corrector

## Caveats
TODO: Currently this is still in an archaic Python 2 dialect. It needs to be modernised.

## Usage
`usage: python2 gbsum.py { -c -OR- -v } FILE.GB  -OR-  python gbsum.py FILE.GB OUTFILE.GB`

With `-c FILE.GB`, a valid header and checksum will produce no output and will exit with a zero (i.e. successful) exit status.

With `-v FILE.GB`, a valid header and checksum might produce output like this:
```
Luoke Ren DX6 (Unlicensed, Japanese) (CBA091) [C].gb: recorded checksum 4E:443C
Luoke Ren DX6 (Unlicensed, Japanese) (CBA091) [C].gb: computed checksum 4E:443C
⣿⢆⢸⡇⣛⢀⡀⣀⠠⣶⠄⣀⣀⠀⣀⢀⡀⠀⣀⣸⡇⢀⣀⡀
```
_`✁┄┄┄┄` (bottom half omitted)_

**aside:** the language designator "Japanese" for this particular cartridge is a little fictitious, but that's at least what the developers were aiming for the appearance of.)

With `FILE.GB OUTFILE.GB`, a valid header in `FILE.GB` will cause a new `OUTFILE.GB` to be created (or overwritten!) containing a copy of `FILE.GB` with the checksum updated to reflect the contents.

In this program, "valid" means the logo data has crc32 0x46195417 - this is probably not how actual BIOS verifies it, but there does exist logo data with this crc32 that is also allowed by several actual BIOS revisions. 

Example error traceback when the logo data does not have the expected crc32:
```
Traceback (most recent call last):
  File "gbsum.py", line 105, in <module>
    main(*sys.argv) # usage: python gbsum.py { -c -OR- -v } FILE.GB  -OR-  python gbsum.py FILE.GB OUTFILE.GB
  File "gbsum.py", line 77, in main
    EXPECTED_LOGO_CHECKSUM)) + '\n' + vlogo(cart[0x104:][:48])
AssertionError: Zock2000VFame.0CFA.gb: logo checksum mismatch: computed D2B57657 vs. expected 46195417
⣿⢆⢸⡇⣛⢀⡀⣀⠠⣶⠄⣀⣀⠀⣀⢀⡀⠀⣀⣸⡇⢀⣀⡀
⣿⠈⢾⡇⣿⠸⣇⡿⠀⣿⠸⣇⣸⠇⢿⣸⠇⢿⣀⣸⠇⢿⣒⡛
```
## Logo display
It can display the "logo" section of the header a few different ways, dependent on CHARSET/DEFAULT_CHARSET environment variables or the current locale setting.
Example from a V.Fame cartridge I have:

Unicode Braille patterns _(I apologize for the Braille abuse. Unicode lacks 2x4 mosaic patterns apart from Braille, even though some old PC's have those in their character sets - e.g. Kaypro 2x)_
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
## BONUS: `gbextract.py`

A tool is provided for extracting GB ROM-shaped blobs from inside larger files. See `gbextract.py` for details.
