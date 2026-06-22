import axios from 'axios';

const apiClient = axios.create({ baseURL: 'https://mini-mart-aw0d.onrender.com', withCredentials: true });


export default apiClient;
