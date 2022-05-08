#!/usr/bin/env python

import sys
import os
import opencc
import subprocess
from DualSubCreator import write_dual_subs

def extract_and_create_dual_subs(file, eng_track, chi_track, convert_to_traditional):
    if(file[-4:] != ".mkv"):
        raise Exception("Expected mkv file")
    eng_path = "eng.srt"
    chi_path = "chi.srt"
    eng_str = "{0}:{1}".format(eng_track, eng_path)
    chi_str = "{0}:{1}".format(chi_track, chi_path)
    subprocess.run(["mkvextract", file, "tracks", eng_str, chi_str], capture_output=True)
    if convert_to_traditional:
        with open(chi_path, "r") as f:
            lines = f.readlines()
        chi_t_path = "chi_t.srt"
        converter = opencc.OpenCC('s2t.json') 
        with open(chi_t_path, "w") as f:
            for line in lines:
                f.write(converter.convert(line))
    out_path = file[:-4]+".dual-sub.ass"
    write_dual_subs(chi_path if not convert_to_traditional else chi_t_path, eng_path, out_path)
    os.remove(eng_path)
    os.remove(chi_path)
    if convert_to_traditional:
        os.remove(chi_t_path)

if __name__ == "__main__":
    arguments = list(sys.argv)
    file_path = arguments[1]
    eng_track = int(arguments[2])
    chi_track = int(arguments[3])
    convert = bool(arguments[4])
    extract_and_create_dual_subs(file_path, eng_track, chi_track, convert)
