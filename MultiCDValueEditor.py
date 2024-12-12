import os
from tkinter import Tk
from tkinter.filedialog import askdirectory

def process_xml_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            updated_lines = []
            for line in lines:
                # Check if the line is a self-closing EventAutomatableProperties tag
                if '<object class="EventAutomatableProperties"' in line and '/>' in line:
                    # Replace self-closing tag with the correct block
                    new_line = line.replace('/>', '>')
                    updated_lines.append(new_line.strip() + '\n')  # Ensure proper spacing
                    updated_lines.append('        <property name="triggerCooldown">\n')
                    updated_lines.append('            <value>10</value>\n')
                    updated_lines.append('        </property>\n')
                    updated_lines.append('    </object>\n')
                else:
                    updated_lines.append(line)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(updated_lines)
            print(f"Processed: {filename}")

# Set up tkinter to allow folder selection
Tk().withdraw()  # Hide the root window
folder_path = askdirectory(title="Select Folder with XML Files")

if folder_path:
    process_xml_files(folder_path)
else:
    print("No folder selected. Exiting...")
