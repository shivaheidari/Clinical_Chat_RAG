rag_azure_project/
│
├─ configs/
│   └─ azure_keys.json           # Connection strings, secret keys (never commit)
│   └─ index_schema.json         # Index field definitions
│   └─ skillset_config.json      # Skillset definition: chunking, embedding
│
├─ data/
│   └─ raw/                      # Backup local copies of notes (optional)
│
├─ scripts/
│   ├─ setup_ai_search.py        # Create service, index, skillset, indexer (SDK code)
│   ├─ check_index_status.py     # Validate index after indexing
│   ├─ query_api.py              # Build REST API for search & answer generation
│   ├─ run_indexer.py            # Trigger/monitor Azure indexer
│
└─ README.md                     # Project instructions/documentation
