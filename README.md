# jerry

jerry is my personal ai assistant. I use this repo to play around with various ideas in AI, NLP, and chat interfaces.

Currently jerry uses the mistral 7b instruct model because it is open, high quality and not too big to run on a laptop or similar low powered computer. The "coder" verion of jerry runs best with openhermes-2.5.

Currently you can use jerry as a simple chatbot like base ChatGPT, connect him to my personal semantic search engine Sailor for RAG or use the --coder flag to give him access to a python code interpreter.

## TODO:

-   [x] Web server and frontend web ui
-   [x] proper formatting in web ui
-   [x] css in web ui
-   [x] darkmode
-   [x] tool use ie. calculator, search engine
-   [x] memory through vector db
-   [ ] rewrite
    -   [x] clean up diff prompts
    -   [x] add added tokens i.e. <|im_start|> and <|im_end|>
    -   [ ] syntax highlighting?
    -   [x] store conversation as a list of
-   [ ] FUNCTION CALLING - general assistant tasks
