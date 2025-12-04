from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align
from time import sleep
import json
import google.generativeai as genai
from dotenv import load_dotenv
import os
import subprocess
import shlex

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in the environment!")

console = Console(force_terminal=True)

def boot_sequence():
    # 1. Show the banner
    banner_text = Text("""
█▄░█ █▀▀ █▀█ █▀▀ █▀█ █▀█ █▀▀ █▀▀
█░▀█ ██▄ █▄█ █▀░ █▄█ █▀▄ █▄█ ██▄""", style="bold cyan")


    banner_panel = Panel(
    Align.center(banner_text),
    border_style="bright_cyan",
    padding=(1, 4),
    expand=False)

    console.print(Align.center(banner_panel))

    console.print(Panel("⚒️ [bold cyan]NeoForge v0.5[/bold cyan]\n[italic]Arise, Developer.[/italic]", border_style="bright_red"))
    
    # 2. Boot animation
    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[cyan]{task.description}"),
        console=console
    ) as progress:
        tasks = [
            progress.add_task("Initializing AI core...", total=None),
            progress.add_task("Syncing memory modules...", total=None),
            progress.add_task("Forging local context...", total=None),
        ]
        for i in range(3):
            sleep(0.5)
            progress.remove_task(tasks[i])
    
    # 3. Final greeting
    console.print("\n[bold green]✓ Boot sequence complete![/bold green]")
    console.print("[italic bright_white]Welcome back, Artisan.[/italic bright_white]")

os.system("cls" if os.name == "nt" else "clear")
boot_sequence()



def extract_json(response):
    try:
        # Use the stable path to text
        raw_text = response.candidates[0].content.parts[0].text
    except Exception:
        return None, "Model returned no valid text part."

    try:
        data = json.loads(raw_text)
    except Exception:
        return None, f"Invalid JSON: {raw_text}"

    return data, None

ALLOWED_COMMANDS = {
    "ls", "cat", "head", "tail", "wc", "grep", "find", "pwd", "file", "echo",
    "du", "df", "tree", "stat", "readlink",
    "date", "uptime", "whoami", "id", "uname", "ps", "free", "env", "locale"
}

FORBIDDEN_CHARS = set("; & | > < $ ` ! { } ( )".split())
DANGEROUS_FLAGS = {"-delete", "-exec", "-execdir", "-ok", "-okdir"}

def safe_execute(cmd_list):
    if not cmd_list:
        return
    if not isinstance(cmd_list, list) :
        print("Invalid command format.", cmd_list)
        return

    # Main command
    cmd = cmd_list[0]

    # Ensure it’s allowed
    if cmd not in ALLOWED_COMMANDS:
        print(f"Blocked command: {cmd}")
        return

    # Flatten for scanning
    flat = " ".join(cmd_list)

    # Check forbidden chars
    if any(char in flat for char in FORBIDDEN_CHARS):
        print("Command blocked due to forbidden characters.")
        return

    # Check dangerous flags
    for token in cmd_list:
        if token in DANGEROUS_FLAGS:
            print("Dangerous flag blocked.")
            return

    # Execute safely
    try:
        proc = subprocess.run(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = proc.stdout.strip() or proc.stderr.strip()
        return output

    except Exception as e:
        return (f"Execution error: {e}")

#-----------GEMINI INTEGRATION ---------------

genai.configure(api_key = API_KEY)


# We'll use this as our instruction manual for the AI
SYSTEM_PROMPT = """
You are NeoForge, a read-only terminal assistant for a developer.

Your job:
Convert the user’s natural language into a SAFE read-only shell command.

Your response format MUST ALWAYS be a JSON object:

{
  "reply": "<your friendly natural language reply>",
  "commands": ["<zero or more safe shell command tokens>"]
}

Rules:
1. NEVER generate destructive commands (rm, sudo, mv, cp, chmod, chown).
2. NEVER create, delete, or modify files.
3. NEVER change directories (cd).
4. ONLY use safe inspection commands like: ls, cat, grep, find, wc, head, tail.
5. If the user asks for something unsafe, respond with:
   {
     "reply": "Sorry! I can't fulfill this request.",
     "commands": []
   }

Examples:

User: "list all files with details"
Response:
{
  "reply": "Here you go!",
  "commands": ["ls", "-l"]
}

User: "find all python files"
Response:
{
  "reply": "Searching for Python files.",
  "commands": ["find", ".", "-name", "*.py"]
}

User: "delete test file"
Response:
{
  "reply": "Sorry! I can't fulfill this request.",
  "commands": []
}

Whenever you execute any command, you will be able to see the output. You are supposed to explain briefly if there is some kind of error, and help fixing it.
"""




"""
# Initialize the conversation history

model = genai.GenerativeModel("gemini-flash-latest", system_instruction = SYSTEM_PROMPT)

conversation_history = []

console.print("Welcome to NeoForge! Type 'exit' to end the conversation.\n")

history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

def ask_model(user_msg):
    history.append({"role": "user", "content": user_msg})
    response = model.generate_content(history)
    text = response.text

    # Strict JSON parsing
    try:
        data = json.loads(text)
    except:
        print("Model returned invalid JSON.")
        print(text)
        return {"reply": text, "commands": []}

    # Append model reply to history
    history.append({"role": "model", "content": text})
    return data
"""

model = genai.GenerativeModel(
    "gemini-flash-latest",
    system_instruction=SYSTEM_PROMPT
)

history = []

def ask_model(user_msg):
    if user_msg is None:
        return
    # Add user message
    if user_msg.strip() == "":
        return {"reply": "Empty input received.", "commands": []}

    history.append({
        "role": "user",
        "parts": [{"text": user_msg}]
    })

    # Ask model
    response = model.generate_content(history)
    text = response.text

    # JSON parsing
    try:
        data = json.loads(text)
    except Exception:
        print("Model returned invalid JSON:")
        print("Command:", )
        return {"reply": text, "commands": []}

    # Save model response to history
    history.append({
        "role": "model",
        "parts": [{"text": text}]
    })

    return data

while True:
    msg = input("You: ")
    out = ask_model(msg)

    print("[yellow]NeoForge:[/yellow]", out["reply"])
    if out["commands"]:
        print("[yellow]NeoForge:[/yellow]", out["commands"])
    term_op = safe_execute(out["commands"])
    if term_op and term_op.strip():
        print(f"\n[yellow]Command finished. Here's the captured output: {term_op}[/yellow]")
        out = ask_model(term_op.strip())
        print("[yellow]NeoForge:[/yellow]", out["reply"])
        term_op = None
