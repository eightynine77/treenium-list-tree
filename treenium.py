import os
import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(add_help=False)
    
    parser.add_argument("root_directory", nargs="?", default=".")
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-ef", "--exclude-files", nargs="+", default=[])
    parser.add_argument("-ee", "--exclude-extensions", nargs="+", default=[])
    parser.add_argument("-ed", "--exclude-directories", nargs="+", default=[])

    args, unknown = parser.parse_known_args()
    if unknown:
        # 'unknown' is a list, e.g., ['--test', '--foo']
        # We grab the first one to show the user, or join them all
        unknown_command = unknown[0] 
        
        print(f'ERROR: unknown command "{unknown_command}"')
        print('')
        print('type -h or --help to see list of all available commands')
        sys.exit(1)

    if args.help:
        print("treenium.py - (c)eightynine77")
        print("")
        print("find me at github: https://github.com/eightynine77")
        print("")
        print("commands:")
        print("[-ef | --exclude-files] exclude files in the tree listing")
        print("[-ee, --exclude-extensions] exclude files by their file extension in the tree listing")
        print("[-ed | --exclude-directories] exclude folders/directories in the tree listing")
        print("[-h | --help] show the help message")
        print("")
        print("example usage:")
        print("just running treenium will list all directories and files.")
        print("treenium C:\\your\\directory")
        print("-----------------------------")
        print("-----------------------------")
        print("")
        print("-----------------------------")
        print("")
        sys.exit(0)
    return args

def should_exclude(name, is_dir, args):
    # Exclude directories by exact name
    if is_dir and name in args.exclude_directories:
        return True
    
    # Exclude files by exact name
    if not is_dir and name in args.exclude_files:
        return True
    
    # Exclude files by extension
    if not is_dir:
        _, ext = os.path.splitext(name)
        if ext in args.exclude_extensions:
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
    for ext in args.exclude_extensions:
        if not ext.startswith("."):
            normalized_exts.append("." + ext)
        else:
            normalized_exts.append(ext)
    args.exclude_extensions = normalized_exts

    print(args.root_directory)
    print_tree(args.root_directory, "", True, args)

if __name__ == "__main__":
    main()