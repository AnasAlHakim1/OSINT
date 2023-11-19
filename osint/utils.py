import importlib.util

def run_script_on_log(log_file_path, script_path):
    try:
        with open(script_path, 'r') as script_file:
            script_code = script_file.read()

        # Execute the script in a custom namespace
        namespace = {}
        exec(script_code, namespace)

        # Access the count_words function from the script
        count_words_function = namespace.get('count_words')
        if count_words_function:
            result = count_words_function(log_file_path)
            return result
        else:
            return "count_words function not found in the script."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_parent_folders_as_string_with_root(folder):
    folder_name = ""
    parent = folder.parent_folder

    while parent:
        folder_name = f"{parent.name}\\{folder_name}"
        parent = parent.parent_folder

    if parent.parent_root:
        root_name = parent.parent_root.name
    else:
        root_name = ""

    return f"{root_name}\\{folder_name}" 

def get_parent_folders_as_string(child):
    folder_name = child.parent_folder.name if child.parent_folder else ""
    parent = child.parent_folder

    while parent and parent.parent_folder:
        folder_name = f"{parent.parent_folder.name}\\{folder_name}"
        parent = parent.parent_folder

    if parent.parent_root:  # Check if there is a parent folder (it's not None)
        root_name = parent.parent_root.name
    else:
        root_name = ""
        
    return f"{root_name}\\{folder_name}"