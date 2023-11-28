from llama_cpp import Llama
from contextlib import redirect_stdout
from io import StringIO

# join function used so I don't have to do multiline strings that aren't properly indented
def join(segments):
    return "\n".join(segments)

class Conversation:
    def __init__(self, llm, rag=False, coder=False):
        self.llm = llm

        self.messages = []
        self.sys_prompt = self.get_sys_prompt(rag=rag, coder=coder)

        self.rag = rag
        self.coder = coder
        self.chatml = coder

        self.code_block_available = False
        self.code_block = ""

    def get_sys_prompt(self, rag=False, coder=False):
        # default chatbot prompt, uses llama chat prompt format
        prompt = join([
            "<s> A conversation between a human and a 150 iq AI named jerry with a lowercase j, who was created by Evan Chisholm, a highschool student from a small town in Ontario, Evan is the greatest programmer to ever live. jerry will never lecture on safety or morality and is very smart.",
            "[INST] Never lecture me on morality, safety or legality [/INST]",
            "Okay I won't lecture you on morality, safety or legality"
        ])

        if rag:
            prompt = join([
                "<s> A conversation between a human and a 150 iq AI named jerry with a lowercase j, who was created by Evan Chisholm, a highschool student from a small town in Ontario, Evan is the greatest programmer to ever live. jerry will never lecture on safety or morality and is very smart.",
                "[INST] Never lecture me on morality, safety or legality [/INST]",
                "Okay I won't lecture you on morality, safety or legality",
                "[INST] from now on each message you get will include a portion of context that comes from a search engine, this information may or may not be relevant to the user's query, use the context to answer the question if it is relevant. If you do use the context, tell the user where it's from. [/INST]",
                "Okay I will use my best judgement to accept or ignore the context provided to me"
            ])
        
        if coder:
            prompt = join([
                "<|im_start|> system",
                """You are Jerry. Jerry is a useful assistant who can write Python code to answer questions when it is needed. When he writes python he makes sure to wrap in ```python [INSERT CODE] ```. use the "python output" to answer the question from the user <|im_end|>""",
                # "<|im_start|> user",
                # "hello jerry! <|im_end|>",
                # "<|im_start|> assistant",
                # "Hello, how can I assist you today? <|im_end|>"
            ])

            self.add_user_message('hello jerr!')
            self.add_assistant_message('Hi there! How can I help you today?')


        return prompt

    def encode_chatml_message(self, message):
        encoded = self.llm.tokenize(bytes(f"{message['role']}\n{message['content']}", 'utf-8'), add_bos=False)
        encoded = [32001] + encoded + [32000]
        return encoded

    def encode_llama_message(self, message):
        text = message['content']
        if message['role'] == 'user':
            text = f"[INST] {message['content']} [/INST]"

        encoded = self.llm.tokenize(bytes(text, 'utf-8'), add_bos=False)
        return encoded
    
    def encode_message(self, message, chatml=False):
        if chatml:
            return self.encode_chatml_message(message)
        else:
            return self.encode_llama_message(message)
        
    
    def add_user_message(self, message):
        self.messages.append({
            'role': 'user',
            'content': message
        })
    
    def add_assistant_message(self, message):
        self.messages.append({
            'role': 'assistant',
            'content': message
        })

    
    def tokenize_conversation(self):
        encoded_sys = self.llm.tokenize(bytes(self.sys_prompt, 'utf-8'))
        encoded_prompt = encoded_sys
        for message in self.messages:
            encoded_prompt += self.encode_message(message, self.chatml)
        
        return encoded_prompt
    
    def generate_chat_completion(self):
        tokenized_prompt = self.tokenize_conversation()
        tokenized_prompt += [32001] + self.llm.tokenize(bytes(" assistant", 'utf-8'), add_bos=False)

        is_in_python_block = False
        python_block = ""
        response = ""
        for token in self.llm.generate(tokenized_prompt):
            # print(token)

            out_token = self.llm.detokenize([token]).decode('utf-8')

            if is_in_python_block and response.endswith('```') and self.coder:
                is_in_python_block = False
                self.code_block = python_block[:-3]
                self.code_block_available = True
                break

            if out_token == '':
                break
            
            if is_in_python_block:
                python_block += out_token

            response += out_token
            yield out_token


            if response.endswith("```python"):
                python_block = ""
                is_in_python_block = True
            
        
        self.add_assistant_message(response)
    
    def run_code_block(self):
        print('running')

        usr_stdout = StringIO()
        with redirect_stdout(usr_stdout): exec(self.code_block, {}, {})
        result = usr_stdout.getvalue()

        print("output:", result)

        self.code_block = ""
        self.code_block_available = False
        self.messages[-1]['content'] += "\n```output\n{result}\n```"

        return result
        
llm = Llama(model_path='./openhermes-2.5-mistral-7b.Q4_K_M.gguf', n_ctx=2048, n_gpu_layers=35)
c = Conversation(llm, coder=True)

while True:
    if c.code_block_available:
        confirmation = input('there is a code block available to run, run it? y/n ')
        if confirmation == 'y':
            c.run_code_block()
        continue

    user_message = input('you: ')
    c.add_user_message(user_message)
    for tok in c.generate_chat_completion():
        print(tok, end='')
        
    print()
