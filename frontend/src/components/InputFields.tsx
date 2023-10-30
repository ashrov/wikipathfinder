import React, { ChangeEvent } from "react";

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
        <div className="form-row">
            <div className="form__group">
                <input
                    type="text"
                    className="form__field"
                    placeholder="Start"
                    name="start"
                    id="start"
                    value={start}
                    onChange={handleStartChange}
                    required
                />
                <label htmlFor="start" className="form__label">
                    Start
                </label>
            </div>

            <div className="form__group">
                <input
                    type="text"
                    className="form__field"
                    placeholder="End"
                    name="end"
                    id="end"
                    value={end}
                    onChange={handleEndChange}
                    required
                />
                <label htmlFor="end" className="form__label">
                    End
                </label>
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
