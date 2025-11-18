from services.email_service import send_email


def main():
    print("System Monitor Started")

    # Example usage of send_email function
    success = send_email(
        to_address="sumon.bd969@gmail.com",
        subject="System Monitor Notification",
        body="The system monitor has started successfully."
    )

    if success:
        print("Notification email sent successfully.")
    else:
        print("Failed to send notification email.")




if __name__ == "__main__":
    main()
