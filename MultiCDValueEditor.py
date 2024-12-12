import os
from tkinter import Tk
from tkinter.filedialog import askdirectory

def process_xml_files(folder_path):
    # List to store the paths of files that need updating
    files_to_update = []

    # First pass: Check all files for triggerCooldown property
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Check if the property exists
            if '<property name="triggerCooldown">' in content:
                files_to_update.append(file_path)

    # If files need updating, ask the user for a new value
    if files_to_update:
        user_value = input(f"Enter new value for triggerCooldown: ").strip()
        if not user_value:
            user_value = "10"  # Default to 10 if no input is provided

        # Second pass: Update the value for all files
        for file_path in files_to_update:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            updated_lines = []
            inside_property_block = False

            for line in lines:
                if '<property name="triggerCooldown">' in line:
                    inside_property_block = True
                    updated_lines.append(line)  # Keep the opening line as is
                elif inside_property_block and '<value>' in line:
                    updated_lines.append(f'            <value>{user_value}</value>\n')  # Replace the value
                    inside_property_block = False  # Exit the block
                else:
                    updated_lines.append(line)  # Keep all other lines as is

            # Save the updated lines back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(updated_lines)
            print(f"Processed: {file_path}")
    else:
        print("No files with triggerCooldown property found.")

# Set up tkinter to allow folder selection
Tk().withdraw()  # Hide the root window
folder_path = askdirectory(title="Select Folder with XML Files")

if folder_path:
    process_xml_files(folder_path)
else:
    print("No folder selected. Exiting...")
