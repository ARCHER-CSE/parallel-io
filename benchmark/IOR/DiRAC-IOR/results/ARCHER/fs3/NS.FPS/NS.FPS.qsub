#!/bin/bash
# ior.pbs
#   Invoke ior with typical arguments and default environment
# vlaues



#PBS -l select=16
#PBS -l walltime=05:30:00
#PBS -A d63
#PBS -N NS_FPS
#PBS -m bea
#PBS -M sid.kashyap@ed.ac.uk
 
  


module swap PrgEnv-cray PrgEnv-intel
module swap intel intel/15.0.2.164

TARGET="/work/d63/d63/shared/IOR_DiRAC_MPIIO/NS.FPS"
IOR="/work/d63/d63/skashyap/sid/ior_install/ior_intel_dyn/ior/ior_build/bin/ior"
IOR_SCRIPT="/work/d63/d63/shared/IOR_DiRAC_MPIIO/NS.FPS/con.ior"

date '+%Y%m%d%H%M%S'

pushd $TARGET

numNodes=(  16 8 4  2 1 )
blockSize=( 16 32 64 128 256 )

for test in `seq 5`
do  
    test=$(( $test - 1 ))
    cmd="$IOR -vvv  -b ${blockSize[$test]}g -f $IOR_SCRIPT"
    aprun -n ${numNodes[$test]} -N 1 $IOR -vvv  -b ${blockSize[$test]}g -f $IOR_SCRIPT
done
popd
