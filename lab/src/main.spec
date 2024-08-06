# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('gui/graph.ui','./gui'),
        ('gui/adjust.ui','./gui'),
        ('dependecies/pyside6-uic.exe','.'),
        ('dependecies/base.qss','./pyqtribbon/styles'),
        ('dependecies/default.qss','./pyqtribbon/styles'),
        ('dependecies/debug.qss','./pyqtribbon/styles'),
        ('dependecies/linking.png','./pyqtribbon/icons'),
        ('dependecies/down.png','./pyqtribbon/icons'),
        ('dependecies/up.png','./pyqtribbon/icons'),
        ('dependecies/help.png','./pyqtribbon/icons'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Image Processing',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    console=False,
    icon='lab.ico'
)
