import axios, { AxiosError, AxiosResponse } from "axios";

export interface ServerData {
    path: string[];
}

export interface RequestBody {
    namespace: "ru";
    start: string;
    end: string;
}

const baseUrl = "http://localhost:45678/path_by_names";

export const getPaths = async (
    request: RequestBody,
): Promise<ServerData | string> => {
    try {
        const response: AxiosResponse<ServerData> = await axios.get(baseUrl, {
            params: {
                namespace: request.namespace,
                start: request.start,
                end: request.end,
            },
        });

        const { data } = response;

        return data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return (error as AxiosError).message;
        }

        return "An unexpected error occurred";
    }
};
