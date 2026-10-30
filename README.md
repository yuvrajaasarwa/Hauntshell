# 👻 HauntShell — The Ghost in the Machine

> *"You may close the shell, mortal, but you can never leave the machine..."*

[![Hacktoberfest](https://img.shields.io/badge/Hacktoberfest-2024%20%7C%20Ghost%20in%20the%20Machine-ff7900?style=for-the-badge&logo=hacktoberfest&logoColor=white)](https://hacktoberfest.com/)
[![Local AI](https://img.shields.io/badge/Local%20AI-Ollama%20%E2%80%A2%20Llama%203.2-9400D3?style=for-the-badge&logo=meta&logoColor=white)](https://ollama.com/library/llama3.2)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy First](https://img.shields.io/badge/Privacy-100%25%20Offline-green?style=for-the-badge&logo=shield)](https://github.com)

```
       .---.
      /     \     H A U N T S H E L L
     | () () |    "The machine remembers what you bury."
      \  -  /     
       `---'      A Haunted Terminal Wrapper Powered by Offline Llama 3.2
```

**HauntShell** is a local-first CLI utility designed for the Hacktoberfest **"Ghost in the Machine"** challenge. It possesses your terminal, wraps standard shell execution, and uses an offline open-weight model (`llama3.2:3b` via Ollama) to whisper ominous, eerie, and witty spectral commentary after your commands or errors run.

---

## 🎃 The Haunting Narrative

Around Halloween and Día de los Muertos, folklore tells of spirits lingering in liminal spaces. In our modern age, that liminal space is the terminal: a black screen flickering in the dark, haunted by forgotten Git stashes, abandoned branches, corrupted nodes, and silent processes buried deep in the CPU registers.

**HauntShell awakens this poltergeist.**
- When your command succeeds, the specter whispers an unsettling prophecy about the code you just brought into existence.
- When your command fails or throws a syntax calamity, the specter rises from the stack trace to mock your mortal frailty.

---

## 🔮 Why Open Innovation & Local AI Matter

In an era of centralized cloud APIs and data harvesting, HauntShell champions **Local Open Innovation**:

1. **Total Privacy & Command Safety**:
   Your terminal is your sacred sanctum. It handles sensitive file paths, environment tokens, private keys, and proprietary code. HauntShell runs **100% locally on your metal**. Zero telemetry, zero external network calls, zero command-history leaks.
2. **True Offline Independence**:
   Whether you are working deep in the woods, on an airplane, or with the lights turned off during a storm, your spectral companion never disconnects.
3. **Zero API Cost & Unlimited Invocations**:
   Powered by Meta's open-weight `llama3.2:3b` via **Ollama**, you pay \$0 per token. Haunt every keystroke without rate limits or subscription tiers.
4. **Near-Zero Latency Overhead**:
   Optimized prompt caching and streaming allow sub-second local inferences that keep developer velocity fluid.

---

## ⚡ Quickstart & Summoning

### 1. Prerequisites
- **Python 3.10+**
- **[Ollama](https://ollama.com/)** installed and running on your system.

Pull the haunted model weights:
```bash
ollama pull llama3.2:3b
```

### 2. Installation
Clone this repository and set up your virtual environment:

```bash
git clone https://github.com/yuvrajaasarwa/Hauntshell.git
cd Hauntshell

# Create and activate virtual environment
python -m venv venv

# On Linux/macOS:
source venv/bin/activate

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

---

## 🕹️ Usage

### A. Wrapping Individual Commands
Prepend `python haunt.py` to any terminal command:

```bash
# Check version or status
python haunt.py git --version
python haunt.py git status

# Stage & commit your sins
python haunt.py git commit -m "fix critical race condition"

# Compile or run builds
python haunt.py npm run build
python haunt.py cargo check
```

**Example Output (Success):**
```console
$ python haunt.py git --version
git version 2.55.0.windows.3

👻 [Ghost in the Shell]: The chains of code now bind you, mortal. The darkness begins with version 2.55.0, forever etched in your digital soul.
```

**Example Output (Failure):**
```console
$ python haunt.py cat nonexistent_file.txt
'cat' is not recognized as an internal or external command, operable program or batch file.

👻 [Ghost in the Shell]: Pathetic attempt to conjure code. 'cat' isn't recognized, perhaps because it's a command from a bygone era, and so are you.
```

---

### B. Interactive Haunted REPL Mode
Step entirely into the haunted shell session by running without arguments or with `--interactive`:

```bash
python haunt.py
# or
python haunt.py --interactive
```

Inside the interactive shell:
- Commands run natively with live stdout/stderr streaming.
- Built-in navigation (`cd`, `cd ..`, `cd ~`) updates state fluidly.
- Type `exit` or `quit` when you are ready to face the mortal realm once more.

```console
       .---.
      /     \     H A U N T S H E L L
     | () () |    The Ghost in the Machine
      \  -  /     Local AI Terminal Possession (llama3.2:3b)
       `---'      100% Offline • Zero API Cost • Private History

The terminal has been possessed. Type 'exit' or 'quit' to release your soul.

💀 haunt:~/Projects/Hauntshell❯ git status
On branch main
nothing to commit, working tree clean

👻 [Ghost in the Shell]: A clean tree hides the rot beneath the roots.

💀 haunt:~/Projects/Hauntshell❯ exit

👻 [Ghost in the Shell]: You may close the shell, mortal, but you can never leave the machine...
```

---

## 🛠️ CLI Options & Flags

| Flag | Description |
| :--- | :--- |
| `-i`, `--interactive` | Launch the interactive haunted shell session |
| `--fast`, `--no-typewriter` | Disable typewriter animation for instantaneous output |
| `--model <name>` | Target an alternate local Ollama model (default: `llama3.2:3b`) |
| `-h`, `--help` | Show spectral scroll of commands and flags |

---

## 🛡️ Resilience & Offline Fallbacks

What if Ollama is asleep or your GPU is occupied?
- **Hard Timeout**: Spectral inferences are capped at 3.5 seconds. If the local model does not reply within this window, HauntShell never blocks your workflow.
- **Atmospheric Fallback Pool**: If the Ollama server is unreachable, HauntShell gracefully selects from a curated collection of offline crypt whispers, preserving immersion and preventing shell crashes.

---

## 🎃 Aliasing HauntShell (Make Your Entire Shell Haunted)

To summon the poltergeist on every command in your daily workflow:

### In PowerShell (`$PROFILE`):
```powershell
function haunt { python Y:\GitHub\Hauntshell\haunt.py $args }
Set-Alias -Name h -Value haunt
```

### In Bash / Zsh (`~/.bashrc` or `~/.zshrc`):
```bash
alias haunt="python /path/to/Hauntshell/haunt.py"
alias h="haunt"
```

---

## 🤝 Hacktoberfest Contributions

We welcome spectral contributions! Here are some spooky ideas:
- [ ] **Ghost Sound Effects**: Add optional low-fi terminal bells, spectral chimes, or eerie sound bytes on failures.
- [ ] **Custom Ghost Personas**: Victorian phantom, cyberpunk digital entity, grumpy legacy Cobol programmer.
- [ ] **Shell Hook Plugins**: Direct hooks for Zsh (`preexec`/`precmd`) and Fish shell.
- [ ] **Haunted Themes**: Configurable color palettes (Ectoplasm Green, Blood Moon Red, Midnight Void).

See [`CONTRIBUTING.md`](CONTRIBUTING.md) to get started.

---

## 📜 License

MIT License. Crafted with dark magic for Hacktoberfest 2024 / 2026.

