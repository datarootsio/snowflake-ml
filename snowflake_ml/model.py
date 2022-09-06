"""Main model functions and helpers."""
from ._vendor.profanityfilter import ProfanityFilter


def get_model() -> ProfanityFilter:
    """Get classification model."""
    return ProfanityFilter()


def predict(s: str) -> float:
    """Predict whether string contains 'toxic' content."""
    return float(get_model().is_profane(s))
