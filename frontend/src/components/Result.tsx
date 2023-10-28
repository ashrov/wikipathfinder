import React from "react";
import {getPathsResponse} from "src/ts/getPaths";

interface ResultProps {
    paths: string | getPathsResponse | undefined,
}

export function Result({paths}: ResultProps) {
    console.log("down")
    console.log(paths)

    return (
        <div className="links-container">
            <p className="result-header">Result:</p>
            <div className={"links"}>
                {}
            </div>
        </div>
    )
}