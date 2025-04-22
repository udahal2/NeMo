# ----------------------------------------------
# Script by Ujwol
# This script is designed to analyze and visualize a directory structure, 
# log it to a file, and optionally generate a new file called `project_generator.py`. 
# Additionally, multithreading is utilized to efficiently perform operations.
#
# - The script can be run normally or with the argument `-make_project=True` to generate a new script
# - The script will create a new file `project_generator.py` with the functionality to build a project
# - Multithreading ensures the project build process runs faster and with minimal blocking
#
# Usage:
# python directory-generator.py
# or 
# python directory-generator.py -make_project=True
# ----------------------------------------------

import os
import sys
import logging
import pyperclip
import argparse
from functools import lru_cache
from threading import Thread
from time import sleep

# -------------------- Configuration --------------------
MAX_DEPTH = 3
EXCLUSIONS = {
    'files': [os.path.basename(__file__), 'directory-setup.log', 'directory-generator.log'],
    'dirs': ['.git', '__pycache__', 'node_modules', 'venv', '.venv', 'env', '.idea'],
    'patterns': ['.', '~', '$']
}
LOG_CONFIG = {
    'filename': 'directory-setup.log',
    'level': logging.INFO,
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S'
}
# -------------------------------------------------------

class DirectoryObserver:
    """Observer pattern for logging events"""
    @staticmethod
    def log_event(event_type, message):
        logging.log(event_type, message)

class ExclusionStrategy:
    """Base exclusion logic with caching"""
    @staticmethod
    @lru_cache(maxsize=2048)
    def should_exclude(path: str, is_dir: bool = False) -> bool:
        base_name = os.path.basename(path)
        if is_dir:
            return any(
                base_name == excl or
                base_name.startswith(tuple(EXCLUSIONS['patterns']))
                for excl in EXCLUSIONS['dirs']
            )
        return any(
            base_name == excl or
            base_name.endswith('.log') or
            base_name.startswith(tuple(EXCLUSIONS['patterns']))
            for excl in EXCLUSIONS['files']
        )

class EnhancedExclusionStrategy(ExclusionStrategy):
    """Enhanced exclusion logic with full path checks"""
    @staticmethod
    @lru_cache(maxsize=2048)
    def should_exclude(path: str, is_dir: bool = False) -> bool:
        full_path = os.path.abspath(path)
        if any(full_path.endswith(excl) for excl in ['Thumbs.db', '.DS_Store']):
            return True
        return ExclusionStrategy.should_exclude(path, is_dir)

class SequentialDirectoryFormatter:
    """Class to handle the directory structure generation"""
    def __init__(self, root_path: str):
        self.root_path = root_path

    def generate_structure(self, current_path: str = None, depth: int = 0) -> str:
        if current_path is None:
            current_path = self.root_path
        if depth >= MAX_DEPTH:
            return ""

        structure = []
        try:
            for item in os.listdir(current_path):
                item_path = os.path.join(current_path, item)
                if EnhancedExclusionStrategy.should_exclude(item_path, is_dir=os.path.isdir(item_path)):
                    continue
                if os.path.isdir(item_path):
                    structure.append(f"{'  ' * depth}╰─ {item}/")
                    structure.append(self.generate_structure(item_path, depth + 1))
                else:
                    structure.append(f"{'  ' * depth}╰─ {item}")
        except PermissionError:
            structure.append(f"{'  ' * depth}╰─ [Permission Denied]")
        except FileNotFoundError:
            structure.append(f"{'  ' * depth}╰─ [File Not Found]")
        return "\n".join(structure)

def create_project_generator_script():
    """Create a new script called `project_generator.py`"""
    script_content = """
import os
import logging

class ProjectBuilder:
    def __init__(self, project_root: str):
        self.project_root = project_root
    
    def create_directories(self):
        try:
            os.makedirs(os.path.join(self.project_root, "src"))
            os.makedirs(os.path.join(self.project_root, "tests"))
            os.makedirs(os.path.join(self.project_root, "docs"))
            logging.info("Directories created successfully!")
        except Exception as e:
            logging.error(f"Error creating directories: {str(e)}")
    
    def create_files(self):
        try:
            with open(os.path.join(self.project_root, "README.md"), 'w') as f:
                f.write("# Project Overview\\n")
            logging.info("Project files created successfully!")
        except Exception as e:
            logging.error(f"Error creating files: {str(e)}")
    
    def build_project(self):
        logging.info("Building project...")
        self.create_directories()
        self.create_files()
        logging.info("Project build completed!")

def start_building(project_root: str):
    builder = ProjectBuilder(project_root)
    builder.build_project()

if __name__ == "__main__":
    project_root = os.getcwd()
    start_building(project_root)
    """
    with open("project_generator.py", 'w', encoding='utf-8') as f:
        f.write(script_content)
    logging.info("project_generator.py created!")

def main():
    """Main function with enhanced error handling and multithreading"""
    logging.basicConfig(**LOG_CONFIG)
    DirectoryObserver.log_event(logging.INFO, "Script started in: " + os.getcwd())
    
    parser = argparse.ArgumentParser(description="Directory Generator Script")
    parser.add_argument("-make_project", type=bool, default=False, help="Create project generator script")
    args = parser.parse_args()

    try:
        if args.make_project:
            create_project_generator_script()

            # Start a new thread to build the project using the newly created script
            thread = Thread(target=build_project_thread)
            thread.start()
            thread.join()

        # Regular directory structure generation
        processor = SequentialDirectoryFormatter(os.getcwd())
        raw_structure = processor.generate_structure()
        
        final_structure = "\n".join([
            line for line in raw_structure.split("\n")
            if not any(excl in line for excl in EXCLUSIONS['files'])
        ])

        # Save structure to log and copy to clipboard
        with open('directory-setup.log', 'w', encoding='utf-8') as f:
            f.write(f"Directory structure for: {os.getcwd()}\n\n")
            f.write(final_structure)
        pyperclip.copy(final_structure)

        DirectoryObserver.log_event(logging.INFO, "Structure visualization completed")
        print(final_structure)
        
        # End of file statement
        with open('directory-setup.log', 'a', encoding='utf-8') as f:
            f.write("\n" + "="*40)
            f.write("\nEnd of directory structure\n")
            f.write("="*40 + "\n")
    
    except Exception as e:
        DirectoryObserver.log_event(logging.CRITICAL, f"Critical failure: {str(e)}")
        sys.exit(1)

def build_project_thread():
    """Build the project in a new thread"""
    logging.info("Building project in a new thread...")
    sleep(2)  # Simulate time taken to run the build
    os.system("python project_generator.py")  # Executes the generated project building script

if __name__ == "__main__":
    main()
