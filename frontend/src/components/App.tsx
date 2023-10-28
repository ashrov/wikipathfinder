import React, {useState} from 'react';
import '../styles/App.css';
import {InputFields} from "src/components/InputFields";
import {getPathsResponse, getPaths, requestBody} from "src/ts/getPaths";
import {Result} from "src/components/Result";

function App() {
    const [start, setStart] = useState('');
    const [end, setEnd] = useState('');
    const [error, setError] = useState('');
    const [paths, setPaths] = useState<string | getPathsResponse>()
    const [isLoading, setIsLoading] = useState<boolean>(false)

    const request: requestBody = {
        namespace: 'ru',
        start: start,
        end: end
    };

    function getPathsFromApi() {
        //set loading
        setIsLoading(true)

        //send request
        getPaths(request)
            .then((response) => {
                //response from API
                setPaths(response);
                console.log(typeof response)
            })
            .catch((error) => {
                //Error from API
                setError(error.message)
            });
    }

    return (
        <div className={"App"}>
            <InputFields
                start={start}
                end={end}
                setStart={setStart}
                setEnd={setEnd}
                onClickButton={getPathsFromApi}
            />
            <Result paths={paths}/>
        </div>
    );
}

export default App;
