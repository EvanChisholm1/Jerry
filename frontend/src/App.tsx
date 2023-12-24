import { useEffect, useState } from "react";
import MessageInput from "./components/MessageInput";
import Messages from "./components/Messages";
import Message from "./types/Message";
import "./App.css";

const socket = new WebSocket("ws://localhost:4000");

function App() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isGenerating, setIsGenerating] = useState(false);
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
        function handleIncomingMessage(e: MessageEvent) {
            console.log(e);
            const m = e.data;
            if (m === "generating...") {
                setIsGenerating(true);
                setIncomingMessage("");
            } else if (m === "END OF SEQUENCE") {
                console.log(incomingMessage);
                setIsGenerating(false);
            } else {
                console.log(e.data);
                setIncomingMessage(`${incomingMessage}${m}`);
            }
        }
        socket.addEventListener("message", handleIncomingMessage);

        return () => {
            socket.removeEventListener("message", handleIncomingMessage);
        };
    }, [messages, incomingMessage, isGenerating]);

    return (
        <div>
            <div className="m-5 ml-10">
                <h1 className="text-3xl font-bold">jerry</h1>
                <p>
                    <small>An AI by Evan Chisholm</small>
                </p>
            </div>
            <hr />
            <div className="mb-24">
                <Messages
                    messages={
                        isGenerating
                            ? [
                                  ...messages,
                                  { role: "jerry", content: incomingMessage },
                              ]
                            : messages
                    }
                />
            </div>
            <MessageInput
                handleMessage={(m) => {
                    if (isGenerating) return false;
                    socket.send(m);
                    setMessages([...messages, { role: "user", content: m }]);
                    return true;
                }}
            />
        </div>
    );
}

export default App;
