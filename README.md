<!--- (C) Copyright 2019 Hewlett Packard Enterprise Development LP -->

# WordStock

Utility to search and take stock of words in large file sets

## Prerequisites

1. Install and run Docker on a Linux workstation. For more information,
   see the [Docker Documentation](https://docs.docker.com/install/).
   Please make sure that docker can reach internet if your workstation
   is behind the proxy. The version of docker used for testing is
   17.05.0-ce

2. Test that your installation works by running the following hello-world Docker image,

   ```bash
   docker run hello-world
    ```

## Usage

### Running WordStock utility
To run the WordStock utility, run the following command

    ```bash
     docker run -it --rm --name <container_name> \
     -v <absolute_path_to_data_set>:/data \
     -v <absolute_path_to_patterns>:/pattern \
     -v <absolute_path_to_output>:/output nithyg/wordstock:v1 -f <csv|json>
     ```

###### Typical WordStock output

Here is an example of output from a typical run (12 test datafiles of
size 500KB approximately). You will also find output file created in the
output volume shared to the docker container

```bash
+------------------------------------------+---------+
|                                          |   words |
|------------------------------------------+---------|
| ('all_is_well_that_ends_well', 'the')    |   14619 |
| ('all_is_well_that_ends_well', 'and')    |   10818 |
| ('all_is_well_that_ends_well', 'to')     |    7935 |
| ('all_is_well_that_ends_well', 'a')      |    7043 |
| ('all_is_well_that_ends_well', 'of')     |    6905 |
| ('all_is_well_that_ends_well', 'is')     |    2861 |
| ('all_is_well_that_ends_well', 'at')     |    1557 |
| ('as_you_like_it', 'the')                |   13527 |
...
...
| ('war_and_peace', 'of')                  |   31167 |
| ('war_and_peace', 'a')                   |   24182 |
| ('war_and_peace', 'is')                  |    8790 |
| ('war_and_peace', 'at')                  |    7825 |
+------------------------------------------+---------+
Execution Time: 11.50390076637268

```
Please note that the warning messages may occur in the above output and is expected as
WordStock does not support Unicode decode error.

If the docker image pull fails please check the internet connectivity
from workstation.

### WordStock Testing

###### Python Linting
WordStock is *flake8* compliant and can be run on the WordStock code
in the container as follows

```bash
    docker run -it --rm --name <container_name> \
    -e http_proxy -e https_proxy -e no_proxy \
    -v <absolute_path_to_data_set>:/data \
    --entrypoint flake8 \
    nithyg/wordstock:v1 /wordstock
```

###### Unit tests
WordStock unittests are based on python unittest framework. It
uses the following
* *magicmock* Python unittest mocking functionality
* *pytest* Test run and coverage
* *ddt* a python package for data driven testing
* *testtools* a python package based on unittests providing additional
  test assert functions

```bash
    docker run -it --rm --name <container_name> \
    -e http_proxy -e https_proxy -e no_proxy \
    -v <absolute_path_to_data_set>:/data \
    --entrypoint pytest \
    nithyg/wordstock:v1 /wordstock/tests
```

###### Unit test coverage
To know the unit test coverage of the code shipped used pytest-cov package
Following is the Unit test coverage so far is
All these tests will be run as a part of the travis CI in the github
project as a next step,

```bash
----------- coverage: platform linux, python 3.7.4-final-0 -----------
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
/wordstock/__init__.py                   0      0   100%
/wordstock/setup.py                      7      7     0%
/wordstock/stock.py                     88     58    34%
/wordstock/tests/__init__.py             0      0   100%
/wordstock/tests/base.py                22      4    82%
/wordstock/tests/create_dataset.py      23     23     0%
/wordstock/tests/test_stock.py          47      1    98%
--------------------------------------------------------
TOTAL                                  187     93    50%

```

###### Functional tests
The functional tests for WordStock are automated using python-unittests
framework and available at tests/test_stock_functional.py


###### Performance tests
The performance of the WordStock utility was measured by varying the
number of input data files

| data files  |  Patterns | Execution time|
| ------------- |-------------|-------------|
| 5  (<2kb)      | Constant(15)   |5 seconds|
| 10  (300-500kb)|  Constant(15)  |11 seconds|
| 30 (300-500kb) | Constant(15)   |48 seconds|
| 40 (300-500kb) | Constant(15)   |120 seconds|
| 100 (300-500kb) | Constant(15)  |274 seconds|

Please note that as the number of words to search is increased the time
taken for the execution increases as well

## Additional information

### Design
WordStock uses Python pandas. pandas is an open source, BSD-licensed
library providing high-performance, easy-to-use data structures and data
analysis tool. It builds pandas dataframes for datasets and patterns and
uses it to group and selectively filter the word patterns from the
dataset frames. The utility is containerised including the test and the
data generations scripts. These can be changed by modifying the
entrypoint of the container.

### Assumptions/Current behavior

* WordStock takes stock of alphabetic words as of today and it does not
  count the occurrences of substrings
* It works only on data and patterns files with *.txt* extension
* The files both data and patterns are expected to be provided as input
  directories to WordStock
* It is tested using docker installed on Ubuntu 16.04.
* Performance of WordStock drops as the number of files to take stock of
  increases. The reason for this behavior need to be checked in the program
  and get tuned

### Building WordStock docker image
Build the wordstock docker image from the parent directory of the
source code, using the following command,

```bash
   docker build --build-arg http_proxy=$http_proxy --build-arg \
   https_proxy=$https_proxy -t wordstock .
```

### Test data generation
To generate test data run the following command, This will create
around 100 books as files in the test data directory. Please note
that depending on the connectivity to the internet the test data
generator may error out while downloading the URLs, but the script
would continue to completion.

    ```bash
     docker run -it --rm --name <container_name> \
     -v <absolute_path_to_data_set>:/data \
     --entrypoint /wordstock/generate_data.sh \
     nithyg/wordstock:v1
    ```
Note: Please add on the proxy variables if you are behind the proxy
as shown below

    ```bash
     docker run -it --rm --name <container_name> \
     -e http_proxy -e https_proxy -e no_proxy
     -v <absolute_path_to_data_set>:/data \
     --entrypoint /wordstock/generate_data.sh \
     nithyg/wordstock:v1
    ```

## Next Steps

* Increase test coverage
* Run the tests as part of CI (travis.ci as its free for github public
  repositories)
* Add the enhancements to provide search and file patterns from command
  line
* Categorize the tests for selective runs
