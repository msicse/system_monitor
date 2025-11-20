"""
Examples demonstrating enhanced email_service features.
Run these after configuring your .env file with SMTP settings.
"""

from services.email_service import send_email


def example_simple_email():
    """Send a simple plain text email."""
    success = send_email(
        to_address="recipient@example.com",
        subject="Simple Test Email",
        body="This is a plain text email."
    )
    print(f"Simple email sent: {success}")


def example_html_email():
    """Send an email with both plain text and HTML versions."""
    success = send_email(
        to_address="recipient@example.com",
        subject="HTML Email Test",
        body="This is the plain text version.",
        html_body="""
        <html>
            <body>
                <h1>System Monitor Alert</h1>
                <p>This is an <strong>HTML</strong> email with formatting.</p>
                <ul>
                    <li>Item 1</li>
                    <li>Item 2</li>
                </ul>
            </body>
        </html>
        """
    )
    print(f"HTML email sent: {success}")


def example_email_with_attachments():
    """Send an email with file attachments."""
    success = send_email(
        to_address="recipient@example.com",
        subject="Screenshots Attached",
        body="Please find attached screenshots from today's monitoring.",
        attachments=[
            "Data/screenshots/HOSTNAME/2025-11-20/screenshot_20251120_143052_1.png",
            "logs/system_monitor.log"
        ]
    )
    print(f"Email with attachments sent: {success}")


def example_multiple_recipients():
    """Send email to multiple recipients with CC and BCC."""
    success = send_email(
        to_address=["user1@example.com", "user2@example.com"],
        subject="System Alert - Multiple Recipients",
        body="This alert is being sent to multiple team members.",
        cc="manager@example.com",
        bcc=["archive@example.com", "backup@example.com"]
    )
    print(f"Multi-recipient email sent: {success}")


def example_screenshot_notification():
    """Example: Send screenshots via email (real-world use case)."""
    from services.screenshot_service import take_screenshot
    
    # Take screenshots
    screenshots = take_screenshot()
    
    if screenshots:
        # Send email with screenshots attached
        success = send_email(
            to_address="admin@example.com",
            subject=f"System Monitor - {len(screenshots)} Screenshots Captured",
            body=f"Captured {len(screenshots)} screenshot(s) at {screenshots[0]}",
            html_body=f"""
            <html>
                <body>
                    <h2>System Monitor Report</h2>
                    <p>Successfully captured <strong>{len(screenshots)}</strong> screenshot(s):</p>
                    <ul>
                        {''.join(f'<li>{s}</li>' for s in screenshots)}
                    </ul>
                </body>
            </html>
            """,
            attachments=screenshots
        )
        print(f"Screenshot notification sent: {success}")
    else:
        print("No screenshots to send")


def example_error_handling():
    """Example showing different error handling approaches."""
    
    # Approach 1: Silent failure (returns False)
    success = send_email(
        to_address="test@example.com",
        subject="Test",
        body="Test",
        raise_on_error=False  # Default behavior
    )
    if not success:
        print("Email failed, but program continues")
    
    # Approach 2: Raise exception on failure
    try:
        send_email(
            to_address="test@example.com",
            subject="Test",
            body="Test",
            raise_on_error=True  # Will raise exception
        )
    except Exception as e:
        print(f"Caught exception: {e}")


if __name__ == "__main__":
    print("Email Service Examples")
    print("=" * 50)
    print("\nUncomment the example you want to run:\n")
    
    # Uncomment one example at a time to test:
    # example_simple_email()
    # example_html_email()
    # example_email_with_attachments()
    # example_multiple_recipients()
    # example_screenshot_notification()
    # example_error_handling()
    
    print("\nRemember to configure your .env file first!")
