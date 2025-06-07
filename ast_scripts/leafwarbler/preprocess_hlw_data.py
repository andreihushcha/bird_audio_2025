import librosa
import os
import json
import soundfile as sf  # Import soundfile to save audio
import numpy as np

def resample_audio(audio_file, target_sr=16000):
    """
    Resample audio to a target sample rate (16 kHz).
    """
    y, sr = librosa.load(audio_file, sr=None)  # Load without resampling to get the original sr
    y_resampled = librosa.resample(y, orig_sr=sr, target_sr=target_sr)  # Corrected resample usage
    return y_resampled, target_sr

def compute_mean_std(data_folder):
    """
    Compute the mean and standard deviation of the audio data in the given folder.
    """
    means = []
    stds = []

    # Loop over all files in the folder to calculate mean and std
    for file_name in os.listdir(data_folder):
        if file_name.endswith('.wav'):
            file_path = os.path.join(data_folder, file_name)
            y_resampled, _ = resample_audio(file_path)

            # Compute the mean and std of the audio file
            means.append(np.mean(y_resampled))
            stds.append(np.std(y_resampled))

    # Calculate overall mean and std for the dataset
    dataset_mean = np.mean(means)
    dataset_std = np.mean(stds)

    return dataset_mean, dataset_std

def create_json_data(input_folder, label, data_type, output_folder):
    """
    Create a JSON structure for the dataset with paths to resampled audio files.
    """
    data = []

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.wav'):
            file_path = os.path.join(input_folder, file_name)

            # Create the metadata entry for this sample
            entry = {
                "wav": os.path.abspath(file_path),  # Full path to the audio file
                "labels": label  # Use the provided label (HLW_Buzz or Non_HLW_Buzz)
            }

            data.append(entry)

            # Save the resampled audio to the corresponding output directory
            output_path = os.path.join(output_folder, file_name)
            y_resampled, sr = resample_audio(file_path)
            sf.write(output_path, y_resampled, sr)

    return data

def save_data_to_json():
    """
    Preprocess audio data and save it in the required JSON format.
    """
    # Define directories for training, validation, and testing
    train_positive_folder = '/Users/tom/Documents/GA Tech/SU25_HLW_Research/ast/egs/leafwarbler/data/train/positive/'
    train_negative_folder = '/Users/tom/Documents/GA Tech/SU25_HLW_Research/ast/egs/leafwarbler/data/train/negative/'

    validation_positive_folder = '/Users/tom/Documents/GA Tech/SU25_HLW_Research/ast/egs/leafwarbler/data/validation/positive/'
    validation_negative_folder = '/Users/tom/Documents/GA Tech/SU25_HLW_Research/ast/egs/leafwarbler/data/validation/negative/'

    test_positive_folder = '/Users/tom/Documents/GA Tech/SU25_HLW_Research/ast/egs/leafwarbler/data/test/positive/'
    test_negative_folder = '/Users/tom/Documents/GA Tech/SU25_HLW_Research/ast/egs/leafwarbler/data/test/negative/'

    # Define output directories for resampled audio files
    output_train_folder = 'processed_data/train/'
    output_val_folder = 'processed_data/validation/'
    output_test_folder = 'processed_data/test/'

    # Create necessary output directories
    os.makedirs(output_train_folder, exist_ok=True)
    os.makedirs(output_val_folder, exist_ok=True)
    os.makedirs(output_test_folder, exist_ok=True)

    # Compute mean and std for the entire dataset (positive and negative samples combined)
    all_data_folders = [train_positive_folder, train_negative_folder, validation_positive_folder, 
                        validation_negative_folder, test_positive_folder, test_negative_folder]

    all_mean_values = []
    all_std_values = []
    for folder in all_data_folders:
        dataset_mean, dataset_std = compute_mean_std(folder)
        all_mean_values.append(dataset_mean)
        all_std_values.append(dataset_std)

    # Calculate the overall mean and standard deviation
    overall_mean = np.mean(all_mean_values)
    overall_std = np.mean(all_std_values)

    print(f"Overall Dataset Mean: {overall_mean}, Overall Dataset Std Dev: {overall_std}")

    # Save the overall mean and std to a config file
    config = {
        "dataset_mean": float(overall_mean),  # Convert to native float
        "dataset_std_dev": float(overall_std)  # Convert to native float
    }

    with open("dataset_config.json", 'w') as config_file:
        json.dump(config, config_file, indent=4)

    # Process and create the JSON structure for each dataset
    train_data = create_json_data(train_positive_folder, "/m/05f6b", "train", output_train_folder) + \
                 create_json_data(train_negative_folder, "/m/0bt9lr", "train", output_train_folder)
    
    valid_data = create_json_data(validation_positive_folder, "/m/05f6b", "validation", output_val_folder) + \
                  create_json_data(validation_negative_folder, "/m/0bt9lr", "validation", output_val_folder)
    
    test_data = create_json_data(test_positive_folder, "/m/05f6b", "test", output_test_folder) + \
                create_json_data(test_negative_folder, "/m/0bt9lr", "test", output_test_folder)

    # Save the data as JSON files
    with open('train_data.json', 'w') as f:
        json.dump({"data": train_data}, f, indent=4)
    with open('valid_data.json', 'w') as f:
        json.dump({"data": valid_data}, f, indent=4)
    with open('test_data.json', 'w') as f:
        json.dump({"data": test_data}, f, indent=4)

    print(f"Data saved in train_data.json, valid_data.json, and test_data.json")

# Run the data saving function and class label creation
save_data_to_json()
