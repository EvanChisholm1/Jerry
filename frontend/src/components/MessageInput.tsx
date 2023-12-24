import { FormEvent, useState } from "react";
import { FC } from "react";

interface Props {
    handleMessage: (message: string) => any;
}

const MessageInput: FC<Props> = ({ handleMessage }) => {
    const [inputMessage, setInputMessage] = useState("");

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        const reset = handleMessage(inputMessage);
        if (reset) setInputMessage("");
    };

    return (
        <form
            className="fixed bottom-0 flex w-full gap-5 p-5"
            onSubmit={handleSubmit}
        >
            <input
                className="grow ring-none outline-none border-none rounded ring-2 ring-gray-200 focus:ring-2 focus:ring-blue-500 p-5 dark:bg-slate-800 dark:ring-gray-600"
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Your Message"
            />
            <button
                className="bg-blue-500 text-white rounded-md p-2 px-6 font-semibold"
                type="submit"
            >
                send
            </button>
        </form>
    );
};

export default MessageInput;
