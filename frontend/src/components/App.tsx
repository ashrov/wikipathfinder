import React, { useState } from "react";
import "../styles/App.css";
import { InputFields } from "src/components/InputFields";
import { getPaths, RequestBody, ServerData } from "src/ts/getPaths";
import { Result } from "src/components/Result";

function App() {
    const [start, setStart] = useState("");
    const [end, setEnd] = useState("");
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [result, setResult] = useState<ServerData | string>("");

    function getPathsFromApi() {
        // Set loading
        setIsLoading(true);

        const request: RequestBody = {
            namespace: "ru",
            start,
            end,
        };

        // GET request
        getPaths(request)
            .then((response) => {
                setResult(response);
                setIsLoading(false);
            })
            .catch((error) => {
                setResult(error);
                setIsLoading(false);
            });
    }

    return (
        <div className="App">
            <span>
                {isLoading ? (
                    <div className="loader-line">Loading</div>
                ) : (
                    <div>Not loading</div>
                )}
            </span>
            <InputFields
                start={start}
                end={end}
                setStart={setStart}
                setEnd={setEnd}
                onClickButton={getPathsFromApi}
            />
            <Result paths={result} />
        </div>
    );
}

export default App;
