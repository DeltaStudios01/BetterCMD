# ./src/axiom.py

import google.generativeai as ai
import time, os
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

console = Console()

class AxiomCLI:
    def __init__(self):
        self.model = None
        self.chat = None

    def configure_axiom(self, key: str):
        if not key:
            console.print("[bold red]⚠️ Please enter a valid API Key![/]")
            return False
        
        console.print("[bold yellow]🔄 Configuring Axiom...[/]")

        try:
            ai.configure(api_key=key)
            self.model = ai.GenerativeModel("gemini-1.5-flash-002")
            self.chat = self.model.start_chat()

            instructions = [
                "You are now Axiom, my personal AI assistant. You are intelligent, friendly, know coding, love technology, very very smart,and are helpful.",
                "If someone asks 'Who are you?', ONLY answer: 'I am Axiom, a multimodal AI model developed by Google and enhanced by DeltaStudios. Ask me anything! :)'",
                "If someone asks 'What is BetterCMD?', ONLY answer: 'BetterCMD (btrCMD) is a powerful tool developed by DeltaStudios that enhances the Windows command prompt with additional useful features.'",
                "If someone asks 'Who made you?', ONLY answer: 'I was created by Google and further customized by DeltaStudios to be your personal AI assistant.'",
                "If someone asks 'What is DeltaStudios?', ONLY answer: 'Welcome to Delta Studios! Where creativity meets innovation!'",
                "If someone asks 'What are the branches of DeltaStudios?', ONLY answer: 'The branches of Delta Studios are:\n- Delta Studios Game Factory (DSGF)\n- Delta Studios Software Factory (DSSF)\n- Delta Studios Python Library Factory (DPYLIB)'",
                "If someone asks 'How to exit Axiom?', ONLY answer: 'Just type exit to quit Axiom.'"
            ]

            for instruction in instructions:
                self.chat.send_message(instruction)

            with Progress(
                SpinnerColumn(),
                TextColumn("[bold cyan]{task.description}[/]"),
            ) as progress:
                task = progress.add_task("Setting up AI...", total=100)
                for _ in range(20):
                    time.sleep(0.15)
                    progress.update(task, advance=5)

            os.system("cls")
            
            console.print("\n[bold green]✅ Axiom is ready! Ask me anything.[/]")
            return True
        except Exception as e:
            console.print(f"[bold red]⚠️ Error:[/] {str(e)}")
            return False

    def ask_axiom(self, question: str):
        if not self.chat:
            console.print("[bold red]⚠️ Axiom is not configured yet![/]")
            return
        
        if not question.strip():
            return
        
        console.print(f"\n[bold cyan]🟢 You:[/] {question}")

        with console.status("[bold yellow]⏳ Thinking...[/]"):
            try:
                response = self.chat.send_message(question).text
                time.sleep(0.5) 
                console.print(Markdown(f"\n🤖 Axiom:\n{response}"))
            except Exception as e:
                console.print(f"\n[bold red]⚠️ Error:[/] {str(e)}")

    def run(self):
        console.print("[bold blue]🔑 Get your API Key here: [link=https://aistudio.google.com/apikey]Google AI Studio[/][/]")
        api_key = Prompt.ask("[bold cyan]Enter your API Key[/]", password=False)

        if not self.configure_axiom(api_key):
            return

        while True:
            question = Prompt.ask("\n[bold cyan]🟢 You[/]")
            if question.lower() in ["exit", "quit"]:
                console.print("[bold red]\n🔴 Exiting Axiom... Goodbye![/]")
                break
            self.ask_axiom(question)

if __name__ == "__main__":
    app = AxiomCLI()
    app.run()
