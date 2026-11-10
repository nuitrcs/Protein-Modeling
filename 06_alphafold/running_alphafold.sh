#!/bin/bash
#SBATCH --account=e32559
#SBATCH --partition=gengpu
#SBATCH --gres=gpu:a100:1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:10:30
#SBATCH --mem=8G
#SBATCH --job-name=af3_prediction
#SBATCH --output=logs/af3_%A_%a.log


module purge all
module load alphafold/3.0.0

# Ensure logs and output directories exist
mkdir -p output_pdbs

# Run AlphaFold3
af3_gpu \
    --model_dir=$(pwd)/model \
    --output_dir=$(pwd)/output_pdbs/ \
    --json_path=$(pwd)/msa_outputs/spycatcher_spytag/spycatcher_spytag_data.json
