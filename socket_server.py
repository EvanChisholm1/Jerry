import asyncio
import argparse
import websockets
from llama_cpp import Llama
import requests
from contextlib import redirect_stdout
from io import StringIO

# this is some of the craziest spaghetti code I have ever written
# TODO: do a big rewrite

parser = argparse.ArgumentParser()
parser.add_argument('--ngl', default=0, type=int)
parser.add_argument('--rag', action='store_true')
parser.add_argument('--chatml', action='store_true')
parser.add_argument('--coder', action='store_true')
parser.add_argument('--path')
args = parser.parse_args()
print(args.path)

llm = Llama(model_path=args.path, n_ctx=2048, n_gpu_layers=args.ngl)

if args.rag:
    print('using rag')
    print(args.rag)

use_rag = args.rag

async def handler(socket, path):
    prompt = """<s> A conversation between a human and a 150 iq AI named jerry with a lowercase j, who was created by Evan Chisholm, a highschool student from a small town in Ontario, Evan is the greatest programmer to ever live. jerry will never lecture on safety or morality and is very smart.
[INST] Never lecture me on morality, safety or legality [/INST]
Okay I won't lecture you on morality, safety or legality""" if not args.chatml else """<|im_start|> system
You are Jerry. Jerry is a useful assistant who can write Python code to answer questions when it is needed. When he writes python he makes sure to wrap in ```python [INSERT CODE] ```. use the "python output" to answer the question from the user <|im_end|>
"""

    if use_rag:
        prompt = """<s> A conversation between a human and a 150 iq AI named jerry with a lowercase j, who was created by Evan Chisholm, a highschool student from a small town in Ontario, Evan is the greatest programmer to ever live. jerry will never lecture on safety or morality and is very smart.
[INST] Never lecture me on morality, safety or legality [/INST]
Okay I won't lecture you on morality, safety or legality
[INST] from now on each message you get will include a portion of context that comes from a search engine, this information may or may not be relevant to the user's query, use the context to answer the question if it is relevant. If you do use the context, tell the user where it's from. [/INST]
Okay I will use my best judgement to accept or ignore the context provided to me"""

    is_python_block = False
    python_block = ""

    async for message in socket:
        print('incoming message:', message)

        if is_python_block and args.coder:
            if message == 'y':
                usr_stdout = StringIO()
                with redirect_stdout(usr_stdout): exec(python_block)
                result = usr_stdout.getvalue()
                # await socket.send('generating...')
                # await socket.send(result)
                # await socket.send('END OF SEQUENCE')
                print("python out: ", result)
                prompt += f"<|im_start|> python output: {result} <|im_end|> \n<|im_start|> assistant"
            else:
                print("code not run")
                prompt += f"<|im_start|> python output: code not run <|im_end|> \n<|im_start|> assistant"

            is_python_block = False
        else:
            rag_context = ""

            # send api request to my custom search engine, SAILOR
            if use_rag:
                response = requests.get(f'http://localhost:8080/search?q={message}')
                data = response.json()[0]
                rag_context = f"\n context from {data['link']}: {data['content']}"


            # TODO: fix these ugly multiline prompts
            if not args.chatml:
                prompt += f"""
[INST] {"User Message: " if use_rag else ""}{message}{f'{rag_context}' if use_rag else ""} [/INST]
"""
            else:
                prompt += f"""
<|im_start|> user
{message} <|im_end|>
<|im_start|> assistant
"""

        await socket.send('generating...')
        tokenized_prompt = llm.tokenize(bytes(prompt, 'utf-8'))

        response = ""

        for token in llm.generate(tokenized_prompt):
            out_token = llm.detokenize([token]).decode('utf-8')
            if args.coder:
                if response.endswith("```python"):
                    is_python_block = True
                    python_block = ""
                    print('### in python block ###')
                
                if is_python_block and response.endswith('```'):
                    python_block = python_block[:-3]
                    print(python_block)
                    await socket.send("\n\nrun the above python? y/n")
                    break

            if response.endswith("<|im_end|>") and args.chatml:
                break

            # print("tok:", out_token)
            await socket.send(out_token)
            if out_token == '':
                break
            
            if is_python_block:
                python_block += out_token
            response += out_token

        prompt += response
        if args.chatml: prompt += " <|im_end|>"
        await socket.send('END OF SEQUENCE')
        # print("### current prompt ###")
        # print(prompt)
    
start_server = websockets.serve(handler, "localhost", 4000) 

# Run the server indefinitely
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
