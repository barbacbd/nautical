# Github Actions

The following information is provided for future reference.

# Systems

- Linux -> Ubuntu -> Latest
- Windows -> Latest
- MacOS -> Latest

# Python Versions

- 3.6
- 3.7
- 3.8
- 3.9

# Python Test Execution Details

The tests are established using a matrix configuration that will pair all
operating systems and python versions from the matrix. The system **should NOT**
execute each step in parallel, or there errors will arise due to the limit on
NCEI lookups.

It is possible to execute the steps in parallel if (these are separate options and not required dependents):

1. Sleep is added to the execution steps

2. Separate the matrices and add a "needs" requirement

3. Big Separation:
- For each system create an email
- register the email as detailed in the token.yaml file in te project
- Create the `secret` token that was provided to the email
- Export the token as an env variable
- Add the ability for the tests to pick up the token in the env variable