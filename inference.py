import os
import openai
import csv
from openai import OpenAI
import re

#  OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = ""
# read chatEDA bench
def load_tasks(path="ChatEDA-Bench.txt"):
    tasks = []
    current = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            text = line.strip()
            # new task
            if text.startswith("<Requirement>"):
                if current:
                    tasks.append(" ".join(current))
                    current = []
                continue
            # skip empty line
            if not text:
                continue
            current.append(text)
        # save last task
        if current:
            tasks.append(" ".join(current))
    return tasks

# 3. INFERENCE
def eval_task(task, model="gpt-4"):
    prompt = f"""### System:
You are AI assistant, capable of utilizing numerous
tools and functions. User will give you a task.
Your job is to generate a Python script to complete
the task using the provided tools and functions.

While performing the task think step-by-step and
justify your steps.

You have access to the following tools and functions:
chateda is an autonomous tool that can automate the RTL
to GDSII flow by executing steps through
tools(functions) with various parameters.
tune is a function that can perform parameter tuning.
Specifically, you have access to the following details
of the provided tools and functions:
<<<API documents>>>
### User:
<<<Requirement>>>{task}

Let's first describe and explain what the task is asking. Then, analyze how to complete the task step
by step using the provided tools and functions.Finally, generate the Python script according to your analysis.

### Assistant:
<<<Response>>>"""
    
    client = OpenAI(api_key=openai.api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role":"user","content":prompt}],
        temperature=0.0
    )
    raw = resp.choices[0].message.content
    # extract ```python ... ``` code block
    match = re.search(r'```(?:python)?\s*([\s\S]*?)```', raw)
    code = match.group(1).strip() if match else raw
    return code

if __name__ == "__main__":
    script_dir = "generated_scripts"
    result_dir = "results"
    os.makedirs(script_dir, exist_ok=True)
    os.makedirs(result_dir, exist_ok=True)

    tasks = load_tasks()
    total = len(tasks)

    result_csv = os.path.join(result_dir, "chateda_eval_results.csv")
    with open(result_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["task_id", "script_path"])

        for i, task in enumerate(tasks, 1):
            code = eval_task(task)
            print(f"[{i}/{total}] save：{task[:50]}...")

            safe_name = task.replace("\n", " ")[:10].replace(" ", "_")
            filename = f"{i:02d}_{safe_name}.py"
            script_path = os.path.join(script_dir, filename)
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(code)

            writer.writerow([i, script_path])
