import "dotenv/config";

export const getEmbeddingResponse = async (document_id, url) => {

const endpoint = `${process.env.FASTAPI_ENDPOINT}:${process.env.FASTAPI_PORT}/api/embed-url`;

console.log("Sending request to FastAPI at", endpoint);

  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ document_id, url }),
  });

  if (!response.ok)
    throw new Error(`FastAPI error: ${response.statusText}`);

  console.log("Embedding response received", response);

  return response.json(); 


}