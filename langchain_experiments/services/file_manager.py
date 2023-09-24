
import datetime
import os
import inspect

def get_caller_file_name():
    stack = inspect.stack()
    frame = stack[2]
    full_path = frame.filename
    file_name = os.path.basename(full_path)
    file_name_without_extension, _ = os.path.splitext(file_name)
    return file_name_without_extension

def generate_output_file()->str:

    # I may create output in another function
    output_dir = "./langchain_experiments/summary/outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_name_caller = get_caller_file_name()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = f"{output_dir}/output_{file_name_caller}_{current_time}.txt"
    return filename

    