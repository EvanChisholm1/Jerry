from llama_cpp import Llama
from contextlib import redirect_stdout
from io import StringIO
import requests
import os
from dotenv import load_dotenv
import requests
import random
from agent_functions import *

get_todos()

# join function used so I don't have to do multiline strings that aren't properly indented
def join(segments):
    return "\n".join(segments)

def run_code(code_block):
    usr_stdout = StringIO()
    with redirect_stdout(usr_stdout): exec(code_block, globals(), locals())
    
    return usr_stdout.getvalue()

class Conversation:
    def __init__(self, llm, rag=False, chatml=False, coder=False, no_sys=False):
        self.llm = llm

        self.rag = rag
        self.coder = coder
        self.chatml = True if chatml or coder else False

        self.messages = []
        self.no_sys = no_sys
        self.sys_prompt = self.get_sys_prompt(rag=rag, coder=coder)

        self.code_block_available = False
        self.code_block = ""

    def get_sys_prompt(self, rag=False, coder=False):
        # default chatbot prompt, uses llama chat prompt format
        if self.no_sys: return ""
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
            # prompt = join([
            #     "<|im_start|> system",
            #     """You are jerry. jerry was created by Evan Chisholm, a highschol student. jerry is a useful assistant who can write Python code to answer questions when it is needed. When he writes python he makes sure to wrap in ```python [INSERT CODE] ```. use the "python output" to answer the question from the user. In your code you can also access the function get_weather(), which returns a string that describes the weather for today. You also have access to a function called send_message(string), which will send a text message to your creator evan. <|im_end|>""",
            # ])
            sys_prompt = join([
                """You are jerry. jerry was created by Evan Chisholm, a highschol student. jerry is a useful assistant who can write Python code to answer questions when it is needed.""",
                """When he writes python he makes sure to wrap in ```python [INSERT CODE] ```. use the "python output" to answer the question from the user.""", 
                """In your code you can also access the function get_todos(), which returns the user's todo list. You also have access to a function called add_todo(string), which will add a todo to the user's list. remove_todo(index) can be used to remove a todo at a zerobased index""",
            ])

            self.messages.append({
                'role': 'system',
                'content': sys_prompt
            })
            prompt = ""

            self.add_user_message('hello jerr!')
            self.add_assistant_message('Hi there! How can I help you today?')

        return prompt

    def encode_chatml_message(self, message):
        encoded = self.llm.tokenize(bytes(f"{message['role']}\n{message['content']}", 'utf-8'), add_bos=False)
        encoded = [32001] + encoded + [32000]
        return encoded

    def encode_llama_message(self, message):
        text = ""
        if message['role'] == 'user':
            text = f"[INST] {message['content']} [/INST]\n"
        else:
            text = f"{message['content']}\n"

        encoded = self.llm.tokenize(bytes(text, 'utf-8'), add_bos=False)[:-1]
        # print(encoded)
        return encoded
    
    def encode_message(self, message, chatml=False):
        # TODO: add rag message encoding with a user message: and context: field
        if chatml:
            return self.encode_chatml_message(message)
        else:
            return self.encode_llama_message(message)
        
    
    def add_user_message(self, message):
        # TODO: add rag context fetching and request
        query = message
        if self.rag:
            message = f"User Message: {message}"

        self.messages.append({
            'role': 'user',
            'content': message
        })

        if self.rag:
            self.fetch_rag_ctx(query)

        print(self.messages[-1])
    
    def add_assistant_message(self, message):
        self.messages.append({
            'role': 'assistant',
            'content': message
        })

    def tokenize_conversation(self, add_end_token=True):
        encoded_sys = self.llm.tokenize(bytes(self.sys_prompt, 'utf-8'))
        encoded_prompt = encoded_sys
        for message in self.messages:
            encoded_prompt += self.encode_message(message, self.chatml)
        
        return encoded_prompt if add_end_token else encoded_prompt[:-1]
    
    def generate_chat_completion(self, add_assistant_prefix=True):
        tokenized_prompt = self.tokenize_conversation(add_end_token=add_assistant_prefix)
        if add_assistant_prefix and self.chatml:
            tokenized_prompt += [32001] + self.llm.tokenize(bytes(" assistant\n", 'utf-8'), add_bos=False)

        # print('generating')
        # print(tokenized_prompt)
        is_in_python_block = False
        python_block = ""
        response = ""
        for token in self.llm.generate(tokenized_prompt):
            out_token = self.llm.detokenize([token]).decode('utf-8')
            print(f"'{out_token}'")

            if is_in_python_block and response.strip().endswith('```') and self.coder:
                is_in_python_block = False
                self.code_block = python_block.strip()[:-3]
                self.code_block_available = True
                break

            if out_token == '':
                break
            
            if is_in_python_block:
                python_block += out_token

            response += out_token
            yield out_token


            if response.strip().endswith("```python"):
                python_block = ""
                is_in_python_block = True
            
        
        # print('done generating')
        if add_assistant_prefix: self.add_assistant_message(response)
        else: self.messages[-1]['content'] += response
    
    def accept_code_block(self):
        print('running')

        result = run_code(self.code_block)
        print("output:", result)

        self.code_block = ""
        self.code_block_available = False
        self.messages[-1]['content'] += f"\n```output\n{result}\n```"

        return result
    
    def reject_code_block(self):
        self.code_block = ""
        self.code_block_available = False
        self.messages[-1]['content'] += f"\n```output\ncode not run\n```"
    
    def fetch_rag_ctx(self, query):
        response = requests.get(f'http://localhost:8080/search?q={query}')
        data = response.json()[0]
        print(data)
        self.messages[-1]['content'] += f"\n context from {data['link']}: {data['content']}"


        

if __name__ == "__main__":
    llm = Llama(model_path='./openhermes-2.5-mistral-7b.Q4_K_M.gguf', n_ctx=2048, n_gpu_layers=35)
    c = Conversation(llm, coder=True)

    while True:
        add_assistant_prefix = True
        if c.code_block_available:
            add_assistant_prefix = False
            confirmation = input('there is a code block available to run, run it? y/n ')
            if confirmation == 'y':
                c.accept_code_block()
            else:
                c.reject_code_block()
            # continue
        else:
            user_message = input('you: ')
            c.add_user_message(user_message)

        for tok in c.generate_chat_completion(add_assistant_prefix=add_assistant_prefix):
            print(tok, end='')
            
        print()
