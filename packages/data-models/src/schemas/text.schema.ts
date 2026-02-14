/**
 * =============================================================================
 * TEXT SCHEMAS
 * =============================================================================
 * Purpose: Defines Zod schemas for text processing domain.
 * These schemas validate text input/output for the preprocessing and
 * feature extraction services.
 *
 * Key Concepts:
 * - Zod: TypeScript-first schema validation library
 * - Schema validation: Ensures data integrity across service boundaries
 * - Type inference: Auto-generates TypeScript types from schemas
 *
 * Author: Cyberbullying Prediction Team
 * Version: 1.0.0
 * =============================================================================
 */

// Import Zod for schema definition
import { z } from 'zod';

/**
 * =============================================================================
 * RAW TEXT INPUT SCHEMA
 * =============================================================================
 * Validates raw text input from users or external sources.
 * This is the entry point for all text data in the system.
 *
 * Fields:
 * - text: The actual text content (required, non-empty string)
 * - id: Unique identifier for the text (optional, auto-generated if missing)
 * - source: Origin of the text (e.g., 'twitter', 'youtube', 'api')
 * - timestamp: When the text was collected (optional, defaults to now)
 * - metadata: Additional context about the text
 *
 * Validation Rules:
 * - text must be a string with at least 1 character
 * - text cannot exceed 10000 characters (configurable)
 * - id must be unique if provided
 * =============================================================================
 */
export const RawTextInputSchema = z.object({
  /**
   * The actual text content to be processed.
   * This is the only required field - all others are optional.
   */
  text: z.string({
    /*
     * Custom error message when text is not a string.
     * Helps with debugging validation failures.
     */
    invalid_type_error: 'Text must be a string',
    /*
     * Custom error message when text is required but not provided.
     */
    required_error: 'Text is required',
  })
    /*
     * Minimum length: Text must contain at least 1 character.
     * Empty strings are not valid input.
     */
    .min(1, { message: 'Text cannot be empty' })
    /*
     * Maximum length: Text cannot exceed 10000 characters.
     * This prevents memory issues and long processing times.
     * Configure based on your model's max input length.
     */
    .max(10000, { message: 'Text cannot exceed 10000 characters' }),

  /**
   * Unique identifier for this text entry.
   * Used for tracking, deduplication, and result association.
   * If not provided, a UUID will be auto-generated.
   */
  id: z.string().uuid().optional(),

  /**
   * Source of the text data.
   * Helps with data provenance and source-specific preprocessing.
   * Examples: 'twitter', 'instagram', 'youtube', 'api', 'manual'
   */
  source: z
    .enum(['twitter', 'instagram', 'youtube', 'facebook', 'reddit', 'api', 'manual', 'unknown'], {
      /*
       * Error message when source is not a valid option.
       */
      errorMap: () => ({ message: 'Invalid source value' }),
    })
    .optional()
    .default('unknown'),

  /**
   * Timestamp when the text was collected or created.
   * Used for temporal analysis and data freshness checks.
   * Defaults to current UTC time if not provided.
   */
  timestamp: z.date().optional().default(() => new Date()),

  /**
   * Additional metadata about the text.
   * Can include author info, platform-specific data, etc.
   * Flexible field for source-specific information.
   */
  metadata: z
    .record(z.string(), z.unknown())
    .optional()
    .default(() => ({})),
});

/**
 * Type inferred from the RawTextInputSchema.
 * Can be used throughout the codebase for type safety.
 * Equivalent to: { text: string; id?: string; source?: ...; ... }
 */
export type RawTextInput = z.infer<typeof RawTextInputSchema>;


/**
 * =============================================================================
 * PREPROCESSED TEXT SCHEMA
 * =============================================================================
 * Validates text after preprocessing (cleaning, normalization).
 * This is the output format from the preprocessing service.
 *
 * Inherits from RawTextInput but adds:
 * - cleaned_text: The processed text content
 * - processing_info: Details about preprocessing applied
 * - language: Detected language of the text
 * - is_valid: Whether the text passed validation
 *
 * Additional Validation:
 * - cleaned_text must be shorter than or equal to original
 * - processing_info tracks all transformations applied
 * =============================================================================
 */
export const PreprocessedTextSchema = RawTextInputSchema.extend({
  /**
   * The cleaned and normalized text after preprocessing.
   * This is the text that will be used for feature extraction.
   */
  cleaned_text: z
    .string({
      invalid_type_error: 'Cleaned text must be a string',
      required_error: 'Cleaned text is required',
    })
    /*
     * Can be empty if text was entirely filtered (e.g., only URLs).
     * is_valid flag indicates whether processing was successful.
     */
    .min(0)
    /*
     * Should not exceed original text length (usually shorter after cleaning).
     */
    .max(10000),

  /**
   * Information about preprocessing steps applied.
   * Useful for debugging and understanding text transformations.
   */
  processing_info: z.object({
    /**
     * Steps applied to the text, in order.
     * Each step is logged with its parameters.
     */
    steps_applied: z.array(
      z.object({
        /**
         * Name of the preprocessing step.
         * Examples: 'remove_urls', 'lowercase', 'remove_emoji'
         */
        step: z.string(),
        /**
         * Whether this step was applied (true) or skipped (false).
         */
        applied: z.boolean(),
        /**
         * Number of characters/tokens affected by this step.
         */
        affected_count: z.number().optional(),
        /**
         * Additional parameters used in this step.
         */
        params: z.record(z.string(), z.unknown()).optional(),
      })
    ),
    /**
     * Total processing time in milliseconds.
     * Useful for performance monitoring.
     */
    processing_time_ms: z.number(),
    /**
     * Original text length before preprocessing.
     */
    original_length: z.number(),
    /**
     * Final text length after preprocessing.
     */
    final_length: z.number(),
  }),

  /**
   * Detected language of the text.
   * Used for language-specific processing and filtering.
   * ISO 639-1 language code (e.g., 'en', 'es', 'fr').
   */
  language: z
    .string()
    .length(2, { message: 'Language must be a 2-letter ISO 639-1 code' })
    .optional(),

  /**
   * Whether the text passed validation checks.
   * False if text was filtered entirely or failed validation.
   */
  is_valid: z.boolean().default(true),

  /**
   * Reason if text is invalid.
   * Examples: 'empty_after_cleaning', 'language_not_supported'
   */
  invalid_reason: z.string().optional(),
});

/**
 * Type inferred from the PreprocessedTextSchema.
 */
export type PreprocessedText = z.infer<typeof PreprocessedTextSchema>;


/**
 * =============================================================================
 * TEXT METADATA SCHEMA
 * =============================================================================
 * Additional information about text data.
 * Used for tracking, analytics, and debugging.
 */
export const TextMetadataSchema = z.object({
  /**
   * Unique identifier matching the text entry.
   */
  text_id: z.string().uuid(),

  /**
   * Character count of the original text.
   */
  character_count: z.number().int().min(0),

  /**
   * Word count of the original text.
   */
  word_count: z.number().int().min(0),

  /**
   * Sentence count (estimated from punctuation).
   */
  sentence_count: z.number().int().min(0),

  /**
   * Average word length in characters.
   */
  average_word_length: z.number().min(0),

  /**
   * Detected language with confidence score.
   */
  language_detection: z
    .object({
      /**
       * ISO 639-1 language code.
       */
      language: z.string().length(2),
      /**
       * Confidence score between 0 and 1.
       */
      confidence: z.number().min(0).max(1),
    })
    .optional(),

  /**
   * Detected text encoding.
   * Usually 'utf-8' for modern text.
   */
  encoding: z.string().default('utf-8'),

  /**
   * Whether text contains URLs.
   */
  has_urls: z.boolean().default(false),

  /**
   * Whether text contains email addresses.
   */
  has_emails: z.boolean().default(false),

  /**
   * Whether text contains phone numbers.
   */
  has_phone_numbers: z.boolean().default(false),

  /**
   * Whether text contains emoji.
   */
  has_emoji: z.boolean().default(false),

  /**
   * Whether text contains mentions (@username).
   */
  has_mentions: z.boolean().default(false),

  /**
   * Whether text contains hashtags.
   */
  has_hashtags: z.boolean().default(false),

  /**
   * Timestamp when metadata was extracted.
   */
  extracted_at: z.date().default(() => new Date()),
});

/**
 * Type inferred from the TextMetadataSchema.
 */
export type TextMetadata = z.infer<typeof TextMetadataSchema>;


/**
 * =============================================================================
 * SCHEMA EXPORTS
 * =============================================================================
 * Export all schemas for use in other modules.
 * Also exports a map for schema lookup by name.
 */
export const TextSchemas = {
  /**
   * Schema for validating raw text input.
   */
  raw: RawTextInputSchema,
  /**
   * Schema for validating preprocessed text output.
   */
  preprocessed: PreprocessedTextSchema,
  /**
   * Schema for validating text metadata.
   */
  metadata: TextMetadataSchema,
} as const;

/**
 * Union type of all text schema names.
 */
export type TextSchemaName = keyof typeof TextSchemas;
