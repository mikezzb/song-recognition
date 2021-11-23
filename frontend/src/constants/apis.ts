import { AxiosRequestConfig } from 'axios';

export const RECOGNIZE: AxiosRequestConfig = {
  method: 'post',
  url: '/songs/recognize',
  headers: {
    'content-type': 'multipart/form-data',
  },
};

export const QUERY_BY_HUMMING: AxiosRequestConfig = {
  method: 'post',
  url: '/songs/query-by-humming',
  headers: {
    'content-type': 'multipart/form-data',
  },
};
