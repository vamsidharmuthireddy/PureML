# Contributing guide

## Where to start?

You can contribute to PureML in a number of ways, depending on your expertise, experience, and interest.

If you want to **dive into the code**, the next sections of this document describes the project structure, commit instructions, etc. We have compiled a list of ["Good first issues"](https://github.com/PureML-Inc/PureML/issues), which are small and well-defined tasks for getting started. We also have a ["Help wanted"](https://github.com/PureML-Inc/PureML/issues) tag that has more general issues.

When you pick up an issue, please post a comment on the Github issue so others know that it's being worked on.

If you have **thoughts about version control for ML**, we would really appreciate a review of [the roadmap](https://github.com/orgs/PureML-Inc/projects/5). You can use the thumbs up/down feature to let us know if you think a roadmap item is useful or not. It's also great if you comment on roadmap issues that you have specific thoughts about. If something is missing on the roadmap, please open a new issue and we'll discuss it there on Github.

The roadmap is a work in progress, not a waterfall-y specification, and we want it to evolve based on the input from the community!

We also host regular "community meetings" where we discuss specific roadmap items, and ML versioning and replicability in general. We send out invites to the meeting in advance, in the [`#community-meeting` Discord channel](https://discord.gg/DQ65HnKY). Anyone is welcome to join, and they tend to be interesting discussions with a mix of industry practitioners and academics.

But perhaps the most useful thing you can do is **use the tool**. Join the [Discord chat](https://discord.gg/DBvedzGu) and let us know if PureML is useful to you, and how it can be improved. Open issues on [Github](https://github.com/PureML-Inc/PureML) if you find bugs or have ideas for enhancements.

## Project structure

There are three main parts to the codebase:

- `pureml/`: This contains the `pureml` Python Library. 
- `tests/`: This are the tests for `pureml` Python library. 



## Making a contribution

### Signing your work

Each commit you contribute to PureML must be signed off. It certifies that you wrote the patch, or have the right to contribute it. It is called the [Developer Certificate of Origin](https://developercertificate.org/) and was originally developed for the Linux kernel.

If you can certify the following:

```
By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```

Then add this line to each of your Git commit messages, with your name and email:

```
Signed-off-by: Mike Adams <mike.adams@email.com>
```

You can sign your commit automatically by passing the `-s` option to Git commit: `git commit -s -m "Reticulate splines"`

## Development environment

PureML is build using poetry. You can install it following these [instructions](https://python-poetry.org/docs/#installation)

Run this to install the Python library and its dependencies locally for development:

    poetry install
    poetry build    


If you make changes to Go code, you will need to re-run the `poetry build` command to build the package.

## Test
PureML uses pytest to run the test suites

Run this to run the test suite:

    pytest

This will run the three test suites in the `test/` directories. 


## Build

This will build the Python package:

    poetry build

The built Python package in `pureml/`. This contains the Python library.



