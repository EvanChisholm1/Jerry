import asyncio
import argparse
import websockets
from llama_cpp import Llama
from conversation import Conversation
import json

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
print (args.rag)

# TYPES OF POSSIBLE MESSAGES, SERVER -> CLIENT:
# Regular tokens
#   type: 'incoming_token', token: str
# start of message:
#   type: "start_message"
# end of message:
#   type: "end_message"
# code available:
#   type: "code_available"


def token_to_json(message):
    return json.dumps({
        'type': 'incoming_token',
        'token': message
    })

async def handler(socket, path):
    conv = Conversation(llm, args.rag, args.coder, args.coder)

    async for message in socket:
        print('incoming message:', message)
        await socket.send(json.dumps({'type': 'start_message'}))

        add_assistant_prefix = True

        # still not 100% happy with this but is infinitely better than what it was
        if conv.code_block_available and conv.coder:
            add_assistant_prefix = False
            if message == 'y':
                result = conv.accept_code_block()
                await socket.send(token_to_json(f'```output\n{result}\n```'))
            else:
                conv.reject_code_block()
                print("code not run")
                await socket.send(token_to_json(f"\noutput: code not run"))
        else:
            conv.add_user_message(message)


        for token in conv.generate_chat_completion(add_assistant_prefix=add_assistant_prefix):
            await socket.send(token_to_json(token))
        
        if conv.code_block_available:
            await socket.send(json.dumps({'type': 'code_available', token: 'Run the above python? y/n'}))

        await socket.send(json.dumps({'type': 'end_message'}))
    
start_server = websockets.serve(handler, "localhost", 4000) 

# Run the server indefinitely
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
