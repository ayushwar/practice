import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
});

export async function fetchQuestions() {
  const response = await api.get("/api/questions");
  return response.data.questions;
}

export async function predictMood(answers) {
  const response = await api.post("/api/predict", { answers });
  return response.data;
}

export async function checkHealth() {
  const response = await api.get("/api/health");
  return response.data;
}

export default api;
