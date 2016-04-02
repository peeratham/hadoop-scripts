#!/bin/bash

# Example qsub script for HokieSpeed

# NOTE: You will need to edit the Walltime, Node and Processor Per Node (ppn), Queue, and Module lines
# to suit the requirements of your job. You will also, of course have to replace the example job
# commands below with those that run your job.
 
# Set the walltime, which is the maximum time your job can run in HH:MM:SS
# Note that if your job exceeds the walltime estimated during submission, the scheduler
# will kill it. So it is important to be conservative (i.e., to err on the high side)
# with the walltime that you include in your submission script. 
#PBS -l walltime=120:00:00

# Set the number of nodes, and the number of processors per node (generally should be 12)
#PBS -I -l nodes=3:ppn=12

# Access group, queue, and accounting project
#PBS -W group_list=hokiespeed
# Queue name. Replace normal_q with long_q to submit a job to the long queue.
# See HokieSpeed documentation for details on queue parameters.
#PBS -q normal_q
#PBS -A hokiespeed

# Uncomment and add your email address to get an email when your job starts, completes, or aborts
#PBS -M tpeera4@vt.edu
#PBS -m bea

# Add any modules you might require. Use the module avail command to see a list of available modules.
# This example removes all modules, adds the GCC, OpenMPI, and CUDA modules, then loads the FFTW module.
module purge
module load jdk
## module add fftw

# Change to the directory from which the job was submitted
# cd $PBS_O_WORKDIR


#cd /home/zjing14/getnode
#cat $PBS_NODEFILE | tee hostfile
# Below here enter the commands to start your job. A few examples are provided below.

# Say "Hello world!"
# echo "Hello world!" 

# Run the program a.out
#./hold

# Run the MPI program mpiProg. The -np flag tells MPI how many processes to use. $PBS_NP
# is an environment variable that holds the number of processes you requested. So if you
# selected nodes=2:ppn=12 above, $PBS_NP will hold 24.
#mpirun -np $PBS_NP ./mpiProg

# Run the OpenMP program ompProg. The CPUSET and AFFINITY lines set thread affinity (tell the
# machine which CPUs to use for which processes); they may boost performance if set correctly
# but are not required. $PBS_NP is an environment variable that holds the number of processes
# you requested. So if you selected nodes=4:ppn=6 above, $PBS_NP will hold 24.
#CPUSET=`numactl --show | awk '/^physcpubind/ {for(i=2;i<=NF;++i){printf"%d ",$i}}' | sed 's/[ \t]*$//'`
# Use this line for OpenMP compiled with Intel cpubinding.
#export KMP_AFFINITY="proclist=[$CPUSET]"
# Use this line for OpenMP compiled with GCC cpubinding.
#export GOMP_CPU_AFFINITY="$CPUSET"
#export OMP_NUM_THREADS=$PBS_NP
#./ompProg

# An example command to launch mpiblast
# -np sets the number of processes (see above)
# -d nt, the database
# -i test.in, the query file
# -p blastn, the query/database type, blastn is nucleotide query against nucleotide database
# -o results.txt, the output file
#mpirun -np $PBS_NP mpiblast -d nt -i test.in -p blastn -o results.txt

#exit;
