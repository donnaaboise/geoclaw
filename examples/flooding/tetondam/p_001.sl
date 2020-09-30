#!/bin/bash

#SBATCH -J SPERO_xgeoclaw_001      # job name
#SBATCH -o xgeoclaw_001.o%j        # output and error file name (%j expands to jobID)
#SBATCH -n 8                       # total number of cpus requested. 28 per node.
#SBATCH -N 1                       # number of nodes requested
##SBATCH --exclusive               # request exclusive usage of your nodes. (for low cpu, high memory jobs)
#SBATCH -p defq                    # queue (partition) -- defq, ipowerq, eduq, gpuq.
#SBATCH -t 4:00:00                 # run time (hh:mm:ss) - 12.0 hours in this example.
#SBATCH --mail-user=hannahspero@boisestate.edu

# Generally needed modules:
module load slurm
module load intel/mkl 
module load intel/mpi
module load anaconda/anaconda3
module load gcc/6.4.0
export OMP_MAX_THREADS=4

# Execute the program:
make data
cd /home/hspero/clawpack5.6/clawpack/geoclaw/examples/flooding/tetondam/_output
cp ../*.data .
../xgeoclaw
