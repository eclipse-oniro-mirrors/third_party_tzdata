#!/usr/bin/env python3
# coding=utf-8/# -*- coding: utf-8 -*-
#
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
 
import os
import sys
import shutil
import subprocess
import getopt
from zone_compactor import ZoneCompactor
 
script_path = os.path.dirname(os.path.abspath(__file__))
iana_path = os.path.join(script_path, "..", "..", "data", "iana")
posix_path = os.path.join(iana_path, "..", "prebuild", "posix")
zic_path = os.path.join(iana_path, "..", "prebuild", "tool", "linux")
 
tool_bin_dir = ""
 
try:
    opts, args = getopt.getopt(sys.argv[1:], "o:b")
except getopt.GetoptError:
    print("unkonw argument")
    sys.exit(1)
 
for opt, arg in opts:
    if opt == "-o":
        tool_bin_dir = arg
 
print(f"tool_bin_dir--@@:{tool_bin_dir}")
 
subprocess.run(["make", "-C", iana_path], check=True)
 
os.makedirs(zic_path, exist_ok=True)
os.makedirs(posix_path, exist_ok=True)
 
zic_src = os.path.join(iana_path, "zic")
if os.path.exists(zic_src):
    zicFile = os.path.join(zic_path, "zic")
    if os.path.exists(zicFile):
        os.remove(zicFile)
    shutil.move(zic_src, zic_path)
 
state_names = ['africa', 'antarctica', 'asia', 'australasia', 'europe', 'etcetera', 'northamerica', 'southamerica', 'backward']
for name in state_names:
    zic_bin = os.path.join(zic_path, "zic")
    subprocess.run([zic_bin, "-d", os.path.join(iana_path, "zoneinfo"), os.path.join(iana_path, name)], check=True)
 
if os.path.exists(posix_path):
    for item in os.listdir(posix_path):
        item_path = os.path.join(posix_path, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
 
zoneinfo_path = os.path.join(iana_path, "zoneinfo")
for item in os.listdir(zoneinfo_path):
    src = os.path.join(zoneinfo_path, item)
    dst = os.path.join(posix_path, item)
    shutil.move(src, dst)
 
toolBinDirList = list(filter(None, tool_bin_dir.split(os.sep)))
print(toolBinDirList)
toolBinDirListStr = os.path.join(*toolBinDirList)
output_path = os.path.join(script_path, "..", "..", "..", "..", toolBinDirListStr, "thirdparty", "tzdata", "output")
print(output_path)
 
os.makedirs(os.path.join(script_path, "..", "..", "data", "prebuild", "posix", "output"), exist_ok=True)
print("compile done")
 
zone_compactor = os.path.join(script_path, "zone_compactor.py")
config_file = os.path.join(script_path, "..", "..", "data", "prebuild", "normal", "timezone_list.cfg")
ZoneCompactor(config_file, posix_path, output_path, "tzdata2026e")

print("package done")
sys.exit(0)