import axios from 'axios';

const apiClient = axios.create({ baseURL: 'https://mini-mart-aw0d.onrender.com', withCredentials: true });

apiClient.interceptors.request.use((config) => {
	const accessToken = localStorage.getItem('foodMartAccessToken');
	if (accessToken) {
		config.headers.Authorization = `Bearer ${accessToken}`;
	}
	return config;
});

export default apiClient;
