import "dotenv/config";

export const getMetadataResponse = async (document_id, url) => {
  const endpoint = `${process.env.FASTAPI_ENDPOINT}:${process.env.FASTAPI_PORT}/api/extract-url`;

  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ document_id, url }),
  });

  if (!response.ok)
    throw new Error(`FastAPI error: ${response.statusText}`);

  return response.json();
};
