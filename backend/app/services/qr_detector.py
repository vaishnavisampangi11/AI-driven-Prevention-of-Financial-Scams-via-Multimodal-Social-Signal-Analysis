import os
from pathlib import Path

from PIL import Image

from app.utils.validators import is_valid_url


def _decode_with_opencv(file_path: str):
    try:
        import cv2
    except Exception:
        return None

    try:
        image = cv2.imread(file_path)
        if image is None:
            return None
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(image)
        return data if data else None
    except Exception:
        return None


def decode_qr_image(file_path: str):
    if not Path(file_path).exists():
        raise FileNotFoundError("QR image could not be found.")

    try:
        from pyzbar.pyzbar import decode as pyzbar_decode
        image = Image.open(file_path)
        decoded_objects = pyzbar_decode(image)
        if decoded_objects:
            raw_data = decoded_objects[0].data.decode("utf-8", errors="ignore")
            return {
                "decoded_content": raw_data,
                "is_url": is_valid_url(raw_data),
                "content_type": "URL" if is_valid_url(raw_data) else "TEXT",
            }
    except Exception:
        pass

    fallback = _decode_with_opencv(file_path)
    if fallback:
        return {
            "decoded_content": fallback,
            "is_url": is_valid_url(fallback),
            "content_type": "URL" if is_valid_url(fallback) else "TEXT",
        }

    raise ValueError("No QR code could be detected in the uploaded image.")
