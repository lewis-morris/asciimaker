import AsciiMaker
asc = AsciiMaker.Maker(w_size=200, block_size=2, invert=False, colour=True, characters="8&@%#", background=True, font_multiplier=3)

asc.write_gif("examples/clap.gif",output="out4.html", frame_time=100)

