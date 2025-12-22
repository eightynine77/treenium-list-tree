import os
import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description="A Python-based directory tree generator with exclusion features.")
    
    parser.add_argument(
        "root_dir", 
        nargs="?", 
        default=".", 
        help="The directory to list (default: current directory)"
    )
    
    parser.add_argument(
        "-xf", "--exclude-files", 
        nargs="+", 
        default=[], 
        help="List of specific file names to exclude (e.g. secret.txt config.json)"
    )
    
    parser.add_argument(
        "-xe", "--exclude-exts", 
        nargs="+", 
        default=[], 
        help="List of file extensions to exclude (e.g. .pyc .tmp .log)"
    )
    
    parser.add_argument(
        "-xd", "--exclude-dirs", 
        nargs="+", 
        default=[], 
        help="List of folder names to exclude (e.g. node_modules .git __pycache__)"
    )

    return parser.parse_args()

def should_exclude(name, is_dir, args):
    # Exclude directories by exact name
    if is_dir and name in args.exclude_dirs:
        return True
    
    # Exclude files by exact name
    if not is_dir and name in args.exclude_files:
        return True
    
    # Exclude files by extension
    if not is_dir:
        _, ext = os.path.splitext(name)
        if ext in args.exclude_exts:
            return True
            
    return False

def print_tree(directory, padding, print_files, args):
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a directory.")
        return

    # specific standard ASCII characters
    PIPE = "|"
    ELBOW = "\\"
    TEE = "+"
    dash = "-" 
    
    try:
        files = os.listdir(directory)
    except PermissionError:
        print(padding + "[Permission Denied]")
        return
    except OSError as e:
        print(padding + f"[Error: {e}]")
        return

    # Sort files for consistent order (case-insensitive)
    files.sort(key=lambda s: s.lower())
    
    # Filter out excluded items
    filtered_files = []
    for f in files:
        full_path = os.path.join(directory, f)
        is_dir = os.path.isdir(full_path)
        if not should_exclude(f, is_dir, args):
            filtered_files.append(f)

    # Iteration logic
    count = len(filtered_files)
    for i, file in enumerate(filtered_files):
        is_last = (i == count - 1)
        
        # Build the connector string
        connector = ELBOW if is_last else TEE
        # Standard ASCII representation: +-- or \--
        prefix = f"{connector}{dash}{dash} "
        
        print(padding + prefix + file)

        full_path = os.path.join(directory, file)
        
        if os.path.isdir(full_path):
            # Prepare padding for the next level
            # If this was the last item, the vertical bar is not needed for children
            if is_last:
                new_padding = padding + "    " 
            else:
                new_padding = padding + f"{PIPE}   "
            
            print_tree(full_path, new_padding, print_files, args)

def main():
    args = parse_arguments()
    
    # Normalize extensions to ensure they match (e.g., user types "py", we check ".py")
    # But user might type ".py", so we handle both.
    normalized_exts = []
    for ext in args.exclude_exts:
        if not ext.startswith("."):
            normalized_exts.append("." + ext)
        else:
            normalized_exts.append(ext)
    args.exclude_exts = normalized_exts

    print(args.root_dir)
    print_tree(args.root_dir, "", True, args)

if __name__ == "__main__":
    main()