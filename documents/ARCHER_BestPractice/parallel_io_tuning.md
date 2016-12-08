Tuning Parallel I/O on ARCHER
=============================

This section provides information on getting the best performance
out of the parallel `/work` file systems on ARCHER when writing
data.

Types of parallel I/O
---------------------

There are a number of different types of I/O that could be considered
but we have limited ourselves to providing information for _write_
performance in the following cases:

_File Per Process (FPP)_
: One binary file written per parallel process. In this scenario we
  have investigated performance for standard unformatted Fortran
  writes.

_Single Shared File (SSF)_
: One binary file written to collectively by all parallel processes.
  In this scenario we have investigated performance using MPI-IO,
  parallel NetCDF, and parallel HDF5.

We have only considered write performance in the first instance as
this is usually the critical factor for parallel modelling or
simulation applications.

Lustre parallel file system parameters
--------------------------------------

The ARCHER `/owrk` file systems use the Lustre parallel file system
technology. On Lustre, users have control of a number of settings
on a per-file basis including the _striping settings_. Although these
parameters can be set on a per-file basis they are usually set on 
directory where your output files will be written so that all output
files inherit the settings.

Setting the striping parameters correcty is a key part of getting the
best write performance for your application on Lustre. There are 
two parameters that you need to be concerned with:

_Stripe Count_
: The stripe count sets the number of OSTs (Object Storage T...) that
  Lustre stripes the file across. In theory, the larger the number
  of stripes, the more parallel write performance is available. However,
  large stripe counts for small files can be detrimental to performance.

_Stripe Size_
: The size of each stripe generally has less of an impact on performance
  than the stripe count but becomes increasingly important as the size
  of the file being written increases.

ARCHER /work default stripe settings and OST counts
---------------------------------------------------

Each of the three Lustre `/work` file systems on ARCHER has the same
default stripe settings:

* A default stripe count of __4__
* A default stripe size of __1 MiB__

These settings have been chosen to provide a good compromise for the
wide variety of I/O patterns that are seen on the system but are 
unlikely to be optimal for any one particular scenario.

The total available number of OSTs available on each file system
are as follows:

* fs2: 48
* fs3: 48
* fs4: 56

### How can I find out which file system I am on?

All projects have their `/work` directory on one of the three Lustre
file systems. You can find out which one your project uses on ARCHER
by moving the your `/work` directory and using the `readlink` command:

```bash
auser@eslogin006:~> cd /work/t01/t01/auser
auser@eslogin006:/work/t01/t01/auser> readlink -f .
/fs3/t01/t01/auser
```

Summary of performance advice
-----------------------------

Our tests show that the maximum bandwidth you can expect to obtain from
the ARCHER Lustre `/work` file systems in practice is __15-17 GiB/s__,
irrespective of whether you use a FPP or SSF approach.

The basic advice is summarised in this table:

| Number of Processes | Scheme | Stripe Count | Stripe Size |
| ------------------: | :----: | -----------: | ----------: |
|            N <= 100 |   FPP  |            1 |       1 MiB |
|     100 < N <= 1000 |   FPP  |           -1 |       1 MiB |

File Per Process (FPP)
----------------------

Single Shared File (SSF)
------------------------



