#!/bin/bash

# Create set of Lustre directories for benchio tests
function create_dirs {

   basedir=$1
   stripesize=$2

   if [ ! -d "${basedir}" ];
   then
      mkdir -p ${basedir}
   fi

   dirpath=${basedir}/unstriped
   if [ ! -d "${dirpath}" ]
   then
      mkdir -p "${dirpath}"
   else
      rm -rf "${dirpath}"
      mkdir -p "${dirpath}"
   fi
   lfs setstripe -c 1 -S ${stripesize} ${dirpath}

   dirpath=${basedir}/striped
   if [ ! -d "${dirpath}" ]
   then
      mkdir -p "${dirpath}"
   else
      rm -rf "${dirpath}"
      mkdir -p "${dirpath}"
   fi
   lfs setstripe -c -1 -S ${stripesize} ${dirpath}

   dirpath=${basedir}/defstriped
   if [ ! -d "${dirpath}" ]
   then
      mkdir -p "${dirpath}"
   else
      rm -rf "${dirpath}"
      mkdir -p "${dirpath}"
   fi
   lfs setstripe -c 4 -S ${stripesize} ${dirpath}
}
