"""
Train SVM for profanities.

Adapted from `https://towardsdatascience.com/
 building-a-better-profanity-detection-library-with-scikit-learn-3638b2f2c4c2`
"""
from pathlib import Path
from tempfile import mkdtemp
from typing import IO, Any, Union

import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


def preprocessor() -> np.ndarray:
    """Get the vectorizer."""
    return TfidfVectorizer(stop_words="english", min_df=0.0001)


def model() -> BaseEstimator:
    """Get the model."""
    model = LinearSVC(dual=False, tol=1e-2, max_iter=1e5)
    return CalibratedClassifierCV(base_estimator=model)


def get_pipeline(**pipeline_kwargs: Any) -> Pipeline:
    """Get the machine learning pipeline."""
    return Pipeline(
        steps=[("vectorizer", preprocessor()), ("clf", model())], **pipeline_kwargs
    )


def train(text: pd.Series, labels: pd.Series, **tmpdir_kwargs: Any) -> Pipeline:
    """Train ML pipeline."""
    cache_dir = mkdtemp(**tmpdir_kwargs)
    pipe = get_pipeline(memory=cache_dir)
    pipe.fit(text, labels)
    return pipe


def predict(pipe: Pipeline, text: pd.Series) -> np.ndarray:
    """Predict toxicity (`is_toxic=True`) probabilities from ML pipeline."""
    predictions = pipe.predict_proba(text)
    return predictions[:, pipe.classes_].flatten()


def save_model(pipeline: Pipeline, file: Union[str, Path, IO]) -> None:
    """Save the model pipeline."""
    joblib.dump(pipeline, file, compress=("gzip", 3))


def load_model(file: Union[str, Path, IO]) -> Pipeline:
    """Load the model pipeline."""
    return joblib.load(file)
