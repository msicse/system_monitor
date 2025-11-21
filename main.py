from services import installed_software_service
from services.email_service import send_email
import services.screenshot_service as screenshot_service
import logging
import services.installed_software_service as installed_software_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/system_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    logger.info("System Monitor Started")
    # Take screenshots
    screenshots = screenshot_service.take_screenshot()
    # if screenshots:
    #     logger.info(f"Screenshot taken successfully: {len(screenshots)} monitor(s) captured")
    #     print(f"✓ Screenshot taken successfully: {len(screenshots)} monitor(s) captured")
    #     for path in screenshots:
    #         print(f"  - {path}")
        
    #     # Optional: Send email notification with screenshots attached
    #     success = send_email(
    #         to_address="sumon.bd969@gmail.com",
    #         subject=f"System Monitor - {len(screenshots)} Screenshots",
    #         body=f"System monitor captured {len(screenshots)} screenshot(s).",
    #         html_body=f"""
    #         <html>
    #             <body>
    #                 <h2>System Monitor Report</h2>
    #                 <p>Captured <strong>{len(screenshots)}</strong> screenshot(s).</p>
    #             </body>
    #         </html>
    #         """,
    #         attachments=screenshots
    #     )
    #     if success:
    #         logger.info("Email notification sent successfully")
    #         print("✓ Email notification sent")
    #     else:
    #         logger.warning("Failed to send email notification")
    #         print("✗ Failed to send email notification")
    # else:
    #     logger.error("Failed to take screenshot")
    #     print("✗ Failed to take screenshot")

    # software_list = installed_software_service.list_installed_software()
    # installed_software_service.save_software_list_to_file(software_list)
    # logger.info(f"Installed software list saved with {len(software_list)} entries")
    # print(f"✓ Installed software list saved with {len(software_list)} entries")



if __name__ == "__main__":
    main()
