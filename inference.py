
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

# 准备输出目录
    script_dir = "generated_scripts"
    result_dir = "results"
    os.makedirs(script_dir, exist_ok=True)
    os.makedirs(result_dir, exist_ok=True)

    # CSV 结果文件
    result_csv = os.path.join(result_dir, "chateda_eval_results.csv")
    with open(result_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["task_id", "passed", "script_path"])

        # 遍历所有任务
        for i, task in enumerate(tasks, 1):
            passed, code = eval_task(task)
            status = "✔" if passed else "✘"
            print(f"[{i}/{total}] {status} {task[:50]}...")

            # 保存脚本：eg. generated_scripts/01_simple_process.py
            # 使用任务序号+前 5 个汉字作为文件名辅助
            safe_name = task.replace("\n", " ")[:10].replace(" ", "_")
            filename = f"{i:02d}_{safe_name}.py"
            script_path = os.path.join(script_dir, filename)
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(code)
