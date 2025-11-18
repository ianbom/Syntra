// Mapping fallback FastAPI -> Prisma Enum
const docTypeFallback = {
  Text: "journal",
  Report: "report",
  Journal: "journal",
  Book: "book",
};

export const normalizeMetadata = (m) => {
  return {
    title: m.title || null,
    creator: m.creator || null,
    keywords: m.keywords || null,
    description: m.description || null,
    publisher: m.publisher || null,
    contributor: m.contributor || null,
    date: m.date ? new Date(m.date) : null,
    type: docTypeFallback[m.type] || "journal", // fallback aman
    format: m.format || null,
    identifier: m.identifier || null,
    source: m.source || null,
    language: m.language || null,
    relation: m.relation || null,
    coverage: m.coverage || null,
    rights: m.rights || null,
    doi: m.doi || null,
    abstract: m.abstract || null,
    citation_count: m.citation_count ? Number(m.citation_count) : null,
  };
};
