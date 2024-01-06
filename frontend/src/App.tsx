import { useEffect, useState } from "react";
import MessageInput from "./components/MessageInput";
import Messages from "./components/Messages";
import Message from "./types/Message";
import "./App.css";
import RunCodePrompt from "./components/RunCodePrompt";

const socket = new WebSocket("ws://localhost:4000");

interface ServerMessage {
    type: "incoming_token" | "start_message" | "end_message" | "code_available";
    token?: string;
}

interface ClientMessage {
    type: "message" | "accept_code_block" | "reject_code_block";
    content?: string;
}

// this component is getting a little wild I need to extract some of the socket handling to a ctx or smth
function App() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isGenerating, setIsGenerating] = useState(false);
    const [isCodeAvailable, setCodeAvailable] = useState(false);
    const [incomingMessage, setIncomingMessage] = useState("");

    useEffect(() => {
        console.log("bro");
        socket.addEventListener("open", () => {
            console.log("connected to socket");
        });
    }, []);

    useEffect(() => {
        if (isGenerating === false && incomingMessage !== "") {
            setMessages([
                ...messages,
                { content: incomingMessage, role: "jerry" },
            ]);
            setIncomingMessage("");
        }
    }, [isGenerating, incomingMessage, messages]);

    useEffect(() => {
        const pageHeight = document.body.scrollHeight;
        window.scroll({
            behavior: "smooth",
            left: 0,
            top: pageHeight,
        });
    }, [incomingMessage, isCodeAvailable]);

    useEffect(() => {
        function handleIncomingMessage(e: MessageEvent) {
            const message: ServerMessage = JSON.parse(e.data);

            if (message.type === "start_message") {
                setIsGenerating(true);
                setIncomingMessage("");
            } else if (message.type === "end_message") {
                console.log(incomingMessage);
                setIsGenerating(false);
            } else if (message.type === "code_available") {
                setCodeAvailable(true);
            } else {
                setIncomingMessage(`${incomingMessage}${message.token}`);
            }
        }

        socket.addEventListener("message", handleIncomingMessage);

        return () => {
            socket.removeEventListener("message", handleIncomingMessage);
        };
    }, [messages, incomingMessage, isGenerating]);

    const handleAccept = () => {
        const m: ClientMessage = { type: "accept_code_block" };
        socket.send(JSON.stringify(m));
        setCodeAvailable(false);
    };

    const handleReject = () => {
        const m: ClientMessage = { type: "reject_code_block" };
        socket.send(JSON.stringify(m));
        setCodeAvailable(false);
    };

    return (
        <div>
            <div className="flex justify-between">
                <div className="m-5 ml-10">
                    <h1 className="text-3xl font-bold">jerry</h1>
                    <p>
                        <small>An AI by Evan Chisholm</small>
                    </p>
                </div>

                {isGenerating && (
                    <div className="flex mr-12 text-center justify-center items-center gap-4">
                        <div className="rounded-full bg-red-500 w-5 h-5"></div>
                        <p>generating...</p>
                    </div>
                )}
            </div>
            <hr />
            <div className="flex justify-center">
                <div className="mb-24 w-full max-w-5xl">
                    <Messages
                        messages={
                            isGenerating
                                ? [
                                      ...messages,
                                      {
                                          role: "jerry",
                                          content: incomingMessage,
                                      },
                                  ]
                                : messages
                        }
                    />

                    {isCodeAvailable && (
                        <RunCodePrompt
                            onAccept={handleAccept}
                            onReject={handleReject}
                        />
                    )}
                </div>
            </div>
            <div className="fixed bottom-0 w-full flex justify-center">
                <div className="w-full max-w-5xl">
                    <MessageInput
                        handleMessage={(m) => {
                            if (isGenerating || isCodeAvailable || m === "")
                                return false;

                            const clientMessage: ClientMessage = {
                                type: "message",
                                content: m,
                            };
                            socket.send(JSON.stringify(clientMessage));

                            setMessages([
                                ...messages,
                                { role: "user", content: m },
                            ]);

                            return true;
                        }}
                    />
                </div>
            </div>
        </div>
    );
}

export default App;
