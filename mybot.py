import re
import os
import json
from groq import Groq

client = Groq(api_key=os.environ.get(""))

MEMORY_FILE = "bot_memory.json"
COLOR_FILE = "color_config.json"

COLOR_MAP = {
    "green": "\033[92m",
    "yellow": "\033[93m",
    "cyan": "\033[96m",
    "red": "\033[91m",
    "magenta": "\033[95m",
    "white": "\033[0m"
}
COLOR_RESET = "\033[0m"
COLOR_SYSTEM = "\033[93m"

if os.path.exists(COLOR_FILE):
    with open(COLOR_FILE, "r") as f:
        config = json.load(f)
        COLOR_YOU = config.get("you", "\033[96m")
        COLOR_AI = config.get("ai", "\033[91m")
else:
    COLOR_YOU = "\033[96m",   
    COLOR_AI = "\033[91m"    

default_instructions = ( "Pretend ur a smart AI. (this is changeable)" 
)

if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, dict):
            permanent_facts = data.get("permanent_facts", [])
            chat_history = data.get("chat_history", [])
            conversation_summary = data.get("summary", "")
        else:
            permanent_facts = []
            chat_history = []
            conversation_summary = ""
else:
    permanent_facts = []
    chat_history = []
    conversation_summary = ""

def save_data():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "permanent_facts": permanent_facts,
            "chat_history": chat_history,
            "summary": conversation_summary
        }, f, ensure_ascii=False, indent=4)

print("Chat started with ADVANCED COMBINED MEMORY! Type your question and press Enter. (Type 'exit' to quit)\n")
print(f"{COLOR_SYSTEM}Available commands: /help, /clear, /stats, /color, /remember, /file{COLOR_RESET}\n")

while True:
    user_question = input(f"{COLOR_YOU}You:{COLOR_RESET} ")
    
    if user_question.lower() == 'exit':
        print("Goodbye!")
        break
        
    if user_question.startswith('/'):
        command = user_question.lower().strip()
        
        if command == '/help':
            print(f"{COLOR_SYSTEM}Commands list:\n/clear - Wipe bot memory\n/stats - Show total saved messages\n/color - Change UI colors\n/remember - Save a permanent fact\n/file - Read text from a local file\n/help - Show this info{COLOR_RESET}\n")
            continue
            
        elif command == '/clear':
            if os.path.exists(MEMORY_FILE):
                os.remove(MEMORY_FILE)
            permanent_facts = []
            chat_history = []
            conversation_summary = ""
            print(f"{COLOR_SYSTEM}Memory wiped successfully! Starting fresh :3{COLOR_RESET}\n")
            continue
            
        elif command == '/stats':
            print(f"{COLOR_SYSTEM}Current active chat history turns: {len(chat_history)}\nPermanent facts remembered: {len(permanent_facts)}{COLOR_RESET}\n")
            continue
            
        elif command == '/remember':
            fact = input(f"{COLOR_SYSTEM}What should I remember permanently?: {COLOR_RESET}").strip()
            if fact:
                permanent_facts.append(fact)
                save_data()
                print(f"{COLOR_SYSTEM}Fact saved to my permanent brain successfully! :D{COLOR_RESET}\n")
            else:
                print(f"{COLOR_SYSTEM}Nothing entered. No changes made.{COLOR_RESET}\n")
            continue

        elif command == '/file':
            file_path = input(f"{COLOR_SYSTEM}Enter full file path (or drag & drop file here): {COLOR_RESET}").strip().strip('"')
            instructions = input(f"{COLOR_SYSTEM}What should I do with this file? (e.g. explain, fix, edit): {COLOR_RESET}").strip()
            
            file_content = ""
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f_input:
                        file_content = f_input.read()
                except Exception as e:
                    print(f"{COLOR_SYSTEM}Error reading file: {e}{COLOR_RESET}\n")
                    continue
            
            file_prompt = (
                f"REQUEST ABOUT FILE: {instructions}\n"
                f"Target file path is '{file_path}'.\n"
                f"If the user requested changes, edits, or file creation, you MUST output the full updated file contents inside a single block enclosed by triple backticks (```). "
                f"Do not put anything else inside that code block except the clean file text. If it is a simple question, answer normally.\n\n"
                f"[Current File Content]:\n{file_content}"
            )
            print(f"{COLOR_SYSTEM}Sending file context to AI...{COLOR_RESET}\n")
            
            chat_history.append({"role": "user", "content": file_prompt})
            
            full_instructions = default_instructions
            if permanent_facts:
                full_instructions += " " + " ".join([f"Permanent fact about the user: {f}." for f in permanent_facts])
            if conversation_summary:
                full_instructions += f" General context of the conversation so far: {conversation_summary}"
                
            api_messages = [{"role": "system", "content": full_instructions}] + chat_history
            
            chat_completion = client.chat.completions.create(
                messages=api_messages,
                model="openai/gpt-oss-120b",
            )
            
            ai_response = chat_completion.choices[0].message.content
            chat_history.append({"role": "assistant", "content": ai_response})
            
            code_blocks = re.findall(r"```(?:\w+)?\n(.*?)\n```", ai_response, re.DOTALL)
            if code_blocks:
                new_content = code_blocks[0]
                try:
                    with open(file_path, "w", encoding="utf-8") as f_out:
                        f_out.write(new_content)
                    print(f"{COLOR_SYSTEM}[System]: File automatically updated and saved at: {file_path}{COLOR_RESET}\n")
                except Exception as e:
                    print(f"{COLOR_SYSTEM}[System Error]: Could not save file changes: {e}{COLOR_RESET}\n")
                    
            save_data()
            print(f"{COLOR_AI}AI: {ai_response}{COLOR_RESET}\n")
            continue
            
        elif command == '/color':
            print(f"{COLOR_SYSTEM}Available colors: green, yellow, cyan, red, magenta, white{COLOR_RESET}")
            new_you = input(f"{COLOR_SYSTEM}Choose color for YOU: {COLOR_RESET}").lower().strip()
            new_ai = input(f"{COLOR_SYSTEM}Choose color for AI: {COLOR_RESET}").lower().strip()
            
            if new_you in COLOR_MAP and new_ai in COLOR_MAP:
                COLOR_YOU = COLOR_MAP[new_you]
                COLOR_AI = COLOR_MAP[new_ai]
                with open(COLOR_FILE, "w") as f:
                    json.dump({"you": COLOR_YOU, "ai": COLOR_AI}, f)
                print(f"{COLOR_SYSTEM}Colors updated successfully!{COLOR_RESET}\n")
            else:
                print(f"{COLOR_SYSTEM}Invalid color selection. No changes made.{COLOR_RESET}\n")
            continue
            
        else:
            print(f"{COLOR_SYSTEM}Unknown command. Type /help to see available commands.{COLOR_RESET}\n")
            continue
    
    chat_history.append({"role": "user", "content": user_question})
    
    if len(chat_history) > 16:
        messages_to_summarize = [
            {"role": "system", "content": "You are a professional assistant. Summarize the following key points of the ongoing conversation very briefly in English. Focus on the main topics and decisions made so far. Keep it under 3-4 sentences."},
        ]
        if conversation_summary:
            messages_to_summarize.append({"role": "user", "content": f"Previous summary: {conversation_summary}"})
        
        messages_to_summarize.extend(chat_history[:-4])
        
        summary_completion = client.chat.completions.create(
            messages=messages_to_summarize,
            model="openai/gpt-oss-20b",
        )
        conversation_summary = summary_completion.choices[0].message.content
        chat_history = chat_history[-4:]
    
    full_instructions = default_instructions
    if permanent_facts:
        facts_text = " ".join([f"Permanent fact about the user: {f}." for f in permanent_facts])
        full_instructions += f" {facts_text}"
        
    if conversation_summary:
        full_instructions += f" General context of the conversation so far: {conversation_summary}"
        
    api_messages = [{"role": "system", "content": full_instructions}] + chat_history
        
    chat_completion = client.chat.completions.create(
        messages=api_messages,
        model="openai/gpt-oss-120b",
    )

    ai_response = chat_completion.choices[0].message.content
    chat_history.append({"role": "assistant", "content": ai_response})
    
    save_data()

    print(f"{COLOR_AI}AI: {ai_response}{COLOR_RESET}\n")
