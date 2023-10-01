import os
from typing import Any
from transformers import BertForSequenceClassification, BertTokenizer
import joblib
import torch


def prepare_model() -> (BertForSequenceClassification, Any, torch.device):
    if os.path.exists("bert_topic_classifier") and os.path.exists("label_encoder.pkl"):
        model = BertForSequenceClassification.from_pretrained(
            "bert_topic_classifier")

        # Load the label encoder
        label_encoder = joblib.load("label_encoder.pkl")

        # Move the model to the GPU if available
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.to(device)

        print("Loaded the saved model and label encoder.")

        return model, label_encoder, device
    raise Exception("Model not found.")


def predict(model: BertForSequenceClassification, label_encoder: joblib, device: torch.device, text: str) -> str:
        # Tokenize and preprocess the text
    tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")
    tokenized_text = tokenizer.encode(text, add_special_tokens=True)
    input_ids = torch.tensor([tokenized_text], dtype=torch.long)

    # Set the model to evaluation mode
    model.eval()
    input_ids = input_ids.to(device)

    # Get predictions
    with torch.no_grad():
        outputs = model(input_ids)
        _, predicted = torch.max(outputs.logits, 1)

    # Convert the numeric prediction back to the text category
    return label_encoder.inverse_transform([predicted.item()])[0]
    

if __name__ == "__main__":
    # Define the text to be classified
    text = """Сервис Getarent (Гетарент) поможет быстро найти и забронировать автомобиль для посуточной аренды у местного жителя без залогов с включенным страхованием для поездок по городу, на природу или в дальнее путешествие"""

    predicted_category = predict(*prepare_model(), text)

    print(f"Predicted category: {predicted_category}")
