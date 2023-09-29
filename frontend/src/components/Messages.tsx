import { FC } from "react";
import type Message from "../types/Message";

interface Props {
    messages: Message[];
}

const Messages: FC<Props> = ({ messages }) => {
    // const messages: Message[] = [{ role: "user", content: "hello world" }];
    return (
        <ul>
            {messages.map((m, i) => (
                <li key={i}>
                    {m.role === "user" ? "you:" : "jerry:"} {m.content}
                </li>
            ))}
        </ul>
    );
};

export default Messages;
