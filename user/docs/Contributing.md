# Contributing Guidelines

Whether you are aiming to become the first mate, second mate ... Deck cadet, engineer, or just walk the plank you have found your
way to the contributions documentation. Please continue reading if you would like to contribute or just follow along with the
development progress of the package.

## Casting off

- Fork the repository on GitHub
- Read the [README](../../README.md) for test instructions.
- Create a virtual environment [Optional].
- Install the build dependencies, see [building and testing](../../README.md).
- Play with the project, submit bugs, submit patches!

## Contribution Flow

Anyone may submit [issues](https://github.com/barbacbd/nautical/issues). The issues will be reviewed by
the captain, and those that are deemed _valuable changes_ to the project will be accepted. Shipmates that
would like to work on pull requests, the workflow is roughly:

1. Create a topic branch from where you want to base your work (usually master).
2. Make commits of logical units.
3. Make commit messages that clearly document the changes.
4. Push your changes to a topic branch in your fork of the repository.
5. Make sure the tests pass, and add any new tests as appropriate.
6. Submit a pull request to the original repository.


## Commit Message Format

A rough convention for commit messages that is designed to answer two
questions: what changed and why. The subject line should feature the what and
the body of the commit should describe the why.

Example:

```

noaa: Added XXX functionality to XXXX

** Added the XXX function to XXX to satisfy the need/
requirement for XXX.

** Additional information followed in other bullet points.

```

_It is suggested (but not required to add the Issue number to the commit message._


## Further Information

Please run the tests [here](../../scripts/). If you cannot execute a shell script, run the equivalent on your system.

The following script executes all project tests. 

```bash
scripts/pytest.sh
```

**NOTE**: If you are adding tests, no tests should make any network API calls. Please refer to [mock](https://pypi.org/project/pytest-mock/)
for information on creating mock tests.


The following script executes the python linter.

```bash
scripts/pylint.sh
```

The linter is *not* executed during `push`, but it will be utilized during all reviews.
