"""
Unit tests for email_service module.
Tests email sending functionality with mocked SMTP connections.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
from pathlib import Path
import smtplib
from services.email_service import send_email


class TestSendEmail:
    """Test cases for send_email function"""
    
    @patch('services.email_service.smtplib.SMTP')
    def test_simple_email_success(self, mock_smtp):
        """Test sending a simple plain text email"""
        # Setup mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        result = send_email(
            to_address="test@example.com",
            subject="Test Subject",
            body="Test body content"
        )
        
        # Assertions
        assert result is True
        mock_server.ehlo.assert_called()
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        mock_server.send_message.assert_called_once()
    
    @patch('services.email_service.smtplib.SMTP')
    def test_email_with_html_body(self, mock_smtp):
        """Test sending email with HTML content"""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        result = send_email(
            to_address="test@example.com",
            subject="HTML Test",
            body="Plain text",
            html_body="<h1>HTML content</h1>"
        )
        
        assert result is True
        # Verify send_message was called
        assert mock_server.send_message.called
    
    @patch('services.email_service.smtplib.SMTP')
    def test_email_with_multiple_recipients(self, mock_smtp):
        """Test sending email to multiple recipients"""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        recipients = ["user1@example.com", "user2@example.com", "user3@example.com"]
        
        result = send_email(
            to_address=recipients,
            subject="Multiple Recipients",
            body="Test body"
        )
        
        assert result is True
        mock_server.send_message.assert_called_once()
    
    @patch('services.email_service.smtplib.SMTP')
    def test_email_with_cc_and_bcc(self, mock_smtp):
        """Test sending email with CC and BCC"""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        result = send_email(
            to_address="primary@example.com",
            subject="CC/BCC Test",
            body="Test body",
            cc="cc@example.com",
            bcc=["bcc1@example.com", "bcc2@example.com"]
        )
        
        assert result is True
    
    @patch('services.email_service.smtplib.SMTP')
    @patch('services.email_service.Path')
    def test_email_with_attachment_success(self, mock_path, mock_smtp):
        """Test sending email with valid attachments"""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Mock file operations
        mock_file_path = MagicMock(spec=Path)
        mock_file_path.exists.return_value = True
        mock_file_path.name = "test_file.pdf"
        mock_path.return_value = mock_file_path
        
        mock_file_content = b"fake file content"
        
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            result = send_email(
                to_address="test@example.com",
                subject="With Attachment",
                body="Body text",
                attachments=["test_file.pdf"]
            )
        
        assert result is True
        mock_server.send_message.assert_called_once()
    
    @patch('services.email_service.smtplib.SMTP')
    @patch('services.email_service.Path')
    def test_email_with_missing_attachment(self, mock_path, mock_smtp):
        """Test sending email when attachment file doesn't exist"""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Mock file that doesn't exist
        mock_file_path = MagicMock(spec=Path)
        mock_file_path.exists.return_value = False
        mock_path.return_value = mock_file_path
        
        result = send_email(
            to_address="test@example.com",
            subject="Missing Attachment",
            body="Body text",
            attachments=["nonexistent.pdf"]
        )
        
        # Should still succeed but log warning
        assert result is True
    
    @patch('services.email_service.smtplib.SMTP')
    @patch('services.email_service.Path')
    def test_email_with_multiple_attachments(self, mock_path, mock_smtp):
        """Test sending email with multiple attachments"""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Mock multiple files
        mock_file_path = MagicMock(spec=Path)
        mock_file_path.exists.return_value = True
        mock_file_path.name = "file.pdf"
        mock_path.return_value = mock_file_path
        
        with patch('builtins.open', mock_open(read_data=b"content")):
            result = send_email(
                to_address="test@example.com",
                subject="Multiple Attachments",
                body="Body text",
                attachments=["file1.pdf", "file2.png", "file3.txt"]
            )
        
        assert result is True
    
    @patch('services.email_service.smtplib.SMTP')
    def test_smtp_exception_handling(self, mock_smtp):
        """Test handling of SMTP exceptions"""
        mock_server = MagicMock()
        mock_server.send_message.side_effect = smtplib.SMTPException("SMTP Error")
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        result = send_email(
            to_address="test@example.com",
            subject="Error Test",
            body="Body text",
            raise_on_error=False
        )
        
        assert result is False
    
    @patch('services.email_service.smtplib.SMTP')
    def test_smtp_exception_raised_when_configured(self, mock_smtp):
        """Test that SMTP exception is raised when raise_on_error=True"""
        mock_server = MagicMock()
        mock_server.send_message.side_effect = smtplib.SMTPException("SMTP Error")
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        with pytest.raises(smtplib.SMTPException):
            send_email(
                to_address="test@example.com",
                subject="Error Test",
                body="Body text",
                raise_on_error=True
            )
    
    @patch('services.email_service.smtplib.SMTP')
    def test_generic_exception_handling(self, mock_smtp):
        """Test handling of generic exceptions"""
        mock_server = MagicMock()
        mock_server.login.side_effect = Exception("Unexpected error")
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        result = send_email(
            to_address="test@example.com",
            subject="Error Test",
            body="Body text",
            raise_on_error=False
        )
        
        assert result is False
    
    @patch('services.email_service.smtplib.SMTP')
    def test_connection_timeout_handling(self, mock_smtp):
        """Test handling of connection timeout"""
        mock_smtp.side_effect = TimeoutError("Connection timeout")
        
        result = send_email(
            to_address="test@example.com",
            subject="Timeout Test",
            body="Body text",
            raise_on_error=False
        )
        
        assert result is False
    
    @patch('services.email_service.smtplib.SMTP')
    def test_authentication_failure(self, mock_smtp):
        """Test handling of authentication failure"""
        mock_server = MagicMock()
        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, "Authentication failed")
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        result = send_email(
            to_address="test@example.com",
            subject="Auth Test",
            body="Body text",
            raise_on_error=False
        )
        
        assert result is False
    
    @patch('services.email_service.smtplib.SMTP')
    def test_smtp_connection_parameters(self, mock_smtp):
        """Test that SMTP connection uses correct parameters"""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        with patch('services.email_service.settings') as mock_settings:
            mock_settings.SMTP_HOST = "smtp.test.com"
            mock_settings.SMTP_PORT = 587
            mock_settings.SMTP_USER = "user@test.com"
            mock_settings.SMTP_PASSWORD = "password123"
            mock_settings.SMTP_TIMEOUT = 15
            
            send_email(
                to_address="test@example.com",
                subject="Connection Test",
                body="Body text"
            )
            
            # Verify SMTP was called with correct parameters
            mock_smtp.assert_called_once()
            call_args = mock_smtp.call_args
            assert call_args[0][0] == "smtp.test.com"
            assert call_args[0][1] == 587


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
