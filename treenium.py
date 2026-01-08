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

    parser.add_argument("-if", "--include-files", nargs="+", default=[])
    parser.add_argument("-ie", "--include-extensions", nargs="+", default=[])
    parser.add_argument("-id", "--include-directories", nargs="+", default=[])

    args, unknown = parser.parse_known_args()
    if unknown:
        # 'unknown' is a list, e.g., ['--test', '--foo']
        # We grab the first one to show the user, or join them all
        unknown_command = unknown[0] 
        
        print(f'ERROR: unknown command "{unknown_command}"')
        print('')
        print('type -h or --help to see list of all available commands')
        sys.exit(1)
    
    has_excludes = args.exclude_files or args.exclude_extensions or args.exclude_directories
    has_includes = args.include_files or args.include_extensions or args.include_directories

    if has_excludes and has_includes:
        print("ERROR: You cannot use exclusion arguments (-ef, -ee, -ed) and inclusion arguments (-if, -ie, -id) at the same time.")
        print("Please choose one mode of operation.")
        print("")
        print('type -h or --help to see list of all available commands')
        sys.exit(1)

    if args.help:
        print("treenium.py - (c)eightynine77")
        print("")
        print("find me at github: https://github.com/eightynine77")
        print("")
        print("commands")
        print("=========================")
        print("[-h | --help] show the help message")
        print("")
        print("[-ef | --exclude-files] exclude files in the tree listing")
        print("NOTE: --exclude-files argument is case sensitive. so if a file is in upper case LIKE-THIS.jpeg or have a mix of upper and lower case characters Like-This.jpeg then you should type it exactly like the filename")
        print("[-ee | --exclude-extensions] exclude files by their file extension in the tree listing")
        print("[-ed | --exclude-directories] exclude folders/directories in the tree listing")
        print("NOTE: just like --exclude-files argument, this one is also case sensitive")
        print("")
        print("[-if | --include-files] include files in the tree listing")
        print("[-ie | --include-extensions] include files by their file extension in the tree listing")
        print("[-id | --include-directories] include folders/directories in the tree listing")
        print("")
        print("")
        print("example usage")
        print("========================")
        print("excluding files and folders:")
        print("just running treenium without arguments will list all directories and files.")
        print("")
        print('treenium "C:\\path\\to\\your\\folder"')
        print("this will list all files and folders in a specified directory.")
        print("")
        print('treenium --exclude-files example-file.txt "example picture.png" example-doc.docx')
        print("treenium --exclude-extensions exe txt jpeg png")
        print('treenium --exclude-directories folder1 "second folder" folder3')
        print('treenium "C:\\path\\to\\your\\folder" --exclude-files "1st text file.txt" picture.png')
        print('treenium "C:\\path\\to\\your\\folder" --exclude-extensions jpeg png')
        print('treenium "C:\\path\\to\\your\\folder" --exclude-directories "3rd folder"')
        print("")
        print("")
        print("including files and folders:")
        print('treenium --include-files example-file.txt "example picture.png" example-doc.docx')
        print("treenium --include-extensions exe txt jpeg png")
        print('treenium --include-directories folder1 "second folder" folder3')
        print('treenium "C:\\path\\to\\your\\folder" --include-files "1st text file.txt" picture.png')
        print('treenium "C:\\path\\to\\your\\folder" --include-extensions jpeg png')
        print('treenium "C:\\path\\to\\your\\folder" --include-directories "3rd folder"')
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

def should_include_file(name, args):
    """
    Checks if a specific file matches the inclusion criteria.
    """
    # 1. Check exact filename match (handles no-extension files too)
    if args.include_files and name in args.include_files:
        return True
    
    # 2. Check extension match
    if args.include_extensions:
        _, ext = os.path.splitext(name)
        # If the file has no extension, os.path.splitext returns empty string for ext
        if ext in args.include_extensions:
            return True
            
    return False

def has_matching_content(directory, args):
    """
    Recursively checks if a directory contains ANY file or folder 
    that matches the inclusion criteria.
    This is used to 'prune' empty directories from the view.
    """
    try:
        # We need to look at everything in this directory
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            
            if os.path.isdir(full_path):
                # If the directory name itself is whitelist, we keep it AND everything inside
                if args.include_directories and item in args.include_directories:
                    return True
                # Otherwise, we have to check inside it
                if has_matching_content(full_path, args):
                    return True
            else:
                # It's a file, does it match?
                if should_include_file(item, args):
                    return True
    except OSError:
        pass
    return False

def print_tree(directory, padding, print_files, args, force_show_all=False):
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a directory.")
        return

    # specific standard ASCII characters
    PIPE = "|"
    ELBOW = "\\"
    TEE = "+"
    dash = "-" 
    
    try:
        items = os.listdir(directory)
    except PermissionError:
        print(padding + "[Permission Denied]")
        return
    except OSError as e:
        print(padding + f"[Error: {e}]")
        return

    # Sort files for consistent order (case-insensitive)
    items.sort(key=lambda s: s.lower())

    inclusion_mode = (args.include_files or 
                      args.include_extensions or 
                      args.include_directories)
    
    # Filter out excluded items
    filtered_items = []
    for item in items:
        full_path = os.path.join(directory, item)
        is_dir = os.path.isdir(full_path)
        
        # If we are in a "force show" state (inside a matched -id folder), shows everything
        if force_show_all:
            filtered_items.append(item)
            continue

        if inclusion_mode:
            keep = False
            if is_dir:
                # If matches -id, we keep it (and will force show children later)
                if args.include_directories and item in args.include_directories:
                    keep = True
                # Else if it has relevant content deep down, we keep it (pathway)
                elif has_matching_content(full_path, args):
                    keep = True
            else:
                if should_include_file(item, args):
                    keep = True
            
            if keep:
                filtered_items.append(item)
        else:
            # Exclusion mode
            if not should_exclude(item, is_dir, args):
                filtered_items.append(item)

    count = len(filtered_items)
    for i, item in enumerate(filtered_items):
        is_last = (i == count - 1)
        connector = ELBOW if is_last else TEE
        print(f"{padding}{connector}{dash}{dash} {item}")

        full_path = os.path.join(directory, item)
        if os.path.isdir(full_path):
            new_padding = padding + ("    " if is_last else f"{PIPE}   ")
            
            # Determine if we should force show children
            # We force show if we are ALREADY forcing, OR if this specific folder matches -id
            will_force = force_show_all or (inclusion_mode and args.include_directories and item in args.include_directories)
            
            print_tree(full_path, new_padding, print_files, args, force_show_all=will_force)

def main():
    args = parse_arguments()
    
    # Normalize extensions to ensure they match (e.g., user types "py", we check ".py")
    # But user might type ".py", so we handle both.
    def normalize_exts(ext_list):
        norm = []
        for ext in ext_list:
            if not ext.startswith("."):
                norm.append("." + ext)
            else:
                norm.append(ext)
        return norm

    # Apply to both lists
    args.exclude_extensions = normalize_exts(args.exclude_extensions)
    args.include_extensions = normalize_exts(args.include_extensions)

    print(args.root_directory)
    print_tree(args.root_directory, "", True, args)

if __name__ == "__main__":
    main()
