import time
import win32gui
import win32con
import win32ui
import smtplib
from email.mime.text import MIMEText
from PIL import Image, ImageChops, ImageGrab

app_class = "classgoeshere" # the app class name you want to monitor. use check_classes.py for this
email = 'emailaddress@gmail.com' # your email address

# Get the window icon
def get_window_icon(hwnd):
    icon_handle = win32gui.SendMessage(hwnd, win32con.WM_GETICON, win32con.ICON_SMALL, 0)
    if not icon_handle:
        icon_handle = win32gui.GetClassLong(hwnd, win32con.GCL_HICONSM)

    if not icon_handle:
        return None

    icon_info = win32gui.GetIconInfo(icon_handle)
    icon_bitmap = icon_info[3]  # hbmColor handle

    # ImageGrab to create an image from the clipboard containing the icon bitmap
    ImageGrab.grabclipboard()
    return ImageGrab.grab()


def is_app_icon_changed(hwnd):
    icon1 = get_window_icon(hwnd)
    time.sleep(0.5)  # Checks icon2 0.5 seconds after icon1
    icon2 = get_window_icon(hwnd)
    return not ImageChops.difference(icon1, icon2).getbbox() # false if no difference, true if there is a difference


def send_email(subject, body, to_email):
    from_email = email  # The email to be sent FROM
    password = 'password'     # Replace with your app password if you 2FA, otherwise regular email password

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server: # for outlook, use: smtp.office365.com
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())


def stop_monitoring():
    # Exit the script gracefully
    import sys
    sys.exit(0)

    
if __name__ == "__main__":
    class_name = app_class 
    hwnd = win32gui.FindWindow(class_name, None)

    if hwnd:
        your_email = email  # The email to be sent FROM

        prev_icon_state = is_app_icon_changed(hwnd)  # sets the initial state of the app icon. false if no difference, true if there is a difference
        email_sent = False  # Flag to track if the email has been sent
        print("Currently monitoring...")

        try:
            while not email_sent: # continue as long as email_sent = False. when it's True, it will jump to stop_monitoring()
                icon_state = is_app_icon_changed(hwnd)  # check the current state of the app icon difference. # false if no difference, true if there is a difference
                if icon_state != prev_icon_state:  # if there IS a difference, run inside of this block
                    if icon_state: #  if true aka there is a difference, run the inside code to send an email, otherwise jump to prev_icon_state = icon_state
                        subject = "Your Toad Query is finished!"
                        body = "Hooray, your Toad Query has finished running!"
                        send_email(subject, body, your_email)
                        email_sent = True  # Set the flag to True to indicate that the email has been sent. this will stop the loop
                    prev_icon_state = icon_state # if there IS NOT a difference, run through the loop again
                time.sleep(2)  # waits 2 seconds before iterating again through the loop. so every 2 seconds it'll run a loop to test the difference in icons 0.5 seconds apart to see if it changed

            # this stop_monitoring function stops the script once the email is sent
            print("Query finished and email sent. Closing script...")
            stop_monitoring()
        except KeyboardInterrupt:
            print("Script interrupted. Exiting...")
    else:
        print("Window not found.")