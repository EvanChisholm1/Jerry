import { FC } from "react";

interface Props {
    isGenerating?: boolean;
}

const Header: FC<Props> = ({ isGenerating }) => {
    return (
        <header className="flex justify-between">
            <div className="m-5 ml-10">
                <h1 className="text-3xl font-bold">jerry</h1>
                <p>
                    <small>An AI by Evan Chisholm</small>
                </p>
            </div>

            {isGenerating && (
                <div className="flex mr-12 text-center justify-center items-center gap-4">
                    <div className="rounded-full bg-red-500 w-5 h-5">
                        <div className="w-full h-full bg-inherit rounded-full animate-ping"></div>
                    </div>
                    <p>generating...</p>
                </div>
            )}
        </header>
    );
};

export default Header;
