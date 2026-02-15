-- Models table
CREATE TABLE IF NOT EXISTS models (
  id VARCHAR(100) PRIMARY KEY,
  provider_id VARCHAR(50) NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  api_id VARCHAR(100),
  type VARCHAR(50) NOT NULL,
  modalities TEXT[] NOT NULL DEFAULT '{}',
  capabilities TEXT[] NOT NULL DEFAULT '{}',
  context_length INTEGER,
  max_output_tokens INTEGER,
  deprecated BOOLEAN NOT NULL DEFAULT false,
  deprecation_date DATE,
  pricing JSONB NOT NULL,
  self_hosted JSONB,
  source_url VARCHAR(500) NOT NULL,
  last_updated TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_models_provider_id ON models(provider_id);
CREATE INDEX IF NOT EXISTS idx_models_type ON models(type);
CREATE INDEX IF NOT EXISTS idx_models_deprecated ON models(deprecated);
CREATE INDEX IF NOT EXISTS idx_models_capabilities ON models USING GIN(capabilities);
