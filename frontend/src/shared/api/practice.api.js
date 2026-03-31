import { request } from "./httpClient.js";

export function correctSentence(sentence) {
  return request("/practice/correct", {
    method: "POST",
    body: JSON.stringify({ sentence }),
  });
}
