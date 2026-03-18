# =============================================
# GROKFORGE v2 - Real Grok-powered self-healing coder
# Built with Grok (xAI) - March 2026
# Safe version: API key loaded from .env file
# Uses cheapest/fast model for low cost
# =============================================

import os
from dotenv import load_dotenv
from openai import OpenAI

def strip_code_block(text):
    """Remove Markdown code fences and return pure Python code."""
    text = text.strip()
    if text.startswith("```python"):
        text = text.split("```python", 1)[1].split("```", 1)[0].strip()
    elif text.startswith("```"):
        parts = text.split("```", 2)
        if len(parts) > 2:
            text = parts[1].strip()
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0].strip()
    return text

# Load your secret key from .env (never hard-code it!)
load_dotenv()


api_key = os.getenv("XAI_API_KEY")
if not api_key:
    print("❌ No key loaded - check .env contents with 'cat .env'")
    exit()
else:
    print("✅ Key loaded successfully (length:", len(api_key), "chars)")

print("🚀 GrokForge v2 starting... Using REAL Grok API safely!\n")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1"
)

def ask_grok(prompt, model="grok-code-fast-1"):
    # Alternatives: "grok-4-1-fast-non-reasoning", "grok-beta", "grok-4"
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"API Error: {str(e)} (check key/credits at console.x.ai?)"

# ============== MAIN LOOP ==============
problem = input("What coding problem do you want Grok to solve?\n> ")

print("\nStep 1: Understanding the problem...")
understood = ask_grok(f"Summarize this coding problem clearly in one sentence: {problem}")
print(understood)

print("\nStep 2: Generating code...")
code_prompt = f"""Write clean, simple, well-commented Python code to exactly solve: {problem}
Return ONLY the function definition (no explanations, no markdown, no example usage, no if __name__ block). Make it runnable as a standalone function."""
raw_generated = ask_grok(code_prompt)
generated_code = strip_code_block(raw_generated)

print("\n📝 Generated code:\n" + "="*50)
print(generated_code)
print("="*50)

print("\nStep 3: Testing the code...")
try:
    local_vars = {}
    exec(generated_code, globals(), local_vars)
    print(" 🎉 Code executed successfully!")

    if "reverse" in problem.lower() and "string" in problem.lower():
        test_strings = ["hello", "Python", "a", "", "racecar"]
        print("   Quick reverse tests:")
        rev_func = local_vars.get('reverse_string')
        if rev_func:
            for s in test_strings:
                result = rev_func(s)
                expected = s[::-1]  # we use slicing only here for verification
                status = "✅ PASS" if result == expected else f"❌ FAIL (got {result})"
                print(f"     '{s}' → '{result}' {status}")
        else:
            print("   No 'reverse_string' function found")

    # Optional quick tests (expand this section for different problem types)
    if "palindrome" in problem.lower():
        tests = [
            ("A man a plan a canal Panama", True),
            ("race a car", False),
            ("Was it a car or a cat I saw?", True),
            ("hello", False),
            ("", True),
        ]
        print("   Quick palindrome tests:")
        is_pal = local_vars.get('is_palindrome')
        if is_pal:
            for s, expected in tests:
                result = is_pal(s)
                status = "✅ PASS" if result == expected else f"❌ FAIL (got {result})"
                print(f"     '{s}' → {result} {status}")
        else:
            print("   No 'is_palindrome' function found to test")

    # You can add more if-conditions for other common problem types later

except Exception as e:
    error_msg = str(e)
    print(f" ❌ Error during execution: {error_msg}")

    print("\nStep 4: Asking Grok to auto-fix...")
    fix_prompt = f"""The following code has this error: {error_msg}

Original code:
{generated_code}

Fix it completely. Return ONLY the corrected code (no explanations, no markdown)."""
    raw_fixed = ask_grok(fix_prompt)
    fixed_code = strip_code_block(raw_fixed)

    print("\n🔧 Fixed version:\n" + "="*50)
    print(fixed_code)
    print("="*50)

print("\n🎉 Done! Grok just coded + debugged using itself.")
print("This loop is a tiny demo of the self-improving coding Elon wants for xAI's rebuild.")
print("Total cost for this run: ~0.01–0.05 cents (super cheap model).")