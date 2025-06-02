# chateda-bench

## Project Overview
## Installation

This project integrates with [ChatEDA](https://github.com/wuhy68/ChatEDA) to automatically generate and execute EDA scripts. By calling the OpenAI API, it converts high-level design intent into OpenROAD TCL scripts, enabling a complete flow from Verilog to GDSII.

```
pip install openai
```
Refer to the ChatEDA repository’s README for any extra dependencies as needed.
## Usage
Generate EDA scripts:
In the project root directory, run:
```
python generate_eda.py
```
Execute the generated script:
```
cd generated_scripts
python your_file_name.py
```
## Notice:
#Ensure you have a working OpenROAD installation (commands like read_verilog, read_lef, synth_design, place_design, clock_tree_synthesis, route_design, and write_gds must be available in your environment).

#Before running generate_eda.py, set your OpenAI API key as an environment variable:

#The generated Python scripts assume the required Verilog/LEF files are in the current directory. Modify file names and paths in the script if your design files are located elsewhere.

