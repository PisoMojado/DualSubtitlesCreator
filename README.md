# DualSubtitlesCreator
A couple of python scripts for quickly extracting substitles, and creating dual-language ASS subtitles

# Tell me more!
I wanted to watch Chinese/Taiwanese media, and I wanted to view both languages' subtitles at the same time. It is much easier than rewinding and changing the settings in my player.
To support this, I created these scripts which extract subtitles from mkv files, optionally convert them to Traditional Chinese (if enabled), and combined to create a single ASS file that will present both simultaneously.
The main file to do all of this is ExtractAndCreateDualSubs.py. You can invoke it directly from the command line, like so:
```
./ExtractAndCreateDualSubs.py file_path 2 3 False
```

The first number is the track according to mkvinfo for the secondary (up top) subtitles, and the second number is the track for the primary (at the bottom) language you want dual-subbed. I typically make English secondary and Chinese primary.
If you are also using this for Chinese viewing, and you desire to have the Simplified Characters converted to Traditional, the final positional argument is a boolean for having the script convert the subtitles to Traditional: False won't convert the characters, True will.

Lastly, you can see that you have to know the track number in the MKV file for each language. Some media players display this, but you can also get this information using:
```
mkvinfo file_path
```
Be sure to use the numbering for "mkvextract" (typically -1 from the track number, but also shown in the output).

# Dependencies
The script was written for Python 3, it runs utilities from mkvtoolnix-cli, and uses opencc for chinese character conversion. On Arch, you can install all of them using the following:
```
pacman -S python mkvtoolnix-cli opencc 
```

# Credits
Much of the code for extracting SRT files and creating an ASS file comes from the work of [Matt Rangel](https://github.com/MattRangel/script.submerge). Please thank him for his work, and check out his Kodi plugin that I linked to.
