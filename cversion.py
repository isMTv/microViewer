from platform import python_version, architecture

arc = architecture()


def set_components_version(form):
    form.label_mv_v.setText(f"v1.3.5 ({arc[0]})")
    form.label_python_v.setText(python_version())
    form.label_qt_v.setText("6.3.1")
    form.label_nuitka_v.setText("1.1.6")
    form.label_kitty_v.setText("0.76.0.11")
    form.label_ultravnc_v.setText("1.3.8.1")
