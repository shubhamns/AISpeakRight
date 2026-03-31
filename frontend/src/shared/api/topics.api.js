import { request } from "./httpClient.js";

export function fetchTopics(levelId) {
  return request(`/topics?level_id=${encodeURIComponent(levelId)}`);
}

export function fetchTopicDetail(topicId) {
  return request(`/topics/${encodeURIComponent(topicId)}`);
}
