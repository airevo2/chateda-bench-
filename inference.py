
import os
import openai

#  OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# read chatEDA bench
def load_tasks(path="data/test/ChatEDA-Bench.txt"):
    with open(path, "r", encoding="utf-8") as f:
        tasks = [line.strip() for line in f if line.strip()]
    return tasks

# 3. INFERENCE
def eval_task(task, model="gpt-4"):
    prompt = f"### System:
You are AI assistant, capable of utilizing numerous
tools and functions. User will give you a task.
Your job is to generate a Python script to complete
the task using the provided tools and functions.
,→
,→
,→
While performing the task think step-by-step and
justify your steps.,→
You have access to the following tools and functions:
chateda is an autonomous tool that can automate the RTL
to GDSII flow by executing steps through
tools(functions) with various parameters.
,→
,→
tune is a function that can perform parameter tuning.
Specifically, you have access to the following details
of the provided tools and functions:,→
<<<API documents>>>
### User:
<<<Requirement>>>{task}
Let's first describe and explain what the task is
asking. Then, analyze how to complete the task step
by step using the provided tools and functions.
Finally, generate the Python script according to
your analysis.
,→
,→
,→
,→
### Assistant:
<<<Response>>>"
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    code = resp.choices[0].message["content"]
    # checking syntax error
    passed = "openroad.run" in code
    return passed, code

