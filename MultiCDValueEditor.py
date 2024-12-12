import os
from tkinter import Tk
from tkinter.filedialog import askdirectory

def process_xml_files(folder_path, cooldown_value):
    for root, dirs, files in os.walk(folder_path):
        if 'Event' in dirs:  # Check if 'Event' folder exists
            event_folder_path = os.path.join(root, 'Event')
            for filename in os.listdir(event_folder_path):
                if filename.endswith(".xml"):
                    file_path = os.path.join(event_folder_path, filename)
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
                            updated_lines.append(f'            <value>{cooldown_value}</value>\n')
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
    try:
        cooldown_value = input("Enter the cooldown value (0-60000): ")
        if not cooldown_value.isdigit() or not (0 <= int(cooldown_value) <= 60000):
            raise ValueError("Invalid input. Please enter a number between 0 and 60000.")

        cooldown_value = int(cooldown_value)
        process_xml_files(folder_path, cooldown_value)

        # Ask if the user wants to process a different project
        while True:
            choice = input("Do you want to change the Cooldown value of a different project? (yes/no): ").strip().lower()
            if choice == 'yes':
                folder_path = askdirectory(title="Select Folder with XML Files")
                if folder_path:
                    cooldown_value = input("Enter the cooldown value (0-60000): ")
                    if not cooldown_value.isdigit() or not (0 <= int(cooldown_value) <= 60000):
                        raise ValueError("Invalid input. Please enter a number between 0 and 60000.")

                    cooldown_value = int(cooldown_value)
                    process_xml_files(folder_path, cooldown_value)
                else:
                    print("No folder selected. Exiting...")
                    break
            elif choice == 'no':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")
    except ValueError as e:
        print(e)
else:
    print("No folder selected. Exiting...")
