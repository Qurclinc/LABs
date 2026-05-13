export async function post(endpoint: string, data: any, signal?: AbortSignal) {
  const res = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    signal,
  });

  const json = await res.json();

  if (!res.ok) {
    throw new Error(json?.error || "Ошибка запроса");
  }

  return json;
}