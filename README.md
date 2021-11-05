# Mutation Testing Online
This is a simple web project for running mutation tests in Python language.
Developed in Flask and deployed in heroku.
The interface is simple so that a user can easily understand the mutation testing process.

Use example in the next link: https://drive.google.com/file/d/1ihS54dunQV2FBTD0kDs0F3GK_4KeFM1G/view

![example](readme_media/example.gif)

## Mutation Testing
___
From article at [Wikipedia](https://en.wikipedia.org/wiki/Mutation_testing):

> **Mutation testing** (or *mutation analysis* or *program mutation*) is used to design new software tests and evaluate the quality of existing software tests. Mutation testing involves modifying a program in small ways. Each mutated version is called a *mutant* and tests detect and reject mutants by causing the behavior of the original version to differ from the mutant. This is called *killing* the mutant. Test suites are measured by the percentage of mutants that they kill. New tests can be designed to kill additional mutants. Mutants are based on well-defined *mutation operators* that either mimic typical programming errors (such as using the wrong operator or variable name) or force the creation of valuable tests (such as dividing each expression by zero). The purpose is to help the tester develop effective tests or locate weaknesses in the test data used for the program or in sections of the code that are seldom or never accessed during execution. Mutation testing is a form of white-box testing.

# MutPy

[Repository](https://github.com/greyngs/mutpy)

> MutPy is a mutation testing tool for Python 3.3+ source code. MutPy supports standard unittest module, generates YAML/HTML reports and has colorful output. It applies mutation on AST level. You could boost your mutation testing process with high order mutations (HOM) and code coverage analysis.

## Bugs and future work 

* some operators don't work correctly causing the app crash, maybe it's the version of mutpy that is installed in heroku.
* We will try to automate the deploy so that users can install the libraries they need in their tests.
