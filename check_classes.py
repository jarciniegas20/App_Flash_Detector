import win32gui

# def get_window_titles():
#     def is_window_visible(hwnd):
#         return win32gui.IsWindowVisible(hwnd)

#     def callback(hwnd, window_titles):
#         if is_window_visible(hwnd):
#             window_title = win32gui.GetWindowText(hwnd)
#             if window_title:
#                 window_titles.append(window_title)

#     window_titles = []
#     win32gui.EnumWindows(callback, window_titles)
#     return window_titles

# if __name__ == "__main__":
#     app_titles = get_window_titles()
#     for title in app_titles:
#         print(title)

def get_class_name(window_title):
    def callback(hwnd, extra):
        if window_title in win32gui.GetWindowText(hwnd):
            extra.append(win32gui.GetClassName(hwnd))

    toad_class_names = []
    win32gui.EnumWindows(callback, toad_class_names)
    return toad_class_names

if __name__ == "__main__":
    window_title = "Toad Data Point"  # this is just the main name of the app. Can retrieve by hovering over it or running the get_window_titles() function above

    class_names = get_class_name(window_title)
    if class_names:
        print("Class names:", class_names)
    else:
        print("Window not found.")
