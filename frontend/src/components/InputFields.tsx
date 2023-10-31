/* eslint-disable */
import React, { ChangeEvent } from "react";
import "../styles/InputFields.css";

interface InputProps {
    start: string;
    end: string;
    setStart: (value: string) => void;
    setEnd: (value: string) => void;
    onClickButton: () => void;
}

export function InputFields({
    start,
    end,
    setStart,
    setEnd,
    onClickButton,
}: InputProps) {
    const handleStartChange = (event: ChangeEvent<HTMLInputElement>) => {
        setStart(event.target.value);
    };

    const handleEndChange = (event: ChangeEvent<HTMLInputElement>) => {
        setEnd(event.target.value);
    };

    return (
        <div className={"input-area"}>
            <div className="form-row">
                <div className="input-container">
                    <input
                        type="text"
                        id="start"
                        required
                        value={start}
                        onChange={handleStartChange}
                        autoComplete="off"
                    />
                    <label htmlFor="input" className="label">
                        Start
                    </label>
                    <div className="underline" />
                </div>

                <div className="input-container">
                    <input
                        type="text"
                        id="end"
                        required
                        value={end}
                        onChange={handleEndChange}
                        autoComplete="off"
                    />
                    <label htmlFor="input" className="label">
                        End
                    </label>
                    <div className="underline" />
                </div>
            </div>
            <button className="button" onClick={onClickButton}>
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="-2 3 23 24"
                    stroke="currentColor"
                    className="icon"
                >
                    <circle cx="10" cy="12" r="7" />
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M15 17l5 5"
                    />
                </svg>

                <div className="text">Search</div>
            </button>
        </div>
    );
}
