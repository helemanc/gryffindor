#!/bin/bash
#SBATCH --job-name=data_wiki            
#SBATCH --mail-user=sefie08@zedat.fu-berlin.de  
#SBATCH --mail-type=end
#SBATCH --nodes=1
#SBATCH --ntasks=1                        
#SBATCH --mem-per-cpu=10240                  
#SBATCH --time=20:00:00                           
#SBATCH --qos=standard                         
#SBATCH --cpus-per-task=1


cd /home/${USER}/projects/

module add Python/3.9.5-GCCcore-10.3.0

source ~/path/to/new/virtual/environment/bin/activate

python wiki_query_service.py