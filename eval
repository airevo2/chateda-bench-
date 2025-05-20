import subprocess
import shlex
import os

def run_openroad(script_path, log_dir="logs", timeout=300):
    """
    """

    os.makedirs(log_dir, exist_ok=True)
    base = os.path.basename(script_path).rsplit('.', 1)[0]
    stdout_log = os.path.join(log_dir, f"{base}.out.log")
    stderr_log = os.path.join(log_dir, f"{base}.err.log")


    cmd = f"openroad {script_path}"
    try:

        proc = subprocess.run(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            universal_newlines=True
        )

        with open(stdout_log, "w") as f_out:
            f_out.write(proc.stdout)
        with open(stderr_log, "w") as f_err:
            f_err.write(proc.stderr)


        success = (proc.returncode == 0) and ("ERROR" not in proc.stderr.upper())
        return success, proc.stdout, proc.stderr

    except subprocess.TimeoutExpired as e:

        with open(stderr_log, "w") as f_err:
            f_err.write(f"TIMEOUT after {timeout} seconds\n")
        return False, "", f"TIMEOUT after {timeout} seconds"

if __name__ == "__main__":

    script_dir = "generated_scripts"
    results = []
    for fn in os.listdir(script_dir):
        if fn.endswith(".tcl") or fn.endswith(".tcl.py"):
            path = os.path.join(script_dir, fn)
            ok, out, err = run_openroad(path)
            status = "PASS" if ok else "FAIL"
            print(f"{fn}: {status}")
            results.append((fn, status))

    total = len(results)
    passed = sum(1 for _, s in results if s == "PASS")
    print(f"\n通过率：{passed}/{total} = {passed/total:.2%}")
