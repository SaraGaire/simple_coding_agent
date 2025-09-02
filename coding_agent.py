import os
import subprocess
import openai
from pathlib import Path

class PythonCodingAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key
        if api_key:
            openai.api_key = api_key
    
    def generate_code(self, prompt, language="python"):
        """Generate code based on natural language prompt"""
        system_prompt = f"""You are a coding assistant. Generate clean, 
        well-commented {language} code based on the user's request. 
        Only return the code, no explanations."""
        
        if self.api_key:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        else:
            # Fallback to template-based generation
            return self._template_based_generation(prompt, language)
    
    def _template_based_generation(self, prompt, language):
        """Simple template-based code generation"""
        templates = {
            "function": '''def {name}({params}):
    """{description}"""
    # TODO: Implement function logic
    pass''',
            "class": '''class {name}:
    """{description}"""
    def __init__(self):
        pass''',
            "script": '''#!/usr/bin/env python3
"""{description}"""

def main():
    # TODO: Implement main logic
    pass

if __name__ == "__main__":
    main()'''
        }
        
        # Simple keyword matching
        if "function" in prompt.lower():
            return templates["function"].format(
                name="new_function", 
                params="", 
                description="Generated function"
            )
        elif "class" in prompt.lower():
            return templates["class"].format(
                name="NewClass", 
                description="Generated class"
            )
        else:
            return templates["script"].format(description="Generated script")
    
    def save_code(self, code, filename):
        """Save generated code to file"""
        Path(filename).write_text(code)
        return f"Code saved to {filename}"
    
    def execute_code(self, filename):
        """Execute Python code file"""
        try:
            result = subprocess.run(
                ["python", filename], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"error": "Code execution timed out"}
    
    def analyze_code(self, filename):
        """Simple code analysis"""
        with open(filename, 'r') as f:
            code = f.read()
        
        analysis = {
            "lines": len(code.split('\n')),
            "functions": code.count('def '),
            "classes": code.count('class '),
            "imports": code.count('import ')
        }
        return analysis

# Usage example.
agent = PythonCodingAgent()
code = agent.generate_code("Create a function that calculates fibonacci numbers")
agent.save_code(code, "fibonacci.py")
result = agent.execute_code("fibonacci.py")
print(result)
