from app.models.enums import WasteClass


def predict_waste_class(image_bytes: bytes) -> WasteClass:
    """
    Placeholder prediction service.

    In production, replace this with model inference from ml_model/scripts/predict.py.
    A deterministic lightweight baseline is used here to keep API responsive.
    """
    if not image_bytes:
        return WasteClass.ORGANIC

    score = sum(image_bytes[:1000]) % 3
    if score == 0:
        return WasteClass.PLASTIC
    if score == 1:
        return WasteClass.METAL
    return WasteClass.ORGANIC
