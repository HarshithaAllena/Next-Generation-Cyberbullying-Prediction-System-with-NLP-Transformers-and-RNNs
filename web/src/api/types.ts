export interface ClassifyRequest {
  text: string
  include_explanation?: boolean
}

export interface ClassifyResponse {
  text_id: string
  predicted_label: string
  confidence: number
  probabilities: Record<string, number>
  is_high_confidence: boolean
  model_version: string
}
