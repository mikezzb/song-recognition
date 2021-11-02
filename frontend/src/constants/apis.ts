import { AxiosRequestConfig } from 'axios';

export const RECOGNIZE: AxiosRequestConfig = {
  method: 'post',
  url: '/songs/recognize',
  headers: {
    'content-type': 'multipart/form-data',
  },
};
