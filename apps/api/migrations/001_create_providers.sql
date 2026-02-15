-- Providers table
CREATE TABLE IF NOT EXISTS providers (
  id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  pricing_url VARCHAR(500) NOT NULL,
  api_docs_url VARCHAR(500),
  last_updated TIMESTAMPTZ NOT NULL
);
