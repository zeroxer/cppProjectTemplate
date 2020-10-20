#coding=utf-8

"""项目构建/运行/调试脚本

Usage:
    manage.py init <arch>
    manage.py build <arch> [--debug=<isDebug>]
    manage.py run <arch> [--debug=<isDebug>]
    manage.py debug <arch>

Arguments:
    arch    架构: x64 或 x86
    isDebug 调试模式：0 或 1

Options:
    -d --debug=<isDebug>    Debug mode [default: 0]
    -h --help               Show this screen.
    -v --version            Show version.
    -r --rebuild            Rebuild and run.
"""

import os
from docopt import docopt
import pprint, vswhere
import subprocess
from dirsync import sync

rootDir = os.getcwd()
resDir = os.path.join(rootDir, 'res')
buildRootDir = os.path.join(rootDir, '.Build')
buildDebugDir = os.path.join(buildRootDir, 'Debug')
buildReleaseDir = os.path.join(buildRootDir, 'Release')
buildResDir = os.path.join(buildRootDir, 'res')

def cleanBuildDir():
    # if os.path.exists('mainApp.exe'):
    #     os.remove('mainApp.exe')
    pass

# 初始化VC环境: rc.exe, cl.exe, link.exe
def initVC(arch):
    VSDir = vswhere.get_latest_path()
    VCEnvInitBatPath = os.path.join(VSDir, 'VC/Auxiliary/Build/vcvars64.bat')
    VCEnvInitBatPath = os.path.abspath(VCEnvInitBatPath)
    if (not VSDir) or (not os.path.exists(VCEnvInitBatPath)):
        print('[Error] Please install Visual Studio: https://visualstudio.microsoft.com/')
        return

    print('[Info] init vc env:', arch)
    with open('initvc.bat', 'w') as initFile:
        initFile.write('@echo off\n')
        initFile.write('call "' + VCEnvInitBatPath + '" > nul')
    print('[Info] 正在初始化 VC++ 开发环境，请稍等...')

def buildProject(arch, isDebug):
    print('[Info] build project:', arch)

    # MSBuildExePath = os.path.join(VSDir, 'MSBuild./Current/Bin/MSBuild.exe')
    # MSBuildExePath = os.path.abspath(MSBuildExePath)
    # print(MSBuildExePath)

    # ENTRY: 
    # - mainCRTStartup (or wmainCRTStartup)
    # - WinMainCRTStartup (or wWinMainCRTStartup)
    if isDebug: # Debug
        print('Debug Mode --- Debug Debug Debug')
        if not os.path.exists(buildDebugDir):
            os.mkdir(buildDebugDir)
        os.chdir(buildDebugDir)
        os.system('cl /c /Od /Zi /Ob0 /Fd.\ /Fo.\ /TP /MP ../../src/*.cpp /EHsc /utf-8 /std:c++17 /DEBUG /D UNICODE')
        os.system('link /out:mainApp.exe /ENTRY:mainCRTStartup /SUBSYSTEM:CONSOLE /machine:x64 /DEBUG *.obj user32.lib gdi32.lib')

    else: # Release
        print('Release Mode --- Release Release Release')
        if not os.path.exists(buildReleaseDir):
            os.mkdir(buildReleaseDir)
        os.chdir(buildReleaseDir)
        os.system('cl /c /Fd.\ /Fo.\ /TP /MP ../../src/*.cpp /EHsc /utf-8 /std:c++17 /D UNICODE')
        os.system('link /out:mainApp.exe /ENTRY:mainCRTStartup /SUBSYSTEM:CONSOLE /machine:x64 *.obj user32.lib gdi32.lib')

    # 复制资源文件
    if os.path.exists(resDir):
        if isDebug:
            buildResDir = os.path.join(buildDebugDir, 'res')
        else:
            buildResDir = os.path.join(buildReleaseDir, 'res')
        if not os.path.exists(buildResDir):
            os.mkdir(buildResDir)
        sync(resDir, buildResDir, 'sync')

    # 返回原目录
    os.chdir(rootDir)

def runProject(arch, isDebug=False):
    # print('[Info] run project:', arch)
    if isDebug:
        os.chdir(buildDebugDir)
        os.system('call mainApp.exe')
    else:
        os.chdir(buildReleaseDir)
        os.system('call mainApp.exe')

def debugProject(arch):
    print('[Info] debug project:', arch)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Project Tool 0.0.1')
    arch = arguments['<arch>']
    debug = False if (arguments['--debug'] == '0') else True

    if not os.path.exists(buildRootDir):
        os.mkdir(buildRootDir)
    os.chdir(buildRootDir)

    if arguments['init']:
        initVC(arch)
    elif arguments['build']:
        cleanBuildDir()
        buildProject(arch, debug)
    elif arguments['run']:
        runProject(arch, debug)
    elif arguments['debug']:
        debugProject(arch)
