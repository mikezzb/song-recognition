import { AxiosRequestConfig } from 'axios';

export const SERVER_ADDRESS =
  process.env.NODE_ENV === 'production' ? '' : 'http://localhost:4000';

export const AXIOS_CONFIGS: AxiosRequestConfig = Object.freeze({
  baseURL: SERVER_ADDRESS,
  timeout: 6000,
});
