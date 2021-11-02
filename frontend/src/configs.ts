import { AxiosRequestConfig } from 'axios';

// Main
export const RECORDER_BIT_RATE = 128;
export const RECORD_SECONDS = 6;

// Axios
export const SERVER_ADDRESS =
  process.env.NODE_ENV === 'production' ? '' : 'http://localhost:4000';

export const AXIOS_CONFIGS: AxiosRequestConfig = Object.freeze({
  baseURL: SERVER_ADDRESS,
  timeout: 6000,
});
