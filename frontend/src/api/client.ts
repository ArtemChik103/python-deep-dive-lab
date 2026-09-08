import type {
  EvaluationResponse,
  ExecutionResult,
  FileNode,
  HintItem,
  InstalledPackage,
  LessonDetail,
  ModuleItem,
  PopularPackage,
} from '../types';

const API_BASE = '/api';

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const errorText = await res.text();
    let message = `Request failed (${res.status})`;
    try {
      const errJson = JSON.parse(errorText);
      if (errJson.detail) {
        message = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail);
      }
    } catch {
      if (errorText) message = errorText;
    }
    throw new Error(message);
  }
  return res.json();
}

// Curriculum
export async function fetchModules(): Promise<{ modules: ModuleItem[]; total_modules: number }> {
  const res = await fetch(`${API_BASE}/curriculum/modules`);
  return handleResponse(res);
}

export async function fetchLesson(lessonId: string): Promise<LessonDetail> {
  const res = await fetch(`${API_BASE}/curriculum/lessons/${lessonId}`);
  return handleResponse(res);
}

export async function fetchHint(lessonId: string, level: number): Promise<HintItem> {
  const res = await fetch(`${API_BASE}/curriculum/lessons/${lessonId}/hints/${level}`);
  return handleResponse(res);
}

export async function fetchSolution(lessonId: string): Promise<{ lesson_id: string; solution: string; title: string }> {
  const res = await fetch(`${API_BASE}/curriculum/lessons/${lessonId}/solution`);
  return handleResponse(res);
}

export async function evaluateLesson(lessonId: string, code: string): Promise<EvaluationResponse> {
  const res = await fetch(`${API_BASE}/curriculum/lessons/${lessonId}/evaluate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code }),
  });
  return handleResponse(res);
}

// Execution
export async function executeCode(code: string): Promise<ExecutionResult> {
  const res = await fetch(`${API_BASE}/execute/code`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code }),
  });
  return handleResponse(res);
}

export async function executeFile(filePath: string): Promise<ExecutionResult> {
  const res = await fetch(`${API_BASE}/execute/file`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ file_path: filePath }),
  });
  return handleResponse(res);
}

// Files
export async function fetchFileTree(): Promise<{ files: FileNode[] }> {
  const res = await fetch(`${API_BASE}/files/tree`);
  return handleResponse(res);
}

export async function readFile(path: string): Promise<{ path: string; content: string }> {
  const res = await fetch(`${API_BASE}/files/read?path=${encodeURIComponent(path)}`);
  return handleResponse(res);
}

export async function saveFile(path: string, content: string): Promise<{ success: boolean; path: string; size: number }> {
  const res = await fetch(`${API_BASE}/files/save`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path, content }),
  });
  return handleResponse(res);
}

export async function createFileOrFolder(
  path: string,
  isDirectory: boolean = false,
  initialContent: string = ''
): Promise<{ success: boolean; path: string }> {
  const res = await fetch(`${API_BASE}/files/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path, is_directory: isDirectory, initial_content: initialContent }),
  });
  return handleResponse(res);
}

export async function renameFile(oldPath: string, newPath: string): Promise<{ success: boolean }> {
  const res = await fetch(`${API_BASE}/files/rename`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ old_path: oldPath, new_path: newPath }),
  });
  return handleResponse(res);
}

export async function deleteFile(path: string): Promise<{ success: boolean }> {
  const res = await fetch(`${API_BASE}/files/delete?path=${encodeURIComponent(path)}`, {
    method: 'DELETE',
  });
  return handleResponse(res);
}

export async function resetWorkspace(): Promise<{ success: boolean; files: FileNode[] }> {
  const res = await fetch(`${API_BASE}/files/reset-workspace`, {
    method: 'POST',
  });
  return handleResponse(res);
}

// Packages
export async function fetchInstalledPackages(): Promise<{ packages: InstalledPackage[]; total: number }> {
  const res = await fetch(`${API_BASE}/packages/list`);
  return handleResponse(res);
}

export async function fetchPopularPackages(): Promise<{ packages: PopularPackage[] }> {
  const res = await fetch(`${API_BASE}/packages/popular`);
  return handleResponse(res);
}

export async function installPackage(packageName: string): Promise<{ success: boolean; stdout: string; stderr: string; returncode: number }> {
  const res = await fetch(`${API_BASE}/packages/install`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ package: packageName }),
  });
  return handleResponse(res);
}

export async function uninstallPackage(packageName: string): Promise<{ success: boolean; stdout: string; stderr: string; returncode: number }> {
  const res = await fetch(`${API_BASE}/packages/uninstall`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ package: packageName }),
  });
  return handleResponse(res);
}
