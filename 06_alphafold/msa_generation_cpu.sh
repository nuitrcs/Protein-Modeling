#!/bin/bash
#SBATCH --account=e32559
#SBATCH --partition=normal
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=3:00:00
#SBATCH --mem=6G
#SBATCH --job-name=af3_cpu_array
#SBATCH --output=logs/af3_cpu_%A_%a.log

module purge
module load alphafold/3.0.0

mkdir -p logs

af3_cpu --model_dir=$(pwd)/model \
        --output_dir=$(pwd)/msa_outputs \
        --json_path=$(pwd)/spycatcher_spytag.json
