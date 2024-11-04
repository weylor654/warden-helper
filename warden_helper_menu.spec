# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['warden_helper_menu.py'],
    pathex=[],
    binaries=[],
    datas=[('my_bar.py', '.'), ('warden_helper_logic.py', '.'), ('warden_helper_ui_abridged.py', '.'), ('warden_helper_ui.py', '.'), ('data/krest.png', 'data'), ('data/pin.png', 'data'), ('data/under_line.png', 'data'), ('data/unpin.png', 'data'), ('data/warden_helper_icon.png', 'data')],
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
    name='warden_helper_menu',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['data\\warden_helper_icon.ico'],
)
