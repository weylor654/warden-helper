# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['warden_helper_menu.py'],
    pathex=[],
    binaries=[],
    datas=[('E:\\vs_code(saves)\\Corvax_warden_helper\\warden_helper_logic.py', '.'), ('E:\\vs_code(saves)\\Corvax_warden_helper\\warden_helper_ui_abridged.py', '.'), ('E:\\vs_code(saves)\\Corvax_warden_helper\\warden_helper_ui.py', '.')],
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
    icon=['E:\\vs_code(saves)\\Corvax_warden_helper\\data\\warden_helper_icon.ico'],
)
