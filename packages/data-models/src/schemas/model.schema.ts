/**
 * =============================================================================
 * MODEL REGISTRY SCHEMAS
 * =============================================================================
 * Purpose: Defines Zod schemas for model versioning, storage, and metadata.
 *
 * Key Concepts:
 * - Model metadata: Information about registered models
 * - Model versions: Tracking changes between iterations
 * - Model artifacts: Storage information for model files
 *
 * Author: Cyberbullying Prediction Team
 * Version: 1.0.0
 * =============================================================================
 */

import { z } from 'zod';

/**
 * =============================================================================
 * MODEL ARCHITECTURE DEFINITIONS
 * =============================================================================
 * All supported model architectures in the system.
 */
export const ModelArchitectureEnum = z.enum([
  'bert-base',
  'bert-large',
  'roberta-base',
  'roberta-large',
  'distilbert-base',
  'deberta-v3-base',
  'deberta-v3-large',
  'lstm',
  'gru',
  'cnn-lstm',
  'bi-lstm',
  'bi-gru',
  'transformer-encoder',
  'ensemble',
  'custom',
]);

/**
 * Type for model architecture values.
 */
export type ModelArchitecture = z.infer<typeof ModelArchitectureEnum>;


/**
 * =============================================================================
 * MODEL ARTIFACT SCHEMA
 * =============================================================================
 * Storage information for model files.
 * Contains paths to model weights, config, and associated files.
 */
export const ModelArtifactSchema = z.object({
  /**
   * Unique identifier for this artifact.
   */
  artifact_id: z.string().uuid(),

  /**
   * Model version this artifact belongs to.
   */
  model_version: z.string(),

  /**
   * Type of artifact.
   */
  artifact_type: z.enum([
    'model_weights',
    'model_config',
    'tokenizer',
    'vocabulary',
    'preprocessor',
    'postprocessor',
    'onnx_model',
    'metrics',
    'other',
  ]),

  /**
   * Storage location (S3 path, local path, etc.).
   */
  storage_path: z.string(),

  /**
   * Size of the artifact in bytes.
   */
  file_size_bytes: z.number().int().positive(),

  /**
   * MD5 checksum for integrity verification.
   */
  checksum: z.string().optional(),

  /**
   * Compression used (if any).
   */
  compression: z.enum(['none', 'gzip', 'zip', 'tar.gz']).default('none'),

  /**
   * Whether this artifact is required for inference.
   */
  required_for_inference: z.boolean().default(true),

  /**
   * Additional metadata about this artifact.
   */
  metadata: z.record(z.string(), z.unknown()).optional(),

  /**
   * Timestamp when artifact was created.
   */
  created_at: z.date().default(() => new Date()),
});

/**
 * Type inferred from ModelArtifactSchema.
 */
export type ModelArtifact = z.infer<typeof ModelArtifactSchema>;


/**
 * =============================================================================
 * MODEL VERSION SCHEMA
 * =============================================================================
 * Specific version of a model.
 * Tracks changes between model iterations.
 */
export const ModelVersionSchema = z.object({
  /**
   * Unique version identifier (semantic versioning).
   * Examples: '1.0.0', '2.1.3', '1.0.0-rc1'
   */
  version: z.string().regex(/^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$/),

  /**
   * Model name this version belongs to.
   */
  model_name: z.string().min(1).max(100),

  /**
   * Model architecture used.
   */
  architecture: ModelArchitectureEnum,

  /**
   * Training configuration used for this version.
   */
  training_config: z.object({
    dataset: z.string(),
    epochs: z.number().int().positive(),
    batch_size: z.number().int().positive(),
    learning_rate: z.number().positive(),
    max_seq_length: z.number().int().positive(),
  }),

  /**
   * Artifacts associated with this version.
   */
  artifacts: z.array(ModelArtifactSchema),

  /**
   * Performance metrics for this version.
   */
  metrics: z.object({
    accuracy: z.number().min(0).max(1).optional(),
    precision: z.number().min(0).max(1).optional(),
    recall: z.number().min(0).max(1).optional(),
    f1_score: z.number().min(0).max(1).optional(),
    auc_roc: z.number().min(0).max(1).optional(),
  }).optional(),

  /**
   * Parent model name (for variants).
   */
  parent_model: z.string().optional(),

  /**
   * Changelog for this version.
   */
  changelog: z.string().optional(),

  /**
   * Whether this version is deprecated.
   */
  deprecated: z.boolean().default(false),

  /**
   * Deprecation message (if deprecated).
   */
  deprecation_message: z.string().optional(),

  /**
   * Timestamp when version was created.
   */
  created_at: z.date().default(() => new Date()),

  /**
   * User who created this version.
   */
  created_by: z.string().optional(),
});

/**
 * Type inferred from ModelVersionSchema.
 */
export type ModelVersion = z.infer<typeof ModelVersionSchema>;


/**
 * =============================================================================
 * MODEL METADATA SCHEMA
 * =============================================================================
 * Information about a registered model.
 * Includes version, author, creation date, and performance metrics.
 */
export const ModelMetadataSchema = z.object({
  /**
   * Unique model identifier.
   */
  model_id: z.string().uuid(),

  /**
   * Unique model name.
   */
  model_name: z.string().min(1).max(100),

  /**
   * Model description.
   */
  description: z.string().max(1000).optional(),

  /**
   * Task this model performs.
   */
  task: z.enum([
    'text_classification',
    'sequence_labeling',
    'token_classification',
    'question_answering',
    'text_generation',
    'embedding',
  ]).default('text_classification'),

  /**
   * Model architecture.
   */
  architecture: ModelArchitectureEnum,

  /**
   * All versions of this model.
   */
  versions: z.array(ModelVersionSchema),

  /**
   * Tags for categorization.
   */
  tags: z.array(z.string()).default([]),

  /**
   * License for the model.
   */
  license: z.string().default('MIT'),

  /**
   * Author information.
   */
  author: z.object({
    name: z.string().optional(),
    email: z.string().email().optional(),
    organization: z.string().optional(),
  }).optional(),

  /**
   * Dataset used for training.
   */
  training_dataset: z.string().optional(),

  /**
   * Paper or reference for the model.
   */
  reference: z.string().url().optional(),

  /**
   * Citation information.
   */
  citation: z.string().optional(),

  /**
   * Input schema for the model.
   */
  input_schema: z.record(z.string(), z.unknown()).optional(),

  /**
   * Output schema for the model.
   */
  output_schema: z.record(z.string(), z.unknown()).optional(),

  /**
   * Framework used (PyTorch, TensorFlow, etc.).
   */
  framework: z.enum(['pytorch', 'tensorflow', 'onnx', 'jax', 'custom']).default('pytorch'),

  /**
   * Whether model supports GPU inference.
   */
  supports_gpu: z.boolean().default(true),

  /**
   * Whether model is available for inference.
   */
  is_available: z.boolean().default(true),

  /**
   * Timestamp when model was registered.
   */
  registered_at: z.date().default(() => new Date()),

  /**
   * Timestamp when model was last updated.
   */
  updated_at: z.date().default(() => new Date()),
});

/**
 * Type inferred from ModelMetadataSchema.
 */
export type ModelMetadata = z.infer<typeof ModelMetadataSchema>;


/**
 * =============================================================================
 * EXPORT ALL MODEL SCHEMAS
 * =============================================================================
 */
export const ModelSchemas = {
  architecture: ModelArchitectureEnum,
  artifact: ModelArtifactSchema,
  version: ModelVersionSchema,
  metadata: ModelMetadataSchema,
} as const;

export type ModelSchemaName = keyof typeof ModelSchemas;
