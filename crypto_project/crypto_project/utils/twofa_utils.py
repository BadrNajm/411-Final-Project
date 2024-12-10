import logging
import pyotp
import qrcode

from PIL import Image

def configure_logger(logger: logging.Logger, log_level=logging.INFO) -> None:
    """
    Configures the logger with the specified log level.

    Args:
        logger (logging.Logger): The logger to configure.
        log_level (int): The log level (default is logging.INFO).
    """
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)

# 2FA Utilities

def generate_totp_secret() -> str:
    """
    Generate a unique base32 TOTP secret key.

    Returns:
        str: A base32-encoded secret key.
    """
    return pyotp.random_base32()

def generate_qr_code(username: str, totp_secret: str, issuer_name: str = "CryptoApp") -> Image.Image:
    """
    Generate a QR code for the TOTP secret.

    Args:
        username (str): The username for the TOTP setup.
        totp_secret (str): The TOTP secret key.
        issuer_name (str): The name of the application or issuer (default is "CryptoApp").

    Returns:
        Image.Image: A PIL image object of the QR code.
    """
    totp = pyotp.TOTP(totp_secret)
    provisioning_uri = totp.provisioning_uri(name=username, issuer_name=issuer_name)
    qr = qrcode.make(provisioning_uri)
    return qr

def verify_totp_token(totp_secret: str, token: str) -> bool:
    """
    Verify a TOTP token using the user's secret.

    Args:
        totp_secret (str): The TOTP secret key.
        token (str): The token to verify.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    totp = pyotp.TOTP(totp_secret)
    return totp.verify(token)

# Save QR code 
def save_qr_code_image(qr_image: Image.Image, file_path: str) -> None:
    """
    Save a QR code image to a file.

    Args:
        qr_image (Image.Image): The PIL image object of the QR code.
        file_path (str): The path to save the image.
    """
    qr_image.save(file_path)

