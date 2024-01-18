import { FormEvent, useState } from "react";
import { FC } from "react";

interface Props {
    handleMessage: (message: string) => boolean;
    isGenerating: boolean;
}

const MessageInput: FC<Props> = ({ handleMessage, isGenerating }) => {
    const [inputMessage, setInputMessage] = useState("");

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        const reset = handleMessage(inputMessage);
        if (reset) setInputMessage("");
    };

    return (
        <form className="flex w-full gap-5 p-5" onSubmit={handleSubmit}>
            <textarea
                className="grow ring-none outline-none border-none rounded ring-2 ring-gray-200 focus:ring-2 focus:ring-blue-500 p-5 dark:bg-slate-800 dark:ring-gray-600"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Your Message"
                autoFocus
            />
            <button
                className={`bg-blue-500 text-white rounded-md p-2 px-6 font-semibold ${
                    isGenerating ? "cursor-not-allowed" : ""
                }`}
                type="submit"
            >
                {isGenerating ? (
                    <div className="w-7 h-7 animate-spin bg-transparent border-4 rounded-full border-t-transparent"></div>
                ) : (
                    "send"
                )}
            </button>
        </form>
    );
};

export default MessageInput;
