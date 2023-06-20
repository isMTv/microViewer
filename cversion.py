from os import chdir
from pathlib import Path
from platform import python_version, architecture
from win32api import GetFileVersionInfo, HIWORD, LOWORD

mv_version = "1.3.7"
qt_version = "6.3.1" # 5.15.7 | 6.3.1
nuitka_version = "1.3.8"

dir_path = Path.cwd()
chdir(dir_path)
path_kitty = Path(f"bin/kitty.exe")
path_uvnc = Path(f"bin/uvnc/winvnc.exe")
arc = architecture()


def set_title_app_version(window: any) -> None:
    window.setWindowTitle(f"microViewer v{mv_version}")


def get_app_version(app_path: str) -> str:
    try:
        file_info = GetFileVersionInfo(app_path, "\\")
        ms_file_ver = file_info['FileVersionMS']
        ls_file_ver = file_info['FileVersionLS']
        # major.minor.build.revision;
        ver_mmbr = (str(HIWORD(ms_file_ver)), str(LOWORD(ms_file_ver)), str(HIWORD(ls_file_ver)), str(LOWORD(ls_file_ver)))

        ver = ".".join(ver_mmbr)
    except Exception:
        ver = "N/A"
    return ver


def set_components_version(form: any) -> None:
    form.label_mv_v.setText(f"v{mv_version} ({arc[0]})")
    form.label_python_v.setText(python_version())
    form.label_qt_v.setText(f"{qt_version}")
    form.label_nuitka_v.setText(f"{nuitka_version}")
    form.label_kitty_v.setText(f"{get_app_version(str(path_kitty))}")
    form.label_ultravnc_v.setText(f"{get_app_version(str(path_uvnc))}")
