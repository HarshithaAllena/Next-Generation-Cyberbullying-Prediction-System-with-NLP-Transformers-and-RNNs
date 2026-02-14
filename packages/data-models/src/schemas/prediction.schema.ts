/**
 * =============================================================================
 * PREDICTION SCHEMAS
 * =============================================================================
 * Purpose: Defines Zod schemas for prediction domain - model inference results,
 * confidence scores, and explainability outputs.
 *
 * Key Concepts:
 * - Classification labels: Valid output classes for cyberbullying detection
 * - Confidence scores: Probability distributions over classes
 * - Batch processing: Optimized schemas for bulk predictions
 * - Explanation: Feature importance and attention weights for XAI
 *
 * Author: Cyberbullying Prediction Team
 * Version: 1.0.0
 * =============================================================================
 */

import { z } from 'zod';

/**
 * =============================================================================
 * CLASSIFICATION LABEL DEFINITIONS
 * =============================================================================
 * All possible classification outcomes for cyberbullying detection.
 * These labels are used throughout the prediction pipeline.
 *
 * Labels:
 * - bullying: Content that contains bullying behavior
 * - not_bullying: Content that does not contain bullying
 * - harassment: Specific form of bullying/harassment
 * - hate_speech: Content containing hate speech
 * - aggression: Aggressive language or behavior
 * - attack: Personal attacks
 * - spam: Irrelevant or harmful spam content
 * - none: No detectable issue with the content
 * =============================================================================
 */
export const ClassificationLabelEnum = z.enum([
  'bullying',
  'not_bullying',
  'harassment',
  'hate_speech',
  'aggression',
  'attack',
  'spam',
  'none',
]);

/**
 * Type for classification label values.
 */
export type ClassificationLabel = z.infer<typeof ClassificationLabelEnum>;


/**
 * =============================================================================
 * CONFIDENCE INTERVAL SCHEMA
 * =============================================================================
 * Statistical confidence bounds for predictions.
 * Provides upper and lower bounds at a given confidence level.
 */
export const ConfidenceIntervalSchema = z.object({
  /**
   * Lower bound of the confidence interval.
   */
  lower: z.number().min(0).max(1),
  /**
   * Upper bound of the confidence interval.
   */
  upper: z.number().min(0).max(1),
  /**
   * Confidence level (e.g., 0.95 for 95% CI).
   */
  level: z.number().min(0).max(1).default(0.95),
});

/**
 * Type inferred from ConfidenceIntervalSchema.
 */
export type ConfidenceInterval = z.infer<typeof ConfidenceIntervalSchema>;


/**
 * =============================================================================
 * PREDICTION RESULT SCHEMA
 * =============================================================================
 * Single prediction result from the model.
 * Contains the predicted class, confidence, and supporting information.
 *
 * This is the primary output format for real-time predictions.
 */
export const PredictionResultSchema = z.object({
  /**
   * Unique identifier matching the input text.
   */
  text_id: z.string().uuid(),

  /**
   * The predicted classification label.
   */
  predicted_label: ClassificationLabelEnum,

  /**
   * Confidence score for the prediction (0-1).
   * Higher values indicate more confident predictions.
   */
  confidence: z.number().min(0).max(1),

  /**
   * Probability distribution over all possible labels.
   * Sum of all values equals 1.
   */
  probabilities: z.record(ClassificationLabelEnum, z.number().min(0).max(1)),

  /**
   * Whether the prediction meets the confidence threshold.
   */
  is_high_confidence: z.boolean(),

  /**
   * Confidence threshold used for classification.
   * Configurable based on precision/recall tradeoffs.
   */
  confidence_threshold: z.number().min(0).max(1).default(0.5),

  /**
   * Model version used for this prediction.
   */
  model_version: z.string(),

  /**
   * Model architecture used (e.g., 'bert-base', 'roberta').
   */
  model_architecture: z.string(),

  /**
   * Timestamp when prediction was made.
   */
  predicted_at: z.date().default(() => new Date()),

  /**
   * Inference time in milliseconds.
   * Useful for performance monitoring.
   */
  inference_time_ms: z.number().optional(),

  /**
   * Optional confidence interval for the prediction.
   */
  confidence_interval: ConfidenceIntervalSchema.optional(),

  /**
   * Additional metadata about the prediction.
   */
  metadata: z.record(z.string(), z.unknown()).optional(),
});

/**
 * Type inferred from PredictionResultSchema.
 */
export type PredictionResult = z.infer<typeof PredictionResultSchema>;


/**
 * =============================================================================
 * BATCH PREDICTION RESULT SCHEMA
 * =============================================================================
 * Optimized schema for batch processing multiple predictions.
 * Includes summary statistics and error tracking.
 */
export const BatchPredictionResultSchema = z.object({
  /**
   * Unique batch identifier.
   */
  batch_id: z.string().uuid(),

  /**
   * Array of individual prediction results.
   */
  predictions: z.array(PredictionResultSchema),

  /**
   * Total number of texts processed.
   */
  total_processed: z.number().int().min(0),

  /**
   * Number of predictions that failed.
   */
  failed_count: z.number().int().min(0).default(0),

  /**
   * Error messages for failed predictions.
   */
  errors: z
    .array(
      z.object({
        text_id: z.string().uuid(),
        error_message: z.string(),
      })
    )
    .optional(),

  /**
   * Processing statistics for the batch.
   */
  batch_stats: z.object({
    /**
     * Total processing time in milliseconds.
     */
    total_time_ms: z.number().min(0),
    /**
     * Average time per prediction in milliseconds.
     */
    avg_time_per_prediction_ms: z.number().min(0),
    /**
     * Maximum time for any single prediction.
     */
    max_time_ms: z.number().min(0),
    /**
     * Minimum time for any single prediction.
     */
    min_time_ms: z.number().min(0),
  }),

  /**
   * Timestamp when batch processing started.
   */
  started_at: z.date(),

  /**
   * Timestamp when batch processing completed.
   */
  completed_at: z.date(),
});

/**
 * Type inferred from BatchPredictionResultSchema.
 */
export type BatchPredictionResult = z.infer<typeof BatchPredictionResultSchema>;


/**
 * =============================================================================
 * PREDICTION EXPLANATION SCHEMA
 * =============================================================================
 * Explainable AI output for model interpretability.
 * Contains feature importance and attention weights.
 *
 * This schema supports multiple explanation methods:
 * - SHAP: Shapley Additive Explanations
 * - LIME: Local Interpretable Model-agnostic Explanations
 * - Attention: Transformer attention weights
 */
export const PredictionExplanationSchema = z.object({
  /**
   * Unique identifier matching the prediction.
   */
  prediction_id: z.string().uuid(),

  /**
   * Text ID this explanation is for.
   */
  text_id: z.string().uuid(),

  /**
   * Method used for generating the explanation.
   */
  explanation_method: z.enum(['shap', 'lime', 'attention', 'integrated']),

  /**
   * Feature importance scores.
   * Maps feature names to importance values.
   */
  feature_importance: z.record(z.string(), z.number()),

  /**
   * Token-level importance (for text).
   * Array of tokens with their importance scores.
   */
  token_importance: z
    .array(
      z.object({
        token: z.string(),
        importance: z.number(),
        /**
         * Token position in the original text.
         */
        position: z.number().int(),
      })
    )
    .optional(),

  /**
   * Attention weights (for transformer models).
   * Contains attention matrices from the model.
   */
  attention_weights: z
    .object({
      /**
         * Number of attention heads.
         */
      num_heads: z.number().int(),
      /**
         * Number of layers.
         */
      num_layers: z.number().int(),
      /**
         * Attention weights as nested arrays.
         */
      weights: z.array(z.array(z.array(z.array(z.number())))),
    })
    .optional(),

  /**
   * Text segments identified as contributing to prediction.
   * Useful for highlighting toxic parts of text.
   */
  highlighted_segments: z
    .array(
      z.object({
        text: z.string(),
        start_position: z.number().int(),
        end_position: z.number().int(),
        importance: z.number(),
        reason: z.string().optional(),
      })
    )
    .optional(),

  /**
   * Natural language explanation of the prediction.
     */
  text_explanation: z.string().optional(),

  /**
   * Model version used for explanation.
   */
  model_version: z.string(),

  /**
   * Timestamp when explanation was generated.
   */
  generated_at: z.date().default(() => new Date()),
});

/**
 * Type inferred from PredictionExplanationSchema.
 */
export type PredictionExplanation = z.infer<typeof PredictionExplanationSchema>;


/**
 * =============================================================================
 * EXPORT ALL SCHEMAS
 * =============================================================================
 */
export const PredictionSchemas = {
  label: ClassificationLabelEnum,
  confidence_interval: ConfidenceIntervalSchema,
  prediction_result: PredictionResultSchema,
  batch_prediction_result: BatchPredictionResultSchema,
  explanation: PredictionExplanationSchema,
} as const;

export type PredictionSchemaName = keyof typeof PredictionSchemas;
