export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}
export interface WelcomeMessage {
  message: string;
  suggestions: string[];
}

export interface UploadResponse {
  message: string;
  project_id: number;
  project_directory: string;
  welcome?: WelcomeMessage;
}