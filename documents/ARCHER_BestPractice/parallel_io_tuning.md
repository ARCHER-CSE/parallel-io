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
this is usually the critical factor for performance in parallel modelling or
simulation applications.

__Note:__ We have not yet included the NetCDF or HDF5 data below
but will add this shortly.

Lustre parallel file system parameters
--------------------------------------

The ARCHER `/owrk` file systems use the Lustre parallel file system
technology. On Lustre, users have control of a number of settings
on a per-file basis including the _striping settings_. Although these
parameters can be set on a per-file basis they are usually set on 
directory where your output files will be written so that all output
files inherit the settings.

Stripe settings for a directory (or file) can be set using the
`lfs setstripe` command.

You can query the stripe settings for a directory (or file) using the
`lfs getstripe` command.

Setting the striping parameters correcty is a key part of getting the
best write performance for your application on Lustre.
There are two parameters that you need to be concerned with: _stripe 
count_ and _stripe size_.  Generally, the stripe count has a larger
impact on performance than the stripe size.


### Stripe Count
The stripe count sets the number of OSTs (Object Storage T...) that
Lustre stripes the file across. In theory, the larger the number
of stripes, the more parallel write performance is available. However,
large stripe counts for small files can be detrimental to performance.

Stripe count is set using the `-c` option to `lfs setstripe`. For example,
to set a stripe count of 1 for directory `res_dir` you would use:

```bash
auser@eslogin006:~> lfs setstripe -c 1 res_dir/
```

The special value '-1' to the stripe count tells Lustre to use maximum 
striping.

### Stripe Size
The size of each stripe generally has less of an impact on performance
than the stripe count but becomes increasingly important as the size
of the file being written increases.

Stripe size is set using the  `-s` option to `lfs setstripe`. For example,
to set a stripe size of 4 MiB for directory `res_dir` along with 
maximum striping you would use:

```bash
auser@eslogin006:~> lfs setstripe -s 4m -c -1 res_dir/
```
Note that the `-s` option understands the following suffixes: 'k': KiB,
'm': MiB, 'g': GiB.

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

We provide detailed performance numbers for the different schemes with 
different striping settings below and provide a high-level summary here.

The basic advice is summarised in this table:

| Number of Writing Processes | Scheme | Stripe Count |    Stripe Size (MiB) |
| --------------------------: | :----: | -----------: | -------------------: |
|                     N <= 50 |   FPP  |            1 |                    1 |
|             50 < N <= 10000 |   FPP  |           -1 |                    1 |
|                  10000 >= N |   SSF  |           -1 | Depends on data size |

This leads to the following advice:

* For most cases we would recommend that users use a FPP scheme. 
* Beyond 10,000 writing processes we have found that the FPP scheme can lead to
  a high failure rate (due to node crashes) so recommend using a SSF scheme.
* The stripe size for SSF depends on the amount of data being written. The 
  larger the data being written, the larger the stripe size should be used.
  Please see the more detailed information provided below.

Put in plot of data: FPP vs SSF
  
File Per Process (FPP)
----------------------

The table below shows the maximum measured write bandwidths (in MiB/s) for the FPP
scheme using unformatted Fortran writes with different numbers of parallel processes.
These writes corresponded to:

* 1024 MiB written per process
* Fully-populated ARCHER nodes (24 processes per node)

A large amount of data needs to be written by each process to make sure that the
aggressive caching and buffering of I/O by the Fortran I/O library is avoided.

In summary:

* Using FPP we can quickly get high levels of performance for
the ARCHER Lustre file systems (just 4 nodes, 96 processes, can give a write performance in excess
of 15 GiB/s)
* At the lowest process counts (< 50 processes) single striping (`-c 1`) produces the 
best performance
* At more than 50 processes maximal striping (`-c -1`) should be used to get 
best performance

Put in plot of data: FFP

| Number of Processes | Stripe Count | Stripe Size (MiB) | Max. Write Bandwidth (MiB) |
| ------------------: | -----------: | ----------------: | -------------------------: |
|                  24 |            1 |                 1 |                      5929  |
|                  48 |            1 |                 1 |                     12261  |
|                  96 |            1 |                 1 |                     13262  |
|                 192 |            1 |                 1 |                     12532  |
|                 384 |            1 |                 1 |                     12048  |
|                 768 |            1 |                 1 |                     12741  |
|                1536 |            1 |                 1 |                     11930  |

| Number of Processes | Stripe Count | Stripe Size (MiB) | Max. Write Bandwidth (MiB) |
| ------------------: | -----------: | ----------------: | -------------------------: |
|                  24 |            4 |                 1 |                      6334  |
|                  48 |            4 |                 1 |                     11365  |
|                  96 |            4 |                 1 |                     11069  |
|                 192 |            4 |                 1 |                     12527  |
|                 384 |            4 |                 1 |                     12466  |
|                 768 |            4 |                 1 |                     13108  |
|                1536 |            4 |                 1 |                     12705  |

| Number of Processes | Stripe Count | Stripe Size (MiB) | Max. Write Bandwidth (MiB) |
| ------------------: | -----------: | ----------------: | -------------------------: |
|                  24 |           -1 |                 1 |                      4655  |
|                  48 |           -1 |                 1 |                      9169  |
|                  96 |           -1 |                 1 |                     15171  |
|                 192 |           -1 |                 1 |                     17149  |
|                 384 |           -1 |                 1 |                     17433  |
|                 768 |           -1 |                 1 |                     15189  |
|                1536 |           -1 |                 1 |                     15092  |

Single Shared File (SSF)
------------------------

### MPI-IO

The table below shows the maximum measured write bandwidths (in MiB/s) for the SSF
scheme using MPI-IO collective writes with different numbers of parallel processes.
These writes corresponded to:

* 16 MiB written per process
* Fully-populated ARCHER nodes (24 processes per node)

Les data is required per process in the SSF scheme compared to the FPP scheme as 
MPI-IO does not employ the agressive buffering and caching seen in the Fortran
I/O library.

In summary:

* Below 96 processes the defaut stripe count of 4 gives the best performance
* Above 96 processes maximal striping (`-c -1`) should be used to get best performance
* Single striping (`-c 1`) was not explored in detail as the performance was so low
  that it made running large tests problematic.

Plot of results: SSF performance comparison

| Number of Processes | Stripe Count | Stripe Size (MiB) | Max. Write Bandwidth (MiB) |
| ------------------: | -----------: | ----------------: | -------------------------: |
|                  24 |           -1 |                 1 |                       616  |
|                  48 |           -1 |                 1 |                      1356  |
|                  96 |           -1 |                 1 |                      2559  |
|                 192 |           -1 |                 1 |                      4944  |
|                 384 |           -1 |                 1 |                      6971  |
|                 768 |           -1 |                 1 |                     13223  |
|                1536 |           -1 |                 1 |                     11262  |
|                3072 |           -1 |                 1 |                     15897  |
|                6144 |           -1 |                 1 |                     14323  |


| Number of Processes | Stripe Count | Stripe Size (MiB) | Max. Write Bandwidth (MiB) |
| ------------------: | -----------: | ----------------: | -------------------------: |
|                  24 |            4 |                 1 |                       896  |
|                  48 |            4 |                 1 |                      1485  |
|                  96 |            4 |                 1 |                      2567  |
|                 192 |            4 |                 1 |                      1983  |
|                 384 |            4 |                 1 |                      1882  |
|                 768 |            4 |                 1 |                      1664  |
|                1536 |            4 |                 1 |                      1620  |
|                3072 |            4 |                 1 |                      1787  |
|                6144 |            4 |                 1 |                      1764  |

