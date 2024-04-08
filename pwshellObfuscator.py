import os
import string
import random 

# List of environment variables to consider for obfuscation
env_vars = [
    "CommonProgramFiles", "ALLUSERSPROFILE", "CommonProgramW6432", "ComSpec", "PATHEXT",
    "ProgramData", "ProgramFiles", "ProgramW6432", "PSModulePath", "PUBLIC", "SystemDrive",
    "SystemRoot", "windir"
]

# Build a map of environment variables containing printable characters
mapa_env = {}
for var in env_vars:
    value = os.getenv(var)
    if value is None:
        print(f"Error: Environment variable '{var}' not found.")
        exit(1)
    for i, c in enumerate(value):
        if c in string.printable:
            if c not in mapa_env:
                mapa_env[c] = {}
            if var not in mapa_env[c]:
                mapa_env[c][var] = []
            mapa_env[c][var].append(i)

# Encode characters into PowerShell syntax
def encodeEnv(string):
    encoded = []
    for c in string:
        possible_vars = mapa_env.get(c, {})
        if not possible_vars:
            encoded.append(f'[char]{ord(c)}')
        else:
            var_chosen = random.choice(list(possible_vars.keys()))
            index_chosen = random.choice(possible_vars[var_chosen])
            encoded.append(f'$env:{var_chosen}[{index_chosen}]')
    return encoded

# Obfuscate PowerShell command
def obfuscatePshell(string):
    iex = encodeEnv('iex')
    parts = encodeEnv(string)
    stage_iex = f'({",".join(iex)} -Join ${random.randint(1, 99999)}) '
    payload_stage = f'({",".join(parts)} -Join ${random.randint(1, 99999)})'
    return f'& {stage_iex} {payload_stage}'

# Prompt user for PowerShell command
def main():
    pshell_command = input("Type the PowerShell command: ")
    try:
        obfuscated_command = obfuscatePshell(pshell_command)
        print("Obfuscated PowerShell Command:")
        print(obfuscated_command)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
