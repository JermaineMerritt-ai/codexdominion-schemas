'use client'

export default function DocumentIngestList() {
  const documents = [
    { id: '1', name: 'Advent Devotional 2025.pdf', status: 'indexed', size: '2.3 MB', date: 'Today' },
    { id: '2', name: 'Product Catalog.xlsx', status: 'processing', size: '1.1 MB', date: 'Today' },
    { id: '3', name: 'Customer FAQs.docx', status: 'indexed', size: '456 KB', date: 'Yesterday' },
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'indexed': return 'codex-badge-success'
      case 'processing': return 'codex-badge-warning'
      case 'error': return 'codex-badge-error'
      default: return 'codex-badge'
    }
  }

  return (
    <div className="codex-card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-serif text-codex-gold">
          Recent Documents
        </h2>
        <button className="codex-button">
          ➕ Ingest Documents
        </button>
      </div>

      <div className="space-y-3">
        {documents.map((doc) => (
          <div key={doc.id} className="codex-panel">
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">📄</span>
                <div>
                  <h3 className="font-semibold text-sm">{doc.name}</h3>
                  <p className="text-xs text-codex-parchment/60">{doc.size} • {doc.date}</p>
                </div>
              </div>
              <span className={getStatusColor(doc.status)}>
                {doc.status.toUpperCase()}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
