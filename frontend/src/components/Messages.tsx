import { FC } from "react";
import type Message from "../types/Message";

interface Props {
    messages: Message[];
}

const Messages: FC<Props> = ({ messages }) => {
    console.log(messages);
    return (
        <ul className="px-5">
            {messages.map((m, i) => (
                <li
                    className={`p-5 flex flex-col gap-3 rounded ${
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
                        .trim() // trim the string because for some reason open hermes is generating 2 new line characters
                        .split("```")
                        .map((chunk, chunkI) =>
                            chunkI % 2 == 1 ? (
                                <pre
                                    className="bg-gray-950 p-3 rounded text-white"
                                    key={`chunk: ${chunkI}`}
                                >
                                    {chunk.trim()}
                                </pre>
                            ) : (
                                chunk
                                    .split("\n")
                                    .map((t, i) =>
                                        t !== "" ? <p key={i}>{t}</p> : ""
                                    )
                            )
                        )}
                </li>
            ))}
        </ul>
    );
};

export default Messages;
