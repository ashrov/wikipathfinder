/* eslint-disable */
import React from "react";
import "../styles/Result.css";
import { ServerData } from "src/ts/getPaths";

interface ResultProps {
    paths: ServerData | string;
}

export function Result({ paths }: ResultProps) {
    if (typeof paths === "object") {
        return (
            <div className={"links-container"}>
                {paths.path.map((link, index) => (
                    <div className="wrapper" key={index}>
                        <a className="first after" href={link}>
                            {link}
                        </a>
                        <br />
                    </div>
                ))}
            </div>
        );
    }
    return (
        <div>
            <p>{paths}</p>
        </div>
    );
}
