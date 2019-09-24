---
title: TESTING-DOCUMENT
tags: [Notebooks/Daily Log]
created: '2019-07-25T21:22:58.145Z'
modified: '2019-08-07T05:00:17.220Z'
---

# pyEnv-Comcast

## Description
Python has it's own way of downloading, storing and resolving package definitions (or modules). The location where these packages are downloaded can be found in your sys.prefix and sys.getsitepackages(). 

So any third party package will be placed in these directories *BUT* if your program has a dependency on packageC, ver1.0 and another one of your programs requires the same package but for version 2.0, you will have a problem with the conflicts. To solve this we create virtual environments that will contain the proper version of packageC in each virtual environment.

At its core, the main purpose of Python virtual environments is to create an isolated environment for Python projects. This means that each project can have its own dependencies, regardless of what dependencies every other project has.

In our little example above, we’d just need to create a separate virtual environment for both ProjectA and ProjectB, and we’d be good to go. Each environment, in turn, would be able to depend on whatever version of ProjectC they choose, independent of the other.

The great thing about this is that there are no limits to the number of environments you can have since they’re just directories containing a few scripts. Plus, they’re easily created using the virtualenv or pyenv command line tools.

### Components

*virtualenv* allows you to create a custom Python installation e.g. in a subdirectory of your project. Each of your projects can thus have their own python (or even several) under their respective virtualenv. It is perfectly fine for some/all virtualenvs to even have the same version of python (e.g. 2.7.16) without conflict - they live separately and don't know of each other. If you want to use any of those pythons, you have to activate it (by running a script which will temporarily modify your PATH to ensure that that virtualenv's bin/ directory comes first). From that point, calling python (or pip etc.) will invoke that virtualenv's version until you deactivate it (which restores the PATH).

*pyenv* operates on a wider scale than virtualenv - it holds a register of Python installations (and can be used to install new ones) and allows you to configure which version of Python to run when you use the python command. Sounds similar but practical use is a bit different. It works by prepending its shim python script to your PATH (permanently) and then deciding which "real" python to invoke. You can even configure pyenv to call into one of your virtualenv pythons (by using the pyenv-virtualenv plugin). Python versions you install using pyenv go into its $(pyenv root)/versions/ directory (by default, pyenv root is ~/.pyenv) so are more 'global' than virtualenv. Ordinarily, you can't duplicate Python versions installed through pyenv, at least doing so is not the main idea.

## Usage

## How It Works

At a high level, pyenv intercepts Python commands using shim
executables injected into your `PATH`, determines which Python version
has been specified by your application, and passes your commands along
to the correct Python installation.

### Understanding PATH

When you run a command like `python` or `pip`, your operating system
searches through a list of directories to find an executable file with
that name. This list of directories lives in an environment variable
called `PATH`, with each directory in the list separated by a colon:

    /usr/local/bin:/usr/bin:/bin

Directories in `PATH` are searched from left to right, so a matching
executable in a directory at the beginning of the list takes
precedence over another one at the end. In this example, the
`/usr/local/bin` directory will be searched first, then `/usr/bin`,
then `/bin`.

### Understanding Shims

pyenv works by inserting a directory of _shims_ at the front of your
`PATH`:
