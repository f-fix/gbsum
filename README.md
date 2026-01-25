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
... followed by a display of the rest of the logo data

With `FILE.GB OUTFILE.GB`, a valid header in `FILE.GB` will cause a new `OUTFILE.GB` to be created (or overwritten!) containing a copy of `FILE.GB` with the checksum updated to reflect the contents.

In this program, "valid" means the logo data has crc32 0x46195417 - this is probably not how actual BIOS verifies it, but there does exist logo data with this crc32 that is also allowed by several actual BIOS revisions. 

It can display the "logo" section of the header a few different ways, dependent on CHARSET/DEFAULT_CHARSET environment variables or the current locale setting.
Example from a V.Fame cartridge I have:
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
