/**
 * =============================================================================
 * SERVICE SCHEMAS
 * =============================================================================
 * Purpose: Defines Zod schemas for service communication - health checks,
 * status, errors, and common service patterns.
 *
 * Key Concepts:
 * - Health checks: Service availability and status
 * - Error handling: Standardized error responses
 * - Pagination: List endpoints pagination
 * - API responses: Common response patterns
 *
 * Author: Cyberbullying Prediction Team
 * Version: 1.0.0
 * =============================================================================
 */

import { z } from 'zod';

/**
 * =============================================================================
 * SERVICE NAMES
 * =============================================================================
 * All available service names in the system.
 */
export const ServiceNameEnum = z.enum([
  'api-gateway',
  'preprocessing-service',
  'feature-service',
  'prediction-service',
  'training-service',
  'explainability-service',
  'model-registry',
  'monitoring-service',
]);

/**
 * Type for service name values.
 */
export type ServiceName = z.infer<typeof ServiceNameEnum>;


/**
 * =============================================================================
 * SERVICE HEALTH SCHEMA
 * =============================================================================
 * Health status of a service.
 * Used for monitoring and load balancing.
 */
export const ServiceHealthSchema = z.object({
  /**
   * Service name.
   */
  service_name: ServiceNameEnum,

  /**
   * Service status.
   */
  status: z.enum(['healthy', 'degraded', 'unhealthy']),

  /**
   * Timestamp of health check.
   */
  checked_at: z.date().default(() => new Date()),

  /**
   * Response time in milliseconds.
   */
  response_time_ms: z.number().positive().optional(),

  /**
   * Dependencies and their health.
   */
  dependencies: z.record(
    z.string(),
    z.object({
      status: z.enum(['healthy', 'degraded', 'unhealthy']),
      message: z.string().optional(),
    })
  ).optional(),
});

/**
 * Type inferred from ServiceHealthSchema.
 */
export type ServiceHealth = z.infer<typeof ServiceHealthSchema>;


/**
 * =============================================================================
 * SERVICE STATUS SCHEMA
 * =============================================================================
 * Detailed status information.
 * Includes uptime, memory usage, and request counts.
 */
export const ServiceStatusSchema = z.object({
  /**
   * Service name.
   */
  service_name: ServiceNameEnum,

  /**
   * Service version.
   */
  version: z.string(),

  /**
   * Service uptime in seconds.
   */
  uptime_seconds: z.number().int().positive(),

  /**
   * Environment (development, staging, production).
   */
  environment: z.enum(['development', 'staging', 'production']).default('development'),

  /**
   * Request statistics.
   */
  requests: z.object({
    /**
     * Total requests served.
     */
    total: z.number().int().positive().default(0),
    /**
     * Requests in the last minute.
     */
    last_minute: z.number().int().positive().default(0),
    /**
     * Requests in the last hour.
     */
    last_hour: z.number().int().positive().default(0),
  }),

  /**
   * Memory usage information.
   */
  memory: z.object({
    /**
     * Used memory in bytes.
     */
    used_bytes: z.number().int().positive(),
    /**
     * Total available memory in bytes.
     */
    total_bytes: z.number().int().positive(),
    /**
     * Memory usage percentage.
     */
    usage_percent: z.number().min(0).max(100),
  }).optional(),

  /**
   * CPU usage percentage.
   */
  cpu_percent: z.number().min(0).max(100).optional(),

  /**
   * Additional custom metrics.
   */
  custom_metrics: z.record(z.string(), z.number()).optional(),

  /**
   * Timestamp when status was recorded.
   */
  recorded_at: z.date().default(() => new Date()),
});

/**
 * Type inferred from ServiceStatusSchema.
 */
export type ServiceStatus = z.infer<typeof ServiceStatusSchema>;


/**
 * =============================================================================
 * API ERROR SCHEMA
 * =============================================================================
 * Standardized error response.
 * Ensures consistent error formatting across services.
 */
export const ApiErrorSchema = z.object({
  /**
   * Error code for programmatic error handling.
   */
  error_code: z.string(),

  /**
   * Human-readable error message.
   */
  message: z.string(),

  /**
   * Detailed error description (for debugging).
   */
  details: z.record(z.string(), z.unknown()).optional(),

  /**
   * HTTP status code.
   */
  status_code: z.number().int().min(100).max(599),

  /**
   * Service that generated the error.
   */
  service: ServiceNameEnum.optional(),

  /**
   * Request ID for tracing.
   */
  request_id: z.string().uuid().optional(),

  /**
   * Timestamp when error occurred.
   */
  timestamp: z.date().default(() => new Date()),
});

/**
 * Type inferred from ApiErrorSchema.
 */
export type ApiError = z.infer<typeof ApiErrorSchema>;


/**
 * =============================================================================
 * PAGINATION PARAMETERS SCHEMA
 * =============================================================================
 * Pagination for list endpoints.
 * Standardizes paginated API responses.
 */
export const PaginationParamsSchema = z.object({
  /**
   * Page number (1-indexed).
   */
  page: z.number().int().positive().default(1),

  /**
   * Number of items per page.
   */
  limit: z.number().int().positive().max(100).default(20),

  /**
   * Sort field.
   */
  sort_by: z.string().optional(),

  /**
   * Sort order.
   */
  sort_order: z.enum(['asc', 'desc']).default('desc'),
});

/**
 * Type inferred from PaginationParamsSchema.
 */
export type PaginationParams = z.infer<typeof PaginationParamsSchema>;


/**
 * =============================================================================
 * PAGINATED RESPONSE SCHEMA
 * =============================================================================
 * Generic paginated response wrapper.
 */
export const PaginatedResponseSchema = z.object({
  /**
   * Array of items for current page.
   */
  items: z.array(z.unknown()),

  /**
   * Pagination metadata.
   */
  pagination: z.object({
    /**
     * Current page number.
     */
    page: z.number().int().positive(),
    /**
     * Items per page.
     */
    limit: z.number().int().positive(),
    /**
     * Total number of items.
     */
    total_items: z.number().int().positive(),
    /**
     * Total number of pages.
     */
    total_pages: z.number().int().positive(),
    /**
     * Whether there's a next page.
     */
    has_next: z.boolean(),
    /**
     * Whether there's a previous page.
     */
    has_prev: z.boolean(),
  }),
});

/**
 * Type inferred from PaginatedResponseSchema.
 */
export type PaginatedResponse<T> = z.infer<typeof PaginatedResponseSchema> & {
  items: T[];
};


/**
 * =============================================================================
 * SUCCESS RESPONSE SCHEMA
 * =============================================================================
 * Standard success response wrapper.
 */
export const SuccessResponseSchema = z.object({
  /**
   * Whether the operation was successful.
   */
  success: z.literal(true),

  /**
   * Response data.
   */
  data: z.unknown(),

  /**
   * Optional message.
   */
  message: z.string().optional(),

  /**
   * Request ID for tracing.
   */
  request_id: z.string().uuid().optional(),
});

/**
 * Type inferred from SuccessResponseSchema.
 */
export type SuccessResponse<T> = z.infer<typeof SuccessResponseSchema> & {
  data: T;
};


/**
 * =============================================================================
 * EXPORT ALL SERVICE SCHEMAS
 * =============================================================================
 */
export const ServiceSchemas = {
  name: ServiceNameEnum,
  health: ServiceHealthSchema,
  status: ServiceStatusSchema,
  error: ApiErrorSchema,
  pagination: PaginationParamsSchema,
  paginated_response: PaginatedResponseSchema,
  success_response: SuccessResponseSchema,
} as const;

export type ServiceSchemaName = keyof typeof ServiceSchemas;
