import os
import librosa
import noisereduce as nr
import soundfile as sf
import numpy as np
from scipy.signal import butter, lfilter
import librosa.display
import matplotlib.pyplot as plt

# High-pass filter function
def highpass_filter(y, sr, cutoff=1000, order=5):
    nyquist = 0.5 * sr
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y_filtered = lfilter(b, a, y)
    return y_filtered

# Function to save side-by-side spectrograms
def save_side_by_side_spectrograms(y_original, y_processed, sr, file_path, title="Spectrogram Comparison"):
    # Compute spectrograms
    D_before = librosa.amplitude_to_db(np.abs(librosa.stft(y_original)), ref=np.max)
    D_after = librosa.amplitude_to_db(np.abs(librosa.stft(y_processed)), ref=np.max)

    # Plot the spectrograms side by side
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Plot the original (before noise reduction) spectrogram
    librosa.display.specshow(D_before, x_axis='time', y_axis='log', sr=sr, ax=axes[0])
    axes[0].set_title('Spectrogram Before Noise Reduction')
    axes[0].set_xlabel('Time (s)')
    axes[0].set_ylabel('Frequency (Hz)')

    # Plot the processed (after noise reduction) spectrogram
    librosa.display.specshow(D_after, x_axis='time', y_axis='log', sr=sr, ax=axes[1])
    axes[1].set_title('Spectrogram After Noise Reduction')
    axes[1].set_xlabel('Time (s)')
    axes[1].set_ylabel('Frequency (Hz)')

    # Add color bars
    plt.colorbar(librosa.display.specshow(D_before, x_axis='time', y_axis='log', sr=sr, ax=axes[0]), ax=axes[0], format="%+2.0f dB")
    plt.colorbar(librosa.display.specshow(D_after, x_axis='time', y_axis='log', sr=sr, ax=axes[1]), ax=axes[1], format="%+2.0f dB")

    # Save the side-by-side spectrograms as an image
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()

# Function to process each audio file and save spectrograms
def process_audio_file(input_path, output_path, spectrogram_folder, cutoff=1000):
    # Load the audio file
    y, sr = librosa.load(input_path, sr=None)

    # Apply the high-pass filter to remove low-frequency noise
    #y_filtered = highpass_filter(y, sr, cutoff=cutoff)

    # Perform noise reduction using spectral gating
    reduced_noise = nr.reduce_noise(y=y, sr=sr, prop_decrease=1.0)

    # Save the denoised audio to the output folder
    sf.write(output_path, reduced_noise, sr)

    # Save the side-by-side spectrograms before and after noise reduction
    save_side_by_side_spectrograms(y, reduced_noise, sr, os.path.join(spectrogram_folder, f"{os.path.basename(input_path)}_spectrogram_comparison.png"))

    print(f"Processed and saved: {input_path} -> {output_path}")

# Function to process all files in a folder
def process_folder(input_folder, output_folder, spectrogram_folder, cutoff=1000):
    # Create the output folder and spectrogram folder if they don't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(spectrogram_folder):
        os.makedirs(spectrogram_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        # Process only .wav files
        if filename.endswith(".wav"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            # Process and save the denoised file and side-by-side spectrograms
            process_audio_file(input_path, output_path, spectrogram_folder, cutoff)

# Set your input and output folders
input_folder = r'/Users/tom/Downloads/OneDrive_4_5-30-2025/psl9_warbler_snippets/'
output_folder = r'/Users/tom/Downloads/OneDrive_4_5-30-2025/psl9_warbler_snippets/processed_audio/'
spectrogram_folder = r'/Users/tom/Downloads/OneDrive_4_5-30-2025/psl9_warbler_snippets/processed_spectrograms/' # Replace with the path to save spectrogram images

# Process all files in the input folder
process_folder(input_folder, output_folder, spectrogram_folder, cutoff=1000)  # Adjust cutoff as needed
