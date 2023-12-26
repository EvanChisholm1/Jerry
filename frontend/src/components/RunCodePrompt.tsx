import { FC, useEffect } from "react";

interface Props {
    onAccept: () => void;
    onReject: () => void;
}

const RunCodePrompt: FC<Props> = ({ onAccept, onReject }) => {
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            console.log(e.key);

            if (e.key === "Enter") {
                onAccept();
            } else if (e.key === "Backspace") {
                onReject();
            }
        };

        window.addEventListener("keydown", handleKeyDown);

        return () => {
            window.removeEventListener("keydown", handleKeyDown);
        };
    }, [onAccept, onReject]);

    return (
        <div className="px-5">
            <div className="p-5">
                <h3 className="pb-4">Run The Above Python?</h3>
                <div className="flex items-stretch justify-evenly gap-3">
                    <button
                        onClick={onAccept}
                        className="bg-green-500 flex-1 p-5 rounded"
                    >
                        yes
                    </button>
                    <button
                        onClick={onReject}
                        className="bg-red-500 flex-1 rounded"
                    >
                        no
                    </button>
                </div>
            </div>
        </div>
    );
};

export default RunCodePrompt;
