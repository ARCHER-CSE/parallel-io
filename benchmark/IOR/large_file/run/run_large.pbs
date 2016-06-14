#!/bin/bash --login

#PBS -l select=64
#PBS -l walltime=3:0:0
#PBS -N ior_large_64
#PBS -A z01-cse

module swap PrgEnv-cray PrgEnv-intel
module swap intel intel/15.0.2.164

cd $PBS_O_WORKDIR

# System and file system identifier
system=ARCHER
fs=fs3

# Base directories
BASE_DIR=/work/z01/z01/aturner/CSE/parallel-io/benchmark/IOR/large_file
RESULT_DIR=${BASE_DIR}/results/${system}/${fs}
CONFIG_DIR=${BASE_DIR}/run
IOR=/work/z01/z01/aturner/CSE/parallel-io/benchmark/IOR/bin/ior

# Make sure the results direcotry exists
if [ ! -d "${RESULT_DIR}" ];
then
   mkdir ${RESULT_DIR}
fi

# Basic test parameters
striping=-1
clients=$(( 64 * 24 ))

# Array of tests and associated block sizes
# testsA=("large.SHF" "large.FPS")
# blockA=(          8           8)
testsA=("large.SHF")
blockA=(          8)

# Loop over all tests
for i in "${!testsA[@]}"
do
   # Set this test parameters
   iortest=${testsA[$i]}
   block=${blockA[$i]}
   timestamp=$(date '+%Y%m%d%H%M%S')
   TARGET="${RESULT_DIR}/${iortest}/data"
   IOR_SCRIPT="${CONFIG_DIR}/${iortest}.config"
   outfile=${RESULT_DIR}/${iortest}/ior_res_s${striping}_c${nodes}_b${block}_${timestamp}.dat

   if [ ! -d "${RESULT_DIR}/${iortest}" ]; then
      mkdir ${RESULT_DIR}/${iortest}
   fi
   cd ${RESULT_DIR}/${iortest}
   if [ ! -d "${TARGET}" ]; then
      mkdir ${TARGET}
   fi

   lfs setstripe -c ${striping} ${TARGET}
   echo "${timestamp} Running: Test=${iortest}, Stripe=${striping}, nodes=${nodes}, blocksize=${block}"
   echo "JobID = ${PBS_JOBID}" > ${outfile}
   echo "Striping = ${striping}" >> ${outfile}
   aprun -n ${clients} $IOR -vvv  -b ${block}g -f $IOR_SCRIPT >> ${outfile}
done

