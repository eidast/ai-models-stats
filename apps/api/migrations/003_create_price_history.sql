-- Price history table (optional, for future use)
CREATE TABLE IF NOT EXISTS price_history (
  id BIGSERIAL PRIMARY KEY,
  model_id VARCHAR(100) NOT NULL REFERENCES models(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  pricing JSONB NOT NULL,
  source VARCHAR(50),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_price_history_model_date ON price_history(model_id, date);
