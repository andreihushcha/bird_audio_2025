import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

df = pd.read_csv("data/data_20250330.csv")

# - SPECIES DISTRIBUTION ANALYSIS - #

species_counts1 = df["Common name"].value_counts().head(30)

# Create plot for 0.5 Confidence Level
plt.figure(figsize=(12, 6))
species_counts1.plot(kind="bar", color="royalblue", edgecolor="black")
plt.xlabel("Species")
plt.ylabel("Number of Unique Detections")
plt.title("Top 30 Bird Species Distribution in 0.5 Confidence Dataset")
plt.xticks(rotation=45, ha="right")
plt.subplots_adjust(bottom=0.45)
plt.savefig("vanessa_plots/0.5_species_distribution.png", bbox_inches="tight", dpi=300)
plt.show()


# - HUME'S LEAF WARBLER ACTIVITY OVER TIME - #

# Filter only Hume's Leaf Warbler
df_hume = df[df["Common name"] == "hume's warbler"]

# Count occurrences of detections per hour and sort
time_counts = df_hume["Time"].value_counts().sort_index()

# Create the plot for 0.5 Confidence Level
plt.figure(figsize=(10, 5))
plt.plot(time_counts.index, time_counts.values, marker="o", linestyle="-", color="royalblue")
plt.xlabel("Time of Day (Hour)")
plt.ylabel("Number of Unique Hume's Leaf Warbler Detections")
plt.title("Hume's Leaf Warbler Activity Over Time - 0.5 Confidence")
plt.grid()
plt.savefig("vanessa_plots/0.5_humes_warbler_activity_over_time.png", bbox_inches="tight", dpi=300)
plt.show()


# - ELEVATION VS SPECIES - #

# Get the top 30 most frequent species
df_filtered = df[df["Common name"].isin(species_counts1.index)]

# Create plot for 0.5 Confidence Level
plt.figure(figsize=(12, 6))
sns.scatterplot(x="Common name", y="Elevation", hue="Common name", data=df_filtered, alpha=0.7, palette="tab20", legend=False)
plt.xticks(rotation=90)
plt.xlabel("Species")
plt.ylabel("Elevation (m)")
plt.title("Elevation Distribution of the 30 Most Frequent Bird Species - 0.5 Confidence")
plt.subplots_adjust(bottom=0.47)
plt.savefig("vanessa_plots/0.5_top_species_elevation_scatter.png", bbox_inches="tight", dpi=300)
plt.show()


# - LOCAL VS UNEXPECTANT SPECIES - #

# Count occurrences of local vs. unexpected species
habitant_counts = df["Habitant"].value_counts()

# Create plot for 0.5 Confidence Level
labels1 = ["Local Species" if i == 1 else "Unexpected Species" for i in habitant_counts.index]
plt.figure(figsize=(6, 6))
plt.pie(habitant_counts, labels=labels1, autopct="%1.1f%%", colors=["green", "red"], startangle=140)
plt.title("Proportion of Local vs. Unexpected Species - 0.5 Confidence")
plt.savefig("vanessa_plots/0.5_local_vs_unexpected_species.png", bbox_inches="tight", dpi=300)
plt.show()


# - AVERAGE SONG LENGTH FOR TOP 30 SPECIES - #

# Get the top 30 most detected species
top_species = df["Common name"].value_counts().head(30).index

# Filter dataset for only these species
df_filtered = df[df["Common name"].isin(top_species)]

song_lengths = []
current_song_length = 0

# Track previous row values
prev_id = None
prev_common_name = None
prev_end_time = None

for _, row in df_filtered.iterrows():
    if (row["ID"] == prev_id and row["Common name"] == prev_common_name and row["Start (s)"] == prev_end_time):
        # If same bird, same ID, and start time matches previous end time, extend the song
        current_song_length += (row["End (s)"] - row["Start (s)"])
    else:
        # If a new song starts, store the previous song length
        if current_song_length > 0:
            song_lengths.append({"Common name": prev_common_name, "Song Length": current_song_length})
        # Reset for new song
        current_song_length = row["End (s)"] - row["Start (s)"]

    # Update previous values
    prev_id = row["ID"]
    prev_common_name = row["Common name"]
    prev_end_time = row["End (s)"]

# Store the last song length
if current_song_length > 0:
    song_lengths.append({"Common name": prev_common_name, "Song Length": current_song_length})

# Convert to DataFrame
song_lengths_df = pd.DataFrame(song_lengths)

# Calculate average song length per species
avg_song_lengths = song_lengths_df.groupby("Common name")["Song Length"].mean().reset_index()

# Sort by longest average song length
avg_song_lengths = avg_song_lengths.sort_values(by="Song Length", ascending=False)

# Set plot style
sns.set(style="whitegrid")

# Plot: Average Song Length for Top 30 Species
plt.figure(figsize=(12, 8))
sns.barplot(data=avg_song_lengths, x="Song Length", y="Common name", hue="Common name", palette="viridis", dodge=False, legend=False)
plt.title("Average Song Length for Top 30 Bird Species")
plt.xlabel("Average Song Length (seconds)")
plt.ylabel("Bird Species")
plt.tight_layout()
plt.savefig("vanessa_plots/0.5_avg_song_length_top_30_species.png", bbox_inches="tight", dpi=300)
plt.show()

# - AVERAGE SONG LENGTH FOR HUME'S LEAF WARBLER - #

# Filter for Hume's Leaf Warbler
df_hume = df[df["Common name"] == "hume's warbler"]

# Initialize variables for song length calculation
song_lengths_hume = []
current_song_length_hume = 0

# Track previous row values
prev_id_hume = None
prev_end_time_hume = None

for _, row in df_hume.iterrows():
    if row["ID"] == prev_id_hume and row["Start (s)"] == prev_end_time_hume:
        # Continue the current song
        current_song_length_hume += (row["End (s)"] - row["Start (s)"])
    else:
        # If a new song starts, store the previous song length
        if current_song_length_hume > 0:
            song_lengths_hume.append(current_song_length_hume)
        # Reset for new song
        current_song_length_hume = row["End (s)"] - row["Start (s)"]

    # Update previous values
    prev_id_hume = row["ID"]
    prev_end_time_hume = row["End (s)"]

# Store the last song length
if current_song_length_hume > 0:
    song_lengths_hume.append(current_song_length_hume)

# Convert to DataFrame
song_lengths_hume_df = pd.DataFrame(song_lengths_hume, columns=["Song Length"])

# Plot: Song Length Distribution for Hume’s Leaf Warbler
plt.figure(figsize=(10, 6))
sns.histplot(song_lengths_hume_df["Song Length"], bins=20, kde=True, color="skyblue")
plt.title("Song Length Distribution for Hume’s Leaf Warbler")
plt.xlabel("Song Length (seconds)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("vanessa_plots/0.5_avg_song_length_humes_warbler.png", bbox_inches="tight", dpi=300)
plt.show()

# - THRESHOLD ANALYSIS - #

confidence_thresholds = np.arange(0.5, 1.05, 0.05)
results = []

for threshold in confidence_thresholds:
    retrieved = df[df["Confidence"] >= threshold]

    total_samples = len(retrieved)
    if total_samples == 0:
        continue

    expected_species_pct = (len(retrieved[retrieved["Habitant"] == 1]) / total_samples) * 100
    unexpected_species_pct = (len(retrieved[retrieved["Habitant"] == 0]) / total_samples) * 100
    hlw_pct = (len(retrieved[retrieved["Common name"] == "hume's warbler"]) / total_samples) * 100

    results.append({
        "Confidence Threshold": threshold,
        "Expected Species (%)": expected_species_pct,
        "Unexpected Species (%)": unexpected_species_pct,
        "Hume's Leaf Warbler (%)": hlw_pct
    })

# Create plot for 0.5 Confidence Level (includes data with 0.5 confidence and above)
results_df = pd.DataFrame(results)
plt.figure(figsize=(10, 6))

# Plot trends (percentages)
sns.lineplot(data=results_df, x="Confidence Threshold", y="Expected Species (%)", label="Expected Species (%)", marker="s", linestyle="-")
sns.lineplot(data=results_df, x="Confidence Threshold", y="Unexpected Species (%)", label="Unexpected Species (%)", marker="^", linestyle="-.")
sns.lineplot(data=results_df, x="Confidence Threshold", y="Hume's Leaf Warbler (%)", label="Hume's Leaf Warbler (%)", marker="d", linestyle=":")

plt.xlabel("Confidence Threshold")
plt.ylabel("Percentage (%)")
plt.title("BirdNet Confidence Threshold Analysis (0.5 Confidence Data) - Percentage")
plt.grid(True)
plt.legend()
plt.savefig("vanessa_plots/threshold_analysis.png", bbox_inches="tight", dpi=300)
plt.show()
