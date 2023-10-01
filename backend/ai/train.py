import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification, AdamW, get_linear_schedule_with_warmup
from torch.utils.data import DataLoader, TensorDataset, random_split
from sklearn.preprocessing import LabelEncoder
from torch.cuda.amp import autocast, GradScaler
import joblib
import os


if os.path.exists("bert_topic_classifier") and os.path.exists("label_encoder.pkl"):
    # Load the model
    exit(0)
else:
    # Load data from CSV
    data = pd.read_csv('train_dataset-2.csv')

    # Choose text and topic columns
    text_column = 'text'
    topic_column = 'topic'

    label_encoder = LabelEncoder()
    data['label'] = label_encoder.fit_transform(data[topic_column])

    tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")
    data['tokenized_text'] = data[text_column].apply(lambda x: tokenizer.encode(x, add_special_tokens=True))

    max_seq_length = max(data['tokenized_text'].apply(len))

    def pad_or_truncate(text):
        if len(text) < max_seq_length:
            padding = [tokenizer.pad_token_id] * (max_seq_length - len(text))
            text.extend(padding)
        elif len(text) > max_seq_length:
            text = text[:max_seq_length]
        return text

    data['tokenized_text'] = data['tokenized_text'].apply(pad_or_truncate)

    text_tensors = torch.tensor([text for text in data['tokenized_text']], dtype=torch.long)
    labels = torch.tensor(data['label'], dtype=torch.long)

    # Move data to CUDA if available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    text_tensors = text_tensors.to(device)
    labels = labels.to(device)

    dataset = TensorDataset(text_tensors, labels)
    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

    batch_size = 64
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    num_classes = len(label_encoder.classes_)

    # Create model and move to CUDA
    model = BertForSequenceClassification.from_pretrained("bert-base-multilingual-cased", num_labels=num_classes)
    model.to(device)

    # Data Parallelism (if multiple GPUs available)
    if torch.cuda.device_count() > 1:
        model = torch.nn.DataParallel(model)

    optimizer = AdamW(model.parameters(), lr=1e-5, weight_decay=1e-4)  # Add weight decay

    # Learning rate scheduling
    num_epochs = 100
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=len(train_dataloader) * num_epochs)

    # Mixed Precision Training
    scaler = GradScaler()

    # Early Stopping
    best_accuracy = 0.0
    patience = 8  # Number of epochs with no improvement to wait before stopping
    no_improvement_count = 0

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        for batch in train_dataloader:
            input_ids, labels = batch
            input_ids = input_ids.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            # Automatic mixed precision
            with autocast():
                outputs = model(input_ids, labels=labels)
                loss = outputs.loss

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            total_loss += loss.item()

        # Learning rate scheduling step
        scheduler.step()

        average_loss = total_loss / len(train_dataloader)
        print(f"Epoch {epoch + 1}/{num_epochs}, Average Loss: {average_loss:.4f}")

        # Evaluation on test data
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for batch in test_dataloader:
                input_ids, labels = batch
                input_ids = input_ids.to(device)
                labels = labels.to(device)

                outputs = model(input_ids)
                _, predicted = torch.max(outputs.logits, 1)

                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        accuracy = correct / total
        print(f'Accuracy on test data: {accuracy:.4f}')

        # Check for early stopping
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            no_improvement_count = 0
        else:
            no_improvement_count += 1

        if no_improvement_count >= patience:
            print(f'Early stopping at epoch {epoch + 1} as there has been no improvement for {patience} consecutive epochs.')
            break

    print(f'Best Accuracy on test data: {best_accuracy:.4f}')

    # Save the trained model to a file
    model.save_pretrained("bert_topic_classifier")

    # Save the label encoder to a file
    joblib.dump(label_encoder, "label_encoder.pkl")
