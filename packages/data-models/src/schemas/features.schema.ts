/**
 * =============================================================================
 * FEATURES SCHEMAS
 * =============================================================================
 * Purpose: Defines Zod schemas for feature extraction domain - embeddings,
 * statistical features, and derived attributes from text.
 *
 * Key Concepts:
 * - Embeddings: Dense vector representations of text
 * - Statistical features: Character count, word count, etc.
 * - Derived features: Sentiment, toxicity scores, etc.
 *
 * Author: Cyberbullying Prediction Team
 * Version: 1.0.0
 * =============================================================================
 */

import { z } from 'zod';

/**
 * =============================================================================
 * EMBEDDING VECTOR SCHEMA
 * =============================================================================
 * Dense vector representation of text.
 * Used for similarity search and as input to ML models.
 */
export const EmbeddingVectorSchema = z.object({
  /**
   * Unique identifier for this embedding.
   */
  embedding_id: z.string().uuid().optional(),

  /**
   * Text ID this embedding represents.
   */
  text_id: z.string().uuid(),

  /**
   * The embedding vector as an array of numbers.
   * Dimensions depend on the embedding model used.
   */
  vector: z.array(z.number()),

  /**
   * Dimensionality of the embedding.
   */
  dimensions: z.number().int().positive(),

  /**
   * Model used to generate this embedding.
   * Examples: 'sentence-transformers/all-MiniLM-L6-v2', 'bert-base-uncased'
   */
  model_name: z.string(),

  /**
   * Pooling method used (for transformer models).
   */
  pooling_method: z.enum(['mean', 'cls', 'max', 'sum']).default('mean'),

  /**
   * Whether this is the pooled [CLS] token embedding.
   */
  use_cls_token: z.boolean().default(false),

  /**
   * Normalized embedding (L2 normalized to unit length).
   */
  normalized: z.boolean().default(false),

  /**
   * Timestamp when embedding was generated.
   */
  generated_at: z.date().default(() => new Date()),
});

/**
 * Type inferred from EmbeddingVectorSchema.
 */
export type EmbeddingVector = z.infer<typeof EmbeddingVectorSchema>;


/**
 * =============================================================================
 * TEXT FEATURES SCHEMA
 * =============================================================================
 * Extracted features from text.
 * Contains embeddings, statistical features, and derived attributes.
 */
export const TextFeaturesSchema = z.object({
  /**
   * Unique identifier for these features.
   */
  features_id: z.string().uuid().optional(),

  /**
   * Text ID these features belong to.
   */
  text_id: z.string().uuid(),

  /**
   * Preprocessed text used for feature extraction.
   */
  preprocessed_text: z.string(),

  /**
   * Statistical features extracted from text.
   */
  statistical_features: z.object({
    /**
     * Number of characters in the text.
     */
    character_count: z.number().int().min(0),
    /**
     * Number of words in the text.
     */
    word_count: z.number().int().min(0),
    /**
     * Number of unique words (vocabulary size).
     */
    unique_word_count: z.number().int().min(0),
    /**
     * Average word length in characters.
     */
    average_word_length: z.number().min(0),
    /**
     * Number of sentences (estimated).
     */
    sentence_count: z.number().int().min(0),
    /**
     * Average sentence length in words.
     */
    average_sentence_length: z.number().min(0),
    /**
     * Number of uppercase characters.
     */
    uppercase_count: z.number().int().min(0),
    /**
     * Ratio of uppercase to total characters.
     */
    uppercase_ratio: z.number().min(0).max(1),
    /**
     * Number of exclamation marks.
     */
    exclamation_count: z.number().int().min(0),
    /**
     * Number of question marks.
     */
    question_count: z.number().int().min(0),
    /**
     * Number of repeated characters (e.g., 'sooo').
     */
    repeated_char_count: z.number().int().min(0),
  }),

  /**
   * Social media specific features.
   */
  social_features: z.object({
    /**
     * Number of mentions (@username).
     */
    mention_count: z.number().int().min(0).default(0),
    /**
     * Number of hashtags.
     */
    hashtag_count: z.number().int().min(0).default(0),
    /**
     * Number of URLs.
     */
    url_count: z.number().int().min(0).default(0),
    /**
     * Number of emojis.
     */
    emoji_count: z.number().int().min(0).default(0),
    /**
     * Number of user mentions (unique).
     */
    unique_mention_count: z.number().int().min(0).default(0),
    /**
     * Whether text is a retweet.
     */
    is_retweet: z.boolean().default(false),
    /**
     * Whether text contains media.
     */
    has_media: z.boolean().default(false),
  }),

  /**
   * Linguistic features.
   */
  linguistic_features: z.object({
    /**
     * Lexical diversity (unique words / total words).
     */
    lexical_diversity: z.number().min(0).max(1),
    /**
     * Readability score (Flesch reading ease).
     */
    readability_score: z.number().optional(),
    /**
     * Sentiment polarity (-1 to 1).
     */
    sentiment_polarity: z.number().min(-1).max(1).optional(),
    /**
     * Sentiment subjectivity (0 to 1).
     */
    sentiment_subjectivity: z.number().min(0).max(1).optional(),
  }),

  /**
   * Embedding vector representation.
   */
  embedding: EmbeddingVectorSchema.optional(),

  /**
   * Custom features added by user.
   */
  custom_features: z.record(z.string(), z.number()).optional(),

  /**
   * Timestamp when features were extracted.
   */
  extracted_at: z.date().default(() => new Date()),
});

/**
 * Type inferred from TextFeaturesSchema.
 */
export type TextFeatures = z.infer<typeof TextFeaturesSchema>;


/**
 * =============================================================================
 * FEATURE IMPORTANCE SCHEMA
 * =============================================================================
 * Importance scores for each feature.
 * Used for model interpretability and feature selection.
 */
export const FeatureImportanceSchema = z.object({
  /**
   * Unique identifier for this importance analysis.
   */
  importance_id: z.string().uuid().optional(),

  /**
   * Model version these importances are for.
   */
  model_version: z.string(),

  /**
   * Feature importance scores.
   * Maps feature names to importance values.
   */
  feature_importances: z.record(z.string(), z.number()),

  /**
   * Top N most important features.
   */
  top_features: z.array(
    z.object({
      feature_name: z.string(),
      importance: z.number(),
      rank: z.number().int().positive(),
    })
  ),

  /**
   * Analysis method used.
   */
  analysis_method: z.enum(['shap', 'permutation', 'coefficient', 'gain']),

  /**
   * Dataset used for analysis.
   */
  dataset_name: z.string().optional(),

  /**
   * Number of samples used for analysis.
   */
  sample_size: z.number().int().positive().optional(),

  /**
   * Timestamp when analysis was performed.
   */
  analyzed_at: z.date().default(() => new Date()),
});

/**
 * Type inferred from FeatureImportanceSchema.
 */
export type FeatureImportance = z.infer<typeof FeatureImportanceSchema>;


/**
 * =============================================================================
 * EXPORT ALL FEATURE SCHEMAS
 * =============================================================================
 */
export const FeatureSchemas = {
  embedding: EmbeddingVectorSchema,
  text_features: TextFeaturesSchema,
  importance: FeatureImportanceSchema,
} as const;

export type FeatureSchemaName = keyof typeof FeatureSchemas;
