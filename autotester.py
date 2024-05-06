import sys
import yaml
import helper_scripts.default_values as dv

def read_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config_data = yaml.safe_load(file)
            return config_data
    except FileNotFoundError:
        print(f"Error: Config file '{config_file}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) > 2:
        print("Usage: python autotester.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1] if len(sys.argv) == 2 else dv.DEFAULT_CONFIG_FILE

    config_data = read_config(config_file)

    print("Config file contents:")
    print(config_data)

if __name__ == "__main__":
    main()
