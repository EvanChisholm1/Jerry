from llama_cpp import Llama
from conversation import Conversation
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--ngl', default=0, type=int)
parser.add_argument('--rag', action='store_true')
parser.add_argument('--chatml', action='store_true')
parser.add_argument('--coder', action='store_true')
parser.add_argument('--path')
args = parser.parse_args()

llm = Llama(model_path=args.path, n_ctx=4096, n_gpu_layers=args.ngl, verbose=False)


c = Conversation(llm, coder=args.coder, rag=args.rag, chatml=True, no_sys=True )

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

    print('jerry: ', end='', flush=True)
    for tok in c.generate_chat_completion(add_assistant_prefix=add_assistant_prefix):
        print(tok, end='', flush=True)
        
    print()

