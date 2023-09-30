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

    function handleIncomingMessage(e: MessageEvent) {
        console.log(e);
        const m = e.data;
        if (m === "generating...") {
            setIsGenerating(true);
            setIncomingMessage("");
        } else if (m === "END OF SEQUENCE") {
            setMessages([
                ...messages,
                { content: incomingMessage, role: "jerry" },
            ]);
            setIsGenerating(false);
            setIncomingMessage("");
        } else {
            console.log(e.data);
            setIncomingMessage(`${incomingMessage}${m}`);
        }
    }

    useEffect(() => {
        console.log("bro");
        socket.addEventListener("open", () => {
            console.log("connected to socket");
        });
    }, []);

    useEffect(() => {
        socket.addEventListener("message", handleIncomingMessage);

        return () => {
            socket.removeEventListener("message", handleIncomingMessage);
        };
    }, [messages, incomingMessage, isGenerating]);

    return (
        <div>
            <h1>Jerry</h1>
            <p>
                <small>An AI by Evan Chisholm</small>
            </p>
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
            <MessageInput
                handleMessage={(m) => {
                    socket.send(m);
                    setMessages([...messages, { role: "user", content: m }]);
                }}
            />
        </div>
    );
}

export default App;
