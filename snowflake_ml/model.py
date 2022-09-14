"""Main model functions and helpers."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd
import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    PreTrainedTokenizer,
    Trainer,
    TrainingArguments,
)
from transformers.tokenization_utils_base import BatchEncoding


class ToxicModel(torch.nn.Module):
    """PyTorch pretrained `unitary/toxic-bert` from HuggingFace model hub."""

    def __init__(
        self: ToxicModel, *from_pretrained_args: str, **from_pretrained_kwargs: Any
    ) -> None:
        """Initialize model with one extra layer to convert it to binary problem."""
        super(ToxicModel, self).__init__()
        self.pretrained = AutoModelForSequenceClassification.from_pretrained(
            *from_pretrained_args, **from_pretrained_kwargs
        )
        self.linear = torch.nn.Linear(6, 1)  # go from 6 outputs to 1
        self.sigmoid = torch.nn.Sigmoid()
        self.loss = torch.nn.BCELoss()

    def forward(
        self: ToxicModel,
        input_ids: torch.int64,
        token_type_ids: torch.int64,
        attention_mask: torch.int64,
        labels: torch.int64 = None,
    ) -> Union[Tuple[torch.FloatTensor, torch.FloatTensor], torch.FloatTensor]:
        """Perform model forward pass."""
        out = self.pretrained(
            input_ids=input_ids.squeeze(),
            token_type_ids=token_type_ids,
            attention_mask=attention_mask,
        )
        pred = self.linear(out.logits.view(-1, 6))
        pred = self.sigmoid(pred)
        if labels is not None:
            loss = self.loss(pred, labels.reshape(pred.size()))
            return loss, pred
        else:
            return pred

    def freeze_pretrained(self: ToxicModel) -> ToxicModel:
        """Freeze `BERT` layers in the model."""
        for name, param in self.named_parameters():
            if "bert" in name:
                param.requires_grad = False
        return self


class ToxicDataset(torch.utils.data.Dataset):
    """PyTorch dataset for toxic data."""

    def __init__(self, encodings: BatchEncoding, labels: List[int]) -> None:
        """Initialize dataset with inputs."""
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, i: int) -> Dict[str, torch.FloatTensor]:
        """
        Get PyTorch values for ith example in input dataset.

        PyTorch's values are represented as a dictionary that maps `input_ids`,
         `token_type_ids` and `attention_mask` to floating point values. `Input_ids` are
         numbers that map to tokens (i.e.: `['Hugging', '##face']`).
        """
        item = {key: torch.tensor(val[i]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor([self.labels[i]], dtype=torch.float)
        return item

    def __len__(self) -> int:
        """Get number of labels."""
        return len(self.labels)


def _process_data(
    data: pd.DataFrame,
    tokenizer: PreTrainedTokenizer,
    x_col: str = "comment_text",
    y_col: str = "is_toxic",
) -> ToxicDataset:
    """Tokenize data from dataframe."""
    train_encodings = tokenizer(data[x_col].tolist(), truncation=True, padding=True)
    train_dataset = ToxicDataset(train_encodings, data[y_col].tolist())
    return train_dataset


def get_model_untrained(
    *toxic_model_args: str, **toxic_model_kwargs: Any
) -> torch.nn.Module:
    """Get untrained model."""
    model = ToxicModel().freeze_pretrained(*toxic_model_args, **toxic_model_kwargs)
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    model.to(device)
    return model


def load_trained(
    model_dir: Path, model_architecture: torch.nn.Module = ToxicModel
) -> torch.nn.Module:
    """Load model weights into `model_architecture` from `model_dir/model.pth`."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model_architecture()
    if torch.cuda.device_count() > 1:
        model = torch.nn.DataParallel(model)

    with (model_dir / "model.pth").open("rb") as f:
        model.load_state_dict(torch.load(f))
    return model.to(device)


def save_model(model: torch.nn.Module, model_dir: Path) -> Path:
    """Save PyTorch model to `model_dir/model.pth`."""
    if not model_dir.is_dir():
        raise ValueError(f"{model_dir} is not a directory.")
    path = model_dir / "model.pth"
    # Recommended way: http://pytorch.org/docs/master/notes/serialization.html
    torch.save(model.cpu().state_dict(), path)
    return path.resolve().absolute()


def train(
    model: torch.nn.Module,
    tokenizer: PreTrainedTokenizer,
    output_dir: str,
    train_data: pd.DataFrame,
    eval_data: Optional[pd.DataFrame] = None,
    **trainer_kwargs: Any,
) -> torch.nn.Module:
    """Train HuggingFace model using `transformers.Trainer`."""
    train_dataset = _process_data(train_data, tokenizer=tokenizer)
    training_args = TrainingArguments(str(output_dir), **trainer_kwargs)
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_data,
    )
    trainer.train()
    return trainer.model


def predict(ds: pd.Series, model_dir: str) -> List[int]:
    """Predict toxicity based on `ToxicModel` with weights on `model_dir/model.pth`."""
    tokenizer = AutoTokenizer.from_pretrained("unitary/toxic-bert")
    model = load_trained(model_dir=Path(model_dir))
    model.eval()
    encodings = tokenizer(
        ds.tolist(), padding=True, return_tensors="pt", truncation=True
    )
    output = model(**encodings)
    return output.round().tolist()
