import prisma from "../config/prisma.js";
import { minioClient, bucketName } from "../config/minio.js";
import { v4 as uuidv4 } from "uuid";
import { getMetadataResponse } from "./metadata.service.js";
import { getEmbeddingResponse } from "./embedding.service.js";
import { normalizeMetadata } from "../utils/normalizeMetadata.js";
import "dotenv/config";

export const createDocument = async (data, file) => {
  if (!file) throw new Error("File is required");

  const generatedFileName = generateFileName(file.originalname);
  const fileUrl = await uploadToMinio(file, generatedFileName);

  const document = await saveInitialDocument(data, generatedFileName, fileUrl);

  const metadata = await getMetadataResponse(document.id, fileUrl);
  await saveExtractedMetadata(document.id, metadata.metadata);

  const embeddingResult = await getEmbeddingResponse(document.id, fileUrl);
  await saveDocumentChunks(document.id, embeddingResult.chunks);

  return document;
};


const generateFileName = (originalName) => {
  const ext = originalName.split(".").pop();
  return `${uuidv4()}.${ext}`;
};

const uploadToMinio = async (file, generatedFileName) => {
  await minioClient.putObject(
    bucketName,
    generatedFileName,
    file.buffer,
    file.size,
    { "Content-Type": file.mimetype }
  );

  return `${process.env.MINIO_PROTOCOL}://${process.env.MINIO_ENDPOINT}:${process.env.MINIO_PORT}/${bucketName}/${generatedFileName}`;
};

const saveInitialDocument = (data, generatedFileName, fileUrl) => {
  return prisma.documents.create({
    data: {
      title: data.title || null,
      creator: data.creator || null,
      keywords: data.keywords || null,
      description: data.description || null,
      publisher: data.publisher || null,
      contributor: data.contributor || null,
      date: data.date ? new Date(data.date) : null,
      type: data.type || "journal",
      format: data.format || null,
      identifier: data.identifier || null,
      source: data.source || null,
      language: data.language || null,
      relation: data.relation || null,
      coverage: data.coverage || null,
      rights: data.rights || null,
      doi: data.doi || null,
      abstract: data.abstract || null,
      citation_count: data.citation_count
        ? Number(data.citation_count)
        : null,
      sentiment: data.sentiment || "neutral",
      uploaded_by: data.uploaded_by ? Number(data.uploaded_by) : null,

      file_path: generatedFileName,
      url: fileUrl,
      is_private: data.is_private === "true",
      is_metadata_complete: false,
    },
  });
};

export const saveExtractedMetadata = async (document_id, rawMetadata) => {
  const metadata = normalizeMetadata(rawMetadata);
  return prisma.documents.update({
    where: { id: document_id },
    data: { ...metadata, is_metadata_complete: true },
  });
};

export const saveDocumentChunks = async (document_id, chunks) => {
  if (!Array.isArray(chunks) || chunks.length === 0)
    throw new Error("Chunk list is empty");

  for (const chunk of chunks) {
    await prisma.$queryRaw`
      INSERT INTO document_chunks 
      (document_id, chunk_index, content, token_count, embedding, created_at, updated_at)
      VALUES (
        ${document_id},
        ${chunk.chunk_index},
        ${chunk.content},
        ${chunk.token_count},
        ${chunk.embedding}::vector,
        NOW(),
        NOW()
      )
    `;
  }

  return true;
};



