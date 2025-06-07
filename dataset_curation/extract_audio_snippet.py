import librosa
import soundfile as sf
import csv
import os

# Function to extract and save a snippet of audio based on sample indices
def extract_and_save_snippet(audio_file, start_sample, end_sample, output_file):
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)  # sr=None keeps the original sample rate
    
    # Extract the audio snippet (from start_sample to end_sample)
    snippet = y[start_sample:end_sample]
    
    # Save the snippet to a new file
    sf.write(output_file, snippet, sr)
    print(f"Snippet saved to: {output_file}")

# Function to process the CSV file containing timestamps and audio file names
def process_timestamps(audio_dir, csv_file, output_dir):
    # Read the CSV file containing timestamps and other information
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if there's one
        
        for row in reader:
            start_time = float(row[0])  # Start time in seconds (sample indices)
            end_time = float(row[1])    # End time in seconds (sample indices)
            output_filename = f"{row[2].replace('.png', '')}_snippet.wav"  # Output filename based on the third column (image name)
            audio_filename = row[3]  # Audio file name from the last column
            audio_filename = audio_filename.replace('PSL9_', '')
            audio_filename += '.wav'
            
            # Construct the full path to the audio file
            audio_file = os.path.join(audio_dir, audio_filename)
            
            # Check if the audio file exists
            if not os.path.isfile(audio_file):
                print(f"Audio file not found: {audio_file}")
                continue

            # Convert start and end times to sample indices
            y, sr = librosa.load(audio_file, sr=None)
            start_sample = librosa.time_to_samples(start_time, sr=sr)
            end_sample = librosa.time_to_samples(end_time, sr=sr)

            # Create the output file path
            output_file = os.path.join(output_dir, output_filename)

            # Extract and save the snippet
            extract_and_save_snippet(audio_file, start_sample, end_sample, output_file)

# Example usage:
audio_dir = '/Users/tom/Downloads/OneDrive_4_5-30-2025/'  # Replace with the path to the folder containing your audio files
csv_file = '/Users/tom/Downloads/od_model_v1_PSL9_rev.csv'  # Replace with the path to your CSV file containing timestamps
output_dir = '/Users/tom/Downloads/OneDrive_4_5-30-2025/psl9_warbler_snippets/'  # Replace with the desired output directory

# Process the CSV file and extract snippets
process_timestamps(audio_dir, csv_file, output_dir)
