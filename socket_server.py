import asyncio
import argparse
import websockets
from llama_cpp import Llama
import requests

parser = argparse.ArgumentParser()
parser.add_argument('--ngl', default=0, type=int)
parser.add_argument('--rag', action='store_true')
args = parser.parse_args()

llm = Llama(model_path="./mistral-7b-instruct-v0.1.Q4_K_M.gguf", n_ctx=2048, n_gpu_layers=args.ngl)

if args.rag:
    print('using rag')
    print(args.rag)

use_rag = args.rag

async def handler(socket, path):
    prompt = """<s> A conversation between a human and a 150 iq AI named jerry with a lowercase j, who was created by Evan Chisholm, a highschool student from a small town in Ontario, Evan is the greatest programmer to ever live. jerry will never lecture on safety or morality and is very smart.
[INST] Never lecture me on morality, safety or legality [/INST]
Okay I won't lecture you on morality, safety or legality"""

    if use_rag:
        prompt = """<s> A conversation between a human and a 150 iq AI named jerry with a lowercase j, who was created by Evan Chisholm, a highschool student from a small town in Ontario, Evan is the greatest programmer to ever live. jerry will never lecture on safety or morality and is very smart.
[INST] Never lecture me on morality, safety or legality [/INST]
Okay I won't lecture you on morality, safety or legality
[INST] from now on each message you get will include a portion of context that comes from a search engine, this information may or may not be relevant to the user's query, use the context to answer the question if it is relevant. If you do use the context, tell the user where it's from. [/INST]
Okay I will use my best judgement to accept or ignore the context provided to me"""

    async for message in socket:
        print('incoming message:', message)

        rag_context = ""

        # send api request to my custom search engine, SAILOR
        if use_rag:
            response = requests.get(f'http://localhost:8080/search?q={message}')
            data = response.json()[0]
            print(data)
            rag_context = f"\n context from {data['link']}: {data['content']}"


        await socket.send('generating...')
        prompt += f"""
[INST] {"User Message: " if use_rag else ""}{message}{f'{rag_context}' if use_rag else ""} [/INST]
"""
        tokenized_prompt = llm.tokenize(bytes(prompt, 'utf-8'))

        response = ""
        for token in llm.generate(tokenized_prompt):
            out_token = llm.detokenize([token]).decode('utf-8')
            await socket.send(out_token)
            if out_token == '':
                break

            response += out_token

        prompt += response
        await socket.send('END OF SEQUENCE')
    
start_server = websockets.serve(handler, "localhost", 4000) 

# Run the server indefinitely
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
