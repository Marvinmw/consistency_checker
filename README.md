# Introduction

- This repository contains a collection of eight DeFi projects found within the `repo_check` folder. 
- Each project is accompanied by a respective .ipynb file, serving as a project-specific checker.
- Interaction with ChatGPT is necessary to use the output as input for the next stage.
- Reports for each DeFi project can be found in their respective folders, labeled as `revenue_**.md`. 
- These reports include the disclosure of hidden fees that may not be presented within the project's whitepaper.

While this tool currently faces some limitations in terms of accuracy, it has demonstrated the potential value of AIGC in evaluating the consistency between a project's whitepaper and its actual implementation.

# Dependencies

- Our tool utilizes tree-sitter to parse source code without requiring compilation. As a dependency, you will need to install `tree-sitter-solidity`.
- install `pytorch` and `transfomers`. Our tool use `SGPT` to mach the variables names.
- install `sympy` and nodeJs. 



