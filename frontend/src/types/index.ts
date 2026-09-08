export type Difficulty = 'beginner' | 'intermediate' | 'advanced' | 'expert';

export interface LessonSummary {
  id: string;
  module_id: string;
  title: string;
  difficulty: Difficulty;
  estimated_minutes: number;
  hints_count: number;
  has_solution: boolean;
}

export interface ModuleItem {
  id: string;
  title: string;
  description: string;
  order: number;
  total_lessons: number;
  lessons: LessonSummary[];
}

export interface LessonDetail {
  id: string;
  module_id: string;
  module_title: string;
  title: string;
  difficulty: Difficulty;
  estimated_minutes: number;
  theory_md: string;
  task_description: string;
  starter_code: string;
  total_hints: number;
  has_solution: boolean;
}

export interface HintItem {
  lesson_id: string;
  level: number;
  title: string;
  content: string;
  total_hints: number;
}

export interface TestCaseResult {
  name: string;
  passed: boolean;
  expected: string | null;
  actual: string | null;
  error: string | null;
  duration_ms: number;
}

export interface EvaluationResponse {
  all_passed: boolean;
  total_tests: number;
  passed_tests: number;
  test_cases: TestCaseResult[];
  stdout: string;
  stderr: string;
  execution_time_ms: number;
  timed_out: boolean;
}

export interface ExecutionResult {
  stdout: string;
  stderr: string;
  returncode: number;
  timed_out: boolean;
  execution_time_ms: number;
  plots: string[];
}

export interface FileNode {
  name: string;
  path: string;
  is_directory: boolean;
  size?: number;
  children?: FileNode[];
}

export interface InstalledPackage {
  name: string;
  version: string;
}

export interface PopularPackage {
  name: string;
  description: string;
  category: string;
  docs_url: string;
}

export interface EditorTab {
  id: string;
  name: string;
  path: string;
  content: string;
  isDirty?: boolean;
  isLessonStarter?: boolean;
}
