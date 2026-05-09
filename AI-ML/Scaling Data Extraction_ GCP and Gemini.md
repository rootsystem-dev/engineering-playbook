In this guide, you will learn how to build a production-grade document processing system that extracts structured data from thousands of financial documents and stores them in a Neo4j graph database for intelligent querying.

Before we dive in, let's understand what we're building and why.

## **What is Document Intelligence?**

Document Intelligence is the process of automatically extracting structured information from unstructured documents (PDFs, images, scans) and organizing that data into a queryable format. This enables you to ask questions like "Show me all bank statements for Company X" or "Find documents where Person Y appears across multiple accounts."

## **Why Use a Graph Database?**

While traditional databases excel at storing flat data, financial documents contain complex relationships: companies own accounts, people appear in multiple documents, emails connect to transactions. A graph database like Neo4j naturally represents these connections, making relationship queries orders of magnitude faster than SQL joins.

## **System Architecture**

This system consists of three main layers

```textproto
┌──────────────────────────────────────────────────────┐
│                   UPLOAD LAYER                       │
│  Google Cloud Storage (GCS) - Raw PDFs/Images       │
└────────────────┬─────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────┐
│                EXTRACTION LAYER                       │
│  Gemini 2.5 Flash - AI-powered data extraction      │
│  • Structured data (companies, people, accounts)     │
│  • Full text preservation (for future embeddings)    │
└────────────────┬─────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────┐
│                PROCESSING LAYER                       │
│  Cloud Run Jobs - Parallel batch processing         │
│  • Rate limiting & retry logic                       │
│  • Progress tracking & error handling                │
└────────────────┬─────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────┐
│                  STORAGE LAYER                        │
│  Neo4j Graph Database - Relationship intelligence    │
│  • Document metadata + full text                     │
│  • Entity nodes (Company, Person, Account, Email)    │
│  • Relationship edges (BELONGS_TO, MENTIONS, etc.)   │
└──────────────────────────────────────────────────────┘
```

Processing flow:

1. Documents uploaded to GCS
2. Gemini extracts structured data \+ full text
3. Cloud Run orchestrates parallel processing
4. Neo4j stores graph relationships
5. Query documents by relationships

## **Project Stack**

This project uses:

- Upload: Google Cloud Storage (GCS)
- Extraction: Gemini 2.5 Flash API
- Processing: Cloud Run Jobs (serverless batch)
- Storage: Neo4j Aura (managed graph database)
- Orchestration: Python 3.11
- Monitoring: Google Cloud Logging

## **Prerequisites**

Before starting, ensure you have:

1. Google Cloud Project with billing enabled
2. Gemini API key from
3. [Google AI Studio](https://aistudio.google.com/apikey)
4. Neo4j Aura instance (8GB RAM minimum)
5. GCS bucket with 40K documents uploaded
6. gcloud CLI installed and configured

## **Part 1: Setup Neo4j Database**

## **Create Neo4j Instance**

1. Go to
2. [Neo4j Aura](https://console.neo4j.io/)
3. Click New Instance
4. Select:
   - Memory: 8GB RAM
   - Storage: 16GB
   - Region: Same as GCS (e.g., us-central1)
5. Save your credentials (you'll need the URI, username, and password)

Cost: \~$538/month with 8-hour daily auto-pause

## **Configure Database Schema**

Open Neo4j Browser and run these commands:

## **Create Constraints (Required)**

```sql
-- Ensure document uniqueness
CREATE CONSTRAINT document_id_unique IF NOT EXISTS
FOR (d:Document) REQUIRE d.id IS UNIQUE;

-- Ensure company name uniqueness
CREATE CONSTRAINT company_name_unique IF NOT EXISTS
FOR (c:Company) REQUIRE c.name IS UNIQUE;

-- Ensure person name uniqueness
CREATE CONSTRAINT person_name_unique IF NOT EXISTS
FOR (p:Person) REQUIRE p.name IS UNIQUE;

-- Ensure account number uniqueness
CREATE CONSTRAINT account_number_unique IF NOT EXISTS
FOR (a:Account) REQUIRE a.number IS UNIQUE;

-- Ensure email address uniqueness
CREATE CONSTRAINT email_address_unique IF NOT EXISTS
FOR (e:Email) REQUIRE e.address IS UNIQUE;

-- Ensure user ID uniqueness
CREATE CONSTRAINT user_id_unique IF NOT EXISTS
FOR (u:User) REQUIRE u.id IS UNIQUE;
```

## **Create Performance Indexes**

```sql
-- Document lookup indexes
CREATE INDEX document_status IF NOT EXISTS
FOR (d:Document) ON (d.status);

CREATE INDEX document_type IF NOT EXISTS
FOR (d:Document) ON (d.docType);

CREATE INDEX document_created IF NOT EXISTS
FOR (d:Document) ON (d.createdAt);

-- Date-based queries (epoch format for range queries)
CREATE INDEX document_statement_date_epoch IF NOT EXISTS
FOR (d:Document) ON (d.statementDateEpoch);

-- Composite index for common query patterns
CREATE INDEX document_type_status_date IF NOT EXISTS
FOR (d:Document) ON (d.docType, d.status, d.statementDateEpoch);

-- Balance queries
CREATE INDEX document_balance IF NOT EXISTS
FOR (d:Document) ON (d.balance);

CREATE INDEX account_balance IF NOT EXISTS
FOR (a:Account) ON (a.balance);

-- User lookup
CREATE INDEX user_email IF NOT EXISTS
FOR (u:User) ON (u.email);
```

Verify indexes:

```sql
CALL db.indexes();
```

You should see all constraints and indexes listed.

## **Part 2: Build the Extraction Layer**

The extraction layer uses Gemini to extract structured data from documents.

## **Install Dependencies**

Create a new directory and install required packages:

```
mkdir doc-intelligence && cd doc-intelligence
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install google-generativeai google-cloud-storage google-cloud-logging google-cloud-secret-manager neo4j pillow python-dotenv
```

## **Create Extraction Module**

Create src/extraction/document_extractor.py:

```python
"""
Document extraction using Gemini 2.5 Flash
Single responsibility: Extract data from documents
"""

from google import genai
import json
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class DocumentExtractor:
    """Extract structured data and full text from documents"""

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-2.5-flash'

    def extract_document(self, gcs_uri: str) -> Tuple[Dict, str]:
        """
        Extract both structured data and full text

        Args:
            gcs_uri: GCS path to document (gs://bucket/path/file.pdf)

        Returns:
            (structured_data_dict, full_text_string)
        """
        file = None
        try:
            # Upload file to Gemini
            file = genai.upload_file(gcs_uri)
            logger.debug(f"Uploaded to Gemini: {file.uri}")

            # Get extraction schema
            schema = self._get_schema()

            # Configure model
            model = genai.GenerativeModel(
                self.model_name,
                generation_config={
                    "response_mime_type": "application/json",
                    "response_schema": schema,
                    "temperature": 0  # Deterministic extraction
                }
            )

            # Extract structured data
            structured_response = model.generate_content([
                self._get_structured_prompt(),
                file
            ])
            structured_data = json.loads(structured_response.text)

            # Extract full text
            text_response = model.generate_content([
                self._get_text_prompt(),
                file
            ])
            full_text = text_response.text

            return structured_data, full_text

        finally:
            # CRITICAL: Delete file to avoid quota exhaustion
            if file:
                try:
                    file.delete()
                    logger.debug(f"Deleted Gemini file: {file.uri}")
                except Exception as e:
                    logger.warning(f"Failed to delete file: {e}")

    def _get_schema(self) -> Dict:
        """JSON schema for structured extraction"""
        return {
            "type": "object",
            "properties": {
                "doc_type": {
                    "type": "string",
                    "enum": ["email", "statement", "invoice", "report",
                             "contract", "letter", "form", "unknown"],
                    "description": "Document category"
                },
                "account_numbers": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "All account numbers found"
                },
                "company_names": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "All company names mentioned"
                },
                "person_names": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "All person names mentioned"
                },
                "email_addresses": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "All email addresses found"
                },
                "statement_date": {
                    "type": "string",
                    "description": "ISO 8601 date (2025-11-10)"
                },
                "page_count": {
                    "type": "integer",
                    "description": "Total pages"
                },
                "balance": {
                    "type": "number",
                    "description": "Account balance if present"
                }
            },
            "required": ["doc_type"]
        }

    def _get_structured_prompt(self) -> str:
        return """Extract ALL structured information from this document:

        - doc_type: Classify as email, statement, invoice, report, contract, letter, form, or unknown
        - account_numbers: ALL account numbers (in text, tables, headers, footers)
        - company_names: ALL company/organization/bank names
        - person_names: ALL person names mentioned
        - email_addresses: ALL email addresses
        - statement_date: Date in ISO 8601 format if this is a statement
        - page_count: Total number of pages
        - balance: Account balance if visible

        Be thorough. Extract EVERYTHING."""

    def _get_text_prompt(self) -> str:
        return """Extract ALL text from this document.

        Include:
        - Headers and footers
        - Body text
        - Tables
        - Everything visible

        Output plain text only."""
```

Key features:

- Extracts structured data (companies, people, accounts)
- Preserves full text for future embedding
- Automatically deletes Gemini files to avoid quota exhaustion
- Uses deterministic extraction (temperature=0)

---

## **Part 3: Build the Storage Layer**

The storage layer handles Neo4j connections and transactions.

## **Create Neo4j Client**

Create src/database/neo4j_client.py:

```py
"""
Neo4j client for graph database operations
Handles connections, transactions, and queries
"""

from neo4j import GraphDatabase
from google.cloud import secretmanager
import os
import json
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Neo4jClient:
    """Manages Neo4j connections and document operations"""

    def __init__(self):
        """Initialize with optimized connection pool"""
        self.uri = self._get_secret("neo4j-uri")
        self.username = self._get_secret("neo4j-username")
        self.password = self._get_secret("neo4j-password")
        self.database = os.getenv("NEO4J_DATABASE", "neo4j")

        # Connection pool optimized for 8GB instance
        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password),
            max_connection_pool_size=5,  # Critical for 8GB
            connection_acquisition_timeout=30000,
            max_transaction_retry_time=15000,
            encrypted=True
        )

        logger.info("Neo4j driver initialized")

    def _get_secret(self, secret_name: str) -> str:
        """Fetch secret from GCP Secret Manager"""
        try:
            client = secretmanager.SecretManagerServiceClient()
            project_id = os.getenv("GCP_PROJECT_ID")
            name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
            response = client.access_secret_version(name=name)
            return response.payload.data.decode('UTF-8')
        except Exception as e:
            logger.error(f"Failed to fetch secret: {e}")
            return os.getenv(secret_name.upper().replace('-', '_'))

    def verify_connectivity(self) -> bool:
        """Test Neo4j connection"""
        try:
            with self.driver.session(database=self.database) as session:
                result = session.run("RETURN 1 as test")
                return result.single()["test"] == 1
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False

    def create_document_with_relationships(
        self,
        doc_id: str,
        extracted_data: Dict,
        full_text: str,
        file_url: str,
        user_id: str = "system"
    ) -> Dict:
        """
        Create document and all relationships atomically

        Args:
            doc_id: Unique document identifier
            extracted_data: Structured data from extraction
            full_text: Complete extracted text
            file_url: GCS URI
            user_id: User who uploaded document

        Returns:
            Creation result
        """
        with self.driver.session(database=self.database) as session:
            return session.execute_write(
                self._create_document_tx,
                doc_id,
                extracted_data,
                full_text,
                file_url,
                user_id
            )

    @staticmethod
    def _create_document_tx(tx, doc_id: str, data: Dict, full_text: str,
                           file_url: str, user_id: str):
        """Atomic transaction for document creation"""

        # Convert date to epoch
        statement_epoch = None
        if data.get('statement_date'):
            try:
                dt = datetime.fromisoformat(data['statement_date'])
                statement_epoch = int(dt.timestamp())
            except:
                pass

        # 1. Create user
        tx.run("""
            MERGE (u:User {id: $userId})
            ON CREATE SET u.createdAt = datetime()
        """, userId=user_id)

        # 2. Create document
        result = tx.run("""
            MATCH (u:User {id: $userId})
            CREATE (d:Document {
                id: $docId,
                name: $name,
                docType: $docType,
                status: 'Succeeded',
                extractedFields: $extractedFields,
                fullText: $fullText,
                fullTextLength: $fullTextLength,
                fileUrl: $fileUrl,
                pageCount: $pageCount,
                statementDate: $statementDate,
                statementDateEpoch: $statementDateEpoch,
                balance: $balance,
                createdAt: datetime(),
                updatedAt: datetime()
            })
            CREATE (d)-[:UPLOADED_BY]->(u)
            RETURN d.id as docId
        """, {
            'userId': user_id,
            'docId': doc_id,
            'name': file_url.split('/')[-1],
            'docType': data.get('doc_type', 'unknown'),
            'extractedFields': json.dumps(data),
            'fullText': full_text,
            'fullTextLength': len(full_text),
            'fileUrl': file_url,
            'pageCount': data.get('page_count'),
            'statementDate': data.get('statement_date'),
            'statementDateEpoch': statement_epoch,
            'balance': data.get('balance')
        })

        doc_info = result.single()

        # 3. Create company relationships
        if data.get('company_names'):
            tx.run("""
                MATCH (d:Document {id: $docId})
                UNWIND $companies as companyName
                MERGE (c:Company {name: companyName})
                ON CREATE SET c.id = randomUUID(), c.createdAt = datetime()
                ON MATCH SET c.updatedAt = datetime()
                MERGE (d)-[:BELONGS_TO]->(c)
            """, {'docId': doc_id, 'companies': data['company_names']})

        # 4. Create person relationships
        if data.get('person_names'):
            tx.run("""
                MATCH (d:Document {id: $docId})
                UNWIND $people as personName
                MERGE (p:Person {name: personName})
                ON CREATE SET p.id = randomUUID(), p.createdAt = datetime()
                ON MATCH SET p.updatedAt = datetime()
                MERGE (d)-[:MENTIONS]->(p)
            """, {'docId': doc_id, 'people': data['person_names']})

        # 5. Create account relationships
        if data.get('account_numbers'):
            tx.run("""
                MATCH (d:Document {id: $docId})
                UNWIND $accounts as accountNumber
                MERGE (a:Account {number: accountNumber})
                ON CREATE SET
                    a.id = randomUUID(),
                    a.balance = $balance,
                    a.createdAt = datetime()
                ON MATCH SET
                    a.balance = COALESCE($balance, a.balance),
                    a.updatedAt = datetime()
                MERGE (d)-[:RELATED_TO]->(a)
            """, {
                'docId': doc_id,
                'accounts': data['account_numbers'],
                'balance': data.get('balance')
            })

        # 6. Create email relationships
        if data.get('email_addresses'):
            tx.run("""
                MATCH (d:Document {id: $docId})
                UNWIND $emails as emailAddress
                MERGE (e:Email {address: emailAddress})
                ON CREATE SET e.id = randomUUID(), e.createdAt = datetime()
                ON MATCH SET e.updatedAt = datetime()
                MERGE (d)-[:MENTIONS_EMAIL]->(e)
            """, {'docId': doc_id, 'emails': data['email_addresses']})

        return {
            'doc_id': doc_info['docId'],
            'status': 'created'
        }

    def query_documents_by_company(self, company_name: str, limit: int = 100) -> List[Dict]:
        """Get all documents for a company"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (d:Document)-[:BELONGS_TO]->(c:Company {name: $companyName})
                RETURN d
                ORDER BY d.statementDateEpoch DESC
                LIMIT $limit
            """, companyName=company_name, limit=limit)

            return [dict(record['d']) for record in result]

    def close(self):
        """Close driver connection"""
        self.driver.close()
        logger.info("Neo4j driver closed")
```

Key features:

- Atomic transactions (all relationships created together or all fail)
- Connection pooling optimized for 8GB Neo4j
- Secret Manager integration for credentials
- Efficient batch operations with UNWIND

---

## **Part 4: Build the Processing Layer**

The processing layer orchestrates the entire pipeline with retry logic and rate limiting.

## **Create Pipeline Processor**

Create src/pipeline/processor.py:

```py
"""
Pipeline orchestration with resilience
Coordinates: GCS → Extraction → Neo4j
"""

from google.cloud import storage, logging as cloud_logging
from src.extraction.document_extractor import DocumentExtractor
from src.database.neo4j_client import Neo4jClient
import os
import hashlib
import time
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class ProcessingResult:
    doc_id: str
    status: str  # 'success', 'extraction_failed', 'neo4j_failed'
    processing_time: float
    error: str = None

class DocumentPipeline:
    """Resilient document processing pipeline"""

    def __init__(self):
        self.extractor = DocumentExtractor(api_key=os.getenv("GEMINI_API_KEY"))
        self.neo4j = Neo4jClient()
        self.storage = storage.Client()
        self.logger = cloud_logging.Client().logger('pipeline')

        # Verify connections
        if not self.neo4j.verify_connectivity():
            raise RuntimeError("Neo4j connection failed")

    def process_gcs_range(
        self,
        bucket_name: str,
        start_idx: int,
        end_idx: int,
        user_id: str = "system"
    ) -> Dict:
        """
        Process documents in range with batching and retries

        Args:
            bucket_name: GCS bucket name
            start_idx: Starting index for this task
            end_idx: Ending index for this task
            user_id: User ID for attribution

        Returns:
            Processing statistics
        """
        bucket = self.storage.bucket(bucket_name)
        blobs = list(bucket.list_blobs())[start_idx:end_idx]

        self.logger.log_struct({
            'event': 'pipeline_start',
            'bucket': bucket_name,
            'count': len(blobs)
        }, severity='INFO')

        # Process in batches for Neo4j efficiency
        batch_size = 10
        all_results = []

        for i in range(0, len(blobs), batch_size):
            batch_blobs = blobs[i:i + batch_size]
            batch_results = self._process_batch(batch_blobs, bucket_name, user_id)
            all_results.extend(batch_results)

        # Aggregate stats
        stats = {
            'total': len(all_results),
            'success': len([r for r in all_results if r.status == 'success']),
            'extraction_failed': len([r for r in all_results if r.status == 'extraction_failed']),
            'neo4j_failed': len([r for r in all_results if r.status == 'neo4j_failed']),
            'avg_processing_time': sum(r.processing_time for r in all_results) / len(all_results) if all_results else 0
        }

        self.logger.log_struct(stats, severity='INFO')
        return stats

    def _process_batch(
        self,
        blobs: List,
        bucket_name: str,
        user_id: str
    ) -> List[ProcessingResult]:
        """Process batch with extraction + Neo4j write"""

        extracted_docs = []
        results = []

        # Step 1: Extract all documents
        for blob in blobs:
            file_url = f"gs://{bucket_name}/{blob.name}"
            doc_id = self._generate_doc_id(file_url)
            start_time = time.time()

            try:
                # Extract with retry
                structured_data, full_text = self._retry_extraction(file_url)

                extracted_docs.append({
                    'doc_id': doc_id,
                    'extracted_data': structured_data,
                    'full_text': full_text,
                    'file_url': file_url
                })

            except Exception as e:
                processing_time = time.time() - start_time
                results.append(ProcessingResult(
                    doc_id=doc_id,
                    status='extraction_failed',
                    processing_time=processing_time,
                    error=str(e)
                ))

                self.logger.log_struct({
                    'event': 'extraction_failed',
                    'doc_id': doc_id,
                    'error': str(e)
                }, severity='ERROR')

        # Step 2: Batch write to Neo4j
        if extracted_docs:
            neo4j_results = self._write_to_neo4j(extracted_docs, user_id)
            results.extend(neo4j_results)

        return results

    def _retry_extraction(self, file_url: str, max_retries: int = 3):
        """Extract with exponential backoff retry"""
        for attempt in range(max_retries):
            try:
                return self.extractor.extract_document(file_url)
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + 1
                    self.logger.log_text(
                        f"Rate limited, retry in {wait_time}s",
                        severity='WARNING'
                    )
                    time.sleep(wait_time)
                elif attempt == max_retries - 1:
                    raise

    def _write_to_neo4j(
        self,
        documents: List[Dict],
        user_id: str
    ) -> List[ProcessingResult]:
        """Write batch to Neo4j with error handling"""

        results = []

        for doc in documents:
            start_time = time.time()
            try:
                self.neo4j.create_document_with_relationships(
                    doc_id=doc['doc_id'],
                    extracted_data=doc['extracted_data'],
                    full_text=doc['full_text'],
                    file_url=doc['file_url'],
                    user_id=user_id
                )

                processing_time = time.time() - start_time
                results.append(ProcessingResult(
                    doc_id=doc['doc_id'],
                    status='success',
                    processing_time=processing_time
                ))

            except Exception as e:
                processing_time = time.time() - start_time
                results.append(ProcessingResult(
                    doc_id=doc['doc_id'],
                    status='neo4j_failed',
                    processing_time=processing_time,
                    error=str(e)
                ))

        return results

    def _generate_doc_id(self, uri: str) -> str:
        """Generate unique document ID"""
        return hashlib.sha256(uri.encode()).hexdigest()[:16]

    def close(self):
        """Cleanup"""
        self.neo4j.close()
```

Key features:

- Batch processing (10 docs at a time)
- Automatic retry with exponential backoff
- Separate error tracking for extraction vs storage failures
- Comprehensive logging

---

## **Part 5: Deploy to Cloud Run**

Cloud Run Jobs allows parallel, serverless batch processing.

## **Create Deployment Files**

requirements.txt:

```bash
google-generativeai==0.8.0
google-cloud-storage==2.18.2
google-cloud-logging==3.11.1
google-cloud-secret-manager==2.20.2
neo4j==5.24.0
Pillow==10.4.0
python-dotenv==1.0.1
```

main.py (entry point):

```py
"""
Cloud Run Job entry point
Processes assigned range of documents
"""

from src.pipeline.processor import DocumentPipeline
import os
import sys

def main():
    # Get task info from Cloud Run
    task_index = int(os.environ.get('CLOUD_RUN_TASK_INDEX', '0'))
    task_count = int(os.environ.get('CLOUD_RUN_TASK_COUNT', '1'))
    bucket_name = os.environ.get('GCS_BUCKET_NAME')
    total_docs = 40000

    # Calculate range for this task
    docs_per_task = total_docs // task_count
    start_idx = task_index * docs_per_task
    end_idx = start_idx + docs_per_task if task_index < task_count - 1 else total_docs

    print(f"Task {task_index}: Processing docs {start_idx}-{end_idx}")

    # Run pipeline
    pipeline = DocumentPipeline()
    try:
        stats = pipeline.process_gcs_range(bucket_name, start_idx, end_idx)

        print(f"Task {task_index} complete:")
        print(f"  Success: {stats['success']}")
        print(f"  Failed: {stats['extraction_failed'] + stats['neo4j_failed']}")

        # Exit with error if success rate < 90%
        if stats['success'] / stats['total'] < 0.9:
            sys.exit(1)

        sys.exit(0)
    except Exception as e:
        print(f"Task {task_index} fatal error: {e}")
        sys.exit(1)
    finally:
        pipeline.close()

if __name__ == "__main__":
    main()
```

## **Deploy Commands**

```bash
# 1. Store secrets
echo -n "neo4j+s://your-instance.neo4j.io" | \
  gcloud secrets create neo4j-uri --data-file=-

echo -n "neo4j" | \
  gcloud secrets create neo4j-username --data-file=-

echo -n "your-neo4j-password" | \
  gcloud secrets create neo4j-password --data-file=-

# 2. Build and push container
gcloud builds submit --tag gcr.io/YOUR_PROJECT/doc-processor

# 3. Create Cloud Run Job with 40 parallel tasks
gcloud run jobs create doc-processor \
  --image gcr.io/YOUR_PROJECT/doc-processor \
  --tasks 40 \
  --set-env-vars GCS_BUCKET_NAME=your-bucket,GCP_PROJECT_ID=your-project,NEO4J_DATABASE=neo4j \
  --set-secrets GEMINI_API_KEY=gemini-api-key:latest \
  --max-retries 2 \
  --task-timeout 2h \
  --memory 8Gi \
  --cpu 2 \
  --region us-central1

# 4. Execute job
gcloud run jobs execute doc-processor
```

Monitor progress:

```shell
# View logs
gcloud logging read "resource.type=cloud_run_job" \
  --limit=50 --format=json
```

## **Part 6: Query Your Graph**

Now that documents are in Neo4j, you can run powerful relationship queries.

## **Example Queries**

Find all documents for a company:

```python
from src.database.neo4j_client import Neo4jClient

neo4j = Neo4jClient()

# Get company documents
docs = neo4j.query_documents_by_company("Acme Corp", limit=50)

for doc in docs:
    print(f"Document: {doc['name']}")
    print(f"  Type: {doc['docType']}")
    print(f"  Date: {doc['statementDate']}")
    print(f"  Balance: ${doc.get('balance', 'N/A')}")

neo4j.close()
```

Complex Cypher query:

```sql
// Find people mentioned across multiple companies
MATCH (p:Person)-[:MENTIONED_IN]->(d:Document)-[:BELONGS_TO]->(c:Company)
WITH p, count(DISTINCT c) as company_count, collect(DISTINCT c.name) as companies
WHERE company_count > 1
RETURN p.name, company_count, companies
ORDER BY company_count DESC
```

Path finding:

```sql
// Find connection between account and person
MATCH path = shortestPath(
  (a:Account {number: "123456"})-[*]-(p:Person {name: "John Smith"})
)
RETURN path
```

## **Cost Breakdown**

One-time processing (40K docs):

- Gemini extraction: $27
- Cloud Run Jobs: $40
- Total: $67

Monthly recurring:

- Neo4j 8GB (8hrs/day auto-pause): $538
- GCS storage: $2
- Total: $540/month

Total first month: $607

## **Troubleshooting**

## **Issue: 429 Rate Limit Errors**

Solution: You're hitting daily quota (10K RPD). Either:

1. Wait for quota reset (midnight PT)
2. Upgrade to Tier 2 ($250 GCP spend \+ 30 days)
3. Use multiple GCP projects

## **Issue: Gemini Files Quota Exhausted**

Solution: Files not being deleted. Verify file.delete() is in finally block in document_extractor.py.

## **Issue: Neo4j Connection Timeout**

Solution: Check connection pool size (should be 5 for 8GB instance). Verify Neo4j instance is running (not paused).

---

## **Next Steps**

## **Add Embeddings Later**

When ready for semantic search, run this script to chunk and embed existing full text:

```py
from src.database.neo4j_client import Neo4jClient
from openai import OpenAI

neo4j = Neo4jClient()
openai = OpenAI()

# Get documents
with neo4j.driver.session() as session:
    docs = session.run("MATCH (d:Document) RETURN d.id, d.fullText LIMIT 100")

    for doc in docs:
        # Chunk text
        chunks = doc['fullText'].split('. ')

        # Create embeddings
        for i, chunk in enumerate(chunks):
            embedding = openai.embeddings.create(
                model="text-embedding-3-small",
                input=chunk
            ).data.embedding

            # Store in Qdrant or Neo4j
            # (implementation depends on vector DB choice)
```

## **Scale Beyond 40K**

To process millions of documents:

1. Use Gemini Batch API (no quota limits, 50% cheaper)
2. Increase Neo4j to 16GB+ RAM
3. Add Qdrant for vector search

---

## **Conclusion**

Congratulations\! You've built a production-grade document intelligence system that:

Extracts structured data from 40K+ documents  
Stores relationships in a graph database  
Enables complex relationship queries  
Preserves full text for future embedding  
Handles failures gracefully with retry logic  
Scales with parallel processing

This architecture is production-ready and can scale to millions of documents with minimal changes.

---

## **Reference**

- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/)
- [Cloud Run Jobs Documentation](https://cloud.google.com/run/docs/create-jobs)

Created by [Mark Dusseau](https://www.linkedin.com/in/aiwithdusseau/)
