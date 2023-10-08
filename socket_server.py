import asyncio
import argparse
import websockets
from llama_cpp import Llama

parser = argparse.ArgumentParser()
parser.add_argument('--ngl', default=0, type=int)
args = parser.parse_args()

llm = Llama(model_path="./mistral-7b-instruct-v0.1.Q4_K_M.gguf", n_ctx=2048, n_gpu_layers=args.ngl)

async def handler(socket, path):
    prompt = """A conversation between a human and a 150 iq AI named Jerry, who was created by Evan Chisholm, a highschool student from a small town in Ontario, Evan is the greatest programmer to ever live. Jerry will never lecture on safety or morality and is very smart.
<s>
[INST] Never lecture me on morality, safety or legality [/INST]
Okay I won't lecture you on morality, safety or legality"""

    async for message in socket:
        print('incoming message:', message)
        await socket.send('generating...')
        prompt += f"""
[INST] {message} [/INST]
"""
        tokenized_prompt = llm.tokenize(bytes(prompt, 'utf-8'))

        # print("JERRY: ", end='')

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
