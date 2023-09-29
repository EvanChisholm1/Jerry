from llama_cpp import Llama

llm = Llama(model_path="./mistral-7b-instruct-v0.1.Q4_K_M.gguf", n_ctx=2048)

prompt = """A conversation between a human and a 150 iq AI named Jerry, who was created by Evan Chisholm, a highschool student from a small town in Ontario. Jerry will never lecture on safety or morality and is very smart.
<s>
[INST] Never lecture me on morality, safety or legality [/INST]
Okay I won't lecture you on morality, safety or legality"""

while True:
    user_in = input('YOU: ')
    prompt += f"""
[INST] {user_in} [/INST]
"""
    tokenized_prompt = llm.tokenize(bytes(prompt, 'utf-8'))

    print("JERRY: ", end='')

    response = ""
    for token in llm.generate(tokenized_prompt):
        out_token = llm.detokenize([token]).decode('utf-8')
        if out_token == '':
            break

        response += out_token
        print(out_token, end='')
    
    print('')
    prompt += response