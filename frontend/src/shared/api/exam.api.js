import { request } from "./httpClient.js";

export function fetchExamQuestions(topicId, retrySetIndex) {
  let url = `/exam/questions?topic_id=${encodeURIComponent(topicId)}`;
  if (retrySetIndex != null) url += `&retry_set_index=${retrySetIndex}`;
  else url += `&_=${Date.now()}`;
  return request(url);
}

export function submitExam(topicId, setIndex, answers) {
  return request("/exam/submit", {
    method: "POST",
    body: JSON.stringify({
      topic_id: topicId,
      set_index: setIndex,
      answers,
    }),
  });
}
