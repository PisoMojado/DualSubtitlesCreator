#!/usr/bin/env python

import sys
import chardet
import re

def time_conv(timeStr):
    timeAry = timeStr.split(":")
    totalTime = 0
    totalTime += (int(timeAry[0])*360000)
    totalTime += (int(timeAry[1])*6000)
    totalTime += int(timeAry[2].replace(".",""))
    return totalTime

def align_subs(mastArray, subMastArray, auto_shift_amount=50):
    timeThresh = auto_shift_amount
    onSubLine = 0
    for i in range(len(mastArray)):
        mastTime = [time_conv(mastArray[i][0]),time_conv(mastArray[i][1])]
        while onSubLine < len(subMastArray):
            subMastTime = [time_conv(subMastArray[onSubLine][0]),time_conv(subMastArray[onSubLine][1])]
            difs = [mastTime[0] - subMastTime[0], mastTime[1] - subMastTime[1]]
            if abs(difs[0]) <= timeThresh and abs(difs[1]) <= timeThresh:
                subMastArray[onSubLine][0] = mastArray[i][0]
                subMastArray[onSubLine][1] = mastArray[i][1]
                onSubLine += 1
                break
            elif difs[0] < 0 or difs[1] < 0:
                break
            else:
                onSubLine += 1
    return [mastArray, subMastArray]

def color_conv(colorStr, opcty=100):
    opcty = 100 - opcty
    opcty = str(hex(round(opcty * 2.55)))[2:]
    if len(opcty) == 1:
        opcty = "0" + opcty
    col = "&H" + opcty + colorStr[-2:] + colorStr[2:4] + colorStr[:2]
    return col

def time_shift(timeStr, shift):
    timeAryShftd = []
    totalTime = time_conv(timeStr)
    totalTime += shift
    timeAryShftd.append(str(int(totalTime/360000)))
    timeAryShftd.append(str(int((totalTime%360000)/6000)))
    timeAryShftd.append(str(int(((totalTime%360000)%6000)/100)))
    timeAryShftd.append(str(int(((totalTime%360000)%6000)%100)))
    for i in range(1,3):
        if len(timeAryShftd[i]) == 1:
            timeAryShftd[i] = ("0" + timeAryShftd[i])
    timeStrShftd = (timeAryShftd[0] + ":" + timeAryShftd[1] + ":" + timeAryShftd[2] + "." + timeAryShftd[3])
    return timeStrShftd

def file_to_array(sub_file, manual_shift_amount=None, manual_sub_shift_amount=None):
    if (sub_file[-4:] == ".srt"):
        sub_file = sub_file.encode(encoding="UTF-8")
        f = open(sub_file, "rb").read()
        detected = (chardet.detect(f)["encoding"])
        f = open(sub_file, "r", encoding=detected)
        lines = f.readlines()
        del(f)
    else:
        raise Exception("Expected an srt file")

    indx = -1
    strPart = False
    splitArray = []

    for line in lines:
        if "-->" in line:
            indx += 1
            timeSplit = line.replace(",",".").split(" --> ")
            splitArray.append([timeSplit[0][1:-1], timeSplit[1].replace("\n","")[1:-1], ""])
            strPart = True
        elif line == "\n":
            strPart = False
        elif strPart:
            splitArray[indx][2] += line
    for i in range(len(splitArray)):
        splitArray[i][2] = splitArray[i][2].rstrip().replace("\n","\\n")
        if len(re.findall("<.>",splitArray[i][2])) > 0:
            splitArray[i][2] = splitArray[i][2].replace("<i>","{\\i1}")
            splitArray[i][2] = splitArray[i][2].replace("<b>","{\\b1}")
            splitArray[i][2] = splitArray[i][2].replace("<u>","{\\u1}")
        splitArray[i][2] = re.sub("<.*?>","",splitArray[i][2])
    shift = 0
    if manual_shift_amount != None:
        shift += manual_shift_amount
    if manual_sub_shift_amount != None:
        shift += manual_sub_shift_amount
    if shift > 0:
        for i in range(len(splitArray)):
            splitArray[i][0] = time_shift(splitArray[i][0], shift)
            splitArray[i][1] = time_shift(splitArray[i][1], shift)
    return splitArray

def get_settings_lines():
    #Settings
    font_size = 20
    border_style = 1 # settings default is 0
    out_width = 1
    mast_colors = [color_conv("FFFFFF"), color_conv("000000", 100), color_conv("000020", 100)]
    mast_loc = 2 # settings default is 1
    shadow_size = 0 
    sub_mast_loc = 8 # settings default is 0
    sub_mast_colors = [color_conv("FFFFFF"), color_conv("000000", 100), color_conv("000020", 100)]

    header = "[Script Info]\n; Generated by Michael Jones with help from mattrangel.net\nTitle: Subtitles\nScriptType: v4.00+\nCollisions: Normal\nPlayDepth: 0\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    default_style = "Style: Default, Arial, {3}, {0}, &H0300FFFF, {1}, {2}, 0, 0, {4}, {5}, {6}, {7}, 10, 10, 10, 1\n".format(mast_colors[0], mast_colors[1], mast_colors[2], font_size, border_style, out_width, shadow_size, mast_loc)
    secondary_style = "Style: Secondary, Arial, {3}, {0}, &H0300FFFF, {1}, {2}, 0, 0, {4}, {5}, {6}, {7}, 10, 10, 10, 1\n\n".format(sub_mast_colors[0], sub_mast_colors[1], sub_mast_colors[2], font_size, border_style, out_width, shadow_size, sub_mast_loc)
    events="[Events]\nFormat: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text\n"
    return [header, default_style, secondary_style, events]


def write_dual_subs(first_file, second_file, output_path):
    mast_array,sub_array = align_subs(file_to_array(first_file), file_to_array(second_file))
    mast_len = len(mast_array)
    sub_len = len(sub_array)
    settings = get_settings_lines()

    with open(output_path, "w") as f:
        for line in settings:
            f.write(line)
        for i in range(mast_len):
            f.write("Dialogue: 0," + mast_array[i][0] + "," + mast_array[i][1]  + ",Default,,0,0,0,," + mast_array[i][2]  + "\n")
        for i in range(sub_len):
            f.write(("Dialogue: 0," + sub_array[i][0] + "," + sub_array[i][1] + ",Secondary,,0,0,0,," + sub_array[i][2] + "\n"))

if __name__ == "__main__":
    arguments = list(sys.argv)
    first_file = arguments[1]
    second_file = arguments[2]
    output_path = arguments[3]
    write_dual_subs(first_file, second_file, output_path)
