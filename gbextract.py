#!/usr/bin/env python3

import sys, os.path

rom_size_shift_addr = 0x148
logo_addr = 0x120
logo_bytes = bytes(
    [int(x, 16) for x in "dd dd d9 99 bb bb 67 63  6e 0e ec cc dd dc 99 9f".split()]
)


def gbextract(input_filename):
    """
    Given an input filename `input_filename`, scan it for blobs that resemble GB ROM images and write each one to a separate file in the current directory. Output filenames are derived from the non-extension part of the input file basename with a numeric tail like `_1`, `_2`, etc. and a `.gb` extension. No header checksum validation or other checks are performed on the data, and the internal size byte is assumed to be accurate.
    """
    buf = open(input_filename, "rb").read()
    j = 0
    while True:
        i = buf.find(logo_bytes)
        if not (i >= 0):
            break
        j = j + 1
        gb, buf = (
            buf[
                i
                - logo_addr : i
                - logo_addr
                + ((32 * 1024) << buf[i - logo_addr + rom_size_shift_addr])
            ],
            buf[i + len(logo_bytes) :],
        )
        output_filename = (
            os.path.splitext(os.path.basename(input_filename))[0] + "_" + str(j) + ".gb"
        )
        if os.path.exists(output_filename):
            print(f"removing previous {output_filename}")
            os.unlink(output_filename)
        print(output_filename, len(gb))
        open(output_filename, "wb").write(gb)


if __name__ == "__main__":
    _, input_filename = sys.argv
    gbextract(input_filename)
