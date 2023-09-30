import { FC } from "react";
import type Message from "../types/Message";

interface Props {
    messages: Message[];
}

const Messages: FC<Props> = ({ messages }) => {
    return (
        <ul>
            {messages.map((m, i) => (
                <li key={i}>
                    {m.role === "user" ? "you:" : "jerry:"}{" "}
                    {m.content.split("\n").map((t, j) => (
                        <p key={j}>{t}</p>
                    ))}
                </li>
            ))}
        </ul>
    );
};

export default Messages;
