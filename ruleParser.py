import os
import yaml

def represent_multiline_string(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, represent_multiline_string)

# Function to save each rule as a separate YAML file, using the id for the filename, and ensure it's valid YAML
def save_rule_files(rules, output_dir, limit=None):
    for i, rule in enumerate(rules):
        if limit is not None and i >= limit:
            break
        # Extract the id and modify it for filename usage
        rule_id = rule.get('id', f'rule_{i+1}')
        print(f"Processing rule {i+1} with ID: {rule_id}")  # Debug: show the rule ID being processed

        # Create filename by removing the last segment after the last dot
        rule_filename = '.'.join(rule_id.split('.')[:-1]) + '.yaml'
        print(f"Generated filename: {rule_filename}")  # Debug: show the generated filename

        # Prepare the file path and save the file
        rule_path = os.path.join(output_dir, rule_filename)
        with open(rule_path, 'w') as file:
            # Wrap the rule in a 'rules' list to ensure valid YAML output
            yaml.dump({'rules': [rule]}, file, default_flow_style=False, sort_keys=False)
        print(f"Saved file at: {rule_path}")  # Debug: confirm the file save location

# Load the YAML file to get the rules
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    print("YAML data loaded successfully.")  # Debug: confirm data load
    return data

# Main function to process the YAML file and save rules
def process_and_save_rules(file_path, output_dir):
    # Load rules from file
    rules_data = load_yaml(file_path)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory created/verified at {output_dir}")  # Debug: confirm directory setup

    # Save all rules into separate files
    save_rule_files(rules_data['rules'], output_dir)

# Path to the YAML file containing the rules
file_path = '/Users/erickufta/Projects/rulesAsCode/semgrepRules.yaml'

# Output directory to store individual rule files
output_dir = '/Users/erickufta/Projects/rulesAsCode/rules'

# Process the rules and save to files
process_and_save_rules(file_path, output_dir)
