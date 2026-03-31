import { request } from "./httpClient.js";

export function fetchProgress() {
  return request("/progress");
}
