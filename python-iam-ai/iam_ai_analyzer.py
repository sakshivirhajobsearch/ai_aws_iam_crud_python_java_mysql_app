import openai

openai.api_key = "your-openai-api-key"

def analyze_policy(policy_document: str) -> str:
    prompt = f"""
You are a cloud IAM security expert. Analyze the following AWS IAM policy:

{policy_document}

Provide:
1. Summary
2. Risks
3. Suggestions
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful IAM security assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response['choices'][0]['message']['content']
