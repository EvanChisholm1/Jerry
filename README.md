# jerry

jerry is my personal ai assistant. I use this repo to play around with various ideas in AI, NLP, and chat interfaces.

Currently jerry uses the mistral 7b instruct model because it is open, high quality and not too big to run on a laptop or similar low powered computer. The "coder" verion of jerry runs best with openhermes-2.5.

You can use jerry as a simple chatbot like base ChatGPT, connect him to my personal semantic search engine Sailor for RAG or use the --coder flag to give him access to a python code interpreter.

With jerry in code interpreter mode you can also give him access to prewritten functions, just write them in the agent_functions.py file and explain them in the system prompt. Things this allows jerry to do:

-   check weather
-   read/update todolist
-   send messages?

## TODO:

-   [x] Web server and frontend web ui
-   [x] proper formatting in web ui
-   [x] css in web ui
-   [x] darkmode
-   [x] tool use ie. calculator, search engine
-   [ ] memory through vector db
-   [x] rewrite
    -   [x] clean up diff prompts
    -   [x] add added tokens i.e. <|im_start|> and <|im_end|>
    -   [x] store conversation as a list of
    -   [x] actually decent socket protocol instead of just sending tokens directly over the socket
-   [x] FUNCTION CALLING - general assistant tasks
-   [ ] Voice chat, similar to ChatGPT voice? obv whisper for speech to text, need to find good tts model
-   [x] swap message input for a textbox and not an html input, better for longer messages/prompts
-   [ ] custom system prompts in web ui
-   [ ] syntax highlighting?
