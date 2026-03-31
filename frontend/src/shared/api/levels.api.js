import { request } from "./httpClient.js";

export function fetchLevels() {
  return request("/levels");
}
