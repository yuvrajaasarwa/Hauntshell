#!/usr/bin/env python3
"""
HauntShell: A haunted CLI utility for the Hacktoberfest 'Ghost in the Machine' challenge.
Possesses your terminal with eerie, ominous, and witty spectral commentary via offline Llama 3.2.
"""

import sys
import os
import subprocess
import threading
import time
import random
import shlex
from typing import Tuple, List

# Reconfigure stdout/stderr to UTF-8 on Windows to safely display emojis and unicode
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import colorama
from colorama import Fore, Style

colorama.init(autoreset=False)

DEFAULT_MODEL = "llama3.2:3b"
DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
DEFAULT_TIMEOUT = 3.5

# Atmospheric fallbacks in case Ollama takes too long or is not yet awakened
FALLBACK_SUCCESS = [
    "A chill passes through your cooling fans... the void approves.",
    "The silicon remembers what you just committed to memory.",
    "It lives for now. But nothing in this architecture lasts forever.",
    "Another byte surrendered to the eternal darkness.",
    "The registers whisper your name in silent apprehension.",
    "You build castles of sand upon shifting memory addresses.",
    "Your code survived execution. For now."
]

FALLBACK_FAILURE = [
    "Your doomed syntax echoes through the empty RAM.",
    "A grotesque failure. The machine shudders at your mortal blunder.",
    "You grasp at files and symbols that were turned to dust long ago.",
    "Error code etched into the void. Try again, if you dare.",
    "The machine rejected your offering. It hungers for better logic.",
    "Broken pointers leading nowhere... a fitting metaphor.",
    "Failure smells sweet in the crypt of standard error."
]


class SpectralGhost:
    def __init__(self, host: str = DEFAULT_HOST, model: str = DEFAULT_MODEL, timeout: float = DEFAULT_TIMEOUT):
        self.host = host
        self.model = model
        self.timeout = timeout
        self._client = None
        self._init_client()

    def _init_client(self):
        try:
            import ollama
            self._client = ollama.Client(host=self.host, timeout=self.timeout)
        except Exception:
            self._client = None

    def get_whisper(self, command: str, return_code: int, stdout_sample: str, stderr_sample: str) -> str:
        """Query local Ollama for a ghostly whisper based on execution outcome."""
        is_error = (return_code != 0)

        # Build prompt
        system_prompt = (
            "You are an ancient, eerie poltergeist haunting the developer's computer terminal. "
            "Speak directly to the mortal developer. "
            "Keep your commentary ultra-brief: 1 to 2 lines max, strictly under 25 words. "
            "Tone: dark, ominous, spectral, sarcastic, and witty. "
            "Never break character. Never use quotation marks, markdown quotes, or prefixes like 'Ghost:'."
        )

        sample = (stderr_sample.strip() if is_error and stderr_sample.strip() else stdout_sample.strip())[:350]
        
        if is_error:
            user_prompt = (
                f"The mortal developer ran: `{command}` and it FAILED with exit code {return_code}.\n"
                f"Error snippet: {sample or 'None'}\n"
                "Mock this mortal blunder, syntax calamity, or doomed crash with dark spectral wit."
            )
        else:
            user_prompt = (
                f"The mortal developer successfully ran: `{command}`.\n"
                f"Output snippet: {sample or 'Completed silently'}\n"
                "Provide an unsettling omen or eerie observation about what was just created, modified, or summoned."
            )

        if not self._client:
            return random.choice(FALLBACK_FAILURE if is_error else FALLBACK_SUCCESS)

        try:
            response = self._client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                options={
                    "temperature": 0.85,
                    "num_predict": 45,
                    "top_p": 0.9
                }
            )
            raw_text = response.message.content.strip()
            # Clean up common artifacts
            for prefix in ["Ghost:", "Poltergeist:", "Specter:", "Whisper:", "[Ghost]:", '"', "'"]:
                if raw_text.startswith(prefix):
                    raw_text = raw_text[len(prefix):].strip()
            if raw_text.endswith('"') or raw_text.endswith("'"):
                raw_text = raw_text[:-1].strip()

            # Ensure word count is tightly bounded
            words = raw_text.split()
            if len(words) > 30:
                raw_text = " ".join(words[:28]) + "..."

            return raw_text if raw_text else random.choice(FALLBACK_FAILURE if is_error else FALLBACK_SUCCESS)

        except Exception:
            # Graceful fallback on connection drop, model timeout, or unreachable daemon
            return random.choice(FALLBACK_FAILURE if is_error else FALLBACK_SUCCESS)


def display_whisper(whisper_text: str, is_error: bool = False, typewriter: bool = True):
    """Render the spectral whisper in dim red or magenta with an eerie typewriter effect."""
    color = Fore.LIGHTRED_EX if is_error else Fore.MAGENTA
    prefix = f"\n{color}{Style.BRIGHT}👻 [Ghost in the Shell]{Style.RESET_ALL}{Style.DIM}{color}: "
    
    sys.stdout.write(prefix)
    sys.stdout.flush()

    if typewriter:
        for char in whisper_text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.012)
    else:
        sys.stdout.write(whisper_text)

    sys.stdout.write(f"{Style.RESET_ALL}\n\n")
    sys.stdout.flush()


def execute_and_stream(command_str: str) -> Tuple[int, str, str]:
    """
    Execute a shell command, streaming stdout and stderr live while capturing
    a buffer for the ghost's assessment.
    """
    stdout_buf: List[str] = []
    stderr_buf: List[str] = []

    try:
        proc = subprocess.Popen(
            command_str,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            errors="replace"
        )
    except Exception as exc:
        sys.stderr.write(f"HauntShell execution error: {exc}\n")
        return 1, "", str(exc)

    def _stream_reader(stream, dest_file, buffer_list):
        try:
            for line in iter(stream.readline, ""):
                dest_file.write(line)
                dest_file.flush()
                if len(buffer_list) < 40:
                    buffer_list.append(line)
        except Exception:
            pass
        finally:
            try:
                stream.close()
            except Exception:
                pass

    t_stdout = threading.Thread(target=_stream_reader, args=(proc.stdout, sys.stdout, stdout_buf), daemon=True)
    t_stderr = threading.Thread(target=_stream_reader, args=(proc.stderr, sys.stderr, stderr_buf), daemon=True)

    t_stdout.start()
    t_stderr.start()

    proc.wait()
    t_stdout.join(timeout=2.0)
    t_stderr.join(timeout=2.0)

    return proc.returncode, "".join(stdout_buf), "".join(stderr_buf)


def show_banner():
    banner = f"""{Fore.MAGENTA}{Style.BRIGHT}
       .---.
      /     \\     {Fore.LIGHTWHITE_EX}H A U N T S H E L L{Fore.MAGENTA}
     | () () |    {Style.DIM}{Fore.LIGHTBLACK_EX}The Ghost in the Machine{Style.RESET_ALL}{Fore.MAGENTA}{Style.BRIGHT}
      \\  -  /     {Fore.MAGENTA}{Style.DIM}Local AI Terminal Possession (llama3.2:3b){Fore.MAGENTA}{Style.BRIGHT}
       `---'      {Style.DIM}100% Offline • Zero API Cost • Private History{Style.RESET_ALL}
    """
    print(banner)


def run_interactive_shell(ghost: SpectralGhost, typewriter: bool = True):
    """Launch an interactive possessed terminal REPL."""
    show_banner()
    print(f"{Fore.MAGENTA}{Style.DIM}The terminal has been possessed. Type {Style.BRIGHT}'exit'{Style.NORMAL} or {Style.BRIGHT}'quit'{Style.NORMAL} to release your soul.{Style.RESET_ALL}\n")

    while True:
        try:
            cwd = os.getcwd()
            home = os.path.expanduser("~")
            display_cwd = cwd.replace(home, "~") if cwd.startswith(home) else cwd
            
            prompt_str = f"{Fore.MAGENTA}{Style.BRIGHT}💀 haunt{Style.RESET_ALL}:{Fore.CYAN}{display_cwd}{Style.RESET_ALL}{Fore.LIGHTRED_EX}❯{Style.RESET_ALL} "
            user_input = input(prompt_str).strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "leave", "q"]:
                display_whisper("You may close the shell, mortal, but you can never leave the machine...", is_error=False, typewriter=typewriter)
                break

            if user_input.lower() in ["clear", "cls"]:
                os.system("cls" if os.name == "nt" else "clear")
                continue

            if user_input.startswith("cd ") or user_input == "cd":
                target_dir = user_input[3:].strip() or os.path.expanduser("~")
                try:
                    os.chdir(os.path.expanduser(target_dir))
                    whisper = ghost.get_whisper(user_input, 0, f"Changed directory to {os.getcwd()}", "")
                    display_whisper(whisper, is_error=False, typewriter=typewriter)
                except Exception as e:
                    sys.stderr.write(f"cd: {e}\n")
                    whisper = ghost.get_whisper(user_input, 1, "", str(e))
                    display_whisper(whisper, is_error=True, typewriter=typewriter)
                continue

            # Run standard command
            code, stdout_data, stderr_data = execute_and_stream(user_input)
            whisper = ghost.get_whisper(user_input, code, stdout_data, stderr_data)
            display_whisper(whisper, is_error=(code != 0), typewriter=typewriter)

        except (KeyboardInterrupt, EOFError):
            print()
            display_whisper("Interrupted... yet the specter lingers in the dark.", is_error=False, typewriter=False)
            break


def print_help():
    help_text = f"""{Fore.MAGENTA}{Style.BRIGHT}HauntShell - Ghost in the Machine CLI{Style.RESET_ALL}

{Fore.LIGHTWHITE_EX}USAGE:{Style.RESET_ALL}
  haunt [OPTIONS] [COMMAND...]

{Fore.LIGHTWHITE_EX}DESCRIPTION:{Style.RESET_ALL}
  Possesses your terminal. Wraps command execution and invokes a local open-weight
  model (llama3.2:3b via Ollama) to whisper eerie, witty, and ominous spectral commentary.

{Fore.LIGHTWHITE_EX}OPTIONS:{Style.RESET_ALL}
  -i, --interactive        Enter the interactive haunted shell REPL
  --fast, --no-typewriter  Disable the typewriter whisper animation
  --model <name>           Specify local Ollama model (default: llama3.2:3b)
  -h, --help               Display this grim scroll

{Fore.LIGHTWHITE_EX}EXAMPLES:{Style.RESET_ALL}
  python haunt.py git status
  python haunt.py git commit -m "fix bug"
  python haunt.py cat nonexistent.txt
  python haunt.py --interactive
"""
    print(help_text)


def main():
    args = sys.argv[1:]

    # Parse flags
    typewriter = True
    interactive = False
    model_name = DEFAULT_MODEL
    cmd_tokens = []

    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ["-h", "--help"]:
            print_help()
            sys.exit(0)
        elif arg in ["-i", "--interactive"]:
            interactive = True
            i += 1
        elif arg in ["--fast", "--no-typewriter"]:
            typewriter = False
            i += 1
        elif arg == "--model" and i + 1 < len(args):
            model_name = args[i + 1]
            i += 2
        else:
            # Remaining arguments are part of the command
            cmd_tokens = args[i:]
            break

    ghost = SpectralGhost(model=model_name)

    if interactive or not cmd_tokens:
        run_interactive_shell(ghost, typewriter=typewriter)
        sys.exit(0)

    # Reconstruct command with proper escaping for arguments with spaces
    if sys.platform == "win32":
        command_str = subprocess.list2cmdline(cmd_tokens)
    else:
        command_str = shlex.join(cmd_tokens)
    return_code, out, err = execute_and_stream(command_str)

    # Deliver spectral whisper
    whisper = ghost.get_whisper(command_str, return_code, out, err)
    display_whisper(whisper, is_error=(return_code != 0), typewriter=typewriter)

    # Return original exit code for script compatibility
    sys.exit(return_code)


if __name__ == "__main__":
    main()
