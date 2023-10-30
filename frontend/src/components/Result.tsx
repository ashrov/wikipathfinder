import React from 'react';
import {ServerData} from "src/ts/getPaths";

interface ResultProps {
    paths: ServerData | string;
}

export function Result({paths}: ResultProps) {
    if (typeof paths === 'object') {
        return (
            <ul>
                {paths.path.map((link, index) => (
                    <div className={"wrapper"} key={index}>
                        <a className="first after" href={link}>{link}</a><br/>
                    </div>
                ))}
            </ul>
        );
    } else {
        return (
            <div>
                <p>{paths}</p>
            </div>
        );
    }
}
