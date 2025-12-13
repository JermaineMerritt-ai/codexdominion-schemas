import RAGStatus from './components/RAGStatus'
import DocumentIngestList from './components/DocumentIngestList'
import KnowledgeMap from './components/KnowledgeMap'

export default function KnowledgePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-serif text-ceremonial mb-2">
          📚 Knowledge Base & RAG
        </h1>
        <p className="text-proclamation">
          Document Ingestion, Vector Storage & Retrieval Augmented Generation
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <RAGStatus />
          <DocumentIngestList />
        </div>

        <div>
          <KnowledgeMap />
        </div>
      </div>
    </div>
  )
}
