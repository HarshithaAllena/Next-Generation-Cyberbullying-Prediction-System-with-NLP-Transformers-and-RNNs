/**
 * =============================================================================
 * TRAINING SCHEMAS
 * =============================================================================
 * Purpose: Defines Zod schemas for model training domain - configuration,
 * metrics, evaluation results, and checkpoint management.
 *
 * Key Concepts:
 * - Training configuration: Hyperparameters and training options
 * - Training metrics: Loss, accuracy, and custom metrics per epoch
 * - Evaluation: Comprehensive model performance metrics
 * - Checkpoints: Saved model states during training
 *
 * Author: Cyberbullying Prediction Team
 * Version: 1.0.0
 * =============================================================================
 */

import { z } from 'zod';

/**
 * =============================================================================
 * TRAINING CONFIGURATION SCHEMA
 * =============================================================================
 * Configuration for model training.
 * Contains all hyperparameters and training options.
 */
export const TrainingConfigSchema = z.object({
  /**
   * Unique identifier for this training run.
   * Used for tracking and reproducibility.
   */
  run_id: z.string().uuid().optional(),

  /**
   * Name of the experiment this training belongs to.
   */
  experiment_name: z.string().min(1).max(100),

  /**
   * Model architecture to use.
   */
  model_architecture: z.enum([
    'bert-base',
    'bert-large',
    'roberta-base',
    'roberta-large',
    'distilbert-base',
    'lstm',
    'gru',
    'cnn-lstm',
    'ensemble',
  ]),

  /**
   * Learning rate for optimization.
   */
  learning_rate: z.number().positive().default(0.001),

  /**
   * Batch size for training.
   */
  batch_size: z.number().int().positive().default(32),

  /**
   * Number of epochs to train.
   */
  epochs: z.number().int().positive().default(10),

  /**
   * Maximum sequence length for tokenization.
   */
  max_seq_length: z.number().int().positive().default(128),

  /**
   * Optimizer to use.
   */
  optimizer: z.enum(['adam', 'adamw', 'sgd', 'rmsprop']).default('adamw'),

  /**
   * Learning rate scheduler.
   */
  scheduler: z
    .enum(['constant', 'linear', 'cosine', 'step', 'exponential'])
    .default('linear'),

  /**
   * Warmup steps for learning rate.
   */
  warmup_steps: z.number().int().min(0).default(0),

  /**
   * Weight decay for regularization.
   */
  weight_decay: z.number().min(0).default(0.01),

  /**
   * Dropout rate for regularization.
   */
  dropout_rate: z.number().min(0).max(1).default(0.1),

  /**
   * Early stopping patience (epochs without improvement).
   */
  early_stopping_patience: z.number().int().min(0).default(3),

  /**
   * Gradient clipping threshold.
   */
  gradient_clip_norm: z.number().positive().optional(),

  /**
   * Mixed precision training.
   */
  use_amp: z.boolean().default(false),

  /**
   * Data augmentation options.
   */
  augmentation: z
    .object({
      /**
       * Enable back-translation augmentation.
       */
      back_translation: z.boolean().default(false),
      /**
       * Enable synonym replacement.
       */
      synonym_replacement: z.boolean().default(false),
      /**
       * Enable random insertion.
       */
      random_insertion: z.boolean().default(false),
      /**
       * Enable random swap.
       */
      random_swap: z.boolean().default(false),
      /**
       * Enable random deletion.
       */
      random_deletion: z.boolean().default(false),
    })
    .optional(),

  /**
   * Paths to training data.
   */
  data_paths: z.object({
    train: z.string(),
    validation: z.string().optional(),
    test: z.string().optional(),
  }),

  /**
   * Output directory for checkpoints and logs.
   */
  output_dir: z.string(),

  /**
   * Random seed for reproducibility.
   */
  seed: z.number().int().default(42),

  /**
   * Number of workers for data loading.
   */
  num_workers: z.number().int().default(4),

  /**
   * Whether to save checkpoints every epoch.
   */
  save_checkpoints: z.boolean().default(true),

  /**
   * Checkpoint save frequency (every N epochs).
   */
  checkpoint_frequency: z.number().int().positive().default(1),
});

/**
 * Type inferred from TrainingConfigSchema.
 */
export type TrainingConfig = z.infer<typeof TrainingConfigSchema>;


/**
 * =============================================================================
 * TRAINING METRICS SCHEMA
 * =============================================================================
 * Metrics collected during training.
 * Includes loss, accuracy, and custom metrics per epoch.
 */
export const TrainingMetricsSchema = z.object({
  /**
   * Training run identifier.
   */
  run_id: z.string().uuid(),

  /**
   * Epoch number (1-indexed).
   */
  epoch: z.number().int().positive(),

  /**
   * Training loss for this epoch.
   */
  train_loss: z.number(),

  /**
   * Training accuracy for this epoch.
   */
  train_accuracy: z.number().min(0).max(1),

  /**
   * Validation loss for this epoch.
   */
  val_loss: z.number().optional(),

  /**
   * Validation accuracy for this epoch.
   */
  val_accuracy: z.number().min(0).max(1).optional(),

  /**
   * Learning rate used in this epoch.
   */
  learning_rate: z.number(),

  /**
   * Epoch duration in seconds.
   */
  epoch_duration_seconds: z.number().positive(),

  /**
   * Batch metrics (optional, for detailed analysis).
   */
  batch_metrics: z
    .array(
      z.object({
        batch: z.number().int().positive(),
        loss: z.number(),
        accuracy: z.number().min(0).max(1),
      })
    )
    .optional(),

  /**
   * Custom metrics for this epoch.
   */
  custom_metrics: z.record(z.string(), z.number()).optional(),

  /**
   * Timestamp when metrics were recorded.
   */
  recorded_at: z.date().default(() => new Date()),
});

/**
 * Type inferred from TrainingMetricsSchema.
 */
export type TrainingMetrics = z.infer<typeof TrainingMetricsSchema>;


/**
 * =============================================================================
 * EVALUATION RESULT SCHEMA
 * =============================================================================
 * Comprehensive model evaluation results.
 * Contains precision, recall, F1, and other classification metrics.
 */
export const EvaluationResultSchema = z.object({
  /**
   * Unique identifier for this evaluation.
   */
  evaluation_id: z.string().uuid(),

  /**
   * Model version being evaluated.
   */
  model_version: z.string(),

  /**
   * Dataset used for evaluation.
   */
  dataset_name: z.string(),

  /**
   * Number of samples in evaluation set.
   */
  sample_count: z.number().int().positive(),

  /**
   * Overall accuracy.
   */
  accuracy: z.number().min(0).max(1),

  /**
   * Per-class metrics.
   */
  per_class_metrics: z.record(
    z.string(),
    z.object({
      /**
       * Precision for this class.
       */
      precision: z.number().min(0).max(1),
      /**
       * Recall for this class.
       */
      recall: z.number().min(0).max(1),
      /**
       * F1 score for this class.
       */
      f1_score: z.number().min(0).max(1),
      /**
       * Support (number of samples) for this class.
       */
      support: z.number().int().positive(),
    })
  ),

  /**
   * Macro-averaged metrics.
   */
  macro_metrics: z.object({
    precision: z.number().min(0).max(1),
    recall: z.number().min(0).max(1),
    f1_score: z.number().min(0).max(1),
  }),

  /**
   * Weighted-averaged metrics.
   */
  weighted_metrics: z.object({
    precision: z.number().min(0).max(1),
    recall: z.number().min(0).max(1),
    f1_score: z.number().min(0).max(1),
  }),

  /**
   * Confusion matrix (rows: actual, columns: predicted).
   */
  confusion_matrix: z.array(z.array(z.number().int())),

  /**
   * ROC AUC scores (one-vs-rest).
   */
  roc_auc: z.record(z.string(), z.number().min(0).max(1)).optional(),

  /**
   * Prediction time statistics.
   */
  inference_stats: z.object({
    total_time_ms: z.number().positive(),
    avg_time_ms: z.number().positive(),
    min_time_ms: z.number().positive(),
    max_time_ms: z.number().positive(),
  }),

  /**
   * Timestamp when evaluation was performed.
   */
  evaluated_at: z.date().default(() => new Date()),
});

/**
 * Type inferred from EvaluationResultSchema.
 */
export type EvaluationResult = z.infer<typeof EvaluationResultSchema>;


/**
 * =============================================================================
 * MODEL CHECKPOINT SCHEMA
 * =============================================================================
 * Saved model state during training.
 * Contains model weights, optimizer state, and metadata.
 */
export const ModelCheckpointSchema = z.object({
  /**
   * Unique identifier for this checkpoint.
   */
  checkpoint_id: z.string().uuid(),

  /**
   * Training run this checkpoint belongs to.
   */
  run_id: z.string().uuid(),

  /**
   * Epoch number when checkpoint was saved.
   */
  epoch: z.number().int().positive(),

  /**
   * Global step number.
   */
  global_step: z.number().int().positive(),

  /**
   * Path to checkpoint files in storage.
   */
  checkpoint_path: z.string(),

  /**
   * Model weights file.
   */
  model_weights_path: z.string().optional(),

  /**
   * Optimizer state file.
   */
  optimizer_state_path: z.string().optional(),

  /**
   * Training configuration used.
   */
  training_config: TrainingConfigSchema,

  /**
   * Metrics at this checkpoint.
   */
  metrics: z.object({
    /**
     * Best validation loss achieved so far.
     */
    best_val_loss: z.number().optional(),
    /**
     * Best validation accuracy achieved so far.
     */
    best_val_accuracy: z.number().optional(),
    /**
     * Current training loss.
     */
    current_train_loss: z.number(),
    /**
     * Current training accuracy.
     */
    current_train_accuracy: z.number().optional(),
  }),

  /**
   * File size in bytes.
   */
  file_size_bytes: z.number().int().positive(),

  /**
   * Whether this is the best checkpoint so far.
   */
  is_best: z.boolean().default(false),

  /**
   * Whether this is the latest checkpoint.
   */
  is_latest: z.boolean().default(false),

  /**
   * Timestamp when checkpoint was saved.
   */
  saved_at: z.date().default(() => new Date()),
});

/**
 * Type inferred from ModelCheckpointSchema.
 */
export type ModelCheckpoint = z.infer<typeof ModelCheckpointSchema>;


/**
 * =============================================================================
 * EXPORT ALL TRAINING SCHEMAS
 * =============================================================================
 */
export const TrainingSchemas = {
  config: TrainingConfigSchema,
  metrics: TrainingMetricsSchema,
  evaluation: EvaluationResultSchema,
  checkpoint: ModelCheckpointSchema,
} as const;

export type TrainingSchemaName = keyof typeof TrainingSchemas;
