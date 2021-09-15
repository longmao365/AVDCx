"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['AVDCx_Main.py']
DATA_FILES = ['Data/c_number', 'Data/cloudscraper', 'Data/zhconv', 'Img']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'Img/AVDCx.icns',
    'plist': {
        'argv_emulation': True,
        'CFBundleName': "AVDCx",   # app名字
        'CFBundleDisplayName': "AVDCx",
        'CFBundleGetInfoString': "AVDCx",
        'CFBundleIdentifier': "github.com",   # 进程名字
        'CFBundleVersion': "20210915",
        'CFBundleShortVersionString': "20210915",   #版本号
        'NSHumanReadableCopyright': u"版权所有 © 2021, hermit",
        'Localization native development region':'China',
        }
    }

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app','lxml','pyquery','cloudscraper','requests','beautifulsoup4','Pillow','PyQt5','PySocks','urllib3','zhconv','langid'],
)