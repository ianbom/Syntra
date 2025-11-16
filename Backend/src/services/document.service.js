import prisma from "../config/prisma.js";
import { minioClient, bucketName } from "../config/minio.js";
import { v4 as uuidv4 } from "uuid";

export const createDocument = async (data, file) => {
  if (!file) {
    throw new Error("File is required");
  }

  const fileExtension = file.originalname.split(".").pop();
  const generatedFileName = `${uuidv4()}.${fileExtension}`;

  // Upload ke MinIO
  await minioClient.putObject(
    bucketName,
    generatedFileName,
    file.buffer,
    file.size,
    {
      "Content-Type": file.mimetype,
    }
  );

  // URL akses file (public)
  const fileUrl = `http://127.0.0.1:9000/${bucketName}/${generatedFileName}`;

  // Simpan metadata ke database Prisma
  const document = await prisma.documents.create({
    data: {
      title: data.title,
      creator: data.creator,
      keywords: data.keywords,
      description: data.description,
      publisher: data.publisher,
      contributor: data.contributor,
      date: data.date ? new Date(data.date) : null,
      type: data.type,
      format: data.format,
      identifier: data.identifier,
      source: data.source,
      language: data.language,
      relation: data.relation,
      coverage: data.coverage,
      rights: data.rights,
      doi: data.doi,
      abstract: data.abstract,
      citation_count: data.citation_count
        ? parseInt(data.citation_count)
        : null,
      sentiment: data.sentiment,
      uploaded_by: data.uploaded_by
        ? parseInt(data.uploaded_by)
        : null,

      file_path: generatedFileName, // disimpan sebagai nama file
      url: fileUrl,                // URL full dari MinIO

      is_private: data.is_private === "true",
      is_metadata_complete: false,
    },
  });

  return document;
};
