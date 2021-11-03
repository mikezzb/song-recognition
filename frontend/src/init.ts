import axios from 'axios';
import { AXIOS_CONFIGS } from './configs';

axios.defaults.baseURL = AXIOS_CONFIGS.baseURL;
axios.defaults.timeout = AXIOS_CONFIGS.timeout;
