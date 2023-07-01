#!/bin/bash
#SBATCH --job-name=data_wiki            
#SBATCH --mail-user=sefie08@zedat.fu-berlin.de  
#SBATCH --mail-type=end
#SBATCH --nodes=1
#SBATCH --ntasks=1                        
#SBATCH --mem-per-cpu=5120                  
#SBATCH --time=6:00:00                           
#SBATCH --qos=standard                         
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --partition=gpu


cd /home/${USER}/projects/

module add Python/3.9.5-GCCcore-10.3.0

source ~/path/to/new/virtual/environment/bin/activate

python generator.py