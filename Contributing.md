# How to Contribute

This document outlines some of the conventions on development workflow and other
resources to make it easier to get your contribution accepted.

## Getting Started

- Fork the repository on GitHub
- Read the [README](README.md) for test instructions.
- Create a virtual environment [Optional].
- Install the build dependencies, see [building and testing](./README.md).
- Play with the project, submit bugs, submit patches!

## Contribution Flow

Anyone may submit [issues](https://github.com/barbacbd/nautical/issues)..
For contributors who want to work up pull requests, the workflow is roughly:

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