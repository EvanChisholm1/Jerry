import { FC } from "react";
import type Message from "../types/Message";

interface Props {
    messages: Message[];
}

const Messages: FC<Props> = ({ messages }) => {
    return (
        <ul className="px-5">
            {messages.map((m, i) => (
                <li
                    className={`p-5 flex flex-col gap-3 ${
                        m.role === "user"
                            ? ""
                            : "bg-slate-100 dark:bg-slate-800"
                    }`}
                    key={i}
                >
                    <p className="font-bold">
                        {m.role === "user" ? "you:" : "jerry:"}
                    </p>
                    {m.content
                        .split("```")
                        .map((chunk, chunkI) =>
                            chunkI % 2 == 1 ? (
                                <pre key={`chunk: ${chunkI}`}>{chunk}</pre>
                            ) : (
                                chunk
                                    .split("\n")
                                    .map((t, i) => <p key={i}>{t}</p>)
                            )
                        )}
                </li>
            ))}
        </ul>
    );
};

export default Messages;
