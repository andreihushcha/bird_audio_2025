#!/bin/bash
#SBATCH -
 sm
#SBATCH --gres=gpu:4
#SBATCH -c 4
#SBATCH -n 1
#SBATCH --mem=48000
#SBATCH --job-name="ast_leafwarbler"
#SBATCH --output=./log_%j.txt

set -x
source ../../venvast/bin/activate
export TORCH_HOME=../../pretrained_models

model=ast
dataset=leafwarbler  # Custom dataset name (your leaf warbler dataset)
imagenetpretrain=True
audioset_pretrain=True  # Use AudioSet pretrained model

# Set paths to your JSON data files (train, validation)
train_data_path="./train_data.json"
valid_data_path="./valid_data.json"

# Use your label csv created earlier
label_csv="./class_label_indices.csv"

# Hyperparameters and settings
lr=1e-5
epoch=10
batch_size=12
fstride=10
tstride=10
freqm=48
timem=192
mixup=0.5

dataset_mean=-0.000015029484529804904  # Mean for AudioSet, update if you want to use different stats
dataset_std=4.5689974  # Standard deviation for AudioSet, update if you want to use different stats
audio_length=1024
noise=False

metrics=mAP
loss=BCE
warmup=True
wa=True

num_workers=0

exp_dir=./exp/leafwarbler-f$fstride-t$tstride-p$imagenetpretrain-b$batch_size-lr${lr}-decoupe
if [ -d $exp_dir ]; then
  echo 'Experiment directory exists, exiting.'
  exit
fi
mkdir -p $exp_dir

CUDA_CACHE_DISABLE=1 python -W ignore ../../src/run.py --model ${model} --dataset ${dataset} \
--data-train ${train_data_path} --data-val ${valid_data_path} --exp-dir $exp_dir \
--label-csv ${label_csv} --n_class 2 \
--lr $lr --n-epochs ${epoch} --batch-size $batch_size --save_model True \
--freqm $freqm --timem $timem --mixup ${mixup} \
--tstride $tstride --fstride $fstride --imagenet_pretrain $imagenetpretrain --audioset_pretrain $audioset_pretrain \
--dataset_mean ${dataset_mean} --dataset_std ${dataset_std} --audio_length ${audio_length} --noise ${noise} \
--metrics ${metrics} --loss ${loss} --warmup ${warmup} \
--wa ${wa} --num-workers ${num_workers}
