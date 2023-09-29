import { FormEvent, useState } from "react";
import { FC } from "react";

interface Props {
    handleMessage: (message: string) => any;
}

const MessageInput: FC<Props> = ({ handleMessage }) => {
    const [inputMessage, setInputMessage] = useState("");

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        console.log(inputMessage);
        handleMessage(inputMessage);
        setInputMessage("");
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
            />
            <button type="submit">send</button>
        </form>
    );
};

export default MessageInput;
