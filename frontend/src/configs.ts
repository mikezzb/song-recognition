import { AxiosRequestConfig } from 'axios';

// Main
export const RECORDER_BIT_RATE = 192;
export const RECORD_SECONDS = 10;

// Axios
export const SERVER_ADDRESS =
  process.env.NODE_ENV === 'production' ? '' : 'http://127.0.0.1:5000';

export const AXIOS_CONFIGS: AxiosRequestConfig = Object.freeze({
  baseURL: SERVER_ADDRESS,
  timeout: 6000,
});
