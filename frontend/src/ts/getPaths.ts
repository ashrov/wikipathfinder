import axios from 'axios';

export interface path {
    link: string
}

export interface getPathsResponse {
    data: path[];
}

export interface requestBody {
    namespace: 'ru'
    start: string,
    end: string
}

export async function getPaths(request: requestBody) {
    try {
        const {data} = await axios.get<getPathsResponse>(
            'http://localhost:45678/path_by_names',
            {
                params: {
                    namespace: request.namespace,
                    start: request.start,
                    end: request.end
                },
                headers: {
                    Accept: 'application/json',
                },
            },
        );

        console.log(JSON.stringify(data, null, 4));

        return data;

    } catch (error) {
        if (axios.isAxiosError(error)) {
            return error.message;
        } else {
            return 'An unexpected error occurred';
        }
    }
}

