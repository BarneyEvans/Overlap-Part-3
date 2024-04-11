#!/bin/sh

#SBATCH --nodes=1

#SBATCH --output=/mainfs/lyceum/be1g21/V6/Ouput
#SBATCH --error=/mainfs/lyceum/be1g21/V6/Output/errors.err
#SBATCH --partition=gpu
#SBATCH -p lyceum
#SBATCH gres=gpu
#SBATCH --time=12:00:00



python lyceum/be1g21/For_Idris/Yolo_Training.py