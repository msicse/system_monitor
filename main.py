from services.email_service import send_email
import services.screenshot_service as screenshot_service


def main():
    print("System Monitor Started")

    # Example usage of send_email function
    # success = send_email(
    #     to_address="sumon.bd969@gmail.com",
    #     subject="System Monitor Notification",
    #     body="The system monitor has started successfully."
    # )

    # if success:
    #     print("Notification email sent successfully.")
    # else:
    #     print("Failed to send notification email.")
    # Example usage of take_screenshot function
    screenshot_success = screenshot_service.take_screenshot()
    if screenshot_success:
        print("Screenshot taken successfully.")
    else:
        print("Failed to take screenshot.")









if __name__ == "__main__":
    main()
