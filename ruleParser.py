import os
import yaml
import requests

# Semgrep token with API access
token = os.environ.get("SEMGREP_APP_TOKEN")

# Test options
output_dir = './tests/rules3'
test_limit = 20

def represent_multiline_string(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, represent_multiline_string)

def fetch_yaml_from_endpoint(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return yaml.safe_load(response.text)
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def save_rule_files(rules, output_dir, limit=None):
    for i, rule in enumerate(rules):
        if limit is not None and i >= limit:
            break
        rule_id = rule.get('id', f'rule_{i+1}')
        rule_filename = '.'.join(rule_id.split('.')[:-1]) + '.yaml'
        rule_path = os.path.join(output_dir, rule_filename)
        with open(rule_path, 'w') as file:
            yaml.dump({'rules': [rule]}, file, default_flow_style=False, sort_keys=False)
        print(f"Saved {rule_filename}")

def process_and_save_rules(rules_data, output_dir, limit=None):
    os.makedirs(output_dir, exist_ok=True)
    save_rule_files(rules_data['rules'], output_dir, limit=limit)

# URL to the ruleset YAML data. Pulls down everything you have access to
url = 'https://semgrep.dev/c/r/all'

# Authorization header
headers = {
    'Authorization': f'Bearer {token}'
}

# Fetching rules and process them
try:
    rules_data = fetch_yaml_from_endpoint(url, headers)
    process_and_save_rules(rules_data, output_dir, limit=test_limit)
    print("Processing completed successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
