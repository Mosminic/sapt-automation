#!/bin/bash

# V.Gazula 8/14/2021

#SBATCH -t 14-00:00:00                             #Time for the job to run
#SBATCH --job-name=sapt_automation                     #Name of the job

#SBATCH -N 1					#Nodes
#SBATCH -n 48                                   	#Number of cores needed for the job max is 128
#SBATCH --mem=180GB
#SBATCH --partition=normal

#SBATCH --mail-type ALL                         #Send email on start/end
#SBATCH --mail-user vka247@uky.edu              #Where to send email

#SBATCH --account=coa_cmri235_uksr                #Name of account to run under

#SBATCH --error=SLURM_JOB_%j.err                #Name of error file
#SBATCH --output=SLURM_JOB_%j.out               #Name of output file

#Module needed for this job
source ~/.bashrc

# activate teh env you need
conda activate p4env 


#Gaussian Program execution command
echo "Job $SLURM_JOB_ID running on SLURM NODELIST: $SLURM_NODELIST "
#export PGI_FASTMATH_CPU=haswell
#g16 H8octahedral.com > H8octahedral.log

export PYTHONPATH=$PWD
python workflow/run_wflow.py
rlaunch rapidfire
