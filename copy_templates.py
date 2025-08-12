import os
import shutil

old_dir = "db_populator/populator/templates"
new_dir = "db_populator/templates"

# Ensure the new directory exists
if not os.path.exists(new_dir):
    os.makedirs(new_dir)

# Copy the directory tree
shutil.copytree(old_dir, new_dir, dirs_exist_ok=True)

print("Templates copied successfully.")
