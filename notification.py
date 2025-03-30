import platform
import subprocess


def send_notification(title: str, message: str) -> None:
    if platform.system() == "Darwin":  # macOS
        try:
            subprocess.run([
                "osascript",
                "-e",
                f'display notification "{message}" with title "{title}"'
            ])
        except:
            print(f"{title}: {message}")
    elif platform.system() == "Linux":
        try:
            subprocess.run([
                "notify-send",
                title,
                message
            ])
        except:
            print(f"{title}: {message}")
    elif platform.system() == "Windows":
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message)
        except:
            print(f"{title}: {message}")
    else:
        print(f"{title}: {message}")
