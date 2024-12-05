import os
from dotenv import load_dotenv, set_key


class EnvManager:
    def __init__(self, env_file=None):
        """
        Initializes the EnvManager class and loads the .env file.
        
        :param env_file: Path to the .env file. If None, defaults to .env in the current directory.
        """
        # Set the path to the .env file (default to current directory if no path is given)
        env_file_path = os.path.join(os.path.dirname(__file__), env_file if env_file else ".env")
        self.load_env_file(env_file_path)


    def update_env_file(self, new_env_file_path):
        self.env_file_path = new_env_file_path
        self.load_env_defaultKeys()


    def load_env_file(self, env_file_path):
        """
        Loads environment variables from a specific .env file at runtime.
        
        :param env_file_path: Path to the .env file to load.
        """
        if os.path.exists(env_file_path):
            load_dotenv(dotenv_path=env_file_path)
            # print(f"Loaded environment variables from: {env_file_path}")
        else:
            # print(f"Error: .env file not found at {env_file_path}")
            # If the .env file doesn't exist, create it with default values
            with open(env_file_path, 'w') as file:
                pass  # Just create an empty .env file if it doesn't exist
            # print(f"Created new .env file at: {env_file_path}")

        self.update_env_file(env_file_path)


    def load_env_defaultKeys(self):
        """
        Loads default keys or performs any other necessary initialization for environment variables.
        This method can be customized further if you need to add default keys or perform additional setup.
        """
        # Example of loading default keys (this can be customized)
        if self.env_file_path.endswith(".env"):
            envs = {
                "FRONTEND_PORT": "8501",
                "BACKEND_PORT": "5000",
                "LLM_API_KEY": "MY-SECRET-KEY",
                "LLM_SRC": "MY-LLM-SRC",
                "LLM_MODEL": "MY-LLM-MODEL",
            }
            for key, value in envs.items():
                self.add_env_key(key, value)  # Add a default key if it doesn't exist


    def load_env_keys(self):
        """
        Loads environment variables from the .env file during initialization.
        """
        load_dotenv(dotenv_path=self.env_file_path)
        # print(f"Loaded environment variables from: {self.env_file_path}")


    def get_env_key(self, key, default=None):
        """
        Retrieves the value of an environment variable.
        
        :param key: The environment variable name.
        :param default: The default value to return if the key is not found.
        :return: The value of the environment variable.
        """
        return os.getenv(key, default)


    def add_env_key(self, key, value):
        """
        Adds a new environment variable to the .env file.
        
        :param key: The environment variable name.
        :param value: The value to set for the environment variable.
        """
        if not self.get_env_key(key):  # If the key doesn't exist, add it
            self.update_env_key(key, value)
        else:
            pass
            # print(f"{key} already exists. Use 'update' method to modify it.")


    def update_env_key(self, key, value):
        """
        Updates the value of an environment variable in the .env file.
        
        :param key: The environment variable name.
        :param value: The value to set for the environment variable.
        """
        # Update environment variable in the current process
        os.environ[key] = value

        # Also update the .env file
        set_key(self.env_file_path, key, value)
        # print(f"Updated {key} = {value} in .env file.")


    def remove_env_key(self, key):
        """
        Removes an environment variable from the .env file.
        
        :param key: The environment variable name to remove.
        """
        # Remove the environment variable from the current process
        if key in os.environ:
            del os.environ[key]
            # print(f"Removed {key} from environment variables.")

        # Remove the key from the .env file
        with open(self.env_file_path, 'r') as file:
            lines = file.readlines()

        with open(self.env_file_path, 'w') as file:
            for line in lines:
                if not line.startswith(f"{key}="):
                    file.write(line)

        print(f"Removed {key} from .env file.")



if __name__ == "__main__":
    # Example usage:
    obj = EnvManager(".env")  # Initialize with default or custom .env file
    obj.add_env_key("NEW_KEY", "new_value")  # Add a new key-value pair
    print(obj.get_env_key("NEW_KEY"))  # Get the value of the newly added key
    obj.update_env_key("NEW_KEY", "updated_value")  # Update the value of the existing key
    obj.remove_env_key("NEW_KEY")  # Remove the key from both environment and .env file
